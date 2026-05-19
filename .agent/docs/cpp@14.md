---
library: cpp
version: 14
latest: false
category: backend
official_docs: https://en.cppreference.com/w/cpp/14
last_updated: 2026-03-20
source: cppreference.com + curated
---

# C++14 (and below)

> C++11/14 — Foundation of modern C++. Move semantics, auto, lambdas, smart pointers.
> ⚠️ For C++17+ features, see `cpp@17.md`.

## Version Comparison

| Feature | C++03 | C++11 | C++14 |
|:--------|:------|:------|:------|
| `auto` type deduction | ❌ | ✅ | ✅ + return type |
| Lambda expressions | ❌ | ✅ basic | ✅ generic/init capture |
| Move semantics | ❌ | ✅ `&&` | ✅ |
| Smart pointers | ❌ | ✅ `unique/shared` | ✅ + `make_unique` |
| Range-for | ❌ | ✅ `for(auto& x : v)` | ✅ |
| `nullptr` | ❌ | ✅ | ✅ |
| `constexpr` | ❌ | ✅ (limited) | ✅ (relaxed) |
| `enum class` | ❌ | ✅ | ✅ |
| Variadic templates | ❌ | ✅ `Args...` | ✅ |
| `static_assert` | ❌ | ✅ (with msg) | ✅ (no msg) |
| User-defined literals | ❌ | ✅ | ✅ |
| `std::array` | ❌ | ✅ | ✅ |
| `std::tuple` | ❌ | ✅ | ✅ |
| `std::thread` | ❌ | ✅ | ✅ |
| `std::chrono` | ❌ | ✅ | ✅ |
| `std::regex` | ❌ | ✅ | ✅ |
| Binary literals | ❌ | ❌ | ✅ `0b1010` |
| Digit separator | ❌ | ❌ | ✅ `1'000'000` |

## Core C++11 Features

### auto & Type Deduction

```cpp
auto x = 42;            // int
auto y = 3.14;           // double
auto s = std::string("hello");
auto v = std::vector<int>{1, 2, 3};

// C++14: auto return type
auto add(int a, int b) { return a + b; }

// decltype — query expression type
decltype(x) z = 100;    // int
```

### Lambda Expressions

```cpp
// C++11 basic lambda
auto square = [](int x) { return x * x; };

// Capture
int factor = 10;
auto multiply = [factor](int x) { return x * factor; };
auto modify = [&factor](int x) { factor = x; };

// C++14: generic lambda
auto print = [](auto val) { std::cout << val << "\n"; };

// C++14: init capture (move into lambda)
auto ptr = std::make_unique<int>(42);
auto closure = [p = std::move(ptr)]() { return *p; };
```

### Move Semantics

```cpp
#include <utility>

// Rvalue references: T&&
std::string create() {
    std::string s = "hello";
    return s;  // NRVO or implicit move
}

// std::move — cast to rvalue
std::vector<int> v1 = {1, 2, 3};
std::vector<int> v2 = std::move(v1);  // v1 is empty after this

// Perfect forwarding
template<typename T>
void wrapper(T&& arg) {
    process(std::forward<T>(arg));  // preserves value category
}
```

### Smart Pointers

```cpp
#include <memory>

// unique_ptr (exclusive ownership)
auto up = std::make_unique<int>(42);       // C++14 make_unique
std::unique_ptr<int> up2(new int(42));     // C++11 alternative

// shared_ptr (shared ownership)
auto sp = std::make_shared<std::string>("hello");
auto sp2 = sp;  // refcount = 2

// weak_ptr (break cycles)
std::weak_ptr<int> wp = sp;
if (auto locked = wp.lock()) {
    // use locked
}
```

### Containers & Algorithms

```cpp
#include <vector>
#include <array>
#include <unordered_map>
#include <algorithm>

// Initializer lists
std::vector<int> v = {1, 2, 3, 4, 5};

// Range-based for
for (const auto& item : v) { /* ... */ }

// std::array — fixed-size, stack-allocated
std::array<int, 5> arr = {1, 2, 3, 4, 5};

// unordered_map (hash map)
std::unordered_map<std::string, int> m = {{"a", 1}, {"b", 2}};

// Algorithms with lambdas
auto it = std::find_if(v.begin(), v.end(), [](int n) { return n > 3; });
std::sort(v.begin(), v.end(), [](int a, int b) { return a > b; });
int sum = std::accumulate(v.begin(), v.end(), 0);
```

### Threading (C++11)

```cpp
#include <thread>
#include <mutex>
#include <future>
#include <atomic>

// Thread
std::thread t([]{ heavy_work(); });
t.join();  // MUST join or detach before destruction

// Mutex
std::mutex mtx;
{
    std::lock_guard<std::mutex> lock(mtx);
    shared_resource.modify();
}

// async/future
auto future = std::async(std::launch::async, [] { return compute(); });
int result = future.get();

// atomic
std::atomic<bool> running{true};
running.store(false);
```

### Enum Class (Scoped Enums)

```cpp
enum class Color { Red, Green, Blue };
enum class Direction : uint8_t { North, South, East, West };

Color c = Color::Red;
// int x = c;           // ❌ no implicit conversion
int x = static_cast<int>(c);  // ✅ explicit

// C++11 also: enum class forward declaration
enum class Status : int;
```

## Gotchas

⚠️ **`std::move` doesn't move**: It's just a cast to `T&&`. Actual move happens in constructor/assignment.

⚠️ **`.join()` required**: `std::thread` calls `std::terminate()` if destroyed without join/detach.

⚠️ **`unique_ptr` not copyable**: Use `std::move()` to transfer ownership.

⚠️ **Lambda capture by ref**: Dangling reference if lambda outlives captured variable.

⚠️ **`auto` pitfall**: `auto x = {1, 2, 3}` is `std::initializer_list<int>`, NOT `std::vector`.

⚠️ **`constexpr` (C++11)**: Very limited — single return statement. C++14 relaxes this significantly.

⚠️ **`std::regex`**: Extremely slow on most implementations. Prefer `RE2` or `CTRE` for performance.

⚠️ **`make_unique`**: C++14 only. In C++11, use `unique_ptr<T>(new T(...))`.

⚠️ **Compiler support**: GCC 4.8+ (C++11), GCC 5+ (full C++14). Clang 3.4+ (C++14). MSVC 2015+.
