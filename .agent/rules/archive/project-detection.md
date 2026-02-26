---
trigger: always_on
version: "4.5"
data_file: "data/build-systems.yaml"
---

# 🔍 Project Detection Rule

> 🌍 **Language / Ngôn ngữ**: English (default) | [Tiếng Việt](#tiếng-việt)
> 📦 **Data**: See `data/build-systems.yaml` for detection patterns
> 🎯 **Token Budget**: 2,400-4,900 tokens (vs 20,000-50,000+ naive scan)

## Enforcement Level: ALWAYS

---

## 🎯 PURPOSE

Agent MUST understand project structure BEFORE implementation:

- Identify IDE/build system
- Detect frameworks/libraries
- Find test framework
- Generate correct build commands

---

## 📊 5-PHASE HIERARCHICAL SCANNING

### Phase 1: Root Discovery (500-1,000 tokens)

```yaml
priority: 1
depth: 0 # Root only
max_files: 20
stop_after: 1 # Stop after first match

patterns:
  visual_studio: ["*.sln", "*.slnx", "*.csproj", "*.vcxproj"]
  cmake: ["CMakeLists.txt", "CMakePresets.json"]
  node: ["package.json"]
  java: ["pom.xml", "build.gradle", "build.gradle.kts"]
  rust: ["Cargo.toml"]
  go: ["go.mod"]
  python: ["pyproject.toml", "setup.py", "requirements.txt"]
  make: ["Makefile", "GNUmakefile"]
```

### Phase 2: Build Config (200-500 tokens)

```yaml
priority: 2
conditional: "IF Phase 1 needs clarification"

files:
  cmake: ["CMakeCache.txt", "build.ninja"]
  gradle: ["gradle-wrapper.properties"]
  dotnet: ["Directory.Build.props", "global.json"]
```

### Phase 3: Dependencies (1,000-2,000 tokens)

```yaml
priority: 1
max_items: 50 # Limit to prevent token explosion

parsers:
  csproj:
    xpath: "//PackageReference"
    attributes: ["Include", "Version"]

  package_json:
    keys: ["dependencies", "devDependencies"]

  requirements_txt:
    max_lines: 50
    skip_comments: true

  cargo_toml:
    section: "[dependencies]"
```

### Phase 4: Source Sampling (500-1,000 tokens)

```yaml
priority: 3
conditional: "IF framework unclear after Phase 3"

strategy:
  sample_size: 5 # Random files
  lines_per_file: 20 # First 20 lines only
  extract_imports: true
```

### Phase 5: Test Detection (200-400 tokens)

```yaml
priority: 2
max_files: 3

patterns:
  python: ["test_*.py", "*_test.py"]
  csharp: ["*Test.cs", "*Tests.cs"]
  cpp: ["*_test.cpp", "*_test.cc"]
  java: ["*Test.java", "*Tests.java"]
  js: ["*.test.js", "*.spec.ts"]

folders:
  - "test/", "tests/", "__tests__/", "spec/"
```

---

## 🔎 BUILD SYSTEM DETECTION

### Visual Studio Ecosystem (2026 Updates)

| Indicator                                    | Meaning                                                |
| -------------------------------------------- | ------------------------------------------------------ |
| `*.slnx`                                     | **NEW** VS2026 XML-based solution (dotnet sln migrate) |
| `*.sln`                                      | Legacy solution file (text-based)                      |
| `PlatformToolset=v145`                       | **VS2026** (MSVC 14.50)                                |
| `PlatformToolset=v143`                       | VS2022                                                 |
| `PlatformToolset=v142`                       | VS2019                                                 |
| `Sdk="Microsoft.NET.Sdk"`                    | SDK-style (modern) C#                                  |
| `<TargetFramework>net10.0</TargetFramework>` | **.NET 10 LTS**                                        |
| `<TargetFramework>net9.0</TargetFramework>`  | .NET 9                                                 |
| `ToolsVersion="4.0"`                         | Legacy C#                                              |

### CMake 4.0 (2025-2026)

| Indicator                             | Meaning                          |
| ------------------------------------- | -------------------------------- |
| `cmake_minimum_required(VERSION 4.0)` | **CMake 4.0** (breaking changes) |
| `cmake_minimum_required(VERSION 3.x)` | CMake 3.x                        |
| `find_package(Qt6)`                   | Qt 6 framework                   |
| `find_package(GTest)`                 | Google Test                      |
| `CMakePresets.json`                   | Modern config sharing            |

### Node.js / JavaScript Runtimes (2025-2026)

| Indicator          | Meaning                           |
| ------------------ | --------------------------------- |
| `package.json`     | Node.js / npm / Yarn / pnpm       |
| `bun.lockb`        | **Bun** runtime (binary lockfile) |
| `deno.json`        | **Deno 2** runtime                |
| `"react":`         | React framework                   |
| `"vue":`           | Vue.js                            |
| `"@angular/core":` | Angular                           |
| `"jest":`          | Jest test framework               |
| `yarn.lock`        | Yarn package manager              |
| `pnpm-lock.yaml`   | pnpm                              |

---

## 📋 OUTPUT FORMAT

Agent MUST output detection results:

```yaml
# Project Detection Result
project:
  name: "MyProject"
  type: "Visual Studio Solution"
  confidence: 95%

ide:
  name: "Visual Studio 2022"
  evidence: "PlatformToolset v143"

language:
  primary: "C++"
  version: "C++20"
  secondary: ["C#"]

build_system:
  name: "MSBuild"
  command: "msbuild MyProject.sln /p:Configuration=Release"

frameworks:
  - name: "Qt"
    version: "6.5"
    confidence: 100%

test_framework:
  name: "Google Test"
  command: "ctest --output-on-failure"
```

---

## 🛠️ BUILD COMMANDS TEMPLATE

### Visual Studio / MSBuild

```bash
# Build
msbuild {solution}.sln /p:Configuration={config} /p:Platform={platform}

# Clean
msbuild {solution}.sln /t:Clean

# Defaults: config=Release, platform=x64
```

### CMake

```bash
# Configure
cmake -B build -DCMAKE_BUILD_TYPE={config}

# Build
cmake --build build --config {config} -j{jobs}

# Test
ctest --test-dir build --output-on-failure
```

### npm/Node.js

```bash
npm install
npm run build
npm test
```

### .NET Core

```bash
dotnet restore
dotnet build --configuration Release
dotnet test
```

---

## ⚠️ SPECIAL CASES

### Monorepo Detection

```yaml
indicators:
  npm_workspaces: 'package.json contains "workspaces"'
  lerna: "lerna.json exists"
  vs_solution: ".sln has multiple <Project> entries"
  nx: "nx.json exists"
  turborepo: "turbo.json exists"
```

### Multi-Language Projects

```yaml
patterns:
  cpp_python: "CMakeLists.txt + setup.py"
  csharp_typescript: "*.csproj + package.json"
  java_kotlin: ".java + .kt files"
```

---

## 📊 TOKEN OPTIMIZATION

| Scan Type        | Token Cost      | Accuracy   |
| ---------------- | --------------- | ---------- |
| Naive full scan  | 20,000-50,000+  | 100%       |
| **5-Phase scan** | **2,400-4,900** | **92%+**   |
| Savings          | **85-90%**      | Minor loss |

### Cost Breakdown

| Phase     | Tokens      | Stop Condition          |
| --------- | ----------- | ----------------------- |
| 1. Root   | 500-1,000   | After first match       |
| 2. Config | 200-500     | Skip if Phase 1 clear   |
| 3. Deps   | 1,000-2,000 | First 50 items          |
| 4. Source | 500-1,000   | Skip if framework known |
| 5. Tests  | 200-400     | After 3 files           |

---

# Tiếng Việt

> 🇻🇳 Phiên bản Tiếng Việt

## Mô Tả

Agent PHẢI phát hiện project structure TRƯỚC khi implementation.

## 5 Giai Đoạn Scan

1. **Root Discovery** — Tìm build file (\*.sln, CMakeLists.txt, package.json)
2. **Build Config** — Đọc config chi tiết (nếu cần)
3. **Dependencies** — Parse dependencies (giới hạn 50 items)
4. **Source Sampling** — Sample code nếu framework chưa rõ
5. **Test Detection** — Tìm test framework

## Format Output Bắt Buộc

```yaml
project:
  name: "MyProject"
  type: "CMake Project"
  confidence: 95%

build_command: "cmake --build build --config Release"
test_command: "ctest --output-on-failure"
```

## Token Budget

- 5-Phase scan: 2,400-4,900 tokens
- Naive full scan: 20,000-50,000+ tokens
- Tiết kiệm: 85-90%

---
