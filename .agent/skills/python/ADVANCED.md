# Python — Advanced Patterns

# DOMYH Awesome Code v5.5 — Tier 3 Reference

## Table of Contents

- [Async Patterns](#async-patterns)
- [Type System](#type-system)
- [Decorators & Metaprogramming](#decorators--metaprogramming)
- [Performance](#performance)

---

## Async Patterns

### Async Context Manager

```python
from contextlib import asynccontextmanager
from typing import AsyncIterator

@asynccontextmanager
async def managed_resource() -> AsyncIterator[Resource]:
    resource = await acquire_resource()
    try:
        yield resource
    finally:
        await resource.close()

# Usage
async with managed_resource() as r:
    await r.process()
```

### Concurrent Execution

```python
import asyncio
from typing import List

async def fetch_all(urls: List[str]) -> List[Response]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)

# With semaphore for rate limiting
async def fetch_limited(urls: List[str], limit: int = 10):
    semaphore = asyncio.Semaphore(limit)

    async def fetch_with_limit(url: str):
        async with semaphore:
            return await fetch_one(url)

    return await asyncio.gather(*[fetch_with_limit(u) for u in urls])
```

---

## Type System

### Protocol Classes

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Serializable(Protocol):
    def to_dict(self) -> dict: ...

    @classmethod
    def from_dict(cls, data: dict) -> 'Serializable': ...

# Usage - structural typing
class User:
    def to_dict(self) -> dict:
        return {"id": self.id}

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        return cls(**data)

# Works without explicit inheritance
def save(obj: Serializable) -> None:
    data = obj.to_dict()
```

### Generic Types

```python
from typing import TypeVar, Generic, Optional

T = TypeVar('T')
E = TypeVar('E', bound=Exception)

class Result(Generic[T, E]):
    def __init__(self, value: Optional[T] = None, error: Optional[E] = None):
        self._value = value
        self._error = error

    def is_ok(self) -> bool:
        return self._error is None

    def unwrap(self) -> T:
        if self._error:
            raise self._error
        return self._value  # type: ignore
```

---

## Decorators & Metaprogramming

### Retry Decorator

```python
import functools
from typing import TypeVar, Callable, Type
import asyncio

F = TypeVar('F', bound=Callable)

def retry(
    max_attempts: int = 3,
    exceptions: tuple[Type[Exception], ...] = (Exception,),
    delay: float = 1.0
) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts - 1:
                        raise
                    await asyncio.sleep(delay * (2 ** attempt))
        return wrapper  # type: ignore
    return decorator

@retry(max_attempts=3, exceptions=(ConnectionError,))
async def fetch_data(url: str) -> dict:
    ...
```

### Dataclass with Validation

```python
from dataclasses import dataclass, field
from typing import ClassVar

@dataclass
class User:
    id: str
    email: str
    age: int
    _registry: ClassVar[dict[str, 'User']] = {}

    def __post_init__(self):
        if self.age < 0:
            raise ValueError("Age must be positive")
        if '@' not in self.email:
            raise ValueError("Invalid email")
        User._registry[self.id] = self
```

---

## Performance

### Caching with LRU

```python
from functools import lru_cache
from cachetools import TTLCache, cached

# Simple LRU cache
@lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# TTL cache for API calls
cache = TTLCache(maxsize=100, ttl=300)

@cached(cache)
def fetch_user(user_id: str) -> dict:
    return api.get_user(user_id)
```

### Slots for Memory Optimization

```python
class OptimizedUser:
    __slots__ = ('id', 'name', 'email')

    def __init__(self, id: str, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email

# 40-50% less memory vs regular class
```

---

_DOMYH Awesome Code v6.0.0 — Tier 3 Reference_
