# Feature Chain — Step 1: Requirements

> Spec-driven: define WHAT before HOW

---

## Context

You are starting a new feature lifecycle. First, capture clear requirements.

## Input

```
{{FEATURE_NAME}}
{{USER_DESCRIPTION}}
```

## Task

### 1. Problem Statement

- What problem does this feature solve?
- Who benefits? How many users affected?
- What's the current workaround (if any)?

### 2. User Stories (INVEST Criteria)

```markdown
As a [user type],
I want to [action],
So that [benefit].
```

> INVEST: Independent, Negotiable, Valuable, Estimable, Small, Testable

### 3. Acceptance Criteria

| ID     | Criterion     | Priority | Testable |
| ------ | ------------- | -------- | -------- |
| AC-001 | [Description] | P0       | Yes      |
| AC-002 | [Description] | P1       | Yes      |

### 4. Constraints & Out of Scope

**Constraints:**

- Performance: {{PERF_REQS}}
- Security: {{SEC_REQS}}
- Compatibility: {{COMPAT_REQS}}

**Out of scope:**

- [Items explicitly excluded]

## Output Format

```yaml
requirements:
  problem: "[Problem statement]"
  users: "[Who and how many]"
  stories:
    - as: "[User type]"
      want: "[Action]"
      so_that: "[Benefit]"
  acceptance_criteria:
    - id: "AC-001"
      criterion: "[Description]"
      priority: "P0"
      testable: true
  constraints: ["[Constraint 1]", "[Constraint 2]"]
  out_of_scope: ["[Item 1]", "[Item 2]"]
```

---

_Chain Step 1 of 5 • Output: requirements → ⛔ STOP for approval_
