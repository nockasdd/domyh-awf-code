---
name: delegation-intelligence
description: "Subagent delegation patterns: task decomposition, handoff preparation, result validation, intelligence capture, and error recovery."
detect: []
category: governance
tier: 1
---

# Delegation Intelligence

## Task Decomposition

### Decision Tree: Should I Delegate?

```
Is this task self-contained (clear input → output)?
  NO → Do it yourself or break it down further
  YES ↓

Does it require context from other running tasks?
  YES → Execute sequentially (wait for dependency)
  NO ↓

Is it a well-defined task type? (code/test/review/debug/browser/research)
  NO → Do it yourself
  YES ↓

Delegate with proper handoff packet ✅
```

### Breaking Down Complex Work

| Pattern | When | Example |
|---------|------|---------|
| **By file** | Independent file changes | "Update 5 config files" → 5 parallel tasks |
| **By layer** | Sequential dependencies | "API → Service → Tests" → 3 sequential tasks |
| **By concern** | Mixed independence | "Frontend + Backend + Docs" → parallel |
| **By phase** | Order matters | "Research → Plan → Implement" → sequential |

## Pre-Delegation: Prepare Handoff

### Handoff Packet (Required)

```
hsa_delegate(
  task_type: "code",
  task_description: "Implement JWT middleware with validation and error handling",
  focus_files: ["src/auth/middleware.ts", "tests/auth.test.ts"],
  max_tokens: 2000
)
```

### Handoff Checklist

Every delegation MUST specify:

| Item | Required | Example |
|------|----------|---------|
| **Task** | ✅ | "Implement JWT middleware" (not "figure it out") |
| **Scope** | ✅ | "Only touch src/auth/. Do NOT modify routes." |
| **Return format** | ✅ | "Return: files changed, tests added, verification output" |
| **Success metric** | ✅ | "All tests pass, TypeScript compiles" |
| **Context files** | ✅ | `focus_files: [...]` |
| **Constraints** | 🟡 | "Use jose library. No external auth services." |
| **Style guide** | 🟡 | "Follow existing patterns in src/auth/" |

### Tool Filtering (Reduce Bloat)

```
hsa_delegate(task_type: "code")
# Returns recommended tool include/exclude lists
# → 93-97% token savings in subagent prompt
```

## Cross-Model Cascade

When the primary model isn't optimal for a sub-task, delegate to a specialized model:

```
# 1. List available models
hsa_delegate({action: 'cascade_models'})

# 2. Send cascade
hsa_delegate({
  action: 'cascade',
  cascade_text: '[detailed prompt with all context]',
  task_type: 'code',           # enables dashboard model routing
  cascade_model: 'model-id'    # optional — override dashboard routing
})
# → returns cascade_id

# 3. Poll for response (3-5s intervals, max 10 polls)
hsa_delegate({action: 'cascade_read', cascade_id: '...'})
# → status: pending | complete | error

# 4. Cancel if needed
hsa_delegate({action: 'cascade_cancel', cascade_id: '...'})
```

### When to Cascade vs Do Yourself

| Scenario | Action |
|----------|--------|
| Task within current model's strength | Do yourself |
| Need stronger reasoning (Opus/Pro) | Cascade with task_type:'review' or 'debug' |
| Need fast cheap output (Flash) | Cascade with task_type:'code' |
| Research needing web access | Cascade with task_type:'research' |
| User configured specific model | Cascade — auto-routes via dashboard |

### Mandatory Cascade Evaluation

⚠️ **MUST evaluate before EXECUTE step** in any workflow:

```
Is hsa_delegate MCP tool available?
  NO → Skip cascade, proceed normally
  YES ↓

Quick Complexity Score ≥ 8?
  YES → AUTO-cascade with matched task_type ✅
  NO ↓

Complexity score 5-7?
  YES → SUGGEST cascade to user ↗️
  NO ↓

Workflow-specific trigger? (security=always, debug L3=auto)
  YES → Follow trigger rule ✅
  NO ↓

Scope trigger? (>100 LOC, >5 files, multi-lang)
  YES → SUGGEST cascade ↗️
  NO → Proceed without cascade ✅
```

Key: Agent ALWAYS has final decision. "AUTO" = strong recommendation. "SUGGEST" = informational.

### Quick Complexity Score (H1-H10)

| Score | Criteria | Cascade |
|:------|:---------|:--------|
| 1-3 | Single file, <30 LOC, clear pattern | Skip |
| 4-5 | Single file, 30-100 LOC, moderate logic | Skip |
| 6-7 | Multi-file, 100-200 LOC, moderate complexity | SUGGEST |
| 8-9 | Multi-file, >200 LOC, complex algorithm/architecture | AUTO |
| 10 | Cross-cutting change, >5 files, breaking change risk | AUTO |

### IDE Cascade Support

| IDE | Supported | Method |
|:----|:----------|:-------|
| Antigravity | ✅ Full | LS RPC (session-managed cascade) |
| VS Code + Copilot | ✅ | vscode.lm API (direct model call) |
| VS Code Insiders | ✅ | vscode.lm API |
| Cursor | ⚠️ Unverified | vscode.lm (may work) |
| Windsurf | ❌ | No extension API available |

### Cascade Prompt Guidelines

Include in `cascade_text`:
- **Goal**: What exactly the sub-agent must produce
- **Context**: Relevant code snippets, file paths, error messages
- **Constraints**: Language, framework, style conventions
- **Return format**: Expected output structure

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
