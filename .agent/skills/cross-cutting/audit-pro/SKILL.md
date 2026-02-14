# Audit Pro System

12-Expert Panel audit system with 222 checkpoints. Conditional activation auto-detects project type (UI, DB, regulated, AI, cloud).

## Decision Tree

```
/ap → Discovery
  ├─ Stack detection (auto)
  │   ├─ Frontend detected → Activate UX/A11y Expert
  │   ├─ Database files → Activate Database Expert
  │   ├─ Cloud config → Activate Cloud Expert
  │   ├─ API routes → Activate API Expert
  │   ├─ ML models → Activate AI Safety Expert
  │   ├─ Regulated industry → Activate Compliance Expert
  │   └─ Mobile project → Activate Mobile Expert
  ├─ Complexity estimation
  │   ├─ Small (<50 files) → Express audit (~15 min)
  │   ├─ Medium (50-200) → Standard audit (~30 min)
  │   └─ Large (200+) → Deep audit (~60 min)
  └─ Expert panel assignment (5 core + conditional)
```

## Standards

- ISO 25010 (quality model)
- CWE Top 25 (security weaknesses)
- OWASP Top 10 (web security)
- WCAG 2.2 (accessibility)
- GDPR (data privacy)
- SRE (reliability engineering)

## Expert Panel

### Core Experts (5 — always active)

| Expert       | Domain                         | Checkpoints |
| ------------ | ------------------------------ | ----------- |
| Security     | Auth, injection, data exposure | ~30         |
| Architecture | Patterns, modularity, coupling | ~30         |
| Performance  | Latency, throughput, memory    | ~25         |
| Quality      | Code smells, testing, docs     | ~35         |
| DevOps       | CI/CD, deployment, monitoring  | ~25         |

### Conditional Experts (7 — auto-activated)

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
3. **Parallel Audit**: Each expert evaluates independently with evidence
4. **Consensus**: Cross-reference findings, resolve conflicts, prioritize
5. **Report**: Production readiness score, findings by severity (P0-P3)

## Severity Levels

| Level | Name     | Description                | Action Required |
| ----- | -------- | -------------------------- | --------------- |
| P0    | Critical | Security breach, data loss | Block deploy    |
| P1    | High     | Significant vulnerability  | Fix before prod |
| P2    | Medium   | Quality/performance issue  | Fix in sprint   |
| P3    | Low      | Tech debt, style issues    | Backlog         |

## Scoring

- **A (90-100)**: Production ready
- **B (75-89)**: Minor issues, safe to deploy
- **C (60-74)**: Significant issues, fix before deploy
- **D (40-59)**: Major issues, not production ready
- **F (0-39)**: Critical issues, requires redesign

## Report Format

```markdown
# 🔬 Audit Pro Report — {Project Name}

## Summary

- Score: **B (82/100)**
- Experts: 5 core + 2 conditional
- Findings: 3 P1, 7 P2, 12 P3

## P0 Critical (0)

_None found_ ✅

## P1 High (3)

1. [SEC-001] SQL injection in user search — `api/users.ts:45`
2. [SEC-002] Missing rate limiting on auth endpoints
3. [PERF-001] N+1 query in dashboard list

## Recommendations

1. Fix all P1 before production deployment
2. Address P2 issues in next sprint
3. Schedule P3 items in backlog
```

## Data Files

- `data/checklists.yaml` — Full checkpoint definitions
- `data/scoring.yaml` — Scoring weights and formulas
