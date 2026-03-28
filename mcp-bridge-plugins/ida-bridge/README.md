# IDA Pro MCP Bridge

HSA MCP Bridge Server for Hex-Rays IDA Pro 8.x / 9.x.

## 🌉 Architecture

```mermaid
flowchart LR
    A[HSA Engine\n(DOMYH Agent)] <-->|stdio| B(Bridge Server\nida-bridge/server.py)
    B <-->|HTTP port 28472| C[hsa_ida_plugin.py\nInside IDA]
    C <-->|IDAPython API| D[(IDA Database)]
```

> **Note:** For IDA 9.x+ with `idalib` configured, this bridge also supports a headless mode where `server.py` runs `idalib` directly without needing the GUI open.

## 📦 Prerequisites

1. **IDA Pro 8.x or 9.x** with Hex-Rays Decompiler.
2. **Python 3.10+** (must be the same architecture as your IDA installation, usually 64-bit).
3. **uv** package manager (`pip install uv`).

## 🚀 Setup & Installation

### 1. Install Python Dependencies
In the `mcp-bridge-plugins/ida-bridge` directory, initialize the environment:
```bash
uv sync
```
*(This installs FastAPI, Uvicorn, and other required dependencies).*

### 2. Install the IDA Plugin
Copy the plugin file into your IDA installation's plugins folder:
- **Source:** `mcp-bridge-plugins/ida-bridge/hsa_ida_plugin.py`
- **Destination:** `%IDADIR%/plugins/hsa_ida_plugin.py`

### 3. Start the Bridge inside IDA
1. Open your binary in IDA Pro.
2. Wait for auto-analysis to finish.
3. Press `Ctrl+Shift+H` (or run the "HSA MCP Bridge" plugin from the Edit -> Plugins menu).
4. The output window will show: `[HSA] Listening on http://127.0.0.1:28472`

## 💻 Usage via HSA

The DOMYH Agent will automatically spawn the external bridge server when it needs to interact with IDA. You can prompt the agent to analyze malware, decompile functions, or rename variables.

**Example MCP Tool Calls used by the Agent:**

```python
hsa_bridge(target="ida", action="ida_get_info")
hsa_bridge(target="ida", action="ida_decompile", payload={"address": "0x140001000"})
hsa_bridge(target="ida", action="ida_rename", payload={"address": "0x140001000", "name": "main"})
hsa_bridge(target="ida", action="ida_search_string", payload={"pattern": "password", "max_results": 10})
```

## 🛠️ Available Tools

| Tool | Description |
|------|-------------|
| `ida_get_info` | Get basic info about the loaded IDA database. |
| `ida_list_functions` | List functions in the database with pagination. |
| `ida_search_functions` | Search functions by name pattern (regex supported). |
| `ida_decompile` | Decompile a function at a specific hex address. |
| `ida_get_disasm` | Get raw assembly instructions at an address. |
| `ida_get_xrefs` | Get cross-references (to or from) an address. |
| `ida_read_bytes` | Read raw bytes from the database. |
| `ida_search_bytes` | Search for a hex byte pattern in the binary (supports `??`). |
| `ida_get_strings` | Get all extracted strings in the database. |
| `ida_search_string` | Search strings using substring or pattern. |
| `ida_get_segments` | List all memory segments and permissions. |
| `ida_rename` | Rename a symbol, function, or auto-generated local variable. |
| `ida_set_comment` | Set inline or function-level comments. |
