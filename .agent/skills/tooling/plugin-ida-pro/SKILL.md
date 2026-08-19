---
name: plugin-ida-pro
description: "Use when analyzing or mutating EXE/DLL/binary targets in IDA Pro, or orchestrating bounded multi-call batch/plan flows for reverse engineering."
category: tooling
tier: 1
---

# IDA Pro Binary & Reverse Engineering Workflow

## 1. When To Use

- Any task mentioning `exe`, `dll`, `binary`, `dump`, `packer`, `anti-tamper`, `disassembly`, `decompile`, `xrefs`, `strings`, `struct`, `class`, or `rename`.
- Any task that needs several IDA facts in one pass to avoid latency.
- Any task that mutates names, comments, types, or structs in an IDA database (`.idb`/`.i64`).

---

## 2. Batch Decision Matrix (Anti-Confusion Guide)

| Operation Goal | Correct Mechanism | Why & How |
| :--- | :--- | :--- |
| **Index source code files** in workspace | `nock-hsa index .` (CPG Indexer) | Runs on Node.js runtime, scans project code into AST + SQLite BM25F. |
| **Query multiple arbitrary binary facts** | `ida_batch` | Packs up to 32 discrete commands (e.g., `get_info` + `list_functions` + `decompile`) in 1 HTTP/MCP roundtrip. |
| **Coordinated IDB Struct/Type Refactoring** | `ida_apply_plan` | Applies an ordered refactoring transaction: declarations → structs → renames → local renames → types → comments. |
| **Single targeted query or mutation** | Individual `ida_*` tool | (e.g. `ida_decompile`, `ida_rename_function`, `ida_get_xrefs`). |

---

## 3. Standard Execution Workflow

1. **Discover Live Instances First**:
   ```json
   hsa_bridge({ "action": "discover", "target": "ida" })
   ```
2. **Pin Identity**: Always extract and pin `port` (e.g., `31337`), `instance_key`, `process_id`, or `binary_path`.
3. **Execute Reads or Writes via Batch**:
   - For mixed/read bundles → use `ida_batch`.
   - For full refactoring plans → use `ida_apply_plan`.
   - For mutations → ALWAYS set `allow_mutations: true`.

---

## 4. Exact Payload Schemas & Examples

### A. Mixed/Read Batch (`ida_batch`)
```json
{
  "port": 31337,
  "allow_mutations": false,
  "stop_on_error": true,
  "requests": [
    { "command": "ida_get_info" },
    { "command": "ida_get_segments" },
    { "command": "ida_search_functions", "params": { "pattern": "Decrypt" } },
    { "command": "ida_decompile", "params": { "address": "0x140001000" } }
  ]
}
```

### B. Coordinated Refactoring Plan (`ida_apply_plan`)
```json
{
  "port": 31337,
  "allow_mutations": true,
  "declarations": "typedef unsigned __int64 QWORD;\nstruct PacketHeader { DWORD magic; DWORD size; };",
  "structs": [
    {
      "name": "NetworkSession",
      "members": [
        { "name": "socket_fd", "offset": 0, "size": 4, "type_name": "int" },
        { "name": "is_authenticated", "offset": 4, "size": 1, "type_name": "bool" }
      ]
    }
  ],
  "renames": [
    { "address": "0x140002100", "name": "PacketHandler_ProcessAuth", "scope": "function" }
  ],
  "local_renames": [
    { "function_address": "0x140002100", "old_name": "v3", "new_name": "pHeader" }
  ],
  "types": [
    { "address": "0x140002100", "c_decl": "int __fastcall PacketHandler_ProcessAuth(void* pSession, struct PacketHeader* pHeader)" }
  ],
  "comments": [
    { "address": "0x140002100", "comment": "Discovered via IDA Bridge — auth packet validation entry" }
  ]
}
```

---

## 5. Multi-Instance Pinning Rules & Error Handling

- If bridge returns: `"Multiple live IDA instances are available. Candidates: [31337, 31338]"`:
  1. Call `hsa_bridge(action='discover', target='ida')` to see all loaded binaries.
  2. Choose the specific `port` or `binary_path` matching your target.
  3. Re-send request with `port: 31337` (or whichever port matches your binary).
- Never assume the first port is the active binary.
- Always check `ok: true` in response before considering the operation successful.
