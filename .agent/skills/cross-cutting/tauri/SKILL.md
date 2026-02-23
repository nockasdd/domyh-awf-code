---
name: tauri
version: "6.4.0"
category: cross-cutting
---

# Tauri 2.0 — Desktop & Mobile Apps

> Rust core • System WebView • Capability-based Security  
> Cross-platform: Windows, macOS, Linux, iOS, Android

---

## Khi Nào Dùng

- Build desktop app với frontend framework (React/Vue/Svelte/Solid)
- Cần app size nhỏ (~3-10MB vs Electron ~150MB+)
- Cần security mạnh (capability-based, no Node.js)
- Cần support cả mobile (iOS/Android) via Tauri 2.0

## Tauri vs Electron

| Feature         | Tauri 2.0                | Electron         |
| --------------- | ------------------------ | ---------------- |
| **Bundle size** | ~3-10MB                  | ~150-300MB       |
| **Memory**      | ~30-80MB                 | ~100-400MB       |
| **Backend**     | Rust                     | Node.js          |
| **WebView**     | System (WebView2/WebKit) | Bundled Chromium |
| **Security**    | Capability-based         | Manual CSP       |
| **Mobile**      | ✅ iOS + Android         | ❌ Desktop only  |
| **Maturity**    | Growing (2.0)            | Mature           |

## Architecture

```
┌──────────────────────────────────────┐
│         Frontend (WebView)           │
│    React / Vue / Svelte / Solid      │
│         @tauri-apps/api              │
└───────────┬──────────────────────────┘
            │ IPC (invoke/listen/emit)
┌───────────▼──────────────────────────┐
│         Rust Core (src-tauri/)       │
│    Commands • Plugins • State        │
│    File System • Shell • HTTP        │
└──────────────────────────────────────┘
```

## Core Patterns

### IPC: Frontend ↔ Rust

```typescript
// Frontend: invoke Rust command
import { invoke } from "@tauri-apps/api/core";
const result = await invoke("greet", { name: "World" });

// Frontend: listen to events
import { listen } from "@tauri-apps/api/event";
await listen("file-changed", (event) => console.log(event.payload));
```

```rust
// Rust: define command
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

// Rust: emit event
app.emit("file-changed", payload)?;

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet])
        .run(tauri::generate_context!())
        .expect("error running tauri app");
}
```

### Capability-based Security

```json
// src-tauri/capabilities/main.json
{
  "identifier": "main-capability",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "fs:allow-read-text-file",
    "dialog:allow-open"
  ]
}
```

**Rules**:

- ✅ Grant minimal permissions per window
- ✅ Use scoped access (specific directories)
- ❌ Never use `fs:default` (grants all fs access)

### Plugins

```rust
// Using official plugin
tauri::Builder::default()
    .plugin(tauri_plugin_fs::init())
    .plugin(tauri_plugin_dialog::init())
    .plugin(tauri_plugin_shell::init())
```

| Plugin         | Purpose              |
| -------------- | -------------------- |
| `fs`           | File system access   |
| `dialog`       | Open/save dialogs    |
| `shell`        | Run system commands  |
| `http`         | HTTP requests        |
| `notification` | System notifications |
| `clipboard`    | Clipboard access     |
| `updater`      | Auto-updates         |

## Common Traps

| Trap                | Fix                                                  |
| ------------------- | ---------------------------------------------------- |
| WebView differences | Test on all platforms (WebView2, WebKit)             |
| Large binary        | Use `cargo build --release`, strip debug symbols     |
| IPC serialization   | Use `serde` correctly, avoid large payloads          |
| Permissions denied  | Check capabilities/\*.json, add required permissions |

---

_DOMYH Awesome Code • Tauri Skill v1.0.0_
