---
description: "🔬 Full project audit (12-expert panel with conditional activation)"
skills: { required: [audit-pro], contextual: [security, coding-rules, testing, observability, authentication] }
related_workflows: [review, security, test, verify, fix]
success_criteria: "Audit report generated with score and P0-P3 findings"
---

# 🔬 /ap — Audit Pro 

> 12-Expert Panel Audit (5 Core + 7 Conditional) • 277 Checkpoints • 16 Files
> 📊 ISO 25010 • CWE Top 25 • OWASP Top 10 • WCAG 2.2 • GDPR • SRE
> 📁 Data: `.agent/skills/cross-cutting/audit-pro/data/checklists/` (per-expert YAML)
> 🧠 SCoT Reasoning • Cross-Expert Critique • Smart Skill Loading

---

## AUDIT FLOW (10 Steps)

1. **DISCOVERY** (Auto 30s)
   - `hsa_session("audit project")`
   - `hsa_detect(stack)` → languages, frameworks, **project type** (web/desktop/CLI/library/MCP/mobile)
   - `hsa_explore(snapshot)` → count files, structure
   - **Diff-aware**: `git diff --name-only HEAD~5..HEAD` if recent commits
   - **Auto-activate** conditional experts based on detected project type

2. **SMART LOAD** (Token-Optimized, ~3000 tok vs 8000)
   - Load ONLY active expert checklists from `data/checklists/{expert}.yaml`
   - Load supplementary checklists if detected (desktop/CLI/library/MCP)
   - `hsa_search(skills, expert.keywords)` → load skill patterns per expert
   - Load `scoring.yaml` for weight profiles
   - **Auto-select weight profile** based on detection:
     ```
     electron/tauri deps  → desktop_app profile
     commander/yargs/clap → cli_tool profile
     publishConfig/exports → library_sdk profile
     react-native/flutter → mobile_app profile
     @modelcontextprotocol → mcp_plugin profile
     has_ai deps          → ai_ml_focus profile
     default              → default profile
     ```
   - **Fallback** (if HSA unavailable): read SKILL.md directly, search via grep

3. **SCOPE CONTRACT** — Display scope options (1-10) → ⛔ **STOP** wait for user
   - Show **active experts** + **supplementary checklists** detected
   - Show **auto-selected weight profile** based on project type
   - Show **previous audit score** if available

4. **EXECUTE** — Run Expert Panels with **SCoT Reasoning Protocol**:
   ```
   PER CHECKPOINT:
   1. LOCATE → hsa_search for relevant code
   2. UNDERSTAND → What does this code do?
   3. ASSESS → Does it meet the standard?
   4. EVIDENCE → file:line reference
   5. IMPACT → What could go wrong? (P0-P3)
   6. COUNTER → Why might this be acceptable? (Devil's advocate)
   7. VERDICT → PASS | FAIL | N/A (confidence 1-10)
   ```
   Show **progress**: `[Panel 2/8] Architecture — Checkpoint 12/20`
   
   **⚡ Context Window Optimization (prevents "lost-in-the-middle"):**
   - **Chunked execution**: Run 1 expert panel at a time, NOT all simultaneously
   - **Intermediate summary**: After each expert, compress results to compact format:
     ```
     [Security] Score: 8.2 | P0: 1 | P1: 3 | P2: 2 | Key: JWT expiration missing (SEC-001)
     ```
   - **Position engineering**: Place current expert's checklist in TAIL (high attention)
   - **Unload previous**: After summarizing expert, unload their checklist items
   - **Token ceiling**: If cumulative findings > 5000 tokens, compress older findings to 1-line summaries

5. **CRITIQUE ROUND** (Cross-Expert Challenge)
   - Only for P0 + P1 findings (skip P2/P3 to save tokens)
   - Security ↔ Architecture: "Could arch issues create security vulns?"
   - Architecture ↔ Security: "Are security measures over-engineered for this context?"
   - Performance ↔ Quality: "Do quality improvements hurt perf?"
   - Quality ↔ Performance: "Are perf optimizations maintainable?"
   - DevOps ↔ Security: "Are deployment practices secure? Are secrets properly managed?"
   - Each critique: AGREE | DISPUTE (reason) | ELEVATE | LOWER
   - **Counter-argument required**: Each expert MUST use their `counter_argument_guide`

6. **HOLISTIC SYNTHESIS** (NEW — Project-Level Assessment)
   > This step prevents "checklist blindness" — passing all checkpoints but missing systemic issues.
   
   After all experts complete, agent asks **5 holistic questions**:
   ```
   Q1. ARCHITECTURE COHERENCE: "Do all components fit together logically?
       Or are there design contradictions between modules?"
   Q2. RISK SURFACE: "What is the single biggest risk to this project?
       Not from a checklist — from holistic observation."
   Q3. TEAM CAPABILITY: "Based on code quality variance across files,
       are there capability gaps? (junior vs senior patterns)"
   Q4. TECHNICAL DEBT TRAJECTORY: "Is debt increasing or decreasing?
       Evidence: TODO count, complexity trends, test coverage direction."
   Q5. PRODUCTION READINESS: "If deployed tomorrow at 10x current load,
       what breaks first? What is the weakest link?"
   ```
   Each answer must include:
   - **Evidence** (file:line or metric)
   - **Severity** (Systemic-Critical / Systemic-Warning / Observation)
   - **Counter-argument** (why it might be acceptable)

7. **DEBATE ROUND** (NEW — Expert Panel Discussion)
   > All experts "discuss" the holistic findings. This catches tensions and tradeoffs.
   
   ```yaml
   debate_protocol:
     trigger: "After holistic synthesis, if Systemic-Critical found"
     format:
       - Moderator (agent) presents each systemic finding
       - Each relevant expert responds:
           FOR: "This is a real problem because..."
           AGAINST: "This is acceptable because..."
           CONDITION: "This is fine IF [condition], dangerous IF [condition]"
       - Moderator synthesizes: CONFIRMED | DOWNGRADED | CONDITIONAL
     
     example:
       finding: "Systemic: No rate limiting on any API endpoint"
       security_says: "FOR — this is critical, allows DoS"
       architecture_says: "CONDITION — fine for internal microservice, critical for public API"
       performance_says: "FOR — will cause cascading failures under load"
       devops_says: "AGAINST — reverse proxy handles rate limiting externally"
       verdict: "CONDITIONAL — verify reverse proxy config exists, if yes → P2, if no → P0"
   ```

8. **SELF-REVIEW** — Re-read findings, remove duplicates, verify evidence
   - Check: "Were disputed findings resolved?"
   - Check: "Are there contradictions between experts?"
   - Check: "Do holistic findings align with individual findings?"
   - Assign final confidence (1-10) per finding

9. **REPORT** — Score (0-10), findings by P0/P1/P2/P3, delta vs previous
   - Include **Holistic Assessment** section (from step 6)
   - Include **Debate Summary** (from step 7, if triggered)
   - Save to `.domyh/audits/audit_YYYY-MM-DD.md`

10. **MEMORY PERSIST** — `hsa_session(persist)`, update `audit_summary.json`

---

## EXPERT PANEL

### Core (Always Active — 5)

| ID           | EN Name        | VN Name | Seniority      | Skills Required                            |
| ------------ | -------------- | ------- | -------------- | ------------------------------------------ |
| security     | David Chen     | Minh    | Principal 15yr | `security`, `authentication`               |
| architecture | Sarah Kim      | Linh    | Staff 12yr     | `coding-rules`, `api-design`               |
| performance  | James Park     | Khoa    | Senior 10yr    | `observability`, `web-perf`                |
| quality      | Emma Wilson    | Hương   | Staff 12yr     | `testing`, `error-handling`, `coding-rules` |
| devops       | Michael Torres | Đức     | Senior 10yr    | `logging`, `observability`                 |

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

## EXPERT REASONING MANDATES

```yaml
reasoning_styles:
  security:     "Assume hostile actor. What can be exploited?"
  architecture: "Trace dependency flow. Where does coupling break isolation?"
  performance:  "Follow the hot path. Where will it break under load?"
  quality:      "Read the tests. What's NOT being tested?"
  devops:       "Imagine 3AM outage. Can the team recover?"
```

---

## DIFF-AWARE MODE

```yaml
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
    - "npx eslint --format json src/"
    - "npm audit --json"
    - "npx semgrep --config auto --json"
  python:
    - "ruff check --output-format json"
    - "pip-audit --format json"
    - "bandit -r src/ -f json"
  go:
    - "go vet ./..."
    - "govulncheck ./..."
    - "golangci-lint run --out-format json"
  rust:
    - "cargo clippy -- -W warnings"
    - "cargo audit"
  csharp:
    - "dotnet build --no-incremental"
    - "dotnet list package --vulnerable"
  general:
    - "trivy fs --format json ."
# Tool results fed as additional context → ~95% accuracy (vs ~78% AI-only)
```

---

## DATA LOADING (v2 — Per-Expert)

```yaml
# v1 (OLD): Load ALL checklists.yaml (8000 tokens)
# v2 (NEW): Load only active expert checklists (~3000 tokens)
checklists_dir: .agent/skills/cross-cutting/audit-pro/data/checklists/
scoring: .agent/skills/cross-cutting/audit-pro/data/scoring.yaml
loading: smart  # per-expert, lazy, token-optimized
```

---

## FINDING FORMAT (v2 — with SCoT)

```
**[P0]** 🔒 Expert `file:line` (Confidence: 9/10)
**Issue:** description
**Evidence:** code snippet
**Impact:** risk
**Counter:** why this might be acceptable
**Verdict:** FAIL (after considering counter-argument)
**Fix:** suggested fix
```

---

## REPORT FORMAT

```
📊 DOMYH AUDIT — [project] — [date] — Score: X.X/10 (↑0.3 from last)
| Expert | Score | Issues | Δ vs Last |
👥 Active Experts: 8/12 (Security, Architecture, Performance, Quality, DevOps, UX, Data, Reliability)
📁 Full: .domyh/audits/audit_YYYY-MM-DD.md
⏱️ Duration: Xm Ys | Files: N | Changed: M
🧠 SCoT: 7-step reasoning | Critique: X disputed, Y elevated
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
| `/ap desktop`        | Desktop app audit (Electron/Tauri)    |
| `/ap cli`            | CLI tool audit                        |
| `/ap library`        | Library/SDK publish audit             |
| `/ap mcp`            | MCP plugin/server audit               |

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