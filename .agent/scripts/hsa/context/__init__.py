# HSA Context Management Module
# =============================================================================
"""
Context management for HSA.

Components:
- TokenBudgetManager: Manage token allocation
- ContextGC: Garbage collection for context items
- SmartTruncator: Intelligent truncation strategies
"""

from .token_budget import (
    TokenBudgetManager,
    BudgetCategory,
    AllocationRequest,
    Allocation,
    BudgetSnapshot,
    allocate_tokens,
)

from .context_gc import (
    ContextGC,
    ContextItem,
    ContextItemType,
    GCStats,
)

from .smart_truncation import (
    SmartTruncator,
    TruncationStrategy,
    TruncationResult,
    truncate_smart,
)

__all__ = [
    # Token Budget
    "TokenBudgetManager",
    "BudgetCategory",
    "AllocationRequest",
    "Allocation",
    "BudgetSnapshot",
    "allocate_tokens",
    # Context GC
    "ContextGC",
    "ContextItem",
    "ContextItemType",
    "GCStats",
    # Smart Truncation
    "SmartTruncator",
    "TruncationStrategy",
    "TruncationResult",
    "truncate_smart",
]
