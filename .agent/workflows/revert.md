---
name: revert
trigger: ["/revert", "undo", "hoàn tác"]
persona: developer
description: "⏪ Revert changes: git rollback, deployment rollback, database rollback"
---

# ⏪ /revert — Revert Pro v3.1

> Safe Reversal of Changes
> 📚 Git • Deployment • Database

---

## 🔄 REVERT FLOW

```
User: /revert [target]
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 1: IDENTIFY                       │
│ ▸ What needs to be reverted?            │
│ ▸ Git / Deploy / Database?              │
│ ▸ Find target state                     │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 2: ANALYZE                        │
│ ▸ Impact assessment                     │
│ ▸ Data loss risks                       │
│ ▸ Dependencies affected                 │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 3: BACKUP                         │
│ ▸ Create backup of current state        │
│ ⛔ STOP → Confirm revert                │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 4: EXECUTE                        │
│ ▸ Perform rollback                      │
│ ▸ Verify success                        │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 5: VERIFY                         │
│ ▸ Test functionality                    │
│ ▸ Confirm state restored                │
└─────────────────────────────────────────┘
```

---

## 🎯 COMMANDS

| Command          | Description         |
| ---------------- | ------------------- |
| `/revert`        | Interactive revert  |
| `/revert git`    | Git rollback        |
| `/revert deploy` | Deployment rollback |
| `/revert db`     | Database rollback   |
| `/revert last`   | Revert last change  |

---

## 🔧 GIT ROLLBACK

```yaml
git_revert:
  # ═══════════════════════════════════════════════════════════════
  # UNDO SCENARIOS
  # ═══════════════════════════════════════════════════════════════

  undo_last_commit:
    keep_changes: "git reset --soft HEAD~1"
    discard: "git reset --hard HEAD~1"

  undo_multiple_commits:
    command: "git reset --hard HEAD~{n}"
    example: "git reset --hard HEAD~3"

  revert_specific_commit:
    command: "git revert {commit_hash}"
    note: "Creates new commit that undoes changes"

  undo_uncommitted:
    single_file: "git checkout -- {file}"
    all_files: "git checkout -- ."

  undo_staged:
    unstage: "git reset HEAD {file}"
    unstage_all: "git reset HEAD"

  recover_deleted_branch:
    find: "git reflog"
    restore: "git checkout -b {branch} {commit_hash}"
```

---

## 🚀 DEPLOYMENT ROLLBACK

```yaml
deployment_rollback:
  vercel:
    list: "vercel ls"
    rollback: "vercel rollback {deployment_url}"

  docker:
    list: "docker images"
    rollback: "docker-compose down && docker-compose up -d {previous_tag}"

  kubernetes:
    list: "kubectl rollout history deployment/{name}"
    rollback: "kubectl rollout undo deployment/{name}"
    rollback_to: "kubectl rollout undo deployment/{name} --to-revision={n}"

  aws:
    ecs_list: "aws ecs describe-services"
    ecs_rollback: "aws ecs update-service --force-new-deployment"

  heroku:
    list: "heroku releases"
    rollback: "heroku rollback v{n}"
```

---

## 🗄️ DATABASE ROLLBACK

```yaml
database_rollback:
  # ═══════════════════════════════════════════════════════════════
  # MIGRATION TOOLS
  # ═══════════════════════════════════════════════════════════════

  atlas:
    down: "atlas migrate down --env dev"
    to_version: "atlas migrate down --to {version}"

  prisma:
    reset: "npx prisma migrate reset"
    rollback: "Manual - apply reverse migration"

  goose:
    down: "goose down"
    down_to: "goose down-to {version}"

  flyway:
    undo: "flyway undo"

  alembic:
    downgrade: "alembic downgrade -1"
    downgrade_to: "alembic downgrade {revision}"

  rails:
    rollback: "rails db:rollback"
    rollback_n: "rails db:rollback STEP=3"
```

---

## 📊 REVERT REPORT

```markdown
⏪ REVERT REPORT

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Type: Git Rollback
Target: HEAD~2 (abc123)

## Before Revert

Current: def456 "Add user authentication"
Target: abc123 "Fix payment integration"

Commits to undo:

1. def456 - Add user authentication
2. 789xyz - Update dependencies

## Impact Analysis

| Impact         | Assessment |
| -------------- | ---------- |
| Files affected | 15         |
| Lines removed  | +320       |
| Dependencies   | 2 packages |

⚠️ Warning: This will remove authentication feature

## Backup Created

Backup branch: backup/pre-revert-2026-01-31

⛔ CONFIRM REVERT? [y/n]

## After Revert

✅ Successfully reverted to abc123
✅ Backup available at: backup/pre-revert-2026-01-31

Recovery command: git checkout backup/pre-revert-2026-01-31

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🚩 FEATURE FLAGS ROLLBACK

```yaml
feature_flags:
  description: "Toggle features without code deploy"

  providers:
    - LaunchDarkly
    - Flagsmith
    - Unleash
    - "Custom: process.env.FEATURE_X"

  rollback_pattern: |
    // Instant rollback via flag toggle
    if (isFeatureEnabled("new_checkout")) {
      return newCheckout();
    }
    return legacyCheckout();

  benefits:
    time: "< 1 minute rollback"
    risk: "Zero code change needed"
    testing: "A/B test before full rollout"
```

---

## 🐤 CANARY ROLLBACK

```yaml
canary_rollback:
  description: "Gradual rollout with quick revert"

  kubernetes:
    check_canary: "kubectl get pods -l version=canary"
    revert_traffic: |
      kubectl patch vs/app --patch '{
        "spec": {"http": [{"route": [
          {"destination": {"host": "app", "subset": "stable"}, "weight": 100}
        ]}]}
      }'
    delete_canary: "kubectl delete deployment/app-canary"

  argo_rollouts:
    abort: "kubectl argo rollouts abort rollout-name"
    undo: "kubectl argo rollouts undo rollout-name"
```

---

## ⚠️ DATABASE ROLLBACK WARNINGS

```yaml
database_warnings:
  ⚠️_critical: |
    Database rollbacks are DESTRUCTIVE.
    Data written after migration WILL BE LOST.

  safe_patterns:
    expand_contract: 1. "Add new columns (don't remove old)"
      2. "Copy data to new structure"
      3. "Update services to use new"
      4. "Deprecate old columns later"

    reversible_only:
      ✅: "Add column, add index, add table"
      ❌: "Drop column, rename, change type"

  backup_commands:
    postgres: "pg_dump -Fc db > backup.dump"
    mysql: "mysqldump db > backup.sql"
    mongodb: "mongodump --db dbname"
```

---

## 🏷️ IMMUTABLE VERSIONING

```yaml
immutable_tags:
  ❌_avoid:
    - ":latest"
    - ":stable"
    - "Any mutable tag"

  ✅_use:
    semver: "v1.2.3"
    date_commit: "2026-02-01-abc123"
    git_sha: "sha-abc123def"
    digest: "sha256:abc..."

  rollback_example: |
    # docker-compose.yml
    services:
      app:
        image: myapp:v1.2.2  # Not :latest

    # Rollback command
    docker-compose down && docker-compose up -d
```

---

## ⚠️ SAFETY RULES

```yaml
safety:
  1_always_backup:
    rule: "Create backup before any revert"
    command: "git branch backup/pre-revert-$(date +%Y%m%d)"

  2_confirm_destructive:
    rule: "Require confirmation for --hard resets"

  3_document_reason:
    rule: "Log why revert was needed"

  4_notify_team:
    rule: "Alert team if production rollback"

  5_prefer_revert:
    rule: "Use 'git revert' over 'git reset' for shared branches"
```

---

## ⚙️ TOKEN OPTIMIZATION

```yaml
token_saving:
  - Focus on target state
  - Auto-detect revert type
  - Concise impact summary
  - Feature flags first, code revert last
```

---

_DOMYH Awesome Code v5.5 • Revert Pro v3.1 • Safe Rollback + Feature Flags_
