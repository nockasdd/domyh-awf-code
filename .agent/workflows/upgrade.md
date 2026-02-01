---
name: upgrade
trigger: ["/upgrade", "update deps", "dependencies"]
persona: developer
description: "📦 Update dependencies: check outdated, apply safe updates, review breaking changes"
---

# 📦 /upgrade — Dependency Upgrade Pro v3.0

> Safe Dependency Management
> 📚 30+ Languages • Security First • Staged Rollout

---

## 🔄 UPGRADE FLOW

```
User: /upgrade [options]
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 1: AUDIT                          │
│ ▸ List all dependencies                 │
│ ▸ Check for outdated                    │
│ ▸ Scan for vulnerabilities              │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 2: ANALYZE                        │
│ ▸ Categorize by risk                    │
│ ▸ Check changelogs                      │
│ ▸ Identify breaking changes             │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 3: UPDATE                         │
│ ▸ Apply patches first                   │
│ ▸ Then minor updates                    │
│ ⛔ STOP → Confirm major updates         │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 4: VERIFY                         │
│ ▸ Run tests                             │
│ ▸ Check build                           │
│ ▸ Validate functionality                │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 5: COMMIT                         │
│ ▸ Commit changes                        │
│ ▸ Document updates                      │
└─────────────────────────────────────────┘
```

---

## 🎯 COMMANDS

| Command             | Description     | Scope     |
| ------------------- | --------------- | --------- |
| `/upgrade`          | Check outdated  | List only |
| `/upgrade patch`    | Apply patches   | Safe      |
| `/upgrade minor`    | Apply minor     | Review    |
| `/upgrade major`    | Apply major     | Careful!  |
| `/upgrade [pkg]`    | Update specific | Targeted  |
| `/upgrade security` | Security only   | Critical  |
| `/upgrade all`      | Update all      | Full      |

---

## 🔧 TOOLS BY LANGUAGE

```yaml
# ═══════════════════════════════════════════════════════════════
# DEPENDENCY MANAGEMENT TOOLS
# ═══════════════════════════════════════════════════════════════

tools:
  go:
    check: "go list -m -u all"
    update: "go get -u"
    update_specific: "go get package@version"
    security: "govulncheck ./..."
    tidy: "go mod tidy"

  typescript:
    check: "npm outdated"
    update: "npm update"
    update_major: "npx npm-check-updates -u"
    security: "npm audit"
    fix: "npm audit fix"
    tools: [dependabot, renovate]

  python:
    check: "pip list --outdated"
    update: "pip install -U package"
    security: "pip-audit"
    tools: [dependabot, safety]
    lock: "pip-compile"

  rust:
    check: "cargo outdated"
    update: "cargo update"
    security: "cargo audit"
    upgrade: "cargo upgrade"

  java:
    check: "mvn versions:display-dependency-updates"
    update: "mvn versions:use-latest-releases"
    security: "mvn dependency-check:check"

  csharp:
    check: "dotnet list package --outdated"
    update: "dotnet add package [name] --version [ver]"
    security: "dotnet list package --vulnerable"

  ruby:
    check: "bundle outdated"
    update: "bundle update"
    security: "bundle audit"

  php:
    check: "composer outdated"
    update: "composer update"
    security: "composer audit"
```

---

## 📊 UPGRADE REPORT

```markdown
📦 DEPENDENCY UPGRADE REPORT

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Project: my-api
Total Dependencies: 145 (42 direct, 103 indirect)

## Summary

| Status             | Count | Action      |
| ------------------ | ----- | ----------- |
| ✅ Up to date      | 138   | None        |
| 🟡 Patch available | 4     | Auto-update |
| 🟠 Minor available | 2     | Review      |
| 🔴 Major available | 1     | Manual      |
| ⚠️ Vulnerable      | 0     | -           |

## Patch Updates (Safe to apply)

| Package            | Current | Latest | Type  |
| ------------------ | ------- | ------ | ----- |
| `gin-gonic/gin`    | 1.9.0   | 1.9.1  | patch |
| `lib/pq`           | 1.10.7  | 1.10.9 | patch |
| `stretchr/testify` | 1.8.2   | 1.8.4  | patch |
| `go-redis/redis`   | 9.0.3   | 9.0.5  | patch |

✅ Auto-applying patches...

## Minor Updates (Review recommended)

| Package       | Current | Latest | Changes           |
| ------------- | ------- | ------ | ----------------- |
| `uber-go/zap` | 1.24.0  | 1.26.0 | [changelog](link) |
| `spf13/viper` | 1.15.0  | 1.18.0 | [changelog](link) |

### uber-go/zap 1.24.0 → 1.26.0

Notable changes:

- New: `sugared.Infow()` performance improvement
- Fix: Race condition in concurrent logging
- No breaking changes

⛔ Apply minor updates? [y/n]

## Major Updates (Breaking changes possible)

| Package        | Current | Latest | Breaking |
| -------------- | ------- | ------ | -------- |
| `gorm.io/gorm` | 1.x     | 2.x    | Yes      |

### gorm.io/gorm 1.x → 2.x

⚠️ BREAKING CHANGES:

- Model definition syntax changed
- Callback API redesigned
- Association handling updated

Migration guide: [docs link]

⛔ STOP: Major update requires manual review

## Security Scan

✅ No known vulnerabilities found

## Post-Update Verification

| Check | Status     |
| ----- | ---------- |
| Build | ✅ Pass    |
| Tests | ✅ 145/145 |
| Lint  | ✅ Clean   |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 📋 SAFETY LEVELS

```yaml
safety_levels:
  patch:
    semver: "x.y.Z"
    risk: "Low"
    action: "Auto-update"
    description: "Bug fixes, no API changes"

  minor:
    semver: "x.Y.z"
    risk: "Medium"
    action: "Review changelog"
    description: "New features, backward compatible"

  major:
    semver: "X.y.z"
    risk: "High"
    action: "Manual review, test thoroughly"
    description: "Breaking changes possible"

update_order:
  1: "Security patches (critical)"
  2: "Bug fix patches"
  3: "Minor updates (one at a time)"
  4: "Major updates (separate branch)"
```

---

## 🔒 SECURITY WORKFLOW

```yaml
security:
  scan_commands:
    go: "govulncheck ./..."
    node: "npm audit"
    python: "pip-audit"
    rust: "cargo audit"

  severity_levels:
    critical: "Update immediately"
    high: "Update within 24h"
    medium: "Update within 1 week"
    low: "Update in next cycle"

  actions:
    1_identify: "Scan for vulnerabilities"
    2_assess: "Check if exploitable"
    3_update: "Apply security patch"
    4_verify: "Run tests"
    5_deploy: "Ship to production"
```

---

## 🔧 AUTOMATION

```yaml
automation:
  dependabot:
    config: |
      version: 2
      updates:
        - package-ecosystem: "npm"
          directory: "/"
          schedule:
            interval: "weekly"
          groups:
            production:
              patterns: ["*"]
              exclude-patterns: ["dev-*"]

  renovate:
    config: |
      {
        "extends": ["config:base"],
        "automerge": true,
        "automergeType": "branch",
        "packageRules": [
          {
            "matchUpdateTypes": ["patch"],
            "automerge": true
          }
        ]
      }
```

---

## 🔒 LOCKFILE MANAGEMENT

```yaml
lockfile_handling:
  backup:
    # Always backup before upgrade
    commands:
      npm: "cp package-lock.json package-lock.json.bak"
      yarn: "cp yarn.lock yarn.lock.bak"
      pnpm: "cp pnpm-lock.yaml pnpm-lock.yaml.bak"
      go: "cp go.sum go.sum.bak"
      rust: "cp Cargo.lock Cargo.lock.bak"
      python: "cp requirements.txt requirements.txt.bak"

  restore:
    # Rollback if tests fail
    trigger: "tests fail after upgrade"
    action: "restore from .bak file"

  verify:
    # Ensure lockfile is committed
    check: "git diff --name-only | grep lock"
    action: "include lockfile in commit"
```

---

## 🛡️ SECURITY-FIRST UPGRADE

```yaml
security_priority:
  order:
    1. vulnerable_critical  # Fix immediately
    2. vulnerable_high      # Fix within 24h
    3. vulnerable_medium    # Fix within 1 week
    4. patch_updates        # Auto-apply
    5. minor_updates        # Review
    6. major_updates        # Manual

  commands:
    npm: "npm audit fix --force"
    go: "govulncheck ./... && go get -u [affected]"
    rust: "cargo audit fix"
    python: "pip-audit --fix"
```

---

## ✅ UPGRADE CHECKLIST

```markdown
📋 UPGRADE CHECKLIST

Before:

- [ ] All tests passing
- [ ] Clean git status
- [ ] Backup lockfile (cp _.lock _.lock.bak)
- [ ] Run security scan

During:

- [ ] Security patches first
- [ ] Check changelog
- [ ] Review breaking changes
- [ ] Update one at a time

After:

- [ ] Tests pass
- [ ] Build succeeds
- [ ] No new lint errors
- [ ] No new vulnerabilities
- [ ] Functionality verified
- [ ] Commit with lockfile
```

---

## ⚙️ TOKEN OPTIMIZATION

```yaml
token_saving:
  - Focus on vulnerable first (security-first)
  - Batch patch updates
  - Use automated tools (Dependabot/Renovate)
  - Cache audit results
```

---

_DOMYH Awesome Code v4.3 • Upgrade Pro v3.1 • Security-First Updates_
