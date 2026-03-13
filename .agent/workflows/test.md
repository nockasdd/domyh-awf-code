---
description: "✅ Run existing tests and write new test cases with proper coverage"
skills: { required: [testing], contextual: [auto] }
success_criteria: "Tests written, all pass, coverage meets target"
---

# ✅ /test — Test Pro

> TDD-First Testing with Coverage Tracking
> 📚 Multi-language • Auto Test Loop • TDD Iron Law • Property-Based Testing

---

## TEST FLOW

1. **DETECT** — `hsa_session("testing: {scope}")`, identify stack via HSA (`hsa_detect`), load test context (`hsa_search`), find test framework, existing tests. Show: `[Step 1/6] Detecting test setup...`
2. **RUN** — Execute tests, collect coverage. Show: `[Step 2/6] Running 42 tests... ✅ 40 passed, ❌ 2 failed`
3. **ANALYZE** — Identify failures, coverage gaps, suggest missing test categories
4. **WRITE** — Generate missing tests (TDD cycle). Show progress: `[Step 4/6] Writing tests for UserService (3/5 cases)`
5. **VERIFY** — Re-run, confirm coverage improved. Show: `Coverage: 68% → 82% (+14%)`
6. **SYNC** — `hsa_check_changes` to update index after test file creation

---

## COMMANDS

| Command                  | Description                   |
| ------------------------ | ----------------------------- |
| `/test`                  | Run all tests                 |
| `/test [file]`           | Test specific file            |
| `/test write [feature]`  | Write tests for feature (TDD) |
| `/test coverage`         | Coverage report               |
| `/test generate [class]` | Auto-generate test cases      |
| `/test watch`            | Watch mode                    |
| `/test mutate [file]`    | Mutation testing              |
| `/test property [func]`  | Property-based testing        |
| `/test uat [scenario]`   | UAT test execution            |
| `/test contract [api]`   | Consumer-driven contract test |

---

## 🔴🟢🔵 TDD — THE IRON LAW

> **NO PRODUCTION CODE WITHOUT FAILING TEST FIRST**

```
🔴 RED → Write failing test
    ↓
🟢 GREEN → Minimum code to pass
    ↓
🔵 REFACTOR → Clean up (stay green)
    ↓
↻ Repeat
```

### Common Rationalizations (IGNORE THESE)

| Excuse               | Reality                        |
| -------------------- | ------------------------------ |
| "Too slow"           | Saves debugging time 10x       |
| "Too simple to test" | Simple code breaks too         |
| "Will add later"     | Technical debt never gets paid |
| "Only a prototype"   | Prototypes become production   |

---

## TESTING FRAMEWORKS

| Language   | Framework        | Runner                | Coverage          | Mocking            |
| ---------- | ---------------- | --------------------- | ----------------- | ------------------ |
| Go         | testing (stdlib) | `go test ./...`       | `go test -cover`  | testify, gomock    |
| TypeScript | Jest / Vitest    | `npx jest` / `vitest` | `--coverage`      | jest.mock, vi.mock |
| Python     | pytest           | `pytest -v`           | `pytest --cov`    | unittest.mock      |
| Rust       | built-in         | `cargo test`          | `cargo tarpaulin` | mockall            |
| Java       | JUnit 5          | `mvn test`            | JaCoCo            | Mockito            |
| C#         | xUnit / NUnit    | `dotnet test`         | Coverlet          | Moq, NSubstitute   |
| Ruby       | RSpec / Minitest | `rspec`               | SimpleCov         | rspec-mocks        |
| PHP        | PHPUnit / Pest   | `phpunit`             | `--coverage-html` | Mockery            |

---

## TEST STRUCTURE: AAA Pattern

> **A**rrange → **A**ct → **A**ssert

### Naming Convention

| Pattern                                | Example                                         |
| -------------------------------------- | ----------------------------------------------- |
| `test_[action]_[condition]_[expected]` | `test_create_user_with_valid_data_returns_user` |
| `should_[expected]_when_[condition]`   | `should_return_error_when_email_invalid`        |

---

## COVERAGE TARGETS

| Type           | Target         | Focus                 |
| -------------- | -------------- | --------------------- |
| Unit           | > 80%          | Business logic, utils |
| Integration    | > 60%          | API endpoints, DB ops |
| E2E            | Critical flows | User journeys         |
| Critical paths | 100%           | Auth, payments, data  |

---

## 🧬 PROPERTY-BASED TESTING

> Instead of testing specific examples, test **properties** that should always hold true

```yaml
tools:
  go: "gopter, rapid"
  python: "hypothesis"
  typescript: "fast-check"
  rust: "proptest"
  java: "jqwik"

example: |
  # Property: reverse(reverse(list)) == list
  # Property: sort(list).length == list.length
  # Property: parse(serialize(obj)) == obj
```

---

## 🦠 MUTATION TESTING

> Verify test quality by introducing mutations (small code changes) and checking if tests catch them

```yaml
tools:
  javascript: "stryker"
  python: "mutmut, cosmic-ray"
  java: "pitest"
  go: "go-mutesting"
  rust: "cargo-mutants"

score_target: "> 70% mutation score (killed / total mutations)"
```

---

## AI TEST GENERATION

| Input                        | Output                                                                  |
| ---------------------------- | ----------------------------------------------------------------------- |
| `/test generate UserService` | test_create_success, test_invalid_email, test_duplicate, test_not_found |
| Function signature           | Happy path + edge cases + error cases                                   |

### LLM-as-Judge

| Dimension   | Weight | Criteria              |
| ----------- | ------ | --------------------- |
| Correctness | 30%    | Tests valid behavior? |
| Coverage    | 25%    | Edge cases covered?   |
| Readability | 20%    | Clear naming, AAA?    |
| Isolation   | 15%    | No shared state?      |
| Performance | 10%    | Fast execution?       |
---

## 🔄 CASCADE EVALUATION (Recommended — MCP)

⚠️ **Evaluate before EXECUTE step** — see `delegation-intelligence` skill for scoring.

For comprehensive test generation, delegate to specialized model via cascade:
```
hsa_delegate({action:'cascade', cascade_text:'[detailed prompt]', task_type:'test'})
→ wait 5s → hsa_delegate({action:'cascade_read', cascade_id:'...'})
→ repeat cascade_read (3-5s intervals, max 10 polls)
```
**Auto-cascade** (complexity ≥8): >10 test cases, property-based/mutation testing
**Suggest cascade** (complexity 5-7): Comprehensive test suite, multi-module coverage

---

## REFLECTION CHECKPOINT

⛔ **MANDATORY** — Execute before completing this workflow (SESSION_005):

1. **VERIFY** — Does output meet success_criteria (see YAML frontmatter)?
2. **PERSIST** (if HSA available — preferred, 1 tool call):
   - `hsa_session({action:'persist', task_summary:'[workflow] [summary]', files_touched:[...], auto_notify:true})`
   - If key decision → `hsa_session({action:'anchor', content:'[decision]', category:'decision'})`
3. **PERSIST** (if HSA unavailable — manual fallback):
   - Append task summary to `memory/session.md`
   - If last task → Update `memory/CONTEXT_SNAPSHOT.md`

