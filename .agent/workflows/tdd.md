---
description: "TDD cycle: Red-Green-Refactor with automatic test verification"
skills: { required: [tdd-workflow, testing], contextual: [auto] }
success_criteria: "All tests pass green, coverage meets target, refactor clean"
---

# /tdd

## IRON LAW

NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.
Write code before test? Delete it. Start over. No exceptions.

## RULES

1. NEVER write production code without a failing test
2. Write ONLY enough test to fail (one assertion)
3. Write ONLY enough code to pass (no more)
4. Refactor ONLY when green (all tests pass)
5. Commit after EVERY green phase

## TDD FLOW

1. **SETUP** — hsa_detect(stack), load TDD skill, identify test framework
2. **RED** — Write ONE failing test defining expected behavior. Run to confirm fail.
3. **GREEN** — Write SIMPLEST code to pass. Hardcoding OK if only one test.
4. **REFACTOR** — Clean up without changing behavior. Re-run all tests.
5. **VERIFY** — Full test suite, check coverage delta.
6. **SYNC** — hsa_check_changes to update index

## PHASE DETAILS

RED (max 5 min):
- One test case, one assertion
- Must FAIL. If passes: wrong test, delete and rethink.
- If errors (syntax/import): fix infrastructure, not logic.

GREEN (max 10 min):
- Simplest code to pass. Don't generalize yet.
- If still fails: fix, don't add new tests.

REFACTOR (max 5 min):
- Remove duplication, improve naming, extract if needed.
- All tests MUST still pass.

## COMMANDS

| Command | Description |
|:--------|:------------|
| `/tdd [feature]` | Full TDD cycle |
| `/tdd red [test]` | Write failing test only |
| `/tdd green` | Implement minimal code |
| `/tdd refactor` | Refactor phase |
| `/tdd cycle [n]` | Run n cycles |

## RED FLAGS (STOP and start over)

- "I'll just write the function first, then test"
- "This is obvious, doesn't need a test"
- "Let me get the code working, then add tests"

ALL mean: STOP. Delete code. Write test first.

## CHECKPOINT

1. Verify success_criteria met
2. `hsa_session({action:'persist', task_summary:'...', files_touched:[...]})`
