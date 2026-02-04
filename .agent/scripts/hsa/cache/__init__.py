# HSA v5.0 Cache Module
# =============================================================================
"""
High-performance caching for HSA v5.0.

Features:
- Tier 0: LRU in-memory cache
- Tier 2: Redis distributed cache (opt-in via HSA_REDIS_URL)
- TTL support
- Merkle-based invalidation
"""

from .lru import (
    LRUCache,
    CacheStats,
    CacheEntry,
    CacheDecorator,
    cached,
)

from .redis_cache import (
    RedisConfig,
    RedisCache,
    is_redis_enabled,
    get_redis_cache,
    redis_cached,
)

__all__ = [
    # LRU (Tier 0)
    "LRUCache",
    "CacheStats",
    "CacheEntry",
    "CacheDecorator",
    "cached",
    # Redis (Tier 2)
    "RedisConfig",
    "RedisCache",
    "is_redis_enabled",
    "get_redis_cache",
    "redis_cached",
]

