# Debug Chain — Step 5: Verify

> Final step: Verify the fix and document

---

## Context

Fix is applied, now verify it works and document.

## Input

```yaml
{ { fix } }
```

## Task

### 1. Verify Fix Works

- [ ] Original error no longer occurs
- [ ] Reproduction steps now succeed
- [ ] New test passes
- [ ] Existing tests still pass

### 2. Check for Regressions

- [ ] Related functionality works
- [ ] No new errors in logs
- [ ] Performance not degraded

### 3. Document for Future

- What was learned?
- How can similar issues be prevented?
- What patterns should be added?

## Output Format

```markdown
## 🐛 Bug Fix Report

### Summary

**Issue:** [One-line description]
**Root Cause:** [One-line root cause]
**Fix:** [One-line fix description]

---

### Investigation Trail

| Step      | Finding             |
| --------- | ------------------- |
| Reproduce | [How reproduced]    |
| Isolate   | [Where isolated to] |
| Analyze   | [Root cause found]  |
| Fix       | [Fix applied]       |

### Root Cause Analysis

**Location:** `file:line`

**Code Path:**
```

function1() → function2() → [problem]

````

**Why it Happened:**
[Detailed explanation]

---

### Fix Applied

**Files Changed:**
- `file1.go` — [Description]
- `file2.go` — [Description]

**Key Change:**
```diff
- old code
+ new code
````

---

### Verification

| Check                | Status |
| -------------------- | ------ |
| Original error fixed | ✅     |
| New test added       | ✅     |
| Existing tests pass  | ✅     |
| No regressions       | ✅     |

---

### Prevention

**Test Added:** `test_file:test_name`

**Recommendations:**

1. [Recommendation to prevent similar issues]
2. [Another recommendation]

**Pattern Learned:**
[If there's a general pattern to add to patterns/bugs_fixed.json]

---

_Fixed by: AI Debug • {{DATE}}_

```

---

_Chain Step 5 of 5 • Input: fix • Output: Final Report_
```
