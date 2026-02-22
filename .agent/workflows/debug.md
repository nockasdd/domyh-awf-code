---
description: "🐛 Systematic debugging: reproduce → isolate → analyze → fix → verify"
skills: { required: [error-handling], contextual: [auto] }
success_criteria: "Root cause identified and verified, fix applied, tests pass"
---

# 🐛 /debug — Debug Pro

> AI-Powered Debugging with Observability & Tracing
> 📚 30+ Languages • Root Cause Analysis • Hypothesis Testing • Failure Repository

---

## DEBUG FLOW

1. **CAPTURE** (Auto) — `hsa_declare_intent("debug: {error_summary}")`, check **episodic memory** (`.domyh/debug/episodic_memory.yaml`) for similar past bugs FIRST. Auto-detect language via HSA (`hsa_detect_stack`), load skill via HSA (`hsa_get_context`, `hsa_search_skills`), parse stack trace, identify affected files, `hsa_prefetch` suspected files. Show: `[Step 1/8] Capturing error context...`
2. **TIMELINE** — Reconstruct event timeline: `git log --oneline -10`, check recent changes to affected files, correlate with error timestamps. Answer: "When did this start?"
3. **REPRODUCE** — Create minimal reproduction, confirm error occurs consistently → ⛔ STOP if cannot reproduce: ask user 5 questions
4. **ISOLATE** — Binary search / git bisect, add trace logging, narrow to exact location. Use `hsa_trace_flow` to trace call chains upstream/downstream
5. **HYPOTHESIZE** — Form 2-3 hypotheses based on evidence:
   ```
   H1: [hypothesis] — Evidence: [what supports it] — Test: [how to verify]
   H2: [hypothesis] — Evidence: [what supports it] — Test: [how to verify]
   → Test each hypothesis systematically → Confirm/reject
   ```
6. **ANALYZE** — 5 Whys on CONFIRMED root cause (not assumptions)
7. **FIX** — Create FAILING test first, implement single fix → if 2 fixes fail → trigger **Progressive Escalation** (`rules/modules/progressive-escalation.yaml`): REFLECT → REFRAME → WIDEN → DECOMPOSE → ESCALATE. Add **prevention guard** to block similar bugs
8. **VERIFY** — Run reproduction steps, run full test suite, show before/after evidence. Persist pattern to `.domyh/debug/failures.yaml` if novel bug pattern discovered

---

## DEBUG MINDSET

```
❌ NEVER assume these:
- "I know what the bug is"         → Always reproduce first
- "I'll be quick"                  → Quick fixes create more bugs
- "It worked before"               → Something changed — check timeline
- "It must be a library bug"       → It's almost never the library
- "One fix should do it"           → Form hypotheses first, test each
```

---

## TIMELINE RECONSTRUCTION

```yaml
# Before diving into code, reconstruct the timeline:
timeline:
  sources:
    - "git log --oneline --since='7 days ago' -- [affected_files]"
    - "Error logs / console output (timestamps)"
    - "Recent dependency updates (package-lock.json diff)"
    - "Environment changes (.env, config files)"
  output: |
    [timestamp] Event 1: Last known working state
    [timestamp] Event 2: Change X committed
    [timestamp] Event 3: Error first reported
    → Most likely cause: Event between 2 and 3
```

---

## HYPOTHESIS TESTING

```yaml
# Instead of jumping to fix, test hypotheses:
process:
  1_form: "Based on evidence, create 2-3 hypotheses"
  2_rank: "Rank by likelihood (most evidence first)"
  3_test: "Design quick test for top hypothesis"
  4_confirm: "If confirmed → proceed to 5 Whys"
  5_reject: "If rejected → test next hypothesis"
  6_stuck: "If all rejected → expand search scope, ask user"

example:
  H1: "Null user from DB query (no validation)"
    evidence: "TypeError at user.id, findUser() called without check"
    test: "Add console.log before line 42, check user value"
    result: "CONFIRMED — user is undefined when ID not found"
```

---

## STACK TRACE PARSERS

| Language   | Error Pattern                                | Debugger          |
| ---------- | -------------------------------------------- | ----------------- |
| Go         | `goroutine \d+ [running]:, panic:`           | dlv               |
| Python     | `Traceback (most recent call last):`         | pdb, debugpy      |
| TypeScript | `at Object.<anonymous> (.ts:\d+)`            | --inspect-brk     |
| Rust       | `thread 'main' panicked at`                  | rust-gdb          |
| Java       | `at com.package.Class.method(File.java:\d+)` | jdb               |
| C++        | `Segmentation fault\|terminate called`       | gdb, lldb         |
| C#         | `Unhandled exception.*at .*\.cs:line`        | dotnet-dump       |
| PHP        | `Fatal error:.*in .*.php on line`            | xdebug            |
| Ruby       | `from .*.rb:\d+:in`                          | byebug            |
| Swift      | `Fatal error:.*file .*\.swift, line`         | lldb              |
| Kotlin     | `at .*\.kt:\d+`                              | IntelliJ debugger |

> Full parsers for 30+ languages via HSA: each skill's META.yaml contains `triggers.file_patterns`.

---

## ⛔ IF CANNOT REPRODUCE

```
Need more information:
1. Exact error message (copy-paste)?
2. Steps to trigger the error?
3. Environment details (OS, versions)?
4. Recent changes (git log)?
5. Logs from when error occurred?
→ If intermittent: suspect race condition, timing, or environment-specific issue
```

---

## GIT BISECT

```bash
git bisect start
git bisect bad HEAD
git bisect good <last_working_commit>
# Agent can automate: git bisect run <test_script>
```

## QUICK DEBUG LOGGING

| Language   | Snippet                                      |
| ---------- | -------------------------------------------- |
| Go         | `log.Printf("[DEBUG] %s: %+v", "var", val)`  |
| Rust       | `dbg!(&variable);`                           |
| Python     | `logging.debug(f"[DEBUG] {variable=}")`      |
| TypeScript | `console.log('[DEBUG]', { variable });`      |
| Java       | `System.out.println("[DEBUG] " + variable);` |

---

## ROOT CAUSE ANALYSIS (5 Whys)

```
Why 1: [immediate cause]
Why 2: [why that happened]
Why 3: [deeper reason]
Why 4: [systemic issue]
Why 5: [root cause]

🎯 ROOT CAUSE: [one-line summary]
🛡️ PREVENTION: [guard to prevent recurrence]
```

## BUG CATEGORIES

| Category       | Pattern                      | Common Fix                       |
| -------------- | ---------------------------- | -------------------------------- |
| Null Reference | `null\|undefined\|None\|nil` | Null checks, optional chaining   |
| Type Error     | `TypeError\|cannot convert`  | Validate types, add guards       |
| Async Race     | `race condition\|deadlock`   | Add locks, atomic ops            |
| Memory Leak    | `out of memory\|heap`        | Cleanup, weak references         |
| Network        | `timeout\|ETIMEDOUT`         | Retry logic, increase timeout    |
| Permission     | `EACCES\|unauthorized`       | Check file/API permissions       |
| State          | `stale data\|inconsistent`   | Cache invalidation, transactions |

---

## OBSERVABILITY INTEGRATION

```yaml
# If observability tools available, use them:
tools:
  sentry: "Check Sentry for error frequency, affected users, breadcrumbs"
  datadog: "Query DataDog APM for traces, latency spikes"
  grafana: "Check Grafana dashboards for metric anomalies"
  cloudwatch: "Search CloudWatch logs for error patterns"

# Ask user: "Do you have any monitoring/APM tools? (Sentry, DataDog, etc.)"
```

---

## DEFENSE-IN-DEPTH

> Validate at EVERY layer data passes through: "We made the bug impossible"

| Layer                    | Purpose                               | Example                                 |
| ------------------------ | ------------------------------------- | --------------------------------------- |
| 1. Entry Point           | Reject invalid input at API boundary  | `if (!dir) throw Error("dir required")` |
| 2. Business Logic        | Ensure data makes sense for operation | Validate IDs, check states              |
| 3. Environment Guard     | Prevent danger in specific contexts   | Refuse ops outside temp in tests        |
| 4. Debug Instrumentation | Capture context for forensics         | Stack traces, debug logs                |

---

## FAILURE REPOSITORY

```yaml
failure_patterns:
  - id: "cache-invalidation"
    symptoms: ["stale data", "deleted item still shows"]
    fix: "Add cache.invalidate() after mutations"
    prevention: "Always invalidate cache in write operations"
  - id: "n+1-query"
    symptoms: ["slow API", "many DB queries"]
    fix: "Use eager loading / batch queries"
    prevention: "Use query analyzer / ORM eager loading"
  - id: "race-condition"
    symptoms: ["intermittent failures", "data corruption"]
    fix: "Add mutex/transaction"
    prevention: "Always use transactions for multi-step writes"
  - id: "off-by-one"
    symptoms: ["missing last item", "index out of bounds"]
    fix: "Check loop boundaries, use length-1"
    prevention: "Prefer forEach/map over manual indexing"
```

---

## PROGRESSIVE ESCALATION

> When fixes repeatedly fail, progressively shift debugging strategy.
> See `rules/modules/progressive-escalation.yaml` for full protocol.

```
Level 1 RETRY     → Fix directly (2 attempts)
Level 2 REFLECT   → Analyze WHY approach fails (Reflexion + Bias Check)
Level 3 REFRAME   → Change perspective (Invert + Rubber Duck + Devil's Advocate)
Level 4 WIDEN     → Expand scope (Trace chain + Git forensics + Env audit)
Level 5 DECOMPOSE → Isolate precisely (Minimal repro + Binary search)
Level 6 ESCALATE  → Full report to user with all evidence
```

**Before ANY fix**: Check episodic memory (`.domyh/debug/episodic_memory.yaml`) for past solutions.
**After resolution**: Save lesson via `templates/reflection/pivot_analysis.md` → episodic memory entry.

---

## SUB-COMMANDS

| Command                  | Description                |
| ------------------------ | -------------------------- |
| `/debug [error]`         | Full debug flow            |
| `/debug ai [error]`      | AI-powered analysis        |
| `/debug similar [error]` | Search failure repository  |
| `/debug save [pattern]`  | Save to repository         |
| `/debug --trace`         | Add verbose logging        |
| `/debug --bisect`        | Git bisect helper          |
| `/debug --profile`       | Performance profiling      |
| `/debug --memory`        | Memory leak detection      |
| `/debug --timeline`      | Reconstruct event timeline |

---

## 🪞 REFLECTION CHECKPOINT

> After fix verified, apply `templates/reflection/critic.md`:
> 1. Root cause proven (5 Whys complete)?
> 2. Prevention guard added?
> 3. On novel failure → `templates/reflection/error_analysis.md` → persist to `failures.yaml`
> 4. On successful debug → `templates/reflection/success_analysis.md`

---

## 💾 SESSION SAVE

After completing this workflow:
1. Update `memory/CONTEXT_SNAPSHOT.md` - what changed, current status
2. Append summary to `memory/session.md`
