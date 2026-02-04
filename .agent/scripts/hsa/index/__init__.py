# HSA v5.0 Index Module
# =============================================================================
"""
Vector storage for HSA v5.0.

Tier 0: FAISS flat index (always available)
Tier 1: FAISS GPU acceleration
Tier 2: Qdrant (opt-in via HSA_QDRANT_URL)
"""

from .faiss_store import (
    FAISSStore,
    AdaptiveVectorStore,
    BaseVectorStore,
    VectorSearchResult,
    get_store,
)

from .qdrant_store import (
    QdrantConfig,
    QdrantStore,
    is_qdrant_enabled,
    get_qdrant_store,
)

__all__ = [
    # FAISS (Tier 0/1)
    "FAISSStore",
    "AdaptiveVectorStore",
    "BaseVectorStore",
    "VectorSearchResult",
    "get_store",
    # Qdrant (Tier 2)
    "QdrantConfig",
    "QdrantStore",
    "is_qdrant_enabled",
    "get_qdrant_store",
]

