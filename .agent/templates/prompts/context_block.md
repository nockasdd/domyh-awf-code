# Context Block Template

> Dynamic project context injection for system prompts

---

## Usage

This template injects current project context into system prompts.

```
{{CONTEXT_BLOCK}}
```

---

## Template

```markdown
## 📂 Current Context

### Project

- **Name:** {{PROJECT_NAME}}
- **Type:** {{PROJECT_TYPE}}
- **Stack:** {{TECH_STACK}}
- **Root:** {{PROJECT_ROOT}}

### Active Branch

**Branch:** {{CURRENT_BRANCH}}

### Recently Changed Files

{{#RECENT_CHANGES}}

- `{{FILE_PATH}}` — {{CHANGE_SUMMARY}}
  {{/RECENT_CHANGES}}

### Open Files

{{#OPEN_FILES}}

- `{{FILE_PATH}}`
  {{/OPEN_FILES}}

### Current Task

{{CURRENT_TASK_DESCRIPTION}}

### Memory Pointers

- Session: {{SESSION_POINTER}}
- State: {{STATE_POINTER}}
- Patterns: {{PATTERNS_POINTER}}
```

---

## Placeholders

| Placeholder                | Source       | Description             |
| -------------------------- | ------------ | ----------------------- |
| `PROJECT_NAME`             | `state.json` | Project name            |
| `PROJECT_TYPE`             | Detection    | Detected project type   |
| `TECH_STACK`               | Detection    | Languages/frameworks    |
| `PROJECT_ROOT`             | Config       | Root directory path     |
| `CURRENT_BRANCH`           | Git          | Active branch           |
| `RECENT_CHANGES`           | Git log      | Recent commits          |
| `OPEN_FILES`               | IDE          | Currently open files    |
| `CURRENT_TASK_DESCRIPTION` | Task         | Active task description |

---

## Example Rendered

```markdown
## 📂 Current Context

### Project

- **Name:** WebServer
- **Type:** Monorepo (Backend + Frontend)
- **Stack:** Go, TypeScript, Nuxt, PostgreSQL
- **Root:** /home/user/projects/WebServer

### Active Branch

**Branch:** feature/payment-gateway

### Recently Changed Files

- `internal/payment/handler.go` — Added VietQR support
- `frontend/pages/deposit.vue` — Updated deposit UI

### Open Files

- `internal/payment/service.go`
- `internal/payment/types.go`

### Current Task

Implementing VietQR auto-polling for bank transactions

### Memory Pointers

- Session: session.md
- State: state.json
- Patterns: patterns/successes.json
```

---

_DOMYH Awesome Code v6.0 • Context Block Template_
