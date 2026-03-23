---
description: "🔬 Full project audit (12-expert panel with conditional activation)"
skills: { required: [audit-pro], contextual: [security, coding-rules, testing, observability, authentication] }
related_workflows: [review, security, test, verify, fix]
success_criteria: "Audit report generated with score and P0-P3 findings"
---

# 🔬 /ap — Audit Pro

> 12-Expert Panel (5 Core + 7 Conditional) • 277 Checkpoints • 16 Files
> 📊 ISO 25010:2023 • CWE Top 25 • OWASP Top 10 • WCAG 2.2 • GDPR • SRE
> 📁 Data: `.agent/skills/cross-cutting/audit-pro/data/checklists/` (per-expert YAML)

---

## ⛔ RULES (Always Apply)

| # | Rule | Category |
|:--|:-----|:---------|
| R1 | All findings MUST have `file:line` evidence | Quality |
| R2 | Counter-argument MANDATORY for every FAIL verdict | Fairness |
| R3 | ⛔ STOP at step 3 — user MUST select scope before execute | Safety |
| R4 | Max total token budget: 40K (core 30K + conditional 10K) | Efficiency |
| R5 | If expert panel exceeds 8K tokens → compress + move on | Efficiency |
| R6 | P0/P1 findings MUST go through Critique Round — never skip | Quality |
| R7 | Negative probe every PASS on P0/P1 checkpoint: "What would make this FAIL?" | Bias Mitigation |

---

## AUDIT FLOW (11 Steps)

1. **DISCOVERY** (30s)
   - `hsa_session("audit project")`, `hsa_detect(stack)` → languages, frameworks, project type
   - `hsa_explore(snapshot)` → file count, structure
   - `git diff --name-only HEAD~5..HEAD` → diff-aware if recent commits
   - Load previous audit from `.domyh/audits/` → extract score + unresolved findings
   - Auto-activate conditional experts based on detected project type

2. **RISK ASSESSMENT** (NEW — 30s heuristic scan)
   ```yaml
   inputs: [project_type, file_count, dep_count, git_history, complexity_hotspots]
   output:
     hot_zones: ["auth/", "api/", "config/"]  # High-risk — full SCoT
     warm_zones: ["services/", "models/"]      # Medium — standard SCoT
     cold_zones: ["docs/", "scripts/", "test/"] # Low — lightweight SCoT
     risk_score: X/10
   impact: "EXECUTE prioritizes hot_zones first, applies SCoT tiering"
   ```

3. **SMART LOAD** (Token-Optimized, ~3000 tok)
   - Load ONLY active expert checklists from `data/checklists/{expert}.yaml`
   - Load supplementary checklists if detected (desktop/CLI/library/MCP)
   - `hsa_search(skills, expert.keywords)` → skill patterns per expert
   - Auto-select weight profile from `scoring.yaml`:
     `electron/tauri → desktop_app` | `commander/clap → cli_tool` | `publishConfig → library_sdk`
     `react-native/flutter → mobile_app` | `@modelcontextprotocol → mcp_plugin` | `default`

4. **SCOPE CONTRACT** — Display scope (1-10) → ⛔ **STOP** wait for user
   - Show: active experts, supplementary checklists, weight profile, previous score, risk zones

5. **EXECUTE** — Run Expert Panels with **SCoT Tiering**:

   **SCoT Tiering** (based on Risk Assessment zones):
   | Zone | SCoT Level | Steps | Example |
   |:-----|:-----------|:------|:--------|
   | Hot (P0/P1 risk) | Full 7-step | LOCATE→UNDERSTAND→ASSESS→EVIDENCE→IMPACT→COUNTER→VERDICT | Auth, secrets |
   | Warm (P2 risk) | Standard 5-step | LOCATE→UNDERSTAND→ASSESS→EVIDENCE→VERDICT | Business logic |
   | Cold (P3 risk) | Lightweight 3-step | LOCATE→ASSESS→VERDICT | Docs, scripts |

   **Context Window Optimization:**
   - Chunked: 1 expert panel at a time, NOT simultaneous
   - Intermediate summary after each expert: `[Security] Score: 8.2 | P0:1 P1:3 P2:2 | Key: ...`
   - Position engineering: current checklist in TAIL (high attention zone)
   - Token ceiling: cumulative findings >5000 tok → compress older to 1-line
   - **Budget**: If approaching 40K → skip P2/P3, complete P0/P1 only → suggest `/ap --resume`

   Show progress: `[Panel 2/8] Architecture — Checkpoint 12/20`

6. **CRITIQUE ROUND** (P0/P1 only)
   - Security ↔ Architecture | Performance ↔ Quality | DevOps ↔ Security
   - Each critique: AGREE | DISPUTE (reason) | ELEVATE | LOWER
   - Counter-argument REQUIRED per expert's `counter_argument_guide`

7. **HOLISTIC SYNTHESIS** (5 project-level questions)
   > Prevents "checklist blindness" — passing all checkpoints but missing systemic issues.

   | # | Question | Focus |
   |:--|:---------|:------|
   | Q1 | Architecture Coherence | Design contradictions between modules? |
   | Q2 | Risk Surface | Single biggest risk (from observation, not checklist)? |
   | Q3 | Team Capability | Code quality variance → capability gaps? |
   | Q4 | Tech Debt Trajectory | Increasing or decreasing? (TODOs, complexity, coverage) |
   | Q5 | Production Readiness | At 10x load, what breaks first? |

   Each answer: Evidence (file:line) + Severity (Systemic-Critical/Warning/Observation) + Counter-argument

8. **DEBATE ROUND** (conditional)
   - Trigger: Systemic-Critical found OR ≥3 Systemic-Warning
   - Each expert responds: FOR | AGAINST | CONDITION
   - Moderator synthesizes: CONFIRMED | DOWNGRADED | CONDITIONAL

9. **SELF-REVIEW** — Deduplicate, verify evidence, resolve disputes, assign final confidence (1-10)

   > ⚠️ **ERROR RECOVERY**: If interrupted → save to `.domyh/audits/audit_PARTIAL_YYYY-MM-DD.md` → `/ap --resume`

10. **REPORT** — Score (0-10), P0/P1/P2/P3 findings, delta vs previous
    - Include: Holistic Assessment, Debate Summary (if triggered), Token Usage (XK/40K)
    - Save to `.domyh/audits/audit_YYYY-MM-DD.md`

11. **PERSIST** — `hsa_session(persist)`, update `audit_summary.json`

---

## EXPERT PANEL

### Core (Always Active — 5)

| ID | Expert | Seniority | Skills | Reasoning Style |
|:---|:-------|:----------|:-------|:----------------|
| security | David Chen | Principal 15yr | `security`, `authentication` | Assume hostile actor |
| architecture | Sarah Kim | Staff 12yr | `coding-rules`, `api-design` | Trace dependency flow |
| performance | James Park | Senior 10yr | `observability`, `web-perf` | Follow the hot path |
| quality | Emma Wilson | Staff 12yr | `testing`, `error-handling` | What's NOT being tested? |
| devops | Michael Torres | Senior 10yr | `logging`, `observability` | Imagine 3AM outage |

### Conditional (Auto-detect — 7)

| ID | Expert | Seniority | Activates When |
|:---|:-------|:----------|:---------------|
| ux | Lisa Wang | Senior 8yr | UI files/deps detected |
| data | Robert Martinez | Principal 15yr | DB/migration files detected |
| compliance | Jennifer Anderson | Distinguished 18yr | Regulated industry indicators |
| product | Daniel Lee | Tech Lead 10yr | `scope_full` or user request |
| reliability | William Brown | Staff 12yr | Production/deploy files |
| cloud | Alexander White | Senior 10yr | IaC/Terraform/K8s files |
| ai_safety | Dr. Sophia Nguyen | Distinguished 20yr | AI/ML/LLM code/deps |

---

## TOOL INTEGRATION

> Auto-run BEFORE AI audit if tools available → ~95% accuracy (vs ~78% AI-only)

| Stack | Commands |
|:------|:---------|
| JavaScript | `npx eslint --format json src/`, `npm audit --json`, `npx semgrep --config auto --json` |
| Python | `ruff check --output-format json`, `pip-audit --format json`, `bandit -r src/ -f json` |
| Go | `go vet ./...`, `govulncheck ./...`, `golangci-lint run --out-format json` |
| Rust | `cargo clippy -- -W warnings`, `cargo audit` |
| C#/.NET | `dotnet build --no-incremental`, `dotnet list package --vulnerable` |
| General | `trivy fs --format json .` |

---

## FINDING FORMAT

```
**[P0]** 🔒 Expert `file:line` (Confidence: 9/10)
Issue: description | Evidence: code snippet | Impact: risk
Counter: why acceptable | Verdict: FAIL | Fix: suggested fix
```

## REPORT FORMAT

```
📊 DOMYH AUDIT — [project] — [date] — Score: X.X/10 (↑0.3 from last)
| Expert | Score | Issues | Δ vs Last |
👥 Active: 8/12 | 📁 .domyh/audits/audit_YYYY-MM-DD.md
⏱️ Xm Ys | Files: N | Changed: M | Tokens: XK/40K
🔍 Holistic: [biggest risk] | ⚔️ Debate: [verdict if triggered]
```

---

## SUB-COMMANDS

| Command | Description |
|:--------|:------------|
| `/ap` | Full audit (all active experts) |
| `/ap quick` | Quick audit (Security + Architecture) |
| `/ap security` / `/ap performance` | Single-domain focus |
| `/ap expert [name]` | Single expert audit |
| `/ap --scope [path]` | Limit scope to path |
| `/ap --diff` | Diff-aware (changed files + dependents) |
| `/ap --compare` | Compare with previous audit |
| `/ap --resume` | Resume interrupted audit |
| `/ap --force [name]` | Force-include conditional expert |
| `/ap desktop` / `cli` / `library` / `mcp` | Platform-specific audit |

---

## REFLECTION CHECKPOINT

⛔ **MANDATORY** — Execute before completing this workflow (SESSION_005):

1. **VERIFY** — Does output meet success_criteria (see YAML frontmatter)?
2. **PERSIST** (if HSA available — preferred, 1 tool call):
   - `hsa_session({action:'persist', task_summary:'[workflow] [summary]', files_touched:[...]})`
   - If key decision → `hsa_session({action:'anchor', content:'[decision]', category:'decision'})`
3. **PERSIST** (if HSA unavailable — manual fallback):
   - Append task summary to `memory/session.md`
   - If last task → Update `memory/CONTEXT_SNAPSHOT.md`