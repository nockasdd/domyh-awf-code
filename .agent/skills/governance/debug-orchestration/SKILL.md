---
name: "debug-orchestration"
description: "Systematic 5-phase debug process: Reproduce → Isolate → Analyze → Fix → Verify. Hypothesis tracking, evidence journal, escalation timeout."
triggers:
  - "When debugging complex or multi-component issues"
  - "When a bug persists after initial fix attempt"
  - "When error root cause is unclear"
  - "When debugging spans multiple files or services"
version: "1.0.0"
---

# Debug Orchestration

**Core principle:** Debug systematically, not randomly. Track hypotheses. Escalate when stuck.

## The 5-Phase Debug Protocol

```
REPRODUCE → ISOLATE → ANALYZE → FIX → VERIFY
```

### Phase 1: Reproduce 🔄

**Goal:** Confirm the bug exists and create a reliable reproduction.

```
# 1. Get exact error message / behavior
# 2. Identify reproduction steps
# 3. Run reproduction to confirm

# Track in hierarchy
hsa_track_progress(level: "tactic", label: "Debug: Reproducing {bug}")
```

| Checklist | |
|-----------|--|
| Error message captured verbatim? | □ |
| Reproduction steps documented? | □ |
| Bug confirmed reproducible? | □ |
| Environment details noted? | □ |

### Phase 2: Isolate 🔍

**Goal:** Narrow down WHERE the bug occurs.

```
# Strategies (try in order):
# 1. Binary search — comment out half the code
# 2. Trace flow — follow data through the system
# 3. Diff — what changed since it last worked?
# 4. Minimal repro — strip down to smallest failing case
```

```
hsa_trace_flow(
  entry_point: "suspectedFunction",
  direction: "downstream",
  depth: 3
)
```

### Phase 3: Analyze 🧠

**Goal:** Understand the ROOT CAUSE (not just the symptom).

#### Hypothesis Tree

Rank hypotheses by likelihood:

```
Bug: Login returns 401 unexpectedly
├── H1 (70%): Token validation failing — expired token?
├── H2 (20%): Middleware order wrong — auth before CORS?
└── H3 (10%): Database connection timeout — pool exhausted?
```

#### Evidence Journal

For each hypothesis, log evidence:

| Hypothesis | Test | Result | Verdict |
|-----------|------|--------|---------|
| H1: Token expired | Check token expiry time | Token valid for 1h, bug occurs at 30min | ❌ Rejected |
| H2: Middleware order | Log middleware execution order | Auth runs before body parser | ✅ Confirmed |
| H3: DB timeout | Check connection pool | Pool at 5/100 | ❌ Rejected |

```
# Save confirmed root cause
hsa_save_anchor(
  content: "[BUG] Login 401. Root cause: middleware order — auth before body-parser. Fix: reorder in app.ts",
  category: "context"
)
```

### Phase 4: Fix 🔧

**Goal:** Fix the root cause, not just the symptom.

```
# Rules:
# 1. Fix the ROOT CAUSE, not the symptom
# 2. Minimal change — don't refactor while debugging
# 3. Add a test that catches this specific bug
# 4. Document the fix in the evidence journal
```

```
hsa_track_progress(
  level: "action",
  label: "Fix applied: {what was changed}"
)
```

### Phase 5: Verify ✅

**Goal:** Confirm the fix works and didn't break anything.

```
# 1. Original repro no longer fails
# 2. New test passes
# 3. Full test suite passes
# 4. Build passes

# Stack-specific verification
npm test   # or equivalent
npm run build

hsa_track_progress(
  level: "action",
  label: "Verified: bug fixed, tests pass",
  status: "completed"
)
```

## Multi-Component Debug

When bug spans multiple files/services:

```
# 1. Map the data flow
hsa_trace_flow(entry_point: "apiEndpoint", direction: "downstream", depth: 4)

# 2. Insert checkpoints at boundaries
#    - API → Service boundary
#    - Service → Database boundary
#    - Frontend → API boundary

# 3. Identify which boundary fails
# 4. Focus debug on that boundary
```

## Escalation Timeout

| Time Spent | Action |
|-----------|--------|
| 0-10 min | Normal debugging — follow 5 phases |
| 10-20 min | **REFLECT** — Re-read the error. Check assumptions. |
| 20-30 min | **REFRAME** — Try a completely different hypothesis. |
| 30-45 min | **WIDEN** — Search docs, issues, Stack Overflow. |
| 45+ min | **ESCALATE** — Ask user for help. Share evidence journal. |

```
# At 30-min mark: save progress
hsa_save_anchor(
  content: "[DEBUG-STUCK] Bug: {description}. Tried: {hypotheses tested}. Rejected: {what didn't work}. Current theory: {best guess}.",
  category: "context"
)
```

## Red Flags

| Thought | Reality |
|---------|---------|
| "Let me just try random fixes" | Systematic beats random. Follow the 5 phases. |
| "I know what the problem is" | You had a hypothesis. Test it. Don't assume. |
| "This fix probably works" | Probably ≠ verified. Run tests. |
| "I've been debugging this for an hour" | You should have escalated at 45 min. |
| "It works on my machine" | Check environment differences. Reproduce in target. |
