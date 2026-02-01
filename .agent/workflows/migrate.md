---
name: migrate
trigger: ["/migrate", "migration", "db migrate", "di chuyển"]
persona: developer
description: "🗃️ Database migrations: create, run, rollback, and seed with safety checks"
---

# 🗃️ /migrate — Database Migration Pro v3.0

> Safe Schema Evolution & Data Migrations
> 📚 20+ Tools • Zero-Downtime • Rollback Safety

---

## 🔄 MIGRATION FLOW

```
User: /migrate [command]
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 1: DETECT (Auto)                 │
│ ▸ Detect database type                  │
│ ▸ Find migration tool                   │
│ ▸ Check pending migrations              │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 2: VALIDATE                       │
│ ▸ Check migration syntax                │
│ ▸ Detect breaking changes               │
│ ▸ Verify rollback exists                │
│ ⛔ STOP → Confirm if destructive        │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 3: BACKUP                         │
│ ▸ Create backup (production)            │
│ ▸ Snapshot current schema               │
│ ▸ Log migration attempt                 │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 4: EXECUTE                        │
│ ▸ Run migrations                        │
│ ▸ Apply in transaction (if supported)   │
│ ▸ Update version table                  │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 5: VERIFY                         │
│ ▸ Validate schema                       │
│ ▸ Run smoke tests                       │
│ ▸ Check data integrity                  │
└─────────────────────────────────────────┘
```

---

## 🎯 COMMANDS

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

## 📋 PHASE 1: DETECT

### Migration Status Report:

```
🗃️ MIGRATION STATUS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Database: PostgreSQL 15
Tool: Prisma Migrate
Migration Dir: prisma/migrations/

Applied Migrations: 15
├── 20240101_init_schema
├── 20240115_add_users
├── 20240201_add_orders
└── ... (12 more)

Pending Migrations: 2
├── 20240301_add_payments ⏳
└── 20240302_add_webhooks ⏳

Schema Drift: ⚠️ Detected
└── Column "status" added directly (not in migrations)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 NEXT STEPS:
1️⃣ Review pending migrations
2️⃣ Fix schema drift
3️⃣ Run: /migrate up

Enter number:
```

---

## 🌐 MIGRATION TOOLS (20+ Databases)

### ORM-Based Tools

```yaml
# ═══════════════════════════════════════════════════════════════
# TYPESCRIPT / JAVASCRIPT
# ═══════════════════════════════════════════════════════════════

prisma:
  databases: [PostgreSQL, MySQL, SQLite, MongoDB, SQL Server]
  commands:
    status: "npx prisma migrate status"
    create: "npx prisma migrate dev --name {name}"
    apply: "npx prisma migrate deploy"
    reset: "npx prisma migrate reset"
    diff: "npx prisma migrate diff"
  features:
    - Schema as code (schema.prisma)
    - Auto-generated SQL
    - Shadow database for safety
    - Baseline for existing DBs

drizzle:
  databases: [PostgreSQL, MySQL, SQLite]
  commands:
    create: "npx drizzle-kit generate"
    apply: "npx drizzle-kit migrate"
    push: "npx drizzle-kit push"
  features:
    - TypeScript-first
    - SQL-like syntax
    - No code generation

knex:
  databases: [PostgreSQL, MySQL, SQLite, Oracle]
  commands:
    create: "npx knex migrate:make {name}"
    up: "npx knex migrate:latest"
    down: "npx knex migrate:rollback"
    status: "npx knex migrate:status"

typeorm:
  databases: [PostgreSQL, MySQL, SQLite, Oracle, SQL Server]
  commands:
    create: "npx typeorm migration:create"
    generate: "npx typeorm migration:generate"
    run: "npx typeorm migration:run"
    revert: "npx typeorm migration:revert"

sequelize:
  databases: [PostgreSQL, MySQL, SQLite, SQL Server]
  commands:
    create: "npx sequelize-cli migration:generate --name {name}"
    up: "npx sequelize-cli db:migrate"
    down: "npx sequelize-cli db:migrate:undo"

# ═══════════════════════════════════════════════════════════════
# PYTHON
# ═══════════════════════════════════════════════════════════════

alembic:
  orm: SQLAlchemy
  databases: [PostgreSQL, MySQL, SQLite, Oracle]
  commands:
    create: 'alembic revision --autogenerate -m "{message}"'
    up: "alembic upgrade head"
    down: "alembic downgrade -1"
    status: "alembic current"
    history: "alembic history"
  features:
    - Autogenerate from models
    - Branching support
    - Offline mode

django:
  databases: [PostgreSQL, MySQL, SQLite, Oracle]
  commands:
    create: "python manage.py makemigrations"
    up: "python manage.py migrate"
    down: "python manage.py migrate app {number}"
    status: "python manage.py showmigrations"
    sql: "python manage.py sqlmigrate app {number}"

tortoise:
  databases: [PostgreSQL, MySQL, SQLite]
  commands:
    create: "aerich migrate --name {name}"
    up: "aerich upgrade"
    down: "aerich downgrade"

# ═══════════════════════════════════════════════════════════════
# GO
# ═══════════════════════════════════════════════════════════════

goose:
  databases: [PostgreSQL, MySQL, SQLite, SQL Server]
  commands:
    create: "goose create {name} sql"
    up: "goose up"
    down: "goose down"
    status: "goose status"
    redo: "goose redo"
  features:
    - SQL or Go migrations
    - Embedded migrations
    - Transaction support

golang_migrate:
  databases: [PostgreSQL, MySQL, SQLite, MongoDB, Cassandra]
  commands:
    create: "migrate create -ext sql -dir migrations {name}"
    up: "migrate -path migrations -database {url} up"
    down: "migrate -path migrations -database {url} down 1"
    force: "migrate -path migrations -database {url} force {version}"

atlas:
  databases: [PostgreSQL, MySQL, SQLite, SQL Server]
  commands:
    diff: "atlas schema diff"
    apply: "atlas schema apply"
    inspect: "atlas schema inspect"
  features:
    - Declarative schema
    - Drift detection
    - CI/CD integration

ent:
  databases: [PostgreSQL, MySQL, SQLite]
  commands:
    create: "go generate ./ent"
    apply: "atlas migrate apply"

# ═══════════════════════════════════════════════════════════════
# JAVA / JVM
# ═══════════════════════════════════════════════════════════════

flyway:
  databases: [PostgreSQL, MySQL, Oracle, SQL Server, DB2]
  commands:
    migrate: "flyway migrate"
    info: "flyway info"
    validate: "flyway validate"
    repair: "flyway repair"
    undo: "flyway undo" # Teams edition
  features:
    - SQL or Java migrations
    - Baseline support
    - CI/CD plugins
    - Callbacks

liquibase:
  databases: [PostgreSQL, MySQL, Oracle, SQL Server, DB2]
  commands:
    update: "liquibase update"
    rollback: "liquibase rollback {tag}"
    status: "liquibase status"
    diff: "liquibase diff"
  features:
    - XML/YAML/JSON/SQL formats
    - Rollback scripts
    - Database comparison

jooq:
  databases: [PostgreSQL, MySQL, Oracle, SQL Server]
  commands:
    generate: "mvn jooq-codegen:generate"

# ═══════════════════════════════════════════════════════════════
# RUBY
# ═══════════════════════════════════════════════════════════════

rails:
  databases: [PostgreSQL, MySQL, SQLite]
  commands:
    create: "rails generate migration {name}"
    up: "rails db:migrate"
    down: "rails db:rollback STEP=1"
    status: "rails db:migrate:status"
    reset: "rails db:reset"
    seed: "rails db:seed"

sequel:
  databases: [PostgreSQL, MySQL, SQLite]
  commands:
    create: "sequel -m migrations -M"

# ═══════════════════════════════════════════════════════════════
# PHP
# ═══════════════════════════════════════════════════════════════

laravel:
  databases: [PostgreSQL, MySQL, SQLite, SQL Server]
  commands:
    create: "php artisan make:migration {name}"
    up: "php artisan migrate"
    down: "php artisan migrate:rollback"
    status: "php artisan migrate:status"
    fresh: "php artisan migrate:fresh"
    seed: "php artisan db:seed"

doctrine:
  databases: [PostgreSQL, MySQL, SQLite, Oracle]
  commands:
    diff: "php bin/console doctrine:migrations:diff"
    migrate: "php bin/console doctrine:migrations:migrate"
    status: "php bin/console doctrine:migrations:status"

# ═══════════════════════════════════════════════════════════════
# RUST
# ═══════════════════════════════════════════════════════════════

diesel:
  databases: [PostgreSQL, MySQL, SQLite]
  commands:
    create: "diesel migration generate {name}"
    run: "diesel migration run"
    revert: "diesel migration revert"
    redo: "diesel migration redo"

sea_orm:
  databases: [PostgreSQL, MySQL, SQLite]
  commands:
    create: "sea-orm-cli migrate generate {name}"
    up: "sea-orm-cli migrate up"
    down: "sea-orm-cli migrate down"

sqlx:
  databases: [PostgreSQL, MySQL, SQLite]
  commands:
    create: "sqlx migrate add {name}"
    run: "sqlx migrate run"
    revert: "sqlx migrate revert"

# ═══════════════════════════════════════════════════════════════
# .NET
# ═══════════════════════════════════════════════════════════════

ef_core:
  databases: [PostgreSQL, MySQL, SQLite, SQL Server]
  commands:
    create: "dotnet ef migrations add {name}"
    up: "dotnet ef database update"
    down: "dotnet ef database update {previous}"
    script: "dotnet ef migrations script"
    remove: "dotnet ef migrations remove"

fluentmigrator:
  databases: [PostgreSQL, MySQL, SQLite, SQL Server, Oracle]
  commands:
    up: "dotnet fm migrate -p postgres -c {connstring}"
    down: "dotnet fm rollback -p postgres"
```

---

## 📋 PHASE 2: VALIDATE

### Breaking Change Detection:

```
⚠️ BREAKING CHANGES DETECTED

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Migration: 20240301_add_payments

Destructive Operations:
├── 🔴 DROP COLUMN: users.legacy_id
├── 🔴 DROP TABLE: temp_orders
└── 🟡 ALTER COLUMN: orders.status (nullable → NOT NULL)

Data Impact:
├── Affected rows: ~50,000
└── Estimated time: 2-3 minutes

Recommendations:
1. Add default value before NOT NULL
2. Backup legacy_id data before drop
3. Verify temp_orders is empty

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⛔ Proceed anyway? (y/n/modify):
```

---

## 📋 PHASE 3: BACKUP

### Backup Strategies:

```yaml
backup_strategies:
  development:
    - Skip backup (fast iteration)
    - Use database snapshots

  staging:
    - Snapshot before migration
    - Keep last 3 backups

  production:
    - Full backup required
    - Point-in-time recovery enabled
    - Backup to separate storage
    - Verify backup before proceed

commands:
  postgresql:
    backup: "pg_dump -Fc {db} > backup.dump"
    restore: "pg_restore -d {db} backup.dump"

  mysql:
    backup: "mysqldump {db} > backup.sql"
    restore: "mysql {db} < backup.sql"

  mongodb:
    backup: "mongodump --db {db}"
    restore: "mongorestore --db {db} dump/{db}"
```

---

## 🔄 ZERO-DOWNTIME STRATEGIES

### Migration Patterns:

```yaml
patterns:
  # ═══════════════════════════════════════════════════════════════
  # EXPAND-CONTRACT (Recommended)
  # ═══════════════════════════════════════════════════════════════

  expand_contract:
    description: "Add new → Migrate data → Remove old"
    steps:
      1_expand: |
        -- Add new column (nullable)
        ALTER TABLE users ADD COLUMN email_new VARCHAR(255);

      2_migrate: |
        -- Copy data
        UPDATE users SET email_new = email;
        -- Deploy app using new column

      3_contract: |
        -- Remove old column (after app deployed)
        ALTER TABLE users DROP COLUMN email;
        ALTER TABLE users RENAME COLUMN email_new TO email;

  # ═══════════════════════════════════════════════════════════════
  # BLUE-GREEN DATABASE
  # ═══════════════════════════════════════════════════════════════

  blue_green:
    description: "Two identical databases, switch traffic"
    steps:
      - Migrate "green" database
      - Validate migration
      - Switch traffic to "green"
      - Keep "blue" for rollback

  # ═══════════════════════════════════════════════════════════════
  # ROLLING MIGRATION
  # ═══════════════════════════════════════════════════════════════

  rolling:
    description: "Incremental migration with replication"
    tools: [pg_logical, gh-ost, pt-online-schema-change]
    use_when: "Large tables, can't lock"

online_schema_change:
  mysql:
    tool: "gh-ost"
    command: |
      gh-ost \
        --host=localhost \
        --database=mydb \
        --table=users \
        --alter="ADD COLUMN new_col VARCHAR(255)" \
        --execute

  postgresql:
    tool: "pg_repack"
    command: "pg_repack -d mydb -t users"
```

---

## 📋 ROLLBACK STRATEGIES

### Rollback Commands by Tool:

```yaml
rollback:
  prisma:
    last: "npx prisma migrate resolve --rolled-back {name}"
    manual: "Apply reverse migration"

  alembic:
    last: "alembic downgrade -1"
    to_version: "alembic downgrade {revision}"

  flyway:
    undo: "flyway undo"  # Teams edition
    manual: "Apply V{N-1}__undo.sql"

  rails:
    last: "rails db:rollback STEP=1"
    to_version: "rails db:migrate VERSION={timestamp}"

  goose:
    last: "goose down"
    to_version: "goose down-to {version}"

rollback_checklist:
  - [ ] Identify failed migration
  - [ ] Check if data was modified
  - [ ] Run rollback command
  - [ ] Verify schema reverted
  - [ ] Restore data if needed
  - [ ] Notify team
```

---

## 🌱 SEEDING

### Seed Commands:

```yaml
seeding:
  prisma:
    run: "npx prisma db seed"
    config: "prisma/seed.ts"

  rails:
    run: "rails db:seed"
    file: "db/seeds.rb"

  laravel:
    run: "php artisan db:seed"
    class: "php artisan db:seed --class=UserSeeder"

  django:
    run: "python manage.py loaddata fixtures.json"

  alembic:
    custom: "alembic -x data=seed upgrade head"

seed_types:
  development:
    - Admin user
    - Test data
    - Sample content

  staging:
    - Admin user
    - Anonymized prod data

  production:
    - System roles only
    - Required lookup data
```

---

## ✅ MIGRATION CHECKLIST

```markdown
⚠️ PRE-MIGRATION CHECKLIST

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Environment: [dev/staging/production]
Migration: {migration_name}

□ Planning
├── [ ] Migration tested locally
├── [ ] Migration tested in staging
├── [ ] Rollback script exists
├── [ ] Data backup completed
└── [ ] Team notified

□ Review
├── [ ] No destructive changes (or approved)
├── [ ] Indexes added for new columns
├── [ ] Constraints validated
└── [ ] Performance impact assessed

□ Execution
├── [ ] Maintenance window scheduled (if needed)
├── [ ] Monitoring in place
├── [ ] Rollback procedure documented
└── [ ] Post-migration verification planned

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🔄 CDC REAL-TIME SYNC

```yaml
cdc_patterns:
  description: "Capture and replicate changes in real-time"

  tools:
    postgres: "Debezium, pgoutput"
    mysql: "Debezium, Binlog"
    generic: "Fivetran, Airbyte"

  benefits:
    - "Minimal cutover downtime"
    - "Continuous validation"
    - "Rollback capability"
    - "Zero-downtime migrations"

  workflow: 1. "Setup CDC connector"
    2. "Sync historical data"
    3. "Enable continuous replication"
    4. "Validate data integrity"
    5. "Cutover when ready"

  command: "/migrate cdc [setup|status]"
```

---

## 📐 SCHEMA EVOLUTION STRATEGIES

```yaml
schema_evolution:
  expand_contract:
    description: "Safe schema changes"
    steps: 1. "Add new columns (don't remove)"
      2. "Deploy app supporting both"
      3. "Migrate data"
      4. "Remove old columns later"

  version_columns:
    description: "Schema version per row"
    use_case: "Mixed data versions"

  schema_registry:
    description: "Centralized management"
    tools: ["Confluent", "Apicurio"]

  serialization:
    recommendation: "Avro/Protobuf over JSON"
    reason: "Built-in schema evolution"

  command: "/migrate schema [evolve|validate]"
```

---

## 🎯 ZERO-DOWNTIME CHECKLIST

```yaml
zero_downtime:
  pre_flight:
    - "Backup verified and restorable"
    - "Rollback plan documented"
    - "Feature flags in place"
    - "Monitoring dashboards ready"

  execution:
    - "Blue-green or canary strategy"
    - "Incremental data sync (CDC)"
    - "Application backward compatible"
    - "Connection pooling active"

  post_migration:
    - "Data integrity validation"
    - "Performance baseline comparison"
    - "Cleanup deprecated columns"
    - "Update documentation"
```

---

## ⚠️ ROLLBACK SAFETY MATRIX

```yaml
rollback_safety:
  matrix: |
    | Change Type | Rollback | Risk     |
    |-------------|----------|----------|
    | Add column  | Safe     | Low      |
    | Add index   | Safe     | Low      |
    | Rename col  | Risky    | High     |
    | Drop column | Destroy  | Critical |
    | Drop table  | Destroy  | Critical |

  ⚠️_warning: |
    Data written after migration
    will be LOST on rollback.

  best_practice: |
    Always use expand-contract pattern
    for schema changes in production.

  command: "/migrate rollback [plan|execute]"
```

---

## ⚙️ TOKEN OPTIMIZATION

```yaml
token_saving:
  # Quick status first
  - Show pending count
  - Highlight breaking changes only

  # Batch operations
  - Group similar migrations
  - Single command execution

  # Smart defaults
  - Auto-detect tool
  - Use environment-appropriate backup
```

---

## 📜 RULES APPLIED

| Phase    | Rules                |
| -------- | -------------------- |
| Detect   | `context-management` |
| Validate | `stop-conditions`    |
| Backup   | `safety`             |
| Execute  | `edit-verification`  |
| Verify   | `evidence`           |

---

_DOMYH Awesome Code v4.3 • Migrate Pro v3.1 • Zero-Downtime CDC_
