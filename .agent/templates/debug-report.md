---
name: debug-report
version: "6.4.5"
type: report
triggers: ["/debug"]
---

# Debug Report Template

## {BUG_TITLE}

### Problem

**Error:** `{ERROR_MESSAGE}`
**File:** `{FILE_PATH}:{LINE}`
**Reproduce:** {STEPS}

### Investigation

| #   | Hypothesis | Test     | Result |
| --- | ---------- | -------- | ------ |
| 1   | {THEORY_1} | {TEST_1} | ✅/❌  |
| 2   | {THEORY_2} | {TEST_2} | ✅/❌  |
| 3   | {THEORY_3} | {TEST_3} | ✅/❌  |

### Root Cause

**Cause:** {EXPLANATION}
**Evidence:** {PROOF}

### Fix

```{LANG}
{FIXED_CODE}
```

### Verification

- [ ] Tests passing
- [ ] No regression
- [ ] Edge cases covered

### Prevention

- [ ] Test case added
- [ ] Docs updated

---

\_DOMYH Awesome Code
