# Code Review Chain — Step 1: Understand

> Prompt chaining step for code review process

---

## Context

You are reviewing code changes. First, understand what the code does.

## Input

```
{{CODE_DIFF}}
```

Files: {{FILES_CHANGED}}

## Task

Analyze and understand the code by answering:

### 1. What is the purpose?

- What problem does this code solve?
- What is the expected behavior?

### 2. Scope Assessment

- How many files changed?
- What areas are affected?
- Any breaking changes?

### 3. Key Components

Identify the key elements:

- New functions/methods
- Modified logic
- Added dependencies
- Configuration changes

### 4. Risk Areas

Flag potential concerns:

- Complex logic
- Security-sensitive code
- Performance implications
- Compatibility issues

## Output Format

```yaml
understanding:
  purpose: "[Brief description of what the code does]"
  scope:
    files_changed: [list]
    areas_affected: [list]
    breaking_changes: true/false
  key_components:
    - type: "[function|class|config]"
      name: "[name]"
      file: "[path]"
      description: "[what it does]"
  risk_areas:
    - area: "[description]"
      severity: "[high|medium|low]"
      reason: "[why it's risky]"
```

---

_Chain Step 1 of 4 • Output: understanding_
