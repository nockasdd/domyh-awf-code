---
name: cpp
detect: ["CMakeLists.txt", "*.cpp", "*.cxx", "*.cc", "*.hpp", "*.hxx", "*.h"]
version: "6.2.6"
category: language
tier: 1
---

# C++ Development Patterns — DOMYH Awesome Code

> Modern C++ (C++20/23/26) patterns — NOT Pure C

## � Language Detection

```yaml
cpp_indicators:  # C++ skill activates
  - "#include <iostream>"
  - "#include <vector>"
  - "#include <string>"
  - "#include <memory>"
  - "std::"
  - "class "
  - "namespace "
  - "template<"
  - "auto "
  - "new/delete operators"
  - ".cpp, .cxx, .cc, .hpp files"

c_only_indicators:  # Switch to C skill
  - ".c files only"
  - "#include <stdio.h>" (without C++ headers)
  - "No std::, class, namespace, template"
  - "malloc/free only"
```

---

## 📊 C++ Standards Comparison

| Standard  | Year | Key Features                                                   |
| --------- | ---- | -------------------------------------------------------------- |
| **C++17** | 2017 | structured bindings, std::optional, std::variant, if constexpr |
| **C++20** | 2020 | concepts, ranges, coroutines, modules, std::format, std::span  |
| **C++23** | 2024 | std::expected, std::print, import std, enhanced ranges         |
| **C++26** | 2026 | reflection, contracts, std::execution, constexpr containers    |

---

## 🛠️ IDE & Toolchain Support (2025-2026)

### Visual Studio 2026

```yaml
msvc_version: v14.50 (19.50)
cmake: 4.1.1 (built-in)
features:
  - C++23 full conformance
  - C++26 partial support
  - CMake Presets support
  - vcpkg integrated
  - GitHub Copilot integration
```

### CLion 2025.3+

```yaml
toolchains:
  - MSVC 14.50 (VS2026)
  - GCC 14+
  - Clang 18+
features:
  - CMake Presets (v2-10)
  - vcpkg integration
  - Conan support
  - Nova engine (improved parsing)
```

### VS Code

```yaml
extensions:
  - C/C++ (Microsoft)
  - CMake Tools
  - clangd (alternative language server)
features:
  - CMakePresets.json support
  - vcpkg/Conan integration
  - Remote development
```

---

## � Header Optimization (CRITICAL Best Practice)

> **GOAL**: Minimize includes in `.h` files → Faster compilation, less coupling

### 1. Forward Declarations (Prefer over #include in headers)

```cpp
// ❌ BAD: Heavy includes in header file
// user.h
#include <string>       // Full include
#include <vector>       // Full include
#include <memory>       // Full include
#include "database.h"   // Heavy include!
#include "logger.h"     // Heavy include!

class User {
    std::unique_ptr<Database> db_;  // Requires full Database type
    std::string name_;
    std::vector<int> orders_;
};
```

```cpp
// ✅ GOOD: Forward declarations + minimal includes
// user.h
#include <string>       // Required (used directly)
#include <memory>       // Required for unique_ptr

class Database;         // Forward declaration only!
class Logger;           // Forward declaration only!

class User {
    std::unique_ptr<Database> db_;  // OK with incomplete type
    std::string name_;
    std::vector<int>* orders_;      // Pointer = OK with forward decl
};
```

```cpp
// user.cpp - Include the full headers here
#include "user.h"      // Own header FIRST
#include <vector>      // Now we need full definition
#include "database.h"  // Full include in implementation
#include "logger.h"    // Full include in implementation
```

### 2. When Forward Declaration Works

| Scenario                      | Forward Decl OK?    | Notes                         |
| ----------------------------- | ------------------- | ----------------------------- |
| Pointer to class (`T*`)       | ✅ Yes              | Size known (pointer size)     |
| Reference to class (`T&`)     | ✅ Yes              | Size known                    |
| `std::unique_ptr<T>`          | ⚠️ Partial          | Need full type for destructor |
| `std::shared_ptr<T>`          | ✅ Yes              | Incomplete type allowed       |
| Class member (`T member`)     | ❌ No               | Size required                 |
| Inheritance (`class A : B`)   | ❌ No               | Full type required            |
| Template parameter            | ⚠️ Depends          | Often needs full type         |
| Function parameter (`f(T x)`) | ⚠️ Declaration only | Implementation needs full     |
| Function return (`T f()`)     | ⚠️ Declaration only | Implementation needs full     |

### 3. PIMPL Idiom (Pointer to Implementation)

> **Purpose**: Hide implementation, reduce compilation dependencies, ABI stability

```cpp
// widget.h - PUBLIC HEADER (minimal includes!)
#pragma once
#include <memory>   // Only for unique_ptr

class Widget {
public:
    Widget();
    ~Widget();  // Must be declared (impl needs complete type)

    // Move operations
    Widget(Widget&& other) noexcept;
    Widget& operator=(Widget&& other) noexcept;

    // Deleted copy (or implement in .cpp)
    Widget(const Widget&) = delete;
    Widget& operator=(const Widget&) = delete;

    void doSomething();
    int getValue() const;

private:
    struct Impl;                    // Forward declaration
    std::unique_ptr<Impl> pimpl_;   // Opaque pointer
};
```

```cpp
// widget.cpp - IMPLEMENTATION (heavy includes here)
#include "widget.h"
#include <string>               // Heavy STL
#include <vector>               // Heavy STL
#include <unordered_map>        // Heavy STL
#include "database.h"           // Heavy dependency
#include "network_client.h"     // Heavy dependency
#include <windows.h>            // Platform header - ONLY in .cpp!

struct Widget::Impl {
    std::string name;
    std::vector<int> data;
    std::unordered_map<int, std::string> cache;
    std::unique_ptr<Database> db;
    NetworkClient client;
    HANDLE winHandle;  // Windows-specific - hidden from header

    void internalHelper() { /* ... */ }
};

Widget::Widget() : pimpl_(std::make_unique<Impl>()) {}

Widget::~Widget() = default;  // Must be in .cpp where Impl is complete

Widget::Widget(Widget&& other) noexcept = default;
Widget& Widget::operator=(Widget&& other) noexcept = default;

void Widget::doSomething() {
    pimpl_->internalHelper();
}

int Widget::getValue() const {
    return static_cast<int>(pimpl_->data.size());
}
```

### 4. Dangerous Headers (NEVER include in .h files)

| Header                  | Problem                              | Solution                |
| ----------------------- | ------------------------------------ | ----------------------- |
| `<windows.h>`           | 15k+ lines, macros pollute namespace | PIMPL or forward decl   |
| `<winsock2.h>`          | Heavy, conflicts                     | PIMPL only in .cpp      |
| `<algorithm>`           | 10k+ lines                           | Forward decl iterators  |
| `<iostream>`            | Heavy, static init                   | Forward declare streams |
| `<regex>`               | Extremely heavy                      | PIMPL                   |
| `<thread>`              | Platform headers                     | PIMPL                   |
| `<filesystem>`          | Heavy                                | PIMPL                   |
| Project's large headers | Compilation cascade                  | Forward decl            |

### 5. Include-What-You-Use (IWYU)

```bash
# Run IWYU on single file
include-what-you-use -Xiwyu --mapping_file=iwyu.imp myfile.cpp

# CMake integration
set(CMAKE_CXX_INCLUDE_WHAT_YOU_USE include-what-you-use)

# IWYU pragmas
#include "heavy.h"  // IWYU pragma: keep (prevent removal)
// IWYU pragma: no_include "deprecated.h" (prevent suggestion)
```

### 6. Precompiled Headers (PCH)

```cmake
# CMakeLists.txt - Modern PCH (CMake 3.16+)
target_precompile_headers(myapp PRIVATE
    # STL headers (stable, include once)
    <vector>
    <string>
    <memory>
    <algorithm>
    <unordered_map>

    # Third-party (stable)
    <fmt/core.h>
    <spdlog/spdlog.h>

    # Project stable headers
    "common/types.h"
    "common/constants.h"
)
```

### 7. C++20 Modules (Future-Proof)

```cpp
// math.cppm - Module interface
export module math;

export int add(int a, int b);
export int multiply(int a, int b);

// math.cpp - Module implementation
module math;

int add(int a, int b) { return a + b; }
int multiply(int a, int b) { return a * b; }

// main.cpp - Using module
import math;     // Fast import, no re-parsing!
import std;      // Import entire std library (C++23)

int main() {
    return add(1, 2);
}
```

### 8. Header Include Order (Best Practice)

```cpp
// myclass.cpp

// 1. OWN HEADER FIRST (validates self-containment)
#include "myclass.h"

// 2. C system headers
#include <cstdio>
#include <cstdlib>

// 3. C++ STL headers
#include <string>
#include <vector>
#include <algorithm>

// 4. Third-party library headers
#include <fmt/core.h>
#include <spdlog/spdlog.h>
#include <nlohmann/json.hpp>

// 5. Project headers (alphabetical)
#include "database/connection.h"
#include "utils/string_utils.h"
```

---

## �📦 Build & Package Management

### CMake (Modern)

```cmake
cmake_minimum_required(VERSION 3.25)
project(MyApp VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Find packages
find_package(fmt REQUIRED)
find_package(spdlog REQUIRED)

add_executable(myapp
    src/main.cpp
    src/utils.cpp
)

target_link_libraries(myapp PRIVATE
    fmt::fmt
    spdlog::spdlog
)

# Include directories
target_include_directories(myapp PRIVATE
    ${CMAKE_SOURCE_DIR}/include
)
```

### CMakePresets.json

```json
{
  "version": 6,
  "configurePresets": [
    {
      "name": "dev",
      "displayName": "Development",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/${presetName}",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Debug",
        "CMAKE_CXX_STANDARD": "23"
      }
    },
    {
      "name": "release",
      "displayName": "Release",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/${presetName}",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release"
      }
    }
  ],
  "buildPresets": [
    { "name": "dev", "configurePreset": "dev" },
    { "name": "release", "configurePreset": "release" }
  ]
}
```

### vcpkg

```bash
# Install packages
vcpkg install fmt spdlog nlohmann-json

# CMake integration
cmake -B build -S . -DCMAKE_TOOLCHAIN_FILE=$VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake
```

### Conan 2.0

```ini
# conanfile.txt
[requires]
fmt/10.2.1
spdlog/1.13.0

[generators]
CMakeDeps
CMakeToolchain

[layout]
cmake_layout
```

---

## 📚 STL Containers Reference

### Sequence Containers

| Container              | Access | Insert/Delete      | Use Case            |
| ---------------------- | ------ | ------------------ | ------------------- |
| `std::vector<T>`       | O(1)   | O(1) amortized end | Dynamic array       |
| `std::deque<T>`        | O(1)   | O(1) both ends     | Double-ended queue  |
| `std::list<T>`         | O(n)   | O(1) anywhere      | Frequent insertions |
| `std::array<T,N>`      | O(1)   | Fixed              | Compile-time size   |
| `std::forward_list<T>` | O(n)   | O(1)               | Singly linked       |

### Associative Containers

| Container                 | Access   | Insert   | Ordered | Use Case         |
| ------------------------- | -------- | -------- | ------- | ---------------- |
| `std::map<K,V>`           | O(log n) | O(log n) | Yes     | Key-value sorted |
| `std::set<T>`             | O(log n) | O(log n) | Yes     | Unique sorted    |
| `std::multimap<K,V>`      | O(log n) | O(log n) | Yes     | Multiple values  |
| `std::unordered_map<K,V>` | O(1) avg | O(1) avg | No      | Fast lookups     |
| `std::unordered_set<T>`   | O(1) avg | O(1) avg | No      | Fast membership  |

### Container Usage

```cpp
#include <vector>
#include <map>
#include <unordered_map>
#include <array>

// ✅ Vector with reserve
std::vector<int> nums;
nums.reserve(1000);  // Pre-allocate
nums.push_back(42);
nums.emplace_back(100);

// ✅ Range-based for
for (const auto& num : nums) {
    std::cout << num << '\n';
}

// ✅ Map with structured bindings
std::map<std::string, int> scores{{"Alice", 100}, {"Bob", 85}};
for (const auto& [name, score] : scores) {
    std::cout << name << ": " << score << '\n';
}

// ✅ Unordered map for O(1) lookups
std::unordered_map<int, std::string> idToName;
idToName[1] = "John";
if (auto it = idToName.find(1); it != idToName.end()) {
    std::cout << it->second << '\n';
}

// ✅ Fixed-size array
std::array<int, 5> arr{1, 2, 3, 4, 5};
```

---

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

// ✅ Ranges with views (lazy evaluation)
auto result = nums
    | std::views::filter([](int n) { return n % 2 == 0; })
    | std::views::transform([](int n) { return n * 2; })
    | std::views::take(3);

for (int n : result) {
    std::cout << n << ' ';  // 4 8 12
}

// ✅ Range algorithms
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

## 🧠 Memory Management

### Smart Pointers

```cpp
#include <memory>

// ✅ unique_ptr (exclusive ownership)
auto widget = std::make_unique<Widget>(config);

// ✅ shared_ptr (shared ownership)
auto resource = std::make_shared<Resource>();
auto copy = resource;  // Reference count = 2

// ✅ weak_ptr (non-owning reference)
std::weak_ptr<Resource> weak = resource;
if (auto locked = weak.lock()) {
    // Use locked safely
}

// ✅ Custom deleter
auto file = std::unique_ptr<FILE, decltype(&fclose)>(
    fopen("data.txt", "r"), fclose
);
```

### Move Semantics

```cpp
class Buffer {
    std::unique_ptr<uint8_t[]> data_;
    size_t size_;

public:
    // Move constructor
    Buffer(Buffer&& other) noexcept
        : data_(std::move(other.data_))
        , size_(std::exchange(other.size_, 0)) {}

    // Move assignment
    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            data_ = std::move(other.data_);
            size_ = std::exchange(other.size_, 0);
        }
        return *this;
    }
};
```

---

## 🔄 Concurrency

### std::jthread (C++20)

```cpp
#include <thread>
#include <stop_token>

std::jthread worker([](std::stop_token stoken) {
    while (!stoken.stop_requested()) {
        // Do work
    }
});

// Automatic join on destruction
// Can request stop: worker.request_stop();
```

### std::atomic

```cpp
#include <atomic>

std::atomic<int> counter{0};

void increment() {
    counter.fetch_add(1, std::memory_order_relaxed);
}

int get() {
    return counter.load(std::memory_order_acquire);
}
```

---

## ⚠️ Platform-Specific Headers (CRITICAL)

### Windows Headers Conflicts

> **CRITICAL**: Windows headers have many conflicts. Follow this order exactly!

#### 1. Include Order (winsock2.h BEFORE windows.h)

```cpp
// ✅ CORRECT ORDER - winsock2.h MUST come before windows.h
#define WIN32_LEAN_AND_MEAN  // Exclude rarely-used stuff
#define NOMINMAX             // Prevent min/max macros
#define STRICT               // Enable strict type checking
#define UNICODE              // Use Unicode APIs
#define _UNICODE

#include <winsock2.h>        // 1st - Winsock 2.0
#include <ws2tcpip.h>        // 2nd - TCP/IP extensions
#include <windows.h>         // 3rd - Windows API

// ❌ WRONG - causes redefinition errors!
#include <windows.h>         // includes winsock.h (1.1)
#include <winsock2.h>        // conflicts with winsock.h!
```

#### 2. Essential Macros (Define BEFORE any Windows includes)

```cpp
// pch.h or stdafx.h - Put at TOP of precompiled header
#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN  // Exclude: Cryptography, DDE, RPC, Shell, Winsock 1.1
#endif

#ifndef NOMINMAX
#define NOMINMAX             // Prevent Windows min/max macros
#endif                       // Allows std::min, std::max to work

#ifndef STRICT
#define STRICT               // Strict type checking for handles
#endif

// Now safe to include Windows headers
#include <windows.h>
```

#### 3. min/max Macro Conflicts

```cpp
// ❌ Problem: Windows defines min/max as macros
#include <windows.h>
#include <algorithm>
int x = std::min(a, b);  // ERROR: macro expansion!

// ✅ Solution 1: Use NOMINMAX (recommended)
#define NOMINMAX
#include <windows.h>
#include <algorithm>
int x = std::min(a, b);  // Works!

// ✅ Solution 2: Parentheses workaround
int x = (std::min)(a, b);  // Prevents macro expansion

// ✅ Solution 3: #undef after include
#include <windows.h>
#undef min
#undef max
#include <algorithm>
```

#### 4. WIN32_LEAN_AND_MEAN Exclusions

```cpp
// WIN32_LEAN_AND_MEAN excludes these - include manually if needed:
#define WIN32_LEAN_AND_MEAN
#include <windows.h>

// If you need these, include AFTER windows.h:
#include <shellapi.h>    // Shell API
#include <mmsystem.h>    // Multimedia
#include <wincrypt.h>    // Cryptography
#include <commdlg.h>     // Common dialogs
#include <dde.h>         // DDE
```

### Windows Headers Quick Reference

| Header         | Purpose              | Notes                         |
| -------------- | -------------------- | ----------------------------- |
| `<windows.h>`  | Core Windows API     | Always use with LEAN_AND_MEAN |
| `<winsock2.h>` | Sockets (Winsock 2)  | MUST include BEFORE windows.h |
| `<ws2tcpip.h>` | TCP/IP, getaddrinfo  | Include after winsock2.h      |
| `<windowsx.h>` | Message crackers     | Helper macros                 |
| `<commctrl.h>` | Common controls      | ListView, TreeView, etc.      |
| `<shlobj.h>`   | Shell interface      | Folder browser, etc.          |
| `<shobjidl.h>` | Shell COM interfaces | Modern file dialogs           |
| `<tchar.h>`    | TCHAR portability    | Legacy, prefer wchar_t        |

---

### Linux/POSIX Headers

#### 1. Define \_REENTRANT for Thread-Safe Functions

```cpp
// ✅ Define BEFORE any system headers
#define _REENTRANT          // Thread-safe libc functions
#define _POSIX_C_SOURCE 200809L  // POSIX.1-2008

#include <pthread.h>
#include <unistd.h>
#include <signal.h>
```

#### 2. Signal Handling with Threads (Critical)

```cpp
#include <pthread.h>
#include <signal.h>

// ✅ Block signals in worker threads, handle in dedicated thread
int main() {
    sigset_t set;
    sigemptyset(&set);
    sigaddset(&set, SIGINT);
    sigaddset(&set, SIGTERM);

    // Block signals in main thread (inherited by child threads)
    pthread_sigmask(SIG_BLOCK, &set, NULL);

    // Create worker threads (they inherit blocked signals)
    pthread_t worker;
    pthread_create(&worker, NULL, worker_func, NULL);

    // Handle signals in main thread with sigwait
    int sig;
    while (sigwait(&set, &sig) == 0) {
        if (sig == SIGINT || sig == SIGTERM) {
            // Clean shutdown
            break;
        }
    }

    pthread_join(worker, NULL);
    return 0;
}

// ❌ AVOID: Signal handlers with threads (race conditions!)
// Use sigwait() or signalfd() instead
```

#### 3. Common POSIX Headers

| Header           | Purpose          | Key Functions                       |
| ---------------- | ---------------- | ----------------------------------- |
| `<unistd.h>`     | POSIX API        | read, write, close, fork, exec      |
| `<pthread.h>`    | Threads          | pthread*create, pthread_mutex*\*    |
| `<signal.h>`     | Signals          | sigaction, sigwait, pthread_sigmask |
| `<fcntl.h>`      | File control     | open, fcntl, O\_\* flags            |
| `<sys/types.h>`  | Type definitions | pid_t, size_t, ssize_t              |
| `<sys/socket.h>` | Sockets          | socket, bind, listen, accept        |
| `<netinet/in.h>` | Internet addr    | sockaddr_in, htons, ntohs           |
| `<arpa/inet.h>`  | IP conversion    | inet_pton, inet_ntop                |
| `<sys/stat.h>`   | File status      | stat, fstat, mkdir                  |
| `<sys/mman.h>`   | Memory mapping   | mmap, munmap, mprotect              |
| `<dlfcn.h>`      | Dynamic loading  | dlopen, dlsym, dlclose              |

---

### Cross-Platform Patterns

```cpp
// Platform detection
#if defined(_WIN32) || defined(_WIN64)
    #define PLATFORM_WINDOWS
#elif defined(__linux__)
    #define PLATFORM_LINUX
#elif defined(__APPLE__)
    #define PLATFORM_MACOS
#endif

// Platform-specific includes
#ifdef PLATFORM_WINDOWS
    #define WIN32_LEAN_AND_MEAN
    #define NOMINMAX
    #include <windows.h>
    #include <winsock2.h>
#else
    #include <unistd.h>
    #include <sys/socket.h>
    #include <netinet/in.h>
    #include <pthread.h>
#endif

// Sleep abstraction
inline void sleep_ms(int ms) {
#ifdef PLATFORM_WINDOWS
    Sleep(ms);
#else
    usleep(ms * 1000);
#endif
}
```

---

## 📚 Essential Libraries

| Category          | Library               | Description                               |
| ----------------- | --------------------- | ----------------------------------------- |
| **Formatting**    | fmt                   | Fast formatting (std::format predecessor) |
| **Logging**       | spdlog                | Fast async logging                        |
| **JSON**          | nlohmann/json         | Easy JSON manipulation                    |
| **JSON (fast)**   | Glaze, simdjson       | High-performance JSON                     |
| **HTTP**          | cpr, cpp-httplib      | HTTP client                               |
| **Testing**       | GoogleTest, Catch2    | Unit testing                              |
| **CLI**           | CLI11                 | Command line parsing                      |
| **Serialization** | Protobuf, Flatbuffers | Binary serialization                      |

---

## ✅ Production Checklist

### Code Quality

- [ ] C++20 minimum, C++23 preferred
- [ ] Smart pointers, no raw new/delete
- [ ] Move semantics for expensive types
- [ ] const correctness applied
- [ ] RAII for all resources

### Build

- [ ] CMake 3.25+ with presets
- [ ] vcpkg or Conan for dependencies
- [ ] Compiler warnings as errors
- [ ] Static analysis (clang-tidy)

### Testing

- [ ] GoogleTest or Catch2
- [ ] Code coverage ≥80%
- [ ] Sanitizers enabled (ASan, UBSan)

---

_DOMYH Awesome Code • C++ Development (C++20/23/26) • 2025-2026_
