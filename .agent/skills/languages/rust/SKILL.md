---
name: rust
detect: ["Cargo.toml", "*.rs", "Cargo.lock"]
version: "6.3.1"
category: systems
tier: 1
---

# Rust Patterns — DOMYH Awesome Code

> **Version**: Rust 1.80+ (2025-2026)
> **Philosophy**: Zero-cost abstractions, fearless concurrency, memory safety

---

## 🎯 When to Use This Skill

Use for: Systems programming, CLI tools, WebAssembly, high-performance services.
**NOT for**: Rapid prototyping (→ python), web frontends (→ typescript).

---

## 📦 Recommended Stack (2025-2026)

### Async Runtime

- **Tokio** - De-facto async runtime 🏆

### Web Frameworks

| Library       | Use Case              | Cargo             |
| ------------- | --------------------- | ----------------- |
| **Axum**      | Tokio-based, Tower 🏆 | `axum = "0.8"`    |
| **Actix-web** | High performance      | `actix-web = "4"` |

### Database

| Library     | Use Case            |
| ----------- | ------------------- |
| **sqlx**    | Compile-time SQL 🏆 |
| **diesel**  | Full ORM            |
| **sea-orm** | Async ORM           |

### Utilities

- **serde** - Serialization (indispensable)
- **tracing** - Structured logging 🏆
- **anyhow/thiserror** - Error handling
- **clap** - CLI parsing
- **reqwest** - HTTP client

### IDE Support

| IDE           | Extension        | Features                   |
| ------------- | ---------------- | -------------------------- |
| **VS Code**   | rust-analyzer 🏆 | Auto-complete, diagnostics |
| **RustRover** | Built-in         | Full debugging, AI assist  |
| **CLion**     | Rust plugin      | Advanced debugging         |

---

## 🆕 Rust 2025-2026 Features

### Async Traits (Stable)

```rust
// ✅ Async traits now stable
trait Repository {
    async fn find(&self, id: u32) -> Option<User>;
    async fn save(&self, user: &User) -> Result<(), Error>;
}

struct PostgresRepo { pool: PgPool }

impl Repository for PostgresRepo {
    async fn find(&self, id: u32) -> Option<User> {
        sqlx::query_as("SELECT * FROM users WHERE id = $1")
            .bind(id)
            .fetch_optional(&self.pool)
            .await
            .ok()
            .flatten()
    }
}
```

### Type Inference Improvements

```rust
// ✅ Better inference for iterators and closures
let numbers = vec![1, 2, 3, 4, 5];
let doubled: Vec<_> = numbers.iter().map(|x| x * 2).collect();
```

---

## 🏗️ Project Structure

```
my-crate/
├── Cargo.toml
├── src/
│   ├── main.rs          # Binary entry
│   ├── lib.rs           # Library root
│   ├── config.rs
│   ├── error.rs
│   ├── routes/
│   │   ├── mod.rs
│   │   └── users.rs
│   ├── services/
│   │   ├── mod.rs
│   │   └── user_service.rs
│   └── models/
│       ├── mod.rs
│       └── user.rs
└── tests/
    └── integration.rs
```

---

## 🔧 Axum Web Patterns

### Basic Router

```rust
use axum::{
    routing::{get, post},
    Router, Json, extract::{State, Path},
};
use std::sync::Arc;

struct AppState {
    db: PgPool,
}

#[tokio::main]
async fn main() {
    let state = Arc::new(AppState {
        db: PgPool::connect(&std::env::var("DATABASE_URL").unwrap())
            .await
            .unwrap(),
    });

    let app = Router::new()
        .route("/users", get(list_users).post(create_user))
        .route("/users/:id", get(get_user).put(update_user))
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

### Handler Functions

```rust
use axum::{extract::{State, Path, Json}, http::StatusCode};
use serde::{Deserialize, Serialize};

#[derive(Serialize)]
struct User {
    id: i32,
    name: String,
    email: String,
}

#[derive(Deserialize)]
struct CreateUser {
    name: String,
    email: String,
}

async fn list_users(
    State(state): State<Arc<AppState>>,
) -> Result<Json<Vec<User>>, StatusCode> {
    let users = sqlx::query_as!(User, "SELECT * FROM users")
        .fetch_all(&state.db)
        .await
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;

    Ok(Json(users))
}

async fn create_user(
    State(state): State<Arc<AppState>>,
    Json(payload): Json<CreateUser>,
) -> Result<(StatusCode, Json<User>), StatusCode> {
    let user = sqlx::query_as!(
        User,
        "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *",
        payload.name,
        payload.email
    )
    .fetch_one(&state.db)
    .await
    .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;

    Ok((StatusCode::CREATED, Json(user)))
}
```

---

## ⚡ Async Best Practices

### TaskGroup Pattern

```rust
use tokio::task::JoinSet;

async fn fetch_all() -> Vec<User> {
    let mut set = JoinSet::new();

    for id in 1..=10 {
        set.spawn(fetch_user(id));
    }

    let mut users = Vec::new();
    while let Some(result) = set.join_next().await {
        if let Ok(Some(user)) = result {
            users.push(user);
        }
    }
    users
}
```

### Blocking Operations

```rust
// ✅ Offload blocking I/O to thread pool
async fn read_large_file(path: String) -> std::io::Result<Vec<u8>> {
    tokio::task::spawn_blocking(move || {
        std::fs::read(&path)
    })
    .await
    .unwrap()
}
```

### Concurrent Requests

```rust
use tokio::try_join;

async fn fetch_dashboard_data() -> Result<DashboardData, Error> {
    let (user, posts, stats) = try_join!(
        fetch_user(),
        fetch_posts(),
        fetch_stats()
    )?;

    Ok(DashboardData { user, posts, stats })
}
```

---

## 🛡️ Error Handling

### thiserror Pattern

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("User not found: {0}")]
    UserNotFound(i32),

    #[error("Database error")]
    Database(#[from] sqlx::Error),

    #[error("Validation error: {0}")]
    Validation(String),
}

// Axum integration
impl axum::response::IntoResponse for AppError {
    fn into_response(self) -> axum::response::Response {
        let (status, message) = match &self {
            AppError::UserNotFound(_) => (StatusCode::NOT_FOUND, self.to_string()),
            AppError::Database(_) => (StatusCode::INTERNAL_SERVER_ERROR, "Database error".into()),
            AppError::Validation(msg) => (StatusCode::BAD_REQUEST, msg.clone()),
        };

        (status, Json(serde_json::json!({ "error": message }))).into_response()
    }
}
```

### Result Pattern

```rust
// ✅ Use ? operator for clean error propagation
async fn get_user(id: i32) -> Result<User, AppError> {
    let user = sqlx::query_as!(User, "SELECT * FROM users WHERE id = $1", id)
        .fetch_optional(&db)
        .await?
        .ok_or(AppError::UserNotFound(id))?;

    Ok(user)
}
```

---

## 🧪 Testing

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use axum::http::StatusCode;
    use axum_test::TestServer;

    #[tokio::test]
    async fn test_list_users() {
        let app = create_app().await;
        let server = TestServer::new(app).unwrap();

        let response = server.get("/users").await;

        response.assert_status(StatusCode::OK);
        let users: Vec<User> = response.json();
        assert!(!users.is_empty());
    }

    #[tokio::test]
    async fn test_create_user() {
        let app = create_app().await;
        let server = TestServer::new(app).unwrap();

        let response = server
            .post("/users")
            .json(&CreateUser {
                name: "Test".into(),
                email: "test@example.com".into(),
            })
            .await;

        response.assert_status(StatusCode::CREATED);
        let user: User = response.json();
        assert_eq!(user.name, "Test");
    }
}
```

---

## ✅ Best Practices Checklist

### Code Quality

- [ ] `cargo clippy` passes
- [ ] `cargo fmt` applied
- [ ] No `unwrap()` in production
- [ ] Proper error types with thiserror

### Performance

- [ ] Async for I/O operations
- [ ] `spawn_blocking` for CPU tasks
- [ ] Connection pooling (sqlx)
- [ ] Zero-copy where possible

### Safety

- [ ] No unsafe without justification
- [ ] Ownership patterns clear
- [ ] Lifetimes properly annotated
- [ ] Thread safety verified

---

_DOMYH Awesome Code • Rust 2025_
