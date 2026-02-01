---
name: debug
trigger: ["/debug", "fix", "error", "bug", "lỗi", "sửa", "crash", "exception"]
persona: debugger
description: "🐛 Systematic debugging: reproduce → isolate → analyze → fix → verify"
---

# 🐛 /debug — Systematic Debugging Pro v3.0

> AI-Powered Debugging with Observability & Tracing
> 📚 30+ Languages • Root Cause Analysis • Failure Repository

---

## 🔄 DEBUG FLOW

```
User: /debug [error|issue]
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 1: CAPTURE (Auto - 10s)          │
│ ▸ Capture error message & stack trace   │
│ ▸ Identify affected files               │
│ ▸ Detect language & load debug skill    │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 2: REPRODUCE                      │
│ ▸ Verify reproduction steps             │
│ ⛔ STOP if cannot reproduce → ask info  │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 3: ISOLATE                        │
│ ▸ Binary search / bisect               │
│ ▸ Add trace logging                     │
│ ▸ Narrow to exact location              │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 4: ANALYZE                        │
│ ▸ Root cause analysis (5 Whys)          │
│ ▸ Check failure repository              │
│ ▸ Identify fix approach                 │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 5: FIX                            │
│ ▸ Implement targeted fix                │
│ ▸ Add regression test                   │
│ ▸ Update failure repository             │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 6: VERIFY                         │
│ ▸ Run reproduction steps                │
│ ▸ Run full test suite                   │
│ ▸ Show before/after evidence            │
└─────────────────────────────────────────┘
```

---

## 📋 PHASE 1: CAPTURE

### Error Report Format:

```
🐛 ERROR CAPTURED

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Error: TypeError: Cannot read property 'id' of undefined
Location: src/services/user.service.ts:45
Stack:
  at UserService.getUser (user.service.ts:45)
  at UserController.show (user.controller.ts:23)
  at Router.handle (router.ts:112)

Language: TypeScript
Skill loaded: typescript-expert

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Affected files identified:
├── src/services/user.service.ts (primary)
├── src/controllers/user.controller.ts
└── src/types/user.types.ts
```

### Stack Trace Parsers (30+ Languages):

```yaml
# ═══════════════════════════════════════════════════════════════
# BACKEND / SYSTEMS
# ═══════════════════════════════════════════════════════════════

go:
  pattern: "goroutine \\d+ \\[running\\]:|panic:"
  debugger: "dlv debug"
  trace: "runtime/debug.Stack()"
  profiler: "go tool pprof"
  race: "go run -race"

rust:
  pattern: "panicked at|RUST_BACKTRACE=1"
  debugger: "rust-gdb, rust-lldb"
  trace: "std::backtrace::Backtrace"
  profiler: "cargo flamegraph"
  sanitizer: "cargo +nightly miri"

java:
  pattern: "Exception in thread|at [\\w.]+\\([\\w]+\\.java:\\d+\\)"
  debugger: "jdb, IntelliJ IDEA"
  trace: "Thread.currentThread().getStackTrace()"
  profiler: "async-profiler, JFR"
  memory: "jmap, VisualVM"

kotlin:
  pattern: "Exception in thread|at [\\w.]+\\([\\w]+\\.kt:\\d+\\)"
  debugger: "IntelliJ IDEA"
  trace: "Throwable().stackTrace"
  profiler: "async-profiler"
  coroutine: "-Dkotlinx.coroutines.debug"

csharp:
  pattern: "Unhandled exception|at [\\w.]+\\.cs:line \\d+"
  debugger: "Visual Studio, dotnet-trace"
  trace: "Environment.StackTrace"
  profiler: "dotnet-counters"
  memory: "dotnet-dump"

cpp:
  pattern: "Segmentation fault|terminate called"
  debugger: "gdb, lldb"
  trace: "backtrace()"
  profiler: "perf, valgrind"
  sanitizer: "AddressSanitizer, UBSan"

c:
  pattern: "Segmentation fault|core dumped"
  debugger: "gdb"
  trace: "backtrace()"
  profiler: "valgrind, perf"
  sanitizer: "AddressSanitizer"

# ═══════════════════════════════════════════════════════════════
# SCRIPTING / DYNAMIC
# ═══════════════════════════════════════════════════════════════

python:
  pattern: "Traceback \\(most recent call last\\)|File \".*\", line \\d+"
  debugger: "pdb, ipdb, debugpy"
  trace: "traceback.print_exc()"
  profiler: "py-spy, cProfile"
  memory: "memory_profiler, tracemalloc"

ruby:
  pattern: "from .+:\\d+:in"
  debugger: "byebug, pry"
  trace: "caller, Kernel#set_trace_func"
  profiler: "ruby-prof, stackprof"
  memory: "ObjectSpace"

php:
  pattern: "PHP Fatal error:|Stack trace:"
  debugger: "xdebug"
  trace: "debug_backtrace()"
  profiler: "Blackfire, Xdebug"
  memory: "memory_get_usage()"

perl:
  pattern: "at .+ line \\d+|Died at"
  debugger: "perl -d"
  trace: "Carp::confess"
  profiler: "Devel::NYTProf"
  memory: "Devel::Size"

lua:
  pattern: "lua: .+:\\d+:"
  debugger: "mobdebug"
  trace: "debug.traceback()"
  profiler: "LuaProfiler"
  memory: "collectgarbage('count')"

# ═══════════════════════════════════════════════════════════════
# JAVASCRIPT / TYPESCRIPT
# ═══════════════════════════════════════════════════════════════

javascript:
  pattern: "at .+ \\(.+:\\d+:\\d+\\)|TypeError:|ReferenceError:"
  debugger: "Node Inspector, Chrome DevTools"
  trace: "console.trace(), Error.stack"
  profiler: "clinic.js, 0x"
  memory: "heapdump, memwatch"

typescript:
  pattern: "at .+ \\(.+\\.ts:\\d+:\\d+\\)"
  debugger: "VS Code, ts-node --inspect"
  trace: "Error.stack with source maps"
  profiler: "clinic.js"
  sourcemap: "source-map-support"

react:
  pattern: "Error: .+ at .+|React ErrorBoundary"
  debugger: "React DevTools"
  trace: "componentStack"
  profiler: "React Profiler"
  render: "why-did-you-render"

nextjs:
  pattern: "Error: .+ at .+|getServerSideProps"
  debugger: "VS Code"
  trace: "next-debug"
  profiler: "@next/bundle-analyzer"
  hydration: "suppressHydrationWarning"

vue:
  pattern: "Vue warn|at .+\\.vue:\\d+"
  debugger: "Vue DevTools"
  trace: "errorCaptured hook"
  profiler: "Vue Performance"
  render: "v-once profiling"

deno:
  pattern: "error: .+ at .+\\.ts:\\d+"
  debugger: "--inspect-brk"
  trace: "Deno.core.opSync"
  profiler: "deno bench"
  permission: "deno run --allow-*"

# ═══════════════════════════════════════════════════════════════
# MOBILE
# ═══════════════════════════════════════════════════════════════

swift:
  pattern: "Fatal error:|Thread \\d+: .+ at"
  debugger: "Xcode LLDB"
  trace: "Thread.callStackSymbols"
  profiler: "Instruments"
  memory: "Leaks, Allocations"

kotlin_android:
  pattern: "FATAL EXCEPTION:|at .+\\(.+\\.kt:\\d+\\)"
  debugger: "Android Studio"
  trace: "Log.d(TAG, Throwable().stackTraceToString())"
  profiler: "Android Profiler"
  memory: "LeakCanary"

dart:
  pattern: "Unhandled exception:|#\\d+ .+"
  debugger: "DevTools, VS Code"
  trace: "StackTrace.current"
  profiler: "Observatory"
  memory: "DevTools Memory"

flutter:
  pattern: "FlutterError|#\\d+ .+"
  debugger: "Flutter DevTools"
  trace: "FlutterError.onError"
  profiler: "Performance overlay"
  widget: "Widget Inspector"

# ═══════════════════════════════════════════════════════════════
# FUNCTIONAL
# ═══════════════════════════════════════════════════════════════

elixir:
  pattern: "\\*\\* \\(\\w+Error\\)|\\(elixir\\) lib/"
  debugger: "IEx.pry"
  trace: "Process.info(self(), :current_stacktrace)"
  profiler: "ExProf, fprof"
  observer: ":observer.start()"

haskell:
  pattern: "\\*\\*\\* Exception:|CallStack"
  debugger: "GHCi :trace"
  trace: "GHC.Stack"
  profiler: "ghc -prof"
  heap: "hp2ps"

scala:
  pattern: "at .+\\(.+\\.scala:\\d+\\)"
  debugger: "IntelliJ IDEA"
  trace: "Thread.currentThread.getStackTrace"
  profiler: "async-profiler"
  akka: "akka.loglevel = DEBUG"

clojure:
  pattern: "clojure\\.lang\\.ExceptionInfo|at clojure\\.core/"
  debugger: "CIDER"
  trace: "clojure.stacktrace/print-stack-trace"
  profiler: "criterium"
  repl: "clojure.repl/pst"

# ═══════════════════════════════════════════════════════════════
# INFRASTRUCTURE
# ═══════════════════════════════════════════════════════════════

shell:
  pattern: "line \\d+:|command not found"
  debugger: "bash -x, set -x"
  trace: "caller, BASH_SOURCE"
  profiler: "time command"
  linter: "shellcheck"

sql:
  pattern: "ERROR:|SQLSTATE"
  debugger: "EXPLAIN ANALYZE"
  trace: "pg_stat_statements"
  profiler: "pgBadger"
  slow: "log_min_duration_statement"

docker:
  pattern: "docker: Error response"
  debugger: "docker logs -f"
  trace: "docker events"
  profiler: "docker stats"
  network: "docker network inspect"
```

---

## 📋 PHASE 2: REPRODUCE

### Reproduction Template:

```
📝 REPRODUCTION STEPS

Environment:
├── OS: Ubuntu 22.04 / Windows 11 / macOS 14
├── Runtime: Node 20.10.0 / Python 3.12 / Go 1.21
├── Dependencies: package.json / requirements.txt
└── Config: .env.example

Steps:
1. [Command or action]
2. [Command or action]
3. [Observe error]

Expected: [What should happen]
Actual: [What happens - error]

Reproduction rate: [Always / Sometimes / Rare]
```

### ⛔ If Cannot Reproduce:

```
⛔ CANNOT REPRODUCE

Need more information:

1. Exact error message (copy-paste)?
2. Steps to trigger the error?
3. Environment details (OS, versions)?
4. Recent changes (git log)?
5. Logs from when error occurred?

Please provide: [specific request]
```

---

## 📋 PHASE 3: ISOLATE

### Binary Search / Git Bisect:

```bash
# Find broken commit
git bisect start
git bisect bad HEAD
git bisect good <last_working_commit>
# Git will find the breaking commit

# Or manually:
git log --oneline -20
# Identify suspect commits
```

### Debug Logging by Language:

```yaml
# Quick debug logging snippets

go: |
  import "log"
  log.Printf("[DEBUG] %s: %+v", "variable", value)

rust: |
  dbg!(&variable);
  println!("[DEBUG] {:?}", variable);

python: |
  import logging
  logging.debug(f"[DEBUG] {variable=}")

typescript: |
  console.log('[DEBUG]', { variable });

java: |
  System.out.println("[DEBUG] " + variable);

swift: |
  print("[DEBUG] \(variable)")

kotlin: |
  println("[DEBUG] $variable")
```

---

## 📋 PHASE 4: ANALYZE

### Root Cause Analysis (5 Whys):

```
🔍 ROOT CAUSE ANALYSIS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Error: Cannot read property 'id' of undefined

Why 1: user object is undefined
Why 2: findUser() returned null
Why 3: Database query returned no results
Why 4: User ID 123 doesn't exist
Why 5: User was deleted but cache wasn't invalidated

🎯 ROOT CAUSE: Cache invalidation missing on user delete

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Common Bug Categories:

```yaml
categories:
  null_reference:
    pattern: "null|undefined|None|nil"
    cause: "Variable not initialized or unexpected null"
    fix: "Add null checks, optional chaining"

  type_error:
    pattern: "TypeError|cannot convert"
    cause: "Wrong type passed to function"
    fix: "Validate types, add type guards"

  async_race:
    pattern: "race condition|concurrent|deadlock"
    cause: "Async operations not synchronized"
    fix: "Add locks, use atomic operations"

  memory_leak:
    pattern: "out of memory|heap overflow"
    cause: "Resources not released"
    fix: "Implement cleanup, use weak references"

  network_timeout:
    pattern: "timeout|ETIMEDOUT|connection refused"
    cause: "Network issues or slow server"
    fix: "Add retry logic, increase timeout"

  permission:
    pattern: "permission denied|EACCES|unauthorized"
    cause: "Missing permissions"
    fix: "Check file/API permissions"
```

---

## 📋 PHASE 5: FIX

### Fix Documentation:

````
🔧 FIX APPLIED

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Root Cause: Cache not invalidated on user delete

File: src/services/user.service.ts:45

Before:
```typescript
async deleteUser(id: string) {
  await this.userRepo.delete(id);
}
````

After:

```typescript
async deleteUser(id: string) {
  await this.userRepo.delete(id);
  await this.cache.invalidate(`user:${id}`);  // Fix: invalidate cache
}
```

Regression Test Added:

```typescript
it("should invalidate cache on delete", async () => {
  // Test verifies cache is cleared
});
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```

---

## 📋 PHASE 6: VERIFY

### Verification Checklist:

```

✅ VERIFICATION COMPLETE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reproduction Test:
├── Step 1: ✅ Passed
├── Step 2: ✅ Passed
└── Step 3: ✅ No error

Test Suite:
├── Unit tests: ✅ 156/156 passed
├── Integration: ✅ 23/23 passed
└── Regression: ✅ New test passes

Build Status: ✅ Success

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 NEXT STEPS:
1️⃣ Commit fix: git commit -am "fix: invalidate cache on user delete"
2️⃣ Update docs if needed
3️⃣ Deploy: /deploy

Enter number:

````

---

## 🗃️ FAILURE REPOSITORY

### Known Issues Pattern:

```yaml
# Store common issues for faster debugging

failure_patterns:
  - id: "cache-invalidation"
    symptoms: ["stale data", "deleted item still shows"]
    root_cause: "Cache not cleared on mutation"
    solution: "Add cache.invalidate() after mutations"
    files: ["*cache*", "*service*"]

  - id: "n+1-query"
    symptoms: ["slow API", "many DB queries"]
    root_cause: "Fetching related data in loop"
    solution: "Use eager loading / batch queries"
    files: ["*repository*", "*service*"]

  - id: "race-condition"
    symptoms: ["intermittent failures", "data corruption"]
    root_cause: "Concurrent access without locks"
    solution: "Add mutex/transaction"
    files: ["*async*", "*worker*"]
````

---

## 🔧 SUB-COMMANDS

| Command            | Description           |
| ------------------ | --------------------- |
| `/debug [error]`   | Full debug flow       |
| `/debug --trace`   | Add verbose logging   |
| `/debug --bisect`  | Git bisect helper     |
| `/debug --profile` | Performance profiling |
| `/debug --memory`  | Memory leak detection |

---

## ⚙️ TOKEN OPTIMIZATION

```yaml
token_saving:
  # Focus only on relevant code
  - Show only affected functions, not entire files
  - Use stack trace to identify exact locations
  - Skip unrelated tests/files

  # Efficient debugging
  - Use binary search, not sequential
  - Check failure repository first
  - Apply known patterns before deep analysis
```

---

## 📜 RULES APPLIED

| Phase     | Rules                                   |
| --------- | --------------------------------------- |
| Capture   | `terminal-safety`, `context-management` |
| Reproduce | `stop-conditions`                       |
| Isolate   | `edit-verification`                     |
| Analyze   | `evidence`, `quality`                   |
| Fix       | `edit-verification`, `safety`           |
| Verify    | `terminal-safety`, `evidence`           |

---

## 🤖 AI ROOT CAUSE ANALYSIS (v3.1)

```yaml
ai_root_cause:
  description: "AI-powered debugging with 69% success rate (2025)"

  workflow:
    1: "Collect error + stack trace"
    2: "Gather execution context"
    3: "Analyze code paths"
    4: "Identify probable cause"
    5: "Suggest fix(es)"
    6: "Human verification"

  context_sources:
    - "Error logs and stack traces"
    - "Recent git commits"
    - "Environment differences"
    - "Dependency changes"
    - "Similar past bugs"

  confidence_scoring:
    high:
      threshold: "> 80%"
      action: "Auto-suggest fix"
    medium:
      threshold: "50-80%"
      action: "Present multiple options"
    low:
      threshold: "< 50%"
      action: "Request more context"

  limitations:
    - "Complex logic bugs need human review"
    - "Race conditions hard to reproduce"
    - "Business rule violations"

  commands:
    ai_debug: "/debug ai [error_message]"
    context: "/debug context [add|show]"
```

---

## 📚 FAILURE REPOSITORY (v3.1)

```yaml
failure_repository:
  description: "Learn from past bugs - never repeat"

  captured_data:
    error_signature: "Unique error identifier"
    root_cause: "What caused it"
    fix_applied: "How it was fixed"
    prevention: "How to prevent"
    tags: ["memory", "async", "database"]

  features:
    search:
      command: "/debug similar [error]"
      pattern_match: true
      fuzzy_search: true

    auto_match:
      description: "Check repository on new errors"
      suggest_fix: true
      show_history: true

    learn:
      description: "Save new patterns"
      command: "/debug save [pattern]"

  storage:
    location: ".brain/failure_repository.json"
    sync: "Optional team sync"

  benefits:
    - "Faster debugging for known issues"
    - "Knowledge transfer between team members"
    - "Pattern recognition for prevention"
```

---

## 🔧 SUB-COMMANDS (Updated)

| Command                  | Description               |
| ------------------------ | ------------------------- |
| `/debug [error]`         | Full debug flow           |
| `/debug ai [error]`      | AI-powered analysis       |
| `/debug similar [error]` | Search failure repository |
| `/debug save [pattern]`  | Save to repository        |
| `/debug --trace`         | Add verbose logging       |
| `/debug --bisect`        | Git bisect helper         |
| `/debug --profile`       | Performance profiling     |
| `/debug --memory`        | Memory leak detection     |

---

_DOMYH Agent v4.3 • Debug Pro v3.1 • AI Root Cause + Failure Repository_
