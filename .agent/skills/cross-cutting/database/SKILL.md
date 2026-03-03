---
name: database
description: "Database design patterns for SQL and NoSQL. Use when designing schemas, queries, indexes, or migrations."
category: infrastructure
---

﻿---
name: database
detect:
  ["*.sql", "schema.prisma", "drizzle/", "migrations/", "*.db", "*.sqlite"]
category: infrastructure
tier: 1
---

# Database Patterns DOMYH Awesome Code

> SQL + NoSQL Patterns PostgreSQL 18, MySQL 9.4, MongoDB 8, Redis 8 2025-2026

## Decision Tree

```
Task → What database need?
   Structured data with relationships
      Complex queries → PostgreSQL (JSON + full-text + GIS)
      Simple reads → MySQL (fast, reliable)
      Global distribution → CockroachDB / TiDB
   Flexible schema
      Document model → MongoDB
      Time-series → InfluxDB / TimescaleDB
   Caching / sessions
      Redis (sub-ms, TTL, pub/sub)
   Search
      Full-text → PostgreSQL GIN or Elasticsearch
      Vector → pgvector / Redis VectorSet
   ORM selection
       Type-safe → Prisma (schema-first)
       SQL-first → Drizzle (lightweight)
       Legacy → TypeORM / Sequelize
```

---

## 📦 What's New in Databases (2025-2026)

| Database       | Version | Release  | Key Features                        |
| -------------- | ------- | -------- | ----------------------------------- |
| **PostgreSQL** | 18      | Sep 2025 | UUIDv7, Virtual Columns, AIO        |
| **MySQL**      | 9.4     | Jul 2025 | Vector type, JSON Duality, HeatWave |
| **MongoDB**    | 8       | 2025     | QE Range Queries, Express Path      |
| **Redis**      | 8       | 2025     | Vector Set, JSON, 87% faster        |

### PostgreSQL 18 Highlights

```sql
-- UUIDv7: Time-ordered UUIDs (better index performance)
id UUID DEFAULT uuidv7()

-- Virtual Generated Columns (compute on demand)
full_name TEXT GENERATED ALWAYS AS (first || ' ' || last) VIRTUAL

-- RETURNING OLD/NEW
UPDATE users SET name = 'New' RETURNING OLD.name, NEW.name

-- UNIQUE NULLS DISTINCT
CREATE UNIQUE INDEX idx ON t(col) NULLS DISTINCT
```

### MySQL 9.4 Highlights

```sql
-- Vector Data Type (for ML/AI)
CREATE TABLE items (
  id INT PRIMARY KEY,
  embedding VECTOR(1536)
);

-- JSON Duality Views (expose relational as JSON)
CREATE JSON DUALITY VIEW users_json AS SELECT * FROM users;

-- Parallel Query (multi-core)
SET SESSION parallel_degree = 4;
```

### MongoDB 8 Highlights

```javascript
// Queryable Encryption with Range Queries (NEW in 8)
db.patients.find({ age: { $gte: 21, $lte: 65 } }); // encrypted!

// Express Path (faster simple queries)
// Automatic for _id and simple equality

// 8.2 Preview: Prefix/Suffix search on encrypted
```

### Redis 8 Highlights

```bash
# Vector Set (AI semantic search, beta)
VADD myvecs id1 [...vector...]
VSEARCH myvecs TOPK 10 [...query...]

# New Hash Commands
HGETDEL myhash field1  # Get and delete
HSETEX myhash EX 3600 field1 value1  # Set with TTL

# Performance: 87% faster latency, 2x throughput
```

## 🔍 Database Detection

```yaml
sql_indicators:
  - "*.sql files"
  - "schema.prisma, drizzle/"
  - "SELECT, INSERT, UPDATE, DELETE"
  - "CREATE TABLE, ALTER TABLE"
  - "JOIN, GROUP BY, ORDER BY"
  - "PostgreSQL: $1, $2 parameters"
  - "MySQL: ?, ? parameters"

nosql_indicators:
  - "mongod, mongoose, mongodb"
  - "redis-cli, ioredis"
  - "db.collection.find()"
  - "HSET, HGET, LPUSH"
```

---

## 📊 Database Selection Guide (2025-2026)

### When to Use What

| Requirement                   | Database                 | Reason                          |
| ----------------------------- | ------------------------ | ------------------------------- |
| **ACID transactions**         | PostgreSQL, MySQL        | Strong consistency              |
| **Complex queries/joins**     | PostgreSQL               | Advanced SQL, JSON support      |
| **Read-heavy, simple schema** | MySQL                    | Fast reads, simple setup        |
| **Flexible schema**           | MongoDB                  | Document model, rapid iteration |
| **Caching**                   | Redis                    | Sub-ms latency, in-memory       |
| **Session storage**           | Redis                    | Fast, TTL support               |
| **Time-series**               | PostgreSQL + TimescaleDB | Optimized for time data         |
| **Full-text search**          | PostgreSQL               | Built-in, or Elasticsearch      |
| **Distributed**               | TiDB, CockroachDB        | Horizontal scaling, global      |
| **Serverless DB**             | PlanetScale, Neon        | Branching, autoscaling          |
| **Graph queries**             | Neo4j, SurrealDB         | Connected data                  |

### Polyglot Persistence (Recommended Pattern)

```

> Application
> PostgreSQL    MongoDB      Redis      Elasticsearch
> (Primary)    (Flexible)  (Cache)      (Search)
> Users        Logs        Sessions     Products
> Orders       Events      Rate Limit   Full-text
> Payments     Analytics   Leaderboard
```

---

## 📚 Deep-Dive References

- **PostgreSQL 17/18** — Table partitioning, JSONB, full-text search, performance tuning
  → See [references/postgresql.md](references/postgresql.md)

- **ORMs Comparison & Patterns** — MySQL, Prisma, Drizzle, TypeORM patterns
  → See [references/orms-patterns.md](references/orms-patterns.md)

- **NoSQL Patterns** — MongoDB aggregation, Redis caching, pub/sub, Streams
  → See [references/nosql-patterns.md](references/nosql-patterns.md)

## ✅ Production Checklist

### Schema Design

- [ ] Primary keys defined (prefer UUID/CUID)
- [ ] Foreign keys with proper constraints
- [ ] Indexes on frequently queried columns
- [ ] Indexes on foreign keys
- [ ] NOT NULL where appropriate
- [ ] Proper data types selected

### Performance

- [ ] Connection pooling configured
- [ ] Query plans analyzed (EXPLAIN ANALYZE)
- [ ] N+1 queries eliminated
- [ ] Slow query logging enabled
- [ ] Autovacuum tuned (PostgreSQL)

### Security

- [ ] Parameterized queries (no SQL injection)
- [ ] Least privilege DB users
- [ ] Secrets in environment variables
- [ ] SSL/TLS connections
- [ ] Row-level security where needed

### Operations

- [ ] Migrations versioned and tested
- [ ] Backup strategy in place
- [ ] Point-in-time recovery tested
- [ ] Monitoring and alerts configured
- [ ] Read replicas for scale (if needed)

---

## 📌 HSA Integration

Data powered by HSA BM25 search engine across 6 database domains:

| Domain     | Query Examples                                |
| ---------- | --------------------------------------------- |
| PostgreSQL | "UUIDv7 AIO virtual columns PG18"             |
| MySQL      | "vector type JSON duality views"              |
| MongoDB    | "aggregation pipeline queryable encryption"   |
| Redis      | "vector set distributed lock pub/sub"         |
| ORM        | "Prisma Drizzle N+1 query optimization"       |
| Migration  | "connection pooling PgBouncer rolling deploy" |

---
