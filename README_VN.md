<!-- Header: Waving type with darker blue-purple gradient -->
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:1E40AF,100:6D28D9&height=200&section=header&text=DOMYH%20Awesome%20Code&fontSize=42&fontColor=FFFFFF&animation=fadeIn&fontAlignY=35&desc=Trợ%20Lý%20Phát%20Triển%20AI&descAlignY=55&descSize=16" width="100%" />
</p>

<!-- Animated Typing -->
<p align="center">
  <a href="https://git.io/typing-svg">
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=20&duration=3000&pause=1000&color=3B82F6&center=true&vCenter=true&multiline=false&repeat=true&width=550&height=35&lines=103+Skills+•+26+IDEs+•+44+Commands" alt="Typing SVG" />
  </a>
</p>

<!-- Badges Row -->
<p align="center">
  <a href="https://www.npmjs.com/package/@nockdev/awf">
    <img src="https://img.shields.io/npm/v/@nockdev/awf?style=for-the-badge&logo=npm&logoColor=white&labelColor=CB3837&color=000000" alt="npm">
  </a>
  <img src="https://img.shields.io/badge/skills-103-8B5CF6?style=for-the-badge&logo=bookstack&logoColor=white" alt="Skills">
  <img src="https://img.shields.io/badge/IDEs-26-3B82F6?style=for-the-badge&logo=visualstudiocode&logoColor=white" alt="IDEs">
  <img src="https://img.shields.io/badge/commands-44-F59E0B?style=for-the-badge&logo=windowsterminal&logoColor=white" alt="Commands">
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-10B981?style=for-the-badge&logo=opensourceinitiative&logoColor=white" alt="License">
  </a>
</p>

<!-- Quick Stats -->
<p align="center">
  <b>🚀 Di động</b> &nbsp;•&nbsp; <b>🌍 Đa ngôn ngữ</b> &nbsp;•&nbsp; <b>💻 Hỗ trợ mọi IDE</b> &nbsp;•&nbsp; <b>🇻🇳 Tiếng Việt</b>
</p>

<!-- Language Switch -->
<p align="center">
  <b>🌐 Ngôn ngữ:</b>&nbsp;
  <a href="README.md">English</a> ·
  <b>Tiếng Việt</b>
</p>

---

## ⚡ Bắt đầu nhanh

```bash
npm install -g @nockdev/cli   # Cài đặt CLI toàn cục (1 lần)
nock awf init                 # Khởi tạo và cài đặt cho project
```

> 💡 **`init` vs `install`**: `nock awf init` phát hiện IDE của bạn, cho chọn IDE nào cần cấu hình và cài đặt tất cả. Dùng `nock awf install` khi cần cài lại hoặc thêm IDE mới.

<details>
<summary><b>📦 Các cách cài đặt khác</b></summary>
<br>

| Cách        | Lệnh                                                       | Ghi chú                  |
| :---------- | :--------------------------------------------------------- | :----------------------- |
| **npm**     | `npm install -g @nockdev/cli`                              | Khuyến nghị (global)     |
| **npx**     | `npx -y @nockdev/cli awf init`                             | Không cần cài           |
| **git**     | `git clone https://github.com/nockasdd/domyh-awf-code.git` | Cài đặt thủ công       |

</details>

### 🔄 Cập Nhật

```bash
nock awf update --check       # Kiểm tra phiên bản mới
nock upgrade                  # Cập nhật CLI + tất cả plugins
nock awf mcp update           # Cập nhật MCP server (HSA)
```

---

<!-- MCP Requirement Note -->
<blockquote>
  <p>⚠️ <strong>Yêu cầu MCP Server</strong></p>
  <p>DOMYH Awesome Code sử dụng <a href="https://www.npmjs.com/package/@nockdev/hsa"><strong>HSA MCP Server</strong></a> để cung cấp context thông minh — tìm kiếm code, phân tích ngữ nghĩa, và hiểu project. <strong>Cài MCP cho IDE của bạn để mở khóa toàn bộ tiềm năng.</strong></p>
  <p>💡 <code>nock awf mcp install</code> tự động tải HSA và dùng <code>node</code> để chạy trực tiếp (nhanh hơn, tốn ít bộ nhớ hơn <code>npx</code>). Fallback về <code>npx</code> khi chưa cài.</p>
</blockquote>

## 🖥️ Web Dashboard & Logs

HSA tích hợp sẵn web dashboard để giám sát real-time — **mặc định tắt** để tiết kiệm bộ nhớ. Bật với `HSA_DASHBOARD=true`.

| URL                                | Mô tả                                                       |
| :--------------------------------- | :----------------------------------------------------------- |
| `http://localhost:13100/dashboard` | 📊 Dashboard với 3 tab: **Dashboard** (KPIs, tech stack, engine status, memory, project explorer, activity feed, charts, PageRank) · **Graph** (CodeGraph visualization) · **Logs** (real-time tool call logs) |
| `http://localhost:13100/health`    | ❤️ Health check endpoint                                     |

<details>
<summary><b>⚙️ Cấu hình Dashboard</b></summary>
<br>

**Bật dashboard** — đặt `HSA_DASHBOARD` là `true` trong MCP config của IDE:

```json
{
  "mcpServers": {
    "domyh-hsa": {
      "command": "npx",
      "args": ["-y", "-p", "@nockdev/hsa@latest", "nock-hsa"],
      "env": {
        "HSA_DASHBOARD": "true",
        "HSA_MAX_TOKENS": "8000"
      }
    }
  }
}
```

**Đổi port** — đặt `HSA_DASHBOARD_PORT`:

```json
"env": {
  "HSA_DASHBOARD": "true",
  "HSA_DASHBOARD_PORT": "13200",
  "HSA_MAX_TOKENS": "8000"
}
```

</details>

### 📲 Thông Báo Telegram (Tùy Chọn)

Nhận thông báo qua Telegram khi AI agent hoàn thành task hoặc lưu session.

<details>
<summary><b>🔧 Hướng Dẫn Cài Đặt</b></summary>
<br>

**Bước 1: Tạo Telegram Bot**
1. Mở Telegram → tìm `@BotFather`
2. Gửi `/newbot` → làm theo hướng dẫn → copy **Bot Token**

**Bước 2: Lấy Chat ID**
1. Gửi tin nhắn bất kỳ cho bot mới tạo
2. Truy cập `https://api.telegram.org/bot<TOKEN_CỦA_BẠN>/getUpdates`
3. Tìm `"chat":{"id":123456789}` → đó là **Chat ID** của bạn

**Bước 3: Thêm vào MCP config**

```json
{
  "mcpServers": {
    "domyh-hsa": {
      "command": "node",
      "args": ["~/.nockdev/hsa/hsa-cli.bundle.js"],
      "env": {
        "HSA_MAX_TOKENS": "8000",
        "HSA_TELEGRAM_TOKEN": "bot-token-của-bạn",
        "HSA_TELEGRAM_CHAT_ID": "chat-id-của-bạn"
      }
    }
  }
}
```

**Sử dụng:** Thông báo được gửi tự động khi agent gọi:
- `hsa_session({action: 'persist'})` — session đã lưu

> 💡 Thông báo tùy chỉnh được xử lý bởi HSA Companion extension.

> 💡 Ngôn ngữ thông báo tự động theo cài đặt người dùng. Nếu bạn dùng tiếng Việt (`/lang vi`), thông báo sẽ hiển thị "✅ Phiên làm việc đã lưu" thay vì tiếng Anh.

> ⚠️ Nếu `HSA_TELEGRAM_TOKEN` chưa được cài, tất cả tính năng thông báo sẽ **tự động bỏ qua** — không có lỗi, không tốn token.

</details>

### 🧩 HSA Companion Extension (Tùy Chọn)

> Nâng cao workflow với extension **HSA Companion** — giám sát real-time, điều khiển từ xa, và tự động hóa.

| Tính năng | Mô tả |
| :-------- | :---- |
| **Auto-Accept** | Tự động chấp nhận agent steps, file edits, terminal commands (có bộ lọc an toàn) |
| **Telegram Remote Control** | Gửi `/ask` messages, nhận thông báo hoàn thành qua Telegram |
| **Session Monitoring** | Theo dõi hoạt động AI agent, phát hiện hoàn thành, trích xuất response |
| **Context Injection** | Tự động thêm `[HSA Context]` vào chat messages để nhắc MCP |

**Cài đặt:** [HSA Companion](https://marketplace.visualstudio.com/items?itemName=nockasdd.nock-hsa-ext) - [HSA Companion-OPEN VSX](https://open-vsx.org/extension/Nockasdd/nock-hsa-ext)  

---

## 🎯 Commands

<table>
<tr>
<td width="50%">

### 🔥 Chính

| Cmd       | Hành động                |
| :-------- | :----------------------- |
| `/ap`     | 🔬 Audit toàn bộ project |
| `/code`   | 💻 Viết code chất lượng  |
| `/debug`  | 🐛 Debug hệ thống        |
| `/plan`   | 📋 Lập kế hoạch feature  |
| `/test`   | ✅ Chạy & viết tests     |
| `/deploy` | 🚀 Deploy lên production |

**Ví dụ sử dụng:**

```
/ap                            → 12-expert audit toàn bộ project
/code Thêm tính năng giỏ hàng → Viết code với đầy đủ types + tests
/debug API trả về 500          → Reproduce → Isolate → Fix → Verify
/plan Tích hợp thanh toán VNPay → Phân tích impact + breakdown tasks
/test                           → Chạy tests + viết thêm test cases
/deploy                         → Pre-check → Build → Deploy → Verify
```

</td>
<td width="50%">

### 🛠️ Tiện ích

| Cmd         | Hành động             |
| :---------- | :-------------------- |
| `/refactor` | 🔧 Refactor code      |
| `/review`   | 👀 Code review        |
| `/init`     | ✨ Khởi tạo project   |
| `/recap`    | 📖 Tóm tắt session    |
| `/status`   | 📊 Trạng thái project |
| `/help`     | ❓ Trợ giúp           |

**Ví dụ sử dụng:**

```
/refactor src/services/auth.ts  → Dọn code + tối ưu
/review                          → Review PR: logic, security, tests
/init Tạo SaaS dashboard Nuxt   → Scaffolding + config + structure
/recap                           → Tóm tắt session: tasks, files, decisions
/status                          → Build ✓ Tests ✓ Lint ✓ Coverage 85%
/help                            → Xem tất cả commands + examples
```

</td>
</tr>
</table>

<details>
<summary><b>📋 Tất cả 44 Commands — Chi tiết & Ví dụ</b></summary>
<br>

### 🔥 Chính (9 commands)

| Cmd         | Mô tả                                                                                                                                     | Ví dụ                                      |
| :---------- | :---------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------- |
| `/ap`       | Audit toàn bộ project bởi panel 5+7 chuyên gia (Security, Architecture, Performance, Quality, DevOps + 7 conditional) với 222 checkpoints | `/ap` → Score 7.2/10, 3 critical findings  |
| `/code`     | Viết code production-ready với error handling, types, docs                                                                                | `/code Thêm middleware rate-limit cho API` |
| `/debug`    | Debug hệ thống: reproduce → isolate → analyze → fix → verify                                                                              | `/debug WebSocket đứt kết nối sau 30 giây` |
| `/plan`     | Lập kế hoạch feature với impact analysis, task breakdown, effort estimation                                                               | `/plan Tích hợp SSO với Google OAuth`      |
| `/test`     | Chạy tests hiện có + viết thêm test cases mới cho coverage                                                                                | `/test src/services/payment.ts`            |
| `/deploy`   | Deploy production với pre-checks, rollback plan, post-verify                                                                              | `/deploy staging`                          |
| `/refactor` | Refactor code: detect code smells → clean → restructure → verify tests pass                                                               | `/refactor Tách monolith auth module`      |
| `/init`     | Khởi tạo project mới với scaffolding thông minh theo stack                                                                                | `/init Tạo REST API với Go + PostgreSQL`   |
| `/review`   | Code review cho PR: logic, quality, security, performance, tests                                                                          | `/review PR #42`                           |

---

### ⚙️ DevOps & Infrastructure (10 commands)

| Cmd         | Mô tả                                                                           | Ví dụ                                            |
| :---------- | :------------------------------------------------------------------------------ | :----------------------------------------------- |
| `/migrate`  | Database migration: create, run, rollback, seed với safety checks               | `/migrate Thêm cột status vào bảng orders`       |
| `/doc`      | Tạo documentation: API docs, README, code comments, changelogs                  | `/doc Viết API docs cho payment endpoint`        |
| `/generate` | Code generation: models, APIs, components, services từ templates                | `/generate CRUD cho entity Product`              |
| `/scaffold` | Scaffolding thống nhất: components, pages, services, models từ project patterns | `/scaffold page Dashboard with charts`           |
| `/perf`     | Performance profiling: CPU, memory, benchmarks + khuyến nghị tối ưu             | `/perf Trang dashboard load chậm > 3s`           |
| `/upgrade`  | Update dependencies: check outdated, apply safe updates, review breaking        | `/upgrade` → 5 minor updates, 1 major cần review |
| `/monitor`  | Setup observability: logging, tracing, metrics, alerting                        | `/monitor Setup Prometheus + Grafana`            |
| `/env`      | Quản lý environment variables, secrets, multi-env config                        | `/env Thêm STRIPE_SECRET_KEY cho production`     |
| `/security` | Security scanning & remediation: SAST, SCA, secrets, containers                 | `/security Scan OWASP Top 10`                    |
| `/git`      | Git operations: commit, branch, stash, log, diff, merge, rebase                 | `/git Tạo feature branch cho auth`               |

---

### 🔧 Tiện ích (8 commands)

| Cmd          | Mô tả                                                                  | Ví dụ                                            |
| :----------- | :--------------------------------------------------------------------- | :----------------------------------------------- |
| `/recap`     | Tóm tắt session: completed tasks, changed files, decisions, next steps | `/recap` → 5 tasks done, 12 files changed        |
| `/status`    | Sức khỏe project: build, tests, coverage, lint metrics, git status     | `/status` → Build ✓ Tests 142/142 ✓ Coverage 87% |
| `/help`      | Xem tất cả commands, usage examples, language settings                 | `/help`                                          |
| `/save`      | Lưu trạng thái session vào memory files cho context sau này            | `/save`                                          |
| `/search`    | Tìm kiếm semantic trong memory và audit history                        | `/search payment integration patterns`           |
| `/suggest`   | Gợi ý thông minh: context-aware next steps dựa trên trạng thái project | `/suggest` → "Nên chạy `/test` trước khi deploy" |
| `/visualize` | UI/UX Design: mockups, wireframes, design system, component design     | `/visualize system` → Generate design system     |
| `/onboard`   | Onboarding project: khám phá kiến trúc, map dependencies, tạo guide    | `/onboard` → Getting-started guide               |

---

### 🎯 Đặc biệt (9 commands)

| Cmd             | Mô tả                                                                 | Ví dụ                                                     |
| :-------------- | :-------------------------------------------------------------------- | :-------------------------------------------------------- |
| `/orchestrate`  | Multi-Agent: điều phối parallel tasks, delegate cho specialists       | `/orchestrate Refactor + Test + Deploy module auth`       |
| `/revert`       | Rollback: git revert, deployment rollback, database rollback          | `/revert Undo 2 commits gần nhất`                         |
| `/think`        | Deep reasoning: 6 methods, 5 tiers, multi-mode analysis               | `/think Kiến trúc microservices cho 10K concurrent users` |
| `/sync-version` | Đồng bộ version từ VERSION.yaml SSoT sang tất cả files                | `/sync-version` → Sync v6.6.8 across 15 files             |
| `/dev`          | Start dev server: detect stack, run dev commands, validate output     | `/dev` → `npm run dev` on port 3000                       |
| `/fix`          | Quick-fix pipeline: capture error → identify → fix → verify (max 60s) | `/fix TypeError: Cannot read property 'id'`               |
| `/lang`         | Chuyển ngôn ngữ agent (English ↔ Tiếng Việt)                          | `/lang vi` → Chuyển sang tiếng Việt                       |
| `/workflow`     | Meta-command: workflow discovery, chaining, aliasing                  | `/workflow list` → Xem tất cả workflows                   |
| `/clean`        | Dọn code: xóa dead code, sắp xếp imports, xóa deps không dùng         | `/clean src/utils/` → Xóa 12 unused exports               |

---

### 🔗 Workflow Chains — Kết hợp commands

> Dùng nhiều commands liên tiếp để hoàn thành task phức tạp

```
🆕 Tính năng mới:
  /plan → /code → /test → /review → /deploy

🐛 Sửa bug:
  /debug → /fix → /test → /deploy

🔍 Quality Gate:
  /ap → /refactor → /test → /review

🚀 Release:
  /status → /sync-version → /test → /deploy

🎨 Tính năng UI:
  /visualize system → /scaffold component Button → /code → /test

📊 Tối ưu hiệu năng:
  /perf → /debug → /refactor → /test → /deploy

📦 Onboarding thành viên mới:
  /onboard → /status → /dev → /help
```

</details>

---

## 🧠 Skills (103 tổng)

<!-- Skills Animation -->
<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=18&duration=2000&pause=800&color=8B5CF6&center=true&vCenter=true&width=550&height=35&lines=28+Languages+•+9+Frameworks;9+Core+•+7+DevOps;26+Cross-cutting+•+6+Tooling+•+9+AI-ML;9+Governance+•+103+Tổng+Skills" alt="Skills" />
</p>
</p>

<table>
<tr>
<td width="50%" valign="top">

### 💬 Ngôn ngữ (28)

<p align="center">
  <img src="https://skillicons.dev/icons?i=go,py,ts,js,rust,cpp,c,cs&theme=dark" />
  <br><br>
  <img src="https://skillicons.dev/icons?i=java,php,kotlin,swift,ruby,lua,scala,haskell&theme=dark" />
</p>

<p align="center">
  <sub><b>+ 12 thêm:</b> Elixir, Clojure, OCaml, F#, Julia, R, Zig, Nim, Crystal, Solidity, Perl, Assembly</sub>
</p>

</td>
<td width="50%" valign="top">

### 🖼️ Frameworks (9)

<p align="center">
  <img src="https://skillicons.dev/icons?i=react,vue,nextjs,angular,nuxt,svelte,flutter,tailwind&theme=dark" />
</p>

### ⚙️ DevOps (7)

<p align="center">
  <img src="https://skillicons.dev/icons?i=docker,kubernetes,aws,gcp,azure,terraform,githubactions&theme=dark" />
</p>

### 🔧 Core & Cross-cutting (35) + Governance (9)

<p align="center">
  <img src="https://skillicons.dev/icons?i=postgres,redis,graphql,jest,webpack,vite,electron,bun&theme=dark" />
</p>

<p align="center">
  <sub><b>Core (9):</b> Security, API Design, Error Handling, Logging, Observability, Auth, Context Engineering, Graph Patterns, Skill Creator</sub>
  <br>
  <sub><b>Cross-cutting (26):</b> Testing, Database, SQL, Tailwind, Electron, Coding Rules, DOMYH Design, Web Perf, Deno, Bun, Audit Pro, TDD Workflow, Accessibility, SEO, Microservices, Monorepo, Event-Driven, Tauri, Real-Time, Wasm, Playwright, Payment Integration, Cascade Review, Digital Marketing, Output Enforcement, Receiving Code Review</sub>
</p>

### 🛠️ Tooling (6)

<p align="center">
  <sub>MCP, API Protocols, IDE Extension, CLI Dev, Browser Agent, HSA Toolkit</sub>
</p>

### 🤖 AI-ML (9)

<p align="center">
  <sub>AI Agents, ML Pipelines, Prompt Engineering, RAG Patterns, Vector Search, Gemini Media Gen, Gemini TTS, Gemini Live, Agentic Orchestration</sub>
</p>

</td>
</tr>
</table>

<details>
<summary><b>📊 Chi tiết Skills theo danh mục</b></summary>
<br>

| Danh mục          | Số lượng | Skills                                                                                                                                                                                                              |
| :---------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Languages**     | 28       | C, C++, Rust, Go, Zig, Nim, ASM, Java, Kotlin, Scala, Clojure, C#, F#, Python, Ruby, PHP, Perl, Lua, JavaScript, TypeScript, Haskell, Elixir, OCaml, R, Julia, Swift, Solidity, Crystal                             |
| **Frameworks**    | 9        | React, Vue, Angular, Svelte, Next.js, Nuxt, Flutter, React Native, Streamlit                                                                                                                                        |
| **Core**          | 9        | Security, API Design, Error Handling, Logging, Observability, Authentication, Context Engineering, Graph Patterns, Skill Creator                                                                                    |
| **DevOps**        | 7        | Docker, Kubernetes, AWS, CI/CD, Terraform, GCP, Azure                                                                                                                                                               |
| **Cross-cutting** | 26       | Testing, Database, SQL, Tailwind, Electron, Coding Rules, DOMYH Design, Web Perf, Deno, Bun, Audit Pro, TDD Workflow, Accessibility, SEO, Microservices, Monorepo, Event-Driven, Tauri, Real-Time, Wasm, Playwright, Payment Integration, Cascade Review, Digital Marketing, Output Enforcement, Receiving Code Review |
| **Tooling**       | 6        | MCP, API Protocols, IDE Extension, CLI Dev, Browser Agent, HSA Toolkit                                                                                                                                              |
| **AI-ML**         | 9        | AI Agents, ML Pipelines, Prompt Engineering, RAG Patterns, Vector Search, Gemini Media Gen, Gemini TTS, Gemini Live, Agentic Orchestration                                                                          |
| **Governance**    | 9        | Drift Prevention, Session Governance, Context Integrity, Progressive Escalation, Stop Conditions, Edit Verification, Performance Optimization, Agent Delegation, Context Compaction                                  |
| **Tổng**          | **103**  |                                                                                                                                                                                                                     |

</details>

---

## 💻 Hỗ trợ IDE (26)

<p align="center">
  <img src="https://img.shields.io/badge/Claude-6366F1?style=for-the-badge&logo=anthropic&logoColor=white" />
  <img src="https://img.shields.io/badge/Gemini-4285F4?style=for-the-badge&logo=googlegemini&logoColor=white" />
  <img src="https://img.shields.io/badge/Cursor-000000?style=for-the-badge&logo=cursor&logoColor=white" />
  <img src="https://img.shields.io/badge/Copilot-000000?style=for-the-badge&logo=githubcopilot&logoColor=white" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Windsurf-0EA5E9?style=flat-square" />
  <img src="https://img.shields.io/badge/Codex-412991?style=flat-square&logo=openai&logoColor=white" />
  <img src="https://img.shields.io/badge/Aider-FF6B6B?style=flat-square" />
  <img src="https://img.shields.io/badge/CodeRabbit-FF9900?style=flat-square" />
  <img src="https://img.shields.io/badge/Continue-10B981?style=flat-square" />
  <img src="https://img.shields.io/badge/Amazon_Q-FF9900?style=flat-square&logo=amazonaws&logoColor=white" />
  <img src="https://img.shields.io/badge/Antigravity-1E40AF?style=flat-square" />
  <img src="https://img.shields.io/badge/JetBrains_AI-000000?style=flat-square&logo=jetbrains&logoColor=white" />
</p>

<details>
<summary><b>📋 Tất cả 26 IDEs & File cấu hình</b></summary>
<br>

| IDE              | File cấu hình                     | Loại            |
| :--------------- | :-------------------------------- | :-------------- |
| Claude Code      | `CLAUDE.md`                       | AI Agent        |
| Gemini CLI       | `GEMINI.md`                       | AI Agent        |
| Antigravity      | `.gemini/`                        | AI Agent        |
| Cursor           | `.cursorrules`                    | AI IDE          |
| GitHub Copilot   | `.github/copilot-instructions.md` | AI Assistant    |
| OpenAI Codex     | `.codex/`                         | AI Agent        |
| Windsurf         | `.windsurfrules`                  | AI IDE          |
| Aider            | `.aider.conf.yml`                 | AI CLI          |
| Continue         | `.continue/`                      | AI Assistant    |
| Cline            | `.clinerules`                     | AI Assistant    |
| Roo Code         | `.roo/`                           | AI Assistant    |
| CodeRabbit       | `.coderabbit.yaml`                | AI Review       |
| Amazon Q         | `.amazonq/`                       | AI Assistant    |
| JetBrains AI     | `.junie/`                         | AI IDE          |
| Tabnine          | `.tabnine/`                       | AI Autocomplete |
| Qodo             | `.qodo/`                          | AI Testing      |
| VS Code          | `.vscode/`                        | IDE             |
| Sourcegraph Cody | `.cody/`                          | AI Assistant    |
| Zed AI           | `.zed/`                           | AI IDE          |
| Void             | `.void/`                          | AI IDE          |
| Trae             | `.trae/`                          | AI IDE          |
| AMP              | `.amp/`                           | AI Assistant    |
| Augment          | `.augment/`                       | AI Assistant    |
| OpenCode         | `.opencode/`                      | AI CLI          |
| Kiro             | `.kiro/`                          | AI IDE          |
| PearAI           | `.pearai/`                        | AI IDE          |

</details>

---

## 📁 Kiến trúc

```
📦 .agent/
├── 📋 manifest.yaml          # Cấu hình Agent
├── 🧠 skills/                # 103 skills chuyên biệt
│   ├── languages/    (28)    # Go, Python, TypeScript, Rust...
│   ├── frameworks/   (9)     # React, Vue, Next.js, Flutter, Streamlit...
│   ├── core/         (9)     # Security, API Design, Auth, Graph Patterns...
│   ├── devops/       (7)     # Docker, K8s, AWS, Terraform, GCP, Azure, CI/CD
│   ├── cross-cutting/ (26)   # Testing, Database, Copywriting, C4...
│   ├── tooling/      (6)     # MCP, API Protocols, IDE Extension, HSA Toolkit...
│   ├── ai-ml/        (9)     # AI Agents, ML Pipelines, Gemini, RAG...
│   └── governance/   (9)     # Drift Prevention, Session Governance...
├── 🔄 workflows/     (44)    # 44 command handlers
├── 📜 rules/                 # Constitutional AI rules
├── 👥 personas/              # Developer, Auditor, Debugger...
└── ⚙️ core/                  # Cấu hình engine
```

---

## 🤝 Đóng góp

<p align="center">
  <a href="CONTRIBUTING.md">
    <img src="https://img.shields.io/badge/PRs-welcome-10B981?style=for-the-badge" />
  </a>
  <a href="https://github.com/nockasdd/domyh-awf-code/issues">
    <img src="https://img.shields.io/badge/Issues-welcome-3B82F6?style=for-the-badge" />
  </a>
</p>

<p align="center">
  <a href="https://github.com/nockasdd/domyh-awf-code/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=nockasdd/domyh-awf-code&max=8" />
  </a>
</p>

---

## 📄 Giấy phép

<p align="center">
  MIT © <a href="https://github.com/nockasdd"><b>NockDev</b></a>
</p>

<!-- Footer: Waving type with darker gradient -->
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:6D28D9,100:1E40AF&height=120&section=footer" width="100%" />
</p>
