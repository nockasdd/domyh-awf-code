# HSA v5.0 - HiRAG Integration
# =============================================================================
"""
Hierarchical RAG integration for HSA v5.0.

This module bridges HSA v5.0 components with the HiRAG retrieval system
from HSA v5.0, providing enhanced entity extraction and retrieval.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger("hsa.hirag")


@dataclass
class Entity:
    """Code entity extracted from AST."""
    name: str
    type: str  # class, function, method, variable, import
    file_path: str
    start_line: int
    end_line: int
    docstring: Optional[str] = None
    signature: Optional[str] = None
    parent: Optional[str] = None  # Parent class/module name
    references: List[str] = field(default_factory=list)


@dataclass 
class Relation:
    """Relation between entities."""
    source: str
    target: str
    type: str  # calls, imports, inherits, uses, defines


@dataclass
class GraphContext:
    """Context from graph traversal."""
    global_summaries: List[str]
    bridge_paths: List[str]
    local_entities: List[Entity]
    retrieval_time_ms: float


class EntityExtractor:
    """
    Enhanced entity extraction using tree-sitter AST.
    
    Extracts:
    - Classes and their methods
    - Functions and their signatures
    - Import statements
    - Variable references
    - Call relationships
    """
    
    def __init__(self):
        self._parser = None
        self._cache: Dict[str, List[Entity]] = {}
    
    def _get_parser(self):
        """Lazy load parser."""
        if self._parser is None:
            from ..ast import get_parser
            self._parser = get_parser()
        return self._parser
    
    def extract(self, file_path: str, content: Optional[str] = None) -> List[Entity]:
        """Extract entities from a file."""
        from pathlib import Path
        
        # Check cache
        cache_key = file_path
        if content is None and cache_key in self._cache:
            return self._cache[cache_key]
        
        # Read file if content not provided
        if content is None:
            try:
                content = Path(file_path).read_text(encoding="utf-8")
            except Exception as e:
                logger.warning(f"Failed to read {file_path}: {e}")
                return []
        
        # Parse file
        parser = self._get_parser()
        result = parser.parse(content, file_path)
        
        entities = []
        
        for code_entity in result.entities:
            entity = Entity(
                name=code_entity.name,
                type=code_entity.type.value if hasattr(code_entity.type, 'value') else str(code_entity.type),
                file_path=file_path,
                start_line=code_entity.start_line,
                end_line=code_entity.end_line,
                docstring=code_entity.docstring,
                signature=code_entity.signature,
                parent=code_entity.parent,
            )
            entities.append(entity)
        
        # Cache result
        if content is None:
            self._cache[cache_key] = entities
        
        return entities
    
    def extract_relations(
        self, 
        file_path: str, 
        entities: List[Entity],
        content: Optional[str] = None
    ) -> List[Relation]:
        """Extract relations between entities."""
        from pathlib import Path
        
        relations = []
        
        # Read file if needed
        if content is None:
            try:
                content = Path(file_path).read_text(encoding="utf-8")
            except:
                return []
        
        # Build entity name set for reference detection
        entity_names = {e.name for e in entities}
        
        for entity in entities:
            # Check for inheritance (classes with bases)
            if entity.type == "class" and entity.signature:
                # Parse base classes from signature
                # e.g., "class Foo(Bar, Baz):" -> inherits Bar, Baz
                if "(" in entity.signature:
                    bases_part = entity.signature.split("(")[1].split(")")[0]
                    for base in bases_part.split(","):
                        base_name = base.strip()
                        if base_name and base_name in entity_names:
                            relations.append(Relation(
                                source=entity.name,
                                target=base_name,
                                type="inherits"
                            ))
            
            # Check for method calls within entity body
            if entity.parent and entity.parent in entity_names:
                relations.append(Relation(
                    source=entity.parent,
                    target=entity.name,
                    type="defines"
                ))
        
        return relations
    
    def clear_cache(self, file_path: Optional[str] = None) -> None:
        """Clear entity cache."""
        if file_path:
            self._cache.pop(file_path, None)
        else:
            self._cache.clear()


class CommunityGraph:
    """
    Graph-based community detection for code.
    
    Groups related entities into communities for:
    - Global context (community summaries)
    - Bridge context (cross-community paths)
    - Local context (entity details)
    """
    
    def __init__(self):
        self._entities: Dict[str, Entity] = {}
        self._relations: List[Relation] = []
        self._communities: Dict[int, Set[str]] = {}
        self._entity_to_community: Dict[str, int] = {}
        self._summaries: Dict[int, str] = {}
    
    def add_entity(self, entity: Entity) -> None:
        """Add entity to graph."""
        key = f"{entity.file_path}:{entity.name}"
        self._entities[key] = entity
    
    def add_relation(self, relation: Relation) -> None:
        """Add relation to graph."""
        self._relations.append(relation)
    
    def build_communities(self) -> None:
        """
        Build communities using Leiden algorithm.
        
        Falls back to simple file-based grouping if leidenalg not available.
        """
        try:
            self._build_leiden_communities()
        except ImportError:
            logger.info("leidenalg not available, using file-based communities")
            self._build_file_communities()
    
    def _build_leiden_communities(self) -> None:
        """Build communities using Leiden algorithm."""
        import leidenalg as la
        import igraph as ig
        
        # Build graph
        entity_names = list(self._entities.keys())
        name_to_idx = {name: i for i, name in enumerate(entity_names)}
        
        edges = []
        for rel in self._relations:
            src_key = None
            tgt_key = None
            
            # Find matching entity keys
            for key in entity_names:
                if key.endswith(f":{rel.source}"):
                    src_key = key
                if key.endswith(f":{rel.target}"):
                    tgt_key = key
            
            if src_key and tgt_key:
                edges.append((name_to_idx[src_key], name_to_idx[tgt_key]))
        
        G = ig.Graph(n=len(entity_names), edges=edges, directed=False)
        
        # Run Leiden
        partition = la.find_partition(G, la.ModularityVertexPartition)
        
        # Store results
        for community_id, members in enumerate(partition):
            self._communities[community_id] = {entity_names[i] for i in members}
            for i in members:
                self._entity_to_community[entity_names[i]] = community_id
    
    def _build_file_communities(self) -> None:
        """Simple file-based community grouping."""
        file_to_entities: Dict[str, Set[str]] = {}
        
        for key, entity in self._entities.items():
            if entity.file_path not in file_to_entities:
                file_to_entities[entity.file_path] = set()
            file_to_entities[entity.file_path].add(key)
        
        for i, (file_path, entities) in enumerate(file_to_entities.items()):
            self._communities[i] = entities
            for key in entities:
                self._entity_to_community[key] = i
    
    def generate_summaries(self) -> None:
        """Generate summaries for each community."""
        for community_id, members in self._communities.items():
            # Get entity types in this community
            types = set()
            names = []
            
            for key in members:
                entity = self._entities.get(key)
                if entity:
                    types.add(entity.type)
                    names.append(entity.name)
            
            # Generate simple summary
            type_str = ", ".join(sorted(types))
            name_str = ", ".join(sorted(names)[:5])
            if len(names) > 5:
                name_str += f"... (+{len(names) - 5} more)"
            
            self._summaries[community_id] = (
                f"Community {community_id}: {type_str} entities including {name_str}"
            )
    
    def get_community_summary(self, community_id: int) -> Optional[str]:
        """Get summary for a community."""
        return self._summaries.get(community_id)
    
    def get_entity_community(self, entity_name: str) -> Optional[int]:
        """Get community ID for an entity."""
        for key, community_id in self._entity_to_community.items():
            if key.endswith(f":{entity_name}"):
                return community_id
        return None
    
    def find_bridge_paths(
        self, 
        source_community: int, 
        target_community: int,
        max_hops: int = 3
    ) -> List[List[str]]:
        """Find paths between communities."""
        if source_community == target_community:
            return []
        
        # Simple BFS for cross-community paths
        source_entities = self._communities.get(source_community, set())
        target_entities = self._communities.get(target_community, set())
        
        paths = []
        
        for rel in self._relations:
            src_key = None
            tgt_key = None
            
            for key in self._entities:
                if key.endswith(f":{rel.source}"):
                    src_key = key
                if key.endswith(f":{rel.target}"):
                    tgt_key = key
            
            if src_key in source_entities and tgt_key in target_entities:
                paths.append([rel.source, f"--{rel.type}-->", rel.target])
        
        return paths[:5]  # Limit paths


class HiRAGRetriever:
    """
    Hierarchical RAG retriever for HSA v5.0.
    
    Implements 3-level retrieval:
    - Level 2 (GLOBAL): Community summaries
    - Level 1 (BRIDGE): Cross-community paths
    - Level 0 (LOCAL): Entity details + vector similarity
    """
    
    def __init__(self):
        self._extractor = EntityExtractor()
        self._graph = CommunityGraph()
        self._indexed = False
    
    def index_codebase(self, file_paths: List[str]) -> None:
        """Index codebase for retrieval."""
        start = time.time()
        
        all_entities = []
        
        for file_path in file_paths:
            entities = self._extractor.extract(file_path)
            all_entities.extend(entities)
            
            for entity in entities:
                self._graph.add_entity(entity)
            
            relations = self._extractor.extract_relations(file_path, entities)
            for rel in relations:
                self._graph.add_relation(rel)
        
        # Build communities
        self._graph.build_communities()
        self._graph.generate_summaries()
        
        self._indexed = True
        
        elapsed = (time.time() - start) * 1000
        logger.info(f"Indexed {len(all_entities)} entities from {len(file_paths)} files in {elapsed:.2f}ms")
    
    def retrieve(
        self,
        query_entities: List[str],
        k_global: int = 3,
        k_bridge: int = 3,
        k_local: int = 5
    ) -> GraphContext:
        """
        Retrieve hierarchical context.
        
        Args:
            query_entities: Entity names to query for
            k_global: Number of global summaries
            k_bridge: Number of bridge paths
            k_local: Number of local entities
        """
        start = time.time()
        
        # Find communities containing query entities
        query_communities = set()
        for name in query_entities:
            community = self._graph.get_entity_community(name)
            if community is not None:
                query_communities.add(community)
        
        # GLOBAL: Community summaries
        global_summaries = []
        for community_id in list(query_communities)[:k_global]:
            summary = self._graph.get_community_summary(community_id)
            if summary:
                global_summaries.append(summary)
        
        # BRIDGE: Cross-community paths
        bridge_paths = []
        community_list = list(query_communities)
        for i, c1 in enumerate(community_list):
            for c2 in community_list[i+1:]:
                paths = self._graph.find_bridge_paths(c1, c2)
                for path in paths[:k_bridge]:
                    bridge_paths.append(" ".join(path))
        
        # LOCAL: Entity details
        local_entities = []
        for name in query_entities:
            for key, entity in self._graph._entities.items():
                if key.endswith(f":{name}"):
                    local_entities.append(entity)
                    break
        
        elapsed = (time.time() - start) * 1000
        
        return GraphContext(
            global_summaries=global_summaries,
            bridge_paths=bridge_paths,
            local_entities=local_entities[:k_local],
            retrieval_time_ms=elapsed
        )


# Global instance
_extractor: Optional[EntityExtractor] = None
_retriever: Optional[HiRAGRetriever] = None


def get_extractor() -> EntityExtractor:
    """Get global entity extractor."""
    global _extractor
    if _extractor is None:
        _extractor = EntityExtractor()
    return _extractor


def get_retriever() -> HiRAGRetriever:
    """Get global HiRAG retriever."""
    global _retriever
    if _retriever is None:
        _retriever = HiRAGRetriever()
    return _retriever
