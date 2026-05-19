---
library: cpp
version: 20
latest: false
category: backend
official_docs: https://en.cppreference.com/w/cpp/20
last_updated: 2026-03-20
source: cppreference.com + curated
---

# C++20

> C++20 — Major revision. Concepts, Ranges, Coroutines, Modules, std::format.
> ⚠️ For latest C++23/26 features, see `cpp.md`.

## Version Comparison

| Feature | C++17 | C++20 |
|:--------|:------|:------|
| Concepts | ❌ | ✅ `template<Concept T>` |
| Ranges | ❌ | ✅ `std::views::filter/transform` |
| Coroutines | ❌ | ✅ `co_await/co_yield/co_return` |
| Modules | ❌ | ✅ `import/export module` |
| `std::format` | ❌ | ✅ `std::format("{}", x)` |
| Three-way comparison | ❌ | ✅ `<=>` spaceship operator |
| `consteval` | ❌ | ✅ Immediate functions |
| `constinit` | ❌ | ✅ Static init guarantee |
| `std::span` | ❌ | ✅ Non-owning view over arrays |
| `std::jthread` | ❌ | ✅ Auto-joining thread |
| `std::latch/barrier` | ❌ | ✅ Synchronization primitives |
| `std::source_location` | ❌ | ✅ `__FILE__/__LINE__` replacement |
| Calendar/timezone | ❌ | ✅ `std::chrono` extensions |
| `starts_with/ends_with` | ❌ | ✅ String methods |
| Designated initializers | ❌ | ✅ `.field = value` |
| `requires` clause | ❌ | ✅ Constraint expressions |

## Concepts

```cpp
#include <concepts>

// Standard concepts
template<std::integral T>          // integer types only
T gcd(T a, T b) { return b == 0 ? a : gcd(b, a % b); }

template<std::floating_point T>    // float/double only
T lerp(T a, T b, T t) { return a + t * (b - a); }

// Custom concept
template<typename T>
concept Hashable = requires(T t) {
    { std::hash<T>{}(t) } -> std::convertible_to<std::size_t>;
};

// Abbreviated function templates
auto process(std::integral auto value) { return value * 2; }
```

## Ranges

```cpp
#include <ranges>
#include <vector>
namespace rv = std::ranges::views;

std::vector<int> v = {5, 3, 8, 1, 9, 2, 7};

// Lazy pipeline
auto result = v
    | rv::filter([](int n) { return n > 3; })
    | rv::transform([](int n) { return n * n; })
    | rv::take(3);

// Range algorithms
std::ranges::sort(v);
auto [min, max] = std::ranges::minmax(v);
auto it = std::ranges::find_if(v, [](int n) { return n > 5; });

// Views
auto iota = rv::iota(1, 11);          // 1..10
auto repeat = rv::repeat(42) | rv::take(5);  // 42,42,42,42,42
```

## std::format

```cpp
#include <format>
#include <string>

std::string s = std::format("Hello, {}!", "World");
std::string n = std::format("{:d} {:x} {:b}", 42, 42, 42);  // "42 2a 101010"
std::string f = std::format("{:.2f}", 3.14159);               // "3.14"
std::string p = std::format("{:>20}", "right-aligned");

// Custom formatter
template<>
struct std::formatter<Point> {
    constexpr auto parse(format_parse_context& ctx) { return ctx.begin(); }
    auto format(const Point& p, format_context& ctx) const {
        return std::format_to(ctx.out(), "({}, {})", p.x, p.y);
    }
};
```

## Spaceship Operator (<=>)

```cpp
#include <compare>

struct Version {
    int major, minor, patch;
    auto operator<=>(const Version&) const = default;  // generates all 6 operators
};

Version v1{1, 2, 3}, v2{1, 3, 0};
bool newer = v1 < v2;   // true
bool same = v1 == v2;   // false
// Also generates: !=, <=, >=, >
```

## std::span — Non-owning View

```cpp
#include <span>

void process(std::span<const int> data) {
    for (int val : data) { /* ... */ }
    auto first3 = data.subspan(0, 3);
    auto last2 = data.last(2);
}

int arr[] = {1, 2, 3, 4, 5};
std::vector<int> vec = {1, 2, 3};
process(arr);   // works with C arrays
process(vec);   // works with vectors
```

## Designated Initializers

```cpp
struct Config {
    int width = 800;
    int height = 600;
    bool fullscreen = false;
    std::string title = "App";
};

Config cfg = {
    .width = 1920,
    .height = 1080,
    .fullscreen = true,
    // .title uses default
};
```

## Calendar & Time Zones

```cpp
#include <chrono>
using namespace std::chrono;

// Calendar types
auto today = floor<days>(system_clock::now());
year_month_day ymd{year{2026}/March/20};
auto weekday = year_month_weekday{ymd}.weekday();  // Thursday

// Duration literals
auto timeout = 5s;          // seconds
auto interval = 100ms;      // milliseconds
auto delay = 2min + 30s;    // 2.5 minutes
```

## Coroutines (Basics)

```cpp
#include <coroutine>

// co_await — suspend and resume
task<int> fetch_data() {
    auto response = co_await http_get("https://api.example.com/data");
    co_return response.status_code;
}

// co_yield — generator pattern (need custom promise_type or C++23 std::generator)
generator<int> range(int start, int end) {
    for (int i = start; i < end; ++i) {
        co_yield i;
    }
}
```

## Gotchas

⚠️ **Modules**: Build system support needed. CMake 3.28+ with `cxx_std_20`. MSVC has best support.

⚠️ **Coroutines**: C++20 provides mechanism only. No `std::generator` until C++23. Use `cppcoro` library.

⚠️ **Ranges**: Some views are not copyable. Use `auto&&` or `std::ranges::to<vector>()` (C++23).

⚠️ **`<=>` default**: Only works when all members are comparable. Custom types need manual impl.

⚠️ **Concepts**: Prefer standard concepts from `<concepts>` before writing custom ones.

⚠️ **`constinit`**: Only for variables with static/thread-local storage duration.

⚠️ **Compiler support**: GCC 11+, Clang 14+, MSVC 19.29+ for most C++20 features.
