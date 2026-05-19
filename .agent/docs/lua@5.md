---
library: lua
version: 5
latest: false
category: language
official_docs: https://www.lua.org/manual/5.4/manual.html
last_updated: 2026-03-28
---

# Lua 5.x Overview

> This document serves as a navigational hub for the 5.x version lifecycle of Lua.
> Due to massive API deviations between minor versions, they have been split for clarity.

## 🗂 Version Definitions

Please select the exact version deployed in your target C++ application, Game Engine, or runtime environment:

### 🟢 [Lua 5.1 & LuaJIT (2006)](lua@5.1.md)
The most widespread specific target in gaming. Features `module()`, `setfenv`, and `getfenv`. If your prompt mentions *Roblox, World of Warcraft, Neovim, LÖVE2D, or Nginx*, **you must read this file**.

### 🟡 [Lua 5.2 (2011)](lua@5.2.md)
The transitional architecture. `setfenv` was deleted and replaced by true lexical environments (`_ENV`). The `goto` statement and `bit32` library were added.

### 🔴 [Lua 5.3 (2015)](lua@5.3.md)
The Arithmetic update. Native 64-bit integers and native bitwise operators (`&`, `|`, `<<`) were introduced to the absolute detriment of backward compatibility for scripts heavily abusing floating point features.

### 🟣 [Lua 5.4 (2020)](lua@5.4.md)
The current global stable benchmark. Features immutable references (`<const>`), deterministic resource closure (`<close>`), and the new Generational GC scheme.

---

## 🏗 The `lua_State` (C API Common Ground)
Throughout all 5.x variants, the core principle remains identical: a virtual stack manipulating a single thread state.

```c
lua_State *L = luaL_newstate(); // Universal 5.x initialization

// Elements are pushed on the top of the stack
lua_pushstring(L, "Top Element");

// Elements are pulled via relative negative indexing (-1 = Top)
const char *val = lua_tostring(L, -1);
```

For detailed changes to the C API and Stack across updates, refer to the **[Lua Migration Guard](lua-migration.md)**.
