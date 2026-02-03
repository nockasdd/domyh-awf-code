# Code Review Chain — Step 2: Analyze

> Prompt chaining step for code review process

---

## Context

Based on the understanding from Step 1, perform detailed analysis.

## Input

```yaml
{ { understanding } }
```

## Task

Analyze the code across these dimensions:

### 1. Code Quality

- [ ] Follows project conventions
- [ ] Clear naming
- [ ] Appropriate comments
- [ ] No code smells
- [ ] DRY principle followed

### 2. Logic Correctness

- [ ] Handles edge cases
- [ ] Error handling complete
- [ ] No off-by-one errors
- [ ] Correct data flow
- [ ] State management correct

### 3. Security

- [ ] Input validation
- [ ] No injection risks
- [ ] Proper authentication/authorization
- [ ] Sensitive data handled correctly
- [ ] No exposed secrets

### 4. Performance

- [ ] No N+1 queries
- [ ] Appropriate data structures
- [ ] No memory leaks
- [ ] Efficient algorithms
- [ ] Caching where needed

### 5. Testing

- [ ] Tests exist
- [ ] Tests cover happy path
- [ ] Tests cover edge cases
- [ ] Tests are meaningful

## Output Format

```yaml
analysis:
  quality:
    score: "[1-10]"
    issues:
      - type: "[naming|style|smell|dry]"
        location: "file:line"
        issue: "[description]"
        severity: "[high|medium|low]"
        suggestion: "[how to fix]"

  logic:
    score: "[1-10]"
    issues:
      - type: "[edge_case|error_handling|data_flow]"
        location: "file:line"
        issue: "[description]"
        severity: "[high|medium|low]"
        suggestion: "[how to fix]"

  security:
    score: "[1-10]"
    issues:
      - type: "[injection|auth|secrets|validation]"
        location: "file:line"
        issue: "[description]"
        severity: "[P0|P1|P2]"
        cwe: "[CWE-XXX if applicable]"
        suggestion: "[how to fix]"

  performance:
    score: "[1-10]"
    issues:
      - type: "[n+1|memory|algorithm|structure]"
        location: "file:line"
        issue: "[description]"
        impact: "[estimated impact]"
        suggestion: "[how to fix]"

  testing:
    coverage_estimate: "[percentage]"
    gaps:
      - area: "[what's not tested]"
        priority: "[high|medium|low]"
```

---

_Chain Step 2 of 4 • Input: understanding • Output: analysis_
