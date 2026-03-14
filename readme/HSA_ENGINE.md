<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:0F172A,50:059669,100:10B981&height=160&section=header&text=DOMYH%20HSA&fontSize=42&fontColor=FFFFFF&animation=fadeIn&fontAlignY=35&desc=Hierarchical%20Semantic%20Analysis%20·%20MCP%20Server%20for%20AI%20Code%20Agents&descAlignY=55&descSize=14" width="100%" />
</p>

<p align="center">
  <a href="https://www.npmjs.com/package/@nockdev/hsa"><img src="https://img.shields.io/npm/v/@nockdev/hsa?style=for-the-badge&logo=npm&logoColor=white&labelColor=CB3837&color=000000" alt="npm" /></a>
  <img src="https://img.shields.io/badge/MCP%20tools-15-10B981?style=for-the-badge&logo=puzzle&logoColor=white" alt="MCP Tools" />
  <img src="https://img.shields.io/badge/node-%E2%89%A518-3B82F6?style=for-the-badge&logo=nodedotjs&logoColor=white" alt="Node.js" />
  <img src="https://img.shields.io/badge/license-MIT-8B5CF6?style=for-the-badge&logo=opensourceinitiative&logoColor=white" alt="License" />
</p>

<p align="center">
  Token-optimized MCP context engine with <b>BM25+ search</b>, <b>Merkle tree</b> change detection, <b>Doc Fetcher</b> for external library docs, <b>LiveCanvas</b> visual feedback, and <b>real-time dashboard</b>.<br/>
  Part of the <a href="https://github.com/nockasdd/domyh-auto-accept"><b>DOMYH Awesome Code Agent</b></a> framework.
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
| 🔍 **Hybrid Search** | BM25+ full-text + CodeGraph + vector search with query expansion |
| 🌳 **Merkle Tree** | O(log n) change detection — instant diff for large codebases |
| 🎯 **Token Budget** | Smart truncation (simple, semantic, code-aware, skeleton, progressive) |
| 💾 **LRU Cache** | Semantic caching with TTL + background revalidation |
| 📚 **Doc Fetcher** | Fetch & search external library docs (llms.txt, npm README, local files, custom URLs) |
| 🎨 **LiveCanvas** | Visual feedback loop — screenshots, visual regression, live CSS edits via CDP |
| 🖌️ **Design System** | Extract Design DNA, health scoring (WCAG), W3C DTCG token generation |
| 🌐 **Browser Engine** | Playwright-powered: screenshot, element inspection, page analysis |
| 🧠 **Session Gov** | Intent declaration, drift detection, 3-level progress tracking, persistent anchors |
| 📊 **Web Dashboard** | Real-time monitoring at `localhost:13100/dashboard` |
| 🔒 **Integrity** | SHA-256 tamper detection across all bundled files |
| 🖥️ **Daemon Mode** | Background process with HTTP transport + OAuth 2.1 |

---

## 🛠️ MCP Tools (15)

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
| `hsa_guide` | — | HSA optimal workflow guide |

### Visual & Design

| Tool | Actions | Description |
|:-----|:--------|:------------|
| `hsa_canvas` | `open` `capture` `diff` `update` `extract` `inspect` `close` | LiveCanvas: dev server, screenshots, visual regression, live CSS edits |
| `hsa_design` | `analyze` `health` `tokens` `analyze_image` | Design DNA extraction, WCAG health scoring, W3C DTCG tokens |

---

## 📚 Doc Fetcher — External Library Documentation

HSA can fetch, index, and search external library documentation. This powers the `hsa_search(action: "docs")` tool.

### Supported Sources (Priority Order)

| Priority | Source | Example |
|:---------|:-------|:--------|
| 1 | **llms.txt Registry** (24 libraries) | `nextjs`, `prisma`, `react` |
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

### Built-in Registry (24 Libraries)

<details>
<summary>Click to expand</summary>

| Library | Source |
|:--------|:-------|
| Next.js | llms.txt |
| React | llms.txt |
| Svelte | llms.txt |
| Vue.js | llms.txt |
| Angular | llms.txt |
| Nuxt | llms.txt |
| Nuxt UI | llms.txt |
| Astro | llms.txt |
| Prisma | llms.txt |
| Drizzle | llms.txt |
| shadcn/ui | llms.txt |
| Radix UI | llms.txt |
| TanStack | llms.txt |
| Vercel AI SDK | llms.txt |
| Supabase | llms.txt |
| Clerk | llms.txt |
| Better Auth | llms.txt |
| Stripe | llms.txt |
| Resend | llms.txt |
| Upstash | llms.txt |
| Zustand | llms-full.txt |
| Convex | llms.txt |
| Sanity | llms.txt |
| Mintlify | llms.txt |
| **Tailwind CSS** | **Local docs** (bundled) |

</details>

---

## ️ Web Dashboard

```bash
nock awf hsa start    # Dashboard at http://localhost:13100/dashboard
```

| Page | Description |
|:-----|:------------|
| `/dashboard` | Real-time project stats, cache metrics, indexed skills |
| `/logs` | Tool call history, search queries, performance traces |
| `/health` | Health check endpoint for monitoring |

---

## 📋 Requirements

- **Node.js** ≥ 18.0.0

## 📄 License

MIT © [**NockDev**](https://github.com/nockasdd)

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:10B981,50:059669,100:0F172A&height=100&section=footer" width="100%" />
</p>
