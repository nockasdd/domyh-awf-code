---
library: lua
version: 4.0
latest: false
category: language
official_docs: https://www.lua.org/ftp/ref-4.0.pdf
last_updated: 2026-03-28
---

# Lua 4.0

> Lua 4.0 — Legacy scripting language (released 2000).
> ⚠️ This is LEGACY. For modern development, use `lua.md` (Lua 5.x).
> Docs: https://www.lua.org/ftp/ref-4.0.pdf

## Version Comparison

| Feature | 4.0 | 5.0+ |
|:--------|:-----|:------|
| C API State | `lua_open()` | `luaL_newstate()` |
| Globals Access | `LUA_GLOBALSINDEX` | `lua_getglobal()` |
| Error Handling | Return codes | `lua_pcall()` + `lua_error()` |
| Coroutines | ❌ | `coroutine.create()` |
| Loading | `lua_dofile()` | `luaL_loadfile()` + `lua_pcall()` |
| Stack Model | Implicit stack | Explicit `lua_State *` |
| Strings | Max 1MB | Configurable |
| Tables | Single hash+array | Same (improved) |

## C API: State Creation

```c
#include <lua.h>

int main() {
    // Lua 4.0: lua_open()
    lua_State *L = lua_open();

    // Load standard libraries
    luaopen_base(L);
    luaopen_math(L);
    luaopen_io(L);
    luaopen_string(L);
    luaopen_table(L);

    // Run a script (direct execution)
    if (lua_dofile(L, "script.lua") != 0) {
        fprintf(stderr, "Error: %s\n", lua_getstring(L, -1));
        lua_pop(L, 1);
    }

    lua_close(L);
    return 0;
}
```

### Compile & Link

```bash
gcc -o myprogram myprogram.c -llua -lm
```

## C API: Loading Scripts

### lua_dofile (Direct Execution)

```c
// Lua 4.0: lua_dofile handles compile + execute
int result = lua_dofile(L, "script.lua");
if (result != 0) {
    // Error: message is on stack
    const char *msg = lua_getstring(L, -1);
    fprintf(stderr, "Error: %s\n", msg);
    lua_pop(L, 1);  // Pop error message
}
```

### lua_dostring (From String)

```c
int result = lua_dostring(L, "print('Hello from Lua 4.0!')");
if (result != 0) {
    const char *msg = lua_getstring(L, -1);
    fprintf(stderr, "Error: %s\n", msg);
    lua_pop(L, 1);
}
```

### lua_dobuffer (From Buffer)

```c
const char *script = "return 42";
int result = lua_dobuffer(L, script, strlen(script), "string_chunk");
if (result == 0) {
    int value = lua_getnumber(L, -1);
    printf("Result: %d\n", value);
    lua_pop(L, 1);
}
```

## C API: Global Variables

### Setting Globals

```c
// Set number
lua_pushnumber(L, 42);
lua_setglobal(L, "x");  // x = 42

// Set string
lua_pushstring(L, "hello");
lua_setglobal(L, "name");  // name = "hello"

// Set table
lua_newtable(L);  // Create empty table on stack
lua_pushnumber(L, 1);
lua_pushstring(L, "first");
lua_settable(L, -3);  // t[1] = "first"
lua_setglobal(L, "arr");  // arr = {1: "first"}
```

### Getting Globals

```c
// Get global
lua_getglobal(L, "x");
if (lua_isnumber(L, -1)) {
    double val = lua_getnumber(L, -1);
    printf("x = %f\n", val);
}
lua_pop(L, 1);  // Pop the value

// Get table and its fields
lua_getglobal(L, "arr");
lua_pushnumber(L, 1);  // key
lua_gettable(L, -2);   // get arr[1]
const char *first = lua_getstring(L, -1);
lua_pop(L, 2);  // Pop table and value
```

## C API: Stack Operations

### Basic Push/Pop

```c
// Push values
lua_pushnil(L);
lua_pushnumber(L, 3.14);
lua_pushstring(L, "hello");
lua_pushcfunction(L, my_c_function);
lua_pushuserdata(L, my_pointer);

// Check and get values
if (lua_isnumber(L, -1)) {
    double n = lua_getnumber(L, -1);
}
if (lua_isstring(L, -1)) {
    const char *s = lua_getstring(L, -1);
}
if (lua_istable(L, -1)) {
    // Handle table
}

// Pop
lua_pop(L, n);  // Remove n elements
```

### Stack Size

```c
// Get stack top index
int top = lua_gettop(L);  // Returns number of elements

// Set stack top (truncate or extend with nil)
lua_settop(L, 5);  // Stack has at least 5 elements
lua_settop(L, -1); // No-op
lua_settop(L, -2); // Remove top element (equivalent to lua_pop(L,1))
```

## C API: Tables

### Creating Tables

```c
// Create table: lua_createtable(narray, nhash)
// narray = pre-allocate array slots, nhash = pre-allocate hash slots
lua_createtable(L, 10, 0);  // Pre-allocate 10 array slots

// Create and assign
lua_newtable(L);  // Shortcut, equivalent to lua_createtable(L, 0, 0)
```

### Setting Table Fields

```c
// t[key] = value (where t is at index -2, key and value on top)
lua_pushstring(L, "name");     // Push key
lua_pushstring(L, "Alice");   // Push value
lua_settable(L, -3);          // t["name"] = "Alice"

// t[n] = value (numeric indexing)
lua_pushnumber(L, 1);         // Push key
lua_pushstring(L, "first");   // Push value
lua_settable(L, -3);          // t[1] = "first"

// Raw set (no metamethods)
lua_pushnumber(L, 2);
lua_pushstring(L, "second");
lua_rawset(L, -3);            // t[2] = "second" (raw, no __newindex)
```

### Getting Table Fields

```c
// Get t[key]
lua_pushstring(L, "name");   // Push key
lua_gettable(L, -2);          // Get t["name"], push value
const char *name = lua_getstring(L, -1);
lua_pop(L, 1);                // Pop value

// Get t[n] (numeric indexing)
lua_pushnumber(L, 1);         // Push key
lua_gettable(L, -2);          // Get t[1]

// Raw get (no metamethods)
lua_pushnumber(L, 2);
lua_rawget(L, -2);            // Get t[2] (raw, no __index)

// Check existence
lua_pushstring(L, "key");
if (lua_gettable(L, -2) != LUA_TNIL) {
    // Key exists
    lua_pop(L, 1);
} else {
    lua_pop(L, 2);  // Pop nil and key
}
```

## C API: C Functions

### Basic C Function

```c
// C function signature: int func(lua_State *)
static int l_add(lua_State *L) {
    int n = lua_gettop(L);  // Number of arguments
    double sum = 0;

    for (int i = 1; i <= n; i++) {
        sum += lua_getnumber(L, i);
    }

    lua_pushnumber(L, sum);  // Return value
    return 1;  // Number of return values
}

// Register function
lua_pushcfunction(L, l_add);
lua_setglobal(L, "add");

// Now in Lua: add(1, 2, 3) returns 6
```

### C Function with Multiple Returns

```c
static int l_divmod(lua_State *L) {
    double a = lua_getnumber(L, 1);
    double b = lua_getnumber(L, 2);

    if (b == 0) {
        lua_pushstring(L, "division by zero");
        lua_error(L);  // Raise error
        return 0;      // Never reached
    }

    lua_pushnumber(L, a / b);   // Quotient
    lua_pushnumber(L, a - b * (a / b));  // Remainder
    return 2;  // Two return values
}
```

### Error Handling

```c
// lua_error raises a Lua error (longjmp)
static int safe_div(lua_State *L) {
    double b = lua_getnumber(L, 2);
    if (b == 0) {
        lua_pushstring(L, "cannot divide by zero");
        lua_error(L);  // Throws error
    }
    double a = lua_getnumber(L, 1);
    lua_pushnumber(L, a / b);
    return 1;
}

// Check arguments
static int l_add(lua_State *L) {
    if (!lua_isnumber(L, 1) || !lua_isnumber(L, 2)) {
        lua_pushstring(L, "add: expected two numbers");
        lua_error(L);
    }
    // ... rest of function
}
```

## C API: Memory Functions

### Custom Allocator

```c
// lua_open accepts optional allocator
void *my_alloc(void *ud, void *ptr, size_t osize, size_t nsize) {
    if (nsize == 0) {
        free(ptr);
        return NULL;
    }
    return realloc(ptr, nsize);
}

int main() {
    lua_State *L = lua_open(my_alloc, NULL);
    // ... use L ...
    lua_close(L);
}
```

## C API: Garbage Collection

```c
// Control garbage collection
lua_gc(L, LUA_GCSTOP);    // Stop GC
lua_gc(L, LUA_GCRESTART);  // Restart GC
lua_gc(L, LUA_GCCOLLECT);  // Force full collection

// Set GC parameters
lua_gc(L, LUA_GCSETPAUSE, 100);   // GC pause (percentage)
lua_gc(L, LUA_GCSETSTEPMUL, 100); // GC step multiplier

// Step GC
lua_gc(L, LUA_GCSTEP, 0);  // One step
```

## Lua Script: Basics

```lua
-- Variables
x = 42  -- Global by default
local y = 10  -- Local variable

-- Tables (only data structure)
t = {name = "Lua", version = 4.0}
arr = {1, 2, 3, 4, 5}

-- Table access (1-based indexing!)
print(arr[1])  -- 1
print(t.name)  -- "Lua"

-- Functions
function add(a, b)
    return a + b
end

-- Closures
function counter(start)
    local count = start or 0
    return function()
        count = count + 1
        return count
    end
end

next_id = counter(0)
print(next_id())  -- 1
print(next_id())  -- 2

-- Control flow
if x > 0 then
    print("positive")
elseif x < 0 then
    print("negative")
else
    print("zero")
end

-- For loop
for i = 1, 10 do
    print(i)
end

-- While loop
while condition do
    -- code
end

-- Repeat loop
repeat
    -- code
until condition
```

## Gotchas & Breaking Changes

⚠️ **Lua 4.0 → 5.0 is a MAJOR breaking change**. The entire C API was redesigned.

⚠️ **lua_open() removed in 5.0**: Always use `luaL_newstate()` in 5.0+.

⚠️ **lua_dofile() removed in 5.0**: Use `luaL_loadfile()` + `lua_pcall()`.

⚠️ **lua_getstring(L, -1)**: In 4.0 this pops. In 5.0+, use `lua_tostring(L, -1)` (doesn't pop).

⚠️ **lua_getnumber() is different**: 4.0 `lua_getnumber()` returns double. 5.0+ has `lua_tonumber()`.

⚠️ **lua_createtable() signature**: `lua_createtable(L, narr, nrec)` in 4.0 vs 5.0+.

⚠️ **Error handling**: 4.0 uses return codes + `lua_error()`. 5.0+ uses `lua_pcall()` for protected calls.

⚠️ **No coroutines**: Lua 4.0 has no coroutine support. Upgrade to 5.0+.

⚠️ **No standard library loader**: Manually call `luaopen_base()`, etc. in 4.0.

⚠️ **Global variables**: In 4.0, globals are accessed via `LUA_GLOBALSINDEX`. In 5.0+, use `lua_getglobal()`.

## Migration Checklist (4.0 → 5.x)

- [ ] Replace `lua_open()` → `luaL_newstate()`
- [ ] Replace `lua_dofile()` → `luaL_loadfile()` + `lua_pcall()`
- [ ] Replace `lua_dostring()` → `luaL_loadstring()` + `lua_pcall()`
- [ ] Replace `lua_getstring(L, -1)` → `lua_tostring(L, -1)`
- [ ] Replace `lua_getnumber(L, i)` → `lua_tonumber(L, i)`
- [ ] Replace `lua_pushcfunction()` → `lua_pushcfunction()` (same signature, new registry)
- [ ] Replace `lua_createtable()` → `lua_createtable()` (same signature)
- [ ] Replace `luaopen_base(L)` etc. → `luaL_openlibs(L)`
- [ ] Replace `lua_error()` error handling → `lua_pcall()` protected calls
- [ ] Replace `lua_gettable()` with key on stack → `lua_getfield(L, idx, key)`
- [ ] Test all C extensions with new Lua version
- [ ] Check `lua_gc()` constants (LUA_GC* still exist but values may differ)

## Links

- Lua 4.0 Reference: https://www.lua.org/ftp/ref-4.0.pdf
- Lua 5.0 Manual: https://www.lua.org/manual/5.0/
- Migration Guide: https://www.lua.org/manual/5.0/manual.html#7
