---
library: lua
version: internals
latest: true
category: architecture
official_docs: https://www.lua.org/source/5.4/
last_updated: 2026-03-28
---

# Lua Internals: The `lua_load` Pipeline

> Deep dive into Lua's C-level architecture for loading and executing scripts.
> This document overrides general usage guides to focus on **Engine Hacking** and **VM Internals**.

## 1. The Public Boundary: `lua_load`

All script execution in Lua (whether invoked via `dofile`, `loadstring`, or `require`) eventually bottlenecks into the central C API function: `lua_load`.

```c
LUA_API int lua_load(lua_State *L, lua_Reader reader, void *data,
                     const char *chunkname, const char *mode);
```

**Crucial Characteristic:** `lua_load` is completely blind to whether the incoming data is readable source code (`.lua`) or compiled binary bytecode (`.luac`). It relies entirely on a provided `reader` function to pull a stream of bytes.

---

## 2. The Heuristic Fork: `luaD_protectedparser`

When `lua_load` begins, it wraps execution in a protected call to prevent parsing errors from crashing the host application. This handler is `luaD_protectedparser`.

Its first action is a **Heuristic Check** (sniffing the first bytes of the stream):
1. It requests the first block of data via the `ZIO` (Zipped I/O) structure.
2. It checks for the presence of the **`LUA_SIGNATURE`**.
   - `LUA_SIGNATURE` is globally defined as the literal string `\x1BLua` (Escape character + 'L' + 'u' + 'a').
3. Based on the signature and the `mode` parameter (e.g., `"b"` for binary, `"t"` for text, `"bt"` for both), execution forks into one of two entirely disparate C systems.

---

## 3A. The Bytecode Pathway: `luaU_undump` (`lundump.c`)

If the stream starts with `\x1BLua`, the VM deduces it is precompiled bytecode. Execution immediately jumps to `luaU_undump` (affectionately known as the "Undumper").

### Step 1: `checkHeader` (Strict Validation)
Bytecode in Lua is **aggressively platform and version dependent**. `luaU_undump` first inspects the binary header to ensure absolute compatibility:
- **Version Byte:** Must match the exact `LUAC_VERSION` of the compiling interpreter.
- **Format / Endianness:** Checks if the machine is Big-Endian or Little-Endian.
- **Type Sizes:** Verifies the `sizeof(int)`, `sizeof(size_t)`, `sizeof(Instruction)`, `sizeof(lua_Integer)`, and `sizeof(lua_Number)`. If the bytecode was compiled on a 64-bit integer system but loaded on a 32-bit one, it instantly aborts.

### Step 2: `loadFunction` (Deserialization)
The Undumper constructs the raw `Proto` (Prototype) object directly into memory:
- **`loadCode`:** Directly memcpy's the array of `Instruction`s (the VM's 32-bit opcodes).
- **`loadConstants`:** Rebuilds the constant table (`k`), parsing out strings, numbers, and sub-functions.
- **`loadUpvalues`:** Maps environmental enclosures.
- **`loadDebug`:** (Optional) Loads local variable names and line mappings if the bytecode wasn't stripped.

### Step 3: Closure Packaging
The finalized `Proto` tree is wrapped in an `LClosure` (Lua Closure object) and pushed onto the very top of the Lua Stack (`L->top`).

---

## 3B. The Source Code Pathway: `luaY_parser` (`lparser.c`)

If the signature is missing, Lua assumes the data is raw text. The process maps over to the Lexer (`llex.c`) and Parser (`lparser.c`).

### Single-Pass Compiling
Unlike traditional compilers (e.g., GCC or Clang) that build massive Abstract Syntax Trees (ASTs) before generating code, Lua is a **Single-Pass Compiler**. 

1. **Lexical Analysis (`luaX_next`):** The lexer reads characters and emits contiguous Tokens.
2. **Recursive Descent Parsing:** The parser reads tokens from top to bottom.
3. **Immediate Code Generation (`lcode.c`):** The exact moment a grammatical rule completes (e.g., recognizing `local a = 1`), the parser directly commands the code generator `luaK_code` to emit the correlating VM `Instruction` (e.g., `OP_LOADK`).
   - There is no intermediate AST representation saved in memory.
   - The emitted instructions are packed directly into a newly created `Proto` struct.

### Step 3: Closure Packaging
Identical to the bytecode path, the result is an `LClosure` pushed to the top of the stack.

---

## 4. Execution Edge: The VM Loop (`lvm.c`)

At the conclusion of `lua_load`, the script is **not running**. It is merely sitting on the stack as an anonymous function.

To execute it, the C host calls `lua_pcall()`.
This hands control over to `luaV_execute` (The Virtual Machine), which:
1. Pops the `LClosure` off the stack.
2. Enters an infinite `for(;;)` loop.
3. Rapidly Fetches, Decodes, and Executes the 32-bit opcodes (e.g., `OP_MOVE`, `OP_ADD`, `OP_CALL`) generated during steps 3A or 3B.

---

## 🏛 Historical Evolution: 4.0 vs 5.x

The internals of loading code changed radically during Lua's history, mapping directly to how its VM evolved.

### Lua 4.0: The Stack VM Era
- **VM Type:** Stack-based Virtual Machine (Instructions pushed and popped values directly to/from a local stack).
- **Loading API:** `lua_loadbuffer` and `lua_dobuffer` were the standards. The multi-purpose reader-based `lua_load` did not exist in its modern form.
- **Bytecode Flow:** Un-dumping 4.0 bytecode loaded Stack-VM opcodes. It is fundamentally impossible to load Lua 4.0 bytecode into any modern Lua interpreter.

### Lua 5.0+: The Register VM Era
- **VM Type:** Register-based Virtual Machine (Instructions operate on specific "registers", i.e., indices in the stack frame window, drastically reducing CPU shuffle instructions).
- **Loading API:** Introduction of the modern `lua_load` taking a `lua_Reader`.
- **Bytecode Flow:** `luaU_undump` was entirely refactored to parse Register-VM opcodes. This architecture set the permanent standard still used in Lua 5.4 and LuaJIT today.
