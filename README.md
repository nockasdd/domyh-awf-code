# 🚀 DOMYH Agent v4.3

> **Complete AI Agent Library for Developers**
> Portable • Multi-language • Universal IDE Support
>
> _Developed by [NockDev](https://github.com/nockdev)_

<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-commands">Commands</a> •
  <a href="#-skills">Skills</a> •
  <a href="#-ide-support">IDE Support</a> •
  <a href="#vietnamese">Tiếng Việt</a>
</p>

---

## 📦 Quick Start

### Option 1: Global Installation (Recommended)

```bash
# Linux/macOS
./domyh-agent/.agent/scripts/install.sh

# Windows PowerShell
.\domyh-agent\.agent\scripts\install.ps1
```

During installation, you'll be prompted to choose:

- **Language**: English (default) or Vietnamese
- **Target IDE**: Claude Code, Cursor, Windsurf, Gemini CLI, etc.

### Option 2: Project-Specific Installation

```bash
# Copy the agent folder into your project root
cp -r domyh-agent/.agent /path/to/your/project/
cp domyh-agent/root/* /path/to/your/project/
```

---

## 🎯 Commands

### 🔧 Development

| Command     | Description                                                                         |
| ----------- | ----------------------------------------------------------------------------------- |
| `/code`     | 💻 Write production-ready code with proper error handling, types, and documentation |
| `/dev`      | ▶️ Start development server: detect stack, run dev commands, validate output        |
| `/debug`    | 🐛 Systematic debugging: reproduce → isolate → analyze → fix → verify               |
| `/test`     | ✅ Run existing tests and write new test cases with proper coverage                 |
| `/refactor` | 🔧 Code refactoring: identify smells → plan changes → apply → verify tests pass     |
| `/generate` | 🏗️ Code generation: models, APIs, components, services, and tests from templates    |

### 📋 Planning & Design

| Command      | Description                                                                                 |
| ------------ | ------------------------------------------------------------------------------------------- |
| `/plan`      | 📋 Feature planning with impact analysis, task breakdown, and effort estimation             |
| `/think`     | 💡 Brainstorming: explore ideas, research solutions, evaluate options                       |
| `/visualize` | 🖼️ UI/UX Design: mockups, wireframes, component design, visual prototyping                  |
| `/doc`       | 📝 Generate documentation: API docs, README, code comments, and changelogs                  |
| `/init`      | ✨ Initialize new project with intelligent scaffolding, P0-P6 phases, and progress tracking |

### 🚀 Deployment & Ops

| Command    | Description                                                                         |
| ---------- | ----------------------------------------------------------------------------------- |
| `/deploy`  | 🚀 Deploy to production with pre-checks, rollback plan, and post-verification       |
| `/env`     | 🔐 Environment management: create, sync, validate .env files and encrypt secrets    |
| `/monitor` | 📡 Setup observability: logging, tracing, metrics, and alerting configuration       |
| `/perf`    | ⚡ Performance profiling: CPU, memory, benchmarks, and optimization recommendations |
| `/revert`  | ⏪ Revert changes: git rollback, deployment rollback, database rollback             |
| `/migrate` | 🗃️ Database migrations: create, run, rollback, and seed with safety checks          |

### 🔍 Quality & Review

| Command    | Description                                                                                                   |
| ---------- | ------------------------------------------------------------------------------------------------------------- |
| `/ap`      | 🔬 Comprehensive code audit with 5-expert panel: security, performance, architecture, testing, best practices |
| `/review`  | 👀 Code review for PRs: logic, quality, security, and tests verification                                      |
| `/modify`  | 🔧 Fix existing project: detect stack → analyze issues → plan → execute → verify                              |
| `/clean`   | 🧹 Code cleanup: remove dead code, organize imports, remove unused dependencies                               |
| `/upgrade` | 📦 Update dependencies: check outdated, apply safe updates, review breaking changes                           |

### 🛠️ Utility

| Command        | Description                                                                      |
| -------------- | -------------------------------------------------------------------------------- |
| `/status`      | 📊 Project health: build, tests, coverage, lint metrics, and recent activity     |
| `/recap`       | 📖 Session summary: completed tasks, changed files, decisions, and next steps    |
| `/suggest`     | ➡️ Smart suggestions: context-aware next steps based on project state            |
| `/orchestrate` | 🎭 Multi-Agent Orchestration: coordinate parallel tasks, delegate to specialists |
| `/help`        | ❓ Show all available commands, usage examples, and language settings            |

---

## 🧠 Skills

**33 auto-detected tech-specific skills** organized by category:

### Languages (12)

| Skill      | Description                            |
| ---------- | -------------------------------------- |
| Go         | Go 1.22/1.23 with generics, iterators  |
| Python     | Python 3.12+ with type hints           |
| TypeScript | TypeScript 5.5+                        |
| Rust       | Ownership, Tokio, Axum                 |
| C++        | C++20/23/26, concepts, ranges          |
| C          | ISO C23, memory safety                 |
| C#         | .NET 8/9, LINQ                         |
| Java       | Java 21+ with records, virtual threads |
| PHP        | PHP 8.3/8.4, Laravel 12                |
| Lua        | Lua 5.4/5.5, LuaJIT, FFI               |
| Kotlin     | Kotlin 2.0, K2 compiler, KMP           |
| Swift      | Swift 6, SwiftUI, Concurrency          |

### Frontend (8)

| Skill         | Description                  |
| ------------- | ---------------------------- |
| React         | React 19, Server Components  |
| Vue           | Vue 3.5, Composition API     |
| Next.js       | App Router, RSC, Turbopack   |
| Nuxt          | Nuxt 4, useFetch, routeRules |
| Angular       | Angular 19/20, signals       |
| Svelte        | Svelte 5, runes              |
| Tailwind      | Tailwind CSS 4, @theme       |
| UI/UX Pro Max | 50+ styles, 21 palettes      |

### Mobile & Desktop (4)

| Skill        | Description                    |
| ------------ | ------------------------------ |
| Flutter      | Flutter 3.27, Riverpod 3.0     |
| React Native | New Architecture, Fabric       |
| Electron     | Context isolation, IPC         |
| Swift        | SwiftUI, iOS/macOS development |

### DevOps & Infrastructure (5)

| Skill      | Description                    |
| ---------- | ------------------------------ |
| Docker     | BuildKit, rootless, Compose v2 |
| Kubernetes | K8s 1.30/1.31, Helm 3          |
| AWS        | Serverless, Lambda, ECS        |
| CI/CD      | GitHub Actions, GitLab CI      |
| Security   | OWASP, CWE Top 25              |

### Core (4)

| Skill        | Description                      |
| ------------ | -------------------------------- |
| Database     | PostgreSQL, MySQL, MongoDB       |
| Testing      | Jest, Vitest, pytest, Go testing |
| Coding Rules | 23 languages, naming conventions |
| ASM          | x86, ARM assembly                |

---

## 🌍 IDE Support

| IDE            | Config File                        | Status |
| -------------- | ---------------------------------- | ------ |
| Claude Code    | `CLAUDE.md`, `~/.claude/`          | ✅     |
| Cursor         | `.cursorrules`, `~/.cursor/rules/` | ✅     |
| Windsurf       | `AGENTS.md`                        | ✅     |
| GitHub Copilot | `.github/copilot-instructions.md`  | ✅     |
| Gemini CLI     | `GEMINI.md`, `~/.gemini/`          | ✅     |
| Antigravity    | `~/.gemini/antigravity/`           | ✅     |
| Continue.dev   | `~/.continue/AGENTS.md`            | ✅     |
| JetBrains AI   | `AGENTS.md`                        | ✅     |
| Augment Code   | `~/.augment/rules/`                | ✅     |
| OpenAI Codex   | `~/.codex/AGENTS.md`               | ✅     |

---

## 📁 Structure

```
domyh-agent/
├── README.md                     # This file
├── LICENSE                       # MIT
│
├── root/                         # IDE config files
│   ├── AGENTS.md                 # Universal
│   ├── CLAUDE.md                 # Claude Code
│   ├── GEMINI.md                 # Gemini CLI
│   └── .cursorrules              # Cursor
│
└── .agent/                       # Agent system
    ├── manifest.yaml             # Core manifest
    ├── config.yaml               # Configuration
    ├── workflows/                # 29 commands
    ├── skills/                   # 33 skills
    ├── rules/                    # Universal rules
    ├── personas/                 # 7 personalities
    ├── i18n/                     # Localization (en, vi)
    └── scripts/                  # Install & utility scripts
```

---

## 📄 License

MIT © 2026 [NockDev](https://github.com/nockdev)

---

<a name="vietnamese"></a>

# 🇻🇳 Tiếng Việt

> **Thư viện Agent AI hoàn chỉnh cho Developer**

## Cài Đặt Nhanh

```bash
# Linux/macOS
./domyh-agent/.agent/scripts/install.sh

# Windows PowerShell
.\domyh-agent\.agent\scripts\install.ps1
```

Khi cài đặt, bạn sẽ được chọn:

- **Ngôn ngữ**: Vietnamese (Tiếng Việt)
- **IDE đích**: Claude Code, Cursor, Gemini CLI, etc.

## 🔧 Nhóm Development

| Lệnh        | Mô tả                                                                       |
| ----------- | --------------------------------------------------------------------------- |
| `/code`     | 💻 Viết code production-ready với xử lý lỗi, types, và documentation đầy đủ |
| `/dev`      | ▶️ Chạy dev server: detect stack, hot reload                                |
| `/debug`    | 🐛 Debug có hệ thống: tái tạo → cô lập → phân tích → sửa → xác nhận         |
| `/test`     | ✅ Chạy tests hiện có và viết test cases mới với coverage đầy đủ            |
| `/refactor` | 🔧 Tái cấu trúc code: code smells → plan → apply → verify                   |
| `/generate` | 🏗️ Sinh code từ templates                                                   |

## 📋 Nhóm Planning & Design

| Lệnh         | Mô tả                                                                |
| ------------ | -------------------------------------------------------------------- |
| `/plan`      | 📋 Lên kế hoạch tính năng với phân tích tác động và ước lượng effort |
| `/think`     | 💡 Brainstorming: khám phá ý tưởng, đánh giá lựa chọn                |
| `/visualize` | 🖼️ Thiết kế UI/UX: mockups, wireframes                               |
| `/doc`       | 📝 Tạo tài liệu                                                      |
| `/init`      | ✨ Tạo dự án mới với scaffolding thông minh                          |

## 🚀 Nhóm Deployment & Ops

| Lệnh       | Mô tả                                         |
| ---------- | --------------------------------------------- |
| `/deploy`  | 🚀 Deploy production với kiểm tra và rollback |
| `/env`     | 🔐 Quản lý môi trường                         |
| `/monitor` | 📡 Thiết lập observability                    |
| `/perf`    | ⚡ Phân tích hiệu năng                        |
| `/revert`  | ⏪ Rollback: git, deployment, database        |
| `/migrate` | 🗃️ Database migrations                        |

## 🔍 Nhóm Quality & Review

| Lệnh       | Mô tả                                       |
| ---------- | ------------------------------------------- |
| `/ap`      | 🔬 Kiểm tra code toàn diện với 5 chuyên gia |
| `/review`  | 👀 Review code cho PRs                      |
| `/modify`  | 🔧 Sửa project có sẵn                       |
| `/clean`   | 🧹 Dọn dẹp code                             |
| `/upgrade` | 📦 Cập nhật dependencies                    |

## 🛠️ Nhóm Utility

| Lệnh           | Mô tả                              |
| -------------- | ---------------------------------- |
| `/status`      | 📊 Sức khỏe project                |
| `/recap`       | 📖 Tóm tắt phiên                   |
| `/suggest`     | ➡️ Gợi ý bước tiếp theo thông minh |
| `/orchestrate` | 🎭 Điều phối đa tác tử             |
| `/help`        | ❓ Trợ giúp                        |

---

_DOMYH Agent v4.3 • Made with ❤️ by NockDev_
