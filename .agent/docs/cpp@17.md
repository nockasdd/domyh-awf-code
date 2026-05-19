---
library: cpp
version: 17
latest: false
category: backend
official_docs: https://en.cppreference.com/w/cpp/17
last_updated: 2026-03-20
source: cppreference.com + curated
---

# C++17

> C++17 — Structured bindings, if constexpr, std::optional/variant/filesystem.
> ⚠️ For C++20+ features, see `cpp@20.md` and `cpp.md`.

## Version Comparison

| Feature | C++14 | C++17 |
|:--------|:------|:------|
| Structured bindings | ❌ | ✅ `auto [x, y] = pair;` |
| `if constexpr` | ❌ | ✅ Compile-time branching |
| `std::optional` | ❌ | ✅ Nullable value |
| `std::variant` | ❌ | ✅ Type-safe union |
| `std::any` | ❌ | ✅ Type-erased value |
| `std::filesystem` | ❌ | ✅ File system operations |
| `std::string_view` | ❌ | ✅ Non-owning string ref |
| `std::byte` | ❌ | ✅ Byte type |
| `if/switch` init | ❌ | ✅ `if (auto x = f(); x > 0)` |
| Fold expressions | ❌ | ✅ `(args + ...)` |
| Class template deduction | ❌ | ✅ `std::pair p{1, 2.0};` |
| `inline` variables | ❌ | ✅ Header-only definitions |
| `std::pmr` | ❌ | ✅ Polymorphic allocators |
| Parallel algorithms | ❌ | ✅ `std::execution::par` |
| Nested namespaces | ❌ | ✅ `namespace A::B::C {}` |

## Structured Bindings

```cpp
// Pair/Tuple
auto [name, age] = std::pair{"Alice", 30};

// Array
int arr[] = {1, 2, 3};
auto [a, b, c] = arr;

// Struct
struct Point { double x, y; };
auto [x, y] = Point{3.14, 2.71};

// Map iteration
std::map<std::string, int> scores = {{"Alice", 95}, {"Bob", 88}};
for (const auto& [name, score] : scores) {
    std::cout << name << ": " << score << "\n";
}
```

## std::optional

```cpp
#include <optional>

std::optional<int> find_user(std::string_view name) {
    if (auto it = db.find(name); it != db.end())
        return it->second;
    return std::nullopt;
}

// Usage
if (auto user = find_user("Alice"); user.has_value()) {
    process(*user);  // dereference
}

auto val = find_user("Bob").value_or(-1);  // default value
```

## std::variant

```cpp
#include <variant>

using Value = std::variant<int, double, std::string>;

Value v = 42;
v = "hello";

// Visit pattern
std::visit([](auto&& val) {
    using T = std::decay_t<decltype(val)>;
    if constexpr (std::is_same_v<T, int>)
        std::cout << "int: " << val << "\n";
    else if constexpr (std::is_same_v<T, std::string>)
        std::cout << "string: " << val << "\n";
}, v);

// Check type
bool is_int = std::holds_alternative<int>(v);
auto& str = std::get<std::string>(v);  // throws if wrong type
```

## if constexpr

```cpp
template<typename T>
auto serialize(const T& val) {
    if constexpr (std::is_arithmetic_v<T>) {
        return std::to_string(val);
    } else if constexpr (std::is_same_v<T, std::string>) {
        return val;
    } else {
        return val.to_string();  // custom method
    }
}
// Dead branches are NOT compiled — no linker errors
```

## std::filesystem

```cpp
#include <filesystem>
namespace fs = std::filesystem;

// Path operations
fs::path p = "/home/user/project/src/main.cpp";
p.filename();       // "main.cpp"
p.stem();           // "main"
p.extension();      // ".cpp"
p.parent_path();    // "/home/user/project/src"

// File operations
bool exists = fs::exists(p);
auto size = fs::file_size(p);
fs::copy("src.txt", "dst.txt");
fs::remove_all("temp_dir");
fs::create_directories("a/b/c");

// Directory iteration
for (auto& entry : fs::recursive_directory_iterator("src")) {
    if (entry.is_regular_file() && entry.path().extension() == ".cpp") {
        std::cout << entry.path() << " (" << entry.file_size() << " bytes)\n";
    }
}
```

## Parallel Algorithms

```cpp
#include <algorithm>
#include <execution>
#include <vector>

std::vector<int> v(1'000'000);

// Sequential (default)
std::sort(v.begin(), v.end());

// Parallel
std::sort(std::execution::par, v.begin(), v.end());

// Parallel + vectorized
std::sort(std::execution::par_unseq, v.begin(), v.end());

// Also: for_each, transform, reduce, inclusive_scan, etc.
auto sum = std::reduce(std::execution::par, v.begin(), v.end());
```

## Fold Expressions

```cpp
// Variadic template — fold over all args
template<typename... Args>
auto sum(Args... args) {
    return (args + ...);  // unary right fold: a + (b + (c + ...))
}

template<typename... Args>
void print_all(Args&&... args) {
    ((std::cout << args << " "), ...);  // comma fold
    std::cout << "\n";
}

sum(1, 2, 3, 4, 5);         // 15
print_all("hello", 42, 3.14);  // "hello 42 3.14"
```

## Gotchas

⚠️ **`std::optional`**: Don't use for error handling with info. Use `std::expected` (C++23) instead.

⚠️ **`std::variant`**: `std::visit` required for type-safe access. Can't visit without including all types.

⚠️ **Structured bindings**: Can't ignore members. All must be bound. Use `auto [_, y] = pair;` convention.

⚠️ **`if constexpr`**: Only removes dead code in templates. In non-template context, both branches compile.

⚠️ **`std::filesystem`**: Link with `-lstdc++fs` on older GCC. Throws on permission errors.

⚠️ **Parallel algorithms**: Need TBB (Threading Building Blocks) on GCC. MSVC has built-in support.

⚠️ **`std::string_view`**: Doesn't own memory! Don't return `string_view` to local string.

⚠️ **Compiler support**: GCC 7+, Clang 5+, MSVC 19.14+ for full C++17.
