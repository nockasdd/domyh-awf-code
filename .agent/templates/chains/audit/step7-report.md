# Step 7: Report

> Generate final audit report → save to `.domyh/audits/`

## Report Structure

```markdown
## 🔬 Audit Report — {project_name}
**Date**: YYYY-MM-DD | **Score**: X.X/10 | **Grade**: A/B/C/D/F

### Summary
| Severity | Count | Key Finding |
|----------|-------|-------------|
| 🔴 P0    | X     | [most critical] |
| 🟠 P1    | X     | |
| 🟡 P2    | X     | |
| ⚪ P3    | X     | |

### Expert Scores
| Expert | Score | P0 | P1 | P2 | Key Finding |
|--------|-------|----|----|----|-------------|

### Holistic Assessment
- Architecture Coherence: [assessment]
- Biggest Risk: [assessment]
- Tech Debt Trajectory: [assessment]
- Production Readiness: [assessment]

### Debate Summary (if triggered)
| Finding | For | Against | Verdict |

### Detailed Findings
#### [P0] 🔴 [Title]
**File:** path/file.go:45
**Expert:** Security
**Evidence:** [code snippet]
**Counter-argument:** [why this might be acceptable]
**Recommendation:** [fix]
**Confidence:** 9/10
```

## Save Locations
1. `.domyh/audits/audit_YYYY-MM-DD.md` — in project
2. `hsa_session(persist)` — in agent memory
3. `memory/audit_summary.json` — update with score + P0 count
