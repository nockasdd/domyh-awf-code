---
name: plugin-x64dbg
description: "Live dynamic binary debugging, memory pattern scanning, hardware breakpoints, register tracing, and runtime hooking with x64dbg/x32dbg."
category: tooling
tier: 1
---

# x64dbg Dynamic Binary Debugging & Tracing Workflow

## 1. When To Use

- Live debugging of running Windows processes (`.exe`) and dynamic link libraries (`.dll`).
- Memory pattern scanning with wildcards (`48 8B ?? 10 ?? ??`) within specific module address spaces.
- Inspecting CPU registers (`RAX`, `RCX`, `RIP`, `RFLAGS`) and stack frame values at runtime.
- Setting hardware/software breakpoints and tracing anti-tamper / packer unpack routines.

---

## 2. x64dbg Bridge Architecture & Discovery

The x64dbg plugin runs inside the debugger process, communicating over a local IPC / HTTP bridge:

```
[Agent] ➔ [HSA x64dbg Bridge] ➔ IPC/Pipe ➔ [x64dbg Plugin Runtime]
```

### Discovery & Module Pinning
```json
hsa_bridge({ "action": "discover", "target": "x64dbg" })
```
Always verify:
*   `process_id` (PID of the attached application)
*   `module_name` (e.g. `GameCore.dll`, `Engine.dll`)
*   `is_paused` (whether the debugee is currently stopped at a breakpoint)

---

## 3. Core Dynamic Debugging Protocols

### A. Module-Scoped Memory Pattern Search
```json
{
  "command": "x64dbg_find_pattern",
  "params": {
    "module_name": "GameCore.dll",
    "pattern": "48 89 5C 24 ?? 57 48 83 EC 20 48 8B D9",
    "max_results": 10
  }
}
```

### B. Setting Hardware Breakpoints & Context Capture
```json
{
  "command": "x64dbg_set_breakpoint",
  "params": {
    "address": "GameCore.dll+0x42A10",
    "type": "hardware_execute",
    "one_shot": true
  }
}
```

### C. Register & Stack Memory Inspection
```json
{
  "command": "x64dbg_get_context",
  "params": {
    "registers": ["rax", "rcx", "rdx", "rip", "rsp"],
    "read_stack_words": 16
  }
}
```

---

## 4. Safety Guardrails & Anti-Deadlock

1. **Auto-Resume Guard**: Never leave a process suspended indefinitely without a timeout or explicit user command.
2. **Module Scope Requirement**: Always specify `module_name` when scanning signatures to avoid scanning kernel / read-protected memory pages.
3. **Thread Safety**: Run debugger commands synchronously on the debugger engine thread to avoid race conditions.
