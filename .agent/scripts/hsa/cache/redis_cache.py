# HSA v5.0 - Redis Cache Layer
# =============================================================================
"""
Redis-backed distributed cache for enterprise deployments.

Features:
- L2 cache with configurable TTL
- Embedding vector caching
- Search result caching
- Pub/sub for cache invalidation
- Connection pooling

Environment:
- HSA_REDIS_URL: Redis connection URL
- HSA_REDIS_PREFIX: Key prefix (default: hsa:)
- HSA_REDIS_TTL: Default TTL in seconds (default: 3600)
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import os
import pickle
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar, Union

logger = logging.getLogger("hsa.redis")

T = TypeVar("T")


@dataclass
class RedisConfig:
    """Configuration for Redis connection."""
    url: str = "redis://localhost:6379"
    prefix: str = "hsa:"
    default_ttl: int = 3600  # 1 hour
    max_connections: int = 10
    socket_timeout: float = 5.0
    retry_on_timeout: bool = True
    decode_responses: bool = False  # We use pickle for binary data
    
    @classmethod
    def from_env(cls) -> "RedisConfig":
        """Create config from environment variables."""
        return cls(
            url=os.environ.get("HSA_REDIS_URL", "redis://localhost:6379"),
            prefix=os.environ.get("HSA_REDIS_PREFIX", "hsa:"),
            default_ttl=int(os.environ.get("HSA_REDIS_TTL", "3600")),
        )


class RedisCache:
    """
    Redis-backed distributed cache.
    
    Provides L2 caching for:
    - Embedding vectors
    - Search results
    - Parsed AST entities
    
    Usage:
        cache = RedisCache()
        await cache.connect()
        
        # Cache embeddings
        await cache.set_embedding("file.py", [0.1, 0.2, ...])
        vectors = await cache.get_embedding("file.py")
        
        # Cache search results
        await cache.set_search("query", results)
        cached = await cache.get_search("query")
    """
    
    def __init__(self, config: Optional[RedisConfig] = None):
        self.config = config or RedisConfig.from_env()
        self._client = None
        self._pubsub = None
        self._connected = False
        self._stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "invalidations": 0,
        }
    
    async def connect(self) -> None:
        """Connect to Redis server."""
        try:
            import redis.asyncio as redis
            
            self._client = redis.from_url(
                self.config.url,
                max_connections=self.config.max_connections,
                socket_timeout=self.config.socket_timeout,
                retry_on_timeout=self.config.retry_on_timeout,
                decode_responses=self.config.decode_responses,
            )
            
            # Test connection
            await self._client.ping()
            
            self._connected = True
            logger.info(f"Connected to Redis at {self.config.url}")
            
        except ImportError:
            raise RuntimeError(
                "redis not installed. "
                "Install with: pip install redis>=5.0"
            )
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    def _make_key(self, namespace: str, key: str) -> str:
        """Create prefixed key."""
        return f"{self.config.prefix}{namespace}:{key}"
    
    def _hash_key(self, value: str) -> str:
        """Create hash for long keys."""
        return hashlib.sha256(value.encode()).hexdigest()[:32]
    
    async def get(self, namespace: str, key: str) -> Optional[Any]:
        """Get value from cache."""
        if not self._connected:
            return None
        
        try:
            full_key = self._make_key(namespace, key)
            data = await self._client.get(full_key)
            
            if data is None:
                self._stats["misses"] += 1
                return None
            
            self._stats["hits"] += 1
            return pickle.loads(data)
            
        except Exception as e:
            logger.warning(f"Redis get failed: {e}")
            self._stats["misses"] += 1
            return None
    
    async def set(
        self,
        namespace: str,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """Set value in cache."""
        if not self._connected:
            return False
        
        try:
            full_key = self._make_key(namespace, key)
            data = pickle.dumps(value)
            
            await self._client.set(
                full_key,
                data,
                ex=ttl or self.config.default_ttl
            )
            
            self._stats["sets"] += 1
            return True
            
        except Exception as e:
            logger.warning(f"Redis set failed: {e}")
            return False
    
    async def delete(self, namespace: str, key: str) -> bool:
        """Delete key from cache."""
        if not self._connected:
            return False
        
        try:
            full_key = self._make_key(namespace, key)
            await self._client.delete(full_key)
            return True
        except Exception as e:
            logger.warning(f"Redis delete failed: {e}")
            return False
    
    async def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching pattern."""
        if not self._connected:
            return 0
        
        try:
            full_pattern = f"{self.config.prefix}{pattern}"
            cursor = 0
            deleted = 0
            
            while True:
                cursor, keys = await self._client.scan(cursor, match=full_pattern)
                if keys:
                    deleted += await self._client.delete(*keys)
                if cursor == 0:
                    break
            
            self._stats["invalidations"] += deleted
            return deleted
            
        except Exception as e:
            logger.warning(f"Redis invalidate failed: {e}")
            return 0
    
    # === Embedding Cache ===
    
    async def get_embedding(self, doc_id: str) -> Optional[List[float]]:
        """Get cached embedding vector."""
        return await self.get("emb", self._hash_key(doc_id))
    
    async def set_embedding(
        self,
        doc_id: str,
        vector: List[float],
        ttl: int = 86400  # 24 hours default
    ) -> bool:
        """Cache embedding vector."""
        return await self.set("emb", self._hash_key(doc_id), vector, ttl)
    
    async def get_embeddings_batch(
        self,
        doc_ids: List[str]
    ) -> Dict[str, Optional[List[float]]]:
        """Get multiple embeddings (pipeline)."""
        if not self._connected or not doc_ids:
            return {}
        
        try:
            pipe = self._client.pipeline()
            keys = [self._make_key("emb", self._hash_key(doc_id)) for doc_id in doc_ids]
            
            for key in keys:
                pipe.get(key)
            
            results = await pipe.execute()
            
            output = {}
            for doc_id, data in zip(doc_ids, results):
                if data:
                    output[doc_id] = pickle.loads(data)
                    self._stats["hits"] += 1
                else:
                    output[doc_id] = None
                    self._stats["misses"] += 1
            
            return output
            
        except Exception as e:
            logger.warning(f"Redis batch get failed: {e}")
            return {}
    
    # === Search Cache ===
    
    async def get_search(
        self,
        query: str,
        k: int = 10
    ) -> Optional[List[Dict[str, Any]]]:
        """Get cached search results."""
        cache_key = self._hash_key(f"{query}:{k}")
        return await self.get("search", cache_key)
    
    async def set_search(
        self,
        query: str,
        results: List[Dict[str, Any]],
        k: int = 10,
        ttl: int = 300  # 5 minutes default
    ) -> bool:
        """Cache search results."""
        cache_key = self._hash_key(f"{query}:{k}")
        return await self.set("search", cache_key, results, ttl)
    
    # === Pub/Sub for Invalidation ===
    
    async def subscribe_invalidation(
        self,
        handler: Callable[[str], None]
    ) -> None:
        """Subscribe to cache invalidation events."""
        if not self._connected:
            return
        
        self._pubsub = self._client.pubsub()
        channel = f"{self.config.prefix}invalidate"
        
        await self._pubsub.subscribe(channel)
        
        async def listen():
            async for message in self._pubsub.listen():
                if message["type"] == "message":
                    pattern = message["data"].decode() if isinstance(message["data"], bytes) else message["data"]
                    await self.invalidate_pattern(pattern)
                    handler(pattern)
        
        asyncio.create_task(listen())
        logger.info("Subscribed to cache invalidation channel")
    
    async def publish_invalidation(self, pattern: str) -> None:
        """Publish cache invalidation event."""
        if not self._connected:
            return
        
        try:
            channel = f"{self.config.prefix}invalidate"
            await self._client.publish(channel, pattern)
            logger.debug(f"Published invalidation: {pattern}")
        except Exception as e:
            logger.warning(f"Failed to publish invalidation: {e}")
    
    # === Stats & Management ===
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total = self._stats["hits"] + self._stats["misses"]
        hit_rate = self._stats["hits"] / total if total > 0 else 0
        
        return {
            **self._stats,
            "hit_rate": hit_rate,
            "connected": self._connected,
        }
    
    async def clear_all(self) -> int:
        """Clear all HSA cache entries."""
        return await self.invalidate_pattern("*")
    
    async def close(self) -> None:
        """Close Redis connection."""
        if self._pubsub:
            await self._pubsub.close()
        if self._client:
            await self._client.close()
            self._connected = False
            logger.info("Redis connection closed")


def is_redis_enabled() -> bool:
    """Check if Redis is enabled via environment."""
    return bool(os.environ.get("HSA_REDIS_URL"))


async def get_redis_cache() -> Optional[RedisCache]:
    """Get Redis cache if enabled."""
    if not is_redis_enabled():
        return None
    
    cache = RedisCache()
    await cache.connect()
    return cache


# Decorator for cached functions
def redis_cached(
    namespace: str,
    ttl: int = 3600,
    key_func: Optional[Callable[..., str]] = None
):
    """
    Decorator to cache function results in Redis.
    
    Usage:
        @redis_cached("embeddings", ttl=86400)
        async def get_embedding(doc_id: str) -> List[float]:
            ...
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        cache: Optional[RedisCache] = None
        
        async def wrapper(*args, **kwargs) -> T:
            nonlocal cache
            
            # Lazy init cache
            if cache is None and is_redis_enabled():
                cache = RedisCache()
                await cache.connect()
            
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                cache_key = str(args) + str(sorted(kwargs.items()))
            
            # Try cache
            if cache:
                cached = await cache.get(namespace, cache_key)
                if cached is not None:
                    return cached
            
            # Call function
            result = await func(*args, **kwargs)
            
            # Cache result
            if cache and result is not None:
                await cache.set(namespace, cache_key, result, ttl)
            
            return result
        
        return wrapper
    return decorator
