# =============================================================================
# hirag_retriever.py — Hierarchical RAG Context Retriever
# =============================================================================
# HSA v5.0 - Phase 3: HiRAG Integration
# Implements 3-level hierarchical context retrieval
# =============================================================================

"""
HiRAG Retriever Module

Implements the core HiRAG (Hierarchical RAG) architecture from research.
Combines three levels of context:

1. Global Context (Community Summaries)
   - High-level abstractions of code clusters
   - Useful for understanding overall architecture
   
2. Bridge Context (Shortest Paths)
   - Connections between different communities
   - Useful for understanding cross-cutting concerns
   
3. Local Context (Entity Details)
   - Specific code elements and their relations
   - Useful for precise implementation details

Research shows this approach achieves:
- 30% better coherence than flat retrieval
- 20% improvement in factual accuracy
- Significant reduction in hallucinations
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path
from typing import Any, Callable, Dict, Iterator, List, Optional, Set, Tuple, Union

from .community_graph import CommunityGraph, Entity, Relation
from .bridge_finder import BridgeFinder, Bridge, BridgeContext


@dataclass
class RetrievalContext:
    """Combined context from all three levels."""
    
    # Global: Community summaries
    global_context: List[Dict[str, Any]] = field(default_factory=list)
    
    # Bridge: Cross-community paths
    bridge_context: Optional[BridgeContext] = None
    
    # Local: Entity details
    local_context: List[Dict[str, Any]] = field(default_factory=list)
    
    # Metadata
    query: str = ""
    retrieval_time_ms: float = 0.0
    
    @property
    def total_entities(self) -> int:
        """Total unique entities in context."""
        entity_ids = set()
        
        for item in self.local_context:
            entity_ids.add(item.get("id", ""))
        
        if self.bridge_context:
            entity_ids.update(self.bridge_context.bridge_entity_ids)
        
        return len(entity_ids)
    
    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "query": self.query,
            "global_context": self.global_context,
            "bridge_context": self.bridge_context.to_dict() if self.bridge_context else None,
            "local_context": self.local_context,
            "total_entities": self.total_entities,
            "retrieval_time_ms": self.retrieval_time_ms
        }
    
    def to_text(self, include_global: bool = True) -> str:
        """
        Convert context to human-readable text for LLM consumption.
        
        Returns formatted text suitable for context injection.
        """
        parts = []
        
        # Global context
        if include_global and self.global_context:
            parts.append("## Global Context (High-Level Overview)")
            for item in self.global_context:
                parts.append(f"### {item.get('name', 'Unknown')}")
                parts.append(f"- **Size**: {item.get('size', 0)} entities")
                parts.append(f"- **Summary**: {item.get('summary', 'No summary')}")
                sample = item.get('entity_ids', [])[:3]
                if sample:
                    parts.append(f"- **Sample**: {', '.join(sample)}")
                parts.append("")
        
        # Bridge context
        if self.bridge_context and self.bridge_context.bridges:
            parts.append("## Bridge Context (Cross-Cutting Connections)")
            for bridge in self.bridge_context.bridges:
                parts.append(f"- **Path**: {' → '.join(bridge.path[:5])}")
                parts.append(f"  - Distance: {bridge.distance:.2f}")
                if bridge.bridge_entities:
                    parts.append(f"  - Bridges: {', '.join(bridge.bridge_entities[:3])}")
            parts.append("")
        
        # Local context
        if self.local_context:
            parts.append("## Local Context (Specific Details)")
            for item in self.local_context:
                parts.append(f"### {item.get('name', 'Unknown')} ({item.get('type', 'entity')})")
                if item.get('description'):
                    parts.append(f"- **Description**: {item['description']}")
                if item.get('outgoing'):
                    deps = [f"{r['target']} ({r['type']})" for r in item['outgoing'][:3]]
                    parts.append(f"- **Dependencies**: {', '.join(deps)}")
                parts.append("")
        
        return "\n".join(parts)


class CodebaseExtractor:
    """
    Extracts code entities and relations from a codebase.
    
    Scans source files to build a knowledge graph of:
    - Files, functions, classes, modules
    - Import/call/extend relationships
    """
    
    # Default ignore patterns
    DEFAULT_IGNORE = {
        "node_modules", ".git", "__pycache__", "venv", ".venv",
        "dist", "build", ".next", "coverage", ".pytest_cache"
    }
    
    # Supported extensions and their entity extractors
    EXTRACTORS = {
        ".py": "_extract_python",
        ".js": "_extract_javascript",
        ".ts": "_extract_typescript",
        ".go": "_extract_go",
    }
    
    def __init__(
        self,
        root_path: Union[str, Path],
        ignore_patterns: Optional[Set[str]] = None,
        max_depth: int = 5
    ):
        """
        Initialize the extractor.
        
        Args:
            root_path: Project root directory
            ignore_patterns: Directories to ignore
            max_depth: Maximum depth to traverse
        """
        self.root_path = Path(root_path).resolve()
        self.ignore_patterns = ignore_patterns or self.DEFAULT_IGNORE
        self.max_depth = max_depth
    
    def extract_to_graph(self) -> CommunityGraph:
        """
        Extract entities and relations into a CommunityGraph.
        
        Returns:
            CommunityGraph populated with codebase entities
        """
        graph = CommunityGraph()
        
        # First pass: collect all files as entities
        for file_path in self._iter_files():
            rel_path = file_path.relative_to(self.root_path)
            entity_id = str(rel_path).replace("\\", "/")
            
            graph.add_entity(Entity(
                id=entity_id,
                name=file_path.stem,
                entity_type="file",
                description=f"File: {rel_path}",
                metadata={"extension": file_path.suffix, "path": str(rel_path)}
            ))
        
        # Second pass: extract relations (imports)
        for file_path in self._iter_files():
            rel_path = file_path.relative_to(self.root_path)
            source_id = str(rel_path).replace("\\", "/")
            
            # Extract imports based on file type
            extractor_name = self.EXTRACTORS.get(file_path.suffix)
            if extractor_name:
                extractor = getattr(self, extractor_name, None)
                if extractor:
                    try:
                        imports = extractor(file_path)
                        for imp in imports:
                            # Try to resolve import to an entity
                            target_id = self._resolve_import(imp, file_path)
                            if target_id and target_id in graph.entities:
                                try:
                                    graph.add_relation(Relation(
                                        source_id=source_id,
                                        target_id=target_id,
                                        relation_type="imports",
                                        weight=1.0
                                    ))
                                except ValueError:
                                    pass
                    except Exception:
                        pass  # Skip files that fail to parse
        
        return graph
    
    def _iter_files(self) -> Iterator[Path]:
        """Iterate over source files."""
        def walk(path: Path, depth: int = 0):
            if depth > self.max_depth:
                return
            
            try:
                for child in path.iterdir():
                    if child.name in self.ignore_patterns:
                        continue
                    if child.name.startswith("."):
                        continue
                    
                    if child.is_file():
                        if child.suffix in self.EXTRACTORS:
                            yield child
                    elif child.is_dir():
                        yield from walk(child, depth + 1)
            except PermissionError:
                pass
        
        yield from walk(self.root_path)
    
    def _extract_python(self, file_path: Path) -> List[str]:
        """Extract Python imports."""
        imports = []
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("import "):
                    # import foo, bar
                    parts = line[7:].split(",")
                    for part in parts:
                        mod = part.strip().split(" as ")[0].split(".")[0]
                        if mod:
                            imports.append(mod)
                elif line.startswith("from "):
                    # from foo import bar
                    parts = line[5:].split(" import ")
                    if parts:
                        mod = parts[0].strip().split(".")[0]
                        if mod and not mod.startswith("."):
                            imports.append(mod)
        except Exception:
            pass
        return imports
    
    def _extract_javascript(self, file_path: Path) -> List[str]:
        """Extract JavaScript/TypeScript imports."""
        imports = []
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            for line in content.split("\n"):
                line = line.strip()
                # import ... from '...'
                if "from " in line and ("import " in line or "require(" in line):
                    # Find the quoted module
                    for quote in ['"', "'"]:
                        if quote in line:
                            parts = line.split(quote)
                            if len(parts) >= 2:
                                mod = parts[1]
                                if mod and not mod.startswith(".") and not mod.startswith("@"):
                                    imports.append(mod.split("/")[0])
                                break
        except Exception:
            pass
        return imports
    
    _extract_typescript = _extract_javascript
    
    def _extract_go(self, file_path: Path) -> List[str]:
        """Extract Go imports."""
        imports = []
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            in_import = False
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("import ("):
                    in_import = True
                elif in_import:
                    if line == ")":
                        in_import = False
                    elif '"' in line:
                        mod = line.split('"')[1] if '"' in line else ""
                        if mod:
                            imports.append(mod.split("/")[-1])
                elif line.startswith("import ") and '"' in line:
                    mod = line.split('"')[1] if '"' in line else ""
                    if mod:
                        imports.append(mod.split("/")[-1])
        except Exception:
            pass
        return imports
    
    def _resolve_import(self, import_name: str, from_file: Path) -> Optional[str]:
        """Resolve import name to entity ID."""
        # Try to find a matching file
        parent = from_file.parent
        
        # Check for local file
        for ext in [".py", ".js", ".ts", ".go"]:
            candidate = parent / f"{import_name}{ext}"
            if candidate.exists():
                return str(candidate.relative_to(self.root_path)).replace("\\", "/")
        
        # Check for package/directory
        candidate = parent / import_name
        if candidate.is_dir():
            for init in ["__init__.py", "index.js", "index.ts", "main.go"]:
                init_file = candidate / init
                if init_file.exists():
                    return str(init_file.relative_to(self.root_path)).replace("\\", "/")
        
        return None


class HiRAGRetriever:
    """
    Hierarchical RAG context retriever.
    
    Combines global, bridge, and local context for optimal
    LLM context injection.
    
    Usage:
        # Initialize
        retriever = HiRAGRetriever.from_project("/path/to/project")
        
        # Retrieve context
        context = retriever.retrieve(
            query_entities=["main.py", "utils.py"],
            k_global=3,
            k_local=5
        )
        
        # Use context
        print(context.to_text())
    """
    
    def __init__(
        self,
        graph: CommunityGraph,
        cache_path: Optional[Union[str, Path]] = None
    ):
        """
        Initialize the retriever.
        
        Args:
            graph: Pre-built CommunityGraph
            cache_path: Path to cache graph state
        """
        self.graph = graph
        self.bridge_finder = BridgeFinder(graph)
        self.cache_path = Path(cache_path) if cache_path else None
        
        # Ensure communities are detected
        if graph.community_count == 0:
            graph.detect_communities()
    
    @classmethod
    def from_project(
        cls,
        project_path: Union[str, Path],
        cache_path: Optional[Union[str, Path]] = None,
        force_rebuild: bool = False
    ) -> "HiRAGRetriever":
        """
        Create retriever from a project directory.
        
        Args:
            project_path: Path to project root
            cache_path: Path to cache graph state
            force_rebuild: Force rebuild even if cache exists
            
        Returns:
            Initialized HiRAGRetriever
        """
        project_path = Path(project_path).resolve()
        
        # Check cache
        if cache_path and not force_rebuild:
            cache_path = Path(cache_path)
            if cache_path.exists():
                try:
                    graph = CommunityGraph.load(cache_path)
                    return cls(graph, cache_path)
                except Exception:
                    pass
        
        # Extract graph from project
        extractor = CodebaseExtractor(project_path)
        graph = extractor.extract_to_graph()
        
        # Detect communities
        graph.detect_communities()
        
        # Save cache
        if cache_path:
            try:
                graph.save(cache_path)
            except Exception:
                pass
        
        return cls(graph, cache_path)
    
    def retrieve(
        self,
        query_entities: List[str],
        k_global: int = 3,
        k_bridge: int = 3,
        k_local: int = 5,
        include_neighbors: bool = True
    ) -> RetrievalContext:
        """
        Retrieve hierarchical context for given entities.
        
        Args:
            query_entities: Entity IDs to build context around
            k_global: Number of global contexts (community summaries)
            k_bridge: Maximum bridge paths
            k_local: Number of local entity details
            include_neighbors: Include 1-hop neighbors in local context
            
        Returns:
            RetrievalContext with all three levels
        """
        start_time = time.perf_counter()
        
        # 1. Global Context - Community summaries
        global_ctx = self.graph.get_global_context(k=k_global)
        
        # 2. Bridge Context - Cross-community paths
        bridge_ctx = None
        if len(query_entities) >= 2:
            bridge_ctx = self.bridge_finder.get_bridge_context(
                query_entities,
                max_bridges=k_bridge
            )
        
        # 3. Local Context - Entity details
        local_entities = list(query_entities)
        
        if include_neighbors:
            for entity_id in query_entities:
                neighbors = self.graph.get_neighbors(entity_id)
                local_entities.extend(list(neighbors)[:2])
        
        # Deduplicate while preserving order
        seen = set()
        unique_local = []
        for eid in local_entities:
            if eid not in seen:
                seen.add(eid)
                unique_local.append(eid)
        
        local_ctx = self.graph.get_local_context(unique_local, k=k_local)
        
        # Calculate time
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        
        return RetrievalContext(
            global_context=global_ctx,
            bridge_context=bridge_ctx,
            local_context=local_ctx,
            query=f"entities: {query_entities}",
            retrieval_time_ms=elapsed_ms
        )
    
    def refresh(self, project_path: Optional[Union[str, Path]] = None) -> None:
        """
        Refresh the graph from the project.
        
        Args:
            project_path: Project path (uses cache path parent if not specified)
        """
        if project_path is None and self.cache_path:
            project_path = self.cache_path.parent
        
        if project_path is None:
            return
        
        extractor = CodebaseExtractor(project_path)
        self.graph = extractor.extract_to_graph()
        self.graph.detect_communities()
        self.bridge_finder = BridgeFinder(self.graph)
        
        if self.cache_path:
            try:
                self.graph.save(self.cache_path)
            except Exception:
                pass


# =============================================================================
# _DOMYH Awesome Code v6.1.2 • HSA v5.0 • HiRAG Retriever_
# =============================================================================
