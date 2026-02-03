# Lua — Advanced Patterns

# DOMYH Awesome Code v5.5 — Tier 3 Reference

## Table of Contents

- [Metatables & OOP](#metatables--oop)
- [Coroutines](#coroutines)
- [Module System](#module-system)
- [Game Development](#game-development)

---

## Metatables & OOP

### Class System

```lua
local Class = {}
Class.__index = Class

function Class:new(...)
    local instance = setmetatable({}, self)
    if instance.init then
        instance:init(...)
    end
    return instance
end

function Class:extend()
    local subclass = {}
    subclass.__index = subclass
    setmetatable(subclass, {
        __index = self,
        __call = function(cls, ...)
            return cls:new(...)
        end
    })
    return subclass
end

-- Usage
local Entity = Class:extend()

function Entity:init(x, y)
    self.x = x or 0
    self.y = y or 0
end

function Entity:move(dx, dy)
    self.x = self.x + dx
    self.y = self.y + dy
end

local Player = Entity:extend()

function Player:init(x, y, name)
    Entity.init(self, x, y)
    self.name = name
end
```

### Operator Overloading

```lua
local Vector = {}
Vector.__index = Vector

function Vector.new(x, y)
    return setmetatable({x = x, y = y}, Vector)
end

function Vector.__add(a, b)
    return Vector.new(a.x + b.x, a.y + b.y)
end

function Vector.__mul(a, b)
    if type(b) == "number" then
        return Vector.new(a.x * b, a.y * b)
    end
    return a.x * b.x + a.y * b.y -- Dot product
end

function Vector.__tostring(v)
    return string.format("(%g, %g)", v.x, v.y)
end
```

---

## Coroutines

### Iterator Pattern

```lua
function range(start, stop, step)
    step = step or 1
    return coroutine.wrap(function()
        for i = start, stop, step do
            coroutine.yield(i)
        end
    end)
end

-- Usage
for i in range(1, 10, 2) do
    print(i) -- 1, 3, 5, 7, 9
end
```

### Async Simulation

```lua
local Scheduler = {
    tasks = {},
    current = nil
}

function Scheduler:spawn(fn)
    local co = coroutine.create(fn)
    table.insert(self.tasks, co)
    return co
end

function Scheduler:sleep(seconds)
    -- In real impl, would schedule wakeup
    coroutine.yield({type = "sleep", duration = seconds})
end

function Scheduler:run()
    while #self.tasks > 0 do
        local task = table.remove(self.tasks, 1)
        self.current = task

        local ok, result = coroutine.resume(task)

        if coroutine.status(task) ~= "dead" then
            table.insert(self.tasks, task)
        end
    end
end
```

---

## Module System

### Module Pattern

```lua
-- mymodule.lua
local M = {}

-- Private state
local cache = {}

-- Private function
local function compute(x)
    return x * 2
end

-- Public API
function M.get(key)
    if not cache[key] then
        cache[key] = compute(key)
    end
    return cache[key]
end

function M.clear()
    cache = {}
end

return M
```

### Lazy Loading

```lua
local function lazy(moduleName)
    local module = nil
    return setmetatable({}, {
        __index = function(_, key)
            if module == nil then
                module = require(moduleName)
            end
            return module[key]
        end
    })
end

-- Only loads when first accessed
local json = lazy("dkjson")
```

---

## Game Development

### Entity Component System

```lua
local World = {
    entities = {},
    systems = {},
    components = {}
}

function World:createEntity()
    local entity = { id = #self.entities + 1, components = {} }
    table.insert(self.entities, entity)
    return entity
end

function World:addComponent(entity, componentName, data)
    entity.components[componentName] = data
    self.components[componentName] = self.components[componentName] or {}
    table.insert(self.components[componentName], entity)
end

function World:addSystem(system)
    table.insert(self.systems, system)
end

function World:update(dt)
    for _, system in ipairs(self.systems) do
        for _, entity in ipairs(self.entities) do
            if system:matches(entity) then
                system:process(entity, dt)
            end
        end
    end
end

-- Movement system
local MovementSystem = {
    required = {"position", "velocity"}
}

function MovementSystem:matches(entity)
    for _, comp in ipairs(self.required) do
        if not entity.components[comp] then return false end
    end
    return true
end

function MovementSystem:process(entity, dt)
    local pos = entity.components.position
    local vel = entity.components.velocity
    pos.x = pos.x + vel.x * dt
    pos.y = pos.y + vel.y * dt
end
```

---

_DOMYH Awesome Code v6.0.0 — Tier 3 Reference_
