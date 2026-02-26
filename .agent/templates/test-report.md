---
name: test-report
type: report
triggers: ["/test"]
---

# Test Report Template

## {FEATURE_NAME}

### Summary

| Metric      | Value       |
| ----------- | ----------- |
| Total tests | {TOTAL}     |
| Passed      | {PASSED}    |
| Failed      | {FAILED}    |
| Coverage    | {COVERAGE}% |

### Test Cases

| Case     | Status | Time     |
| -------- | ------ | -------- |
| {TEST_1} | ✅/❌  | {TIME_1} |
| {TEST_2} | ✅/❌  | {TIME_2} |
| {TEST_3} | ✅/❌  | {TIME_3} |

### Failures

#### {FAILED_TEST}

**Expected:** {EXPECTED}
**Actual:** {ACTUAL}
**Fix:** {SUGGESTION}

### Coverage Gaps

| File     | Coverage | Missing   |
| -------- | -------- | --------- |
| {FILE_1} | {COV_1}% | {LINES_1} |
| {FILE_2} | {COV_2}% | {LINES_2} |

### Next Steps

- [ ] Fix failing tests
- [ ] Add missing edge cases
- [ ] Improve coverage

---
