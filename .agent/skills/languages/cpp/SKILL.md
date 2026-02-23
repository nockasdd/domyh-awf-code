---
name: cpp
detect: ["CMakeLists.txt", "*.cpp", "*.cxx", "*.cc", "*.hpp", "*.hxx", "*.h"]
version: "6.4.0"
category: language
tier: 1
---

# C++ Development Patterns — DOMYH Awesome Code

> Modern C++ (C++20/23/26) patterns — NOT Pure C

## 🔍 Language Detection

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

---

## 📦 Build & Package Management

### CMake (Modern)

```cmake
cmake_minimum_required(VERSION 3.25)
project(MyApp VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

find_package(fmt REQUIRED)
find_package(spdlog REQUIRED)

add_executable(myapp src/main.cpp src/utils.cpp)
target_link_libraries(myapp PRIVATE fmt::fmt spdlog::spdlog)
target_include_directories(myapp PRIVATE ${CMAKE_SOURCE_DIR}/include)
```

### CMakePresets.json

```json
{
  "version": 6,
  "configurePresets": [
    {
      "name": "dev",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/${presetName}",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Debug",
        "CMAKE_CXX_STANDARD": "23"
      }
    },
    {
      "name": "release",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/${presetName}",
      "cacheVariables": { "CMAKE_BUILD_TYPE": "Release" }
    }
  ]
}
```

### Package Managers

```bash
# vcpkg
vcpkg install fmt spdlog nlohmann-json
cmake -B build -S . -DCMAKE_TOOLCHAIN_FILE=$VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake
```

```ini
# Conan 2.0 (conanfile.txt)
[requires]
fmt/10.2.1
spdlog/1.13.0
[generators]
CMakeDeps
CMakeToolchain
```

---

## 📚 Deep-Dive References

For detailed patterns, see these reference files:

- **Header Optimization** — PIMPL, forward declarations, PCH, IWYU, C++20 modules
  → See [references/headers-optimization.md](references/headers-optimization.md)

- **STL Containers** — Sequence/Associative containers comparison, usage patterns
  → See [references/stl-containers.md](references/stl-containers.md)

- **Modern C++ Features** — C++20 Concepts, Ranges, std::format, C++23 std::expected/print
  → See [references/modern-cpp-features.md](references/modern-cpp-features.md)

- **Memory & Concurrency** — Smart pointers, move semantics, jthread, atomic
  → See [references/memory-concurrency.md](references/memory-concurrency.md)

- **Platform Headers** — Windows/Linux-specific includes, macro conflicts, cross-platform
  → See [references/platform-headers.md](references/platform-headers.md)

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
