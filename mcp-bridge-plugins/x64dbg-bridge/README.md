# x64dbg MCP Bridge

HSA MCP Bridge Server for x64dbg debugger via [x64dbg-automate](https://github.com/dariushoule/x64dbg-automate).

## 🌉 Architecture

```mermaid
flowchart LR
    A[HSA Engine\n(DOMYH Agent)] <-->|stdio| B(Bridge Server\nx64dbg-bridge/server.py)
    B <-->|ZMQ| C[x64dbg-automate.dp64\nInside x64dbg]
    C <-->|Native API| D[(Debugged Process)]
```

## 📦 Prerequisites

1. **x64dbg** with the `x64dbg-automate` plugin installed (`.dp64`/`.dp32`)
2. **Python 3.10+**
3. **uv** package manager (`pip install uv`)

## 🚀 Setup & Installation

### 1. Install the x64dbg-automate plugin

Download the latest plugin from [x64dbg-automate releases](https://github.com/dariushoule/x64dbg-automate/releases).

Extract contents into:
- `x64dbg/release/x64/plugins/` (for 64-bit binaries)
- `x64dbg/release/x32/plugins/` (for 32-bit binaries)

Required files:
- `x64dbg-automate.dp64` (or `.dp32`)
- `libzmq-mt-4_3_5.dll`

### 2. Install Python dependencies

In the `mcp-bridge-plugins/x64dbg-bridge` directory:
```bash
uv sync
```
*(This installs the x64dbg-automate python package and FastMCP).*

### 3. Usage via HSA

Open x64dbg, load and attach to a binary, then let the DOMYH Agent take control. The agent will automatically start the bridge server.

**Example MCP Tool Calls used by the Agent:**

```python
hsa_bridge(target="x64dbg", action="x64_list_sessions")
hsa_bridge(target="x64dbg", action="x64_auto_connect", payload={"pid": 1234})
hsa_bridge(target="x64dbg", action="x64_get_modules")
hsa_bridge(target="x64dbg", action="x64_find_string", payload={"pattern": "CreateFile", "module_name": "kernel32"})
hsa_bridge(target="x64dbg", action="x64_find_references", payload={"address": "0x7FF9E67E0000"})
```

## 🛠️ Available Tools

Generated from `server.py` — the ten `@mcp.tool()` functions it actually defines.

| Tool | Description | Params |
|------|-------------|--------|
| `x64_list_sessions` | List running x64dbg sessions and their PIDs. | `scan_ports` |
| `x64_auto_connect` | Connect to a running x64dbg session, by PID or the first found. | `pid`, `session_id` |
| `x64_start_session` | Launch x64dbg with a target executable. *(mutates)* | `executable`, `args` |
| `x64_attach_process` | Attach x64dbg to a process PID. *(mutates)* | `pid` |
| `x64_get_modules` | List loaded modules with base addresses and sizes. | `pid`, `session_id`, `module_name`, `module_path`, `scan_ports` |
| `x64_find_string` | Search readable memory for ASCII/UTF-16 strings, optionally scoped to one module. | `pattern`, `max_results`, `pid`, `session_id`, `module_name`, `module_path` |
| `x64_find_pattern` | Search memory for a hex byte pattern, optionally scoped to one module. | `hex_pattern`, `max_results`, `pid`, `session_id`, `module_name`, `module_path` |
| `x64_find_references` | Search code sections for references to an address. | `address`, `pid`, `session_id`, `module_name`, `module_path` |
| `x64_find_api_calls` | Resolve an API address and return the address to pass to `x64_find_references`. | `api_name`, `pid`, `session_id`, `module_name`, `module_path` |
| `x64_search_command` | Execute a raw x64dbg command. *(mutates)* | `command`, `pid`, `session_id` |

### What this bridge does not do

There is no register read, memory read, disassembly, stepping, or callstack tool.
Those come from the upstream `x64dbg-automate` MCP server, which this bridge runs
alongside — the HSA tool manifest only covers what `server.py` here defines.

`x64_search_command` passes its argument straight to the debugger with no
validation, so treat it as a debugger console and prefer the specific tools
above.
