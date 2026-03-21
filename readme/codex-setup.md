# HSA + Codex Setup Guide

HSA (Hybrid Search Agent) supports **OpenAI Codex** as an MCP client.

## Quick Setup

Add HSA to your Codex `config.toml`:

```toml
# ~/.codex/config.toml
[mcp.servers.hsa]
type = "stdio"
command = "hsa"
args = ["--stdio"]
```

## Project Root Detection

HSA automatically detects the project root using multiple strategies:

| Priority | Method | Auto? |
|----------|--------|-------|
| **1** | `HSA_PROJECT_PATH` env var | Manual |
| **1.5** | `CODEX_SANDBOX_PROJECT_DIR` env var | Auto (sandbox) |
| **2.6** | `.codex/config.toml` upward detection | Auto |
| **2.7** | Workspace registry (last known) | Auto |
| **3.5** | Git/monorepo markers upward traversal | Auto |

### If auto-detection fails

Set the project path explicitly in `config.toml`:

```toml
[mcp.servers.hsa]
type = "stdio"
command = "hsa"
args = ["--stdio"]
env = { HSA_PROJECT_PATH = "/path/to/your/project" }
```

### Codex sandbox mode

When Codex runs in sandbox mode, it sets `CODEX_SANDBOX_PROJECT_DIR` automatically.
HSA reads this env var at Priority 1.5 — no manual configuration needed.

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `HSA_PROJECT_PATH` | Explicit project root override | No |
| `CODEX_SANDBOX_PROJECT_DIR` | Set by Codex sandbox (auto) | No |
| `HSA_IDE_NAME` | Force IDE name to `codex` | No |
| `CODEX_CLI` / `CODEX_SESSION` | IDE detection markers | Auto |

## Git Worktrees

Codex uses git worktrees for parallel tasks. HSA detects worktree roots automatically
via `.git` file parsing — no configuration needed.

## Troubleshooting

### HSA returns empty search results

1. Check if project root was detected correctly:
   ```
   hsa_report({action: 'status'})
   ```
2. If root is wrong, set `HSA_PROJECT_PATH` explicitly in `config.toml`

### Skills not loading

Project-specific skills (`.agent/skills/`) require correct project root.
If root detection fails, skills fall back to global-only (`~/.nockdev/hsa/skills/`).

### Index is stale

Run `hsa_check_changes()` to force re-index after root correction.
