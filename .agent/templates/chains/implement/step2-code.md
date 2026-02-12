# Implement Chain — Step 2: Implement

> Prompt chaining step for implementation process

---

## Context

Based on the plan, implement the code.

## Input

```yaml
{ { plan } }
```

## Task

For each task in the plan:

### 1. Write Quality Code

Follow best practices:

- Clear naming
- Proper error handling
- Type safety
- Appropriate comments

### 2. Apply Design Patterns

Use appropriate patterns:

- SOLID principles
- DRY (Don't Repeat Yourself)
- KISS (Keep It Simple)

### 3. Handle Edge Cases

Consider:

- Invalid inputs
- Error conditions
- Boundary cases

## Output Format

```yaml
code:
  completed_tasks:
    - task_id: 1
      status: "complete"
      files_created:
        - path: "path/to/new/file"
          language: "typescript"
          lines: 45
          key_exports: ["function1", "function2"]
      files_modified:
        - path: "path/to/modified/file"
          changes_summary: "[What was changed]"
          lines_added: 10
          lines_removed: 5
    # ...more tasks

  code_samples:
    - file: "path/to/file"
      highlight: "Key implementation"
      code: |
        // Important code snippet

  decisions:
    - decision: "[What was decided]"
      reason: "[Why this approach]"
      alternatives: "[What was considered]"

  dependencies_added:
    - name: "package-name"
      version: "1.0.0"
      command: "npm install package-name"

  notes:
    - "[Any important notes for reviewers]"
```

---

_Chain Step 2 of 4 • Input: plan • Output: code_
