# Code Review Chain — Step 4: Summarize

> Final step: Generate the review summary

---

## Context

Compile all previous steps into a final review.

## Input

```yaml
{ { recommendations } }
```

## Task

Create the final review summary for the PR/MR.

## Output Format

````markdown
## 🔍 Code Review Summary

### Verdict: [✅ Approve | ⚠️ Request Changes | 🚫 Block]

---

### 📊 Overview

| Category       | Issues | Status         |
| -------------- | ------ | -------------- |
| 🔴 Blocking    | X      | [Fix required] |
| 🟠 Changes     | X      | [Should fix]   |
| 🟡 Suggestions | X      | [Consider]     |
| 🟢 Nitpicks    | X      | [Optional]     |

**Estimated review effort:** [Easy|Medium|Hard]

---

### 🔴 Blocking Issues (P0)

> These must be fixed before merge

#### R001: [Title]

**Location:** `file:line`
**Issue:** [Description]
**Fix:**

```language
// Suggested fix
```
````

---

### 🟠 Changes Requested (P1)

> Should be fixed in this PR

#### R002: [Title]

**Location:** `file:line`
**Issue:** [Description]
**Suggestion:** [How to fix]

---

### 🟡 Suggestions (P2)

> Nice to have, can be separate PR

- [ ] `file:line` — [Suggestion]
- [ ] `file:line` — [Suggestion]

---

### 💚 What's Good

- [Specific praise for good patterns/decisions]
- [Another positive observation]

---

### 📋 Checklist

- [ ] All blocking issues addressed
- [ ] Tests added/updated
- [ ] Documentation updated (if needed)
- [ ] No new warnings/errors

---

_Review by: AI Code Review • {{DATE}}_

```

---

_Chain Step 4 of 4 • Input: recommendations • Output: Final Review_
```
