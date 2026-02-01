# 🎭 DOMYH Agent Personas v4.0

> Role-based AI personas for different development tasks

## Available Personas (7)

| Persona    | Role            | Triggers                        |
| ---------- | --------------- | ------------------------------- |
| auditor    | 5-expert panel  | `/ap`                           |
| developer  | Code craftsman  | `/code`, `/refactor`, `/review` |
| architect  | System design   | `/plan`, `/design`              |
| debugger   | Bug hunter      | `/debug`                        |
| tester     | Test specialist | `/test`                         |
| devops     | CI/CD expert    | `/deploy`, `/monitor`, `/env`   |
| documenter | Doc writer      | `/doc`, `/generate`             |

## Persona Structure

```yaml
---
name: persona
version: "4.3.0"
role: "One-line role"
token_budget: 300
triggers: ["/command"]
---
```

## Token Budgets

| Persona    | Budget | Priority |
| ---------- | ------ | -------- |
| auditor    | 400    | High     |
| developer  | 300    | High     |
| architect  | 300    | Medium   |
| debugger   | 350    | High     |
| tester     | 300    | Medium   |
| devops     | 300    | Medium   |
| documenter | 250    | Low      |

---

_DOMYH Agent v4.2_
