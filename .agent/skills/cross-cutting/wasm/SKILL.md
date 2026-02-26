---
name: wasm
category: cross-cutting
---

# WebAssembly — WASM • WASI • Component Model

> Browser WASM • Server-side WASM • Near-native performance

---

## Khi Nào Dùng

- Chạy compute-intensive code trong browser (image/video processing, games)
- Server-side WASM cho lightweight serverless functions
- Port native code (Rust/C++) sang web platform
- Cross-language component sharing via WIT

## Architecture

```

> Browser / Server Runtime
> 
>     WASM Runtime           
>   (V8, wasmtime, wasmer)   
>     
>      WASM Module         
>     (compiled Rust/Go)   
>     
> 
> ↕ WASI System Interface
```

## Browser WASM (wasm-bindgen)

```rust
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn add(a: i32, b: i32) -> i32 { a + b }

// Build: wasm-pack build --target web
```

```javascript
import init, { add } from "./pkg/my_wasm.js";
await init();
console.log(add(2, 3)); // 5
```

## Server-side WASM (Spin)

```rust
use spin_sdk::http::{Request, Response};

#[spin_sdk::http_component]
fn handle_request(req: Request) -> Response {
    Response::builder()
        .status(200)
        .body("Hello from WASM!")
        .build()
}
```

## WIT Interface (Component Model)

```wit
package example:calculator;

interface operations {
    add: func(a: f64, b: f64) -> f64;
    multiply: func(a: f64, b: f64) -> f64;
}

world calculator {
    export operations;
}
```

## Common Traps

| Trap            | Fix                               |
| --------------- | --------------------------------- |
| Large WASM file | Use wasm-opt, tree shaking        |
| DOM access      | Use wasm-bindgen JS interop       |
| Threading       | SharedArrayBuffer + Web Workers   |
| Debugging       | Use DWARF debug info, source maps |

---
