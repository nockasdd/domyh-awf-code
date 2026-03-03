---
name: crystal
description: "Crystal type-safe Ruby-like language patterns. Use when working with .cr files."
detect: ["*.cr", "shard.yml", "shard.lock"]
category: language
tier: 3
---

# Crystal Patterns — DOMYH Awesome Code

> **Version**: Crystal 1.10+ (2025-2026)
> **Framework**: Kemal, Lucky
> **Philosophy**: Ruby syntax, C speed, type safety

---

## 🎯 When to Use

Use for: APIs, CLI tools, Ruby developers wanting performance.
**NOT for**: Windows (limited support), large ecosystem needs.

---

## 🔧 Project Setup

```bash
crystal init app myapp
cd myapp
shards install
crystal run src/myapp.cr
```

---

## 🔄 Core Patterns

### Classes and Structs

```crystal
class User
  property id : Int32
  property name : String
  property email : String
  property active : Bool = true

  def initialize(@name : String, @email : String)
    @id = Random.rand(Int32::MAX)
  end

  def greet : String
    "Hello, #{name}!"
  end
end

# Struct for value types
struct Point
  getter x : Int32
  getter y : Int32

  def initialize(@x, @y)
  end

  def distance_from_origin : Float64
    Math.sqrt(x**2 + y**2)
  end
end
```

### HTTP Server with Kemal

```crystal
require "kemal"

get "/" do
  "Hello World!"
end

get "/users/:id" do |env|
  id = env.params.url["id"]
  {"id": id}.to_json
end

post "/users" do |env|
  name = env.params.json["name"].as(String)
  {"created": name}.to_json
end

Kemal.run
```

### Concurrency with Fibers

```crystal
channel = Channel(Int32).new

spawn do
  10.times { |i| channel.send(i) }
  channel.close
end

while value = channel.receive?
  puts value
end
```

---

## ✅ Production Checklist

- [ ] `crystal tool format` applied
- [ ] Tests with `crystal spec`
- [ ] Static binary compiled
- [ ] `ameba` linter passing

---
