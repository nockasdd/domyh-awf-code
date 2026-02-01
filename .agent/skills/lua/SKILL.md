---
name: lua
detect: ["*.lua", ".luarc.json", "init.lua", "conf.lua", "main.lua"]
version: "4.3.0"
category: scripting
tier: 1
---

# Lua Patterns — DOMYH Agent v4.3

> **Versions**: Lua 5.1, 5.2, 5.3, 5.4, 5.5 (Dec 2025), LuaJIT 2.1
> **Philosophy**: Simplicity, embeddability, flexibility via metatables

---

## 🎯 When to Use This Skill

Use for: Game scripting, embedded systems, configuration, plugin systems.
**NOT for**: Web backend (→ nodejs/python), mobile apps (→ swift/kotlin).

---

## 🔍 Version Detection

```lua
-- Check Lua version
print(_VERSION)  -- "Lua 5.4"

-- Check if LuaJIT
if jit then
    print("LuaJIT " .. jit.version)
end

-- Feature detection
if table.create then
    print("Lua 5.5+")
elseif rawlen then
    print("Lua 5.2+")
end
```

---

## 📦 Recommended Stack (2025-2026)

### Game Engines/Frameworks

| Framework       | Use Case                 | Version         |
| --------------- | ------------------------ | --------------- |
| **Love2D**      | 2D games, game jams      | Lua 5.1/LuaJIT  |
| **Defold**      | 2D/3D, cross-platform 🏆 | LuaJIT          |
| **Roblox Luau** | Roblox games             | Luau (Lua 5.1+) |
| **Solar2D**     | Mobile 2D                | Lua 5.1         |
| **Gideros**     | Mobile games             | Lua 5.1         |

### C/C++ Bindings

| Library        | Use Case           | Performance     |
| -------------- | ------------------ | --------------- |
| **LuaJIT FFI** | Direct C calls 🏆  | ~5 clock cycles |
| **sol3**       | Modern C++ binding | Very fast       |
| **LuaBridge3** | Lightweight C++    | Fast            |
| **tolua++**    | Legacy binding     | Moderate        |

### Web/Server

| Library       | Use Case      |
| ------------- | ------------- |
| **OpenResty** | Nginx + Lua   |
| **Lapis**     | Web framework |
| **LuaSocket** | Networking    |

### Utilities

| Library           | Use Case         |
| ----------------- | ---------------- |
| **Penlight**      | Stdlib extension |
| **LuaFileSystem** | File operations  |
| **LPeg**          | Parsing          |
| **Serpent**       | Serialization    |
| **inspect**       | Debug printing   |

### IDE Support

| IDE                    | Features             | Lua Versions    |
| ---------------------- | -------------------- | --------------- |
| **ZeroBrane Studio**   | Built-in debugger 🏆 | 5.1-5.4, LuaJIT |
| **VS Code + LuaLS**    | LSP, completion      | 5.1-5.5         |
| **IntelliJ + EmmyLua** | Refactoring, debug   | 5.1-5.4         |

---

## 🆕 Lua 5.4/5.5 Features

### Const Variables (Lua 5.4)

```lua
-- ✅ Constant variable (cannot be reassigned)
local MAX_PLAYERS <const> = 100

-- MAX_PLAYERS = 200  -- ERROR: attempt to assign to const variable

-- ✅ To-be-closed variable (auto cleanup)
local file <close> = io.open("data.txt", "r")
-- file:close() called automatically when scope ends
```

### Lua 5.5 Features (Dec 2025)

```lua
-- ✅ Global declaration (explicit)
global GameState = {}  -- New in 5.5

-- ✅ Pre-allocate table
local array = table.create(1000)  -- Pre-allocate 1000 slots

-- ✅ Read-only for loop variables
for i = 1, 10 do
    -- i = i + 1  -- ERROR in 5.5: can't modify loop variable
    print(i)
end
```

### Generational GC (Lua 5.4+)

```lua
-- ✅ GC modes
collectgarbage("generational")  -- Better for short-lived objects
collectgarbage("incremental")   -- Traditional mode

-- ✅ Tune GC
collectgarbage("setpause", 200)
collectgarbage("setstepmul", 200)
```

---

## 🎯 Core Patterns

### OOP with Metatables

```lua
-- ✅ Class pattern
local Entity = {}
Entity.__index = Entity

function Entity:new(x, y)
    local self = setmetatable({}, Entity)
    self.x = x or 0
    self.y = y or 0
    return self
end

function Entity:move(dx, dy)
    self.x = self.x + dx
    self.y = self.y + dy
end

-- ✅ Inheritance
local Player = setmetatable({}, {__index = Entity})
Player.__index = Player

function Player:new(x, y, name)
    local self = Entity.new(self, x, y)
    setmetatable(self, Player)
    self.name = name
    return self
end

function Player:greet()
    return "Hello, " .. self.name
end
```

### Module Pattern

```lua
-- ✅ Modern module (return table)
local M = {}

-- Private
local cache = {}

-- Public
function M.process(data)
    if cache[data] then
        return cache[data]
    end
    local result = heavyComputation(data)
    cache[data] = result
    return result
end

return M

-- Usage
local mymodule = require("mymodule")
mymodule.process("input")
```

### Error Handling

```lua
-- ✅ Protected call
local ok, result = pcall(function()
    return riskyOperation()
end)

if not ok then
    print("Error: " .. tostring(result))
end

-- ✅ With traceback
local ok, result = xpcall(function()
    return riskyOperation()
end, debug.traceback)

-- ✅ assert for preconditions
function divide(a, b)
    assert(b ~= 0, "Division by zero")
    return a / b
end

-- ✅ Custom error objects
local function createError(code, message)
    return {code = code, message = message}
end

local ok, err = pcall(function()
    error(createError("NOT_FOUND", "User not found"))
end)
```

---

## ⚡ Coroutines

```lua
-- ✅ Basic coroutine
local co = coroutine.create(function(x)
    for i = 1, 3 do
        print("co: " .. i)
        coroutine.yield(i * x)
    end
    return "done"
end)

-- Resume and get yielded values
print(coroutine.resume(co, 10))  -- true, 10
print(coroutine.resume(co))      -- true, 20
print(coroutine.resume(co))      -- true, 30
print(coroutine.resume(co))      -- true, "done"

-- ✅ Producer-Consumer pattern
local function producer()
    return coroutine.create(function()
        for i = 1, 100 do
            coroutine.yield(i)
        end
    end)
end

local function consumer(prod)
    while true do
        local ok, value = coroutine.resume(prod)
        if not ok or coroutine.status(prod) == "dead" then
            break
        end
        process(value)
    end
end

-- ✅ Close coroutine (Lua 5.4+)
coroutine.close(co)  -- Ensures cleanup of <close> variables
```

---

## 🎮 Game Engine Patterns

### Love2D

```lua
-- main.lua
function love.load()
    player = {
        x = 400,
        y = 300,
        speed = 200,
        sprite = love.graphics.newImage("player.png")
    }
end

function love.update(dt)
    -- Input handling
    if love.keyboard.isDown("left") then
        player.x = player.x - player.speed * dt
    elseif love.keyboard.isDown("right") then
        player.x = player.x + player.speed * dt
    end
end

function love.draw()
    love.graphics.draw(player.sprite, player.x, player.y)
end

function love.keypressed(key)
    if key == "escape" then
        love.event.quit()
    end
end
```

### Defold

```lua
-- player.script
function init(self)
    self.speed = 200
    msg.post(".", "acquire_input_focus")
end

function update(self, dt)
    local pos = go.get_position()
    pos.x = pos.x + self.velocity.x * dt
    go.set_position(pos)
end

function on_input(self, action_id, action)
    if action_id == hash("left") then
        self.velocity.x = -self.speed
    elseif action_id == hash("right") then
        self.velocity.x = self.speed
    end
end
```

### Roblox Luau

```lua
-- ServerScriptService/main.server.lua
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

Players.PlayerAdded:Connect(function(player)
    print(player.Name .. " joined!")

    player.CharacterAdded:Connect(function(character)
        local humanoid = character:WaitForChild("Humanoid")
        humanoid.WalkSpeed = 20
    end)
end)
```

---

## 🔧 LuaJIT FFI

```lua
local ffi = require("ffi")

-- ✅ Declare C types
ffi.cdef[[
typedef struct { double x, y; } Point;
typedef struct { Point a, b; } Line;

double sqrt(double x);
int printf(const char *fmt, ...);
]]

-- ✅ Call C functions
local x = ffi.C.sqrt(2.0)
ffi.C.printf("Result: %g\n", x)

-- ✅ Create C structs
local point = ffi.new("Point", {10.0, 20.0})
print(point.x, point.y)

-- ✅ Arrays
local arr = ffi.new("int[?]", 100)  -- VLA
for i = 0, 99 do
    arr[i] = i * 2
end

-- ✅ Load external library
local mylib = ffi.load("mylib")
local result = mylib.my_function(42)
```

---

## 📏 Performance Best Practices

```lua
-- ✅ Local is faster than global
local math_sin = math.sin
local table_insert = table.insert

-- ✅ Pre-allocate tables (Lua 5.5)
local results = table.create and table.create(1000) or {}

-- ✅ Avoid string concatenation in loops
local parts = {}
for i = 1, 1000 do
    parts[i] = "item" .. i
end
local result = table.concat(parts, ",")  -- Single allocation

-- ✅ Object pooling
local Pool = {}
Pool.__index = Pool

function Pool:new(factory)
    return setmetatable({factory = factory, items = {}}, Pool)
end

function Pool:get()
    return table.remove(self.items) or self.factory()
end

function Pool:release(item)
    table.insert(self.items, item)
end

-- ✅ Avoid creating closures in hot loops
local function process(x) return x * 2 end  -- Define once
for i = 1, 1000000 do
    result = process(i)  -- Reuse
end
```

---

## 🧪 Testing

```lua
-- ✅ Simple test pattern
local function test_add()
    assert(add(1, 2) == 3, "add(1, 2) should equal 3")
    assert(add(-1, 1) == 0, "add(-1, 1) should equal 0")
    print("✓ test_add passed")
end

-- ✅ Using busted (test framework)
describe("User", function()
    it("should create with name", function()
        local user = User:new("Alice")
        assert.are.equal("Alice", user.name)
    end)

    it("should greet", function()
        local user = User:new("Bob")
        assert.has.match("Hello", user:greet())
    end)
end)
```

---

## ✅ Best Practices Checklist

### Code Quality

- [ ] Use `local` for all variables
- [ ] Return tables from modules
- [ ] Use metatables correctly
- [ ] Handle errors with `pcall`/`xpcall`

### Performance

- [ ] Cache global functions as locals
- [ ] Pre-allocate tables when possible
- [ ] Use `table.concat` for strings
- [ ] Avoid closures in hot loops

### Memory

- [ ] Use weak tables for caches
- [ ] Use `<close>` for resources (Lua 5.4+)
- [ ] Consider object pooling
- [ ] Tune GC for your use case

### Version-Specific

- [ ] Check `_VERSION` for compatibility
- [ ] Use `jit` check for LuaJIT
- [ ] Feature-detect before using new APIs
- [ ] Document minimum Lua version

---

_DOMYH Agent v4.3 • Lua 5.1-5.5, LuaJIT_
