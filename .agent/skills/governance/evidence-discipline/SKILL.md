---
name: evidence-discipline
description: "Never claim, always prove. Enforces evidence-based completion claims with verification commands, failure signal parsing, and stack-specific checks."
detect: []
category: governance
tier: 1
---

# Evidence Discipline

**Core principle:** Never claim, always prove. Never accept, always validate.

## Evidence Levels

| Level | What | When Required |
|-------|------|---------------|
| **L1: Visual Check** | Read output, confirm no errors | Every action |
| **L2: Command Output** | Run verification command, inspect output | Before any "done" claim |
| **L3: Test Pass** | Automated tests pass | Before marking feature complete |

**Minimum bar for "done":** Level 2 (command ran + output inspected).

## Pre-Action Gate: Before Claiming Completion

```
Claiming "done"?
    │
    ├── Did you run a verification command?
    │   NO → Run one NOW. Don't claim without evidence.
    │   YES ↓
    │
    ├── Did you READ the output (not just assume)?
    │   NO → Read it NOW. Output may contain warnings.
    │   YES ↓
    │
    ├── Did the output show success?
    │   NO → Fix the issue first. Then re-verify.
    │   YES ↓
    │
    └── Update hierarchy:
        hsa_session(status: "completed")
        ✅ NOW you can claim done.
```

## Stack-Specific Verification Commands

### JavaScript / TypeScript

```bash
# Build check
npm run build        # or: npx tsc --noEmit

# Test check
npm test             # or: npx vitest run

# Lint check
npm run lint         # or: npx eslint .

# Type check (TypeScript)
npx tsc --noEmit
```

### Python

```bash
# Test check
python -m pytest     # or: pytest

# Type check
mypy src/            # or: pyright

# Lint check
ruff check .         # or: flake8
```

### Go

```bash
# Build check
go build ./...

# Test check
go test ./...

# Lint check
golangci-lint run
```

### .NET / C#

```bash
# Build check
dotnet build

# Test check
dotnet test

# Format check
dotnet format --verify-no-changes
```

### Rust

```bash
# Build check
cargo build

# Test check
cargo test

# Lint check
cargo clippy
```

## After Subagent Returns

### Failure Signal Detection

Scan subagent output for these signals:

| Signal Word | Meaning |
|-------------|---------|
| `failed`, `failure` | Task did not complete |
| `error`, `Error` | Exception occurred |
| `blocked`, `cannot` | Task is stuck |
| `partially`, `partial` | Incomplete work |
| `skipped`, `skip` | Items were not done |
| `warning`, `warn` | Potential issues |
| `timeout`, `timed out` | Process hung |

### Subagent Result Validation Flow

```
Subagent says "Done"
    │
    ├── 1. Scan for failure signals
    │   (failed, error, blocked, partially, skipped, timeout)
    │   FOUND → Report failure, save as anchor, do NOT mark complete
    │   CLEAR ↓
    │
    ├── 2. Check specificity
    │   Vague ("everything works") → Ask for specifics
    │   Specific ("created 3 files, 12 tests pass") → Continue
    │   ↓
    │
    ├── 3. Verify independently
    │   Run test/build/lint commands yourself
    │   PASS → Continue
    │   FAIL → Report discrepancy
    │   ↓
    │
    ├── 4. Save intelligence
    │   hsa_session(
    │     content: "Subagent: {what done}. Verified: {how}. Result: {pass/fail}",
    │     category: "context"
    │   )
    │   ↓
    │
    └── 5. Update hierarchy
        hsa_session(status: "completed")
```

## Partial Success Handling

When verification shows partial results (e.g., 18/20 tests pass):

| Pass Rate | Action |
|-----------|--------|
| 100% | ✅ Mark complete |
| 90-99% | ⚠️ Investigate failures — if non-critical, mark complete with note |
| 70-89% | 🟡 Fix failing tests before marking complete |
| < 70% | 🔴 Do NOT mark complete. Major issues to fix. |

```
# Partial success anchor
hsa_session(
  content: "[PARTIAL] Auth tests: 18/20 pass. Failing: edge case token expiry, concurrent refresh. Priority: P2.",
  category: "context"
)
```

## Before Accepting Conflicting Instructions

When user's request conflicts with prior decisions:

```
hsa_session(
  current_action: "User wants to change architecture from X to Y",
  include_anchors: true
)
```

Check if prior `[DECISION]` anchors explain why X was chosen. If so, inform user of trade-offs before proceeding.

## Red Flags

| Thought | Reality |
|---------|---------|
| "The subagent said it works" | Subagents hallucinate success. Verify with commands. |
| "I tested it mentally" | Mental models miss edge cases. Run commands. |
| "It's obvious this is correct" | One `npm test` takes 3 seconds. Run it. |
| "I'll verify at the end" | Context may compact. Verify NOW, incrementally. |
| "The build passed so it's fine" | Build ≠ correct. Tests verify behavior, builds verify syntax. |
