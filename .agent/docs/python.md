---
library: python
version: 3.13
latest: true
category: backend
official_docs: https://docs.python.org/3
last_updated: 2026-03-20
last_checked: 2026-03-21
source: official docs + crawl4ai/trafilatura extraction
---

# Python 3.14

> Python — Versatile, high-level programming language.
> Current: 3.14 (Free-threaded officially supported, JIT compiler) | Previous: 3.13
> Docs: https://docs.python.org/3

## Version Comparison

| Feature | 3.12 | 3.13 | 3.14 |
|:--------|:-----|:-----|:-----|
| Speed | Faster | Faster | Fastest (JIT compiler) |
| Error messages | Better | Best | Better still |
| Type params `[T]` | ✅ `type X[T]` | ✅ | ✅ |
| `f-string` nesting | Full | Full | Full |
| Template strings `t""` | ❌ | ❌ | ✅ (PEP 750) |
| Free-threaded (no GIL) | ❌ | Experimental | Official support |
| Deferred annotations | ❌ | ❌ | ✅ (PEP 649) |
| Multiple interpreters | ❌ | ❌ | ✅ (PEP 734) |
| Improved REPL | ❌ | ✅ (colors, multiline) | ✅ |
| Zstandard compression | ❌ | ❌ | ✅ (PEP 784) |

## Core Types & Syntax

```python
# Type hints (modern style)
from typing import Optional, Union, Callable, TypeAlias

name: str = "Alice"
age: int = 30
scores: list[int] = [90, 85, 92]
user: dict[str, str] = {"name": "Alice"}
coords: tuple[float, float] = (1.0, 2.0)
maybe: str | None = None          # 3.10+ union syntax
callback: Callable[[int], str]

# Type aliases (3.12+)
type Vector = list[float]
type Matrix = list[Vector]
type UserDict = dict[str, str | int]

# f-strings
greeting = f"Hello, {name}!"
debug = f"{scores = }"            # 3.8+: scores = [90, 85, 92]
nested = f"{'yes' if age > 18 else 'no'}"

# Template strings (3.14+ — PEP 750)
from string.templatelib import Template, Interpolation
variety = 'Stilton'
template = t'Try some {variety} cheese!'  # returns Template object, NOT str
type(template)  # <class 'string.templatelib.Template'>

# Iterate template parts
for part in template:
    if isinstance(part, Interpolation):
        print(f"Dynamic: {part.value}")  # 'Stilton'
    else:
        print(f"Static: {part}")         # 'Try some ', ' cheese!'

# Use case: SQL sanitization, HTML escaping, custom DSLs

# Walrus operator :=
if (n := len(scores)) > 2:
    print(f"Got {n} scores")

# Match statement (3.10+)
match command:
    case "quit":
        exit()
    case "hello" | "hi":
        print("Hello!")
    case {"action": "move", "x": x, "y": y}:
        move(x, y)
    case [first, *rest]:
        print(f"First: {first}, rest: {rest}")
    case _:
        print("Unknown")

# Bracketless except (3.14+ — PEP 758)
try:
    risky_operation()
except ValueError, TypeError:  # no parentheses needed in 3.14+!
    handle_error()
```

## Data Structures

```python
# List comprehension
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
flat = [item for sublist in nested for item in sublist]

# Dict comprehension
word_counts = {word: len(word) for word in words}
filtered = {k: v for k, v in data.items() if v > 0}

# Set operations
a = {1, 2, 3}
b = {2, 3, 4}
a | b  # union: {1, 2, 3, 4}
a & b  # intersection: {2, 3}
a - b  # difference: {1}
a ^ b  # symmetric difference: {1, 4}

# Unpacking
first, *rest = [1, 2, 3, 4]     # first=1, rest=[2,3,4]
merged = {**dict1, **dict2}
combined = [*list1, *list2]

# Named tuple
from typing import NamedTuple
class Point(NamedTuple):
    x: float
    y: float
    z: float = 0.0
```

## Functions & Classes

```python
# Type-hinted function
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"

# *args, **kwargs
def func(*args: int, **kwargs: str) -> None:
    print(args, kwargs)

# Decorators
from functools import wraps

def retry(max_attempts: int = 3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Retry {attempt + 1}/{max_attempts}: {e}")
        return wrapper
    return decorator

@retry(max_attempts=3)
async def fetch_data(url: str) -> dict:
    ...

# Dataclass (preferred for data containers)
from dataclasses import dataclass, field

@dataclass
class User:
    name: str
    email: str
    age: int = 0
    tags: list[str] = field(default_factory=list)

    def is_adult(self) -> bool:
        return self.age >= 18

# Frozen dataclass (immutable)
@dataclass(frozen=True)
class Config:
    host: str
    port: int = 8080

# Protocol (structural typing, like TS interface)
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...

# Abstract class
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

# Enum
from enum import Enum, auto

class Status(Enum):
    ACTIVE = auto()
    INACTIVE = auto()
    PENDING = "pending"
```

## Async/Await

```python
import asyncio
import aiohttp

async def fetch(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

# Concurrent execution
async def main():
    results = await asyncio.gather(
        fetch("https://api.example.com/a"),
        fetch("https://api.example.com/b"),
        fetch("https://api.example.com/c"),
    )
    return results

asyncio.run(main())

# TaskGroup (3.11+)
async with asyncio.TaskGroup() as tg:
    task1 = tg.create_task(fetch(url1))
    task2 = tg.create_task(fetch(url2))
# Both tasks complete here, exceptions propagate

# Async generator
async def stream_data():
    async for chunk in response.content.iter_any():
        yield chunk

# Semaphore (limit concurrency)
sem = asyncio.Semaphore(10)
async def limited_fetch(url):
    async with sem:
        return await fetch(url)
```

## FastAPI (Web Framework)

```python
from fastapi import FastAPI, HTTPException, Depends, Query, Path
from pydantic import BaseModel, Field, EmailStr

app = FastAPI(title="My API", version="1.0.0")

# Pydantic model (request/response validation)
class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)
    tags: list[str] = []

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    model_config = {"from_attributes": True}  # read from ORM objects

# Endpoints
@app.get("/users", response_model=list[UserResponse])
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    q: str | None = None,
):
    users = await db.get_users(skip=skip, limit=limit, search=q)
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int = Path(..., gt=0)):
    user = await db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    return await db.create_user(user.model_dump())

# Dependency injection
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = await verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

@app.get("/me")
async def read_me(user: User = Depends(get_current_user)):
    return user

# Run: uvicorn main:app --reload
```

## File I/O & Pathlib

```python
from pathlib import Path

# Path operations
p = Path("src") / "utils" / "helper.py"
p.exists()
p.is_file()
p.suffix        # '.py'
p.stem          # 'helper'
p.parent        # Path('src/utils')
p.name          # 'helper.py'

# Read/write
content = Path("data.json").read_text(encoding="utf-8")
Path("output.txt").write_text("hello", encoding="utf-8")

# Glob
for py_file in Path("src").rglob("*.py"):
    print(py_file)

# JSON
import json
data = json.loads(json_string)
json_string = json.dumps(data, indent=2, ensure_ascii=False)
```

## Common Standard Library

```python
# collections
from collections import Counter, defaultdict, deque
Counter("hello")          # {'l': 2, 'h': 1, ...}
dd = defaultdict(list)    # auto-create list for missing keys

# itertools
from itertools import chain, groupby, islice, product, combinations, batched
list(chain([1,2], [3,4]))  # [1, 2, 3, 4]
list(batched(range(10), 3))  # [(0,1,2), (3,4,5), (6,7,8), (9,)]  # 3.12+

# functools
from functools import lru_cache, cache, partial, reduce

@cache  # unlimited cache (3.9+)
def fib(n: int) -> int:
    return n if n < 2 else fib(n-1) + fib(n-2)

# contextlib
from contextlib import contextmanager, asynccontextmanager

@contextmanager
def timer():
    import time
    start = time.time()
    yield
    print(f"Took {time.time() - start:.3f}s")

# subprocess
import subprocess
result = subprocess.run(["git", "status"], capture_output=True, text=True, check=True)
print(result.stdout)

# logging
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)
logger.info("Processing %d items", count)
```

## Virtual Environments & Packaging

```bash
# venv
python -m venv .venv
source .venv/bin/activate    # Linux/macOS
.venv\Scripts\activate       # Windows

# pip
pip install fastapi uvicorn
pip install -r requirements.txt
pip freeze > requirements.txt

# uv (fast alternative — recommended)
uv venv
uv pip install fastapi
uv pip compile requirements.in -o requirements.txt
uv run python script.py  # auto-creates venv and installs
```

## Generics & Advanced Typing (3.12+)

```python
# Generic functions (3.12+)
def first[T](items: list[T]) -> T | None:
    return items[0] if items else None

# Generic classes (3.12+)
class Stack[T]:
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

# TypeVar with bounds (3.12+)
from typing import SupportsFloat
def average[T: SupportsFloat](items: list[T]) -> float:
    return sum(float(x) for x in items) / len(items)

# TypedDict
from typing import TypedDict, Required, NotRequired

class Movie(TypedDict):
    title: Required[str]
    year: Required[int]
    director: NotRequired[str]
```

## Gotchas

⚠️ **Mutable defaults**: `def f(items=[])` shares list across calls. Use `items=None` + `items = items or []`.

⚠️ **`is` vs `==`**: `is` checks identity (same object), `==` checks equality.

⚠️ **GIL**: Global Interpreter Lock limits true parallelism. Use `asyncio` for I/O-bound, `multiprocessing` for CPU-bound.

⚠️ **3.14 free-threaded**: Now officially supported (no longer experimental). Use `python3.14t` binary.

⚠️ **Type hints NOT enforced**: Runtime ignores them. Use `mypy` or `pyright` for static checking.

⚠️ **Template strings `t""` ≠ f-strings**: t-strings return `Template` object, NOT `str`. Must process explicitly.

⚠️ **`@cache` vs `@lru_cache`**: `@cache` (3.9+) is unlimited. `@lru_cache(maxsize=128)` evicts old entries.

⚠️ **`asyncio.run()`**: Can only be called once. Don't call inside already-running loop.

⚠️ **Deferred annotations (3.14+)**: Annotations evaluated lazily now. Use `typing.get_type_hints()` or `annotationlib.get_annotations()` to resolve.

⚠️ **Zstandard (3.14+)**: Use `compression.zstd` module for high-performance compression. Replaces third-party `zstandard`.
