# Implement Chain — Step 3: Test

> Prompt chaining step for implementation process

---

## Context

Code is implemented, now add tests.

## Input

```yaml
{ { code } }
```

## Task

### 1. Write Unit Tests

For each new function/method:

- Test happy path
- Test edge cases
- Test error conditions

### 2. Write Integration Tests

If applicable:

- Test component interactions
- Test data flow

### 3. Verify All Tests Pass

- Run the test suite
- Ensure no regressions

## Output Format

```yaml
tests:
  unit_tests:
    - file: "path/to/test/file"
      tests:
        - name: "test_function_with_valid_input"
          type: "happy_path"
          covers: "function_name"
          code: |
            test('should return correct result', () => {
              // Arrange, Act, Assert
            });
        - name: "test_function_with_invalid_input"
          type: "error_handling"
          covers: "function_name"
          code: |
            test('should throw error', () => {
              // ...
            });
    # ...more test files

  integration_tests:
    - file: "path/to/integration/test"
      tests:
        - name: "test_full_flow"
          covers: "[What flow is covered]"

  test_results:
    total: 10
    passed: 10
    failed: 0
    duration: "1.5s"

  coverage:
    lines: "92%"
    branches: "85%"
    functions: "95%"

  coverage_gaps:
    - file: "path/to/file"
      uncovered: "lines 45-48"
      reason: "[Why not covered or todo]"
```

---

_Chain Step 3 of 4 • Input: code • Output: tests_
