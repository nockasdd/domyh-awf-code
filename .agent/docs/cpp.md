---
library: cpp
version: 23
latest: true
category: backend
official_docs: https://en.cppreference.com/w/cpp
last_updated: 2026-03-20
source: cppreference.com + curated
---

# C++ (C++23/26)

> C++ — High-performance systems programming language.
> Current: C++23 (ISO/IEC 14882:2024) | Next: C++26 (expected 2026)
> Ref: https://en.cppreference.com/w/cpp

## Version Comparison

| Feature | C++14 | C++17 | C++20 | C++23 | C++26 |
|:--------|:------|:------|:------|:------|:------|
| `auto` return type | ✅ | ✅ | ✅ | ✅ | ✅ |
| Structured bindings | ❌ | ✅ | ✅ | ✅ | ✅ |
| `if constexpr` | ❌ | ✅ | ✅ | ✅ | ✅ |
| `std::optional/variant/any` | ❌ | ✅ | ✅ | ✅ | ✅ |
| `std::filesystem` | ❌ | ✅ | ✅ | ✅ | ✅ |
| Concepts | ❌ | ❌ | ✅ | ✅ | ✅ |
| Ranges | ❌ | ❌ | ✅ | ✅ | ✅ |
| Coroutines | ❌ | ❌ | ✅ | ✅ | ✅ |
| Modules | ❌ | ❌ | ✅ | ✅ | ✅ |
| `std::format` | ❌ | ❌ | ✅ | ✅ | ✅ |
| `std::expected` | ❌ | ❌ | ❌ | ✅ | ✅ |
| `std::print/println` | ❌ | ❌ | ❌ | ✅ | ✅ |
| `std::flat_map/flat_set` | ❌ | ❌ | ❌ | ✅ | ✅ |
| `std::generator` | ❌ | ❌ | ❌ | ✅ | ✅ |
| `std::mdspan` | ❌ | ❌ | ❌ | ✅ | ✅ |
| `std::stacktrace` | ❌ | ❌ | ❌ | ✅ | ✅ |
| Contracts | ❌ | ❌ | ❌ | ❌ | ✅ |
| Reflection | ❌ | ❌ | ❌ | ❌ | ✅ |
| `std::execution` (sender/receiver) | ❌ | ❌ | ❌ | ❌ | ✅ |

## Modern I/O — std::print (C++23)

```cpp
#include <print>

// Replaces printf AND cout — type-safe, fast, Unicode-aware
std::println("Hello, {}!", name);                        // with newline
std::print("x = {}, y = {}\n", x, y);                   // without newline
std::println("Pi = {:.4f}", 3.14159);                    // format spec
std::println("Hex: {:#x}, Bin: {:#b}", 255, 42);        // 0xff, 0b101010
std::println("Pad: {:>10}, {:0>5}", "right", 42);       // "     right", "00042"

// Print to stream
std::println(std::cerr, "Error: {}", msg);
```

## Error Handling — std::expected (C++23)

```cpp
#include <expected>
#include <string>

enum class Error { NotFound, InvalidInput, Timeout };

std::expected<int, Error> parse_int(std::string_view s) {
    try {
        return std::stoi(std::string(s));
    } catch (...) {
        return std::unexpected(Error::InvalidInput);
    }
}

// Usage — monadic operations
auto result = parse_int("42")
    .transform([](int n) { return n * 2; })         // map value
    .or_else([](Error e) -> std::expected<int, Error> {
        return std::unexpected(e);                    // handle error
    });

if (result) {
    std::println("Value: {}", *result);
} else {
    std::println("Error occurred");
}
```

## Concepts (C++20)

```cpp
#include <concepts>

// Define concept
template<typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

template<typename T>
concept Printable = requires(T t) {
    { std::println("{}", t) };
};

template<typename T>
concept Container = requires(T c) {
    { c.begin() } -> std::input_iterator;
    { c.end() } -> std::sentinel_for<decltype(c.begin())>;
    { c.size() } -> std::convertible_to<std::size_t>;
};

// Use concept — constrained template
template<Numeric T>
T add(T a, T b) { return a + b; }

// Shorthand (abbreviated function templates)
auto multiply(Numeric auto a, Numeric auto b) { return a * b; }

// requires clause
template<typename T>
    requires std::copyable<T> && std::equality_comparable<T>
class Cache { /* ... */ };
```

## Ranges (C++20/23)

```cpp
#include <ranges>
#include <algorithm>
#include <vector>

namespace rv = std::ranges::views;

std::vector<int> nums = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

// Pipeline — lazy, composable
auto result = nums
    | rv::filter([](int n) { return n % 2 == 0; })   // 2, 4, 6, 8, 10
    | rv::transform([](int n) { return n * n; })       // 4, 16, 36, 64, 100
    | rv::take(3);                                      // 4, 16, 36

// Range algorithms (namespace std::ranges)
std::ranges::sort(nums);
auto it = std::ranges::find(nums, 5);
bool all_pos = std::ranges::all_of(nums, [](int n) { return n > 0; });

// C++23: zip, enumerate, chunk, slide, cartesian_product
for (auto [i, val] : rv::enumerate(nums)) {
    std::println("[{}] = {}", i, val);
}

auto pairs = rv::zip(names, scores);  // zip two ranges together
auto chunks = nums | rv::chunk(3);    // [[1,2,3], [4,5,6], [7,8,9], [10]]
```

## Smart Pointers

```cpp
#include <memory>

// unique_ptr — exclusive ownership (zero overhead)
auto ptr = std::make_unique<Widget>(42);
auto arr = std::make_unique<int[]>(10);   // array
ptr->doSomething();
// auto ptr2 = ptr;                       // ❌ compile error
auto ptr2 = std::move(ptr);              // ✅ transfer ownership

// shared_ptr — shared ownership (reference counted)
auto shared = std::make_shared<Widget>(42);
auto copy = shared;                       // refcount++
std::println("count: {}", shared.use_count());  // 2

// weak_ptr — non-owning observer (breaks cycles)
std::weak_ptr<Widget> weak = shared;
if (auto locked = weak.lock()) {
    locked->doSomething();
}
```

## Containers (Modern)

```cpp
#include <vector>
#include <unordered_map>
#include <string>
#include <flat_map>    // C++23

// vector — dynamic array
std::vector<int> v = {1, 2, 3};
v.push_back(4);
v.emplace_back(5);              // construct in-place
v.reserve(100);                 // pre-allocate

// unordered_map — hash map (O(1) average)
std::unordered_map<std::string, int> scores;
scores["Alice"] = 95;
scores.insert_or_assign("Bob", 88);
scores.try_emplace("Charlie", 92);   // only insert if not exists

if (auto it = scores.find("Alice"); it != scores.end()) {
    std::println("{}: {}", it->first, it->second);
}

// flat_map (C++23) — sorted vector, cache-friendly
std::flat_map<std::string, int> fm = {{"a", 1}, {"b", 2}};
fm.insert_or_assign("c", 3);
// Better cache performance than std::map for small-to-medium sets
```

## Strings & String Views

```cpp
#include <string>
#include <string_view>
#include <format>

// string_view — non-owning, no allocation
void process(std::string_view sv) {
    std::println("Length: {}", sv.size());
    auto sub = sv.substr(0, 5);       // no copy
    bool has = sv.contains("hello");  // C++23
    bool starts = sv.starts_with("http");  // C++20
    bool ends = sv.ends_with(".cpp");      // C++20
}

// std::format (C++20) — type-safe formatting
std::string msg = std::format("Hello, {}! Score: {:.1f}", name, 95.5);
```

## Coroutines (C++20)

```cpp
#include <coroutine>
#include <generator>  // C++23

// Generator — lazy sequence (C++23 std::generator)
std::generator<int> fibonacci() {
    int a = 0, b = 1;
    while (true) {
        co_yield a;
        auto tmp = a;
        a = b;
        b = tmp + b;
    }
}

// Usage
for (int n : fibonacci() | std::views::take(10)) {
    std::println("{}", n);  // 0, 1, 1, 2, 3, 5, 8, 13, 21, 34
}
```

## Modules (C++20)

```cpp
// math.cppm — module interface unit
export module math;

export int add(int a, int b) { return a + b; }
export int multiply(int a, int b) { return a * b; }

// Implementation partition
module math:impl;

// main.cpp — import module
import math;
import <print>;

int main() {
    std::println("{}", add(2, 3));  // 5
}
```

## Multithreading

```cpp
#include <thread>
#include <mutex>
#include <future>
#include <atomic>
#include <latch>        // C++20
#include <barrier>      // C++20
#include <semaphore>    // C++20
#include <jthread>      // C++20

// jthread — auto-joining, supports stop_token
std::jthread worker([](std::stop_token st) {
    while (!st.stop_requested()) {
        // do work
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
});
worker.request_stop();  // cooperative cancellation

// async/future
auto future = std::async(std::launch::async, [] {
    return heavy_computation();
});
int result = future.get();  // blocks until ready

// mutex + scoped_lock
std::mutex mtx;
{
    std::scoped_lock lock(mtx);  // RAII, unlocks on scope exit
    shared_data.push_back(42);
}

// atomic
std::atomic<int> counter{0};
counter.fetch_add(1, std::memory_order_relaxed);

// latch — one-time barrier
std::latch done(3);
// Each thread: done.count_down(); 
done.wait();  // blocks until count reaches 0

// semaphore
std::counting_semaphore<5> pool(5);  // max 5 concurrent
pool.acquire();
// ... use resource
pool.release();
```

## RAII & Move Semantics

```cpp
// Move semantics — transfer resources, avoid copies
class Buffer {
    std::unique_ptr<char[]> data_;
    size_t size_;
public:
    Buffer(size_t n) : data_(std::make_unique<char[]>(n)), size_(n) {}

    // Move constructor
    Buffer(Buffer&& other) noexcept
        : data_(std::move(other.data_)), size_(other.size_) {
        other.size_ = 0;
    }

    // Move assignment
    Buffer& operator=(Buffer&& other) noexcept {
        data_ = std::move(other.data_);
        size_ = other.size_;
        other.size_ = 0;
        return *this;
    }

    // Rule of Five: if you define one special member, define all five
    // (or = default / = delete)
    ~Buffer() = default;
    Buffer(const Buffer&) = delete;            // no copy
    Buffer& operator=(const Buffer&) = delete; // no copy assign
};
```

## Lambda Expressions

```cpp
// Basic
auto add = [](int a, int b) { return a + b; };

// Capture
int x = 10;
auto by_val = [x](int y) { return x + y; };     // copy x
auto by_ref = [&x](int y) { x += y; };          // reference x
auto all_val = [=]() { return x; };              // copy all
auto all_ref = [&]() { x++; };                   // reference all

// Generic lambda (C++14)
auto print = [](auto&& val) { std::println("{}", val); };

// Lambda with template (C++20)
auto add_typed = []<typename T>(T a, T b) { return a + b; };

// Immediately invoked
auto result = [&]() {
    if (condition) return computeA();
    return computeB();
}();

// Mutable (modify captured-by-value)
auto counter = [n = 0]() mutable { return ++n; };
```

## Compile-Time Programming

```cpp
// constexpr — compile-time evaluation
constexpr int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
static_assert(factorial(5) == 120);

// consteval — MUST be evaluated at compile-time (C++20)
consteval int square(int n) { return n * n; }
constexpr int s = square(5);   // ✅ compile-time
// int x = 5; square(x);       // ❌ compile error

// constexpr if (C++17) — compile-time branching
template<typename T>
auto to_string(T val) {
    if constexpr (std::is_same_v<T, std::string>) {
        return val;
    } else if constexpr (std::is_arithmetic_v<T>) {
        return std::to_string(val);
    } else {
        return std::string("unknown");
    }
}

// constinit (C++20) — ensure static init at compile-time
constinit int global_val = 42;  // no dynamic init order issues
```

## Gotchas & Best Practices

⚠️ **Prefer `std::expected` over exceptions** (C++23): For expected failure paths, use `std::expected<T, E>`.

⚠️ **Use `std::print/println`** (C++23): Replaces `printf` AND `cout`. Type-safe, fast, Unicode.

⚠️ **Use `std::string_view`**: For function params that read strings. Zero-copy, no allocation.

⚠️ **`auto` everywhere**: Return types, lambda params, range declarations. Let compiler deduce.

⚠️ **Smart pointers**: `unique_ptr` (default), `shared_ptr` (shared ownership), `weak_ptr` (cycles). Never use raw `new`/`delete`.

⚠️ **Rule of Five/Zero**: If you define destructor/copy/move, define all 5. Otherwise, `= default` all.

⚠️ **`std::move` doesn't move**: It casts to rvalue reference. Actual move happens in constructor/assignment.

⚠️ **`constexpr` vs `consteval`**: `constexpr` = CAN be compile-time. `consteval` = MUST be compile-time.

⚠️ **Modules vs Headers**: Modules compile faster but need build system support (CMake 3.28+, MSVC).

⚠️ **Ranges are lazy**: Views don't evaluate until iterated. Use `std::ranges::to<vector>()` (C++23) to materialize.

⚠️ **`jthread` > `thread`**: Auto-joins on destruction, supports `stop_token` for cancellation.

⚠️ **Structured bindings** (C++17): `auto [x, y] = pair;` — works with tuples, arrays, structs.

⚠️ **`std::format` > `stringstream`**: Type-safe formatting. `std::println` for output.

⚠️ **Compiler support**: GCC 14+, Clang 18+, MSVC 19.38+ for full C++23. C++26 partial.
