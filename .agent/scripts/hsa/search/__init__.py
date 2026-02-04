# HSA v5.0 Search Module
# =============================================================================
"""
Search functionality for HSA v5.0.

Tier 0: BM25 keyword search (always available)
"""

from .bm25 import (
    BM25Index,
    SearchResult,
    IndexStats,
    CodeTokenizer,
    get_index,
    search,
)

__all__ = [
    "BM25Index",
    "SearchResult",
    "IndexStats",
    "CodeTokenizer",
    "get_index",
    "search",
]
