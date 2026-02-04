# HSA v5.0 Tokenizer Module
# =============================================================================
"""
Accurate token counting using tiktoken.

This module provides the P0 critical fix for token counting accuracy.
"""

from .accurate import (
    AccurateTokenCounter,
    count_tokens,
    count_tokens_batch,
    truncate_to_tokens,
    estimate_tokens,
    get_counter,
    rough_token_count,  # DEPRECATED
)

__all__ = [
    "AccurateTokenCounter",
    "count_tokens",
    "count_tokens_batch", 
    "truncate_to_tokens",
    "estimate_tokens",
    "get_counter",
]
