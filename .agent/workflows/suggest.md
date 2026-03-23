---
description: "➡️ Smart suggestions: context-aware next steps based on project state"
skills: { required: [], contextual: [auto] }
success_criteria: "Top suggestions presented with rationale and commands"
---

# ➡️ /suggest — Smart Suggestions Pro

> Context-Aware Next Steps
> 📚 Auto-detect context • Prioritized • Actionable

---

## ⛔ RULES (Always Apply)

| # | Rule | Category |
|:--|:-----|:---------|
| R1 | Max 5 suggestions — don't overwhelm | UX |
| R2 | Every suggestion MUST include a runnable command | Actionable |
| R3 | Prioritize by impact: broken > missing > optional | Quality |

---

## SUGGEST FLOW

1. **ANALYZE** — Check recent activity, project state, pending tasks, git status.
2. **GENERATE** — Produce suggestions based on workflow stage, prioritized by impact + dependencies.
3. **PRESENT** — Show top 5 with priority, rationale, and quick-run command.

---

## COMMANDS

| Command | Focus |
|:--------|:------|
| `/suggest` | Smart suggestions (auto-detect context) |
| `/suggest code` | Code-focused next steps |
| `/suggest test` | Testing next steps |
| `/suggest deploy` | Deployment next steps |

---

## CONTEXT TRIGGERS

| After... | Check | Suggest |
|:---------|:------|:--------|
| `/code` | tests, lint, coverage | Run tests, check lint, commit |
| `/test` (pass) | — | Commit, create PR, deploy staging |
| `/test` (fail) | — | Fix failing tests, debug errors |
| `/deploy` | logs, metrics, errors | Monitor, health check, smoke tests |
| Project state | deps, coverage, TODOs, branches | Update deps, write tests, address TODOs, merge/delete |

---

## DEPLOY GUARDS

> Before suggesting deploy, verify prerequisites:

| Check | Fail Action |
|:------|:------------|
| `.git/` exists | Suggest: `git init` |
| Remote configured | Suggest: `git remote add origin <url>` |
| Clean working tree | Suggest: `git add . && git commit` |
| Tests pass | Suggest: `/test` first |

---

## OUTPUT FORMAT

```markdown
➡️ SMART SUGGESTIONS

Based on: {context summary}

| # | Priority | Suggestion | Rationale | Command |
|:--|:---------|:-----------|:----------|:--------|
| 1 | 🔴 High | Fix Failing Tests | 3 tests broken | `/test fix` |
| 2 | 🟠 Med | Improve Coverage | Below 80% target | `/test coverage` |
| 3 | 🟡 Low | Fix Lint Warnings | 5 new warnings | `/clean lint` |
| 4 | 🟡 Low | Commit Changes | 12 files modified | `git commit` |
| 5 | 🔵 Opt | Update Dependencies | 3 patches available | `/upgrade patch` |

Quick: Enter 1-5 to run suggestion
```

---

## REFLECTION CHECKPOINT

⛔ **MANDATORY** — Execute before completing this workflow (SESSION_005):

1. **VERIFY** — Does output meet success_criteria (see YAML frontmatter)?
2. **PERSIST** (if HSA available):
   - `hsa_session({action:'persist', task_summary:'[workflow] [summary]', files_touched:[...]})`
3. **PERSIST** (if HSA unavailable):
   - Append task summary to `memory/session.md`
