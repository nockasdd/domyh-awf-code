# 📄 DOMYH Awesome Code Templates v6.2.1

> Output templates for agent-generated reports and plans

## Available Templates (11)

| Template          | Type   | Commands         |
| ----------------- | ------ | ---------------- |
| audit-report.md   | Report | `/ap`            |
| debug-report.md   | Report | `/debug`         |
| test-report.md    | Report | `/test`          |
| deploy-plan.md    | Plan   | `/deploy`        |
| project-plan.md   | Plan   | `/init`          |
| migrate-plan.md   | Plan   | `/migrate`       |
| task-list.md      | Format | `/plan`, `/code` |
| findings.md       | Format | all              |
| doc-template.md   | Wizard | `/doc`           |
| phase-template.md | Format | `/init`, `/plan` |

## Template Structure

```yaml
---
name: template-name
version: "6.2.1"
type: report|plan|format|wizard
triggers: ["/command"]
---
```

## Placeholder Standard

Use `{PLACEHOLDER}` format:

- `{PROJECT_NAME}` - Project name
- `{DATE}` - Current date
- `{SCOPE}` - Audit scope
- `{LANG}` - Language/stack

---

_DOMYH Awesome Code_
