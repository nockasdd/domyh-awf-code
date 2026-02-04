# HSA v5.0 - LRU Cache with TTL and Merkle Invalidation
# =============================================================================
"""
High-performance LRU cache for HSA v5.0.

Features:
- LRU eviction policy
- Optional TTL (time-to-live)
- Cache statistics
- Thread-safe operations
- Merkle-based invalidation support
"""

from __future__ import annotations

import logging
import threading
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Generic, Optional, TypeVar

logger = logging.getLogger("hsa.cache")

K = TypeVar("K")  # Key type
V = TypeVar("V")  # Value type


@dataclass
class CacheStats:
    """Cache performance statistics."""
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    expirations: int = 0
    current_size: int = 0
    max_size: int = 0
    
    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate percentage."""
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "hits": self.hits,
            "misses": self.misses,
            "evictions": self.evictions,
            "expirations": self.expirations,
            "current_size": self.current_size,
            "max_size": self.max_size,
            "hit_rate": f"{self.hit_rate:.1f}%"
        }


@dataclass
class CacheEntry(Generic[V]):
    """Cache entry with optional TTL."""
    value: V
    expires_at: Optional[float] = None
    created_at: float = field(default_factory=time.time)
    access_count: int = 0
    
    def is_expired(self) -> bool:
        """Check if entry has expired."""
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at


class LRUCache(Generic[K, V]):
    """
    Thread-safe LRU cache with TTL support.
    
    Usage:
        cache = LRUCache(maxsize=1000, ttl_seconds=300)
        cache.set("key", "value")
        value = cache.get("key")  # Returns "value"
        
        # With TTL override
        cache.set("temp_key", "temp_value", ttl=60)
        
        # Check stats
        print(cache.stats.hit_rate)
    """
    
    def __init__(
        self, 
        maxsize: int = 1000,
        ttl_seconds: Optional[float] = 300.0,  # 5 minutes default
        on_evict: Optional[Callable[[K, V], None]] = None
    ):
        """
        Initialize LRU cache.
        
        Args:
            maxsize: Maximum number of items in cache
            ttl_seconds: Default TTL in seconds (None = no expiry)
            on_evict: Optional callback when item is evicted
        """
        self._maxsize = maxsize
        self._default_ttl = ttl_seconds
        self._on_evict = on_evict
        
        self._cache: OrderedDict[K, CacheEntry[V]] = OrderedDict()
        self._lock = threading.RLock()
        self._stats = CacheStats(max_size=maxsize)
        
        logger.debug(f"LRU cache initialized: maxsize={maxsize}, ttl={ttl_seconds}s")
    
    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            default: Default value if not found
            
        Returns:
            Cached value or default
        """
        with self._lock:
            if key not in self._cache:
                self._stats.misses += 1
                return default
            
            entry = self._cache[key]
            
            # Check expiration
            if entry.is_expired():
                self._stats.expirations += 1
                self._stats.misses += 1
                del self._cache[key]
                self._stats.current_size = len(self._cache)
                return default
            
            # Move to end (most recently used)
            self._cache.move_to_end(key)
            entry.access_count += 1
            
            self._stats.hits += 1
            return entry.value
    
    def set(
        self, 
        key: K, 
        value: V, 
        ttl: Optional[float] = None
    ) -> None:
        """
        Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: TTL in seconds (overrides default)
        """
        with self._lock:
            # Calculate expiration
            ttl_to_use = ttl if ttl is not None else self._default_ttl
            expires_at = (
                time.time() + ttl_to_use 
                if ttl_to_use is not None 
                else None
            )
            
            # Update or insert
            if key in self._cache:
                # Update existing
                self._cache[key] = CacheEntry(value=value, expires_at=expires_at)
                self._cache.move_to_end(key)
            else:
                # Evict if at capacity
                while len(self._cache) >= self._maxsize:
                    self._evict_oldest()
                
                # Insert new
                self._cache[key] = CacheEntry(value=value, expires_at=expires_at)
            
            self._stats.current_size = len(self._cache)
    
    def _evict_oldest(self) -> None:
        """Evict least recently used item."""
        if not self._cache:
            return
        
        oldest_key, oldest_entry = self._cache.popitem(last=False)
        self._stats.evictions += 1
        
        if self._on_evict:
            try:
                self._on_evict(oldest_key, oldest_entry.value)
            except Exception as e:
                logger.warning(f"Error in eviction callback: {e}")
    
    def delete(self, key: K) -> bool:
        """
        Delete item from cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if deleted, False if not found
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                self._stats.current_size = len(self._cache)
                return True
            return False
    
    def invalidate_pattern(self, predicate: Callable[[K], bool]) -> int:
        """
        Invalidate all keys matching predicate.
        
        Args:
            predicate: Function that returns True for keys to invalidate
            
        Returns:
            Number of items invalidated
        """
        with self._lock:
            keys_to_delete = [k for k in self._cache if predicate(k)]
            for key in keys_to_delete:
                del self._cache[key]
            
            count = len(keys_to_delete)
            self._stats.current_size = len(self._cache)
            
            if count > 0:
                logger.debug(f"Invalidated {count} cache entries")
            
            return count
    
    def invalidate_by_file(self, file_path: str) -> int:
        """
        Invalidate cache entries related to a file.
        
        Supports Merkle-based invalidation by matching file paths.
        
        Args:
            file_path: Path of changed file
            
        Returns:
            Number of items invalidated
        """
        def matches_file(key: K) -> bool:
            key_str = str(key)
            return file_path in key_str or key_str.startswith(file_path)
        
        return self.invalidate_pattern(matches_file)
    
    def clear(self) -> None:
        """Clear all cache entries."""
        with self._lock:
            self._cache.clear()
            self._stats = CacheStats(max_size=self._maxsize)
            logger.debug("Cache cleared")
    
    def contains(self, key: K) -> bool:
        """Check if key exists and is not expired."""
        with self._lock:
            if key not in self._cache:
                return False
            
            entry = self._cache[key]
            if entry.is_expired():
                del self._cache[key]
                self._stats.current_size = len(self._cache)
                return False
            
            return True
    
    def cleanup_expired(self) -> int:
        """
        Remove all expired entries.
        
        Returns:
            Number of entries removed
        """
        with self._lock:
            expired_keys = [
                k for k, v in self._cache.items() 
                if v.is_expired()
            ]
            
            for key in expired_keys:
                del self._cache[key]
                self._stats.expirations += 1
            
            self._stats.current_size = len(self._cache)
            
            if expired_keys:
                logger.debug(f"Cleaned up {len(expired_keys)} expired entries")
            
            return len(expired_keys)
    
    @property
    def stats(self) -> CacheStats:
        """Get cache statistics."""
        with self._lock:
            self._stats.current_size = len(self._cache)
            return self._stats
    
    @property
    def size(self) -> int:
        """Current number of items in cache."""
        return len(self._cache)
    
    @property
    def maxsize(self) -> int:
        """Maximum cache size."""
        return self._maxsize
    
    def __len__(self) -> int:
        return len(self._cache)
    
    def __contains__(self, key: K) -> bool:
        return self.contains(key)
    
    def __getitem__(self, key: K) -> V:
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value
    
    def __setitem__(self, key: K, value: V) -> None:
        self.set(key, value)


class CacheDecorator:
    """Decorator for caching function results."""
    
    def __init__(
        self, 
        cache: LRUCache,
        key_func: Optional[Callable[..., str]] = None
    ):
        """
        Initialize cache decorator.
        
        Args:
            cache: LRU cache instance
            key_func: Optional function to generate cache key from args
        """
        self._cache = cache
        self._key_func = key_func or self._default_key_func
    
    @staticmethod
    def _default_key_func(*args, **kwargs) -> str:
        """Generate default cache key from arguments."""
        return str(hash((args, tuple(sorted(kwargs.items())))))
    
    def __call__(self, func: Callable) -> Callable:
        """Decorate function with caching."""
        def wrapper(*args, **kwargs):
            key = self._key_func(*args, **kwargs)
            
            cached = self._cache.get(key)
            if cached is not None:
                return cached
            
            result = func(*args, **kwargs)
            self._cache.set(key, result)
            return result
        
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        wrapper._cache = self._cache  # Expose cache for testing
        
        return wrapper


def cached(
    maxsize: int = 1000, 
    ttl_seconds: float = 300.0
) -> Callable:
    """
    Decorator factory for function caching.
    
    Usage:
        @cached(maxsize=100, ttl_seconds=60)
        def expensive_function(x):
            return x * 2
    """
    cache = LRUCache(maxsize=maxsize, ttl_seconds=ttl_seconds)
    decorator = CacheDecorator(cache)
    
    def wrapper(func: Callable) -> Callable:
        return decorator(func)
    
    return wrapper
