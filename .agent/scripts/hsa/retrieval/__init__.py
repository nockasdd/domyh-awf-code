# HSA v5.0 Retrieval Module
# =============================================================================
"""
Retrieval module for HSA v5.0.

Includes HiRAG hierarchical retrieval, hybrid search, and @-mention parsing.
"""

from .hirag import (
    Entity,
    Relation,
    GraphContext,
    EntityExtractor,
    CommunityGraph,
    HiRAGRetriever,
    get_extractor,
    get_retriever,
)

from .hybrid import (
    FusionStrategy,
    HybridResult,
    HybridConfig,
    ScoreNormalizer,
    HybridSearchEngine,
    create_hybrid_engine,
)

from .mention import (
    MentionType,
    Mention,
    ParsedQuery,
    MentionParser,
    ContextBooster,
    get_parser,
    parse_query,
)

__all__ = [
    # HiRAG
    "Entity",
    "Relation", 
    "GraphContext",
    "EntityExtractor",
    "CommunityGraph",
    "HiRAGRetriever",
    "get_extractor",
    "get_retriever",
    # Hybrid Search
    "FusionStrategy",
    "HybridResult",
    "HybridConfig",
    "ScoreNormalizer",
    "HybridSearchEngine",
    "create_hybrid_engine",
    # Mention Parser
    "MentionType",
    "Mention",
    "ParsedQuery",
    "MentionParser",
    "ContextBooster",
    "get_parser",
    "parse_query",
]

