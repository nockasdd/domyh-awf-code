---
name: error-handling
description: "Error handling patterns for robust applications. Use when implementing error boundaries, recovery strategies, or structured logging."
detect: ["*error*", "*exception*", "*Error*"]
category: core
tier: 1
---

# Error Handling Skill

> 🛡️ **Comprehensive error handling patterns for 12 languages**
> **Patterns**: 298 | **Languages**: 12 | **Categories**: 8

---

## Quick Reference

| What You Need                            | Data File                           | Patterns |
| ---------------------------------------- | ----------------------------------- | -------- |
| Core patterns (Result, Either, wrapping) | `core-patterns.yaml`                | 30       |
| C/C++ (errno, RAII, std::expected)       | `language-c-cpp.yaml`               | 18       |
| Go/Rust (errors.Is, Result, ?)           | `language-go-rust.yaml`             | 30       |
| Python/Java (try-except, checked)        | `language-python-java.yaml`         | 30       |
| Swift/Kotlin (throws, runCatching)       | `language-swift-kotlin.yaml`        | 30       |
| TypeScript/PHP/Ruby                      | `language-typescript-php-ruby.yaml` | 30       |
| Resilience (circuit breaker, retry)      | `resilience-patterns.yaml`          | 25       |
| Error code design                        | `error-codes.yaml`                  | 25       |
| Error message best practices             | `error-messages.yaml`               | 25       |
| UI error handling (React, Vue)           | `ui-error-patterns.yaml`            | 20       |
| API error responses (RFC 9457)           | `api-error-patterns.yaml`           | 20       |
| Anti-patterns to avoid                   | `anti-patterns.yaml`                | 15       |

---

## Language Coverage

| Language       | Paradigm            | Key Patterns                                 |
| -------------- | ------------------- | -------------------------------------------- |
| **C**          | Return codes        | errno, setjmp/longjmp, goto cleanup          |
| **C++**        | RAII + Exceptions   | std::expected (C++23), noexcept, try-catch   |
| **Go**         | Errors as values    | `if err != nil`, errors.Is/As, panic/recover |
| **Rust**       | Result type         | Result<T,E>, `?` operator, thiserror/anyhow  |
| **Python**     | Exceptions          | try-except, `from` chaining, contextlib      |
| **Java**       | Checked exceptions  | try-with-resources, checked vs unchecked     |
| **Swift**      | throws/Result       | do-catch, try?, try!, async throws           |
| **Kotlin**     | Result + Coroutines | runCatching, CancellationException           |
| **TypeScript** | Type-safe           | Type guards, Result pattern, Promise.catch   |
| **PHP**        | Throwable           | Error + Exception, set_error_handler         |
| **Ruby**       | Begin-rescue        | ensure, retry, dry-monads Result             |
| **C#**         | Exception filters   | AggregateException, async await              |

---

## Paradigm Comparison

| Approach             | Languages                  | Pros                          | Cons                     |
| -------------------- | -------------------------- | ----------------------------- | ------------------------ |
| **Result/Either**    | Rust, Scala, Swift, Kotlin | Compile-time safety, explicit | Verbose, learning curve  |
| **Errors as Values** | Go, C                      | Simple, no stack unwinding    | Easy to ignore           |
| **Exceptions**       | Python, Java, C#, PHP      | Natural syntax, stack trace   | Performance, hidden flow |
| **RAII**             | C++                        | Automatic cleanup             | C++ only                 |

---

## Resilience Patterns

### Circuit Breaker States

```
CLOSED ──(failures > threshold)──> OPEN
   ↑                                 │
   │                                 ↓
   └─(probe success)─── HALF-OPEN ──┘
```

### Backoff Strategies

| Strategy    | Formula                  | Best For         |
| ----------- | ------------------------ | ---------------- |
| Fixed       | `wait(1s)`               | Simple cases     |
| Linear      | `wait(n * delay)`        | Moderate load    |
| Exponential | `wait(2^n * delay)`      | Distributed      |
| Full Jitter | `random(0, 2^n * delay)` | High concurrency |

---

## Error Taxonomy

| Type           | Description                | Action                 |
| -------------- | -------------------------- | ---------------------- |
| **Transient**  | Temporary, self-correcting | Retry with backoff     |
| **Permanent**  | Requires intervention      | Fail fast, notify      |
| **Validation** | User input issues          | Return detailed errors |
| **Business**   | Domain rule violations     | Return specific codes  |
| **System**     | Infrastructure failures    | Log, alert, fallback   |

---

## Common Patterns by Use Case

### Input Validation

```
// TypeScript Result pattern
type Result<T> = { ok: true; value: T } | { ok: false; error: Error };
```

### API Error Response (RFC 9457)

```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Validation Error",
  "status": 422,
  "detail": "The email field is required",
  "errors": [{ "field": "email", "code": "required" }]
}
```

### Circuit Breaker (Pseudocode)

```
if circuit.isOpen() and !timeout.expired():
    return fallback()

result = callService()
if result.isError():
    circuit.recordFailure()
else:
    circuit.recordSuccess()
```

---

## Anti-Patterns to Avoid

| ❌ Anti-Pattern     | ✅ Better Approach      |
| ------------------- | ----------------------- |
| Silent `catch {}`   | Log or rethrow          |
| Catch-all Exception | Catch specific types    |
| String errors       | Use Error classes       |
| Log and throw same  | Either log or throw     |
| panic for flow      | Use Result/error return |

---

## HSA Integration

Data powered by HSA BM25 search engine. Query YAML data via skill search:

| Domain     | Query Examples                   |
| ---------- | -------------------------------- |
| Core       | "result pattern either monad"    |
| Language   | "rust result error handling"     |
| Resilience | "circuit breaker retry backoff"  |
| API        | "RFC 9457 error response format" |

---


## 📁 Data Files

| File | Patterns | Coverage |
|------|----------|----------|
| `core-patterns.yaml` | 20+ | Try-catch, Result type, error boundaries |
| `api-error-patterns.yaml` | 15+ | RFC 9457, HTTP status, GraphQL errors |
| `resilience-patterns.yaml` | 15+ | Circuit breaker, retry, fallback |
| `error-codes.yaml` | 30+ | Categorized error code standards |
| `error-messages.yaml` | 15+ | i18n, user-friendly messaging |
| `anti-patterns.yaml` | 10+ | Silent catch, pokemon catch, etc |
| `ui-error-patterns.yaml` | 10+ | Toast, error boundary, loading states |
| `language-*.yaml` (5 files) | 50+ | Language-specific: Go/Rust, Python/Java, TS/PHP/Ruby, C/C++, Swift/Kotlin |

**Total: 12 data files, 180+ patterns**

---

## Failure Modes
<!-- Các cách skill có thể fail và cách xử lý -->
| Failure | Symptom | Mitigation |
|:--------|:--------|:-----------|

## Integration
<!-- Skill nào bổ trợ/xung đột -->
| Skill | Relationship |
|:------|:-------------|
