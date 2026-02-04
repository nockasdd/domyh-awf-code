# HSA — Hierarchical Skills Architecture
# =============================================================================
"""
HSA (Hierarchical Skills Architecture) — Unified Module

A SOLID-compliant, progressive enhancement architecture for context management.

## Architecture Tiers

- **Tier 0 (Baseline)**: Works on ANY machine, zero config
- **Tier 1 (GPU)**: Auto-detected when GPU available
- **Tier 2 (Distributed)**: Opt-in via environment variables

## Usage

```python
from hsa import HSAEngine, get_context

# Quick API
context = get_context(
    query_files=["main.py", "utils.py"],
    max_tokens=8000
)

# Full engine
engine = HSAEngine.from_project("/path/to/project")
result = engine.get_context(query="handle authentication")
```
"""

__version__ = "1.0.0"
__author__ = "NockDev"

# =============================================================================
# Lazy Import System
# =============================================================================
# To prevent circular imports and improve startup time, we use lazy imports
# for optional/heavy modules.

import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Type hints only - not executed at runtime
    from .core import (
        SystemCapabilities, GPUInfo, AutoConfig, DeploymentTier,
        MemoryStats, MemoryBudget, GPUMemoryManager,
        CircuitBreaker, RetryHandler, StreamController,
    )
    from .tokenizer import AccurateTokenCounter
    from .cache import LRUCache, CacheStats
    from .search import BM25Index, SearchResult
    from .index import FAISSStore, BaseVectorStore
    from .embedding import CodeSageEmbedder, BaseEmbedder
    from .ast import TreeSitterParser, ParseResult
    from .retrieval import HiRAGRetriever, Entity, Relation
    from .engine import HSAEngine, EngineConfig, ContextResult


# =============================================================================
# Core Exports (Eagerly Loaded)
# =============================================================================
# Engine is the main entry point, always load it
from .engine import (
    HSAEngine,
    EngineConfig,
    ContextResult,
    get_engine,
    get_context,
)


# =============================================================================
# Submodule Accessors
# =============================================================================
# These allow `from hsa import core` etc. without eager loading

def __getattr__(name: str):
    """Lazy import for submodules."""
    modules = {
        "core": ".core",
        "tokenizer": ".tokenizer",
        "cache": ".cache",
        "search": ".search",
        "index": ".index",
        "embedding": ".embedding",
        "ast": ".ast",
        "retrieval": ".retrieval",
        "daemon": ".daemon",
        "context": ".context",
        "detection": ".detection",
        "merkle": ".merkle",
        "prefetch": ".prefetch",
        "engine": ".engine",
    }
    
    if name in modules:
        import importlib
        return importlib.import_module(modules[name], package=__name__)
    
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


# =============================================================================
# Public API
# =============================================================================
__all__ = [
    # Version
    "__version__",
    # Engine (main entry point)
    "HSAEngine",
    "EngineConfig",
    "ContextResult",
    "get_engine",
    "get_context",
    # Submodules (lazy loaded)
    "core",
    "tokenizer",
    "cache",
    "search",
    "index",
    "embedding",
    "ast",
    "retrieval",
    "daemon",
    "context",
    "detection",
    "merkle",
    "prefetch",
    "engine",
]
