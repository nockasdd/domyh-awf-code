---
name: plugin-ida-pro
description: "Advanced IDA Pro & Hex-Rays reverse engineering: struct reconstruction, VTable binding, type propagation, and batch refactoring."
category: tooling
tier: 1
---

# IDA Pro Binary & Reverse Engineering Workflow

## 1. When To Use

- Any task analyzing or mutating `exe`, `dll`, `so`, `dylib`, or memory dumps.
- Decompiler analysis, function renaming, C-type imports, and struct layout synthesis.
- Transforming raw pointer arithmetic (`*(QWORD*)(a1 + 0x18)`) into typed C-struct references (`pSession->rx_buffer`).
- Reconstructing C++ VTables (`CLASSNAME_vtbl`) to turn indirect calls (`(*vftable + 0x20)(...)`) into clear method calls.

---

## 2. Batch Decision Matrix (Anti-Confusion Guide)

| Operation Goal | Correct Mechanism | Why & How |
| :--- | :--- | :--- |
| **Index source code files** in workspace | `nock-hsa index .` (CPG Indexer) | Scans project source files into AST + SQLite BM25F on Node.js runtime. |
| **Query multiple arbitrary binary facts** | `ida_batch` | Packs up to 32 discrete commands (e.g. `get_info` + `list_functions` + `decompile`) in 1 roundtrip. |
| **Coordinated IDB Struct/Type Refactoring** | `ida_apply_plan` | Executes ordered refactoring transaction: declarations → structs → renames → local renames → types → comments. |
| **Single targeted query or mutation** | Individual `ida_*` tool | (e.g. `ida_decompile`, `ida_rename_function`, `ida_get_xrefs`). |

---

## 3. Pointer-to-Struct & VTable Transformation Protocol

When decompiled pseudocode exhibits raw pointer offsets (`*(DWORD*)(a1 + 0x8)`) or indirect calls, follow this 4-step reconstruction protocol:

```
[1. HARVEST OFFSETS] ➔ [2. SYNTHESIZE STRUCTS] ➔ [3. IMPORT & PROPAGATE] ➔ [4. VERIFY CLEAN PSEUDOCODE]
```

### Step 1: Harvest Offsets from Disassembly / Pseudocode
Trace all field accesses on the pointer argument (e.g., `a1`):
*   `+0x00`: `__vftable` (VTable pointer, 8 bytes)
*   `+0x08`: `socket_fd` (4 bytes `int`)
*   `+0x0C`: `_pad0C` (4 bytes padding)
*   `+0x10`: `session_id` (8 bytes `long long`)
*   `+0x18`: `rx_buffer` (8 bytes pointer `PacketBuffer*`)
*   `+0x20`: `is_authenticated` (1 byte `bool`)

### Step 2: Formulate C Structs & VTable Declarations
Hex-Rays recognizes C++ classes and VTables when named `CLASSNAME_vtbl` with field `__vftable`:

```c
struct PacketBuffer;
struct NetworkSession;

struct NetworkSession_vtbl {
    int (__fastcall *InitSession)(struct NetworkSession* this, int port);
    void (__fastcall *CloseSession)(struct NetworkSession* this);
    int (__fastcall *ProcessAuth)(struct NetworkSession* this, void* pHeader);
};

struct NetworkSession {
    struct NetworkSession_vtbl* __vftable; // +0x00
    int socket_fd;                         // +0x08
    int _pad0C;                            // +0x0C
    long long session_id;                  // +0x10
    struct PacketBuffer* rx_buffer;        // +0x18
    bool is_authenticated;                 // +0x20
};
```

### Step 3: Apply via `ida_apply_plan`
```json
{
  "port": 31337,
  "allow_mutations": true,
  "declarations": "struct PacketBuffer; struct NetworkSession; struct NetworkSession_vtbl { int (__fastcall *InitSession)(struct NetworkSession* this, int port); void (__fastcall *CloseSession)(struct NetworkSession* this); int (__fastcall *ProcessAuth)(struct NetworkSession* this, void* pHeader); }; struct NetworkSession { struct NetworkSession_vtbl* __vftable; int socket_fd; int _pad0C; long long session_id; struct PacketBuffer* rx_buffer; bool is_authenticated; };",
  "types": [
    { "address": "0x140002100", "c_decl": "int __fastcall PacketHandler_ProcessAuth(struct NetworkSession* pSession, void* pHeader)" }
  ],
  "renames": [
    { "address": "0x140002100", "name": "PacketHandler_ProcessAuth", "scope": "function" }
  ],
  "local_renames": [
    { "function_address": "0x140002100", "old_name": "a1", "new_name": "pSession" }
  ],
  "comments": [
    { "address": "0x140002100", "comment": "Reconstructed NetworkSession struct and virtual dispatch" }
  ]
}
```

### Step 4: Verify Clean Pseudocode
Call `ida_decompile(address="0x140002100")`. Verify that `*(QWORD*)(a1 + 0x18)` is now cleanly rendered as `pSession->rx_buffer` and virtual calls render as `pSession->__vftable->ProcessAuth(pSession, pHeader)`.

---

## 4. Multi-Instance Pinning & Error Recovery

- If bridge returns: `"Multiple live IDA instances are available. Candidates: [31337, 31338]"`:
  1. Call `hsa_bridge(action='discover', target='ida')` to list all loaded binaries and ports.
  2. Pin exact `port` (e.g., `31337`) or `binary_path` matching your target.
  3. Always pass `"port": 31337` in every subsequent payload.
- Always check `"ok": true` before proceeding.
