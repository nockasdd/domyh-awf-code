# 📄 DOMYH Awesome Code Templates v4.3

> Output templates for agent-generated reports and plans

## Available Templates (10)

| Template        | Type   | Commands         |
| --------------- | ------ | ---------------- |
| audit-report.md | Report | `/ap`            |
| debug-report.md | Report | `/debug`         |
| test-report.md  | Report | `/test`          |
| deploy-plan.md  | Plan   | `/deploy`        |
| project-plan.md | Plan   | `/init`          |
| migrate-plan.md | Plan   | `/migrate`       |
| task-list.md    | Format | `/plan`, `/code` |
| findings.md     | Format | all              |
| doc-template.md | Wizard | `/doc`           |
| error-format.md | Format | all              |

## Template Structure

```yaml
---
name: template-name
version: "4.3.0"
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

_DOMYH Awesome Code v4.3_
