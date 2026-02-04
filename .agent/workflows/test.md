---
name: test
trigger: ["/test", "testing", "tests", "kiểm thử"]
persona: developer
description: "✅ Run existing tests and write new test cases with proper coverage"
---

# ✅ /test — Test Pro v3.2

> Complete Testing Workflow
> 📚 30+ Languages • TDD • Coverage Analysis

---

## 🔄 TESTING FLOW

```
User: /test [target]
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 1: DETECT                         │
│ ▸ Find test framework                   │
│ ▸ Identify test files                   │
│ ▸ Check configuration                   │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 2: RUN                            │
│ ▸ Execute tests                         │
│ ▸ Collect coverage                      │
│ ▸ Record results                        │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 3: ANALYZE                        │
│ ▸ Identify failures                     │
│ ▸ Find root causes                      │
│ ▸ Check coverage gaps                   │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 4: FIX/WRITE                      │
│ ▸ Fix failing tests                     │
│ ▸ Write missing tests                   │
│ ⛔ STOP → Confirm new tests             │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 5: VERIFY                         │
│ ▸ Re-run all tests                      │
│ ▸ Confirm coverage improved             │
└─────────────────────────────────────────┘
```

---

## 🔴🟢🔵 TDD — THE IRON LAW

> **Source**: Superpowers Test-Driven Development
> **Philosophy**: NO PRODUCTION CODE WITHOUT FAILING TEST FIRST

### The Iron Law

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚠️  STOP! If you didn't watch the test fail, you DON'T know   │
│       if it tests the right thing!                              │
└─────────────────────────────────────────────────────────────────┘
```

### Red-Green-Refactor Cycle (MANDATORY)

```
   ┌──────────────┐
   │   🔴 RED      │
   │ Write test   │──────┐
   │ (must fail)  │      │
   └──────────────┘      │
         │               │
         ▼               │
   ┌──────────────┐      │
   │ VERIFY FAIL  │      │
   │ (watch it!)  │      │
   └──────────────┘      │
         │               │
         ▼               │
   ┌──────────────┐      │
   │  🟢 GREEN    │      │
   │ Minimal code │      │
   │ (to pass)    │      │
   └──────────────┘      │
         │               │
         ▼               │
   ┌──────────────┐      │
   │ VERIFY PASS  │      │
   │ (all green!) │      │
   └──────────────┘      │
         │               │
         ▼               │
   ┌──────────────┐      │
   │ 🔵 REFACTOR  │      │
   │ Clean up     │      │
   │ (stay green) │      │
   └──────────────┘      │
         │               │
         └───────────────┘
```

### Common Rationalizations (IGNORE THESE)

| Excuse                    | Reality                                  |
| ------------------------- | ---------------------------------------- |
| "Too simple to test"      | Simple code breaks. Test takes 30s.      |
| "I'll test after"         | Tests passing immediately prove nothing. |
| "Already manually tested" | Ad-hoc ≠ systematic.                     |
| "The test is obvious"     | Until you watch it fail, you don't know. |
| "Just a quick fix"        | Quick fixes create more bugs.            |

### TDD Verification Checklist

```yaml
before_merge:
  - "Every new function has a test?"
  - "Watched each test fail first?"
  - "All tests pass, output pristine?"
  - "No skipped/commented tests?"
```

---

## 🎯 COMMANDS

| Command                | Description        |
| ---------------------- | ------------------ |
| `/test`                | Run all tests      |
| `/test [file]`         | Test specific file |
| `/test coverage`       | Coverage report    |
| `/test write [target]` | Write new tests    |
| `/test fix`            | Fix failing tests  |
| `/test watch`          | Watch mode         |

---

## 🔧 TESTING FRAMEWORKS

```yaml
# ═══════════════════════════════════════════════════════════════
# TESTING FRAMEWORKS BY LANGUAGE
# ═══════════════════════════════════════════════════════════════

frameworks:
  go:
    unit: "testing (stdlib)"
    runner: "go test"
    coverage: "go test -cover"
    mocking: [testify, gomock, mockery]
    commands:
      run: "go test ./..."
      verbose: "go test -v ./..."
      coverage: "go test -coverprofile=coverage.out ./..."

  typescript:
    unit: [vitest, jest]
    runner: "npm test"
    coverage: "vitest --coverage"
    mocking: [vitest, jest, sinon]
    commands:
      run: "npm test"
      watch: "npm test -- --watch"
      coverage: "npm run test:coverage"

  python:
    unit: [pytest, unittest]
    runner: "pytest"
    coverage: "pytest --cov"
    mocking: [pytest-mock, unittest.mock]
    commands:
      run: "pytest -v"
      coverage: "pytest --cov --cov-report=html"
      watch: "pytest-watch"

  rust:
    unit: "built-in"
    runner: "cargo test"
    coverage: "cargo tarpaulin"
    mocking: [mockall]
    commands:
      run: "cargo test"
      verbose: "cargo test -- --nocapture"

  java:
    unit: [JUnit5, TestNG]
    runner: "mvn test"
    coverage: "jacoco"
    mocking: [Mockito, PowerMock]
    commands:
      run: "mvn test"
      coverage: "mvn jacoco:report"

  csharp:
    unit: [xUnit, NUnit, MSTest]
    runner: "dotnet test"
    coverage: "coverlet"
    mocking: [Moq, NSubstitute]
    commands:
      run: "dotnet test"
      coverage: 'dotnet test --collect:"XPlat Code Coverage"'

  ruby:
    unit: [RSpec, Minitest]
    runner: "rspec"
    coverage: "simplecov"
    mocking: [rspec-mocks]

  php:
    unit: [PHPUnit, Pest]
    runner: "phpunit"
    coverage: "phpunit --coverage-html"
    mocking: [Mockery, Prophecy]
```

---

## 📋 TEST STRUCTURE

### AAA Pattern (Arrange-Act-Assert)

```yaml
aaa_pattern:
  typescript: |
    describe('UserService', () => {
      it('should create user with valid data', async () => {
        // Arrange
        const userData = { name: 'John', email: 'john@example.com' };
        const mockRepo = vi.fn().mockResolvedValue({ id: 1, ...userData });
        const service = new UserService(mockRepo);
        
        // Act
        const result = await service.create(userData);
        
        // Assert
        expect(result.id).toBe(1);
        expect(result.name).toBe('John');
        expect(mockRepo).toHaveBeenCalledWith(userData);
      });
    });

  go: |
    func TestUserService_Create(t *testing.T) {
      // Arrange
      mockRepo := mocks.NewUserRepository(t)
      mockRepo.On("Create", mock.Anything).Return(&User{ID: 1}, nil)
      service := NewUserService(mockRepo)
      
      // Act
      result, err := service.Create(context.Background(), CreateUserInput{Name: "John"})
      
      // Assert
      assert.NoError(t, err)
      assert.Equal(t, 1, result.ID)
      mockRepo.AssertExpectations(t)
    }

  python: |
    def test_user_service_create(mock_repo):
      # Arrange
      mock_repo.create.return_value = User(id=1, name="John")
      service = UserService(mock_repo)
      
      # Act
      result = service.create(CreateUserInput(name="John"))
      
      # Assert
      assert result.id == 1
      assert result.name == "John"
      mock_repo.create.assert_called_once()
```

---

## 📊 COVERAGE TARGETS

```yaml
coverage_targets:
  unit:
    target: "> 80%"
    critical_paths: "100%"

  integration:
    target: "> 60%"
    focus: "API endpoints, DB operations"

  e2e:
    target: "Critical user flows"
    examples: ["login", "checkout", "signup"]

coverage_report:
  good: "> 80%"
  acceptable: "60-80%"
  poor: "< 60%"
```

---

## 📊 TEST REPORT

```markdown
✅ TEST REPORT

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Summary

| Metric   | Value | Status |
| -------- | ----- | ------ |
| Total    | 145   | -      |
| Passed   | 142   | ✅     |
| Failed   | 3     | ❌     |
| Skipped  | 0     | ⏭️     |
| Duration | 12.3s | -      |

## Coverage

| Package    | Lines   | Status |
| ---------- | ------- | ------ |
| handlers   | 85%     | 🟢     |
| services   | 72%     | 🟡     |
| repository | 68%     | 🟡     |
| **Total**  | **78%** | 🟡     |

## Failed Tests

### 1. TestUserCreate

📍 `user/service_test.go:45`
```

Error: context deadline exceeded
Expected: user created within 1s
Actual: timed out after 5s

```
**Root Cause:** Missing mock for external API
**Fix:** Add mock for email service

### 2. TestOrderValidation
📍 `order/validator_test.go:78`
```

Error: assertion failed
Expected: validation error for negative amount
Actual: nil

```
**Root Cause:** Missing validation rule
**Fix:** Add negative amount check

## Uncovered Code

| File | Lines | Reason |
|------|-------|--------|
| `error_handler.go` | 45-60 | Error paths |
| `cache.go` | 20-35 | Cache miss |

## Recommendations

1. 🔴 Fix 3 failing tests
2. 🟠 Add tests for error_handler.go
3. 🟡 Increase services coverage

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 📝 TEST GENERATION

```yaml
test_generation:
  triggers:
    - "/test write [file]"
    - "/test generate [function]"

  strategy:
    1_analyze:
      - Read function signature
      - Identify inputs/outputs
      - Find edge cases

    2_generate:
      - Happy path test
      - Error cases
      - Edge cases
      - Boundary conditions

    3_output:
      - Follow project conventions
      - Use existing mocks
      - Match file naming
```

---

## 🔧 TDD WORKFLOW

### Red-Green-Refactor Cycle

```yaml
tdd:
  cycle:
    1_red: "Write failing test"
    2_green: "Write minimum code to pass"
    3_refactor: "Improve code quality"

  commands:
    start: "/test write [feature]"
    check: "/test"
    complete: "/test coverage"
```

### Domain-Driven TDD

```yaml
domain_driven_tdd:
  description: "Combine TDD with Domain-Driven Design"

  steps:
    1_scenario: |
      Define business scenario in domain language
      Example: "When user exceeds rate limit, return 429"

    2_test: |
      Write test using domain terminology
      test_rate_limit_exceeded_returns_429()

    3_implement: |
      Let failing test guide implementation
      Focus on domain behavior, not implementation

    4_refactor: |
      Improve design while tests green
      Extract domain concepts
```

---

## 🤖 AI-ASSISTED TESTING

### AI Test Generation

```yaml
ai_test_generation:
  commands:
    - "/test generate [file]" # Generate tests for file
    - "/test edge [function]" # Generate edge cases
    - "/test scenario [feature]" # Generate scenario tests

  patterns:
    happy_path: "Normal successful flow"
    edge_cases: "Boundary conditions, empty inputs"
    error_cases: "Invalid inputs, exceptions"
    integration: "Component interactions"

  example:
    input: "/test generate UserService"
    output:
      - test_create_user_success
      - test_create_user_invalid_email
      - test_create_user_duplicate
      - test_get_user_not_found
```

### LLM-as-Judge Evaluation

````yaml
llm_evaluation:
  description: "Use LLM to evaluate test results"

  workflow:
    1_run: "Execute tests, capture output"
    2_analyze: "LLM reviews failures"
    3_diagnose: "Identify root cause"
    4_suggest: "Propose fix"

  stability:
    # Multiple evaluations for consistency
    runs: 3
    consensus: "majority vote"

  output: |
    ❌ TestUserCreate failed

    Root Cause: Missing mock for EmailService
    Confidence: 95%

    Suggested Fix:
    ```go
    mockEmail := mocks.NewEmailService(t)
    mockEmail.On("Send", mock.Anything).Return(nil)
    ```
````

---

## 📊 COVERAGE ENFORCEMENT

```yaml
coverage_gates:
  # Block merge if below threshold
  unit:
    minimum: 80%
    critical_paths: 100%
    action_on_fail: "block PR"

  integration:
    minimum: 60%
    focus: "API endpoints, DB operations"

  tracking:
    command: "/test coverage --track"
    report: "coverage-trend.json"
```

---

## ⚙️ TOKEN OPTIMIZATION

```yaml
token_saving:
  - Run only affected tests first
  - Focus on failures only
  - Use coverage to prioritize
  - Cache test results in session
  - Skip unchanged test files
```

---

_DOMYH Awesome Code v6.1.2 • Test Pro v3.2 • TDD Iron Law + AI Testing_
