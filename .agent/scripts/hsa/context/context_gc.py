# =============================================================================
# context_gc.py — Mark-and-Sweep Context Garbage Collector
# =============================================================================
# HSA v5.0 - Phase 4: Token Budget & GC
# Implements intelligent context cleanup when approaching budget limits
# =============================================================================

"""
Context Garbage Collector Module

Implements mark-and-sweep garbage collection for context:
- Mark phase: Score items by recency + frequency + relevance
- Sweep phase: Remove lowest-scored items to free budget

GC triggers:
- Budget threshold exceeded (default: 85%)
- Manual trigger via gc_collect()
- Periodic background check
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Set, Tuple


class ContextItemType(Enum):
    """Types of context items."""
    SKILL = auto()
    ENTITY = auto()        # File/function/class from HiRAG
    COMMUNITY = auto()     # Community summary
    CONVERSATION = auto()  # Historical message
    CACHE = auto()         # Cached computation


@dataclass
class ContextItem:
    """An item in the context pool."""
    id: str
    item_type: ContextItemType
    content: Any
    token_size: int
    created_at: float = field(default_factory=time.time)
    last_accessed: float = field(default_factory=time.time)
    access_count: int = 1
    priority: int = 5  # 1-10, higher = keep longer
    pinned: bool = False  # Never garbage collect
    
    @property
    def age_seconds(self) -> float:
        return time.time() - self.created_at
    
    @property
    def idle_seconds(self) -> float:
        return time.time() - self.last_accessed
    
    def touch(self) -> None:
        """Mark as recently accessed."""
        self.last_accessed = time.time()
        self.access_count += 1


@dataclass
class GCStats:
    """Garbage collection statistics."""
    items_before: int
    items_after: int
    tokens_before: int
    tokens_after: int
    items_collected: int
    tokens_freed: int
    duration_ms: float
    
    def __repr__(self) -> str:
        return (
            f"GCStats(collected={self.items_collected}, "
            f"freed={self.tokens_freed:,} tokens, "
            f"time={self.duration_ms:.1f}ms)"
        )


class ContextGC:
    """
    Mark-and-sweep garbage collector for context items.
    
    Scoring formula (from HSA_V4.yaml):
    score = 0.4 * recency + 0.3 * frequency + 0.3 * relevance
    
    Where:
    - recency: Normalized by idle time
    - frequency: Normalized by access count
    - relevance: Base priority score
    
    Usage:
        gc = ContextGC(threshold_pct=0.85)
        
        # Add items
        gc.add_item(ContextItem(
            id="typescript-skill",
            item_type=ContextItemType.SKILL,
            content="...",
            token_size=1500,
            priority=8
        ))
        
        # Collect when over threshold
        if gc.should_collect():
            stats = gc.collect()
            print(f"Freed: {stats.tokens_freed}")
    """
    
    # Scoring weights
    WEIGHT_RECENCY = 0.4
    WEIGHT_FREQUENCY = 0.3
    WEIGHT_RELEVANCE = 0.3
    
    # Time constants
    RECENCY_HALFLIFE = 300  # 5 minutes
    
    def __init__(
        self,
        token_capacity: int = 100000,
        threshold_pct: float = 0.85,
        target_pct: float = 0.70,
        min_age_seconds: float = 30.0
    ):
        """
        Initialize the garbage collector.
        
        Args:
            token_capacity: Total token budget for context
            threshold_pct: Collect when usage exceeds this (0.85 = 85%)
            target_pct: Target usage after collection (0.70 = 70%)
            min_age_seconds: Don't collect items newer than this
        """
        self.token_capacity = token_capacity
        self.threshold_pct = threshold_pct
        self.target_pct = target_pct
        self.min_age_seconds = min_age_seconds
        
        # Item storage
        self._items: Dict[str, ContextItem] = {}
        self._total_tokens: int = 0
        
        # Stats
        self._collections: int = 0
        self._total_freed: int = 0
    
    def add_item(self, item: ContextItem) -> None:
        """Add an item to the context pool."""
        if item.id in self._items:
            # Replace existing
            old_item = self._items[item.id]
            self._total_tokens -= old_item.token_size
        
        self._items[item.id] = item
        self._total_tokens += item.token_size
    
    def get_item(self, item_id: str) -> Optional[ContextItem]:
        """Get an item and mark it as accessed."""
        item = self._items.get(item_id)
        if item:
            item.touch()
        return item
    
    def remove_item(self, item_id: str) -> Optional[ContextItem]:
        """Explicitly remove an item."""
        item = self._items.pop(item_id, None)
        if item:
            self._total_tokens -= item.token_size
        return item
    
    def pin_item(self, item_id: str) -> bool:
        """Pin an item to prevent garbage collection."""
        item = self._items.get(item_id)
        if item:
            item.pinned = True
            return True
        return False
    
    def unpin_item(self, item_id: str) -> bool:
        """Unpin an item."""
        item = self._items.get(item_id)
        if item:
            item.pinned = False
            return True
        return False
    
    @property
    def usage_pct(self) -> float:
        """Current usage percentage."""
        if self.token_capacity == 0:
            return 0.0
        return self._total_tokens / self.token_capacity
    
    @property
    def item_count(self) -> int:
        return len(self._items)
    
    @property
    def total_tokens(self) -> int:
        return self._total_tokens
    
    def should_collect(self) -> bool:
        """Check if garbage collection is needed."""
        return self.usage_pct > self.threshold_pct
    
    def collect(self, force: bool = False) -> GCStats:
        """
        Perform garbage collection.
        
        Args:
            force: Collect even if below threshold
            
        Returns:
            GCStats with collection results
        """
        start_time = time.perf_counter()
        
        items_before = len(self._items)
        tokens_before = self._total_tokens
        
        # Check if collection needed
        if not force and not self.should_collect():
            return GCStats(
                items_before=items_before,
                items_after=items_before,
                tokens_before=tokens_before,
                tokens_after=tokens_before,
                items_collected=0,
                tokens_freed=0,
                duration_ms=0.0
            )
        
        # Calculate target
        target_tokens = int(self.token_capacity * self.target_pct)
        tokens_to_free = max(0, self._total_tokens - target_tokens)
        
        if tokens_to_free == 0:
            return GCStats(
                items_before=items_before,
                items_after=items_before,
                tokens_before=tokens_before,
                tokens_after=tokens_before,
                items_collected=0,
                tokens_freed=0,
                duration_ms=(time.perf_counter() - start_time) * 1000
            )
        
        # Mark phase: Score all items
        scored_items: List[Tuple[float, str]] = []
        now = time.time()
        
        for item_id, item in self._items.items():
            # Skip pinned items
            if item.pinned:
                continue
            
            # Skip items too new
            if item.age_seconds < self.min_age_seconds:
                continue
            
            score = self._calculate_score(item, now)
            scored_items.append((score, item_id))
        
        # Sort by score (lowest first = most likely to collect)
        scored_items.sort(key=lambda x: x[0])
        
        # Sweep phase: Remove lowest-scored items
        tokens_freed = 0
        items_collected = 0
        
        for score, item_id in scored_items:
            if tokens_freed >= tokens_to_free:
                break
            
            item = self._items.pop(item_id, None)
            if item:
                tokens_freed += item.token_size
                items_collected += 1
        
        self._total_tokens -= tokens_freed
        self._collections += 1
        self._total_freed += tokens_freed
        
        duration_ms = (time.perf_counter() - start_time) * 1000
        
        return GCStats(
            items_before=items_before,
            items_after=len(self._items),
            tokens_before=tokens_before,
            tokens_after=self._total_tokens,
            items_collected=items_collected,
            tokens_freed=tokens_freed,
            duration_ms=duration_ms
        )
    
    def _calculate_score(self, item: ContextItem, now: float) -> float:
        """
        Calculate retention score for an item.
        
        Higher score = keep longer.
        """
        # Recency score (0-10, higher = more recent)
        idle_time = now - item.last_accessed
        recency = 10 * (0.5 ** (idle_time / self.RECENCY_HALFLIFE))
        
        # Frequency score (0-10, higher = more accessed)
        frequency = min(10, item.access_count)
        
        # Relevance score (1-10 from priority)
        relevance = item.priority
        
        # Combined score
        score = (
            self.WEIGHT_RECENCY * recency +
            self.WEIGHT_FREQUENCY * frequency +
            self.WEIGHT_RELEVANCE * relevance
        )
        
        return score
    
    def get_items_by_type(self, item_type: ContextItemType) -> List[ContextItem]:
        """Get all items of a specific type."""
        return [
            item for item in self._items.values()
            if item.item_type == item_type
        ]
    
    def get_summary(self) -> str:
        """Get human-readable summary."""
        lines = [
            f"Context GC Summary",
            f"{'='*40}",
            f"Items: {self.item_count}",
            f"Tokens: {self._total_tokens:,} / {self.token_capacity:,}",
            f"Usage: {self.usage_pct:.1%}",
            f"Threshold: {self.threshold_pct:.0%}",
            f"Collections: {self._collections}",
            f"Total freed: {self._total_freed:,}",
            f"",
            f"By Type:",
        ]
        
        type_counts: Dict[ContextItemType, Tuple[int, int]] = {}
        for item in self._items.values():
            if item.item_type not in type_counts:
                type_counts[item.item_type] = (0, 0)
            count, tokens = type_counts[item.item_type]
            type_counts[item.item_type] = (count + 1, tokens + item.token_size)
        
        for item_type, (count, tokens) in type_counts.items():
            lines.append(f"  {item_type.name}: {count} items, {tokens:,} tokens")
        
        return "\n".join(lines)


# =============================================================================
# _DOMYH Awesome Code v6.1.2 • HSA v5.0 • Context GC_
# =============================================================================
