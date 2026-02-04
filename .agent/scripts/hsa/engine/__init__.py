# HSA Engine Module
# =============================================================================
"""
Unified HSA Engine - Main Orchestrator.

Combines best of v4 and v5:
- v4: Token budget, GC, prefetching, Merkle change detection
- v5: Progressive enhancement, GPU auto-detect, HiRAG

SOLID Principles:
- Facade Pattern: Simplified interface to complex subsystems
- Dependency Inversion: Depends on abstractions, uses factory functions
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Import from unified modules (not v4/v5)
# Note: These will work after the full migration is complete
# For now, we'll use a hybrid approach


@dataclass
class EngineConfig:
    """Configuration for HSA Engine."""
    
    # Token budget
    total_capacity: int = 128000
    safety_margin: float = 0.90
    
    # HiRAG
    k_global: int = 3
    k_bridge: int = 3
    k_local: int = 5
    
    # GC
    gc_threshold: float = 0.85
    gc_target: float = 0.70
    
    # Prefetching
    prefetch_count: int = 3
    prefetch_min_prob: float = 0.1
    
    # Caching
    cache_dir: Optional[Path] = None
    
    # Tier auto-detection
    auto_tier: bool = True
    force_tier: Optional[int] = None  # 0, 1, or 2
    
    @classmethod
    def from_yaml(cls, path: Path) -> "EngineConfig":
        """Load config from YAML file."""
        import yaml
        data = yaml.safe_load(path.read_text())
        return cls(**data.get("engine", {}))
    
    @classmethod
    def default(cls) -> "EngineConfig":
        """Get default configuration."""
        return cls()


@dataclass
class ContextResult:
    """Result of context retrieval."""
    
    # Retrieved content
    content: str = ""
    
    # Metadata
    files_included: List[str] = field(default_factory=list)
    tokens_used: int = 0
    tokens_available: int = 0
    
    # Performance
    retrieval_time_ms: float = 0.0
    cache_hit: bool = False
    
    # Tier info
    tier_used: int = 0
    tier_name: str = "baseline"
    
    def to_text(self) -> str:
        """Convert to text format for context injection."""
        return self.content
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "content": self.content,
            "files": self.files_included,
            "tokens_used": self.tokens_used,
            "tokens_available": self.tokens_available,
            "retrieval_time_ms": self.retrieval_time_ms,
            "cache_hit": self.cache_hit,
            "tier": self.tier_name,
        }


class HSAEngine:
    """
    Unified HSA Engine.
    
    Facade that orchestrates all HSA components with progressive enhancement.
    
    Usage:
        # Quick start
        engine = HSAEngine.from_project("/path/to/project")
        context = engine.get_context(query="implement auth")
        
        # With config
        config = EngineConfig(total_capacity=64000)
        engine = HSAEngine(config)
        engine.initialize("/path/to/project")
    """
    
    def __init__(self, config: Optional[EngineConfig] = None):
        self.config = config or EngineConfig.default()
        self._project_root: Optional[Path] = None
        self._initialized = False
        self._tier: int = 0
        
        # Components (lazy initialized)
        self._detector = None
        self._embedder = None
        self._index = None
        self._cache = None
        self._retriever = None
        self._budget_manager = None
        self._gc = None
        self._prefetcher = None
        self._merkle = None
    
    @classmethod
    def from_project(
        cls,
        project_path: Union[str, Path],
        config: Optional[EngineConfig] = None
    ) -> "HSAEngine":
        """Create engine from project path."""
        engine = cls(config)
        engine.initialize(project_path)
        return engine
    
    def initialize(self, project_path: Union[str, Path]) -> None:
        """Initialize engine with project."""
        self._project_root = Path(project_path).resolve()
        
        # Detect tier
        if self.config.auto_tier:
            self._tier = self._detect_tier()
        elif self.config.force_tier is not None:
            self._tier = self.config.force_tier
        
        # Initialize components based on tier
        self._init_components()
        self._initialized = True
    
    def _detect_tier(self) -> int:
        """Detect available tier."""
        try:
            # Check for Tier 2 (Distributed)
            import os
            if os.getenv("HSA_QDRANT_URL") or os.getenv("HSA_REDIS_URL"):
                return 2
            
            # Check for Tier 1 (GPU)
            try:
                import torch
                if torch.cuda.is_available():
                    return 1
            except ImportError:
                pass
            
            # Default to Tier 0 (Baseline)
            return 0
            
        except Exception:
            return 0
    
    def _init_components(self) -> None:
        """Initialize components for current tier."""
        # Always initialize Tier 0 components
        self._init_tier0()
        
        if self._tier >= 1:
            self._init_tier1()
        
        if self._tier >= 2:
            self._init_tier2()
    
    def _init_tier0(self) -> None:
        """Initialize Tier 0 (Baseline) components."""
        # These will use hsa.* imports after full migration
        pass
    
    def _init_tier1(self) -> None:
        """Initialize Tier 1 (GPU) components."""
        pass
    
    def _init_tier2(self) -> None:
        """Initialize Tier 2 (Distributed) components."""
        pass
    
    def get_context(
        self,
        query: Optional[str] = None,
        query_files: Optional[List[str]] = None,
        max_tokens: Optional[int] = None,
    ) -> ContextResult:
        """
        Get optimized context for query or files.
        
        Args:
            query: Natural language query
            query_files: List of file paths to include
            max_tokens: Maximum tokens to use
            
        Returns:
            ContextResult with retrieved content and metadata
        """
        if not self._initialized:
            raise RuntimeError("Engine not initialized. Call initialize() first.")
        
        start_time = time.time()
        
        max_tokens = max_tokens or int(
            self.config.total_capacity * self.config.safety_margin
        )
        
        # Build context (simplified for now)
        content_parts = []
        files_included = []
        tokens_used = 0
        
        if query_files:
            for file_path in query_files:
                full_path = self._project_root / file_path
                if full_path.exists():
                    try:
                        content = full_path.read_text(encoding="utf-8")
                        content_parts.append(f"# {file_path}\n```\n{content}\n```\n")
                        files_included.append(file_path)
                        # Rough token estimate (will use accurate counter later)
                        tokens_used += len(content) // 4
                    except Exception:
                        pass
        
        elapsed_ms = (time.time() - start_time) * 1000
        
        tier_names = {0: "baseline", 1: "gpu", 2: "distributed"}
        
        return ContextResult(
            content="\n".join(content_parts),
            files_included=files_included,
            tokens_used=tokens_used,
            tokens_available=max_tokens - tokens_used,
            retrieval_time_ms=elapsed_ms,
            cache_hit=False,
            tier_used=self._tier,
            tier_name=tier_names.get(self._tier, "unknown"),
        )
    
    def detect_stack(self) -> Dict[str, Any]:
        """Detect project tech stack."""
        if not self._initialized:
            raise RuntimeError("Engine not initialized. Call initialize() first.")
        
        # Will use hsa.detection after migration
        return {
            "project_root": str(self._project_root),
            "detected": True,
        }
    
    def check_changes(self) -> Dict[str, Any]:
        """Check for file changes since last check."""
        if not self._initialized:
            raise RuntimeError("Engine not initialized. Call initialize() first.")
        
        # Will use hsa.merkle after migration
        return {
            "changed_files": [],
            "added_files": [],
            "deleted_files": [],
        }
    
    @property
    def tier(self) -> int:
        """Get current tier."""
        return self._tier
    
    @property
    def tier_name(self) -> str:
        """Get current tier name."""
        return {0: "baseline", 1: "gpu", 2: "distributed"}.get(self._tier, "unknown")


# =============================================================================
# Module-level convenience functions
# =============================================================================

_engine_instance: Optional[HSAEngine] = None


def get_engine() -> HSAEngine:
    """Get or create singleton engine instance."""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = HSAEngine()
    return _engine_instance


def get_context(
    query_files: Optional[List[str]] = None,
    query: Optional[str] = None,
    max_tokens: int = 8000,
    project_path: Optional[Union[str, Path]] = None,
) -> ContextResult:
    """
    Quick API for getting context.
    
    Usage:
        from hsa import get_context
        
        context = get_context(
            query_files=["main.py", "utils.py"],
            max_tokens=8000
        )
        print(context.to_text())
    """
    engine = get_engine()
    
    if project_path and not engine._initialized:
        engine.initialize(project_path)
    elif not engine._initialized:
        # Use current directory
        engine.initialize(Path.cwd())
    
    return engine.get_context(
        query=query,
        query_files=query_files,
        max_tokens=max_tokens,
    )


__all__ = [
    "HSAEngine",
    "EngineConfig",
    "ContextResult",
    "get_engine",
    "get_context",
]
