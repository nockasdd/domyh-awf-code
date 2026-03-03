---
description: "🔬 Full project audit (12-expert panel with conditional activation)"
skills: { required: [security, audit-pro], contextual: [auto] }
success_criteria: "Audit report generated with score and P0-P3 findings"
---

# 🔬 /ap — Audit Pro

> 12-Expert Panel Audit (5 Core + 7 Conditional) • 222 Checkpoints
> 📊 ISO 25010 • CWE Top 25 • OWASP Top 10 • WCAG 2.2 • GDPR • SRE
> 📁 Data: `.agent/skills/cross-cutting/audit-pro/data/` (HSA queryable)

---

## AUDIT FLOW

1. **DISCOVERY** (Auto 30s) — `hsa_session("audit project")`, detect stack (`hsa_detect`), project snapshot (`hsa_explore`), count files, load audit-pro checklists via HSA (`hsa_search`), check audit history, **diff-aware**: if recent commits, focus on `git diff --name-only HEAD~5..HEAD`, **auto-activate** conditional experts based on detected project type
2. **SCOPE CONTRACT** — Display scope options (from scoring.yaml) → ⛔ STOP wait for user selection (1-5). Show **previous audit score** if available for delta comparison. Show **active experts** based on detection
3. **EXECUTE** — Run active Expert Panels sequentially, collect findings with evidence. Show **progress**: `[Panel 2/8] Architecture — Checkpoint 12/20`
4. **SELF-REVIEW** — Agent re-reads findings, removes duplicates, verifies evidence accuracy, assigns confidence (1-10) per finding
5. **REPORT** — Production Readiness Score (0-10), findings by P0/P1/P2/P3, **delta** vs previous audit (↑↓), save to `.domyh/audits/audit_YYYY-MM-DD.md`
6. **MEMORY PERSIST** — Update `.agent/memory/audit_summary.json`, log decisions, update `.agent/memory/state.json` scores

---

## EXPERT PANEL

### Core (Always Active — 5)

| ID           | EN Name        | VN Name | Seniority      | Focus            |
| ------------ | -------------- | ------- | -------------- | ---------------- |
| security     | David Chen     | Minh    | Principal 15yr | OWASP, CWE, Auth |
| architecture | Sarah Kim      | Linh    | Staff 12yr     | SOLID, patterns  |
| performance  | James Park     | Khoa    | Senior 10yr    | Latency, memory  |
| quality      | Emma Wilson    | Hương   | Staff 12yr     | ISO 25010, tests |
| devops       | Michael Torres | Đức     | Senior 10yr    | CI/CD, IaC       |

### Conditional (Auto-detect — 7)

| ID          | EN Name           | VN Name | Seniority          | Activates When                |
| ----------- | ----------------- | ------- | ------------------ | ----------------------------- |
| ux          | Lisa Wang         | Thảo    | Senior 8yr         | UI files/deps detected        |
| data        | Robert Martinez   | Tuấn    | Principal 15yr     | DB/migration files detected   |
| compliance  | Jennifer Anderson | Hà      | Distinguished 18yr | Regulated industry indicators |
| product     | Daniel Lee        | Lan     | Tech Lead 10yr     | `scope_full` or user request  |
| reliability | William Brown     | Phong   | Staff 12yr         | Production/deploy files       |
| cloud       | Alexander White   | Bảo     | Senior 10yr        | IaC/Terraform/K8s files       |
| ai_safety   | Dr. Sophia Nguyen | Vy      | Distinguished 20yr | AI/ML/LLM code/deps           |

---

## DIFF-AWARE MODE

```yaml
# When recent changes detected:
diff_aware:
  trigger: "git log -1 --since='7 days ago'"
  scope: "git diff --name-only HEAD~5..HEAD"
  behavior: "Focus audit on changed files + their dependents"
  full_scan: "Still run full scan but prioritize changed files first"
```

---

## TOOL INTEGRATION (Optional)

> If tools available in project, auto-run BEFORE AI audit for higher accuracy:

```yaml
pre_audit_tools:
  javascript:
    - "npx eslint --format json src/" # Lint issues
    - "npm audit --json" # Dependency vulns
    - "npx semgrep --config auto --json" # SAST security
  python:
    - "ruff check --output-format json" # Lint
    - "pip-audit --format json" # Dependency vulns
    - "bandit -r src/ -f json" # Security
  go:
    - "go vet ./..." # Static analysis
    - "govulncheck ./..." # Vulnerability check
    - "golangci-lint run --out-format json" # Lint
  general:
    - "trivy fs --format json ." # Container/FS scan
# Tool results are fed as additional context to Expert Panels
# This achieves ~95% accuracy (vs ~78% AI-only)
```

---

## DATA LOADING

```yaml
checklists: .agent/skills/cross-cutting/audit-pro/data/checklists.yaml # 12 experts, 222 checkpoints
scoring: .agent/skills/cross-cutting/audit-pro/data/scoring.yaml # 6 weight profiles, grades, scope options
```

---

## FINDING FORMAT

```
**[P0]** 🔒 Expert `file:line` (Confidence: 9/10)
**Issue:** description  **Evidence:** code snippet  **Impact:** risk  **Fix:** suggested fix
```

---

## REPORT FORMAT

```
📊 DOMYH AUDIT — [project] — [date] — Score: X.X/10 (↑0.3 from last)
| Expert | Score | Issues | Δ vs Last |
👥 Active Experts: 8/12 (Security, Architecture, Performance, Quality, DevOps, UX, Data, Reliability)
📁 Full: .domyh/audits/audit_YYYY-MM-DD.md
⏱️ Duration: Xm Ys | Files: N | Changed: M
```

---

## SUB-COMMANDS

| Command              | Description                           |
| -------------------- | ------------------------------------- |
| `/ap`                | Full audit (all active experts)       |
| `/ap quick`          | Quick audit (Security + Architecture) |
| `/ap security`       | Security focus only                   |
| `/ap performance`    | Performance focus only                |
| `/ap expert [name]`  | Single expert audit                   |
| `/ap --scope [path]` | Limit scope                           |
| `/ap --diff`         | Diff-aware (changed files only)       |
| `/ap --compare`      | Compare with previous audit           |
| `/ap --experts`      | Show active/inactive expert status    |
| `/ap --force [name]` | Force-include a conditional expert    |

---

## REFLECTION CHECKPOINT

⛔ **MANDATORY** — Execute before completing this workflow (SESSION_005):

1. **VERIFY** — Does output meet success_criteria (see YAML frontmatter)?
2. **PERSIST** (if HSA available — preferred, 1 tool call):
   - `hsa_session({action:'persist', task_summary:'[workflow] [summary]', files_touched:[...], auto_notify:true})`
   - If key decision → `hsa_session({action:'anchor', content:'[decision]', category:'decision'})`
3. **PERSIST** (if HSA unavailable — manual fallback):
   - Append task summary to `memory/session.md`
   - If last task → Update `memory/CONTEXT_SNAPSHOT.md`

