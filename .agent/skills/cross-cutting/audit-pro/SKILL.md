# Audit Pro System

12-Expert Panel audit system with 222 checkpoints. Conditional activation auto-detects project type (UI, DB, regulated, AI, cloud).

## Standards

- ISO 25010 (quality model)
- CWE Top 25 (security weaknesses)
- OWASP Top 10 (web security)
- WCAG 2.2 (accessibility)
- GDPR (data privacy)
- SRE (reliability engineering)

## Expert Panel

### Core Experts (5 - always active)

| Expert       | Domain                         | Checkpoints |
| ------------ | ------------------------------ | ----------- |
| Security     | Auth, injection, data exposure | ~30         |
| Architecture | Patterns, modularity, coupling | ~30         |
| Performance  | Latency, throughput, memory    | ~25         |
| Quality      | Code smells, testing, docs     | ~35         |
| DevOps       | CI/CD, deployment, monitoring  | ~25         |

### Conditional Experts (7 - auto-activated)

| Expert     | Trigger                 | Domain                        |
| ---------- | ----------------------- | ----------------------------- |
| UX/A11y    | Frontend detected       | WCAG, usability               |
| Database   | DB files detected       | Schema, queries, migrations   |
| Compliance | Regulated industry      | GDPR, HIPAA, PCI-DSS          |
| AI Safety  | ML models detected      | Bias, drift, interpretability |
| Cloud      | Cloud config detected   | Cost, HA, disaster recovery   |
| API        | API routes detected     | REST maturity, versioning     |
| Mobile     | Mobile project detected | Platform guidelines           |

## Workflow

```
/ap → Discovery → Expert Assignment → Parallel Audit → Consensus → Report
```

1. **Discovery**: Detect stack, count files, estimate complexity
2. **Expert Assignment**: Activate relevant experts based on project type
3. **Parallel Audit**: Each expert evaluates independently
4. **Consensus**: Cross-reference findings, resolve conflicts
5. **Report**: Production readiness score, prioritized findings

## Scoring

- **A (90-100)**: Production ready
- **B (75-89)**: Minor issues, safe to deploy
- **C (60-74)**: Significant issues, fix before deploy
- **D (40-59)**: Major issues, not production ready
- **F (0-39)**: Critical issues, requires redesign

## Data Files

- `data/checklists.yaml` — Full checkpoint definitions
- `data/scoring.yaml` — Scoring weights and formulas
