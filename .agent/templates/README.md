# 📄 DOMYH Awesome Code Templates

> Output templates for agent-generated reports and plans

## Available Templates (15)

| Template                       | Type       | Commands         |
| ------------------------------ | ---------- | ---------------- |
| audit-report.md                | Report     | `/ap`            |
| debug-report.md                | Report     | `/debug`         |
| test-report.md                 | Report     | `/test`          |
| deploy-plan.md                 | Plan       | `/deploy`        |
| project-plan.md                | Plan       | `/init`          |
| migrate-plan.md                | Plan       | `/migrate`       |
| task-list.md                   | Format     | `/plan`, `/code` |
| findings.md                    | Format     | all              |
| doc-template.md                | Wizard     | `/doc`           |
| phase-template.md              | Format     | `/init`, `/plan` |
| feature-lifecycle.md           | Lifecycle  | `/feature`       |
| reflection/critic.md           | Reflection | `/code`, `/fix`  |
| reflection/error_analysis.md   | Reflection | `/debug`, `/fix` |
| reflection/success_analysis.md | Reflection | `/code`, `/ap`   |
| reflection/pivot_analysis.md   | Reflection | `/debug`, `/fix` |

## Template Structure

```yaml
---
name: template-name
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
