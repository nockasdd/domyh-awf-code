---
description: "🧪 TDD cycle: Red-Green-Refactor with automatic test verification loop"
skills: { required: [tdd-workflow, testing], contextual: [auto] }
success_criteria: "All tests pass green, coverage meets target, refactor clean"
---

# 🧪 /tdd — Test-Driven Development

> Red-Green-Refactor Loop with Auto-Verification
> 📚 12 Languages • BDD/ATDD • Mutation Testing

---

## TDD FLOW

1. **SETUP** — Detect stack via HSA (`hsa_detect`), load TDD skill, load test context (`hsa_search`), identify test framework. Show: `[Step 1/6] Detecting stack and test framework...`
2. **RED** — Write a failing test that defines the expected behavior. Run tests to confirm it fails. Show: `[Step 2/6] 🔴 RED — Writing failing test: test_[feature]`
3. **GREEN** — Write the SIMPLEST production code that makes the test pass. Show: `[Step 3/6] 🟢 GREEN — Implementing minimal code to pass`
4. **REFACTOR** — Clean up code and tests without changing behavior. Re-run tests. Show: `[Step 4/6] 🔵 REFACTOR — Cleaning up (all tests still green)`
5. **VERIFY** — Run full test suite, check coverage delta. Show: `[Step 5/6] ✅ Coverage: 75% → 83% (+8%)`
6. **SYNC** — `hsa_check_changes` to update index after test/code creation

---

## COMMANDS

| Command           | Description                     |
| ----------------- | ------------------------------- |
| `/tdd [feature]`  | TDD cycle for a feature         |
| `/tdd red [test]` | Write failing test only         |
| `/tdd green`      | Implement minimal code          |
| `/tdd refactor`   | Refactor phase                  |
| `/tdd cycle [n]`  | Run n Red-Green-Refactor cycles |

---

## THE IRON LAWS

```
1. NEVER write production code without a failing test
2. Write ONLY enough test to fail (one assertion)
3. Write ONLY enough code to pass (no more)
4. Refactor ONLY when green (all tests pass)
5. Commit after EVERY green phase
```

---

## TDD CYCLE EXECUTION

### Phase 1: 🔴 RED

```
1. Identify the next requirement
2. Write ONE test case
3. Run test → MUST FAIL
4. If test passes → wrong test (delete & rethink)
5. If test errors (syntax/import) → fix infrastructure, not logic
```

### Phase 2: 🟢 GREEN

```
1. Write the SIMPLEST code to pass
2. Hardcoding is OK if only one test
3. Don't generalize yet
4. Run test → MUST PASS
5. If still fails → fix, don't add new tests
```

### Phase 3: 🔵 REFACTOR

```
1. Remove duplication (DRY)
2. Improve naming and readability
3. Extract functions/classes if needed
4. Run ALL tests → MUST PASS
5. Commit with message: "refactor: [what improved]"
```

---

## TIMING CONSTRAINTS

| Phase      | Max Time | Action If Exceeded          |
| ---------- | -------- | --------------------------- |
| RED        | 5 min    | Simplify the test           |
| GREEN      | 10 min   | Simplify the implementation |
| REFACTOR   | 5 min    | Defer complex refactoring   |
| Full cycle | 15 min   | Break into smaller tests    |

---

## OUTPUT FORMAT

```
🧪 TDD Cycle: [feature]

🔴 RED — test_calculate_discount_applies_10_percent
   ❌ FAIL: calculateDiscount is not defined

🟢 GREEN — Added calculateDiscount()
   ✅ PASS: 1/1 tests passing

🔵 REFACTOR — Extracted discount logic to DiscountService
   ✅ PASS: 1/1 tests passing

📊 Coverage: 78% → 82% (+4%)
⏱️ Cycle time: 8 min
```
---

## 🔄 CASCADE EVALUATION (Recommended — MCP)

⚠️ **Evaluate before EXECUTE step** — see `delegation-intelligence` skill for scoring.

For complex TDD feature cycles, delegate to specialized model via cascade:
```
hsa_delegate({action:'cascade', cascade_text:'[detailed prompt]', task_type:'test'})
→ wait 5s → hsa_delegate({action:'cascade_read', cascade_id:'...'})
→ repeat cascade_read (3-5s intervals, max 10 polls)
```
**Auto-cascade** (complexity ≥8): >3 TDD cycles, domain-specific testing
**Suggest cascade** (complexity 5-7): Complex feature requiring specialized model

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

