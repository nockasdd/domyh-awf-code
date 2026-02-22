---
name: "pre-stop-checklist"
description: "5-point gate before ending any task or session. Prevents incomplete work, unsaved state, and silent failures."
triggers:
  - "Before claiming task is complete"
  - "Before ending a session"
  - "Before responding 'done' to user"
  - "When user cancels mid-work"
version: "1.0.0"
---

# Pre-Stop Checklist

**Core principle:** Never stop without checking. Incomplete stops compound into lost work.

## The 5-Point Gate

Before ANY "done" claim or session end, verify ALL 5 points:

```
□ 1. BUILD passes?
□ 2. TESTS pass?
□ 3. HIERARCHY updated?
□ 4. SESSION archived?
□ 5. USER notified?
```

### Gate Flow

```
Ready to stop?
    │
    ├── 1. BUILD — Run build command
    │   FAIL → Fix before stopping
    │   PASS ↓
    │
    ├── 2. TESTS — Run test suite
    │   FAIL → Fix or note failures explicitly
    │   PASS ↓
    │
    ├── 3. HIERARCHY — Is progress tracking current?
    │   STALE → Update: hsa_track_progress(status: "completed")
    │   CURRENT ↓
    │
    ├── 4. ARCHIVE — Is session state saved?
    │   NO → Save: hsa_save_anchor(category: "context")
    │   YES ↓
    │
    └── 5. NOTIFY — Does user know the status?
        NO → Report: what's done, what's pending, any issues
        YES → ✅ Safe to stop
```

## Verification Commands by Stack

| Stack | Build | Test |
|-------|-------|------|
| Node/TS | `npm run build` | `npm test` |
| Python | `python -m py_compile` | `pytest` |
| Go | `go build ./...` | `go test ./...` |
| Rust | `cargo build` | `cargo test` |
| .NET | `dotnet build` | `dotnet test` |

## Session Archive Format

```
hsa_save_anchor(
  content: "[SESSION-END] Topic: {what}. Done: {completed}. Pending: {remaining}. Files: {key files}. Build: pass/fail. Tests: X/Y pass.",
  category: "context"
)
```

## Graceful Stop (User Cancel Mid-Work)

When user cancels before work is complete:

```
# 1. IMMEDIATELY save current progress
hsa_save_anchor(
  content: "[INTERRUPTED] Was working on: {task}. Progress: {what's done}. State: {build pass? tests?}. Resume from: {next step}.",
  category: "context"
)

# 2. Update hierarchy with partial status
hsa_track_progress(
  level: "action",
  label: "Interrupted: {what was in progress}",
  status: "blocked"
)

# 3. Brief user on status
# Tell them: what's done, what's not, how to resume
```

## Partial Completion Report

When not everything passed:

```
## Stop Report
- ✅ Build: passes
- ⚠️ Tests: 18/20 pass (2 edge case failures — documented)
- ✅ Hierarchy: updated
- ✅ Session: archived
- ✅ User: notified

Recommendation: P2 fix for remaining test failures.
```

## Red Flags

| Thought | Reality |
|---------|---------|
| "It's obviously done" | Run the checklist. It takes 30 seconds. |
| "I'll save the session later" | Compaction may fire. Save NOW. |
| "The user can see what I did" | They see your summary, not your work. Be explicit. |
| "Tests aren't needed for this" | If you changed code, tests verify you didn't break anything. |
| "I'll just say done" | "Done" without evidence is a claim, not a fact. |
