---
description: "Autonomous dev loop: understand, implement, verify, de-sloppify, review, commit"
skills: { required: [coding-rules, testing], contextual: [auto] }
success_criteria: "All iterations complete: build+lint+test pass, zero code smells, review approved"
---

# /loop

## RULES

- L1: Max 5 loop iterations — then STOP and report
- L2: Max 3 retries per same failure — then ESCALATE
- L3: NEVER push to remote — commit only, user controls push
- L4: NEVER refactor code outside task scope
- L5: ALWAYS run de-sloppify before commit
- L6: Token budget >80% — summarize + persist + STOP

## LOOP FLOW (7 Phases)

1. **UNDERSTAND** — Read task, hsa_search for related files, hsa_trace_flow for deps, classify SIZE (MICRO/SMALL/MEDIUM/LARGE). LARGE = STOP, break into sub-tasks.
2. **IMPLEMENT** — Follow /code canonical write: LOCATE > UNDERSTAND > SIZE > WRITE > VERIFY. Max 1-3 files per iteration.
3. **VERIFY** — Type check > Lint > Build > Test. If FAIL: auto-fix (max 3). If 3 failures same issue: ESCALATE.
4. **DE-SLOPPIFY** — Remove: console.log/debug, debugger, `any` types, @ts-ignore, eslint-disable (without reason), unused imports.
5. **REVIEW** — If complexity >=6.5: cascade review via hsa_delegate. Else: self-review (intent, edge cases, errors, naming, security).
6. **COMMIT** — git add, conventional commit. DO NOT push.
7. **LOOP or EXIT** — More tasks: goto 1. All done: persist + report. Budget >80%: STOP.

## COMMANDS

| Command | Description |
|:--------|:------------|
| `/loop [task]` | Full autonomous loop |
| `/loop fix [issue]` | Fix-only loop |
| `/loop continue` | Resume interrupted |
| `/loop status` | Show current state |

## EXIT CONDITIONS

| Condition | Action |
|:----------|:-------|
| All tasks complete | persist, success report |
| Max 5 iterations | summarize, STOP |
| 3 failures same issue | ESCALATE to user |
| Token >80% | summarize, persist, STOP |
| User "stop"/"done" | commit pending, persist, STOP |

## DE-SLOPPIFY DETAILS

Remove automatically:
- console.log/debug/warn (except logger files)
- debugger statements
- `: any` type annotations (replace with proper types)
- @ts-ignore/@ts-nocheck (except with documented reason)
- eslint-disable (except with inline reason)
- Unused imports

Flag only (user decides):
- TODO/FIXME/HACK markers
- Empty catch blocks

## CHECKPOINT

1. Verify success_criteria met
2. `hsa_session({action:'persist', task_summary:'...', files_touched:[...]})`
