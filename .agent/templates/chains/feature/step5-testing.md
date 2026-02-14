# Feature Chain — Step 5: Testing & Ship

> Verify all ACs met, then ship

---

## Context

Implementation complete. Verify quality and ship.

## Input

```
{{IMPLEMENTATION_OUTPUT}}
{{REQUIREMENTS_OUTPUT}}
```

## Task

### 1. Test Strategy

| Type        | Scope                 | Framework   | Target         |
| ----------- | --------------------- | ----------- | -------------- |
| Unit        | Core logic            | Auto-detect | 80%+ coverage  |
| Integration | Component interaction | Auto-detect | Key paths      |
| E2E         | User flows (if UI)    | Auto-detect | Critical paths |

### 2. Test Cases (Traceable)

| ID     | Case          | Covers | Type        | Status |
| ------ | ------------- | ------ | ----------- | ------ |
| TC-001 | [Description] | AC-001 | Unit        | ⬜     |
| TC-002 | [Description] | AC-002 | Integration | ⬜     |

> Every AC-xxx MUST have at least one TC-xxx. Uncovered AC = incomplete.

### 3. Coverage Results

| Metric          | Target | Actual | Status |
| --------------- | ------ | ------ | ------ |
| Line Coverage   | 80%    | _TBD_  | ⬜     |
| Branch Coverage | 70%    | _TBD_  | ⬜     |
| AC Coverage     | 100%   | _TBD_  | ⬜     |

### 4. AC Verification Matrix

| AC     | Test(s) | Pass | Notes       |
| ------ | ------- | ---- | ----------- |
| AC-001 | TC-001  | ⬜   | [Any notes] |
| AC-002 | TC-002  | ⬜   | [Any notes] |

### 5. Ship Checklist

- [ ] All tests pass
- [ ] All ACs verified
- [ ] Coverage targets met
- [ ] Design docs updated with final state
- [ ] Implementation log complete
- [ ] No regressions (existing tests still pass)
- [ ] Run `/verify` for final gate

## Output Format

```yaml
testing:
  test_cases:
    - id: "TC-001"
      case: "[Description]"
      covers: "AC-001"
      type: "unit"
      result: "pass"
  coverage:
    line: 85
    branch: 72
    ac: 100
  ship_ready: true
```

---

_Chain Step 5 of 5 • Output: testing results + ship decision_
