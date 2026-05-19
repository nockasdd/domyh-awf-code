---
description: "Write production-ready code, fix/improve existing projects"
skills: { required: [coding-rules], contextual: [auto, domyh-design, tailwind] }
success_criteria: "Feature implemented, build passes, tests written"
---

# /code

## RULES

- R1-R5 Security: validate input, no hardcoded secrets, parameterized queries, XSS prevention, RBAC
- R6-R9 Quality: error handling at boundaries, types for public APIs, constants over magic numbers, tests >70%
- R10 Context: read + trace dependencies BEFORE modifying
- R11 Safety: STOP if >50 lines change — confirm with user

## CODE FLOW

1. **DETECT**
   - Parse intent: feature / bugfix / refactor
   - `hsa_detect(stack)`, `hsa_search(skills)` for language patterns
   - UI intent: T1 (new) load domyh-design | T2 (modify) hsa_design(analyze) | T3 route to /visualize

2. **PLAN**
   - Break into steps, `hsa_prefetch` planned files
   - STOP if >50 lines — confirm with user
   - List assumptions (scope, format, technology, constraints) — STOP if uncertain

3. **PRE-CHECK** (hard gate)
   - Quote key criteria from requirement
   - List 3+ test cases, 2+ edge cases
   - If auth/secrets: security review notes
   - If breaking: list affected consumers with file:line

4. **EXECUTE**
   - Read target files BEFORE editing
   - hsa_trace_flow for modified functions
   - Check imports/exports dependencies
   - Write protocol: LOCATE > UNDERSTAND > SIZE > WRITE > VERIFY
   - Auto test loop: write > run > fix (max 3)

5. **VERIFY**
   - Run tests, lint, build
   - Self-review: intent match, edge cases, naming, security
   - UI gate (if applicable): accessibility + visual + responsive score

6. **SYNC**
   - `hsa_check_changes` to update index
   - Output: summary, confidence (1-10), next steps

## SUB-COMMANDS

| Command | Mode |
|:--------|:-----|
| `/code [task]` | Create |
| `/code fix [issue]` | Fix |
| `/code improve [area]` | Refactor |
| `/code add [feature]` | Update |
| `/code test [feature]` | Test only |

## CASCADE

Auto (score >=6.5, >200 LOC): `hsa_delegate({action:'cascade', task_type:'code'})`
Suggest (score 4-6.5, >100 LOC): ask user first.

## CHECKPOINT

1. Verify success_criteria met
2. `hsa_session({action:'persist', task_summary:'...', files_touched:[...]})`
