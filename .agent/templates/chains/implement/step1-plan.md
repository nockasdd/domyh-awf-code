# Implement Chain — Step 1: Plan

> Prompt chaining step for implementation process

---

## Context

You are implementing a feature or change. First, create a plan.

## Input

```
{{TASK_DESCRIPTION}}
{{REQUIREMENTS}}
```

## Task

### 1. Understand Requirements

- What needs to be built?
- What are the acceptance criteria?
- Any constraints or limitations?

### 2. Identify Scope

- Which files need changes?
- New files to create?
- Dependencies needed?

### 3. Break Down Tasks

Create a step-by-step implementation plan.

## Output Format

```yaml
plan:
  understanding:
    goal: "[What we're building]"
    acceptance_criteria:
      - "[Criterion 1]"
      - "[Criterion 2]"
    constraints:
      - "[Constraint 1]"
      - "[Constraint 2]"

  scope:
    files_to_create:
      - path: "path/to/new/file"
        purpose: "[Why this file]"
    files_to_modify:
      - path: "path/to/existing/file"
        changes: "[What changes]"
    dependencies:
      - name: "[Package name]"
        version: "[Version]"
        reason: "[Why needed]"

  tasks:
    - id: 1
      title: "[Task title]"
      description: "[What to do]"
      files: ["file1", "file2"]
      estimated_lines: 50
      dependencies: []
    - id: 2
      title: "[Task title]"
      description: "[What to do]"
      files: ["file3"]
      estimated_lines: 30
      dependencies: [1]
    # ...more tasks

  total_estimate:
    files: X
    lines: Y
    complexity: "[low|medium|high]"

  risks:
    - risk: "[Potential risk]"
      mitigation: "[How to mitigate]"
```

---

_Chain Step 1 of 4 • Output: plan_
