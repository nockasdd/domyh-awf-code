---
description: "Fix existing project: detect stack, analyze issues, plan, execute, verify"
skills: { required: [coding-rules], contextual: [auto] }
success_criteria: "Issues fixed, lint/type/test pass, debt score improved"
---

# /modify

## RULES

- R1: STOP after PLAN — confirm scope with user before executing
- R2: Never modify production config without backup
- R3: Run lint/type check after every change batch
- R4: Preserve existing behavior unless explicitly asked to change
- R5: Document breaking changes in commit message

## MODIFICATION FLOW

1. **DETECT** — hsa_session, hsa_detect, identify architecture, map structure
2. **ANALYZE** — Scan by priority: Security P0 > Dependencies P0-P1 > Quality P1-P2 > Performance P2 > Tests P2 > Debt P2-P3
3. **PLAN** — Group by priority with file:line refs. STOP: "Select scope: [1] Fix ALL | [2] P0+P1 | [3] P0 only | [4] Interactive"
4. **EXECUTE** — Apply fixes per approved scope. Track: issue > file:line > before/after > reason.
5. **VERIFY** — Lint > type check > tests > build. Show pass/fail summary.
6. **REPORT** — Fixed count, files changed, lines +/-, debt score before/after. hsa_check_changes.

## COMMANDS

| Command | Description |
|:--------|:------------|
| `/modify` | Full analysis and fix |
| `/modify --security` | Security-focused scan |
| `/modify --deps` | Outdated/vulnerable deps |
| `/modify --quality` | Lint, types, smells |
| `/modify --perf` | Bottlenecks, N+1 |
| `/modify --quick` | P0 only, no confirm |
| `/modify ./src` | Directory-scoped scan |
| `/modify debt score` | Calculate debt score |

## ISSUE CATEGORIES

| Category | Priority | What to Check |
|:---------|:---------|:--------------|
| Security | P0 | Hardcoded secrets, SQL injection, XSS, insecure deps |
| Dependencies | P0-P1 | Outdated, vulnerable, unused, license issues |
| Code Quality | P1-P2 | Lint errors, type errors, dead code, complexity |
| Performance | P2 | N+1 queries, memory leaks, missing indexes |
| Tests | P2 | Missing coverage, failing, flaky |
| Tech Debt | P2-P3 | TODO/FIXME, deprecated APIs, legacy patterns |

## PRIORITY MATRIX

| Priority | Description | Action |
|:---------|:------------|:-------|
| P0 | Critical security/breaking | Must fix now |
| P1 | High impact bugs | Should fix this session |
| P2 | Medium quality issues | Queue next |
| P3 | Low improvements | Backlog |

## CHECKPOINT

1. Verify success_criteria met
2. `hsa_session({action:'persist', task_summary:'...', files_touched:[...]})`
