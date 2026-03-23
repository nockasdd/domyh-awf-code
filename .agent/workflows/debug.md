---
description: "🐛 Systematic debugging: reproduce → isolate → analyze → fix → verify"
skills: { required: [error-handling], contextual: [auto] }
success_criteria: "Root cause identified and verified, fix applied, tests pass"
---

# 🐛 /debug — Debug Pro

> AI-Powered Debugging with Observability & Tracing
> 📚 30+ Languages • Root Cause Analysis • Hypothesis Testing

---

## ⛔ RULES (Always Apply)

| # | Rule | Category |
|:--|:-----|:---------|
| R1 | Check episodic memory for similar past bugs FIRST | Efficiency |
| R2 | Never apply fix without reproduction evidence | Quality |
| R3 | ⛔ STOP if cannot reproduce — ask user 5 questions | Safety |
| R4 | Form hypotheses before editing code | Discipline |
| R5 | Max 3 fix attempts — escalate if still failing | Efficiency |

---

## ⛔ THE IRON LAW

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

**Violating the letter of this process is violating the spirit of debugging.**

---

## DEBUG FLOW (8 Steps)

1. **CAPTURE** — `hsa_session("debug: {error_summary}")`, check **episodic memory** first. Auto-detect language, parse stack trace, identify affected files. Show: `[1/8] Capturing error context...`
2. **TIMELINE** — Reconstruct: `git log --oneline -10`, check recent changes, correlate timestamps. Answer: "When did this start?"
3. **REPRODUCE** — Minimal reproduction, confirm consistent.
   → ⛔ STOP if cannot reproduce: "Need: (1) exact error, (2) steps to trigger, (3) environment, (4) recent changes, (5) logs"
4. **ISOLATE** — Binary search / `git bisect`, trace logging, `hsa_trace_flow` for call chains. Narrow to exact location.
5. **HYPOTHESIZE** — Form 2-3 hypotheses:
   ```
   H1: [hypothesis] — Evidence: [supports] — Test: [verify method]
   H2: [hypothesis] — Evidence: [supports] — Test: [verify method]
   → Test systematically → Confirm/Reject
   ```
6. **ANALYZE** — 5 Whys on CONFIRMED root cause → `🎯 ROOT CAUSE: [summary]` → `🛡️ PREVENTION: [guard]`
7. **FIX** — Failing test FIRST → single fix → if 2 fail → Progressive Escalation → add prevention guard.
8. **VERIFY** — Run reproduction, full test suite, show before/after. Persist to episodic memory if novel.

---

## ⛔ 3-FIX ESCALATION

| Attempt | Action |
|:--------|:-------|
| Fix #1 fails | Return to root cause investigation |
| Fix #2 fails | Re-analyze with new info |
| Fix #3 fails | **STOP. Question the architecture.** |

Signs of architectural problem (not a bug): each fix reveals coupling, requires "massive refactoring", creates new symptoms. **→ Discuss with user before continuing.**

---

## DEBUG MINDSET

```
❌ NEVER assume:
- "I know what the bug is"         → Always reproduce first
- "I'll be quick"                  → Quick fixes create more bugs
- "It worked before"               → Something changed — check timeline
- "It must be a library bug"       → It's almost never the library
- "One fix should do it"           → Form hypotheses first
```

---

## RATIONALIZATION PREVENTION

| Excuse | Reality |
|:-------|:--------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check. |
| "Just try this first" | First fix sets the pattern. Do it right. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+) | 3+ failures = architectural problem. Stop. |

---

## COMMANDS

| Command | Description |
|:--------|:------------|
| `/debug [error]` | Full debug flow |
| `/debug ai [error]` | AI-powered analysis |
| `/debug similar [error]` | Search episodic memory |
| `/debug save [pattern]` | Save to failure repository |
| `/debug --trace` | Add verbose logging |
| `/debug --bisect` | Git bisect helper |
| `/debug --profile` | Performance profiling |
| `/debug --memory` | Memory leak detection |
| `/debug --timeline` | Reconstruct event timeline |

---

## STACK TRACE PARSERS

| Language | Error Pattern | Debugger |
|:---------|:--------------|:---------|
| Go | `goroutine \d+ [running]:, panic:` | dlv |
| Python | `Traceback (most recent call last):` | pdb, debugpy |
| TypeScript | `at Object.<anonymous> (.ts:\d+)` | --inspect-brk |
| Rust | `thread 'main' panicked at` | rust-gdb |
| Java | `at com.package.Class(File.java:\d+)` | jdb |
| C# | `Unhandled exception.*\.cs:line` | dotnet-dump |

> Full parsers for 30+ languages via HSA — each skill's META.yaml contains `triggers.file_patterns`.

---

## BUG CATEGORIES

| Category | Pattern | Common Fix |
|:---------|:--------|:-----------|
| Null Reference | null, undefined, None, nil | Null checks, optional chaining |
| Type Error | TypeError, cannot convert | Type guards, validation |
| Async Race | race condition, deadlock | Locks, atomic ops, transactions |
| Memory Leak | out of memory, heap | Cleanup, weak references |
| Network | timeout, ETIMEDOUT | Retry logic, timeout increase |
| State | stale data, inconsistent | Cache invalidation, transactions |

---

## DEFENSE-IN-DEPTH

> Validate at EVERY layer: "We made the bug impossible"

| Layer | Purpose | Example |
|:------|:--------|:--------|
| Entry Point | Reject invalid input at boundary | `if (!x) throw Error("required")` |
| Business Logic | Data makes sense for operation | Validate IDs, check states |
| Environment Guard | Prevent danger in context | Refuse ops outside temp in tests |
| Debug Instrumentation | Forensic context | Stack traces, debug logs |

---

## PROGRESSIVE ESCALATION

> When fixes repeatedly fail → shift strategy. See `rules/modules/progressive-escalation.yaml`.

```
L1 RETRY     → Fix directly (2 attempts)
L2 REFLECT   → Analyze WHY approach fails
L3 REFRAME   → Change perspective (Invert + Rubber Duck)
L4 WIDEN     → Expand scope (Trace chain + Git forensics)
L5 DECOMPOSE → Minimal repro + Binary search
L6 ESCALATE  → Full report to user with all evidence
```

**Before ANY fix:** Check episodic memory. **After resolution:** Save lesson.

---

## CASCADE EVALUATION (Recommended — MCP)

```
hsa_delegate({action:'cascade', cascade_text:'[prompt]', task_type:'debug'})
→ wait 5s → hsa_delegate({action:'cascade_read', cascade_id:'...'})
```
**Auto-cascade** (≥6.5): After L3 escalation, race conditions, concurrency
**Suggest cascade** (4.0-6.5): Multi-step reasoning, complex RCA

---

## REFLECTION CHECKPOINT

⛔ **MANDATORY** — Execute before completing this workflow (SESSION_005):

1. **VERIFY** — Does output meet success_criteria (see YAML frontmatter)?
2. **PERSIST** (if HSA available):
   - `hsa_session({action:'persist', task_summary:'[workflow] [summary]', files_touched:[...]})`
   - If key decision → `hsa_session({action:'anchor', content:'[decision]', category:'decision'})`
3. **PERSIST** (if HSA unavailable):
   - Append task summary to `memory/session.md`
   - If last task → Update `memory/CONTEXT_SNAPSHOT.md`
