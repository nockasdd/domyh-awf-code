---
name: python
detect: ["pyproject.toml", "requirements.txt", "*.py", "Pipfile", "setup.py"]
version: "6.4.3"
category: backend
tier: 1
---

# Python Patterns — DOMYH Awesome Code

> **Version**: Python 3.12/3.13 (2025-2026)
> **Frameworks**: FastAPI, Django 5+
> **Philosophy**: Type-safe, async-first, batteries included

---

## 🎯 When to Use This Skill

Use for: Web APIs, data science, ML/AI, automation, scripting.
**NOT for**: High-performance systems (→ rust), mobile apps (→ flutter/kotlin).

---

## 📦 Recommended Stack (2025-2026)

### Web Frameworks

| Framework    | Use Case            | Install                       |
| ------------ | ------------------- | ----------------------------- |
| **FastAPI**  | APIs, async, ML 🏆  | `pip install fastapi uvicorn` |
| **Django 5** | Full-stack, admin   | `pip install django`          |
| **Litestar** | FastAPI alternative | `pip install litestar`        |

### Data & ML

| Category | Libraries               | Install                 |
| -------- | ----------------------- | ----------------------- |
| **Data** | pandas, polars 🏆       | `pip install polars`    |
| **ML**   | scikit-learn, pytorch   | `pip install torch`     |
| **LLM**  | transformers, langchain | `pip install langchain` |
| **Viz**  | plotly, seaborn         | `pip install plotly`    |

### Utilities

| Library          | Use Case                | Install                  |
| ---------------- | ----------------------- | ------------------------ |
| **Pydantic v2**  | Validation 🏆           | `pip install pydantic`   |
| **httpx**        | Async HTTP              | `pip install httpx`      |
| **SQLAlchemy 2** | ORM                     | `pip install sqlalchemy` |
| **pytest**       | Testing                 | `pip install pytest`     |
| **ruff**         | Linting + formatting 🏆 | `pip install ruff`       |

### IDE Support

| IDE         | Features                             |
| ----------- | ------------------------------------ |
| **PyCharm** | Full-featured, debugging, testing 🏆 |
| **VS Code** | Python extension, Pylance, Jupyter   |

---

## 🆕 Python 3.12/3.13 Features

### Free-Threaded Mode (3.13 Experimental)

```python
# ✅ Python 3.13 with --disable-gil (experimental)
# True multi-threading without GIL
import threading

def cpu_intensive():
    return sum(i * i for i in range(10_000_000))

# With free-threading, these run in parallel
threads = [threading.Thread(target=cpu_intensive) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

### JIT Compiler (3.13 Experimental)

```bash
# Enable JIT for performance
python -X jit script.py
```

### Improved Error Messages

```python
# Python 3.12+ provides precise error locations
def process(data):
    return data["user"]["profile"]["avatar"]["url"]
    #                             ~~~~~~~^^^^^^^
    # KeyError: 'avatar'
```

### Type Parameter Syntax (3.12)

```python
# ✅ New generic syntax (3.12+)
def first[T](items: list[T]) -> T | None:
    return items[0] if items else None

class Stack[T]:
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

# ✅ @override decorator (3.12+)
from typing import override

class Animal:
    def speak(self) -> str:
        return "..."

class Dog(Animal):
    @override
    def speak(self) -> str:
        return "Woof!"
```

---

## 🚀 FastAPI Best Practices

### Project Structure

```
src/
├── main.py
├── config.py
├── database.py
├── routers/
│   ├── __init__.py
│   ├── users.py
│   └── posts.py
├── schemas/
│   ├── __init__.py
│   ├── user.py
│   └── post.py
├── models/
│   ├── __init__.py
│   └── user.py
├── services/
│   ├── __init__.py
│   └── user_service.py
└── dependencies.py
tests/
├── conftest.py
├── test_users.py
└── test_posts.py
```

### Dependency Injection Pattern

```python
# src/dependencies.py
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_db
from .services.user_service import UserService

async def get_user_service(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> UserService:
    return UserService(db)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
```

### Router with Async Endpoints

```python
# src/routers/users.py
from fastapi import APIRouter, HTTPException, status
from typing import Annotated

from ..schemas.user import UserCreate, UserResponse, UserList
from ..dependencies import UserServiceDep

router = APIRouter(prefix="/users", tags=["users"])

@router.get("", response_model=UserList)
async def list_users(
    service: UserServiceDep,
    page: int = 1,
    per_page: int = 20,
) -> UserList:
    """List all users with pagination."""
    return await service.list(page=page, per_page=per_page)

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    service: UserServiceDep,
    data: UserCreate,
) -> UserResponse:
    """Create a new user."""
    user = await service.create(data)
    return user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    service: UserServiceDep,
    user_id: int,
) -> UserResponse:
    """Get user by ID."""
    user = await service.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user
```

### Pydantic v2 Schemas

```python
# src/schemas/user.py
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(min_length=2, max_length=100)

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserList(BaseModel):
    items: list[UserResponse]
    total: int
    page: int
    per_page: int
```

---

## 🔄 Async Patterns

### asyncio TaskGroup (3.12+)

```python
import asyncio

async def fetch_all_data():
    async with asyncio.TaskGroup() as tg:
        user_task = tg.create_task(fetch_user())
        posts_task = tg.create_task(fetch_posts())
        comments_task = tg.create_task(fetch_comments())

    # All tasks completed or exception raised
    return {
        "user": user_task.result(),
        "posts": posts_task.result(),
        "comments": comments_task.result(),
    }
```

### Blocking Operations

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

# ✅ Use asyncio.to_thread for blocking I/O
async def process_file(path: str) -> str:
    content = await asyncio.to_thread(read_file_sync, path)
    return content

# ✅ Custom executor for CPU-bound
executor = ThreadPoolExecutor(max_workers=4)

async def cpu_intensive_task(data: bytes) -> bytes:
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, process_data, data)
    return result
```

### Async Context Managers

```python
from contextlib import asynccontextmanager
from typing import AsyncGenerator

@asynccontextmanager
async def database_transaction() -> AsyncGenerator[AsyncSession, None]:
    session = async_session()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()

# Usage
async def create_user(data: UserCreate):
    async with database_transaction() as session:
        user = User(**data.model_dump())
        session.add(user)
        return user
```

---

## 🐍 Django 5 Patterns

### Modern Model

```python
# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True)

    class Meta:
        ordering = ["-date_joined"]

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["author", "-created_at"]),
        ]
```

### Async Views (Django 5+)

```python
# views.py
from django.http import JsonResponse
from asgiref.sync import sync_to_async

async def list_posts(request):
    posts = await sync_to_async(list)(
        Post.objects.select_related("author")[:20]
    )
    return JsonResponse({
        "posts": [
            {"id": p.id, "title": p.title, "author": p.author.username}
            for p in posts
        ]
    })
```

---

## 🧪 Testing with pytest

```python
# tests/test_users.py
import pytest
from httpx import AsyncClient, ASGITransport

from src.main import app

@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client

class TestUserAPI:
    @pytest.mark.asyncio
    async def test_create_user(self, client: AsyncClient):
        response = await client.post("/users", json={
            "email": "test@example.com",
            "name": "Test User",
            "password": "password123",
        })

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"

    @pytest.mark.asyncio
    async def test_get_nonexistent_user(self, client: AsyncClient):
        response = await client.get("/users/99999")
        assert response.status_code == 404

# ✅ Parametrized tests
@pytest.mark.parametrize("email,valid", [
    ("valid@example.com", True),
    ("invalid", False),
    ("", False),
])
def test_email_validation(email: str, valid: bool):
    from src.schemas.user import UserCreate
    if valid:
        UserCreate(email=email, name="Test", password="password123")
    else:
        with pytest.raises(ValueError):
            UserCreate(email=email, name="Test", password="password123")
```

---

## 📊 Type Hints Best Practices

```python
from typing import Annotated, Literal, TypeAlias
from collections.abc import Callable, Awaitable

# ✅ Use native types (3.9+)
def process(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# ✅ Union with | (3.10+)
def find_user(id: int) -> User | None:
    return db.query(User).get(id)

# ✅ TypeAlias for complex types
JsonDict: TypeAlias = dict[str, "JsonValue"]
JsonValue: TypeAlias = str | int | float | bool | None | list["JsonValue"] | JsonDict

# ✅ Literal for specific values
def set_status(status: Literal["active", "inactive", "pending"]) -> None:
    ...

# ✅ Annotated for validation
from pydantic import Field
UserId = Annotated[int, Field(gt=0)]

# ✅ Callable types
Handler: TypeAlias = Callable[[Request], Awaitable[Response]]
```

---

## ✅ Production Checklist

### Code Quality

- [ ] Type hints complete
- [ ] ruff linting passing
- [ ] mypy/pyright type checking
- [ ] Docstrings on public APIs
- [ ] Python 3.12+ features used

### Performance

- [ ] Async for I/O operations
- [ ] Connection pooling (databases)
- [ ] Caching implemented (Redis)
- [ ] Profiling done (cProfile)

### Testing

- [ ] pytest tests passing
- [ ] Test coverage > 80%
- [ ] Async tests with pytest-asyncio
- [ ] Integration tests included

### Security

- [ ] Input validation (Pydantic)
- [ ] SQL injection prevented (ORM)
- [ ] Secrets in environment variables
- [ ] Dependencies audited

---

_DOMYH Awesome Code • Python 3.12/3.13_
