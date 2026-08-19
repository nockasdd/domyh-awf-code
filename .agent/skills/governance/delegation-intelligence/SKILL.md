---
name: delegation-intelligence
description: "Subagent delegation patterns: task decomposition, handoff preparation, result validation, intelligence capture, and error recovery."
detect: []
category: governance
tier: 1
---

# Delegation Intelligence

> **Philosophy**: Subagent-Driven Development (SDD) + 2-Tier Review Gate + Workspace Isolation (inspired by *obra/superpowers*).

## 1. Task Decomposition & The 1% Trigger Gate

### 1% Trigger Gate: When to Delegate
If there is even a 1% chance that the task requires multi-domain coordination, cross-file refactoring, or independent verification:
- **Do NOT** jump straight into monolithic implementation.
- **Force** decomposition into **bite-sized subtasks (2–5 minutes runtime)**.
- **Prepare** a formal Task Contract before dispatching.

```
Is task single-file & < 30 LOC?
  YES → Execute directly in main agent ✅
  NO ↓

Does it span multiple domains / files / concerns?
  YES → Generate SDD DAG (Task Decomposition)
  ↓

Is hsa_delegate available?
  YES → Call hsa_delegate({action:'prepare', task_type:'...', focus_files:[...]})
  NO → Prepare manual handoff packet
```

### Breaking Down Complex Work into Bite-Sized Tasks

| Pattern | When | Sizing Rule | Example |
|---|---|---|---|
| **By File / Component** | Independent file logic | Max 1-2 files per subtask | "Build Auth Token Generator" $\rightarrow$ `src/auth/jwt.ts` + `tests/jwt.test.ts` |
| **By Layer (TDD)** | Sequential pipeline | Red (Test) $\rightarrow$ Green (Impl) | 1. Write tests $\rightarrow$ 2. Implement logic $\rightarrow$ 3. Refactor |
| **By Concern** | Cross-cutting features | Parallel isolated tasks | Frontend Component + Backend API + Migration script |
| **By Audit / Quality** | Verification & Security | Read-only specialist | Security audit or Performance profiling |

---

## 2. Pre-Delegation: SDD Task Contract

Every subagent MUST receive an immutable, explicit contract:

```typescript
// 1. Call MCP to prepare contract & get native dispatch instructions
hsa_delegate({
  action: "prepare",
  task_type: "code", // code | test | review | debug | browser | research
  task_description: "Implement JWT middleware with expiration and role checking",
  focus_files: ["src/auth/middleware.ts", "tests/auth/middleware.test.ts"],
  workspace_mode: "branch", // branch | share | inherit
  acceptance_criteria: {
    tdd_stage: "red_to_green",
    required_tests: ["should verify valid token", "should reject expired token"],
    lint_check: "npm run lint",
    build_check: "tsc --noEmit"
  }
})
```

### Handoff Contract Checklist

| Field | Requirement | Description |
|---|---|---|
| **Task Description** | ✅ Required | Concrete, bite-sized goal (not open-ended research) |
| **Focus Files** | ✅ Required | Exact list of allowed files to touch (Surgical containment) |
| **Tool Policy** | ✅ Required | Recommended & restricted tools (reduces context bloat by 90%+) |
| **Acceptance Criteria** | ✅ Required | Exact verification commands, tests, and lint rules |
| **Workspace Mode** | ✅ Required | `branch` (isolated worktree), `share`, or `inherit` |

---

## 3. Multi-Platform Native Dispatch

Always use the **Native Subagent Engine** of the active platform first:

### A. Antigravity (Google DeepMind)
Use native `invoke_subagent` tool with workspace branching:
```json
{
  "Subagents": [{
    "TypeName": "self",
    "Role": "DEVELOPER [code]",
    "Prompt": "[TASK CONTRACT: sdd_code_...]\nImplement JWT middleware in src/auth/middleware.ts.\nOnly touch focus files. Run tests to verify.",
    "Workspace": "branch"
  }]
}
```

### B. Claude Code (Anthropic)
Use `.claude/agents/` definitions and Git worktree isolation:
- Launch subagent in isolated git worktree: `git worktree add -b task-auth ../worktrees/auth`
- Provide strict prompt with focus files and acceptance criteria.

### C. OpenAI Codex / CLI
Use `AGENTS.md` persona routing with scoped directory execution:
- Restrict file access to `focus_files`.

### D. Cursor & MCP Fallback
If native subagents are unavailable, fallback to `hsa_delegate`:
```typescript
// Dispatch cascade
hsa_delegate({ action: "cascade", cascade_text: "...", task_type: "code" })
// Poll transcript
hsa_delegate({ action: "cascade_read", cascade_id: "..." })
```

---

## 4. Post-Execution: 2-Tier Quality Review Gate

Never trust subagent assertions ("I have finished successfully"). Always run the 2-Tier Gate:

```
Subagent Deliverable Returned
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│ TIER 1: SPEC COMPLIANCE REVIEW (Scope Containment)          │
│ • Call: hsa_delegate({                                      │
│     action: "verify",                                       │
│     focus_files: ["src/auth/middleware.ts"],                │
│     modified_files: ["src/auth/middleware.ts"]              │
│   })                                                        │
│ • PASS: All edits strictly within focus scope               │
│ • FAIL: Out-of-scope files modified → REJECT & REVERT       │
└──────────────────────────────┬──────────────────────────────┘
                               │ PASS
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ TIER 2: CODE QUALITY & TDD VERIFICATION                     │
│ • Run test suite (npm test / pytest / cargo test)           │
│ • Run typechecker (tsc --noEmit) & linter (eslint)          │
│ • Inspect diff for surgical precision (no formatting churn) │
│ • PASS: 100% tests green, 0 errors                          │
│ • FAIL: Re-dispatch correction or fix failing assertion     │
└──────────────────────────────┬──────────────────────────────┘
                               │ PASS
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ MERGE & PERSIST INTELLIGENCE                                │
│ • Merge branched workspace into main                        │
│ • hsa_session({ action: "persist", task_summary: "..." })   │
│ • hsa_check_changes to sync Merkle search index             │
└─────────────────────────────────────────────────────────────┘
```

## Parallel vs Sequential

| Pattern | When | How | Risk |
|---------|------|-----|------|
| **Parallel** | Independent tasks, no shared files | Dispatch simultaneously | File conflicts |
| **Sequential** | Task B needs Task A's output | Wait for A, verify, then B | Slower |
| **Fan-out** | Same task, different files | Parallel with per-file scope | Low |
| **Pipeline** | Transform chain | Output A → Input B | Error cascade |

### Independence Test

Before running parallel:

```
Task A files: [auth.ts, auth.test.ts]
Task B files: [user.ts, user.test.ts]

Overlap? → NO → Safe to parallel ✅
Overlap? → YES → Sequential or merge into one task
```

**Rule:** If unsure, default to sequential. Parallel requires independence proof.

## Post-Delegation: Validate + Capture

### Result Parsing Protocol

```
Subagent returns result
    │
    ├── 1. Scan for failure signals
    │   Keywords: failed, error, blocked, partially, skipped, timeout
    │   FOUND → Do NOT mark complete
    │   CLEAR ↓
    │
    ├── 2. Check completeness
    │   Did subagent address ALL items in task description?
    │   MISSING items → Note what's missing
    │   ALL addressed ↓
    │
    ├── 3. Check specificity
    │   Vague output ("everything works") → Ask for details
    │   Specific output ("3 files, 12 tests") → Continue
    │   ↓
    │
    ├── 4. Verify independently
    │   Run build/test/lint yourself
    │   Read generated code — don't trust blindly
    │   PASS → Continue
    │   FAIL → Report discrepancy
    │   ↓
    │
    ├── 5. Capture intelligence
    │   hsa_session(
    │     content: "[SUBAGENT] Task: {what}. Result: {outcome}. Files: {changed}. Tests: {pass/fail}",
    │     category: "context"
    │   )
    │   ↓
    │
    └── 6. Update hierarchy
        hsa_session(level: "action", label: "{task}", status: "completed")
```

### Intelligence Capture Format

```
hsa_session(
  content: "[SUBAGENT] JWT middleware delegation.
    Task: Implement token validation + error handling.
    Result: 2 files created, 12 tests pass.
    Files: src/auth/middleware.ts, tests/auth.test.ts.
    Library: jose (as specified).
    Notes: Added token refresh handling (not requested but useful).",
  category: "context"
)
```

## Error Recovery

### When Subagent Fails

```
Subagent reports failure
    │
    ├── 1. Save failure intelligence
    │   hsa_session(
    │     content: "[FAIL] Task: {what}. Error: {error}. Attempted: {what subagent tried}",
    │     category: "context"
    │   )
    │   ↓
    │
    ├── 2. Assess retry viability
    │   Was it a transient error? (timeout, network) → Retry once
    │   Was it a logic error? (wrong approach) → Modify task description
    │   Was it a scope error? (too complex) → Break into smaller tasks
    │   ↓
    │
    ├── 3. Retry or escalate
    │   Retry: Re-dispatch with clarified instructions
    │   Escalate: Do it yourself or ask user
    │   ↓
    │
    └── 4. Max retries: 2
        After 2 failures → do it yourself or report to user
```

### Retry Protocol

```
# Modified retry with more context
hsa_delegate(
  task_type: "code",
  task_description: "RETRY: Implement JWT middleware. Previous attempt failed because: {reason}. Additional context: {what to do differently}.",
  focus_files: ["src/auth/middleware.ts"],
  max_tokens: 3000  # More context for retry
)
```

## Multi-Delegation Coordination

When managing multiple parallel subagents:

```
# 1. Dispatch all
dispatch(Task A → Subagent 1)
dispatch(Task B → Subagent 2)
dispatch(Task C → Subagent 3)

# 2. Collect results (as they return)
# Validate each independently using Result Parsing Protocol

# 3. Integration check
# After all return: run full build + test suite
# Individual successes ≠ combined success

# 4. Save combined intelligence
hsa_session(
  content: "[DELEGATION] 3 tasks parallel. A: done. B: done. C: partial. Integration: pass.",
  category: "context"
)
```

## Red Flags

| Thought | Reality |
|---------|---------|
| "The subagent said done, moving on" | Parse the result. Check for failure signals. Verify. |
| "I'll capture intelligence later" | Compaction may fire before later. Save NOW. |
| "This failure is minor" | Unacknowledged failures compound. Address it. |
| "I know what the subagent did" | Prove it with verification commands. |
| "These tasks are probably independent" | Prove independence before parallelizing. Check file overlap. |
| "One retry should be enough" | Set max retries. After 2 failures, change approach. |
