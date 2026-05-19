---
description: "Verification loop: build, lint, test, validate cycle until all pass"
skills: { required: [testing], contextual: [auto] }
success_criteria: "All pipeline stages pass (type check, lint, build, test)"
---

# /verify

## IRON LAW

NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE.
Claiming work is complete without verification is dishonesty, not efficiency.

## VERIFICATION GATE (MANDATORY)

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete run)
3. READ: Full output — check exit code, count failures
4. VERIFY: Does output ACTUALLY confirm the claim?
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying.

## RULES

- R1: Max 3 iterations — then report failures to user
- R2: Auto-fix lint/format issues only. Type/test errors need analysis.
- R3: Never claim "tests pass" without showing command output
- R4: Never use "should", "probably", "seems to" — show evidence

## VERIFY FLOW

1. **DETECT** — hsa_detect(stack) to identify correct commands
2. **TYPE CHECK** — tsc --noEmit / mypy / go vet / cargo check
3. **LINT** — eslint / ruff / golangci-lint (auto-fix enabled)
4. **BUILD** — npm run build / go build / cargo build
5. **TEST** — npm test / pytest / go test
6. **REPORT** — Pass/fail per stage with evidence

If any stage fails: fix > re-run (max 3). If 3 failures: report to user.

## COMMANDS

| Command | Description |
|:--------|:------------|
| `/verify` | Full pipeline |
| `/verify types` | Type check only |
| `/verify lint` | Lint only |
| `/verify build` | Build only |
| `/verify tests` | Tests only |
| `/verify --fix` | Auto-fix and re-run |

## RED FLAGS (STOP)

- Using "should", "probably", "seems to" before verification
- Expressing satisfaction before running commands
- About to commit/push without verification
- Relying on partial verification

## CHECKPOINT

1. Show pass/fail evidence for each stage
2. `hsa_session({action:'persist', task_summary:'...'})`
