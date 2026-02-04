# 🌐 HSA MCP Server

> **Version**: 6.0.0 | **Node.js**: ≥18.0.0 | **Author**: NockDev

Model Context Protocol server for HSA intelligent context management.

---

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Build
npm run build

# Run (stdio mode for MCP)
npm start

# Run (HTTP mode for testing)
npm run start:http
```

---

## 📋 Available Tools

### Core Context Tools

| Tool                | Description                                           |
| ------------------- | ----------------------------------------------------- |
| `hsa_get_context`   | Get optimized context for files with semantic caching |
| `hsa_detect_stack`  | Detect project tech stack                             |
| `hsa_check_changes` | Check file changes via Merkle tree                    |
| `hsa_prefetch`      | Prefetch predicted files                              |
| `hsa_status`        | Get engine health status                              |

### Optimization Tools

| Tool                   | Description                        |
| ---------------------- | ---------------------------------- |
| `hsa_cache_stats`      | View cache hit/miss statistics     |
| `hsa_clear_cache`      | Clear all caches                   |
| `hsa_optimize_context` | Compress context for token savings |

### Multi-Agent Tools

| Tool                | Description               |
| ------------------- | ------------------------- |
| `hsa_agent_request` | Submit request from agent |
| `hsa_agent_sync`    | Synchronize agent state   |

---

## ⚙️ Configuration

### Claude Desktop

Add to `~/.config/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "hsa": {
      "command": "node",
      "args": ["/path/to/.agent/mcp/hsa-server/dist/index.js"],
      "env": {
        "HSA_PROJECT_PATH": "/path/to/project"
      }
    }
  }
}
```

### Environment Variables

| Variable           | Default | Description                          |
| ------------------ | ------- | ------------------------------------ |
| `HSA_PROJECT_PATH` | cwd     | Project root path                    |
| `HSA_SCRIPTS_PATH` | auto    | Path to Python scripts               |
| `HSA_PYTHON_PATH`  | python  | Python executable                    |
| `HSA_LOG_LEVEL`    | info    | Log level (debug, info, warn, error) |
| `HSA_CACHE_TTL`    | 3600    | Cache TTL in seconds                 |
| `HSA_MAX_TOKENS`   | 8000    | Default token budget                 |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP Server (TypeScript)                  │
├─────────────────────────────────────────────────────────────┤
│  tools.ts     │  config.ts    │  streaming.ts │  health.ts  │
│  Tool defs    │  Configuration│  SSE support  │  Health     │
├───────────────┴───────────────┴───────────────┴─────────────┤
│                python-bridge.ts (IPC)                       │
├─────────────────────────────────────────────────────────────┤
│                 HSA Python Engine (hsa/)                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧪 Development

```bash
# Development mode (auto-reload)
npm run dev

# Type checking
npm run typecheck

# Linting
npm run lint

# Tests
npm test
```

---

## 📁 File Structure

```
hsa-server/
├── src/
│   ├── index.ts           # MCP entry point
│   ├── tools.ts           # Tool definitions
│   ├── config.ts          # Configuration
│   ├── python-bridge.ts   # Python IPC
│   ├── health.ts          # Health checks
│   ├── streaming.ts       # SSE support
│   ├── optimization.ts    # Caching & compression
│   └── multi-agent.ts     # Multi-agent coordination
├── dist/                  # Compiled output
├── tests/                 # Test files
├── package.json
└── tsconfig.json
```

---

_HSA MCP v6.0.0 • DOMYH Awesome Code • NockDev_
