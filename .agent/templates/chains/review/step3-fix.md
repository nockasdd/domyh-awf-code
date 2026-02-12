# Code Review Chain — Step 3: Recommend

> Prompt chaining step for code review process

---

## Context

Based on the analysis from Step 2, formulate actionable recommendations.

## Input

```yaml
{ { analysis } }
```

## Task

Create prioritized recommendations:

### Priority Framework

| Priority | Criteria            | Action Required     |
| -------- | ------------------- | ------------------- |
| 🔴 P0    | Security/Data Loss  | Block merge         |
| 🟠 P1    | Logic/Correctness   | Request changes     |
| 🟡 P2    | Quality/Performance | Suggest improvement |
| 🟢 P3    | Nitpick/Style       | Optional            |

### For Each Issue

1. Categorize by priority
2. Provide specific fix
3. Include code example if helpful
4. Explain the "why"

## Output Format

```yaml
recommendations:
  blocking: # P0 - Must fix before merge
    - id: "R001"
      priority: "P0"
      category: "[security|data_loss|critical_bug]"
      location: "file:line"
      title: "[Brief title]"
      issue: "[What's wrong]"
      reason: "[Why it matters]"
      fix: |
        [Code example or description of fix]

  changes_requested: # P1 - Should fix
    - id: "R002"
      priority: "P1"
      category: "[logic|correctness|error_handling]"
      location: "file:line"
      title: "[Brief title]"
      issue: "[What's wrong]"
      reason: "[Why it matters]"
      fix: |
        [Code example or description of fix]

  suggestions: # P2 - Nice to fix
    - id: "R003"
      priority: "P2"
      category: "[quality|performance|readability]"
      location: "file:line"
      title: "[Brief title]"
      issue: "[What could be better]"
      reason: "[Why it would help]"
      suggestion: |
        [Code example or description]

  nitpicks: # P3 - Optional
    - id: "R004"
      priority: "P3"
      location: "file:line"
      comment: "[Minor suggestion]"

  praise: # Things done well
    - location: "file:line"
      comment: "[What was good]"

  summary:
    verdict: "[approve|request_changes|block]"
    blocking_count: 0
    changes_count: 0
    suggestion_count: 0
```

---

_Chain Step 3 of 4 • Input: analysis • Output: recommendations_
