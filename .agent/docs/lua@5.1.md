---
library: lua
version: 5.1
latest: false
category: language
official_docs: https://www.lua.org/manual/5.1/manual.html
last_updated: 2026-03-28
---

# Lua 5.1 (and 5.1.4)

> Lua 5.1 — The most widely deployed embedded version and **the strict baseline for LuaJIT**.
> ⚠️ This is NOT the latest Lua version. For Lua 5.4/5.5, see `lua.md`.
> Docs: https://www.lua.org/manual/5.1/manual.html

## Overview

Lua 5.1 (released 2006, finalized as 5.1.4 in 2008) is arguably the most important legacy version of Lua. It acts as the canonical baseline for **LuaJIT**, which powers many modern game engines, proxies (Envoy/Nginx), and frameworks (Roblox/Neovim).

**Key Defining Features:**
- Introduction of the `module()` and `require` package system.
- Introduction of `setfenv` and `getfenv` (function environments).
- Incremental Garbage Collector.
- Coroutines supporting `yield` across C boundaries (partially).
- Length operator `#`.
- `%` operator for modulo.

## Version Specifics: `5.1` vs `5.1.4`

- **5.1:** The base specification.
- **5.1.4:** The final stable bug-fix release before 5.2. It resolved minor bugs in the VM and parser (e.g., handling of `...` in nested functions, GC edge cases). When developers refer to "Lua 5.1", they almost exclusively mean the `5.1.4` implementation state.

---

## 🛠 C API: State & Modules

### State Creation
```c
#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>

int main() {
    lua_State *L = luaL_newstate();  // Also lua_open() was retained for compat
    luaL_openlibs(L);                // Load all standard libraries

    if (luaL_dofile(L, "script.lua") != 0) {
        fprintf(stderr, "Error: %s\n", lua_tostring(L, -1));
        lua_pop(L, 1);
    }
    
    lua_close(L);
    return 0;
}
```

### Module Registration (The 5.1 Way)
In 5.1, `luaL_register` was the standard (it creates global variables, unlike 5.2+).
```c
static const luaL_Reg mylib[] = {
    {"add", l_add},
    {NULL, NULL}
};

int luaopen_mylib(lua_State *L) {
    // luaL_register automatically creates a global table named "mylib"
    luaL_register(L, "mylib", mylib);
    return 1;
}
```

---

## 📜 Lua Script: 5.1 Defining Features

### The `module()` Function
Lua 5.1 introduced `module()` to declare modules. This sets the function environment (`setfenv`) automatically.
```lua
-- mymath.lua
module("mymath", package.seeall) -- 'package.seeall' exposes _G to the module

function add(a, b) -- Automatically placed inside 'mymath' table
    return a + b
end

-- Usage elsewhere:
require("mymath")
print(mymath.add(2, 3))
```
> ⚠️ **Note:** `module()` and `package.seeall` were **deprecated in 5.2** due to environment pollution. Do not use this pattern in modern Lua (5.2+).

### Function Environments (`setfenv` / `getfenv`)
Lua 5.1 allows dynamic scoping of global environments per function. This is heavily used for sandboxing.

```lua
local env = { print = print } -- Clean sandbox

local func = loadstring("print('Sandboxed!')")
setfenv(func, env) -- Bind the environment
func()

-- Getting the environment
local curr_env = getfenv(1) -- 1 = current function, 2 = caller
```

### Regular Expressions / Patterns
Lua 5.1 finalized its unique pattern matching engine.
```lua
local str = "hello_123"
local word, num = string.match(str, "(%a+)_(%d+)")
print(word) -- "hello"
```

---

## ⚠️ LuaJIT Considerations

If you are reading this document because you are writing code for **LuaJIT**, remember:
1. **LuaJIT is permanently locked to Lua 5.1 semantics** (with a few 5.2 extensions ported over conditionally).
2. `goto` statements (a 5.2 feature) ARE supported in standard LuaJIT builds.
3. Bitwise operations are provided via the `bit` library (`require("bit")`), **not** native `&`/`|` operators.
4. Integer types do not exist (everything is a 64-bit float, though the JIT uses 32-bit integers internally for optimization).

## ⛔ Migration Traps (5.1 → 5.2+)
- `setfenv`/`getfenv` are **completely removed** in 5.2. They are replaced by the `_ENV` upvalue.
- `module()` is removed. Return tables explicitly instead.
- `unpack` was moved to `table.unpack`.
- `loadstring` was merged into `load`.
- String formatting `%q` changed behavior slightly.
