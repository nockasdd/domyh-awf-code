---
name: plugin-ghidra
description: "Ghidra headless batch analysis, PDB symbol parsing, cross-platform binary decompilation, and DataTypeManager automation."
category: tooling
tier: 1
---

# Ghidra Headless & Binary Analysis Workflow

## 1. When To Use

- Automated headless binary analysis across large directories of DLLs/EXEs/ELFs.
- Parsing and mapping public PDB symbol files into structured data types.
- Multi-architecture decompilation (x86, x64, ARM64, MIPS, RISC-V).
- Programmatic AST querying via Ghidra `DecompInterface` and `HighFunction`.

---

## 2. Ghidra Bridge Architecture & Discovery

Ghidra operates either in GUI mode with the Ghidra Bridge extension or in Headless mode via PyGhidra/GhidraScript.

```
[Agent] ➔ [HSA Ghidra Bridge (server.py)] ➔ HTTP/Socket ➔ [Ghidra Runtime / GhidraScript]
```

### Discovery & Instance Pinning
```json
hsa_bridge({ "action": "discover", "target": "ghidra" })
```
Extract `port` (default `28473`), `project_name`, or `program_path` to pin targeted execution.

---

## 3. Core Execution Capabilities

### A. Batch Function Listing & Symbol Export
```json
{
  "command": "ghidra_list_symbols",
  "params": {
    "filter": "Crypto",
    "symbol_type": "Function",
    "limit": 50
  }
}
```

### B. HighFunction Decompilation
```json
{
  "command": "ghidra_decompile",
  "params": {
    "address": "0x140001000",
    "timeout_sec": 30
  }
}
```

### C. DataTypeManager Ingestion (C Header Parsing)
Ghidra's `DataTypeManager` parses complete C header definitions (`.h`) to assign composite structs to memory ranges:
```json
{
  "command": "ghidra_import_datatypes",
  "params": {
    "c_headers": "typedef unsigned int DWORD;\ntypedef struct { DWORD magic; DWORD size; void* data; } MsgPacket;"
  }
}
```

---

## 4. Best Practices & Safety

1. **Memory Bounds**: Cap headless analysis batches to 50 functions per pass to avoid JVM Heap exhaustion.
2. **PDB Synchronization**: Verify PDB GUID matches executable timestamp before committing types.
3. **Transaction Safety**: Wrap mutation scripts inside `currentProgram.startTransaction("awf_patch")` and commit only on success.
