---
description: "🗃️ Database migrations: create, run, rollback, and seed with safety checks"
skills: { required: [database], contextual: [auto] }
success_criteria: "migrations applied successfully, schema validated, data integrity verified"
---

# 🗃️ /migrate — Migrate Pro

> Safe Schema Evolution & Data Migrations
> 📚 25+ Tools • Zero-Downtime • Rollback Safety

---

## MIGRATION FLOW

1. **DETECT** (Auto) — `hsa_declare_intent("migration: {operation}")`, detect stack via HSA (`hsa_detect_stack`), load DB context (`hsa_get_context`), find migration tool, check pending
2. **VALIDATE** — Check migration syntax, detect breaking changes, verify rollback exists → ⛔ STOP if destructive
3. **BACKUP** — Create backup (required for production), snapshot schema, log attempt
4. **EXECUTE** — Run migrations in transaction, apply changes, update version table
5. **VERIFY** — Validate schema, run smoke tests, check data integrity
6. **SYNC** — `hsa_check_changes` to update index after schema changes

---

## COMMANDS

| Command               | Description           | Risk        |
| --------------------- | --------------------- | ----------- |
| `/migrate`            | Show status & pending | 🟢 Safe     |
| `/migrate up`         | Run all pending       | 🟡 Medium   |
| `/migrate up 1`       | Run next migration    | 🟢 Safe     |
| `/migrate down`       | Rollback last         | 🟠 High     |
| `/migrate down 3`     | Rollback N steps      | 🔴 Critical |
| `/migrate new [name]` | Create migration      | 🟢 Safe     |
| `/migrate seed`       | Run seeders           | 🟡 Medium   |
| `/migrate reset`      | Rollback all + up     | 🔴 Critical |
| `/migrate fresh`      | Drop all + migrate    | 🔴 Critical |
| `/migrate diff`       | Show schema diff      | 🟢 Safe     |

---

## MIGRATION TOOLS

### TypeScript / JavaScript

```yaml
# tool: databases | create | up | down | status
prisma: PG,MySQL,SQLite,Mongo,MSSQL | prisma migrate dev --name {n} | prisma migrate deploy | prisma migrate resolve --rolled-back | prisma migrate status
drizzle: PG,MySQL,SQLite | drizzle-kit generate | drizzle-kit migrate | — | drizzle-kit push
knex: PG,MySQL,SQLite,Oracle | knex migrate:make {n} | knex migrate:latest | knex migrate:rollback | knex migrate:status
typeorm: PG,MySQL,SQLite,Oracle,MSSQL | typeorm migration:create | typeorm migration:run | typeorm migration:revert | —
sequelize: PG,MySQL,SQLite,MSSQL | sequelize migration:generate --name {n} | sequelize db:migrate | sequelize db:migrate:undo | —
```

### Python

```yaml
alembic: PG,MySQL,SQLite,Oracle | alembic revision --autogenerate -m "{msg}" | alembic upgrade head | alembic downgrade -1 | alembic current
django: PG,MySQL,SQLite,Oracle | manage.py makemigrations | manage.py migrate | manage.py migrate app {num} | manage.py showmigrations
tortoise: PG,MySQL,SQLite | aerich migrate --name {n} | aerich upgrade | aerich downgrade | —
```

### Go

```yaml
goose: PG,MySQL,SQLite,MSSQL | goose create {n} sql | goose up | goose down | goose status
migrate: PG,MySQL,SQLite,Mongo | migrate create -ext sql -dir migrations {n} | migrate up | migrate down 1 | —
atlas: PG,MySQL,SQLite,MSSQL | — | atlas schema apply | — | atlas schema inspect
ent: PG,MySQL,SQLite | go generate ./ent | atlas migrate apply | — | —
```

### Java / JVM

```yaml
flyway: PG,MySQL,Oracle,MSSQL,DB2 | — | flyway migrate | flyway undo (Teams) | flyway info
liquibase: PG,MySQL,Oracle,MSSQL,DB2 | — | liquibase update | liquibase rollback {tag} | liquibase status
```

### Ruby / PHP / Rust / .NET

```yaml
rails: PG,MySQL,SQLite | rails g migration {n} | rails db:migrate | rails db:rollback STEP=1 | rails db:migrate:status
laravel: PG,MySQL,SQLite,MSSQL | artisan make:migration {n} | artisan migrate | artisan migrate:rollback | artisan migrate:status
diesel: PG,MySQL,SQLite | diesel migration generate {n} | diesel migration run | diesel migration revert | —
sqlx: PG,MySQL,SQLite | sqlx migrate add {n} | sqlx migrate run | sqlx migrate revert | —
ef_core: PG,MySQL,SQLite,MSSQL | dotnet ef migrations add {n} | dotnet ef database update | dotnet ef database update {prev} | —
```

---

## ZERO-DOWNTIME STRATEGIES

| Pattern                | Description                                       | Use When                  |
| ---------------------- | ------------------------------------------------- | ------------------------- |
| **Expand-Contract** ⭐ | Add new → Migrate data → Remove old               | Production schema changes |
| **Blue-Green DB**      | Two identical DBs, switch traffic                 | Critical migrations       |
| **Rolling**            | Incremental with replication (gh-ost, pg_repack)  | Large tables, can't lock  |
| **CDC**                | Capture changes in real-time (Debezium, pgoutput) | Minimal cutover downtime  |

---

## ROLLBACK SAFETY MATRIX

| Change Type   | Rollback       | Risk     |
| ------------- | -------------- | -------- |
| Add column    | ✅ Safe        | Low      |
| Add index     | ✅ Safe        | Low      |
| Rename column | ⚠️ Risky       | High     |
| Drop column   | ❌ Destructive | Critical |
| Drop table    | ❌ Destructive | Critical |

> ⚠️ Data written after migration will be LOST on rollback. Always use expand-contract in production.

---

## BACKUP COMMANDS

```yaml
postgresql: pg_dump -Fc {db} > backup.dump | pg_restore -d {db} backup.dump
mysql: mysqldump {db} > backup.sql | mysql {db} < backup.sql
mongodb: mongodump --db {db} | mongorestore --db {db} dump/{db}
```

---

## SEEDING

```yaml
# tool: run command | config
prisma: npx prisma db seed | prisma/seed.ts
rails: rails db:seed | db/seeds.rb
laravel: php artisan db:seed | --class=UserSeeder
django: manage.py loaddata fixtures.json

# Seed types: dev (admin+test data) | staging (admin+anonymized) | prod (system roles only)
```
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

