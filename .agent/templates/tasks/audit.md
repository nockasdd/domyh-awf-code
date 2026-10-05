# Audit Task Template

> Structured template for audit tasks

---

## Schema

```yaml
task_type: audit

# Required fields
scope: string              # What to audit
audit_type: enum           # [full, security, performance, quality]

# Optional fields
experts: list              # Which experts to use
checklist: reference       # Link to checklist
output_format: reference   # Link to output format
focus_areas: list          # Specific areas to emphasize
exclusions: list           # Areas to skip
```

---

## Example Task

```yaml
task:
  type: audit
  
  scope: |
    Full backend audit of the WebServer project.
    Focus on security, performance, and code quality.
  
  audit_type: full
  
  experts:
    - alex:     # Security
        focus: ["Authentication", "Input validation", "SQL injection"]
        weight: 1.5
    - sarah:    # Quality
        focus: ["Test coverage", "Code maintainability"]
        weight: 1.2
    - david:    # Code
        focus: ["Design patterns", "Error handling"]
        weight: 1.0
    - emma:     # Performance
        focus: ["Database queries", "API latency"]
        weight: 1.0
    - mike:     # DevOps
        focus: ["CI/CD", "Docker config", "Monitoring"]
        weight: 1.0
  
  focus_areas:
    - Payment processing (critical)
    - User authentication
    - Database queries
  
  exclusions:
    - Legacy migration scripts
    - Deprecated API v1 endpoints
  
  checklist:
    security: "checklists/security-audit.yaml"
    quality: "checklists/quality-audit.yaml"
    performance: "checklists/performance-audit.yaml"
  
  output_format: "templates/output/finding.md"
  
  priority: P1
  
  deliverables:
    - Prioritized finding list (P0-P3)
    - Executive summary
    - Remediation recommendations
```

---

## Usage in Prompts

```markdown
## Task: Audit

**Scope:**
{{task.scope}}

**Audit Type:** {{task.audit_type}}

**Expert Panel:**
{{#task.experts}}
- **{{name}}** ({{domain}}): {{#focus}}{{.}}, {{/focus}}
{{/task.experts}}

**Focus Areas:**
{{#task.focus_areas}}
- 🎯 {{.}}
{{/task.focus_areas}}

**Exclusions:**
{{#task.exclusions}}
- ⏭️ {{.}}
{{/task.exclusions}}

**Deliverables:**
{{#task.deliverables}}
- [ ] {{.}}
{{/task.deliverables}}
```

---

## Workflow Integration

This task type triggers:
- **Persona:** Auditor (12-expert panel with SCoT reasoning)
- **Workflow:** /ap workflow
- **Output:** Finding report with P0-P3 prioritization

---

## Audit Types

### Full Audit
All experts participate, comprehensive review.

### Security Audit
- Lead: Alex (Security)
- Support: David (Code for secure coding)
- Focus: OWASP Top 10, CWE Top 25

### Performance Audit
- Lead: Emma (Performance)
- Support: Mike (DevOps for infrastructure)
- Focus: Bottlenecks, N+1 queries, caching

### Quality Audit
- Lead: Sarah (Quality)
- Support: David (Code)
- Focus: Test coverage, maintainability, code smells

---
