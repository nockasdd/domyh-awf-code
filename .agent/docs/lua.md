---
library: lua
version: 5.4
latest: true
category: language
official_docs: https://www.lua.org/docs.html
last_updated: 2026-03-28
---

# Lua (Modern)

> Lua — The leading lightweight, embeddable scripting language.
> **Current Default Stable:** Lua 5.4
> **Upcoming:** Lua 5.5 (Conceptual/Beta)
> Docs: https://www.lua.org/manual/

This is the primary document for modern Lua development (5.4+). If you are working on a legacy project or a specific Game Engine (like Roblox, WoW, or Neovim) using LuaJIT, you must refer to the **[Lua 5.1 Specification](lua@5.1.md)** instead.

## 🧭 Historical Version Navigation

Due to Lua's unique embedded nature, different projects use vastly different versions. Use the specific guide for your target:
- **[Lua 4.0](lua@4.md)** — Legacy (2000). Pre-state-machine refactoring.
- **[Lua 5.1 & LuaJIT](lua@5.1.md)** — The golden standard for high-performance JIT execution and Game Engines.
- **[Lua 5.2](lua@5.2.md)** — The environment restructuring (`_ENV`).
- **[Lua 5.3](lua@5.3.md)** — The Integer and Bitwise update.
- **[Lua 5.4](lua@5.4.md)** — The Modern standard (To-be-closed RAII, Generational GC).
- **[Lua Migration Guide](lua-migration.md)** — Cheat sheet for C API and Script syntax changes across forms.
- **[Lua Internals](lua-internals.md)** — Deep dive into the `lua_load` pipeline, Bytecode parsing, C API compilation flows, and VM architecture.

---

## ⚡ Modern Lua (5.4+) Quick Reference

### Core Architecture & State
```c
#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>

int main() {
    lua_State *L = luaL_newstate();
    luaL_openlibs(L); // Standard libs: base, coroutine, table, io, os, string, math, utf8, debug
    
    // Set Generational Collector (Default in 5.4)
    lua_gc(L, LUA_GCGEN, 0, 0);

    // Protected Call Execution
    if (luaL_dofile(L, "init.lua") != LUA_OK) {
        fprintf(stderr, "Initialization Failed: %s\n", lua_tostring(L, -1));
        lua_pop(L, 1);
    }
    
    lua_close(L);
    return 0;
}
```

### Scripting Primitives

```lua
-- Modern Block Scoping & Immutability
local MAX_RETRIES <const> = 5

-- Native 64-bit Integers (since 5.3)
local flag = 0xFF00
local result = flag | 0x00FF -- Bitwise OR

-- UTF-8 Support
local length = utf8.len("안녕하세요")

-- RAII / Deterministic Resource Destruction (since 5.4)
-- The __close metamethod is guaranteed to fire when leaving scope.
local function read_safe()
    local file <close> = io.open("data.bin", "rb")
    if not file then return nil end
    return file:read("a")
    -- 'file' is safely closed here automatically
end
```

### Table Iteration & `__ipairs`

Lua 5.5 (upcoming drafts) aims to solidify the `__ipairs` metamethod, which allows custom structures to behave identically to native array iteration. Be aware that relying on `#` (length operator) on arrays with `nil` holes is undefined behavior.

```lua
-- Safe iteration over arrays
for index, value in ipairs(my_table) do
    print(index, value)
end

-- Safe iteration over hashes
for key, value in pairs(my_table) do
    if type(value) == "function" then
        print(key .. " is a method.")
    end
end
```

### C API: Multiple User values
Modern Lua replaced singular `uservalue` with an explicit slot-based allocation (`lua_newuserdatauv`).
```c
MyObject *obj = (MyObject*)lua_newuserdatauv(L, sizeof(MyObject), 2); // 2 Slots
lua_pushstring(L, "Identifier");
lua_setiuservalue(L, -2, 1); // Set directly into slot 1
```

## 🛠 Integrating C API with Modern Lua

The standard for exposing C implementations into Lua 5.4 is:
1. Fetch arguments using `luaL_check*` functions.
2. Return values onto the stack.
3. Handle errors securely through `luaL_error` (which performs a `longjmp` internally, avoiding segmentation faults).

```c
static int l_calculate_delta(lua_State *L) {
    // 1. Argument Validation
    lua_Integer basis = luaL_checkinteger(L, 1);
    lua_Number deviation = luaL_checknumber(L, 2);
    
    // 2. Logic
    if (deviation <= 0.0) {
        return luaL_error(L, "Deviation must be strictly positive!");
    }
    
    lua_Number result = basis * deviation;
    
    // 3. Return
    lua_pushnumber(L, result);
    return 1; // Number of elements left on stack
}
```

## Future Outlook: Lua 5.5
As of early 2026, Lua 5.5 remains under conceptual testing. The primary focus involves improving memory safety inside the C API stack operations, finalizing iteration protocol ambiguities (`__ipairs`), and potential further garbage collection fine-tuning for embedded environments.

For now, target **5.4** as the absolute maximum stable for new projects unless targeting LuaJIT.
