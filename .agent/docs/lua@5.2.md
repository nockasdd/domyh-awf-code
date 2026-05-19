---
library: lua
version: 5.2
latest: false
category: language
official_docs: https://www.lua.org/manual/5.2/manual.html
last_updated: 2026-03-28
---

# Lua 5.2

> Lua 5.2 — Restructuring Environments and Coroutine Yielding.
> ⚠️ This is NOT the latest Lua version. For Lua 5.4/5.5, see `lua.md`.
> Docs: https://www.lua.org/manual/5.2/manual.html

## Overview

Lua 5.2 (released in 2011) was a controversial but necessary transition architecture. It stripped away `setfenv` and `module()`, replacing them with a more robust lexical scoping mechanism for global variables (`_ENV`). 

**Key Defining Features:**
- `_ENV` (Lexical Environments) replacing `setfenv/getfenv`.
- Yieldable C functions (`lua_yieldk`, `lua_callk`, `lua_pcallk`).
- Standard `goto` statement.
- The `bit32` standard library.
- Ephemeron tables (weak tables where the value only lives if the key lives).
- Yieldable `pcall` and `metamethods`.

---

## 🛠 C API: The `*k` Continuations

Prior to 5.2, if a C function called into Lua and that Lua code yielded, the C stack could not easily resume. Lua 5.2 solved this via **Continuations**.

```c
#include <lua.h>

static int k_continuation(lua_State *L, int status, lua_KContext ctx) {
    // This is called when the coroutine resumes
    printf("Resumed!\n");
    return 1; 
}

static int my_yielding_c_func(lua_State *L) {
    lua_pushinteger(L, 42);
    // Yield the state, and specify what happens when it's resumed
    return lua_yieldk(L, 1, 0, k_continuation);
}
```

### Module Registration (The 5.2 Way)
`luaL_register` was deprecated. Libraries are now created cleanly on the stack without polluting globals.
```c
static const luaL_Reg mylib[] = {
    {"add", l_add},
    {NULL, NULL}
};

int luaopen_mylib(lua_State *L) {
    // Creates a new table and registers functions into it
    luaL_newlib(L, mylib);
    return 1; // Return the table on the stack
}
```

---

## 📜 Lua Script: Environments & Lexical Scoping

### The `_ENV` Transition
In Lua 5.2, all "global" variables are strictly syntactic sugar for `_ENV.variable`. This removed the need for magical function environments.

```lua
-- All free variables resolve to _ENV:
a = 1 
-- is exactly evaluated as:
_ENV.a = 1

-- Sandboxing in 5.2
local my_sandbox = { print = print }

-- We redefine _ENV for the local block
local function run_trusted()
    local _ENV = my_sandbox
    print("This runs.")
    -- os.execute() -- Error: os is nil in my_sandbox
end
```

### Loading Sandboxed Code
Since `setfenv` is gone, the `load` function now accepts a 4th argument for the environment table.
```lua
local env = { print = print, a = 10 }
local chunk = load("print(a * 2)", "sandbox", "t", env)
chunk() -- Outputs 20
```

### Native `goto`
Lua introduces the `goto` statement, restricted to block scoping (cannot jump into blocks).

```lua
for i = 1, 10 do
    if i == 5 then goto continue end
    print(i)
    
    ::continue::
end
```

---

## ⛔ Migration Traps (5.2 → 5.3+)
- The `bit32` library introduced in 5.2 is **deprecated and removed** in 5.3, replaced by native `&` `|` operators.
- `_ENV` behavior is stable moving forward.
- Lua 5.2 still uses double-precision floats for everything. True Integers do not exist until Lua 5.3.
- `math.log10` was deprecated, favoring `math.log(x, 10)`.
