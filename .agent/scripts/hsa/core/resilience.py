# HSA v5.0 - Resilience Patterns
# =============================================================================
"""
Circuit breaker and retry patterns for robust API handling.

Features:
- Circuit breaker (open/half-open/closed states)
- Exponential backoff with jitter
- Fallback to local on API failure
- Request timeout handling
- Health monitoring
"""

from __future__ import annotations

import asyncio
import logging
import random
import time
from dataclasses import dataclass, field
from enum import Enum
from functools import wraps
from typing import Any, Callable, Dict, Generic, Optional, TypeVar, Union

logger = logging.getLogger("hsa.resilience")

T = TypeVar("T")
R = TypeVar("R")


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if recovered


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker."""
    failure_threshold: int = 5       # Failures before opening
    success_threshold: int = 3       # Successes to close from half-open
    timeout_seconds: float = 30.0    # Time in open state before half-open
    half_open_max_calls: int = 1     # Max concurrent calls in half-open


@dataclass
class CircuitStats:
    """Statistics for circuit breaker."""
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    success_count: int = 0
    last_failure_time: float = 0
    last_success_time: float = 0
    total_calls: int = 0
    total_failures: int = 0
    total_successes: int = 0


class CircuitBreaker:
    """
    Circuit breaker for external service calls.
    
    States:
    - CLOSED: Normal operation, requests pass through
    - OPEN: Service failing, requests rejected immediately
    - HALF_OPEN: Testing recovery, limited requests allowed
    
    Usage:
        breaker = CircuitBreaker("voyage-api")
        
        try:
            result = await breaker.call(api_function, *args)
        except CircuitOpenError:
            # Circuit is open, use fallback
            result = fallback()
    """
    
    def __init__(
        self,
        name: str,
        config: Optional[CircuitBreakerConfig] = None
    ):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self._stats = CircuitStats()
        self._lock = asyncio.Lock()
        self._half_open_calls = 0
    
    @property
    def state(self) -> CircuitState:
        """Get current circuit state."""
        return self._stats.state
    
    @property
    def is_closed(self) -> bool:
        return self._stats.state == CircuitState.CLOSED
    
    @property
    def is_open(self) -> bool:
        return self._stats.state == CircuitState.OPEN
    
    async def _should_allow_request(self) -> bool:
        """Check if request should be allowed."""
        async with self._lock:
            if self._stats.state == CircuitState.CLOSED:
                return True
            
            if self._stats.state == CircuitState.OPEN:
                # Check if timeout expired
                elapsed = time.time() - self._stats.last_failure_time
                if elapsed >= self.config.timeout_seconds:
                    self._stats.state = CircuitState.HALF_OPEN
                    self._half_open_calls = 0
                    logger.info(f"Circuit '{self.name}' entering half-open state")
                    return True
                return False
            
            # Half-open: allow limited calls
            if self._half_open_calls < self.config.half_open_max_calls:
                self._half_open_calls += 1
                return True
            
            return False
    
    async def _record_success(self) -> None:
        """Record successful call."""
        async with self._lock:
            self._stats.success_count += 1
            self._stats.total_successes += 1
            self._stats.last_success_time = time.time()
            
            if self._stats.state == CircuitState.HALF_OPEN:
                if self._stats.success_count >= self.config.success_threshold:
                    self._stats.state = CircuitState.CLOSED
                    self._stats.failure_count = 0
                    self._stats.success_count = 0
                    logger.info(f"Circuit '{self.name}' closed (recovered)")
    
    async def _record_failure(self, error: Exception) -> None:
        """Record failed call."""
        async with self._lock:
            self._stats.failure_count += 1
            self._stats.total_failures += 1
            self._stats.last_failure_time = time.time()
            
            if self._stats.state == CircuitState.HALF_OPEN:
                # Immediate open on failure in half-open
                self._stats.state = CircuitState.OPEN
                logger.warning(f"Circuit '{self.name}' opened (half-open test failed)")
            
            elif self._stats.state == CircuitState.CLOSED:
                if self._stats.failure_count >= self.config.failure_threshold:
                    self._stats.state = CircuitState.OPEN
                    logger.warning(f"Circuit '{self.name}' opened (threshold reached)")
    
    async def call(
        self,
        func: Callable[..., T],
        *args,
        **kwargs
    ) -> T:
        """
        Execute function through circuit breaker.
        
        Raises:
            CircuitOpenError: If circuit is open
        """
        self._stats.total_calls += 1
        
        if not await self._should_allow_request():
            raise CircuitOpenError(
                f"Circuit '{self.name}' is open. "
                f"Retry after {self.config.timeout_seconds}s"
            )
        
        try:
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            
            await self._record_success()
            return result
            
        except Exception as e:
            await self._record_failure(e)
            raise
    
    def get_stats(self) -> Dict[str, Any]:
        """Get circuit breaker statistics."""
        return {
            "name": self.name,
            "state": self._stats.state.value,
            "failure_count": self._stats.failure_count,
            "success_count": self._stats.success_count,
            "total_calls": self._stats.total_calls,
            "total_failures": self._stats.total_failures,
            "total_successes": self._stats.total_successes,
        }
    
    def reset(self) -> None:
        """Manually reset circuit to closed state."""
        self._stats = CircuitStats()
        logger.info(f"Circuit '{self.name}' manually reset")


class CircuitOpenError(Exception):
    """Raised when circuit breaker is open."""
    pass


@dataclass
class RetryConfig:
    """Configuration for retry behavior."""
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 30.0
    exponential_base: float = 2.0
    jitter: bool = True
    jitter_factor: float = 0.5
    retryable_exceptions: tuple = (Exception,)


class RetryHandler:
    """
    Retry handler with exponential backoff.
    
    Features:
    - Exponential backoff
    - Random jitter to prevent thundering herd
    - Configurable per exception type
    
    Usage:
        retry = RetryHandler()
        
        result = await retry.execute(unstable_function, *args)
    """
    
    def __init__(self, config: Optional[RetryConfig] = None):
        self.config = config or RetryConfig()
    
    def _calculate_delay(self, attempt: int) -> float:
        """Calculate delay for attempt."""
        delay = self.config.base_delay * (self.config.exponential_base ** attempt)
        delay = min(delay, self.config.max_delay)
        
        if self.config.jitter:
            jitter = delay * self.config.jitter_factor * random.random()
            delay = delay + jitter
        
        return delay
    
    async def execute(
        self,
        func: Callable[..., T],
        *args,
        **kwargs
    ) -> T:
        """Execute function with retries."""
        last_exception = None
        
        for attempt in range(self.config.max_attempts):
            try:
                if asyncio.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                else:
                    return func(*args, **kwargs)
                    
            except self.config.retryable_exceptions as e:
                last_exception = e
                
                if attempt < self.config.max_attempts - 1:
                    delay = self._calculate_delay(attempt)
                    logger.warning(
                        f"Attempt {attempt + 1}/{self.config.max_attempts} failed: {e}. "
                        f"Retrying in {delay:.2f}s"
                    )
                    await asyncio.sleep(delay)
        
        raise last_exception


class ResilientClient(Generic[T]):
    """
    Resilient wrapper combining circuit breaker and retry.
    
    Usage:
        client = ResilientClient(
            primary=voyage_embedder.embed_batch,
            fallback=local_embedder.embed_batch,
            name="embedding"
        )
        
        vectors = await client.execute(texts)
    """
    
    def __init__(
        self,
        primary: Callable[..., T],
        fallback: Optional[Callable[..., T]] = None,
        name: str = "service",
        circuit_config: Optional[CircuitBreakerConfig] = None,
        retry_config: Optional[RetryConfig] = None
    ):
        self.primary = primary
        self.fallback = fallback
        self.name = name
        self._breaker = CircuitBreaker(name, circuit_config)
        self._retry = RetryHandler(retry_config)
        self._fallback_count = 0
    
    async def execute(self, *args, **kwargs) -> T:
        """
        Execute with resilience patterns.
        
        1. Try primary through circuit breaker
        2. Retry on transient failures
        3. Fall back to local if circuit open or all retries fail
        """
        try:
            return await self._breaker.call(
                self._retry.execute,
                self.primary,
                *args,
                **kwargs
            )
            
        except (CircuitOpenError, Exception) as e:
            if self.fallback is None:
                raise
            
            self._fallback_count += 1
            logger.warning(
                f"{self.name}: Using fallback due to {type(e).__name__}: {e}"
            )
            
            if asyncio.iscoroutinefunction(self.fallback):
                return await self.fallback(*args, **kwargs)
            else:
                return self.fallback(*args, **kwargs)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get resilience statistics."""
        return {
            **self._breaker.get_stats(),
            "fallback_count": self._fallback_count,
        }


# Decorator versions

def with_circuit_breaker(
    name: str,
    config: Optional[CircuitBreakerConfig] = None
):
    """Decorator to add circuit breaker to function."""
    breaker = CircuitBreaker(name, config)
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            return await breaker.call(func, *args, **kwargs)
        return wrapper
    return decorator


def with_retry(config: Optional[RetryConfig] = None):
    """Decorator to add retry behavior to function."""
    handler = RetryHandler(config)
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            return await handler.execute(func, *args, **kwargs)
        return wrapper
    return decorator


def with_fallback(fallback_func: Callable[..., T]):
    """Decorator to add fallback behavior."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            try:
                if asyncio.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                else:
                    return func(*args, **kwargs)
            except Exception as e:
                logger.warning(f"Using fallback due to: {e}")
                if asyncio.iscoroutinefunction(fallback_func):
                    return await fallback_func(*args, **kwargs)
                else:
                    return fallback_func(*args, **kwargs)
        return wrapper
    return decorator
