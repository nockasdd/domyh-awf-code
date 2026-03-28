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
hsa_bridge(target="x64dbg", action="x64_get_registers")
hsa_bridge(target="x64dbg", action="x64_read_memory", payload={"address": "0x401000", "size": 64})
hsa_bridge(target="x64dbg", action="x64_set_breakpoint", payload={"address": "0x401000"})
hsa_bridge(target="x64dbg", action="x64_step_over")
```

## 🛠️ Available Tools

| Tool | Description |
|------|-------------|
| `x64_get_registers` | Read all CPU registers. |
| `x64_read_memory` | Hex dump memory at the specified address. |
| `x64_get_disasm` | Disassemble instructions. |
| `x64_step_over` | Step over (F8). |
| `x64_step_into` | Step into (F7). |
| `x64_run` | Resume execution (F9). |
| `x64_pause` | Pause execution (F12). |
| `x64_set_breakpoint` | Set a software or hardware breakpoint. |
| `x64_get_modules` | List all loaded modules in the process memory. |
| `x64_get_callstack` | Get the current call stack context. |
