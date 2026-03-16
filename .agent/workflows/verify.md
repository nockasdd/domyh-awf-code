---
description: "🔄 Verification loop: build → lint → test → validate cycle until all pass"
skills: { required: [testing], contextual: [auto] }
success_criteria: "All pipeline stages pass (type check, lint, build, test)"
---

# 🔄 /verify — Verification Loop

> Automated Build → Lint → Test → Validate cycle
> 📚 Auto-detect • Max 3 iterations • Clear pass/fail reporting

---

## ⛔ THE IRON LAW

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

**Claiming work is complete without verification is dishonesty, not efficiency.**

---

## VERIFICATION GATE FUNCTION (MANDATORY)

<HARD-GATE>
BEFORE claiming ANY status or expressing satisfaction:

1. **IDENTIFY**: What command proves this claim?
2. **RUN**: Execute the FULL command (fresh, complete run)
3. **READ**: Full output — check exit code, count failures
4. **VERIFY**: Does output ACTUALLY confirm the claim?
   - If NO → State actual status with evidence
   - If YES → State claim WITH evidence
5. **ONLY THEN**: Make the claim

Skip any step = lying, not verifying.
</HARD-GATE>

### Common Failures

| Claim | Requires | NOT Sufficient |
|-------|----------|-----------|
| "Tests pass" | Test command output: 0 failures | Previous run, "should pass" |
| "Build succeeds" | Build command: exit 0 | Linter passing, extrapolation |
| "Bug fixed" | Test original symptom passes | "Code changed, assumed fixed" |
| "Lint clean" | Linter output: 0 errors | Partial check |
| "Requirements met" | Line-by-line checklist verified | "Tests passing" |

### Red Flags — STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Done!")
- About to commit/push without verification
- Relying on partial verification
- ANY wording implying success without running commands

### Rationalization Prevention

| Excuse | Reality |
|--------|--------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Linter passed" | Linter ≠ compiler ≠ runtime |
| "I'm tired" | Exhaustion ≠ excuse |
| "Partial check is enough" | Partial proves nothing |

---

## VERIFY FLOW

1. **DETECT** — Detect stack via HSA (`hsa_detect`), identify build system, linter, test runner. Show: `[Step 1/5] Detecting verification pipeline...`
2. **RUN** — Execute verification pipeline sequentially. Show: `[Step 2/5] Running 4-stage pipeline...`
3. **FIX** — Auto-fix what's possible (lint, format). Show: `[Step 3/5] Auto-fixing 3 lint issues...`
4. **RE-RUN** — Loop until all pass or max iterations. Show: `[Step 4/5] Iteration 2/3 — All checks passed ✅`
5. **SYNC** — `hsa_check_changes` to update index after auto-fixes

---

## COMMANDS

| Command              | Description                  |
| -------------------- | ---------------------------- |
| `/verify`            | Full verification pipeline   |
| `/verify build`      | Build check only             |
| `/verify lint`       | Lint check only              |
| `/verify test`       | Test check only              |
| `/verify quick`      | Type-check + lint (no tests) |
| `/verify pre-commit` | Pre-commit hook verification |

---

## VERIFICATION PIPELINE

```
┌─────────────────────────────────────────────────┐
│  Stage 1: TYPE CHECK                            │
│  ├── TypeScript: tsc --noEmit                   │
│  ├── Python: mypy / pyright                     │
│  ├── Go: go vet ./...                           │
│  └── Rust: cargo check                          │
├─────────────────────────────────────────────────┤
│  Stage 2: LINT                                  │
│  ├── ESLint / Biome (JS/TS)                     │
│  ├── Ruff / Flake8 (Python)                     │
│  ├── golangci-lint (Go)                         │
│  └── clippy (Rust)                              │
├─────────────────────────────────────────────────┤
│  Stage 3: BUILD                                 │
│  ├── npm run build / next build                 │
│  ├── go build ./...                             │
│  ├── cargo build                                │
│  └── dotnet build                               │
├─────────────────────────────────────────────────┤
│  Stage 4: TEST                                  │
│  ├── Unit tests                                 │
│  ├── Integration tests                          │
│  └── Coverage report                            │
└─────────────────────────────────────────────────┘
```

---

## ITERATION RULES

| Rule             | Value                                  |
| ---------------- | -------------------------------------- |
| Max iterations   | 3                                      |
| Auto-fix enabled | Lint + format only                     |
| Stop on          | Build failure (can't proceed to tests) |
| Success          | All 4 stages green                     |
| Failure          | Report remaining issues after 3 tries  |

---

## AUTO-FIX CAPABILITIES

| Issue Type     | Can Auto-Fix        | Tool                     |
| -------------- | ------------------- | ------------------------ |
| Formatting     | ✅ Yes              | Prettier, gofmt, rustfmt |
| Lint warnings  | ✅ Yes (safe rules) | ESLint --fix, Ruff --fix |
| Import sorting | ✅ Yes              | isort, organize-imports  |
| Type errors    | ❌ No               | Requires manual fix      |
| Test failures  | ❌ No               | Requires code fix        |
| Build errors   | ❌ No               | Requires code fix        |

---

## OUTPUT FORMAT

```
🔄 Verification Loop — Iteration 1/3

  ✅ Type Check   — 0 errors
  ⚠️  Lint         — 3 warnings (auto-fixed 2, 1 remaining)
  ✅ Build        — Success (4.2s)
  ❌ Tests        — 47/48 passed (1 failed)

🔧 Auto-fixed:
  - Removed unused import (src/utils.ts:3)
  - Fixed semicolon (src/api.ts:15)

❌ Remaining (manual fix needed):
  - test_user_create_duplicate — Expected 409, got 500

🔄 Re-running after fix... Iteration 2/3

  ✅ Type Check   — 0 errors
  ✅ Lint         — 0 warnings
  ✅ Build        — Success (4.1s)
  ✅ Tests        — 48/48 passed

✅ ALL CHECKS PASSED — Ready to commit
```
---

## REFLECTION CHECKPOINT

⛔ **MANDATORY** — Execute before completing this workflow (SESSION_005):

1. **VERIFY** — Does output meet success_criteria (see YAML frontmatter)?
2. **PERSIST** (if HSA available — preferred, 1 tool call):
   - `hsa_session({action:'persist', task_summary:'[workflow] [summary]', files_touched:[...]})`
   - If key decision → `hsa_session({action:'anchor', content:'[decision]', category:'decision'})`
3. **PERSIST** (if HSA unavailable — manual fallback):
   - Append task summary to `memory/session.md`
   - If last task → Update `memory/CONTEXT_SNAPSHOT.md`

