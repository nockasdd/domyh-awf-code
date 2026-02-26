---
description: "🩺 System doctor: environment diagnostics, runtime checks, config validation, dependency health"
skills: { required: [], contextual: [auto] }
success_criteria: "All checks reported with fix recommendations"
---

# 🩺 /doctor — System Doctor Pro

> Environment Diagnostics & Fix Recommendations
> 📚 Runtime Check • Config Validation • Dependency Health • Auto-Fix
> ℹ️ Complements `/status` (project health); `/doctor` focuses on environment readiness

---

## DOCTOR FLOW

1. **SCAN** — `hsa_declare_intent("environment diagnostics")`, detect environment via HSA (`hsa_detect_environment`), identify OS, shell, runtimes, package managers. Show: `[Step 1/4] Scanning environment...`
2. **VALIDATE** — Check runtime versions, required tools, config files, permissions. Show: `[Step 2/4] Validating 12 checks...`
3. **DIAGNOSE** — Identify issues, classify severity (🔴 Critical / 🟡 Warning / 🟢 OK). Show: `[Step 3/4] Found 2 issues`
4. **PRESCRIBE** — Generate fix commands, link docs, offer auto-fix for safe items. Show: `[Step 4/5] Generating prescriptions...`
5. **SYNC** — `hsa_check_changes` to update index after auto-fix config changes

---

## COMMANDS

| Command             | Description                             |
| ------------------- | --------------------------------------- |
| `/doctor`           | Full environment diagnostic             |
| `/doctor quick`     | Brief summary (🔴 only)                 |
| `/doctor fix`       | Auto-fix safe issues                    |
| `/doctor [runtime]` | Check specific runtime (node/go/python) |

---

## 📋 DIAGNOSTIC CHECKS

### Runtime Checks

| Check   | Command            | 🟢 Good | 🟡 Warning | 🔴 Critical      |
| ------- | ------------------ | ------- | ---------- | ---------------- |
| Node.js | `node -v`          | ≥ 18.x  | 16.x       | < 16 / missing   |
| npm     | `npm -v`           | ≥ 9.x   | 7-8.x      | < 7 / missing    |
| Go      | `go version`       | ≥ 1.22  | 1.20-1.21  | < 1.20 / missing |
| Python  | `python --version` | ≥ 3.11  | 3.9-3.10   | < 3.9 / missing  |
| Git     | `git --version`    | ≥ 2.40  | 2.30-2.39  | < 2.30 / missing |
| Docker  | `docker --version` | ≥ 24.x  | 20-23.x    | < 20 / missing   |

### Config Validation

| Check                  | What                            | Auto-fix    |
| ---------------------- | ------------------------------- | ----------- |
| `.env` exists          | Required env vars present       | ⚠️ Template |
| `tsconfig.json`        | Strict mode enabled             | ✅ Yes      |
| `package.json` engines | Node version constraint         | ✅ Yes      |
| `.gitignore`           | Sensitive files excluded        | ✅ Yes      |
| Lock file              | Consistent with package manager | ❌ No       |

### Dependency Health

| Check              | Command                         | Action            |
| ------------------ | ------------------------------- | ----------------- |
| Outdated deps      | `npm outdated`                  | Show update plan  |
| Security vulns     | `npm audit`                     | Show fix commands |
| Peer dep conflicts | `npm ls --all`                  | Show resolution   |
| Unused deps        | Analyze imports vs package.json | Suggest removal   |

### HSA Engine Health

| Check       | Tool                   | Expected         |
| ----------- | ---------------------- | ---------------- |
| HSA running | `hsa_status`           | Engine healthy   |
| Index built | `hsa_status` (verbose) | BM25 + Vector OK |
| Cache warm  | `hsa_status` (verbose) | Hit rate > 50%   |

---

## 📊 REPORT FORMAT

```
🩺 System Doctor Report

Environment: Windows 11 | PowerShell 7.5 | VS Code
Project: my-app (TypeScript + React)

Runtime         Version    Status    Fix
──────────────────────────────────────────
Node.js         22.4.0     🟢 OK
npm             10.8.2     🟢 OK
Git             2.45.1     🟢 OK
Docker          —          🟡 Not installed

Config          Status     Fix
──────────────────────────────────
.env            🟢 OK
tsconfig.json   🟡 strict: false   → /doctor fix
.gitignore      🟢 OK

Dependencies    Status     Action
──────────────────────────────────
Outdated        🟡 3 minor → npm update
Security        🟢 0 vulns
Unused          🟡 2 found → npm uninstall lodash dayjs

HSA Engine      Status
──────────────────────
Engine          🟢 Healthy (uptime: 2h)
Index           🟢 1,234 docs indexed
Cache           🟡 Hit rate: 45%

Score: 85/100 (🟢 Good)
Quick fix: `/doctor fix` (2 auto-fixable issues)
```

---

## ⛔ SAFETY

- Auto-fix only applies to safe items (config formatting, gitignore)
- Confirm with user before installing system dependencies
- Create .env.example templates instead of modifying .env files directly
- Show exact commands before executing

---

---

## REFLECTION CHECKPOINT

⛔ **MANDATORY** — Execute before completing this workflow (SESSION_005):

1. **VERIFY** — Does output meet success_criteria (see YAML frontmatter)?
2. **PERSIST** — Update session memory:
   - Append task summary to `memory/session.md` (per SESSION_005 format)
   - If key decision made → append to `memory/decisions.md`
3. **SNAPSHOT** — If this is the last task in session:
   - Update `memory/CONTEXT_SNAPSHOT.md` (Recent Changes, Status, Decisions)
4. **ANCHOR** (if HSA available):
   - `hsa_track_progress(level: "action", label: "[workflow] completed", status: "completed")`
   - `hsa_save_anchor(content: "[SESSION] Done: [summary]. Files: [list].", category: "context")`

