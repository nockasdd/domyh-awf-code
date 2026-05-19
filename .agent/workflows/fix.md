---
description: "Quick-fix pipeline: capture error, identify, fix, verify (max 60s)"
skills: { required: [error-handling], contextual: [auto] }
success_criteria: "Error resolved, build passes, no regressions"
---

# /fix

## RULES

- R1: Max 60s total — escalate to /debug if exceeded
- R2: Minimal changes only — preserve existing behavior
- R3: Max 2 retry attempts — then escalate
- R4: Run affected tests after every fix

## FIX FLOW

1. **DETECT** (5s) — hsa_session, parse error, hsa_detect(stack), locate file:line, read surrounding code, classify category
2. **EXECUTE** (30s) — LOCATE > UNDERSTAND > SIZE > WRITE > VERIFY. Minimal changes only.
3. **VERIFY** (15s) — Build check, run affected tests. If FAIL: retry (max 2) then escalate to /debug
4. **SYNC** — hsa_check_changes to update index

## COMMANDS

| Command | Description |
|:--------|:------------|
| `/fix [error]` | Fix specific error |
| `/fix last` | Fix last terminal error |
| `/fix build` | Fix build errors |
| `/fix lint` | Fix all lint errors |
| `/fix types` | Fix type errors |
| `/fix imports` | Fix import errors |
| `/fix tests` | Fix failing tests |

## FIX CATEGORIES

| Category | Detect Pattern | Confidence |
|:---------|:---------------|:-----------|
| Syntax | SyntaxError, unexpected token | 95% |
| Types | TypeError, type mismatch, TS errors | 90% |
| Imports | ModuleNotFoundError, Cannot find module | 95% |
| Null safety | Cannot read property of null/undefined | 85% |
| Build | Build failed, compilation error | 80% |
| Lint | ESLint, golangci-lint, ruff | 90% |
| Dependency | Version mismatch, peer dependency | 85% |

## ESCALATION

After 2 retries fail, activate progressive escalation:
1. REFLECT — list attempts, check biases (confirmation, anchoring, tunnel vision)
2. REFRAME — invert assumption, rubber duck, devil's advocate
3. WIDEN — checklist: code, config, env, deps, data, logs
4. DECOMPOSE — minimal reproduction, binary search
5. ESCALATE — full report to user with evidence + recommendations

## SAFETY

- Max changed files: 3, max changed lines: 30
- Confirm if: >3 files, >30 lines, modifies test/config

## CHECKPOINT

1. Verify success_criteria met
2. `hsa_session({action:'persist', task_summary:'...', files_touched:[...]})`
