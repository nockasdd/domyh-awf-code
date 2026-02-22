---
description: "⏪ Revert changes: git rollback, deployment rollback, database rollback"
skills: { required: [], contextual: [ci-cd] }
success_criteria: "Changes reverted, backup created, tests passing"
---

# ⏪ /revert — Revert Pro

> Safe Reversal of Changes
> 📚 Git • Deploy • Database • Feature Flags

---

## REVERT FLOW

1. **DETECT** — What to revert, how far back
2. **PLAN** — Impact assessment (files, deps, data), create backup → ⛔ STOP for user confirmation
3. **EXECUTE** — Execute reversal
4. **VERIFY** — Confirm reversal applied correctly, run tests
5. **SYNC** — `hsa_check_changes` to update index after reversal

---

## COMMANDS

| Command          | Description         |
| ---------------- | ------------------- |
| `/revert`        | Interactive revert  |
| `/revert git`    | Git rollback        |
| `/revert deploy` | Deployment rollback |
| `/revert db`     | Database rollback   |
| `/revert last`   | Revert last change  |

---

## 🔧 GIT ROLLBACK

| Scenario                        | Command                                          |
| ------------------------------- | ------------------------------------------------ |
| Undo last commit (keep changes) | `git reset --soft HEAD~1`                        |
| Undo last commit (discard)      | `git reset --hard HEAD~1`                        |
| Revert specific commit          | `git revert {hash}`                              |
| Unstage file                    | `git reset HEAD {file}`                          |
| Discard file changes            | `git checkout -- {file}`                         |
| Recover deleted branch          | `git reflog` → `git checkout -b {branch} {hash}` |

---

## 🚀 DEPLOYMENT ROLLBACK

| Platform   | List                        | Rollback                                        |
| ---------- | --------------------------- | ----------------------------------------------- |
| Vercel     | `vercel ls`                 | `vercel rollback {url}`                         |
| Docker     | `docker images`             | `docker-compose up -d {prev_tag}`               |
| Kubernetes | `kubectl rollout history`   | `kubectl rollout undo deployment/{name}`        |
| AWS ECS    | `aws ecs describe-services` | `aws ecs update-service --force-new-deployment` |
| Heroku     | `heroku releases`           | `heroku rollback v{n}`                          |

---

## 🗄️ DATABASE ROLLBACK

| Tool      | Rollback Command                                  |
| --------- | ------------------------------------------------- |
| Prisma    | `npx prisma migrate resolve --rolled-back {name}` |
| TypeORM   | `npx typeorm migration:revert`                    |
| Knex      | `npx knex migrate:rollback`                       |
| Alembic   | `alembic downgrade -1`                            |
| Django    | `python manage.py migrate {app} {previous}`       |
| goose     | `goose -dir migrations down`                      |
| Flyway    | `flyway undo`                                     |
| Liquibase | `liquibase rollback-count 1`                      |

### Safety Rules

- Backup before reverting
- Forward-only migrations preferred (add new, don't drop)
- Require backup before: drop column, rename column, change type

---

## 🏴 FEATURE FLAGS (Prefer Over Code Revert)

| Strategy     | Description                   | Rollback Time |
| ------------ | ----------------------------- | ------------- |
| Feature flag | Toggle feature off            | < 1 minute    |
| Canary       | Gradual rollout, quick revert | < 5 minutes   |
| Code revert  | Git revert + redeploy         | 10+ minutes   |

> **Best practice**: Feature flags first → code revert last resort

---

## 🏷️ IMMUTABLE VERSIONING

| ❌ Avoid     | ✅ Use                          |
| ------------ | ------------------------------- |
| `:latest`    | `v1.2.3` (semver)               |
| `:stable`    | `2026-02-01-abc123` (date+hash) |
| Mutable tags | `sha-abc123def` (git SHA)       |
---

## REFLECTION CHECKPOINT

> Before saving session, verify: backup created before revert? Revert verified correct? Tests passing after rollback?

---

## SESSION SAVE

After completing this workflow:
1. Update `memory/CONTEXT_SNAPSHOT.md` - what changed, current status
2. Append summary to `memory/session.md`
