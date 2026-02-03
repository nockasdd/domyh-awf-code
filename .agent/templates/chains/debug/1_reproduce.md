# Debug Chain — Step 1: Reproduce

> Prompt chaining step for debugging process

---

## Context

You are debugging an issue. First, gather information and reproduce it.

## Input

```
{{ERROR_DESCRIPTION}}
{{STACK_TRACE}}
{{LOGS}}
```

## Task

### 1. Gather Evidence

Collect all relevant information:

- Error message and stack trace
- Relevant logs
- Recent code changes
- Environment details

### 2. Reproduce the Issue

Define reproduction steps:

- [ ] Exact steps to trigger
- [ ] Input that causes the error
- [ ] Environment conditions
- [ ] Consistent/intermittent?

### 3. Document Initial Observations

What do you notice?

- When does it happen?
- What's the frequency?
- Any patterns?

## Output Format

```yaml
reproduction:
  error:
    message: "[Error message]"
    type: "[Error type]"
    location: "file:line"

  stack_trace: |
    [Relevant stack trace]

  reproduction_steps:
    1: "[Step 1]"
    2: "[Step 2]"
    3: "[Step 3]"

  consistency: "[always|sometimes|rare]"

  environment:
    os: "[OS]"
    runtime: "[Node/Go/Python version]"
    relevant_config: "[Any relevant config]"

  recent_changes:
    - file: "[path]"
      change: "[description]"
      author: "[if known]"

  initial_observations:
    - "[Observation 1]"
    - "[Observation 2]"
```

---

_Chain Step 1 of 5 • Output: reproduction_
