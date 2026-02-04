---
name: coding-rules
description: "Awesome Coding Rules - Multi-language naming conventions, architecture patterns, design patterns, and coding standards. 23 languages, 10 architecture patterns, 20 design patterns, 70 coding rules. Verified from Google Style Guides, Microsoft Conventions, PEP 8, Effective Go, Rust API Guidelines, Swift API Design, Kotlin Conventions, PHP PSR-12, Ruby Style Guide, Zig Documentation, Nim NEP-1."
---

# 🏗️ Awesome Coding Rules

Comprehensive, verified coding standards for 23 programming languages. Based on official style guides from Google, Microsoft, Apple, JetBrains, PHP-FIG, Rust team, Zig team, Nim team, Linux Kernel, and framework documentation.

## Quick Reference

### Naming Conventions by Language

| Language   | Classes    | Functions            | Variables  | Constants   | Private      | Files            |
| ---------- | ---------- | -------------------- | ---------- | ----------- | ------------ | ---------------- |
| C++        | PascalCase | PascalCase           | snake_case | kPascalCase | snake*case*  | snake_case.cpp   |
| C#         | PascalCase | PascalCase           | camelCase  | PascalCase  | \_camelCase  | PascalCase.cs    |
| Java       | PascalCase | camelCase            | camelCase  | UPPER_SNAKE | camelCase    | PascalCase.java  |
| Python     | PascalCase | snake_case           | snake_case | UPPER_SNAKE | \_snake_case | snake_case.py    |
| Go         | PascalCase | PascalCase/camelCase | camelCase  | PascalCase  | camelCase    | snake_case.go    |
| Rust       | PascalCase | snake_case           | snake_case | SCREAMING   | snake_case   | snake_case.rs    |
| TypeScript | PascalCase | camelCase            | camelCase  | UPPER_SNAKE | \_camelCase  | kebab-case.ts    |
| Swift      | PascalCase | camelCase            | camelCase  | camelCase   | camelCase    | PascalCase.swift |
| Kotlin     | PascalCase | camelCase            | camelCase  | UPPER_SNAKE | \_camelCase  | PascalCase.kt    |
| PHP        | PascalCase | camelCase            | camelCase  | UPPER_SNAKE | camelCase    | PascalCase.php   |
| Ruby       | PascalCase | snake_case           | snake_case | SCREAMING   | @snake_case  | snake_case.rb    |

### Key Corrections from Research

| Common Mistake              | Correct Practice                 | Source                   |
| --------------------------- | -------------------------------- | ------------------------ |
| TS: `IUserService`          | `UserService` (no I prefix)      | ts.dev, modern TS guides |
| C++: snake_case functions   | PascalCase (Google Style)        | google.github.io         |
| Go: UPPER_SNAKE constants   | PascalCase/camelCase (by export) | go.dev                   |
| Swift: PascalCase constants | camelCase                        | swift.org                |

## Architecture Patterns

| Pattern               | Best For          | Testability  |
| --------------------- | ----------------- | ------------ |
| Clean Architecture    | Enterprise apps   | ✅ Excellent |
| Vertical Slice        | Feature-rich apps | ✅ Excellent |
| Hexagonal             | Domain-driven     | ✅ Excellent |
| Feature-Sliced Design | Large frontend    | ✅ Very Good |
| Modular Monolith      | Large teams       | ✅ Very Good |

### Clean Architecture Folder Structure

```
src/
├── Domain/              # Core business logic (NO dependencies)
│   ├── Entities/
│   ├── ValueObjects/
│   ├── Repositories/    # Interfaces only
│   └── DomainEvents/
├── Application/         # Use cases (depends on Domain only)
│   ├── Commands/
│   ├── Queries/
│   └── Behaviors/
├── Infrastructure/      # External services
│   ├── Persistence/
│   ├── Messaging/
│   └── Services/
└── Presentation/        # API/UI layer
    ├── Controllers/
    └── Middlewares/
```

## Coding Rules (Top 10)

| ID   | Rule                  | Severity | Description                            |
| ---- | --------------------- | -------- | -------------------------------------- |
| N001 | Descriptive Names     | CRITICAL | Names reveal intent without comments   |
| F001 | Single Responsibility | CRITICAL | Each function does one thing           |
| E002 | No Silent Catch       | CRITICAL | Never swallow exceptions               |
| S001 | Input Validation      | CRITICAL | Validate all user input                |
| S002 | No Hardcoded Secrets  | CRITICAL | Use environment variables              |
| C001 | Single Purpose        | CRITICAL | Each class has one reason to change    |
| C005 | Dependency Injection  | HIGH     | Inject dependencies, don't create them |
| F005 | Early Return          | MEDIUM   | Return early to reduce nesting         |
| D001 | Why Not What          | HIGH     | Comments explain why, not what         |
| T001 | Test Naming           | HIGH     | Tests describe expected behavior       |

## Design Patterns (Best Language per Pattern)

| Pattern   | Best Implementation | Reason                         |
| --------- | ------------------- | ------------------------------ |
| Singleton | Python/JS           | Modules are natural singletons |
| Factory   | C++/C#/Java         | Strong typing benefits         |
| Decorator | Python              | Native @decorator syntax       |
| Observer  | C#                  | Built-in event keyword         |
| Strategy  | C++                 | Compile-time polymorphism      |
| Iterator  | Python              | Generator expressions          |
| Visitor   | Rust                | Pattern matching with enum     |

## Data Files

| File                         | Content                      | Entries       |
| ---------------------------- | ---------------------------- | ------------- |
| `naming-conventions.csv`     | Multi-language naming rules  | 22 languages  |
| `architecture-patterns.csv`  | Project structure patterns   | 10 patterns   |
| `coding-rules.csv`           | Universal coding rules       | 32+ rules     |
| `design-patterns.csv`        | GoF patterns by language     | 20 patterns   |
| `build-systems.csv`          | Build system commands        | 38 configs    |
| `framework-signatures.csv`   | Framework detection rules    | 47 frameworks |
| `test-frameworks.csv`        | Test framework detection     | 24 frameworks |
| `solid-principles.csv`       | SOLID implementation         | 5 principles  |
| `memory-management.csv`      | Memory allocation benchmarks | 9 languages   |
| `performance-benchmarks.csv` | Cross-language performance   | 12 categories |
| `concurrency-patterns.csv`   | Async/threading comparison   | 9 languages   |

## Usage

```bash
# Search naming conventions
python .agent/skills/coding-rules/scripts/search.py "python function naming"

# Get architecture for project type
python .agent/skills/coding-rules/scripts/search.py "enterprise backend" --domain architecture

# Find design pattern implementation
python .agent/skills/coding-rules/scripts/search.py "observer csharp" --domain patterns
```

## Sources

| Language   | Official Source                                                                                                      |
| ---------- | -------------------------------------------------------------------------------------------------------------------- |
| C++        | [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)                                          |
| C#         | [Microsoft Naming Guidelines](https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/naming-guidelines) |
| Java       | [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html)                                        |
| Python     | [PEP 8](https://peps.python.org/pep-0008/)                                                                           |
| Go         | [Effective Go](https://go.dev/doc/effective_go)                                                                      |
| Rust       | [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/naming.html)                                        |
| TypeScript | [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/)                                                       |
| Swift      | [Swift API Design Guidelines](https://swift.org/documentation/api-design-guidelines/)                                |
| Kotlin     | [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html)                                     |
| PHP        | [PSR-12](https://www.php-fig.org/psr/psr-12/)                                                                        |
| Ruby       | [Ruby Style Guide](https://rubystyle.guide/)                                                                         |

---

_DOMYH Awesome Code v6.1.2 • Awesome Coding Rules • 23 Languages • 10 Architectures • 70+ Rules_
