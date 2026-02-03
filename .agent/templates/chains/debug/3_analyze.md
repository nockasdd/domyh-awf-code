# Debug Chain — Step 3: Analyze

> Prompt chaining step for debugging process

---

## Context

With the issue isolated, analyze to find root cause.

## Input

```yaml
{ { isolation } }
```

## Task

### 1. Form Hypotheses

Based on isolated area, form max 3 hypotheses:

| #   | Hypothesis | Likelihood | Test          |
| --- | ---------- | ---------- | ------------- |
| 1   | [Theory 1] | High       | [How to test] |
| 2   | [Theory 2] | Medium     | [How to test] |
| 3   | [Theory 3] | Low        | [How to test] |

### 2. Test Each Hypothesis

For each hypothesis:

- Design a test
- Execute the test
- Record the result
- Confirm or eliminate

### 3. Identify Root Cause

- Which hypothesis was correct?
- Why did this happen?
- What's the exact code path?

## Output Format

```yaml
root_cause:
  hypotheses:
    - id: 1
      theory: "[Description of theory]"
      likelihood: "high"
      test: "[How you tested it]"
      result: "confirmed|eliminated"
      evidence: "[What proved/disproved it]"
    - id: 2
      theory: "[Description of theory]"
      likelihood: "medium"
      test: "[How you tested it]"
      result: "confirmed|eliminated"
      evidence: "[What proved/disproved it]"
    - id: 3
      theory: "[Description of theory]"
      likelihood: "low"
      test: "[How you tested it]"
      result: "confirmed|eliminated"
      evidence: "[What proved/disproved it]"

  confirmed_cause:
    location: "file:line"
    code: |
      // The problematic code
    explanation: "[Why this causes the issue]"
    root_reason: "[The fundamental reason - not just symptoms]"

  contributing_factors:
    - "[Factor 1 that contributed]"
    - "[Factor 2 that contributed]"

  why_not_caught:
    - "[Why tests didn't catch this]"
    - "[What was missing]"
```

---

_Chain Step 3 of 5 • Input: isolation • Output: root_cause_
