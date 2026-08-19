---
name: plugin-ida-pro
description: "Advanced IDA Pro & Hex-Rays reverse engineering: 8-pillar decompilation mastery, struct reconstruction, VTables, enums, unions, usercall, and batch refactoring."
category: tooling
tier: 1
---

# IDA Pro Binary & Reverse Engineering Workflow

## 1. When To Use

- Analyzing or mutating `exe`, `dll`, `so`, `dylib`, or memory dumps.
- Full decompilation refinement: transforming raw offsets (`*(ptr + 0x18)`) into typed C structs.
- Resolving magic numbers into Enums and Bitfields.
- Binding C++ VTables (`CLASSNAME_vtbl`) to turn indirect calls into typed method calls.
- Normalizing custom register calling conventions (`__usercall`).

---

## 2. Batch Decision Matrix (Anti-Confusion Guide)

| Operation Goal | Correct Mechanism | Why & How |
| :--- | :--- | :--- |
| **Index source code files** in workspace | `nock-hsa index .` (CPG Indexer) | Scans project source files into AST + SQLite BM25F on Node.js runtime. |
| **Query multiple arbitrary binary facts** | `ida_batch` | Packs up to 32 discrete commands (e.g. `get_info` + `list_functions` + `decompile`) in 1 roundtrip. |
| **Coordinated IDB Struct/Type Refactoring** | `ida_apply_plan` | Executes ordered refactoring transaction: declarations → structs → renames → local renames → types → comments. |
| **Single targeted query or mutation** | Individual `ida_*` tool | (e.g. `ida_decompile`, `ida_rename_function`, `ida_get_xrefs`). |

---

## 3. The Complete 8-Pillar Decompilation Mastery

```
[1. FLIRT & CRT] ➔ [2. CALLING CONVENTION] ➔ [3. STRUCT & UNIONS] ➔ [4. VTABLE & RTTI] ➔ [5. ENUMS] ➔ [6. ARRAYS] ➔ [7. SPLIT LVARS] ➔ [8. VERIFY]
```

### Pillar 1: FLIRT Signatures & CRT Noise Filtering
- Apply static CRT signatures before analyzing user code:
  `hsa_bridge(action='call', target='ida', tool='ida_apply_sig', payload={sig_name: 'vc_ucrt'})`
- Skip `mainCRTStartup` / `__scrt_common_main_seh` to jump straight to the real user `main()` or `WinMain()`.

### Pillar 2: Custom Calling Conventions & Register Arguments (`__usercall`)
When functions receive non-standard register parameters, declare explicit prototypes to eliminate dummy register variables (`_ESI`, `_EBX`):
```c
int __usercall ProcessBuffer@<eax>(void* pBuffer@<esi>, int length@<ebx>, int flags@<ecx>);
```

### Pillar 3: Structs & Tagged Unions (Resolving Overlapping Offsets)
```c
union PacketPayload {
    struct LoginRequest  login;
    struct ChatMessage   chat;
    unsigned char        raw_bytes[256];
};

struct Packet {
    int                  opcode;
    int                  length;
    union PacketPayload  payload; // offset +0x08
};
```

### Pillar 4: C++ RTTI & VTable Virtual Dispatch Binding
1. Extract RTTI class descriptor from `.rdata` (preceding vtable).
2. Define `CLASSNAME_vtbl` struct with function pointers.
3. Define class with `__cppobj` and `__vftable` member pointer:
```c
struct __cppobj NetworkSession {
    struct NetworkSession_vtbl* __vftable; // +0x00
    int socket_fd;                         // +0x08
    int _pad0C;                            // +0x0C
    long long session_id;                  // +0x10
    struct PacketBuffer* rx_buffer;        // +0x18
    bool is_authenticated;                 // +0x20
};
```
*Result*: Indirect calls `(*(_QWORD*)a1 + 0x20)(a1, pHeader)` become `pSession->__vftable->ProcessAuth(pSession, pHeader)`.

### Pillar 5: Enums, Bitfields & Magic Number Resolution
Convert conditional raw constants (`(flags & 0x400) != 0 && state == 3`) into typed Enums:
```c
enum SessionState : int { STATE_DISCONNECTED = 0, STATE_AUTHENTICATED = 2, STATE_TIMEOUT = 3 };
enum PacketFlags : unsigned int { FLAG_NONE = 0, FLAG_ASYNC = 0x0400, FLAG_RELIABLE = 0x0800 };
```

### Pillar 6: Array Stride & Switch Jump Tables
- When seeing `base + 56 * i + 16`: recognize `sizeof(GameItem) == 56` and assign `GameItem g_ItemTable[100];` so it decompiles to `g_ItemTable[i].item_price`.

### Pillar 7: Local Variable Splitting (`split_lvar`)
- When compiler register allocation reuses `RAX` for two unrelated variables in separate scopes, use `split_lvar` to decouple their types and lifespans.

### Pillar 8: Verification of Clean Pseudocode
- Call `ida_decompile` to verify pseudocode reads like original source code without pointer arithmetic artifacts.

---

## 4. Example Coordinated Refactoring Plan (`ida_apply_plan`)

```json
{
  "port": 31337,
  "allow_mutations": true,
  "declarations": "enum SessionState : int { STATE_DISCONNECTED = 0, STATE_TIMEOUT = 3 }; enum PacketFlags : unsigned int { FLAG_ASYNC = 0x0400 }; struct PacketBuffer; struct NetworkSession; struct NetworkSession_vtbl { int (__fastcall *ProcessAuth)(struct NetworkSession* this, void* pHeader); }; struct NetworkSession { struct NetworkSession_vtbl* __vftable; int socket_fd; int _pad0C; struct PacketBuffer* rx_buffer; enum SessionState state; enum PacketFlags flags; };",
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
    { "address": "0x140002100", "comment": "Reconstructed NetworkSession VTable, enums, and typed parameters" }
  ]
}
```

---

## 5. Multi-Instance Pinning & Error Recovery

- If bridge returns: `"Multiple live IDA instances are available. Candidates: [31337, 31338]"`:
  1. Call `hsa_bridge(action='discover', target='ida')` to list all loaded binaries and ports.
  2. Pin exact `port` (e.g., `31337`) or `binary_path` matching your target.
  3. Always pass `"port": 31337` in every subsequent payload.
- Always check `"ok": true` before proceeding.
