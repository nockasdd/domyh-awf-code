---
name: hsa-toolkit
description: Install and configure DOMYH HSA MCP Server for enhanced AI-powered code intelligence. Provides hybrid BM25+Vector search, CodeGraph tracing, blast radius analysis, persistent memory, design analysis, and 100+ development skills.
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins: [node, npm]
    emoji: 🔌
    homepage: https://www.npmjs.com/package/@nockdev/cli
---

# DOMYH HSA MCP Toolkit

> Hybrid Search + CodeGraph + Impact Analysis + Persistent Memory + Cross-model Cascade

## Quick Install

```bash
# 1. Install nock CLI
npm i -g @nockdev/cli

# 2. Install HSA engine
nock awf hsa install

# 3. Configure MCP for OpenClaw
nock awf mcp install --ide openclaw --scope global
```

After install, restart OpenClaw to load MCP tools.

## Available MCP Tools (16)

### Core Analysis

| Tool | Actions | Description |
|------|---------|-------------|
| `hsa_search` | `context` `files` `skills` `docs` | BM25+Vector hybrid code search, file glob, skill patterns, 84+ library docs |
| `hsa_explore` | `repo_map` `snapshot` | PageRank-ranked file overview, project structure snapshot |
| `hsa_detect` | `stack` `environment` | Detect tech stack, runtimes, package managers, IDE shell |
| `hsa_trace_flow` | `trace` `impact` | Trace call chains (up/down/both) + blast radius analysis (scoring, test gaps) |
| `hsa_check_changes` | — | Merkle diff + re-index changed files (BM25, CodeGraph, Vector) |
| `hsa_prefetch` | — | Pre-load files/library docs into cache for faster retrieval |
| `hsa_feedback` | — | Record file usefulness — improves future search ranking |

### Session & Governance

| Tool | Actions | Description |
|------|---------|-------------|
| `hsa_session` | `persist` `track` `anchor` `drift` `intent` | Session governance: context snapshots, progress tracking, drift detection |
| `hsa_memory` | `store` `recall` `list` `delete` `stats` | Persistent cross-session memory: decisions, patterns, errors, semantic recall |
| `hsa_get_agent_config` | `bootstrap` `commands` `rules` `skills` `modules` `all` | Load DOMYH agent configuration |
| `hsa_report` | `status` `export` `tasks` | Engine health, cache stats, active task list |
| `hsa_delegate` | `prepare` `filter` `cascade` `cascade_read` `cascade_models` `cascade_cancel` | Sub-agent delegation, cross-model cascade |
| `hsa_research` | `index` `overview` `read` `search` `list` `pkg` `releases` `compare` `file` | External repo research, package metadata |
| `hsa_guide` | — | HSA optimal workflow guide |

### Visual & Design

| Tool | Actions | Description |
|------|---------|-------------|
| `hsa_canvas` | `open` `capture` `diff` `update` `extract` `inspect` `close` | LiveCanvas: dev server, screenshots, visual regression, live CSS edits |
| `hsa_design` | `analyze` `health` `tokens` `analyze_image` | Design DNA extraction, WCAG health scoring, W3C DTCG tokens |

## Usage Examples

### Search codebase
```
Search for authentication-related code in my project
```
→ Agent calls `hsa_search({query: "authentication", output_mode: "skeleton"})`

### Blast radius analysis
```
What's the impact of changing the handleLogin function?
```
→ Agent calls `hsa_trace_flow({entry_point: "handleLogin", action: "impact"})`

### Persistent memory
```
Remember this architecture decision for future sessions
```
→ Agent calls `hsa_memory({action: "store", content: "...", category: "decision"})`

### Recall past decisions
```
What architecture decisions did we make before?
```
→ Agent calls `hsa_memory({action: "recall", query: "architecture decisions"})`

### Trace dependencies
```
What functions call the handleLogin function?
```
→ Agent calls `hsa_trace_flow({entry_point: "handleLogin", direction: "upstream"})`

### Design analysis
```
Analyze the CSS design system for accessibility issues
```
→ Agent calls `hsa_design({action: "health", strict: true})`

## Requirements

- **Node.js** 18+ (recommended: 22 LTS)
- **npm** or **pnpm**
- Works on Windows, macOS, Linux
