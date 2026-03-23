---
description: "🔧 Fix existing project: detect stack → analyze issues → plan → execute → verify"
skills: { required: [coding-rules], contextual: [auto] }
success_criteria: "issues fixed, lint/type/test pass, debt score improved"
---

# 🔧 /modify — Project Modification Pro

> AI-Powered Issue Resolution & Legacy Modernization
> 📚 30+ Languages • Technical Debt Scoring • Automated Analysis

---

## ⛔ RULES (Always Apply)

| # | Rule | Category |
|:--|:-----|:---------|
| R1 | ⛔ STOP after PLAN — confirm scope with user before executing | Safety |
| R2 | Never modify production config without backup | Safety |
| R3 | Run lint/type check after every change batch | Quality |
| R4 | Preserve existing behavior unless explicitly asked to change | Quality |
| R5 | Document breaking changes in commit message | Communication |

---

## MODIFICATION FLOW (6 Phases)

1. **DETECT** — `hsa_session`, `hsa_detect`, identify architecture pattern, map project structure. Show: `[1/6] Detected: {stack} | Files: {n} | Packages: {m}`
2. **ANALYZE** — Scan for issues by category (Security P0 → Dependencies P0-P1 → Quality P1-P2 → Performance P2 → Tests P2 → Tech Debt P2-P3). Use stack-specific tools via `hsa_detect`.
   Show: `[2/6] Analysis: {n} issues (P0: {x}, P1: {y}, P2: {z}) | Debt: {score}/10`
3. **PLAN** — Group issues by priority (P0→P3), each with `file:line` references. Estimate effort.
   → ⛔ **STOP: "Select scope: [1] Fix ALL | [2] P0+P1 | [3] P0 only | [4] Interactive"**
4. **EXECUTE** — Apply fixes per approved scope. For each: Issue → File:Line → Before/After diff → Reason.
   Track: `[4/6] Fix #{n}/{m} | P0: {x}/{y} ✅ | Files: {n} modified`
5. **VERIFY** — Run lint → type check → tests → build (per stack). Show pass/fail summary.
   > Stack-specific verify commands: use `hsa_detect` result to select lint/test/build tools.
6. **REPORT** — Summary: fixed count, files changed, lines ±, debt score before→after. Suggest next steps. `hsa_check_changes` to update index.

---

## COMMANDS

| Command | Focus | Description |
|:--------|:------|:------------|
| `/modify` | All issues | Full analysis & fix |
| `/modify --security` | Vulnerabilities | Security-focused scan |
| `/modify --deps` | Dependencies | Outdated/vulnerable |
| `/modify --quality` | Code quality | Lint, types, smells |
| `/modify --perf` | Performance | Bottlenecks, N+1 |
| `/modify --quick` | P0 only | Critical fixes, no confirm |
| `/modify ./src` | Specific path | Directory-scoped scan |
| `/modify debt score` | Tech debt | Calculate debt score (0-100) |

---

## ISSUE CATEGORIES

| Category | Priority | What to Check | Tools (auto-detected via `hsa_detect`) |
|:---------|:---------|:--------------|:---------------------------------------|
| Security | P0 | Hardcoded secrets, SQL injection, XSS, insecure deps, missing auth | gosec, bandit, npm audit, snyk |
| Dependencies | P0-P1 | Outdated, vulnerable, unused, license issues | govulncheck, pip-audit, depcheck |
| Code Quality | P1-P2 | Lint errors, type errors, dead code, complexity | golangci-lint, ruff, eslint, clippy |
| Performance | P2 | N+1 queries, memory leaks, missing indexes | pprof, py-spy, clinic.js |
| Tests | P2 | Missing coverage, failing, flaky, outdated mocks | go test, pytest, jest |
| Tech Debt | P2-P3 | TODO/FIXME, deprecated APIs, legacy patterns | grep, AST analysis |

---

## PRIORITY MATRIX

| Priority | Description | SLA | Action |
|:---------|:------------|:----|:-------|
| **P0** | Critical security/breaking | Immediate | Must fix now |
| **P1** | High impact bugs | This session | Should fix |
| **P2** | Medium quality issues | This week | Queue next |
| **P3** | Low improvements | Optional | Backlog |

---

## TECHNICAL DEBT SCORING

```
Score = complexity×0.3 + coverage_gap×0.2 + dependency_age×0.2 + security_findings×0.3
```

| Level | Score | Action |
|:------|:------|:-------|
| Healthy | < 20 | Minimal maintenance |
| Manageable | 20-50 | Regular maintenance |
| Concerning | 50-80 | Prioritize remediation |
| Critical | > 80 | Modernize now |

---

## MODERNIZATION PATTERNS

| Pattern | Trigger | Description |
|:--------|:--------|:------------|
| Extract Method | Function > 50 lines | Break down large functions |
| Replace Conditional | Nesting > 3 levels | Simplify complex conditionals |
| Parameter Object | Params > 4 | Group related parameters |
| Extract Class | Class > 500 lines | Split responsibilities |
| Remove Dead Code | Unreachable detected | Delete unused code |
| API Modernization | Deprecated calls | Replace with modern equivalents |

---

## CASCADE EVALUATION (Recommended — MCP)

⚠️ **Evaluate before EXECUTE** — see `delegation-intelligence` skill for scoring.

```
hsa_delegate({action:'cascade', cascade_text:'[prompt]', task_type:'code'})
→ wait 5s → hsa_delegate({action:'cascade_read', cascade_id:'...'})
```
**Auto-cascade** (≥6.5): >50 issues, multi-language project, legacy modernization
**Suggest cascade** (4.0-6.5): >20 issues, complex dependency updates

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
