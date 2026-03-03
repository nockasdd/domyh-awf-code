# Feature Chain — Step 2: Design

> Architecture decisions before code

---

## Context

Requirements approved. Now design the solution architecture.

## Input

```
{{REQUIREMENTS_OUTPUT}}
{{CODEBASE_CONTEXT}}
```

## Task

### 1. Architecture Overview

- How does this feature fit into existing architecture?
- What patterns to follow? (check existing code via `hsa_search`)
- Any new components or modules needed?

### 2. Data Models

```
// Define new or modified data structures
// Include types, interfaces, DB schemas
```

### 3. API Design (if applicable)

| Method | Endpoint         | Request    | Response   | Auth |
| ------ | ---------------- | ---------- | ---------- | ---- |
| POST   | `/api/v1/{name}` | `{schema}` | `{schema}` | Yes  |

### 4. Architecture Decision Records (ADR)

| ID     | Decision           | Rationale | Alternatives Considered |
| ------ | ------------------ | --------- | ----------------------- |
| DD-001 | [What was decided] | [Why]     | [Other options]         |

### 5. Risk Assessment

| Risk          | Impact   | Likelihood | Mitigation |
| ------------- | -------- | ---------- | ---------- |
| [Description] | High/Med | Med/Low    | [Strategy] |

## Output Format

```yaml
design:
  architecture: "[Overview]"
  patterns: ["[Pattern 1]", "[Pattern 2]"]
  data_models:
    - name: "[Model]"
      fields: ["[field: type]"]
  apis:
    - method: "POST"
      path: "/api/v1/{name}"
      auth: true
  decisions:
    - id: "DD-001"
      decision: "[Choice]"
      rationale: "[Why]"
  risks:
    - risk: "[Description]"
      mitigation: "[Strategy]"
```

---

_Chain Step 2 of 5 • Output: design_
