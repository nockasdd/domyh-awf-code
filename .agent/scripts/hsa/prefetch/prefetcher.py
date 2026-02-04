# =============================================================================
# prefetcher.py — Proactive File Prefetching
# =============================================================================
# HSA v5.0 - Phase 5: Proactive Prefetching
# Implements intelligent file preloading based on trajectory predictions
# =============================================================================

"""
Prefetcher Module

Proactively loads files that are likely to be accessed next.
Combines trajectory predictions with context awareness.

From HSA_V4.yaml spec:
- algorithm: markov_chain
- hit_rate_target: 60%
- preload_count: 3
"""

from __future__ import annotations

import asyncio
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from .trajectory_model import MarkovTrajectoryModel, Prediction


@dataclass
class PrefetchedFile:
    """A prefetched file in cache."""
    file_id: str
    content: str
    size_bytes: int
    prefetch_time: float
    prediction_probability: float
    was_accessed: bool = False
    access_time: Optional[float] = None
    
    @property
    def latency_saved_ms(self) -> float:
        """Estimate of latency saved if file was accessed."""
        if not self.was_accessed or not self.access_time:
            return 0.0
        return (self.access_time - self.prefetch_time) * 1000


@dataclass
class PrefetchStats:
    """Statistics for prefetching performance."""
    total_prefetches: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    bytes_prefetched: int = 0
    total_latency_saved_ms: float = 0.0
    
    @property
    def hit_rate(self) -> float:
        total = self.cache_hits + self.cache_misses
        if total == 0:
            return 0.0
        return self.cache_hits / total
    
    def to_dict(self) -> dict:
        return {
            "total_prefetches": self.total_prefetches,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "hit_rate": f"{self.hit_rate:.1%}",
            "bytes_prefetched": self.bytes_prefetched,
            "latency_saved_ms": self.total_latency_saved_ms
        }


class FileLoader:
    """
    Abstract file loader interface.
    
    Subclass to customize how files are loaded.
    """
    
    def load(self, file_id: str) -> Optional[str]:
        """Load file content. Returns None if not found."""
        try:
            path = Path(file_id)
            if path.exists() and path.is_file():
                return path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            pass
        return None
    
    def get_size(self, file_id: str) -> int:
        """Get file size in bytes."""
        try:
            path = Path(file_id)
            if path.exists():
                return path.stat().st_size
        except Exception:
            pass
        return 0


class Prefetcher:
    """
    Proactive file prefetcher.
    
    Loads predicted files into cache before they're needed.
    
    Features:
    - Markov-based prediction
    - LRU cache eviction
    - Background prefetching
    - Hit rate tracking
    
    Usage:
        prefetcher = Prefetcher(max_cache_size=10)
        
        # Record access and trigger prefetch
        content = prefetcher.get_file("main.py")
        
        # Later, likely files are already cached
        content = prefetcher.get_file("utils.py")  # Fast!
    """
    
    def __init__(
        self,
        max_cache_size: int = 10,
        preload_count: int = 3,
        min_probability: float = 0.1,
        file_loader: Optional[FileLoader] = None,
        model_path: Optional[Path] = None
    ):
        """
        Initialize the prefetcher.
        
        Args:
            max_cache_size: Maximum files to keep in cache
            preload_count: Number of files to prefetch per access
            min_probability: Minimum prediction probability to prefetch
            file_loader: Custom file loader
            model_path: Path to save/load trajectory model
        """
        self.max_cache_size = max_cache_size
        self.preload_count = preload_count
        self.min_probability = min_probability
        self.file_loader = file_loader or FileLoader()
        self.model_path = model_path
        
        # Trajectory model
        self.trajectory_model = MarkovTrajectoryModel()
        if model_path and model_path.exists():
            self.trajectory_model.load(model_path)
        
        # Cache: file_id -> PrefetchedFile
        self._cache: Dict[str, PrefetchedFile] = {}
        self._cache_order: List[str] = []  # LRU order
        
        # Stats
        self._stats = PrefetchStats()
        
        # Background prefetch lock
        self._prefetch_lock = threading.Lock()
        self._prefetch_pending: Set[str] = set()
    
    def get_file(
        self,
        file_id: str,
        trigger_prefetch: bool = True
    ) -> Optional[str]:
        """
        Get file content, using cache if available.
        
        Args:
            file_id: File identifier
            trigger_prefetch: Whether to prefetch predicted files
            
        Returns:
            File content or None
        """
        now = time.time()
        
        # Record access for trajectory model
        self.trajectory_model.record_access(file_id)
        
        # Check cache
        if file_id in self._cache:
            cached = self._cache[file_id]
            cached.was_accessed = True
            cached.access_time = now
            
            self._stats.cache_hits += 1
            self._stats.total_latency_saved_ms += cached.latency_saved_ms
            
            # Move to end of LRU
            if file_id in self._cache_order:
                self._cache_order.remove(file_id)
            self._cache_order.append(file_id)
            
            # Trigger prefetch for next predictions
            if trigger_prefetch:
                self._prefetch_predicted(file_id)
            
            return cached.content
        
        # Cache miss - load file
        self._stats.cache_misses += 1
        content = self.file_loader.load(file_id)
        
        # Trigger prefetch
        if trigger_prefetch:
            self._prefetch_predicted(file_id)
        
        return content
    
    def prefetch(self, file_id: str, probability: float = 1.0) -> bool:
        """
        Explicitly prefetch a file.
        
        Args:
            file_id: File to prefetch
            probability: Prediction probability
            
        Returns:
            True if prefetched successfully
        """
        # Skip if already cached
        if file_id in self._cache:
            return True
        
        # Skip if already pending
        with self._prefetch_lock:
            if file_id in self._prefetch_pending:
                return False
            self._prefetch_pending.add(file_id)
        
        try:
            content = self.file_loader.load(file_id)
            if content is None:
                return False
            
            size = len(content.encode("utf-8"))
            
            # Add to cache
            self._cache[file_id] = PrefetchedFile(
                file_id=file_id,
                content=content,
                size_bytes=size,
                prefetch_time=time.time(),
                prediction_probability=probability
            )
            self._cache_order.append(file_id)
            
            self._stats.total_prefetches += 1
            self._stats.bytes_prefetched += size
            
            # Evict if over limit
            self._evict_if_needed()
            
            return True
        finally:
            with self._prefetch_lock:
                self._prefetch_pending.discard(file_id)
    
    def _prefetch_predicted(self, current_file: str) -> None:
        """Prefetch files predicted from current file."""
        predictions = self.trajectory_model.predict(
            current_file,
            k=self.preload_count
        )
        
        for pred in predictions:
            if pred.probability >= self.min_probability:
                # Run in background thread
                thread = threading.Thread(
                    target=self.prefetch,
                    args=(pred.file_id, pred.probability),
                    daemon=True
                )
                thread.start()
    
    def _evict_if_needed(self) -> None:
        """Evict oldest entries if cache is full."""
        while len(self._cache) > self.max_cache_size:
            if not self._cache_order:
                break
            
            # Remove oldest
            oldest = self._cache_order.pop(0)
            if oldest in self._cache:
                del self._cache[oldest]
    
    def invalidate(self, file_id: str) -> bool:
        """Remove a file from cache."""
        if file_id in self._cache:
            del self._cache[file_id]
            if file_id in self._cache_order:
                self._cache_order.remove(file_id)
            return True
        return False
    
    def clear_cache(self) -> None:
        """Clear entire cache."""
        self._cache.clear()
        self._cache_order.clear()
    
    def get_stats(self) -> PrefetchStats:
        """Get prefetching statistics."""
        return self._stats
    
    def get_cache_contents(self) -> List[str]:
        """Get list of cached file IDs."""
        return list(self._cache.keys())
    
    def save_model(self) -> None:
        """Save trajectory model to disk."""
        if self.model_path:
            self.trajectory_model.save(self.model_path)
    
    def new_session(self) -> None:
        """Start a new session."""
        self.trajectory_model.new_session()
    
    def get_summary(self) -> str:
        """Get human-readable summary."""
        trajectory_stats = self.trajectory_model.get_stats()
        
        lines = [
            "Prefetcher Summary",
            "=" * 40,
            f"Cache: {len(self._cache)}/{self.max_cache_size} files",
            f"Prefetch hit rate: {self._stats.hit_rate:.1%}",
            f"Trajectory hit rate: {trajectory_stats.hit_rate:.1%}",
            f"Total prefetches: {self._stats.total_prefetches}",
            f"Bytes prefetched: {self._stats.bytes_prefetched:,}",
            f"Latency saved: {self._stats.total_latency_saved_ms:.1f}ms",
            "",
            "Cached files:",
        ]
        
        for file_id in self._cache_order[-5:]:
            cached = self._cache.get(file_id)
            if cached:
                status = "✓ accessed" if cached.was_accessed else "○ pending"
                lines.append(f"  - {file_id}: {status}")
        
        return "\n".join(lines)


class AsyncPrefetcher:
    """
    Async version of Prefetcher for use with asyncio.
    
    Usage:
        prefetcher = AsyncPrefetcher()
        content = await prefetcher.get_file("main.py")
    """
    
    def __init__(self, prefetcher: Optional[Prefetcher] = None, **kwargs):
        self._prefetcher = prefetcher or Prefetcher(**kwargs)
    
    async def get_file(
        self,
        file_id: str,
        trigger_prefetch: bool = True
    ) -> Optional[str]:
        """Get file content asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self._prefetcher.get_file(file_id, trigger_prefetch)
        )
    
    async def prefetch(self, file_id: str, probability: float = 1.0) -> bool:
        """Prefetch a file asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self._prefetcher.prefetch(file_id, probability)
        )
    
    def get_stats(self) -> PrefetchStats:
        return self._prefetcher.get_stats()


# =============================================================================
# Convenience Functions
# =============================================================================

_default_prefetcher: Optional[Prefetcher] = None


def get_prefetcher(**kwargs) -> Prefetcher:
    """Get or create default prefetcher."""
    global _default_prefetcher
    if _default_prefetcher is None:
        _default_prefetcher = Prefetcher(**kwargs)
    return _default_prefetcher


def prefetch_file(file_id: str) -> bool:
    """Quick prefetch using default prefetcher."""
    return get_prefetcher().prefetch(file_id)


# =============================================================================
# _DOMYH Awesome Code v6.1.2 • HSA v5.0 • Prefetcher_
# =============================================================================
