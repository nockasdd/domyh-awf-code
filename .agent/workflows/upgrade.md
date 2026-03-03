---
description: "📦 Update dependencies: check outdated, apply safe updates, review breaking changes"
skills: { required: [], contextual: [auto] }
success_criteria: "Dependencies updated, no vulnerabilities, tests pass"
---

# 📦 /upgrade — Upgrade Pro

> Security-First Dependency Updates
> 📚 Multi-language • Vulnerability Scanning • Safe Update Order • Changelog Review

---

## UPGRADE FLOW

1. **DETECT** — Detect stack via HSA (`hsa_detect`), detect package manager, list outdated. Show: `[Step 1/6] Scanning 127 dependencies...`
2. **PLAN** — Check changelogs, identify breaking changes, classify by semver. Show: `Found: 3 security, 8 patch, 4 minor, 2 major`
3. **EXECUTE (Safe)** — Apply patches + minor updates automatically
4. **EXECUTE (Major)** — ⛔ STOP: show breaking changes, confirm before applying major updates
5. **VERIFY** — Run tests, build, lint after each batch. Show: `[Step 5/6] Tests: ✅ 42/42 passed`
6. **SYNC** — Summary of updates, failed updates, breaking changes noted. `hsa_check_changes`

---

## COMMANDS

| Command             | Description         | Scope     |
| ------------------- | ------------------- | --------- |
| `/upgrade`          | Check outdated      | List only |
| `/upgrade patch`    | Apply patches       | Safe      |
| `/upgrade minor`    | Apply minor updates | Review    |
| `/upgrade major`    | Major update guide  | Manual    |
| `/upgrade security` | Security fixes only | Critical  |
| `/upgrade --dry`    | Preview only        | Safe      |
| `/upgrade lockfile` | Regenerate lockfile | Lockfile  |

---

## 🔧 DEPENDENCY TOOLS

| Language   | Check Outdated                            | Update                             | Security Scan                      |
| ---------- | ----------------------------------------- | ---------------------------------- | ---------------------------------- |
| Go         | `go list -m -u all`                       | `go get -u`                        | `govulncheck ./...`                |
| TypeScript | `npm outdated`                            | `npm update`                       | `npm audit`                        |
| Python     | `pip list --outdated`                     | `pip install -U`                   | `pip-audit`                        |
| Rust       | `cargo outdated`                          | `cargo update`                     | `cargo audit`                      |
| Java       | `mvn versions:display-dependency-updates` | `mvn versions:use-latest-versions` | `mvn dependency-check:check`       |
| C#         | `dotnet list package --outdated`          | `dotnet add package`               | `dotnet list package --vulnerable` |
| Ruby       | `bundle outdated`                         | `bundle update`                    | `bundle audit`                     |
| PHP        | `composer outdated`                       | `composer update`                  | `composer audit`                   |

---

## 📊 UPDATE ORDER (Safety First)

| Priority | Type             | Risk        | Action                            |
| -------- | ---------------- | ----------- | --------------------------------- |
| 1        | Security patches | 🔴 Critical | Update immediately                |
| 2        | Bug fix patches  | 🟢 Low      | Batch update                      |
| 3        | Minor updates    | 🟡 Medium   | One at a time, test               |
| 4        | Major updates    | 🔴 High     | Separate branch, review changelog |

---

## 🔒 SECURITY WORKFLOW

| Severity | Response Time | Action               |
| -------- | ------------- | -------------------- |
| Critical | Immediately   | Update, deploy       |
| High     | Within 24h    | Update, test, deploy |
| Medium   | Within 1 week | Schedule update      |
| Low      | Next cycle    | Track                |

---

## 🤖 AUTOMATION

| Tool           | Purpose        | Config File              |
| -------------- | -------------- | ------------------------ |
| **Dependabot** | GitHub native  | `.github/dependabot.yml` |
| **Renovate**   | Multi-platform | `renovate.json`          |
| **Socket**     | Supply chain   | `.socket.yml`            |

> Best practice: Auto-merge patches, review minor, block major

---

## ✅ UPGRADE CHECKLIST

- Before: Tests passing, clean git, backup lockfile
- During: Security first, check changelog, one at a time for major
- After: Tests pass, build OK, no new vulns, commit w/ lockfile

---

## 📊 REPORT FORMAT

```
📦 Upgrade Report

✅ Updated: 11 packages
  - 3 security patches (critical)
  - 5 bug fix patches
  - 3 minor updates

⚠️ Skipped: 2 major updates (require review)
  - react 18 → 19 (breaking: new JSX transform)
  - prisma 4 → 5 (breaking: client generation)

Tests: ✅ 42/42 | Build: ✅ Pass | Lint: ✅ 0 issues
```
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

