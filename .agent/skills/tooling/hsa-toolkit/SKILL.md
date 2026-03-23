---
name: hsa-toolkit
description: Install and configure DOMYH HSA MCP Server for enhanced AI-powered code intelligence. Provides hybrid BM25+Vector search, CodeGraph tracing, design analysis, and 100+ development skills.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins: [node, npm]
    emoji: 🔌
    homepage: https://www.npmjs.com/package/@nockdev/cli
---

# DOMYH HSA MCP Toolkit

> Hybrid Search + CodeGraph + Design Analysis + Cross-model Cascade

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

## Available MCP Tools (15)

| Tool | Action | Description |
|------|--------|-------------|
| `hsa_search` | context | BM25+Vector hybrid code search within token budget |
| `hsa_search` | files | Filename/glob search |
| `hsa_search` | skills | Knowledge pattern search |
| `hsa_search` | docs | External library documentation (24+ libs) |
| `hsa_explore` | repo_map | PageRank-ranked file overview with signatures |
| `hsa_explore` | snapshot | Full project snapshot (tree + stack + symbols) |
| `hsa_trace_flow` | - | Trace call chains through dependency graph |
| `hsa_detect` | stack | Detect project tech stack and frameworks |
| `hsa_detect` | environment | Detect installed runtimes and tools |
| `hsa_design` | analyze | Design system analysis (Design DNA) |
| `hsa_design` | health | WCAG accessibility scoring |
| `hsa_delegate` | cascade | Cross-model delegation for complex tasks |
| `hsa_session` | intent | Declare session focus and mode |
| `hsa_check_changes` | - | Merkle diff + re-index changed files |
| `hsa_research` | - | Research external GitHub repos |

## Usage Examples

### Search codebase
```
Search for authentication-related code in my project
```
→ Agent calls `hsa_search({query: "authentication", output_mode: "skeleton"})`

### Explore project structure
```
Give me an overview of the project architecture
```
→ Agent calls `hsa_explore({action: "repo_map"})`

### Trace dependencies
```
What functions call the `handleLogin` function?
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
