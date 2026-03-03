---
name: "session-lifecycle"
description: "Session backbone: declare → track → [work] → archive. Full lifecycle using HSA governance tools with concrete examples."
triggers:
  - "At session start (no intent declared)"
  - "When switching focus or direction"
  - "Before ending session or compacting context"
  - "When resuming after a gap"
---

# Session Lifecycle

## The Backbone

Every productive session follows one pattern:

```
declare_intent → track_progress → [work] → check_drift → archive
```

Skip any phase and you lose governance: no drift detection, no progress tracking, no session continuity.

## Phase 1: Declare (Session Start)

**ALWAYS declare before writing code.**

```
hsa_session(
  focus: "Build authentication system with JWT",
  mode: "plan_driven",
  goals: ["JWT middleware", "Login endpoint", "Integration tests"]
)
```

### Mode Selection Guide

| Mode | When | Example |
|------|------|---------|
| `plan_driven` | New features, multi-step work | "Build auth system" |
| `bugfix` | Known issue, fix + verify | "Fix login 401 error" |
| `exploration` | Research, spike, investigation | "Evaluate ORM options" |
| `refactor` | Restructure without behavior change | "Extract service layer" |

### Decision Tree

```
Is this fixing a known bug?
  YES → mode: "bugfix"
  NO  → Is this research/investigation?
    YES → mode: "exploration"
    NO  → Is this restructuring existing code?
      YES → mode: "refactor"
      NO  → mode: "plan_driven"
```

### Goal Writing Rules

- **Be concrete**: "JWT middleware" not "auth stuff"
- **Be verifiable**: Each goal should have a clear "done" state
- **Be scoped**: 3-5 goals max per session
- **Include tests**: If building feature, include test goal

## Phase 2: Track (During Work)

### 3-Level Hierarchy

| Level | When | Cadence | Example |
|-------|------|---------|---------|
| `trajectory` | Major goal started | 1-2 per session | "Auth system" |
| `tactic` | Sub-task started | Every 3-5 actions | "JWT validation middleware" |
| `action` | Leaf step done | Every meaningful step | "Write middleware test" |

### Concrete Examples

```
# Starting major goal
hsa_session(
  level: "trajectory",
  label: "Authentication system with JWT"
)
# Returns: t1

# Starting sub-task
hsa_session(
  level: "tactic",
  label: "JWT validation middleware",
  parent_id: "t1"
)
# Returns: t1.1

# Completing leaf step
hsa_session(
  level: "action",
  label: "Created auth.middleware.ts with token validation",
  parent_id: "t1.1",
  status: "completed"
)

# Completing sub-task
hsa_session(
  level: "tactic",
  label: "JWT validation middleware",
  parent_id: "t1",
  status: "completed"
)
```

### Checkpoint Cadence

| Task Complexity | Checkpoint Every | Example |
|----------------|-----------------|---------|
| Simple (1-2 files) | Every 3 actions | Fix typo, update config |
| Medium (3-5 files) | Every 5 actions | Add endpoint, write tests |
| Complex (6+ files) | Every 3-4 actions | New feature, refactor |

**Rule:** If you haven't updated hierarchy in 5+ turns, update NOW.

## Phase 3: Drift Check

### Before Concluding Any Task

```
hsa_session(
  current_action: "About to mark JWT middleware complete"
)
```

### Reading Drift Report

The drift report contains:
- **Alignment score**: How well current action matches declared intent
- **Progress summary**: What's done vs what's pending
- **Anchors**: Saved decisions and context

### When Drift Is Detected

```
# Drift report shows misalignment
# 1. Check if drift is intentional (scope change)
# 2. If intentional → re-declare intent
hsa_session(
  focus: "Changed scope: now adding OAuth alongside JWT",
  mode: "plan_driven",
  goals: ["JWT middleware", "OAuth provider", "Login endpoint"]
)

# 3. If unintentional → re-align
hsa_session(
  level: "action",
  label: "Re-aligning: returning to JWT middleware (drifted to UI work)"
)
```

## Phase 4: Archive (Session End)

### Session Summary Anchor

Save session state for next session pickup:

```
hsa_session(
  content: "[SESSION] Auth system. Done: JWT middleware + 12 tests pass. Pending: Login endpoint, OAuth. Key files: src/auth/middleware.ts, tests/auth.test.ts. Blockers: none.",
  category: "context"
)
```

### Session Summary Format

```
[SESSION] {topic}.
Done: {completed items}.
Pending: {remaining items}.
Key files: {important files}.
Blockers: {any blockers}.
Decisions: {key decisions made}.
```

## Multi-Session Continuity

### When Work Spans Multiple Sessions

```
# Session 1 end: Save state
hsa_session(
  content: "[SESSION] Auth system week 1. Done: JWT + tests. Pending: OAuth, Login UI. Decision: jose library for JWT.",
  category: "context"
)

# Session 2 start: Resume
hsa_session(
  current_action: "Resuming auth system work",
  include_anchors: true
)

# Read context anchors → declare intent
hsa_session(
  focus: "Continuing auth system: OAuth + Login UI (JWT done in prior session)",
  mode: "plan_driven",
  goals: ["OAuth provider integration", "Login UI", "E2E tests"]
)
```

## Resume Protocol (After Gap)

1. `hsa_session(include_anchors: true)` — retrieve prior state
2. Read `[SESSION]` anchors from output — understand where you left off
3. Read `[DECISION]` anchors — don't re-debate
4. `hsa_session` with focus referencing prior work
5. Continue from where you left off — not from scratch

## Red Flags

| Thought | Reality |
|---------|---------|
| "I'll declare intent later" | Drift detection is OFF until you do. |
| "This is just a quick fix" | Quick fixes compound. Use `mode: "bugfix"`. |
| "I'll archive at the end" | Context may compact before end. Archive incrementally. |
| "I don't need to track this" | If it takes >3 steps, track it. |
| "The hierarchy is too detailed" | Under-tracking leads to drift. Over-tracking is harmless. |
