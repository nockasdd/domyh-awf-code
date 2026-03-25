<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:0F172A,50:059669,100:10B981&height=160&section=header&text=DOMYH%20HSA&fontSize=42&fontColor=FFFFFF&animation=fadeIn&fontAlignY=35&desc=Hierarchical%20Semantic%20Analysis%20·%20MCP%20Server%20for%20AI%20Code%20Agents&descAlignY=55&descSize=14" width="100%" />
</p>

<p align="center">
  <a href="https://www.npmjs.com/package/@nockdev/hsa"><img src="https://img.shields.io/npm/v/@nockdev/hsa?style=for-the-badge&logo=npm&logoColor=white&labelColor=CB3837&color=000000" alt="npm" /></a>
  <img src="https://img.shields.io/badge/MCP%20tools-15-10B981?style=for-the-badge&logo=puzzle&logoColor=white" alt="MCP Tools" />
  <img src="https://img.shields.io/badge/docs-84+-06B6D4?style=for-the-badge&logo=bookstack&logoColor=white" alt="Built-in Docs" />
  <img src="https://img.shields.io/badge/node-%E2%89%A518-3B82F6?style=for-the-badge&logo=nodedotjs&logoColor=white" alt="Node.js" />
  <img src="https://img.shields.io/badge/license-MIT-8B5CF6?style=for-the-badge&logo=opensourceinitiative&logoColor=white" alt="License" />
</p>

<p align="center">
  Token-optimized MCP context engine with <b>BM25+ search</b>, <b>HNSW vector search</b>, <b>Merkle tree</b> change detection, <b>84+ built-in library docs</b>, <b>cross-model cascade delegation</b>, <b>LiveCanvas</b> visual feedback, and <b>real-time dashboard</b>.<br/>
  Part of the <a href="https://github.com/nockasdd/domyh-awf-code"><b>DOMYH AWF </b></a> framework.
</p>

---

## ⚡ Quick Start

```bash
# Via nock-cli (recommended)
npm install -g @nockdev/cli
nock awf hsa start

# Or run standalone via npx
npx -y @nockdev/hsa@latest

# Or install globally
npm install -g @nockdev/hsa
nock-hsa
```

---

## ✨ Features

| Feature | Description |
|:--------|:------------|
| 🔍 **Hybrid Search** | BM25+ full-text + CodeGraph + HNSW vector search with automatic query expansion |
| 🏆 **Relevance Reranking** | Multi-signal reranking (PageRank, recency, feedback) for search result quality |
| 🧬 **Knowledge Graph** | Semantic edges between symbols — auto-built from imports, calls, and type relationships |
| 🌳 **Merkle Tree** | O(log n) change detection — instant incremental re-indexing for large codebases |
| 🎯 **Context Compaction** | Smart truncation strategies (simple, semantic, code-aware, skeleton, progressive, chunked) |
| 💾 **LRU Cache** | Semantic caching with TTL + background revalidation |
| 📚 **Doc Fetcher** | 84+ built-in library docs + llms.txt, npm README, local files, custom URLs |
| 🔬 **External Research** | GitHub repo indexing, npm/PyPI package metadata, release notes, remote file reading |
| 🔄 **Cross-Model Cascade** | Delegate tasks to Gemini, Claude, GPT models with dashboard-configurable routing |
| 🎨 **LiveCanvas** | Visual feedback loop — dev server management, screenshots, visual regression, live CSS edits via CDP |
| 🖌️ **Design Intelligence** | Design DNA extraction, WCAG health scoring (0-100), W3C DTCG token generation, image analysis |
| 🌐 **Browser Engine** | Playwright-powered: screenshot, element inspection, page analysis |
| 🧠 **Session Governance** | Intent declaration, drift detection, 3-level progress tracking, persistent anchors |
| 📊 **Web Dashboard** | Real-time 3-tab SPA (Dashboard · Graph · Logs) at `localhost:13100` |
| 📋 **Activity Ledger** | Tool call tracking, latency measurement, per-tool usage statistics |
| 📲 **Notifications** | Telegram Bot + Discord Webhook for session persistence and task completion alerts |
| 🔒 **Integrity** | SHA-256 tamper detection across all 490+ bundled files |
| 🖥️ **Daemon Mode** | Background process with HTTP transport + OAuth 2.1 |

---

## 🛠️ MCP Tools (15)

> 15 public tools with 40+ actions covering search, exploration, delegation, design, and session governance.

### Core Analysis

| Tool | Actions | Description |
|:-----|:--------|:------------|
| `hsa_search` | `context` `files` `skills` `docs` | Hybrid code search, file glob, skill patterns, external library docs |
| `hsa_explore` | `repo_map` `snapshot` | PageRank-ranked file overview, project structure snapshot |
| `hsa_detect` | `stack` `environment` | Detect tech stack, frameworks, runtimes, package managers |
| `hsa_check_changes` | — | Check file changes via Merkle tree diff, re-index BM25/CodeGraph |
| `hsa_trace_flow` | — | Trace code execution flow through dependency graph (up to 5 hops) |
| `hsa_prefetch` | — | Pre-load files/library docs into cache for faster retrieval |
| `hsa_feedback` | — | Record file usefulness — improves future search ranking |

### Session & Governance

| Tool | Actions | Description |
|:-----|:--------|:------------|
| `hsa_session` | `persist` `track` `anchor` `drift` `intent` | Session governance: context snapshots, progress tracking, drift detection |
| `hsa_get_agent_config` | `bootstrap` `commands` `rules` `skills` `modules` `all` | Load DOMYH agent configuration, rules, skills |
| `hsa_report` | `status` `export` `tasks` | Engine health, cache stats, active task list |
| `hsa_delegate` | `prepare` `filter` `cascade` `cascade_read` `cascade_models` `cascade_cancel` | Sub-agent delegation, cross-model cascade |
| `hsa_research` | `index` `overview` `read` `search` `list` `refresh` `delete` `pkg` `releases` `compare` `file` | External repo research, package metadata, release notes, remote file reading |
| `hsa_guide` | — | HSA optimal workflow guide |

### Visual & Design

| Tool | Actions | Description |
|:-----|:--------|:------------|
| `hsa_canvas` | `open` `capture` `diff` `update` `extract` `inspect` `close` | LiveCanvas: dev server, screenshots, visual regression, live CSS edits |
| `hsa_design` | `analyze` `health` `tokens` `analyze_image` | Design DNA extraction, WCAG health scoring, W3C DTCG tokens |

---

## 📚 Doc Fetcher — 84+ Built-in Library Docs

HSA ships with **84+ pre-bundled documentation files** covering major frameworks, languages, and tools. Additional docs can be fetched from llms.txt, npm, or custom URLs via `hsa_search(action: "docs")`.

### Supported Sources (Priority Order)

| Priority | Source | Example |
|:---------|:-------|:--------|
| 1 | **Bundled docs** (84+ libraries) | `nextjs`, `prisma`, `react`, `tailwindcss`, `go`, `rust`... |
| 1.5 | **Local docs folder** `~/.nockdev/hsa/docs/{lib}.md` | `tailwindcss.md` |
| 2 | **npm homepage probe** `/llms.txt` | Auto-probed from npm registry |
| 3 | **npm README fallback** | Packages with long READMEs |
| — | **Custom URL** | Any `https://` .md file |
| — | **Local file path** | Any local `.md`, `.txt`, `.mdx` file |

### Usage

```bash
# Search docs by library name (auto-resolves source)
hsa_search(action: "docs", query: "dark mode", doc_libraries: ["tailwindcss"])

# Search docs from a custom URL
hsa_search(action: "docs", query: "installation", doc_libraries: ["https://raw.githubusercontent.com/microsoft/playwright/main/README.md"])

# Search docs from a local file
hsa_search(action: "docs", query: "api reference", doc_libraries: ["/path/to/my-docs.md"])

# Prefetch library docs for faster search
hsa_prefetch(libs: ["nextjs", "prisma", "tailwindcss"])
```

### Adding Custom Documentation

Place `.md` files in `~/.nockdev/hsa/docs/` named after the npm package:

```bash
# File name must match npm package name
~/.nockdev/hsa/docs/tailwindcss.md    # → hsa_search(docs, ["tailwindcss"])
~/.nockdev/hsa/docs/my-lib.md         # → hsa_search(docs, ["my-lib"])
~/.nockdev/hsa/docs/my-lib-docs.md    # → also matches "my-lib"
```

The file is automatically discovered when you search for that library name. No configuration needed.

### Built-in Registry (84+ Libraries)

<details>
<summary>Click to expand</summary>

| Category | Libraries |
|:---------|:----------|
| **Frameworks** | Next.js, React, Vue.js, Angular, Svelte, Nuxt, Astro, Expo, React Native, Flutter |
| **CSS/UI** | Tailwind CSS (v2, v3, v4), shadcn/ui, Nuxt UI, Framer Motion, Lottie |
| **Backend** | Node.js, Express, NestJS, Hono, FastAPI, Django, Flask, Laravel, Ruby on Rails |
| **Database** | Prisma, Drizzle, Mongoose, PostgreSQL, Redis, Entity Framework |
| **Languages** | TypeScript, Python, Go, Rust, C#, Java, PHP, C++ (C++14/17/20) |
| **DevOps** | Docker, Kubernetes, Terraform, GitHub Actions, Vite, Turborepo |
| **Testing** | Playwright, Vitest, Jest, Cypress, Storybook |
| **AI/API** | OpenAI, Anthropic, Gemini, Vercel AI SDK, tRPC, GraphQL, Socket.IO |
| **Auth/Payment** | Clerk, Supabase, Stripe, Zustand |
| **Other** | MCP, Deno, Bun, ESLint, Zod (v3, v4), Three.js, D3.js, Chart.js, GSAP, PixiJS |

</details>

---

## 🖥️ Web Dashboard

```bash
nock awf hsa start    # Dashboard at http://localhost:13100/dashboard
```

Single-page app with 3 tabs — all accessible from the tab bar:

| Tab | Description |
|:----|:------------|
| **📊 Dashboard** | KPIs, tech stack, AI engine status, memory health, active skills, project explorer, activity feed, cache/latency charts, PageRank rankings |
| **🕸️ Graph** | Interactive CodeGraph force-directed visualization (nodes = files, edges = imports) |
| **📋 Logs** | Real-time tool call logs with filtering, SSE streaming, per-tool stats |
| `/health` | Health check endpoint for monitoring |

---

## 📋 Requirements

- **Node.js** ≥ 18.0.0

## 📄 License

MIT © [**NockDev**](https://github.com/nockasdd)

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:10B981,50:059669,100:0F172A&height=100&section=footer" width="100%" />
</p>
