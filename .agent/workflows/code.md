---
name: code
trigger: ["/code", "write", "implement", "viết", "create", "add"]
persona: developer
description: "💻 Write production-ready code with proper error handling, types, and documentation"
---

# 💻 /code — Code Generation Pro v3.0

> Intelligent code generation with language-specific patterns
> 📚 30+ Languages • Token-optimized • Production-ready

---

## 🔄 CODE GENERATION FLOW

```
User: /code [request]
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 1: UNDERSTAND (5s)               │
│ ▸ Parse request intent                  │
│ ▸ Identify target files                 │
│ ▸ Detect tech stack                     │
│ ▸ Load language-specific skill          │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 2: PLAN                           │
│ ▸ Break down into steps                 │
│ ▸ Identify dependencies                 │
│ ⛔ STOP if major change (>50 lines)     │
└─────────────────────────────────────────┘
    │ User confirms (if needed)
    ▼
┌─────────────────────────────────────────┐
│ PHASE 3: IMPLEMENT                      │
│ ▸ Write code following patterns         │
│ ▸ Apply language best practices         │
│ ▸ Add error handling & types            │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 4: VERIFY                         │
│ ▸ Syntax check                          │
│ ▸ Build/compile test                    │
│ ▸ Show diff evidence                    │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 5: OUTPUT                         │
│ ▸ Summary of changes                    │
│ ▸ Next steps (test, commit)             │
└─────────────────────────────────────────┘
```

---

## 📋 PHASE 1: UNDERSTAND

### Request Analysis:

```
📝 CODE REQUEST ANALYSIS

Task: [Parsed intent]
Type: [feature|bugfix|refactor|test|docs]
Scope: [new file|modify|multiple files]

Files:
├── Create: src/services/auth.ts
├── Modify: src/handlers/user.ts
└── Update: src/types/index.ts

Stack: TypeScript + Express
Skill: typescript-expert (loaded)

Complexity: [small|medium|large]
Est. lines: ~45
```

### ⛔ STOP Conditions:

- Request unclear → Ask for clarification
- Multiple interpretations → Present options
- Destructive action → Require confirmation

---

## 🌐 LANGUAGE REGISTRY (30+ Languages)

### Backend / Systems

```yaml
go:
  patterns: ["Clean Architecture", "Interface-driven"]
  style: "gofmt standard"
  error: "if err != nil { return err }"
  struct: "handlers/ services/ repositories/ models/"
  tests: "*_test.go"

rust:
  patterns: ["Ownership", "Result<T,E>"]
  style: "rustfmt"
  error: "Result<T, Error>, ? operator"
  struct: "src/lib.rs, mod.rs"
  tests: "#[test] modules"

java:
  patterns: ["Spring Boot", "Dependency Injection"]
  style: "Google Java Style"
  error: "try-catch, Optional<T>"
  struct: "src/main/java/, pom.xml"
  tests: "JUnit 5, Mockito"

kotlin:
  patterns: ["Coroutines", "DSL builders"]
  style: "ktlint"
  error: "runCatching, sealed class"
  struct: "src/main/kotlin/"
  tests: "kotest, MockK"

csharp:
  patterns: [".NET Core", "LINQ"]
  style: "dotnet format"
  error: "try-catch, nullable"
  struct: "Controllers/ Services/ Models/"
  tests: "xUnit, Moq"

cpp:
  patterns: ["RAII", "Smart pointers"]
  style: "clang-format"
  error: "exceptions, error codes"
  struct: "include/ src/ tests/"
  tests: "Google Test, Catch2"

c:
  patterns: ["Procedural", "Header guards"]
  style: "clang-format"
  error: "Error codes, errno"
  struct: "include/ src/"
  tests: "Unity, Check"
```

### Scripting / Dynamic

```yaml
python:
  patterns: ["PEP8", "Type hints"]
  style: "black, ruff"
  error: "try-except, raise"
  struct: "src/ tests/ pyproject.toml"
  tests: "pytest"

ruby:
  patterns: ["Rails conventions", "Blocks"]
  style: "rubocop"
  error: "begin-rescue"
  struct: "app/ lib/ spec/"
  tests: "RSpec, MiniTest"

php:
  patterns: ["PSR-12", "Laravel/Symfony"]
  style: "php-cs-fixer"
  error: "try-catch, exceptions"
  struct: "app/ src/ tests/"
  tests: "PHPUnit, Pest"

perl:
  patterns: ["Moose OOP", "CPAN modules"]
  style: "perltidy"
  error: "eval, die"
  struct: "lib/ t/"
  tests: "Test::More"

lua:
  patterns: ["Tables", "Metatables"]
  style: "stylua"
  error: "pcall, xpcall"
  struct: "*.lua"
  tests: "busted"
```

### JavaScript / TypeScript

```yaml
typescript:
  patterns: ["Strict types", "Generics"]
  style: "prettier + eslint"
  error: "try-catch, custom Error classes"
  struct: "src/ types/ __tests__/"
  tests: "Jest, Vitest"

nodejs:
  patterns: ["CommonJS/ESM", "Express/Fastify"]
  style: "prettier"
  error: "async/await, try-catch"
  struct: "src/ routes/ services/"
  tests: "Jest, Mocha"

react:
  patterns: ["Hooks", "Components"]
  style: "prettier + eslint"
  error: "Error Boundaries"
  struct: "src/components/ hooks/"
  tests: "React Testing Library"

nextjs:
  patterns: ["App Router", "Server Components"]
  style: "prettier"
  error: "error.tsx boundaries"
  struct: "app/ components/ lib/"
  tests: "Jest, Playwright"

vue:
  patterns: ["Composition API", "Pinia"]
  style: "prettier"
  error: "errorCaptured hook"
  struct: "src/components/ composables/"
  tests: "Vitest, Vue Testing Library"

svelte:
  patterns: ["Reactivity", "Stores"]
  style: "prettier"
  error: "handleError"
  struct: "src/lib/ routes/"
  tests: "Vitest, Playwright"

deno:
  patterns: ["URL imports", "Permissions"]
  style: "deno fmt"
  error: "try-catch, Result"
  struct: "mod.ts, deps.ts"
  tests: "Deno.test"

bun:
  patterns: ["All-in-one runtime"]
  style: "prettier"
  error: "try-catch"
  struct: "src/, bun.lockb"
  tests: "bun:test"
```

### Mobile

```yaml
swift:
  patterns: ["SwiftUI", "Combine"]
  style: "swift-format"
  error: "do-try-catch, Result"
  struct: "Sources/ Tests/"
  tests: "XCTest"

kotlin_android:
  patterns: ["Jetpack Compose", "MVVM"]
  style: "ktlint"
  error: "runCatching, sealed class"
  struct: "app/src/main/"
  tests: "JUnit, Espresso"

dart:
  patterns: ["Null safety", "Streams"]
  style: "dart format"
  error: "try-catch, Result"
  struct: "lib/ test/"
  tests: "flutter_test"

flutter:
  patterns: ["Widget composition", "BLoC"]
  style: "dart format"
  error: "try-catch, ErrorWidget"
  struct: "lib/src/ lib/widgets/"
  tests: "widget testing"

react_native:
  patterns: ["Hooks", "Native Modules"]
  style: "prettier"
  error: "Error Boundaries"
  struct: "src/ __tests__/"
  tests: "Jest, Detox"
```

### Functional

```yaml
elixir:
  patterns: ["GenServer", "Pipelines"]
  style: "mix format"
  error: "{:ok, _}, {:error, _}"
  struct: "lib/ test/"
  tests: "ExUnit"

haskell:
  patterns: ["Monads", "Type classes"]
  style: "ormolu"
  error: "Either, Maybe"
  struct: "src/ test/ app/"
  tests: "HSpec, QuickCheck"

scala:
  patterns: ["FP", "Akka"]
  style: "scalafmt"
  error: "Try, Either, Option"
  struct: "src/main/scala/"
  tests: "ScalaTest, Specs2"

clojure:
  patterns: ["Functional", "REPL-driven"]
  style: "cljfmt"
  error: "try-catch, ex-info"
  struct: "src/ test/"
  tests: "clojure.test"

fsharp:
  patterns: ["Railway-oriented"]
  style: "fantomas"
  error: "Result, Option"
  struct: "src/ tests/"
  tests: "Expecto, FsUnit"

ocaml:
  patterns: ["Functors", "Modules"]
  style: "ocamlformat"
  error: "Result, Option"
  struct: "lib/ bin/ test/"
  tests: "OUnit, Alcotest"
```

### Data / ML

```yaml
python_ml:
  patterns: ["NumPy", "PyTorch/TensorFlow"]
  style: "black, isort"
  error: "try-except"
  struct: "src/ notebooks/ models/"
  tests: "pytest"

r:
  patterns: ["Tidyverse", "Functional"]
  style: "styler"
  error: "tryCatch"
  struct: "R/ tests/"
  tests: "testthat"

julia:
  patterns: ["Multiple dispatch", "Broadcasting"]
  style: "JuliaFormatter"
  error: "try-catch"
  struct: "src/ test/"
  tests: "@testset"
```

### Infrastructure

```yaml
terraform:
  patterns: ["Modules", "State"]
  style: "terraform fmt"
  error: "validation blocks"
  struct: "modules/ environments/"
  tests: "terratest"

dockerfile:
  patterns: ["Multi-stage", "Layer caching"]
  style: "hadolint"
  error: "HEALTHCHECK"
  struct: "Dockerfile, .dockerignore"
  tests: "container-structure-test"

shell:
  patterns: ["Bash strict mode"]
  style: "shfmt"
  error: "set -euo pipefail"
  struct: "scripts/"
  tests: "bats-core"

sql:
  patterns: ["Migrations", "Indexes"]
  style: "sqlfluff"
  error: "TRANSACTION"
  struct: "migrations/"
  tests: "pgTAP"
```

---

## 📋 PHASE 2: PLAN

### For Major Changes (>50 lines):

```
📋 IMPLEMENTATION PLAN

Task: Add user authentication service

Steps:
1. [Create] src/services/auth.service.ts
   └── AuthService class with login/logout/verify

2. [Create] src/types/auth.types.ts
   └── User, Token, AuthResponse types

3. [Modify] src/handlers/user.handler.ts
   └── Add authentication middleware

4. [Create] src/tests/auth.test.ts
   └── Unit tests for AuthService

Dependencies:
- jsonwebtoken (already installed)
- bcrypt (need to install)

Est. lines: ~120
Risk: 🟡 Medium

⛔ Proceed? (y/n):
```

---

## 📋 PHASE 3: IMPLEMENT

### Code Quality Principles:

```yaml
always:
  - Clear, descriptive naming
  - Proper error handling
  - Type safety (where applicable)
  - Comments for "why", not "what"
  - Small focused functions
  - DRY (Don't Repeat Yourself)

never:
  - Magic numbers/strings
  - Catch-all error handling
  - Any/unknown types without reason
  - Overly clever one-liners
  - Deep nesting (>3 levels)
  - Functions >50 lines
```

### Token Optimization:

```yaml
token_saving:
  # DON'T regenerate entire files
  - Use targeted edits for modifications
  - Show only changed sections
  - Reference existing code instead of copying

  # DON'T include unnecessary context
  - Skip boilerplate explanations
  - Omit obvious imports
  - Use snippets instead of full files

  # DO be efficient
  - Group related changes
  - Use code generation templates
  - Leverage language patterns
```

---

## 📋 PHASE 4: VERIFY

### Verification Commands by Language:

```yaml
build_check:
  go: "go build ./..."
  rust: "cargo build"
  typescript: "npx tsc --noEmit"
  python: "python -m py_compile"
  java: "mvn compile"
  csharp: "dotnet build"

lint_check:
  go: "golangci-lint run"
  rust: "cargo clippy"
  typescript: "npx eslint ."
  python: "ruff check ."
  java: "checkstyle"
  csharp: "dotnet format --verify-no-changes"

test_check:
  go: "go test ./... -v"
  rust: "cargo test"
  typescript: "npm test"
  python: "pytest"
  java: "mvn test"
  csharp: "dotnet test"
```

### Verification Output:

```
✅ VERIFICATION COMPLETE

Build: ✅ Passed
Lint: ✅ 0 errors, 0 warnings
Types: ✅ No issues

Files Changed:
├── [+] src/services/auth.service.ts (45 lines)
├── [+] src/types/auth.types.ts (20 lines)
├── [M] src/handlers/user.handler.ts (+12 lines)
└── [+] src/tests/auth.test.ts (35 lines)

Total: +112 lines, 4 files
```

---

## 📋 PHASE 5: OUTPUT

### Summary Format:

```
💻 IMPLEMENTATION COMPLETE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Changes Made:
1. Created `auth.service.ts` - JWT authentication
2. Created `auth.types.ts` - Type definitions
3. Updated `user.handler.ts` - Added auth middleware
4. Created `auth.test.ts` - Unit tests

Key Decisions:
- Used bcrypt for password hashing (security)
- JWT expires in 24h (configurable via env)
- Refresh token pattern for persistence

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 NEXT STEPS:
1️⃣ Run tests: npm test
2️⃣ Review diff: git diff
3️⃣ Commit: git commit -am "feat: add auth service"
4️⃣ Deploy: /deploy

Enter number or command:
```

---

## ⚙️ RULES APPLIED

| Phase      | Rules                          |
| ---------- | ------------------------------ |
| Understand | `context-management`           |
| Plan       | `stop-conditions` (if major)   |
| Implement  | `edit-verification`, `quality` |
| Verify     | `terminal-safety`, `evidence`  |
| Output     | `safety` (no secrets)          |

---

## 🔧 SUB-COMMANDS

| Command           | Description                     |
| ----------------- | ------------------------------- |
| `/code [request]` | Generate code for request       |
| `/code --plan`    | Show plan only, don't implement |
| `/code --test`    | Generate with tests             |
| `/code --docs`    | Generate with documentation     |
| `/code --dry`     | Preview changes only            |
| `/code --secure`  | Security-first generation       |
| `/code quality`   | Run AI quality analysis         |

---

## 🛡️ AI QUALITY GATES (v3.1)

```yaml
ai_quality_gates:
  description: "Multi-layer code quality assurance"

  layer_1_ai:
    name: "AI Auto-Fix"
    actions:
      linting: "Auto-fix obvious issues"
      formatting: "Consistent style"
      naming: "Semantic variable names"
      comments: "Add where needed"

  layer_2_static:
    name: "Static Analysis"
    tools:
      security: ["Snyk", "Semgrep", "CodeQL"]
      quality: ["SonarQube", "ESLint", "Pylint"]
      complexity: "Cyclomatic < 10 per function"

    thresholds:
      critical: "0 allowed"
      high: "Must acknowledge"
      medium: "Track in debt"

  layer_3_human:
    name: "Human Review"
    triggers:
      - "Complex business logic"
      - "Security-critical code"
      - "Infrastructure changes"
      - "Changes > 100 lines"

    workflow: "PR review required"

  commands:
    analyze: "/code quality analyze [path]"
    fix: "/code quality fix [path]"
    report: "/code quality report"
```

---

## 🔐 SECURITY-FIRST GENERATION (v3.1)

```yaml
security_generation:
  description: "Generate secure code by default"

  default_secure:
    input_validation:
      - "Validate all user input"
      - "Sanitize before use"
      - "Type coercion checks"

    output_encoding:
      - "Context-aware encoding"
      - "XSS prevention"
      - "SQL parameterization"

    error_handling:
      - "Non-revealing errors"
      - "Structured logging"
      - "No stack traces in prod"

    secrets:
      - "Environment variables"
      - "No hardcoded secrets"
      - "Rotation support"

  vulnerability_check:
    pre_commit: true
    patterns:
      - "SQLi"
      - "XSS"
      - "SSRF"
      - "Path Traversal"
      - "Command Injection"
      - "Insecure Deserialization"

  owasp_coverage:
    a01_broken_access: "RBAC checks"
    a02_crypto_failures: "Modern algorithms"
    a03_injection: "Parameterized queries"
    a07_auth_failures: "Secure session handling"

  commands:
    secure_generate: "/code secure [feature]"
    audit: "/code security audit"
```

---

_DOMYH Awesome Code v4.3 • Code Pro v3.1 • AI Quality + Security-First_
