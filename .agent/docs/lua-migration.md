---
library: lua
version: migration
latest: true
category: language
official_docs: https://www.lua.org/manual/5.4/manual.html
last_updated: 2026-03-28
---

# Lua Migration Guide

> Lua — Complete migration guide for all major version transitions.
> Source: lua.org manuals, HOPL papers, implementation research.
> Covers: 4.0→5.0, 5.1→5.2, 5.2→5.3, 5.3→5.4, 5.4→5.5

## Version Comparison

| Feature | 4.0→5.0 | 5.1→5.2 | 5.2→5.3 | 5.3→5.4 | 5.4→5.5 |
|:--------|:----------|:----------|:----------|:----------|:----------|
| State Creation | BREAKING | Stable | Stable | Stable | Stable |
| Environment API | BREAKING | BREAKING | Stable | Stable | Stable |
| Integer Types | Stable | Stable | BREAKING | Stable | Stable |
| Bitwise Ops | N/A | BREAKING | BREAKING | Stable | Stable |
| Userdata Values | Stable | Stable | Stable | BREAKING | Stable |
| GC Controls | BREAKING | Stable | Stable | BREAKING | Stable |
| Coroutines | N/A | BREAKING | Stable | Stable | Stable |

## Migration: Lua 4.0 → Lua 5.0

### State Creation

```c
// BEFORE (Lua 4.0)
lua_State *L = lua_open();
lua_dofile(L, "script.lua");

// AFTER (Lua 5.0+)
lua_State *L = luaL_newstate();
luaL_openlibs(L);
if (luaL_loadfile(L, "script.lua") == LUA_OK) {
    lua_pcall(L, 0, LUA_MULTRET, 0);
}
lua_close(L);
```

### Global Variable Access

```c
// BEFORE (Lua 4.0)
lua_pushnumber(L, 42);
lua_setglobal(L, LUA_GLOBALSINDEX, "x");
lua_getglobal(L, LUA_GLOBALSINDEX, "x");

// AFTER (Lua 5.0+)
lua_pushnumber(L, 42);
lua_setglobal(L, "x");
lua_getglobal(L, "x");

// Lua 5.2+: lua_getglobal is macro
// #define lua_getglobal(L,s) lua_getfield(L, LUA_GLOBALSINDEX, s)
```

### Error Handling

```c
// BEFORE (Lua 4.0)
// Errors returned as C return codes
int result = lua_dofile(L, "script.lua");
if (result != 0) {
    // Handle error
}

// AFTER (Lua 5.0+)
// Errors via lua_error() which does longjmp
// lua_pcall() catches errors
if (luaL_loadfile(L, "script.lua") != LUA_OK) {
    fprintf(stderr, "Syntax error: %s\n", lua_tostring(L, -1));
    lua_pop(L, 1);
} else if (lua_pcall(L, 0, 0, 0) != LUA_OK) {
    fprintf(stderr, "Runtime error: %s\n", lua_tostring(L, -1));
    lua_pop(L, 1);
}
```

## Migration: Lua 5.1 → Lua 5.2

### Environment API Removed (MAJOR)

The biggest breaking change. C functions no longer have environments.

```c
// BEFORE (Lua 5.1) — REMOVED in 5.2
lua_getfenv(L, func_index);    // Get C function's environment
lua_setfenv(L, func_index, env);  // Set C function's environment

// Use with globals:
lua_getregistry(L, LUA_GLOBALSINDEX);  // Get globals
lua_replace(L, LUA_ENVIRONINDEX);  // Set for next C call

// AFTER (Lua 5.2+)
// Use upvalues instead of environments
lua_pushinteger(L, 42);
lua_pushcclosure(L, my_func, 1);  // 1 upvalue
lua_setupvalue(L, func_idx, upvalue_idx);  // Update upvalue

// Environment in Lua code:
// _ENV is now a regular upvalue, not a pseudo-index
lua_getupvalue(L, func_idx, 1);  // Get _ENV
lua_setupvalue(L, func_idx, 1, new_env);  // Set _ENV
```

### Global Table Access

```c
// BEFORE (Lua 5.1) — LUA_GLOBALSINDEX still works but deprecated
lua_getglobal(L, "x");  // Macro: lua_getfield(L, LUA_GLOBALSINDEX, "x")

// AFTER (Lua 5.2+) — Explicit access preferred
lua_pushglobaltable(L);  // Push _G
lua_getfield(L, -1, "x");
lua_pop(L, 1);  // Pop global table
```

### Module System Changed

```c
// BEFORE (Lua 5.1) — module() function
module("mymodule")
function foo() end

// AFTER (Lua 5.2+) — Plain return table
local M = {}
function M.foo() end
return M
```

### package.loaders → package.searchers

```lua
-- BEFORE (Lua 5.1)
package.loaders  -- Array of loader functions

-- AFTER (Lua 5.2+)
package.searchers  -- Same concept, renamed
```

### luaL_register Deprecated

```c
// BEFORE (Lua 5.1)
luaL_register(L, "mymodule", mylib);  // Creates global "mymodule"

// AFTER (Lua 5.2+)
luaL_newlib(L, mylib);  // Creates table WITHOUT global
return 1;  // Caller does: local mymodule = require("mymodule")

// Or explicitly set global:
luaL_newlib(L, mylib);
lua_setglobal(L, "mymodule");
```

### lua_resume Signature Changed

```c
// BEFORE (Lua 5.1)
int lua_resume(lua_State *L, int nargs);

// AFTER (Lua 5.2+)
int lua_resume(lua_State *L, lua_State *from, int nargs);
// 'from' is the thread doing the resume, pass NULL if main
```

### Yield from C Functions

```c
// BEFORE (Lua 5.1)
static int my_yielding_func(lua_State *L) {
    lua_pushnumber(L, 42);
    return lua_yield(L, 1);  // Returns values, suspends
}

// AFTER (Lua 5.2+) — Continuation required
static int k_continuation(lua_State *L, int status, lua_KContext ctx) {
    // Called when resumed
    return 0;
}

static int my_yielding_func(lua_State *L) {
    lua_pushnumber(L, 42);
    return lua_yieldk(L, 1, ctx, k_continuation);
}
```

## Migration: Lua 5.2 → Lua 5.3

### Integer Types Introduced

```c
// BEFORE (Lua 5.2)
lua_Number n = lua_tonumber(L, -1);  // Always double
lua_pushnumber(L, 42);  // Push as double

// AFTER (Lua 5.3)
lua_Integer i = lua_tointeger(L, -1);  // Now int64_t
lua_pushinteger(L, 42);  // Push as integer

// Check conversion success
lua_Integer i;
int success;
i = lua_tointegerx(L, -1, &success);
if (!success) {
    // Handle conversion error
}
```

### Bitwise Operators

```lua
-- BEFORE (Lua 5.2) — Required bit32 library
local bit = require("bit32")
local result = bit.band(0xFF, 0x0F)

-- AFTER (Lua 5.3+) — Native operators
local result = 0xFF & 0x0F  -- bitwise AND
result = 0xFF | 0x0F       -- bitwise OR
result = ~0xFF               -- bitwise NOT
result = 1 << 8              -- left shift
result = 256 >> 2            -- right shift
```

### C API: lua_arith Extended

```c
// BEFORE (Lua 5.2) — Only arithmetic
lua_arith(L, LUA_OPADD);   // +
lua_arith(L, LUA_OPSUB);   // -
lua_arith(L, LUA_OPMUL);   // *
lua_arith(L, LUA_OPDIV);   // /
lua_arith(L, LUA_OPPOW);  // ^
lua_arith(L, LUA_OPMOD);   // %
lua_arith(L, LUA_OPUNM);  // unary -

// AFTER (Lua 5.3+) — Adds bitwise
lua_arith(L, LUA_OPBAND);  // &
lua_arith(L, LUA_OPBOR);   // |
lua_arith(L, LUA_OPBXOR);  // ~
lua_arith(L, LUA_OPSHL);  // <<
lua_arith(L, LUA_OPSHR);  // >>
lua_arith(L, LUA_OPBNOT);  // unary ~
```

### string.pack / string.unpack

```lua
-- New in Lua 5.3
local data = string.pack(">I4", 0x12345678)  -- Big-endian 32-bit uint
local value = string.unpack(">I4", data)     -- Unpack

-- Format codes: I=int, i=signed, f=float, d=double, s=string
local packed = string.pack("z", "hello")  -- Zero-terminated string
```

## Migration: Lua 5.3 → Lua 5.4

### Userdata Values Changed (BREAKING)

```c
// BEFORE (Lua 5.3)
void *ud = lua_newuserdata(L, sizeof(MyData));
lua_pushvalue(L, -1);  // Copy userdata
lua_setuservalue(L, -2);  // Set user value

// Get user value
lua_getuservalue(L, idx);

// AFTER (Lua 5.4+) — Multiple values, indexed
void *ud = lua_newuserdatauv(L, sizeof(MyData), 3);  // 3 values
lua_pushinteger(L, 42);
lua_setiuservalue(L, -2, 1);  // Set value 1
lua_pushstring(L, "meta");
lua_setiuservalue(L, -2, 2);  // Set value 2

// Get user value
lua_getiuservalue(L, idx, n);  // Get value n
```

### Garbage Collection Changed

```c
// BEFORE (Lua 5.3)
lua_gc(L, LUA_GCSETPAUSE, 200);   // Set pause %
lua_gc(L, LUA_GCSETSTEPMUL, 200); // Set step multiplier

// AFTER (Lua 5.4+) — LUA_GCSETPAUSE/SETSTEPMUL deprecated
// Use LUA_GCINC for incremental mode
lua_gc(L, LUA_GCINC, pause, step, 0);  // pause=200, step=200

// NEW: Generational GC mode
lua_gc(L, LUA_GCGEN, minor_pause, major_pause);  // e.g., 20, 100
```

### lua_rotate Added

```c
// NEW in Lua 5.4 (auxiliary library had similar before)
// Rotate stack elements
lua_rotate(L, idx, 3);  // Rotate top 3 elements
lua_rotate(L, -2, 1);    // Rotate 1 element at idx -2

// Use case: Move element to top efficiently
lua_rotate(L, idx, -1);  // Bring element at idx to top
```

## Migration: Lua 5.4 → Lua 5.5

### Minor Changes

```lua
-- __ipairs metamethod (NEW)
local mt = {
    __ipairs = function(t)
        return ipairs(custom_data)  -- Custom iteration
    end
}

-- To-be-closed variables
local file <close> = io.open("data.txt")
-- Automatically closed when going out of scope
```

### lua_version Changed

```c
// BEFORE (Lua 5.4)
const lua_Number *v = lua_version(L);  // Returns pointer
printf("Lua %s\n", *v);

// AFTER (Lua 5.5)
lua_Number v = lua_version(L);  // Returns value directly
printf("Lua %.1f\n", v);
```

### lua_toclose and lua_closeslot

```c
// NEW in Lua 5.4+
lua_toclose(L, idx);  // Mark slot for to-be-closed
lua_closeslot(L, idx);  // Explicitly close slot

// Use case: RAII-style resource management
void *resource = acquire_resource();
lua_pushlightuserdata(L, resource);
lua_toclose(L, -1);  // Will call __close when scope ends
```

## Common Patterns

### Loading a Script with Error Handling

```c
int load_script(lua_State *L, const char *filename) {
    int status = luaL_loadfile(L, filename);
    if (status != LUA_OK) {
        fprintf(stderr, "Load error: %s\n", lua_tostring(L, -1));
        lua_pop(L, 1);
        return status;
    }

    status = lua_pcall(L, 0, LUA_MULTRET, 0);
    if (status != LUA_OK) {
        fprintf(stderr, "Runtime error: %s\n", lua_tostring(L, -1));
        lua_pop(L, 1);
        return status;
    }
    return LUA_OK;
}
```

### Calling Lua Functions

```c
int call_lua_function(lua_State *L, const char *name, int nargs) {
    lua_getglobal(L, name);  // Push function

    // Push arguments
    for (int i = 0; i < nargs; i++) {
        lua_pushinteger(L, args[i]);
    }

    int status = lua_pcall(L, nargs, LUA_MULTRET, 0);
    if (status != LUA_OK) {
        fprintf(stderr, "Error: %s\n", lua_tostring(L, -1));
        lua_pop(L, 1);
        return -1;
    }

    // Get results
    int nresults = lua_gettop(L);
    // ... process results ...
    lua_pop(L, nresults);  // Clear stack
    return nresults;
}
```

### Module Registration (5.2+)

```c
// Recommended pattern for 5.2+
static int l_add(lua_State *L) {
    lua_Integer a = luaL_checkinteger(L, 1);
    lua_Integer b = luaL_checkinteger(L, 2);
    lua_pushinteger(L, a + b);
    return 1;
}

static const luaL_Reg lib[] = {
    {"add", l_add},
    {NULL, NULL}
};

// luaopen_* function for require()
int luaopen_mymodule(lua_State *L) {
    luaL_newlib(L, lib);  // Creates table, sets functions
    // Set module metadata
    lua_pushstring(L, "version");
    lua_pushstring(L, "1.0.0");
    lua_settable(L, -3);
    return 1;  // Table on stack
}

// Lua usage:
// local mymodule = require("mymodule")
// print(mymodule.add(2, 3))  -- 5
```

### Coroutine with Resume

```lua
-- Lua side
local co = coroutine.create(function()
    for i = 1, 5 do
        print("Yielding:", i)
        coroutine.yield(i)
    end
    return "done"
end)

for i = 1, 6 do
    local ok, val = coroutine.resume(co)
    if not ok then
        print("Error:", val)
        break
    end
    print("Received:", val)
end
```

## Gotchas

⚠️ **LuaJIT / 5.1 Constraints**: If you are maintaining code for LuaJIT, you CANNOT migrate to 5.2/5.3/5.4 features (like `_ENV`, native integers, or `<close>`). LuaJIT supports 5.1 syntax + `goto` + the `bit` library.

⚠️ **luaL_loadfile vs luaL_dofile**: `luaL_dofile` = `luaL_loadfile` + `lua_pcall`. Use `luaL_dofile` for simple cases.

⚠️ **lua_newstate vs lua_open**: `lua_open()` was removed in Lua 5.0. Always use `luaL_newstate()`.

⚠️ **lua_tostring invalidates stack during traversal**: Never call `lua_tostring` on a key during `lua_next` iteration.

⚠️ **Userdata memory is managed**: Don't `free()` userdata. Lua's GC handles it.

⚠️ **Coroutine in C vs Lua**: `coroutine.create()` (Lua) vs `lua_newthread()` (C) create different types.

⚠️ **Integer division**: In Lua 5.3+, `5 / 2` returns `2.5` (float). Use `5 // 2` for integer division.

⚠️ **Bitwise on floats**: Bitwise operators in Lua 5.3+ require integers. `~3.14` is invalid.

⚠️ **lua_close is not immediate**: Calls `__gc` finalizers. Order is reverse of creation.

## Links

- Migration Reference: https://www.lua.org/manual/5.4/manual.html#8
- Lua 5.2 Changes: https://www.lua.org/manual/5.2/manual.html#8.3
- Lua 5.3 Changes: https://www.lua.org/manual/5.3/manual.html#8.3
- Lua 5.4 Changes: https://www.lua.org/manual/5.4/manual.html#8.3
