# Step 4: Critique Round

> Cross-expert challenge on P0/P1 findings only.

## Critique Pairs (5)

| Pair | Question |
|:-----|:---------|
| Security ↔ Architecture | "Could arch issues create security vulns?" |
| Architecture ↔ Security | "Are security measures over-engineered?" |
| Performance ↔ Quality | "Do quality improvements hurt perf?" |
| Quality ↔ Performance | "Are perf optimizations maintainable?" |
| DevOps ↔ Security | "Are deployment practices secure? Secrets managed?" |

## Outcomes

- **AGREE**: Confirmed, severity appropriate
- **DISPUTE**: Disagree because [reason] — may ELEVATE or LOWER
- **ELEVATE**: More severe than reported → upgrade priority
- **LOWER**: Less severe → recommend downgrade

## Rules

- Only P0 + P1 findings (skip P2/P3 — token savings)
- Each expert MUST use their `counter_argument_guide`
- Counter-argument is MANDATORY for every FAIL verdict
- N/A verdicts still require brief justification
