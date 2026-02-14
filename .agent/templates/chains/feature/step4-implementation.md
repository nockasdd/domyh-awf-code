# Feature Chain — Step 4: Implementation

> Execute with traceability, log every decision

---

## Context

Plan approved. Implement tasks following the breakdown.

## Input

```
{{PLANNING_OUTPUT}}
{{DESIGN_OUTPUT}}
```

## Task

### 1. Execute Tasks

For each task in the plan:

- Reference task ID: `// T-001: [description]`
- Follow design decisions (DD-xxx)
- Use existing patterns detected by HSA
- Run `hsa_check_changes` after each milestone

### 2. Log Files Changed

| File               | Action | Task  | Description            |
| ------------------ | ------ | ----- | ---------------------- |
| `path/to/file.ts`  | New    | T-001 | [What was created]     |
| `path/to/other.ts` | Modify | T-002 | [What changed and why] |

### 3. Decision Log

| Date       | Decision           | Context             | Task  |
| ---------- | ------------------ | ------------------- | ----- |
| YYYY-MM-DD | [What was decided] | [Why at this point] | T-001 |

### 4. Progress Tracking

```
████████░░ 80% (8/10 tasks)
```

- [x] T-001: Completed
- [x] T-002: Completed
- [/] T-003: In progress
- [ ] T-004: Not started

## Output Format

```yaml
implementation:
  files_changed:
    - path: "path/to/file.ts"
      action: "new"
      task: "T-001"
  decisions:
    - date: "YYYY-MM-DD"
      decision: "[Choice]"
      task: "T-001"
  progress:
    completed: ["T-001", "T-002"]
    in_progress: ["T-003"]
    remaining: ["T-004"]
    percentage: 80
```

---

_Chain Step 4 of 5 • Output: implementation log_
