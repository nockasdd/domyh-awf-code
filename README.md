<!-- Header: Waving type with darker blue-purple gradient -->
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:1E40AF,100:6D28D9&height=200&section=header&text=DOMYH%20Awesome%20Code&fontSize=42&fontColor=FFFFFF&animation=fadeIn&fontAlignY=35&desc=AI-Powered%20Development%20Assistant&descAlignY=55&descSize=16" width="100%" />
</p>

<!-- Animated Typing -->
<p align="center">
  <a href="https://git.io/typing-svg">
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=20&duration=3000&pause=1000&color=3B82F6&center=true&vCenter=true&multiline=false&repeat=true&width=550&height=35&lines=104+Skills+•+26+IDEs+•+45+Commands" alt="Typing SVG" />
  </a>
</p>

<!-- Badges Row -->
<p align="center">
  <a href="https://www.npmjs.com/package/@nockdev/awf">
    <img src="https://img.shields.io/npm/v/@nockdev/awf?style=for-the-badge&logo=npm&logoColor=white&labelColor=CB3837&color=000000" alt="npm">
  </a>
  <img src="https://img.shields.io/badge/skills-104-8B5CF6?style=for-the-badge&logo=bookstack&logoColor=white" alt="Skills">
  <img src="https://img.shields.io/badge/IDEs-26-3B82F6?style=for-the-badge&logo=visualstudiocode&logoColor=white" alt="IDEs">
  <img src="https://img.shields.io/badge/commands-45-F59E0B?style=for-the-badge&logo=windowsterminal&logoColor=white" alt="Commands">
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-10B981?style=for-the-badge&logo=opensourceinitiative&logoColor=white" alt="License">
  </a>
</p>

<!-- Quick Stats -->
<p align="center">
  <b>🚀 Portable</b> &nbsp;•&nbsp; <b>🌍 Multi-language</b> &nbsp;•&nbsp; <b>💻 Universal IDE Support</b> &nbsp;•&nbsp; <b>🇻🇳 Vietnamese</b>
</p>

<!-- Language Switch -->
<p align="center">
  <b>🌐 Language:</b>&nbsp;
  <b>English</b> ·
  <a href="README_VN.md">Tiếng Việt</a>
</p>

---

## ⚡ Quick Start

```bash
npm install -g @nockdev/cli   # Install CLI globally (one-time)
nock awf init                 # Initialize & install for your project
```

> 💡 **`init` vs `install`**: `nock awf init` detects your IDEs, lets you choose which to configure, and installs everything. Use `nock awf install` only if you want to reinstall or add a specific IDE later.

<details>
<summary><b>📦 More Installation Options</b></summary>
<br>

| Method      | Command                                                    | Note                      |
| :---------- | :--------------------------------------------------------- | :------------------------ |
| **npm**     | `npm install -g @nockdev/cli`                              | Recommended (global)      |
| **npx**     | `npx -y @nockdev/cli awf init`                             | No install needed         |
| **git**     | `git clone https://github.com/nockasdd/domyh-awf-code.git` | Manual setup              |

</details>

### 🔄 Updating

```bash
nock awf update --check       # Check for available updates
nock upgrade                  # Update CLI + all plugins
nock awf mcp update           # Update MCP server (HSA)
```

---

<!-- MCP Requirement Note -->
<blockquote>
  <p>⚠️ <strong>MCP Server Required</strong></p>
  <p>DOMYH Awesome Code uses <a href="https://www.npmjs.com/package/@nockdev/hsa"><strong>HSA MCP Server</strong></a> for intelligent context — code search, semantic analysis, and project understanding. <strong>Install MCP for your IDE to unlock full potential.</strong></p>
  <p>💡 <code>nock awf mcp install</code> automatically downloads HSA and uses <code>node</code> for direct execution (faster, lower memory than <code>npx</code>). Falls back to <code>npx</code> on first run.</p>
</blockquote>

### 🔧 MCP Installation

**Method 1: Via nock-cli (recommended)**

```bash
npm install -g @nockdev/cli               # Install CLI globally
nock awf mcp install --ide all             # Configure MCP for all IDEs
nock awf mcp install --ide cursor          # Or configure for specific IDE
```

**Method 2: Manual IDE Configuration**

<details>
<summary><b>📋 Per-IDE MCP Config (click to expand)</b></summary>
<br>

**Step 1: Install HSA locally** (one-time)
```bash
npm install -g @nockdev/hsa          # or: nock awf mcp install
```

> After install, HSA lives at `~/.nockdev/hsa/hsa-cli.bundle.js`. The configs below use **`node`** for direct execution (1 process, ~40MB less than `npx`).

**Cursor** — `~/.cursor/mcp.json` (global):
```json
{
  "mcpServers": {
    "domyh-hsa": {
      "command": "node",
      "args": ["~/.nockdev/hsa/hsa-cli.bundle.js"],
      "env": { "HSA_MAX_TOKENS": "8000", "HSA_DASHBOARD": "false" }
    }
  }
}
```

**Claude Code** — run:
```bash
claude mcp add domyh-hsa -- node ~/.nockdev/hsa/hsa-cli.bundle.js
```

**VS Code (GitHub Copilot)** — `.vscode/mcp.json` (project-local):
```json
{
  "servers": {
    "domyh-hsa": {
      "command": "node",
      "args": ["~/.nockdev/hsa/hsa-cli.bundle.js"],
      "env": { "HSA_MAX_TOKENS": "8000", "HSA_DASHBOARD": "false" }
    }
  }
}
```

**Antigravity (Gemini)** — `~/.gemini/settings.json` (global):
```json
{
  "mcpServers": {
    "domyh-hsa": {
      "command": "node",
      "args": ["~/.nockdev/hsa/hsa-cli.bundle.js"],
      "env": { "HSA_MAX_TOKENS": "8000", "HSA_DASHBOARD": "false" }
    }
  }
}
```

**Windsurf** — `~/.codeium/windsurf/mcp_config.json` (global):
```json
{
  "mcpServers": {
    "domyh-hsa": {
      "command": "node",
      "args": ["~/.nockdev/hsa/hsa-cli.bundle.js"],
      "env": { "HSA_MAX_TOKENS": "8000", "HSA_DASHBOARD": "false" }
    }
  }
}
```

<details>
<summary><b>⚡ Quick-start with npx (no install)</b></summary>
<br>

> If you don't want to install HSA locally, use `npx` — it downloads on first run but uses ~40MB more memory (2 processes).

```json
{
  "mcpServers": {
    "domyh-hsa": {
      "command": "npx",
      "args": ["-y", "-p", "@nockdev/hsa@latest", "nock-hsa"],
      "env": { "HSA_MAX_TOKENS": "8000", "HSA_DASHBOARD": "false" }
    }
  }
}
```

</details>

</details>

### ⚙️ Environment Variables

| Variable             | Default | Description                     |
| :------------------- | :------ | :------------------------------ |
| `HSA_MAX_TOKENS`     | `8000`  | Maximum token budget per query  |
| `HSA_DASHBOARD`      | `false` | Enable/disable web dashboard    |
| `HSA_DASHBOARD_PORT` | `13100` | Dashboard port                  |
| `HSA_LOG_LEVEL`      | `info`  | Log level: debug/info/warn/error|
| `HSA_TELEGRAM_TOKEN` | —       | Telegram Bot token for notifications |
| `HSA_TELEGRAM_CHAT_ID`| —      | Telegram Chat ID to send to     |
| `HSA_DISCORD_WEBHOOK_URL`| —   | Discord Webhook URL (optional)  |

### 📲 Telegram Notifications (Optional)

Get notified on Telegram when AI agent completes tasks or persists sessions.

<details>
<summary><b>🔧 Setup Guide</b></summary>
<br>

**Step 1: Create a Telegram Bot**
1. Open Telegram → search `@BotFather`
2. Send `/newbot` → follow prompts → copy the **Bot Token**

**Step 2: Get your Chat ID**
1. Send any message to your new bot
2. Open `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
3. Find `"chat":{"id":123456789}` → that's your **Chat ID**

**Step 3: Add to MCP config**

```json
{
  "mcpServers": {
    "domyh-hsa": {
      "command": "node",
      "args": ["~/.nockdev/hsa/hsa-cli.bundle.js"],
      "env": {
        "HSA_MAX_TOKENS": "8000",
        "HSA_TELEGRAM_TOKEN": "your-bot-token",
        "HSA_TELEGRAM_CHAT_ID": "your-chat-id"
      }
    }
  }
}
```

**Usage:** Notifications are sent automatically when agent calls:
- `hsa_session({action: 'persist'})` — session saved

> 💡 Custom notifications are handled by the HSA Companion extension independently.

> 💡 Notification language matches your configured preference. Vietnamese users (`/lang vi`) see "✅ Phiên làm việc đã lưu" instead of English.

> ⚠️ If `HSA_TELEGRAM_TOKEN` is not set, all notification features are **silently skipped** — no errors, no token waste.

</details>

### 🧩 HSA Companion Extension (Optional)

> Enhance your workflow with the **HSA Companion** IDE extension — real-time monitoring, remote control, and automation.

| Feature | Description |
| :------ | :---------- |
| **Auto-Accept** | Automatically accept AI agent steps, file edits, terminal commands (with safety filters) |
| **Telegram Remote Control** | Send `/ask` messages, receive completion notifications via Telegram |
| **Session Monitoring** | Track AI agent activity, detect completion, extract response previews |
| **Context Injection** | Automatically append `[HSA Context]` to chat messages for MCP guidance |

**Install:** [HSA Companion](https://open-vsx.org/extension/Nockasdd/nock-hsa-ext)

---

## 🖥️ Web Dashboard & Logs

HSA includes a built-in web dashboard for real-time monitoring — **disabled by default** to save memory. Enable with `HSA_DASHBOARD=true`.

| URL                                | Description                                                  |
| :--------------------------------- | :----------------------------------------------------------- |
| `http://localhost:13100/dashboard` | 📊 Single-page dashboard with 3 tabs: **Dashboard** (KPIs, tech stack, engine status, memory, project explorer, activity feed, charts, PageRank) · **Graph** (interactive CodeGraph visualization) · **Logs** (real-time tool call logs with filtering) |
| `http://localhost:13100/health`    | ❤️ Health check endpoint                                     |

<details>
<summary><b>⚙️ Dashboard Configuration</b></summary>
<br>

**Enable dashboard** — set `HSA_DASHBOARD` to `true` in your IDE's MCP config:

```json
{
  "mcpServers": {
    "domyh-hsa": {
      "command": "node",
      "args": ["~/.nockdev/hsa/hsa-cli.bundle.js"],
      "env": {
        "HSA_DASHBOARD": "true",
        "HSA_MAX_TOKENS": "8000"
      }
    }
  }
}
```

**Change port** — set `HSA_DASHBOARD_PORT`:

```json
"env": {
  "HSA_DASHBOARD": "true",
  "HSA_DASHBOARD_PORT": "13200",
  "HSA_MAX_TOKENS": "8000"
}
```

</details>

---

## 🎯 Commands

<table>
<tr>
<td width="50%">

### 🔥 Core

| Cmd       | Action                  |
| :-------- | :---------------------- |
| `/ap`     | 🔬 Full project audit   |
| `/code`   | 💻 Write quality code   |
| `/debug`  | 🐛 Debug systematically |
| `/plan`   | 📋 Plan features        |
| `/test`   | ✅ Run & write tests    |
| `/deploy` | 🚀 Deploy to prod       |

**Example flows:**

```
/ap                            → 12-expert audit of the entire project
/code Add shopping cart feature → Write code with full types + tests
/debug API returns 500          → Reproduce → Isolate → Fix → Verify
/plan Integrate VNPay payment   → Impact analysis + task breakdown
/test                           → Run tests + write new test cases
/deploy                         → Pre-check → Build → Deploy → Verify
```

</td>
<td width="50%">

### 🛠️ Utilities

| Cmd         | Action            |
| :---------- | :---------------- |
| `/refactor` | 🔧 Refactor code  |
| `/review`   | 👀 Code review    |
| `/init`     | ✨ Init project   |
| `/recap`    | 📖 Session recap  |
| `/status`   | 📊 Project status |
| `/help`     | ❓ Show help      |

**Example flows:**

```
/refactor src/services/auth.ts  → Clean code + optimize
/review                          → Review PR: logic, security, tests
/init Create SaaS dashboard Nuxt → Scaffolding + config + structure
/recap                           → Summarize: tasks, files, decisions
/status                          → Build ✓ Tests ✓ Lint ✓ Coverage 85%
/help                            → Show all commands + examples
```

</td>
</tr>
</table>

<details>
<summary><b>📋 All 45 Commands — Details & Example Flows</b></summary>
<br>

### 🔥 Core (9 commands)

| Cmd         | Description                                                                                                                          | Example                                         |
| :---------- | :----------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------- |
| `/ap`       | Full project audit by a 5+7 expert panel (Security, Architecture, Performance, Quality, DevOps + 7 conditional) with 222 checkpoints | `/ap` → Score 7.2/10, 3 critical findings       |
| `/code`     | Write production-ready code with error handling, types, and docs                                                                     | `/code Add rate-limit middleware for API`       |
| `/debug`    | Systematic debugging: reproduce → isolate → analyze → fix → verify                                                                   | `/debug WebSocket disconnects after 30 seconds` |
| `/plan`     | Feature planning with impact analysis, task breakdown, effort estimation                                                             | `/plan Integrate SSO with Google OAuth`         |
| `/test`     | Run existing tests + write new test cases for coverage                                                                               | `/test src/services/payment.ts`                 |
| `/deploy`   | Deploy to production with pre-checks, rollback plan, and post-verification                                                           | `/deploy staging`                               |
| `/refactor` | Refactor code: detect code smells → clean → restructure → verify tests pass                                                          | `/refactor Split monolith auth module`          |
| `/init`     | Initialize a new project with smart scaffolding based on stack                                                                       | `/init Create REST API with Go + PostgreSQL`    |
| `/review`   | Code review for PRs: logic, quality, security, performance, tests                                                                    | `/review PR #42`                                |

---

### ⚙️ DevOps & Infrastructure (10 commands)

| Cmd         | Description                                                                      | Example                                            |
| :---------- | :------------------------------------------------------------------------------- | :------------------------------------------------- |
| `/migrate`  | Database migrations: create, run, rollback, seed with safety checks              | `/migrate Add status column to orders table`       |
| `/doc`      | Generate documentation: API docs, README, code comments, changelogs              | `/doc Write API docs for payment endpoint`         |
| `/generate` | Code generation: models, APIs, components, services from templates               | `/generate CRUD for Product entity`                |
| `/scaffold` | Unified scaffolding: components, pages, services, models from project patterns   | `/scaffold page Dashboard with charts`             |
| `/perf`     | Performance profiling: CPU, memory, benchmarks + optimization advice             | `/perf Dashboard page loads > 3s`                  |
| `/upgrade`  | Update dependencies: check outdated, apply safe updates, review breaking changes | `/upgrade` → 5 minor updates, 1 major needs review |
| `/monitor`  | Setup observability: logging, tracing, metrics, alerting                         | `/monitor Setup Prometheus + Grafana`              |
| `/env`      | Environment management: variables, secrets, multi-env config                     | `/env Add STRIPE_SECRET_KEY for production`        |
| `/security` | Security scanning & remediation: SAST, SCA, secrets, containers                  | `/security Scan for OWASP Top 10`                  |
| `/git`      | Git operations: commit, branch, stash, log, diff, merge, rebase                  | `/git Create feature branch for auth`              |

---

### 🔧 Utility (8 commands)

| Cmd          | Description                                                                 | Example                                          |
| :----------- | :-------------------------------------------------------------------------- | :----------------------------------------------- |
| `/recap`     | Session summary: completed tasks, changed files, decisions, next steps      | `/recap` → 5 tasks done, 12 files changed        |
| `/status`    | Project health: build, tests, coverage, lint metrics, git status            | `/status` → Build ✓ Tests 142/142 ✓ Coverage 87% |
| `/help`      | Show all commands, usage examples, and language settings                    | `/help`                                          |
| `/save`      | Save session state to memory files for later context                        | `/save`                                          |
| `/search`    | Semantic search across memory and audit history                             | `/search payment integration patterns`           |
| `/suggest`   | Smart suggestions: context-aware next steps based on project state          | `/suggest` → "Run `/test` before deploying"      |
| `/visualize` | UI/UX Design: mockups, wireframes, design system, component design          | `/visualize system` → Generate design system     |
| `/onboard`   | Project onboarding: discover architecture, map dependencies, generate guide | `/onboard` → Getting-started guide generated     |

---

### 🎯 Special (10 commands)

| Cmd             | Description                                                           | Example                                                      |
| :-------------- | :-------------------------------------------------------------------- | :----------------------------------------------------------- |
| `/orchestrate`  | Multi-Agent coordination: parallel tasks, delegate to specialists     | `/orchestrate Refactor + Test + Deploy auth module`          |
| `/revert`       | Rollback: git revert, deployment rollback, database rollback          | `/revert Undo last 2 commits`                                |
| `/think`        | Deep reasoning: 6 methods, 5 tiers, multi-mode analysis               | `/think Microservices architecture for 10K concurrent users` |
| `/sync-version` | Sync version from VERSION.yaml SSoT across all files                  | `/sync-version` → Sync v6.6.8 across 15 files               |
| `/dev`          | Start dev server: detect stack, run dev commands, validate output     | `/dev` → `npm run dev` on port 3000                          |
| `/fix`          | Quick-fix pipeline: capture error → identify → fix → verify (max 60s) | `/fix TypeError: Cannot read property 'id'`                  |
| `/game`         | Comprehensive game development assistant (Unity/UE/HTML5/Godot)       | `/game Create 2D player movement script`                       |
| `/lang`         | Switch agent language (English ↔ Vietnamese)                          | `/lang vi` → Switch to Vietnamese                            |
| `/workflow`     | Meta-command: workflow discovery, chaining, and aliasing              | `/workflow list` → Show all available workflows              |
| `/clean`        | Code cleanup: remove dead code, organize imports, unused deps         | `/clean src/utils/` → Removed 12 unused exports              |

---

### 🔗 Workflow Chains — Combine commands

> Chain multiple commands to complete complex tasks

```
🆕 New Feature Flow:
  /plan → /code → /test → /review → /deploy

🐛 Bug Fix Flow:
  /debug → /fix → /test → /deploy

🔍 Quality Gate Flow:
  /ap → /refactor → /test → /review

🚀 Release Flow:
  /status → /sync-version → /test → /deploy

🎨 UI Feature Flow:
  /visualize system → /scaffold component Button → /code → /test

📊 Performance Fix:
  /perf → /debug → /refactor → /test → /deploy

📦 New Team Member:
  /onboard → /status → /dev → /help
```

</details>

---

## 🧠 Skills (104 total)

<!-- Skills Animation -->
<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=18&duration=2000&pause=800&color=8B5CF6&center=true&vCenter=true&width=550&height=35&lines=28+Languages+•+9+Frameworks;9+Core+•+7+DevOps;27+Cross-cutting+•+6+Tooling+•+9+AI-ML;9+Governance+•+104+Total+Skills" alt="Skills" />
</p>

<table>
<tr>
<td width="50%" valign="top">

### 💬 Languages (28)

<p align="center">
  <img src="https://skillicons.dev/icons?i=go,py,ts,js,rust,cpp,c,cs&theme=dark" />
  <br><br>
  <img src="https://skillicons.dev/icons?i=java,php,kotlin,swift,ruby,lua,scala,haskell&theme=dark" />
</p>

<p align="center">
  <sub><b>+ 12 more:</b> Elixir, Clojure, OCaml, F#, Julia, R, Zig, Nim, Crystal, Solidity, Perl, Assembly</sub>
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

### 🔧 Core & Cross-cutting (36) + Governance (9)

<p align="center">
  <img src="https://skillicons.dev/icons?i=postgres,redis,graphql,jest,webpack,vite,electron,bun&theme=dark" />
</p>

<p align="center">
  <sub><b>Core (9):</b> Security, API Design, Error Handling, Logging, Observability, Auth, Context Engineering, Graph Patterns, Skill Creator</sub>
  <br>
  <sub><b>Cross-cutting (27):</b> Testing, Database, SQL, Tailwind, Electron, Coding Rules, DOMYH Design, Web Perf, Deno, Bun, Audit Pro, TDD Workflow, Accessibility, SEO, Microservices, Monorepo, Event-Driven, Tauri, Real-Time, Wasm, Playwright, Payment Integration, Cascade Review, Digital Marketing, Output Enforcement, Receiving Code Review, Game Development</sub>
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
<summary><b>📊 Skill Breakdown by Category</b></summary>
<br>

| Category          | Count  | Skills                                                                                                                                                                                                              |
| :---------------- | :----- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Languages**     | 28     | C, C++, Rust, Go, Zig, Nim, ASM, Java, Kotlin, Scala, Clojure, C#, F#, Python, Ruby, PHP, Perl, Lua, JavaScript, TypeScript, Haskell, Elixir, OCaml, R, Julia, Swift, Solidity, Crystal                             |
| **Frameworks**    | 9      | React, Vue, Angular, Svelte, Next.js, Nuxt, Flutter, React Native, Streamlit                                                                                                                                        |
| **Core**          | 9      | Security, API Design, Error Handling, Logging, Observability, Authentication, Context Engineering, Graph Patterns, Skill Creator                                                                                    |
| **DevOps**        | 7      | Docker, Kubernetes, AWS, CI/CD, Terraform, GCP, Azure                                                                                                                                                               |
| **Cross-cutting** | 26     | Testing, Database, SQL, Tailwind, Electron, Coding Rules, DOMYH Design, Web Perf, Deno, Bun, Audit Pro, TDD Workflow, Accessibility, SEO, Microservices, Monorepo, Event-Driven, Tauri, Real-Time, Wasm, Playwright, Payment Integration, Cascade Review, Digital Marketing, Output Enforcement, Receiving Code Review, Game Development |
| **Tooling**       | 6      | MCP, API Protocols, IDE Extension, CLI Dev, Browser Agent, HSA Toolkit                                                                                                                                              |
| **AI-ML**         | 9      | AI Agents, ML Pipelines, Prompt Engineering, RAG Patterns, Vector Search, Gemini Media Gen, Gemini TTS, Gemini Live, Agentic Orchestration                                                                          |
| **Governance**    | 9      | Drift Prevention, Session Governance, Context Integrity, Progressive Escalation, Stop Conditions, Edit Verification, Performance Optimization, Agent Delegation, Context Compaction                                  |
| **Total**         | **104** |                                                                                                                                                                                                                     |

</details>

---

## 💻 IDE Support (26)

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
<summary><b>📋 All 26 IDEs & Configuration Files</b></summary>
<br>

| IDE              | Config File                       | Type            |
| :--------------- | :-------------------------------- | :-------------- |
| Claude Code      | `CLAUDE.md`                       | AI Agent        |
| Gemini CLI       | `GEMINI.md`                       | AI Agent        |
| Antigravity      | `.gemini/`                        | AI Agent        |
| Cursor           | `.cursorrules`                    | AI IDE          |
| GitHub Copilot   | `.github/copilot-instructions.md` | AI Assistant    |
| OpenAI Codex     | `.codex/`                         | AI Agent        |
| Windsurf         | `.windsurfrules`                  | AI IDE          |
| Aider            | `.aider.conf.yml`                 | AI CLI          |
| AMP              | `.amp/`                           | AI Assistant    |
| Augment          | `.augment/`                       | AI Assistant    |
| Continue         | `.continue/`                      | AI Assistant    |
| Cline            | `.clinerules`                     | AI Assistant    |
| Roo Code         | `.roo/`                           | AI Assistant    |
| CodeRabbit       | `.coderabbit.yaml`                | AI Review       |
| Amazon Q         | `.amazonq/`                       | AI Assistant    |
| JetBrains AI     | `.junie/`                         | AI IDE          |
| OpenCode         | `.opencode/`                      | AI CLI          |
| Tabnine          | `.tabnine/`                       | AI Autocomplete |
| Sourcegraph Cody | `.cody/`                          | AI Assistant    |
| VS Code          | `.vscode/`                        | IDE             |
| Kiro             | `.kiro/`                          | AI IDE          |
| Zed AI           | `.zed/`                           | AI IDE          |
| Qodo             | `.qodo/`                          | AI Testing      |
| Void             | `.void/`                          | AI IDE          |
| Trae             | `.trae/`                          | AI IDE          |
| PearAI           | `.pearai/`                        | AI IDE          |

</details>

---

## 📁 Architecture

```
📦 .agent/
├── 📋 manifest.yaml          # Agent configuration
├── 🧠 skills/                # 104 specialized skills
│   ├── languages/    (28)    # Go, Python, TypeScript, Rust...
│   ├── frameworks/   (9)     # React, Vue, Next.js, Flutter, Streamlit...
│   ├── core/         (9)     # Security, API Design, Auth, Graph Patterns...
│   ├── devops/       (7)     # Docker, K8s, AWS, Terraform, GCP, Azure, CI/CD
│   ├── cross-cutting/ (27)   # Testing, Database, Playwright, Cascade Review...
│   ├── tooling/      (6)     # MCP, API Protocols, IDE Extension, HSA Toolkit...
│   ├── ai-ml/        (9)     # AI Agents, ML Pipelines, Gemini, RAG...
│   └── governance/   (9)     # Drift Prevention, Session Governance...
├── 🔄 workflows/     (45)    # 45 command handlers (including /skill-create)
├── 📜 rules/                 # Constitutional AI rules
├── 👥 personas/              # Developer, Auditor, Debugger...
└── ⚙️ core/                  # Engine configurations
```

---

## 🤝 Contributing

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

## 📄 License

<p align="center">
  MIT © <a href="https://github.com/nockasdd"><b>NockDev</b></a>
</p>

<!-- Footer: Waving type with darker gradient -->
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:6D28D9,100:1E40AF&height=120&section=footer" width="100%" />
</p>
