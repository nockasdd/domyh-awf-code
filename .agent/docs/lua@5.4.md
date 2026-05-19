---
library: lua
version: 5.4
latest: true
category: language
official_docs: https://www.lua.org/manual/5.4/manual.html
last_updated: 2026-03-28
---

# Lua 5.4

> Lua 5.4 — Modern Language Semantics & GC Rework.
> ⚠️ This is the Current Broadly Deployed Stable Version.
> Docs: https://www.lua.org/manual/5.4/manual.html

## Overview

Lua 5.4 (released 2020) acts as the modern foundation for Lua embedders. While keeping syntax familiar, it radically changes under-the-hood optimization features (Generational GC) and adds modern control flow paradigms (deterministic resource destruction).

**Key Defining Features:**
- `<const>` and `<close>` variable attributes (To-be-closed variables).
- A new **Generational Garbage Collector** mode (improving peak performance exponentially for short-lived objects).
- Multiple Userdata values (replaces the singular 5.3 `uservalue`).
- Improved Random Number Generator (`math.random` uses xoshiro256** natively).

---

## 🛠 C API: Modern GC & Multiple User Values

### Multiple Userdata Slots
Lua 5.3 allowed mapping a single Lua value to a userdata struct. Lua 5.4 expands this into distinct, fast slots, completely changing the C API pattern.

```c
#include <lua.h>

typedef struct { int dummy; } MyObject;

void allocate_resource(lua_State *L) {
    // 3 slots available to bind Lua Values independently of _ENV
    MyObject *obj = (MyObject*)lua_newuserdatauv(L, sizeof(MyObject), 3);

    // Slot 1: Store a function mapping
    lua_pushcfunction(L, some_handler);
    lua_setiuservalue(L, -2, 1);

    // Slot 2: Store an identifying string
    lua_pushstring(L, "WidgetA");
    lua_setiuservalue(L, -2, 2);
}

void use_resource(lua_State *L) {
    // Assuming object is at index 1
    // Fetch slot 2 directly back onto the stack
    lua_getiuservalue(L, 1, 2);
    printf("Acting upon: %s\n", lua_tostring(L, -1));
    lua_pop(L, 1);
}
```

### Generational Garbage Collector
By default, Lua 5.4 runs in `LUA_GCGEN` mode, splitting objects into "young" and "old".
```c
// Enable Generational Collector
lua_gc(L, LUA_GCGEN, 0, 0);

// Revert to Incremental Collector (useful for realtime/games where predictability beats throughput)
lua_gc(L, LUA_GCINC, 0, 0, 0);
```

### The `__close` Metamethod Binding (RAII for C)
When closing slots linked to `<close>`, the C API provides tools to force early closure.
```c
lua_toclose(L, idx);   // Marks a slot as to-be-closed (triggers __close when popped)
lua_closeslot(L, idx); // Immediately invokes __close without waiting for scope exit
```

---

## 📜 Lua Script: Constants and Resource Safety

### `<const>` Variables
Lua 5.4 can finally enforce constant references (shallow). Note importantly: The *table reference* is constant, its *contents* are not.

```lua
local PI <const> = 3.14159
-- PI = 3.0 -- Error!

local T <const> = { x = 1 }
T.x = 2 -- Perfectly valid. The reference T cannot change, but fields can.
```

### `<close>` Variables (RAII / Deterministic Cleanup)
The killer feature of 5.4. Appending `<close>` guarantees that the item's `__close` metamethod is triggered EXACTLY when lexical scope exits, regardless of crashes, returns, or yields.

```lua
-- File handles use `__close` automatically in 5.4
local function parse_config()
    local f <close> = io.open("config.ini", "r")
    
    if not f then return false end
    if f:read() == "" then 
        return false -- `f` is guaranteed to be closed here!
    end
    
    return true -- `f` is guaranteed to be closed here too!
end

-- Using Custom Closables
local function Transaction()
    local this = {}
    return setmetatable(this, {
        __close = function(t, err)
            if err then
                print("Transaction aborted due to:", err)
            else
                print("Transaction committed cleanly.")
            end
        end
    })
end

do
    local tx <close> = Transaction()
    -- End of `do` block triggers __close
end
```

## ⛔ Migration Traps (5.4 → 5.5+)
- The generational GC is incredibly aggressive for game engines. If you notice stutter vs 5.3, revert to `LUA_GCINC` in your initialization C API code.
- `print()` calls `tostring` explicitly and will bypass `__tostring` metamethods of numbers.
- `debug.getinfo` results behave stringently regarding active C-level calls.
