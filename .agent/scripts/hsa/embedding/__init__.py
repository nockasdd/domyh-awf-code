# HSA v5.0 Embedding Module
# =============================================================================
"""
Code embeddings for HSA v5.0.

Tier 0: CodeSage V2 Base on CPU
Tier 1: CodeSage V2 Large on GPU with INT8
Tier 2: VoyageCode3 API (opt-in via VOYAGE_API_KEY)
"""

from .codesage import (
    CodeSageEmbedder,
    BM25PseudoEmbedder,
    VoyageAPIEmbedder,
    AdaptiveEmbedder,
    BaseEmbedder,
    EmbeddingResult,
    get_embedder,
    embed,
    embed_single,
)

from .voyage import (
    VoyageConfig,
    VoyageEmbedder,
    UsageStats,
    RateLimiter,
    is_voyage_enabled,
    get_voyage_embedder,
    should_use_voyage,
    RARE_LANGUAGES,
)

__all__ = [
    # CodeSage (Tier 0/1)
    "CodeSageEmbedder",
    "BM25PseudoEmbedder",
    "VoyageAPIEmbedder",
    "AdaptiveEmbedder",
    "BaseEmbedder",
    "EmbeddingResult",
    "get_embedder",
    "embed",
    "embed_single",
    # VoyageAI (Tier 2)
    "VoyageConfig",
    "VoyageEmbedder",
    "UsageStats",
    "RateLimiter",
    "is_voyage_enabled",
    "get_voyage_embedder",
    "should_use_voyage",
    "RARE_LANGUAGES",
]

