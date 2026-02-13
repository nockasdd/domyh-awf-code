---
name: julia
detect: ["*.jl", "Project.toml", "Manifest.toml"]
version: "6.2.6"
category: scientific
tier: 2
---

# Julia Patterns — DOMYH Awesome Code

> **Version**: Julia 1.10+ (2025-2026)
> **Focus**: Scientific computing, ML, high performance
> **Philosophy**: Fast as C, easy as Python

---

## 🎯 When to Use This Skill

Use for: Numerical computing, ML, simulations, scientific research.
**NOT for**: Web apps (→ python/go), mobile (→ flutter).

---

## 📦 Why Julia?

| Feature | Julia      | Python  | R       |
| ------- | ---------- | ------- | ------- |
| Speed   | C-like 🏆  | Slow    | Slow    |
| Syntax  | Easy 🏆    | Easy    | Easy    |
| ML      | Flux/MLJ   | PyTorch | Limited |
| Interop | Python/C/R | C       | C       |

---

## 🔧 Project Setup

```julia
# Create project
julia> ] generate MyProject
julia> cd MyProject
julia> ] activate .

# Add packages
julia> ] add DataFrames, Plots, Flux
```

### Project Structure

```
MyProject/
├── Project.toml
├── Manifest.toml
├── src/
│   └── MyProject.jl
└── test/
    └── runtests.jl
```

---

## 🔄 Core Patterns

### Multiple Dispatch

```julia
# ✅ Define methods for different types
function process(x::Int)
    println("Integer: $x")
end

function process(x::Float64)
    println("Float: $x")
end

function process(x::String)
    println("String: $x")
end

# ✅ Custom types
struct User
    name::String
    age::Int
end

function greet(u::User)
    println("Hello, $(u.name)!")
end
```

### Broadcasting

```julia
# ✅ Dot syntax for element-wise
a = [1, 2, 3]
b = [4, 5, 6]

c = a .+ b        # [5, 7, 9]
d = sin.(a)       # Apply sin to each
e = a .^ 2        # Square each

# ✅ Custom function broadcasting
double(x) = x * 2
double.(a)        # [2, 4, 6]
```

---

## 📊 DataFrames

```julia
using DataFrames, CSV

# ✅ Create DataFrame
df = DataFrame(
    name = ["Alice", "Bob", "Carol"],
    age = [25, 30, 35],
    salary = [50000, 60000, 70000]
)

# ✅ Filter and transform
result = df |>
    x -> filter(row -> row.age > 25, x) |>
    x -> select(x, :name, :salary) |>
    x -> transform(x, :salary => (s -> s .* 1.1) => :new_salary)

# ✅ Group and aggregate
grouped = combine(
    groupby(df, :age),
    :salary => mean => :avg_salary,
    nrow => :count
)
```

---

## 🤖 ML with Flux

```julia
using Flux

# ✅ Define model
model = Chain(
    Dense(784, 128, relu),
    Dropout(0.2),
    Dense(128, 64, relu),
    Dense(64, 10),
    softmax
)

# ✅ Loss and optimizer
loss(x, y) = Flux.crossentropy(model(x), y)
opt = Adam(0.001)

# ✅ Training loop
for epoch in 1:10
    for (x, y) in train_loader
        gs = gradient(() -> loss(x, y), params(model))
        Flux.update!(opt, params(model), gs)
    end
end
```

---

## ✅ Production Checklist

- [ ] Type annotations for performance
- [ ] Tests with `@testset`
- [ ] JuliaFormatter applied
- [ ] Package documented

---

_DOMYH Awesome Code • Julia 1.10+_
