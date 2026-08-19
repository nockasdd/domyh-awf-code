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
hsa_bridge(action="call", target="ida", tool="ida_get_info")
hsa_bridge(action="call", target="ida", tool="ida_decompile", payload={"address": "0x140001000"})
hsa_bridge(action="call", target="ida", tool="ida_rename", payload={"address": "0x140001000", "name": "main"})
hsa_bridge(action="call", target="ida", tool="ida_rename_function", payload={"address": 4198400, "name": "main", "force": false})
hsa_bridge(action="call", target="ida", tool="ida_rename_many", payload={"items": [{"address": "0x140001000", "name": "main"}]})
hsa_bridge(action="call", target="ida", tool="ida_apply_type", payload={"address": "0x140001000", "c_decl": "int __cdecl main(int argc, char **argv)"})
hsa_bridge(action="call", target="ida", tool="ida_apply_plan", payload={"allow_mutations": True, "renames": [{"address": "0x140001000", "name": "main"}]})
hsa_bridge(action="call", target="ida", tool="ida_create_struct", payload={"name": "MY_STRUCT", "members": [{"name": "field_0", "offset": 0, "size": 4}]})
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
| `ida_rename` | Rename a symbol/function with diagnostics and optional force fallback. |
| `ida_rename_function` | Rename the function containing or starting at an address. |
| `ida_rename_global` | Rename the exact address/global label. |
| `ida_rename_many` | Rename several functions/symbols with per-item diagnostics. |
| `ida_rename_local` | Rename a Hex-Rays local variable inside a function. |
| `ida_set_comment` | Set inline or function-level comments. |
| `ida_apply_type` | Apply a C declaration or type to an address. |
| `ida_apply_types` | Apply several C declarations/prototypes to addresses. |
| `ida_set_function_type` | Set a function prototype at an address. |
| `ida_import_c_declarations` | Import C declarations into Local Types. |
| `ida_create_struct` | Create or update a struct/class-like type. |
| `ida_add_struct_member` | Add a member to an existing struct. |
| `ida_set_struct_member_type` | Set a struct member type by member name or offset. |
| `ida_rename_struct_member` | Rename a struct member by member name or offset. |
| `ida_delete_struct_member` | Delete a struct member by offset. |
| `ida_list_structs` | List structs and local types by name pattern. |
| `ida_get_types` | List type inventory using the struct/type fallback. |
| `ida_apply_plan` | Apply declarations, structs, renames, local renames, types, and comments in one bounded plan. |
