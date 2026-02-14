## 🔧 Modern C++ Features

### C++20: Concepts

```cpp
#include <concepts>

// Define concept
template<typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

// Use concept
template<Numeric T>
T add(T a, T b) {
    return a + b;
}

// Requires clause
template<typename T>
requires std::copyable<T>
void process(T value) {
    // ...
}
```

### C++20: Ranges

```cpp
#include <ranges>
#include <vector>
#include <algorithm>

std::vector<int> nums{1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

// 📦 Ranges with views (lazy evaluation)
auto result = nums
    | std::views::filter([](int n) { return n % 2 == 0; })
    | std::views::transform([](int n) { return n * 2; })
    | std::views::take(3);

for (int n : result) {
    std::cout << n << ' ';  // 4 8 12
}

// 📦 Range algorithms
std::ranges::sort(nums);
auto found = std::ranges::find(nums, 5);
bool all_positive = std::ranges::all_of(nums, [](int n) { return n > 0; });
```

### C++20: std::format

```cpp
#include <format>
#include <string>

std::string msg = std::format("User {}: {}", id, name);
std::string formatted = std::format("{:0>8}", 42);  // "00000042"
std::string hex = std::format("{:#x}", 255);        // "0xff"
```

### C++23: std::expected

```cpp
#include <expected>
#include <string>

enum class Error { NotFound, Invalid };

std::expected<User, Error> findUser(int id) {
    if (auto it = users.find(id); it != users.end()) {
        return it->second;
    }
    return std::unexpected(Error::NotFound);
}

// Usage
auto result = findUser(42);
if (result) {
    std::cout << result->name;
} else {
    std::cerr << "Error: " << static_cast<int>(result.error());
}

// Or with transform
result.transform([](const User& u) { return u.name; })
      .or_else([](Error e) { return "Unknown"; });
```

### C++23: std::print

```cpp
#include <print>

// Type-safe printf replacement
std::print("Hello, {}!\n", name);
std::println("User {}: score = {}", id, score);  // with newline

// Formatted output
std::print("{:>10} | {:>5}\n", "Name", "Score");
```

### C++23: Modules

```cpp
// mymodule.cppm
export module mymodule;

export class Widget {
public:
    void process();
};

export void helper();

// main.cpp
import mymodule;   // Import custom module
import std;        // Import entire standard library!

int main() {
    Widget w;
    w.process();
}
```

---
