---
library: lua
version: 5.3
latest: false
category: language
official_docs: https://www.lua.org/manual/5.3/manual.html
last_updated: 2026-03-28
---

# Lua 5.3

> Lua 5.3 — The Integers Update.
> ⚠️ This is NOT the latest Lua version. For Lua 5.4/5.5, see `lua.md`.
> Docs: https://www.lua.org/manual/5.3/manual.html

## Overview

Lua 5.3 (released 2015) introduced arguably the most profound change to Lua's type layout in decades: **true native 64-bit integers**. Prior to 5.3, all numbers were `double` precision floats. With Native Integers came Native Bitwise operators, eliminating the clunky `bit` or `bit32` libraries.

**Key Defining Features:**
- A native 64-bit `integer` subtype.
- Native Bitwise operators: `&`, `|`, `~`, `<<`, `>>`.
- Floor division `//`.
- The `utf8` library for basic Unicode string handling.
- Pattern matching binary string packing (`string.pack`, `unpack`, `packsize`).

---

## 🛠 C API: Integers & Bitwise Additions

### The Native Integer Distinction
Lua 5.3 distinguishes internally between floats and ints. `lua_tonumber()` still returns a double, but `lua_tointeger()` returns true 64-bit ints.

```c
#include <lua.h>

// Pushing a 64-bit integer
lua_pushinteger(L, 9007199254740992LL); // Fits beautifully now!

// Reading a number safely
int is_num;
lua_Integer val = lua_tointegerx(L, -1, &is_num);
if (is_num) {
    printf("It genuinely is a native integer: %lld\n", val);
}

// Check exactly what the internal subtype is:
int type = lua_type(L, -1);
if (type == LUA_TNUMBER) {
    if (lua_isinteger(L, -1)) {
        // It's a 64-bit lua_Integer
    } else {
        // It's a lua_Number (double)
    }
}
```

### Advanced Lua Arithmetic API
The `lua_arith` API now supports bitwise operations natively from C.
```c
lua_arith(L, LUA_OPBAND);  // Bitwise AND (&)
lua_arith(L, LUA_OPSHR);   // Right Shift (>>)
lua_arith(L, LUA_OPBNOT);  // Bitwise NOT (~)
```

---

## 📜 Lua Script: Integers & Operators

### 64-bit Integers vs Floats
The syntax of a literal number dictates whether Lua compiles it as an Integer or a Float.

```lua
local a = 10     -- Internal type: integer
local b = 10.0   -- Internal type: float
local c = 10e0   -- Internal type: float

-- Arithmetic conversion:
print(a + 0)     -- 10 (int + int = int)
print(a + 0.0)   -- 10.0 (int + float = float)

-- Division:
print(5 / 2)     -- 2.5 (Standard division ALWAYS returns a float)
print(5 // 2)    -- 2 (Floor division ALWAYS returns an integer if operands are int)
```

### Native Bitwise Operators
All bitwise operations implicitly convert operands to integers.

```lua
local hex = 0xFF
local mask = 0x0F

print(hex & mask)   -- Bitwise AND
print(hex | mask)   -- Bitwise OR
print(hex ~ mask)   -- Bitwise XOR
print(1 << 8)       -- Left Shift
print(256 >> 2)     -- Right Shift

-- Unary bitwise NOT:
print(~0xFF)
```

### Packing Binaries & UTF-8
Lua 5.3 handles arbitrary binary structures natively.

```lua
-- Packing an unsigned 32-bit big endian integer
local bin = string.pack(">I4", 0xAABBCCDD)

-- Unpacking
local val, next_pos = string.unpack(">I4", bin)

-- Testing string lengths properly (with UTF-8, instead of raw bytes)
local u_str = "ãéì"
print(#u_str)             -- 6 (Size in raw bytes)
print(utf8.len(u_str))    -- 3 (Length in unicode scalar characters)
```

## ⛔ Migration Traps (5.3 → 5.4+)
- The `bit32` library dropped entirely. Convert `bit32.band(x, y)` to `x & y`.
- Float conversions to Strings act differently. Previously `print(10.0)` output `"10"`. In 5.3+, it correctly outputs `"10.0"`.
- `math.cosh`, `math.sinh`, `math.tanh`, and `math.pow` were removed. (Use `x^y` instead of `math.pow`).
- Userdata in 5.3 allows mapping to arbitrary user values efficiently (`lua_getuservalue`), but this drastically changes syntax in 5.4 to multiple user values.
