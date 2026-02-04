# =============================================================================
# token_budget.py — Adaptive Token Budget Manager
# =============================================================================
# HSA v5.0 - Phase 4: Token Budget & GC
# Implements dynamic token allocation based on task complexity
# =============================================================================

"""
Token Budget Module

Implements adaptive token budget management with:
- Base allocation per category (system, skills, context)
- Dynamic expansion up to safety margin
- Priority-based allocation for competing requests

From HSA_V4.yaml spec:
- base_context: 2000 tokens
- per_skill: 1500 tokens  
- max_skills: 5
- safety_margin: 90%
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple


class BudgetCategory(Enum):
    """Categories for token budget allocation."""
    SYSTEM = auto()      # System prompts, rules
    SKILLS = auto()      # Loaded skills
    CONTEXT = auto()     # Retrieved context (HiRAG)
    HISTORY = auto()     # Conversation history
    RESPONSE = auto()    # Reserved for response
    BUFFER = auto()      # Safety buffer


@dataclass
class AllocationRequest:
    """Request for token allocation."""
    category: BudgetCategory
    requested_tokens: int
    priority: int = 5  # 1-10, higher = more important
    source: str = ""   # Identifier for debugging
    shrinkable: bool = True  # Can be reduced if over budget
    
    def __repr__(self) -> str:
        return f"Request({self.category.name}, {self.requested_tokens}, pri={self.priority})"


@dataclass
class Allocation:
    """Granted token allocation."""
    category: BudgetCategory
    allocated_tokens: int
    requested_tokens: int
    source: str = ""
    
    @property
    def utilization(self) -> float:
        """How much of request was fulfilled."""
        if self.requested_tokens == 0:
            return 1.0
        return self.allocated_tokens / self.requested_tokens
    
    @property
    def was_reduced(self) -> bool:
        return self.allocated_tokens < self.requested_tokens


@dataclass
class BudgetSnapshot:
    """Snapshot of current budget state."""
    total_capacity: int
    total_allocated: int
    allocations: Dict[BudgetCategory, int]
    timestamp: float = field(default_factory=time.time)
    
    @property
    def remaining(self) -> int:
        return self.total_capacity - self.total_allocated
    
    @property
    def utilization(self) -> float:
        if self.total_capacity == 0:
            return 0.0
        return self.total_allocated / self.total_capacity
    
    def to_dict(self) -> dict:
        return {
            "total_capacity": self.total_capacity,
            "total_allocated": self.total_allocated,
            "remaining": self.remaining,
            "utilization": f"{self.utilization:.1%}",
            "allocations": {
                cat.name: tokens for cat, tokens in self.allocations.items()
            }
        }


class TokenBudgetManager:
    """
    Adaptive token budget manager.
    
    Features:
    - Category-based allocation (system, skills, context, etc.)
    - Priority-based arbitration when over budget
    - Dynamic expansion with safety margins
    - Allocation tracking and reporting
    
    Usage:
        manager = TokenBudgetManager(total_capacity=128000)
        
        # Request allocations
        alloc = manager.allocate(AllocationRequest(
            category=BudgetCategory.SKILLS,
            requested_tokens=4500,
            priority=8,
            source="typescript-skill"
        ))
        
        print(f"Allocated: {alloc.allocated_tokens}")
        
        # Check budget
        snapshot = manager.get_snapshot()
        print(f"Remaining: {snapshot.remaining}")
    """
    
    # Default category limits (fraction of total)
    DEFAULT_LIMITS = {
        BudgetCategory.SYSTEM: 0.15,    # 15% for system
        BudgetCategory.SKILLS: 0.25,    # 25% for skills
        BudgetCategory.CONTEXT: 0.30,   # 30% for context
        BudgetCategory.HISTORY: 0.15,   # 15% for history
        BudgetCategory.RESPONSE: 0.10,  # 10% for response
        BudgetCategory.BUFFER: 0.05,    # 5% safety buffer
    }
    
    def __init__(
        self,
        total_capacity: int = 128000,
        safety_margin: float = 0.90,
        category_limits: Optional[Dict[BudgetCategory, float]] = None,
        allow_overflow: bool = False
    ):
        """
        Initialize the budget manager.
        
        Args:
            total_capacity: Total token capacity
            safety_margin: Fraction of capacity to use (0.9 = 90%)
            category_limits: Custom category limits as fractions
            allow_overflow: Allow categories to exceed limits if space available
        """
        self.total_capacity = total_capacity
        self.safety_margin = safety_margin
        self.allow_overflow = allow_overflow
        
        # Effective capacity after safety margin
        self.effective_capacity = int(total_capacity * safety_margin)
        
        # Category limits
        limits = category_limits or self.DEFAULT_LIMITS
        self.category_limits = {
            cat: int(self.effective_capacity * frac)
            for cat, frac in limits.items()
        }
        
        # Current allocations
        self._allocations: Dict[str, Allocation] = {}
        self._category_usage: Dict[BudgetCategory, int] = {
            cat: 0 for cat in BudgetCategory
        }
        
        # Tracking
        self._allocation_history: List[Tuple[float, str, int]] = []
    
    def allocate(self, request: AllocationRequest) -> Allocation:
        """
        Allocate tokens for a request.
        
        Args:
            request: Allocation request
            
        Returns:
            Allocation with granted tokens
        """
        category = request.category
        requested = request.requested_tokens
        
        # Calculate available in category
        category_limit = self.category_limits.get(category, 0)
        category_used = self._category_usage.get(category, 0)
        category_available = category_limit - category_used
        
        # Calculate global availability
        total_used = sum(self._category_usage.values())
        global_available = self.effective_capacity - total_used
        
        # Determine allocation
        if self.allow_overflow:
            # Can use up to global available
            available = min(requested, global_available)
        else:
            # Limited by category
            available = min(requested, category_available, global_available)
        
        # Apply priority-based reduction if needed
        if available < requested and request.shrinkable:
            # Reduce proportionally
            if request.priority >= 8:
                allocated = available  # High priority gets what's available
            elif request.priority >= 5:
                allocated = int(available * 0.8)  # Medium gets 80%
            else:
                allocated = int(available * 0.5)  # Low gets 50%
        else:
            allocated = min(requested, available)
        
        # Create allocation
        allocation = Allocation(
            category=category,
            allocated_tokens=allocated,
            requested_tokens=requested,
            source=request.source
        )
        
        # Track allocation
        alloc_key = f"{category.name}:{request.source}:{time.time()}"
        self._allocations[alloc_key] = allocation
        self._category_usage[category] = category_used + allocated
        
        # History
        self._allocation_history.append((time.time(), request.source, allocated))
        
        return allocation
    
    def release(self, source: str, category: Optional[BudgetCategory] = None) -> int:
        """
        Release allocations by source.
        
        Args:
            source: Source identifier to release
            category: Optional category filter
            
        Returns:
            Number of tokens released
        """
        released = 0
        to_remove = []
        
        for key, alloc in self._allocations.items():
            if alloc.source == source:
                if category is None or alloc.category == category:
                    released += alloc.allocated_tokens
                    self._category_usage[alloc.category] -= alloc.allocated_tokens
                    to_remove.append(key)
        
        for key in to_remove:
            del self._allocations[key]
        
        return released
    
    def get_snapshot(self) -> BudgetSnapshot:
        """Get current budget state."""
        return BudgetSnapshot(
            total_capacity=self.effective_capacity,
            total_allocated=sum(self._category_usage.values()),
            allocations=dict(self._category_usage)
        )
    
    def get_category_usage(self, category: BudgetCategory) -> Tuple[int, int]:
        """
        Get usage for a category.
        
        Returns:
            (used, limit) tuple
        """
        return (
            self._category_usage.get(category, 0),
            self.category_limits.get(category, 0)
        )
    
    def can_allocate(self, category: BudgetCategory, tokens: int) -> bool:
        """Check if allocation is possible."""
        used, limit = self.get_category_usage(category)
        
        if self.allow_overflow:
            total_used = sum(self._category_usage.values())
            return (total_used + tokens) <= self.effective_capacity
        else:
            return (used + tokens) <= limit
    
    def resize(self, new_capacity: int) -> None:
        """
        Resize total capacity.
        
        Recalculates all limits proportionally.
        """
        if new_capacity <= 0:
            return
        
        ratio = new_capacity / self.total_capacity
        
        self.total_capacity = new_capacity
        self.effective_capacity = int(new_capacity * self.safety_margin)
        
        # Rescale category limits
        for cat in self.category_limits:
            self.category_limits[cat] = int(self.category_limits[cat] * ratio)
    
    def reset(self) -> None:
        """Reset all allocations."""
        self._allocations.clear()
        self._category_usage = {cat: 0 for cat in BudgetCategory}
        self._allocation_history.clear()
    
    def get_allocation_summary(self) -> str:
        """Get human-readable allocation summary."""
        lines = [
            f"Token Budget Summary",
            f"{'='*40}",
            f"Capacity: {self.effective_capacity:,} / {self.total_capacity:,}",
            f"Safety Margin: {self.safety_margin:.0%}",
            f"",
            f"Category Allocations:",
        ]
        
        for cat in BudgetCategory:
            used = self._category_usage.get(cat, 0)
            limit = self.category_limits.get(cat, 0)
            pct = (used / limit * 100) if limit > 0 else 0
            bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
            lines.append(f"  {cat.name:10} [{bar}] {used:,}/{limit:,} ({pct:.0f}%)")
        
        total_used = sum(self._category_usage.values())
        total_pct = total_used / self.effective_capacity * 100
        lines.append(f"")
        lines.append(f"Total: {total_used:,} / {self.effective_capacity:,} ({total_pct:.0f}%)")
        
        return "\n".join(lines)


# =============================================================================
# Convenience Functions
# =============================================================================

_default_manager: Optional[TokenBudgetManager] = None


def get_budget_manager(capacity: int = 128000) -> TokenBudgetManager:
    """Get or create default budget manager."""
    global _default_manager
    if _default_manager is None:
        _default_manager = TokenBudgetManager(total_capacity=capacity)
    return _default_manager


def allocate_tokens(
    category: BudgetCategory,
    tokens: int,
    priority: int = 5,
    source: str = ""
) -> Allocation:
    """Quick allocation using default manager."""
    manager = get_budget_manager()
    return manager.allocate(AllocationRequest(
        category=category,
        requested_tokens=tokens,
        priority=priority,
        source=source
    ))


# =============================================================================
# _DOMYH Awesome Code v6.1.2 • HSA v5.0 • Token Budget_
# =============================================================================
