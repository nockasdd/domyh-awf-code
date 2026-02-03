---
name: dev
trigger: ["/dev", "start", "run dev", "chạy"]
persona: developer
description: "▶️ Start development server: detect stack, run dev commands, validate output"
---

# ▶️ /dev — Dev Pro v3.1

> Intelligent Development Runner
> 📚 30+ Languages • Auto-detect • Hot Reload

---

## 🔄 DEV FLOW

```
User: /dev [options]
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 1: DETECT                         │
│ ▸ Identify project stack                │
│ ▸ Find config files                     │
│ ▸ Check dependencies                    │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 2: PREPARE                        │
│ ▸ Install deps if needed                │
│ ▸ Set environment                       │
│ ▸ Check ports                           │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 3: START                          │
│ ▸ Run dev command                       │
│ ▸ Watch for output                      │
│ ▸ Report URL/port                       │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 4: VALIDATE                       │
│ ▸ Health check                          │
│ ▸ Open browser (optional)               │
│ ▸ Watch for errors                      │
└─────────────────────────────────────────┘
```

---

## 🎯 COMMANDS

| Command           | Description       |
| ----------------- | ----------------- |
| `/dev`            | Start dev server  |
| `/dev stop`       | Stop server       |
| `/dev restart`    | Restart server    |
| `/dev logs`       | View logs         |
| `/dev port [num]` | Use specific port |

---

## 🔧 DEV COMMANDS BY STACK

```yaml
# ═══════════════════════════════════════════════════════════════
# DEVELOPMENT COMMANDS BY LANGUAGE/FRAMEWORK
# ═══════════════════════════════════════════════════════════════

commands:
  # Node.js / TypeScript
  typescript:
    detect: ["package.json", "tsconfig.json"]
    dev:
      - "npm run dev"
      - "yarn dev"
      - "pnpm dev"
    frameworks:
      nextjs: "next dev"
      vite: "vite"
      remix: "remix dev"
      nuxt: "nuxt dev"

  # Go
  go:
    detect: ["go.mod", "main.go"]
    dev:
      - "go run ."
      - "air" # Hot reload
    frameworks:
      gin: "go run main.go"
      fiber: "go run main.go"

  # Python
  python:
    detect: ["requirements.txt", "pyproject.toml", "setup.py"]
    dev:
      - "python main.py"
      - "uvicorn main:app --reload"
    frameworks:
      fastapi: "uvicorn main:app --reload"
      django: "python manage.py runserver"
      flask: "flask run --reload"

  # Rust
  rust:
    detect: ["Cargo.toml"]
    dev:
      - "cargo run"
      - "cargo watch -x run" # Hot reload

  # Java
  java:
    detect: ["pom.xml", "build.gradle"]
    dev:
      maven: "mvn spring-boot:run"
      gradle: "./gradlew bootRun"

  # C#/.NET
  csharp:
    detect: ["*.csproj", "*.sln"]
    dev: "dotnet run --watch"

  # PHP
  php:
    detect: ["composer.json"]
    dev:
      laravel: "php artisan serve"
      symfony: "symfony server:start"

  # Ruby
  ruby:
    detect: ["Gemfile"]
    dev:
      rails: "rails server"
      sinatra: "ruby app.rb"
```

---

## 📊 OUTPUT FORMAT

```markdown
▶️ DEV SERVER STARTED

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Stack: Next.js 14 + TypeScript
Command: npm run dev
Port: 3000

🌐 Local: http://localhost:3000
🌐 Network: http://192.168.1.100:3000

✅ Server ready in 2.3s

Watching for changes...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Commands:

- /dev stop → Stop server
- /dev restart → Restart
- /dev logs → View full logs
```

---

## 🔧 HOT RELOAD TOOLS

```yaml
hot_reload:
  go: "air"
  rust: "cargo-watch"
  python: "uvicorn --reload"
  node: "nodemon"
  dotnet: "dotnet watch"
```

---

## ⚙️ TOKEN OPTIMIZATION

```yaml
token_saving:
  - Auto-detect stack (no manual config)
  - Concise output
  - Only show errors/warnings
```

---

## ⚡ HMR 2025 STANDARDS (v3.1)

```yaml
hmr_optimization:
  description: "Sub-100ms hot module replacement"

  targets:
    module_update: "< 100ms"
    full_reload: "< 1s for config changes"
    state_preservation: "React/Vue state maintained"
    cold_start: "< 3s for large projects"

  native_esm:
    description: "No dev bundling needed"
    benefits:
      - "Instant cold start"
      - "On-demand compilation"
      - "Browser caching"
      - "Parallel module resolution"

  performance_patterns:
    dynamic_imports: "Lazy load non-critical modules"
    barrel_exports: "Avoid large re-exports"
    circular_deps: "Detect and warn"

  anti_patterns:
    - "Large barrel exports (index.ts)"
    - "Circular dependencies"
    - "Sync dynamic imports"
    - "Importing entire libraries"

  tools:
    vite: "Native ESM, < 50ms updates"
    turbopack: "Rust-based, incremental compute"
    rspack: "Rust port of webpack"

  commands:
    check: "/dev optimize check"
    fix: "/dev optimize fix"
    benchmark: "/dev optimize benchmark"
```

---

## 🚨 ERROR OVERLAY ENHANCEMENT (v3.1)

```yaml
error_overlay:
  description: "Developer-friendly error display"

  features:
    stack_trace:
      clickable: true
      source_links: "Open in editor"
      file_context: "Show surrounding lines"

    source_map:
      original_source: true
      minified_fallback: false

    quick_fix:
      suggestions: true
      one_click_apply: "Safe fixes only"
      explain: "Why this error happened"

  ai_assist:
    explain_error: true
    suggest_fix: true
    auto_apply: "Safe fixes only"
    learn_pattern: "Prevent similar errors"

  integration:
    vscode: "Click to open file"
    cursor: "AI explain button"
    terminal: "Formatted output"

  commands:
    overlay_config: "/dev overlay [config]"
    ai_explain: "/dev explain [error]"
```

---

## 🔧 SUB-COMMANDS

| Command                | Description            |
| ---------------------- | ---------------------- |
| `/dev`                 | Start dev server       |
| `/dev stop`            | Stop server            |
| `/dev restart`         | Restart server         |
| `/dev logs`            | View full logs         |
| `/dev optimize check`  | Check HMR performance  |
| `/dev optimize fix`    | Fix performance issues |
| `/dev explain [error]` | AI explain error       |

---

_DOMYH Awesome Code v5.5 • Dev Pro v3.1 • HMR 2025 + Error Overlay_
