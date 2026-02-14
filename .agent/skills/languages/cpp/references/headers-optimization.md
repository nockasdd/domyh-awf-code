## ⚡ Header Optimization (CRITICAL Best Practice)

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

| Scenario                      | Forward Decl OK?       | Notes                         |
| ----------------------------- | ---------------------- | ----------------------------- |
| Pointer to class (`T*`)       | ✅ Yes                | Size known (pointer size)     |
| Reference to class (`T&`)     | ✅ Yes                | Size known                    |
| `std::unique_ptr<T>`          | ⚠️ Partial          | Need full type for destructor |
| `std::shared_ptr<T>`          | ✅ Yes                | Incomplete type allowed       |
| Class member (`T member`)     | ❌ No                  | Size required                 |
| Inheritance (`class A : B`)   | ❌ No                  | Full type required            |
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
