# Rust — Advanced Patterns

# DOMYH Awesome Code v5.5 — Tier 3 Reference

## Table of Contents

- [Ownership Patterns](#ownership-patterns)
- [Async Rust](#async-rust)
- [Error Handling](#error-handling)
- [Unsafe & FFI](#unsafe--ffi)

---

## Ownership Patterns

### Interior Mutability

```rust
use std::cell::{Cell, RefCell};
use std::rc::Rc;

// Cell for Copy types
struct Counter {
    count: Cell<u32>,
}

impl Counter {
    fn increment(&self) {
        self.count.set(self.count.get() + 1);
    }
}

// RefCell for non-Copy types
struct Cache {
    data: RefCell<HashMap<String, String>>,
}

impl Cache {
    fn get_or_insert(&self, key: &str) -> String {
        let mut data = self.data.borrow_mut();
        data.entry(key.to_string())
            .or_insert_with(|| fetch(key))
            .clone()
    }
}
```

### Arc + Mutex Pattern

```rust
use std::sync::{Arc, Mutex};
use std::thread;

struct SharedState {
    data: Arc<Mutex<Vec<i32>>>,
}

impl SharedState {
    fn new() -> Self {
        Self { data: Arc::new(Mutex::new(Vec::new())) }
    }

    fn spawn_worker(&self) -> thread::JoinHandle<()> {
        let data = Arc::clone(&self.data);
        thread::spawn(move || {
            let mut guard = data.lock().unwrap();
            guard.push(42);
        })
    }
}
```

---

## Async Rust

### Tokio Runtime

```rust
use tokio::sync::mpsc;
use tokio::time::{timeout, Duration};

async fn fetch_with_timeout(url: &str) -> Result<Response, Error> {
    timeout(Duration::from_secs(30), reqwest::get(url))
        .await
        .map_err(|_| Error::Timeout)?
        .map_err(Error::Network)
}

// Channel-based worker
async fn worker(mut rx: mpsc::Receiver<Job>) {
    while let Some(job) = rx.recv().await {
        process(job).await;
    }
}
```

### Select Pattern

```rust
use tokio::select;

async fn race_requests(urls: Vec<&str>) -> Result<Response, Error> {
    let futures: Vec<_> = urls.iter()
        .map(|url| Box::pin(fetch(url)))
        .collect();

    select! {
        result = futures[0] => result,
        result = futures[1] => result,
        _ = tokio::time::sleep(Duration::from_secs(5)) => {
            Err(Error::Timeout)
        }
    }
}
```

---

## Error Handling

### Custom Error Types

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),

    #[error("Not found: {resource} with id {id}")]
    NotFound { resource: String, id: String },

    #[error("Validation failed")]
    Validation(#[source] ValidationError),
}

// With anyhow for applications
use anyhow::{Context, Result};

fn load_config() -> Result<Config> {
    let content = std::fs::read_to_string("config.toml")
        .context("Failed to read config file")?;
    toml::from_str(&content)
        .context("Failed to parse config")
}
```

---

## Unsafe & FFI

### Safe Abstraction over Unsafe

```rust
pub struct Buffer {
    ptr: *mut u8,
    len: usize,
    cap: usize,
}

impl Buffer {
    pub fn new(cap: usize) -> Self {
        let layout = Layout::array::<u8>(cap).unwrap();
        let ptr = unsafe { alloc(layout) };
        Self { ptr, len: 0, cap }
    }

    pub fn push(&mut self, byte: u8) {
        assert!(self.len < self.cap);
        unsafe {
            self.ptr.add(self.len).write(byte);
        }
        self.len += 1;
    }
}

impl Drop for Buffer {
    fn drop(&mut self) {
        unsafe {
            let layout = Layout::array::<u8>(self.cap).unwrap();
            dealloc(self.ptr, layout);
        }
    }
}
```

### C FFI

```rust
use std::ffi::{CStr, CString};
use std::os::raw::c_char;

extern "C" {
    fn external_process(input: *const c_char) -> *mut c_char;
}

pub fn safe_process(input: &str) -> Result<String, Error> {
    let c_input = CString::new(input)?;
    let result = unsafe { external_process(c_input.as_ptr()) };
    if result.is_null() {
        return Err(Error::NullPointer);
    }
    let c_str = unsafe { CStr::from_ptr(result) };
    Ok(c_str.to_string_lossy().into_owned())
}
```

---

_DOMYH Awesome Code v6.0.0 — Tier 3 Reference_
