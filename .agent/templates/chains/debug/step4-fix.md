# Debug Chain — Step 4: Fix

> Prompt chaining step for debugging process

---

## Context

With root cause identified, implement the fix.

## Input

```yaml
{ { root_cause } }
```

## Task

### 1. Design the Fix

Consider:

- Minimal change to fix the issue
- Side effects
- Backward compatibility
- Related areas that might need update

### 2. Implement the Fix

Apply the change:

- Make the minimal fix
- Don't change unrelated code
- Keep the fix focused

### 3. Add Regression Test

Write a test that:

- Would have caught this bug
- Covers the edge case
- Prevents future regression

## Output Format

```yaml
fix:
  approach:
    strategy: "[Description of fix approach]"
    alternatives_considered:
      - option: "[Alternative 1]"
        rejected_because: "[Why not chosen]"
      - option: "[Alternative 2]"
        rejected_because: "[Why not chosen]"

  changes:
    - file: "path/to/file"
      type: "modify|add|delete"
      before: |
        // Old code
      after: |
        // New code
      explanation: "[Why this change fixes it]"

  side_effects:
    - area: "[Affected area]"
      impact: "[What might be affected]"
      mitigation: "[How it's handled]"

  regression_test:
    file: "path/to/test_file"
    test_name: "test_specific_case_that_was_broken"
    code: |
      // Test code that would have caught this
    covers: "[What this test covers]"

  verification_steps:
    1: "[How to verify the fix works]"
    2: "[Another verification step]"
    3: "[Final verification]"
```

---

_Chain Step 4 of 5 • Input: root_cause • Output: fix_
