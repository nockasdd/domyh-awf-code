---
name: database
detect:
  ["*.sql", "schema.prisma", "drizzle/", "migrations/", "*.db", "*.sqlite"]
version: "6.2.0"
category: infrastructure
tier: 1
---

# Database Patterns — DOMYH Awesome Code

> SQL + NoSQL Patterns — PostgreSQL 18, MySQL 9.4, MongoDB 8, Redis 8 — 2025-2026

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
┌─────────────────────────────────────────────────────┐
│                   Application                        │
├───────────┬───────────┬───────────┬─────────────────┤
│ PostgreSQL│  MongoDB  │   Redis   │  Elasticsearch  │
│ (Primary) │ (Flexible)│ (Cache)   │   (Search)      │
│ Users     │ Logs      │ Sessions  │  Products       │
│ Orders    │ Events    │ Rate Limit│  Full-text      │
│ Payments  │ Analytics │ Leaderboard│               │
└───────────┴───────────┴───────────┴─────────────────┘
```

---

## 🐘 PostgreSQL 17/18 (2024-2025)

### Version Comparison

| Feature                   | PG 17 (2024) | PG 18 (2025) |
| ------------------------- | ------------ | ------------ |
| JSON_TABLE()              | ✅           | ✅           |
| Incremental Backup        | ✅           | ✅           |
| MERGE + RETURNING         | ✅           | ✅           |
| Asynchronous I/O (AIO)    | ❌           | ✅ NEW       |
| Skip Scan (B-tree)        | ❌           | ✅ NEW       |
| RETURNING OLD/NEW         | ❌           | ✅ NEW       |
| UUIDv7                    | ❌           | ✅ NEW       |
| Virtual Generated Columns | ❌           | ✅ NEW       |
| NOT NULL (NOT VALID)      | ❌           | ✅ NEW       |

### PostgreSQL Core Patterns

```sql
-- ✅ Parameterized queries (prevent SQL injection)
SELECT id, name, email FROM users WHERE id = $1;

-- ✅ Indexes (critical for performance)
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_user_created
    ON orders(user_id, created_at DESC);

-- ✅ Partial index (index subset of rows)
CREATE INDEX idx_active_users ON users(email)
    WHERE active = true;

-- ✅ Covering index (include columns to avoid table lookup)
CREATE INDEX idx_orders_covering
    ON orders(user_id) INCLUDE (status, total);

-- ✅ BRIN index (for large time-series tables)
CREATE INDEX idx_events_created
    ON events USING BRIN(created_at);
```

### PostgreSQL 18 New Features

```sql
-- ✅ PG 18: RETURNING OLD and NEW values
UPDATE products SET price = price * 1.1
RETURNING OLD.price AS old_price, NEW.price AS new_price;

DELETE FROM users WHERE inactive = true
RETURNING OLD.*;

-- ✅ PG 18: UUIDv7 (time-ordered, better for indexes)
SELECT uuidv7();  -- e.g., 019445a0-c000-7000-8000-000000000001

-- ✅ PG 18: NOT NULL constraint without full scan
ALTER TABLE large_table
    ADD CONSTRAINT col_not_null
    CHECK (col IS NOT NULL) NOT VALID;
-- Validate later without ACCESS EXCLUSIVE lock
ALTER TABLE large_table
    VALIDATE CONSTRAINT col_not_null;
```

### PostgreSQL JSON Operations

```sql
-- ✅ JSONB storage and querying
CREATE TABLE events (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    data JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- GIN index for JSONB
CREATE INDEX idx_events_data ON events USING GIN(data);

-- Query JSONB
SELECT * FROM events
WHERE data @> '{"type": "purchase"}';

SELECT data->>'user_id' AS user_id,
       (data->>'amount')::NUMERIC AS amount
FROM events
WHERE data->>'type' = 'purchase';

-- ✅ PG 17: JSON_TABLE (convert JSON to rows)
SELECT jt.*
FROM events,
     JSON_TABLE(
         data,
         '$.items[*]'
         COLUMNS (
             product_id INT PATH '$.product_id',
             quantity INT PATH '$.qty',
             price NUMERIC PATH '$.price'
         )
     ) AS jt;
```

### PostgreSQL Transactions & Locking

```sql
-- ✅ Transaction with proper isolation
BEGIN;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

COMMIT;

-- ✅ Advisory locks (application-level)
SELECT pg_advisory_lock(12345);  -- Acquire
-- Do work...
SELECT pg_advisory_unlock(12345);  -- Release
```

### PostgreSQL Configuration (Performance)

```sql
-- Key parameters for performance tuning
-- postgresql.conf

-- Memory (adjust based on RAM)
shared_buffers = '4GB'           -- 25% of RAM
effective_cache_size = '12GB'    -- 75% of RAM
work_mem = '256MB'               -- Per operation
maintenance_work_mem = '1GB'     -- For VACUUM, CREATE INDEX

-- WAL
wal_buffers = '64MB'
checkpoint_timeout = '15min'
max_wal_size = '4GB'

-- Connections
max_connections = 200
-- Use PgBouncer for connection pooling!

-- Queries
statement_timeout = '30s'        -- Prevent long queries
lock_timeout = '10s'             -- Prevent lock waiting
```

---

## 🐬 MySQL 8.x

### MySQL Core Patterns

```sql
-- ✅ Parameterized queries (use ? placeholder)
SELECT id, name FROM users WHERE id = ?;

-- ✅ Indexes
CREATE INDEX idx_users_email ON users(email);

-- ✅ Full-text search
CREATE FULLTEXT INDEX idx_products_search
    ON products(name, description);

SELECT * FROM products
WHERE MATCH(name, description) AGAINST('laptop' IN NATURAL LANGUAGE MODE);

-- ✅ Window functions
SELECT id, name, price,
       ROW_NUMBER() OVER (ORDER BY price DESC) AS rank,
       AVG(price) OVER () AS avg_price
FROM products;
```

### MySQL vs PostgreSQL

| Feature          | PostgreSQL              | MySQL             |
| ---------------- | ----------------------- | ----------------- |
| JSON Support     | JSONB (binary, indexed) | JSON (text-based) |
| Full-text Search | Built-in tsquery        | FULLTEXT index    |
| CTEs             | Optimized               | Less optimized    |
| Arrays           | Native                  | JSON workaround   |
| Enums            | Native                  | Limited           |
| Partitioning     | Declarative             | Hash, Range, List |
| Replication      | Logical + Physical      | Group Replication |

---

## 📦 ORMs Comparison (2025)

### Node.js/TypeScript

| ORM           | Type Safety | Performance | Bundle Size | Best For              |
| ------------- | ----------- | ----------- | ----------- | --------------------- |
| **Prisma 7**  | ⭐⭐⭐⭐⭐  | ⭐⭐⭐⭐    | 90% smaller | Type-safe, Next.js    |
| **Drizzle**   | ⭐⭐⭐⭐⭐  | ⭐⭐⭐⭐⭐  | ~7.4kb      | Serverless, SQL-first |
| **TypeORM**   | ⭐⭐⭐⭐    | ⭐⭐⭐      | Medium      | NestJS, Enterprise    |
| **Sequelize** | ⭐⭐⭐      | ⭐⭐⭐      | Medium      | Legacy, Beginner      |
| **Kysely**    | ⭐⭐⭐⭐⭐  | ⭐⭐⭐⭐⭐  | Tiny        | Type-safe SQL builder |

### Python

| ORM                | Use Case                         |
| ------------------ | -------------------------------- |
| **SQLAlchemy 2.0** | Industry standard, async support |
| **Tortoise ORM**   | Async-first, Django-like         |
| **SQLModel**       | Pydantic + SQLAlchemy            |

### Go

| Library  | Use Case                    |
| -------- | --------------------------- |
| **GORM** | Full-featured ORM           |
| **sqlc** | Code generation from SQL    |
| **sqlx** | Extensions for database/sql |
| **pgx**  | PostgreSQL driver           |

---

## 🔷 Prisma Patterns

### Schema Definition

```prisma
// schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  role      Role     @default(USER)
  posts     Post[]
  profile   Profile?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([email])
  @@index([createdAt])
}

model Post {
  id        String   @id @default(cuid())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  String
  tags      Tag[]
  createdAt DateTime @default(now())

  @@index([authorId])
  @@index([published, createdAt])
}

enum Role {
  USER
  ADMIN
  MODERATOR
}
```

### Prisma Queries

```typescript
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

// ✅ Find with relations
const users = await prisma.user.findMany({
  where: { role: "ADMIN" },
  include: { posts: { where: { published: true } } },
  orderBy: { createdAt: "desc" },
  take: 10,
});

// ✅ Create with nested relations
const user = await prisma.user.create({
  data: {
    email: "alice@example.com",
    name: "Alice",
    posts: {
      create: [{ title: "Hello World", content: "First post!" }],
    },
  },
  include: { posts: true },
});

// ✅ Transaction (atomic operations)
const [updatedUser, newPost] = await prisma.$transaction([
  prisma.user.update({
    where: { id: userId },
    data: { postCount: { increment: 1 } },
  }),
  prisma.post.create({
    data: { title: "New Post", authorId: userId },
  }),
]);

// ✅ Interactive transaction
await prisma.$transaction(async (tx) => {
  const balance = await tx.account.findUnique({
    where: { id: fromAccountId },
  });

  if (balance.amount < transferAmount) {
    throw new Error("Insufficient funds");
  }

  await tx.account.update({
    where: { id: fromAccountId },
    data: { amount: { decrement: transferAmount } },
  });

  await tx.account.update({
    where: { id: toAccountId },
    data: { amount: { increment: transferAmount } },
  });
});
```

---

## 🔶 Drizzle Patterns

### Schema Definition

```typescript
// schema.ts
import { pgTable, text, timestamp, boolean, index } from "drizzle-orm/pg-core";
import { relations } from "drizzle-orm";

export const users = pgTable(
  "users",
  {
    id: text("id")
      .primaryKey()
      .$defaultFn(() => crypto.randomUUID()),
    email: text("email").notNull().unique(),
    name: text("name"),
    createdAt: timestamp("created_at").defaultNow().notNull(),
  },
  (table) => ({
    emailIdx: index("users_email_idx").on(table.email),
  }),
);

export const posts = pgTable(
  "posts",
  {
    id: text("id")
      .primaryKey()
      .$defaultFn(() => crypto.randomUUID()),
    title: text("title").notNull(),
    content: text("content"),
    published: boolean("published").default(false),
    authorId: text("author_id")
      .notNull()
      .references(() => users.id),
    createdAt: timestamp("created_at").defaultNow().notNull(),
  },
  (table) => ({
    authorIdx: index("posts_author_idx").on(table.authorId),
  }),
);

export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
}));

export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, {
    fields: [posts.authorId],
    references: [users.id],
  }),
}));
```

### Drizzle Queries

```typescript
import { drizzle } from "drizzle-orm/node-postgres";
import { eq, and, desc } from "drizzle-orm";
import * as schema from "./schema";

const db = drizzle(pool, { schema });

// ✅ SQL-like query API
const activeUsers = await db
  .select()
  .from(schema.users)
  .where(eq(schema.users.active, true))
  .orderBy(desc(schema.users.createdAt))
  .limit(10);

// ✅ Relational query API
const usersWithPosts = await db.query.users.findMany({
  with: {
    posts: {
      where: eq(schema.posts.published, true),
    },
  },
});

// ✅ Transaction
await db.transaction(async (tx) => {
  await tx
    .update(schema.accounts)
    .set({ balance: sql`balance - 100` })
    .where(eq(schema.accounts.id, 1));

  await tx
    .update(schema.accounts)
    .set({ balance: sql`balance + 100` })
    .where(eq(schema.accounts.id, 2));
});
```

---

## 🍃 MongoDB Patterns

### When to Use MongoDB

| ✅ Good For              | ❌ Not Good For               |
| ------------------------ | ----------------------------- |
| Flexible/evolving schema | Complex joins                 |
| JSON-like documents      | ACID transactions (multi-doc) |
| Rapid prototyping        | Strong consistency            |
| Content management       | Financial data                |
| IoT data ingestion       | Complex queries               |
| Real-time analytics      | Relational data               |

### MongoDB Node.js Patterns

```typescript
import { MongoClient, ObjectId } from "mongodb";

const client = new MongoClient(process.env.MONGODB_URI);
const db = client.db("myapp");

// ✅ Insert
await db.collection("users").insertOne({
  email: "alice@example.com",
  name: "Alice",
  metadata: { lastLogin: new Date(), preferences: { theme: "dark" } },
  createdAt: new Date(),
});

// ✅ Find with projection
const user = await db.collection("users").findOne(
  { email: "alice@example.com" },
  { projection: { password: 0 } }, // Exclude password
);

// ✅ Aggregation pipeline
const results = await db
  .collection("orders")
  .aggregate([
    { $match: { status: "completed" } },
    {
      $group: {
        _id: "$userId",
        totalAmount: { $sum: "$amount" },
        orderCount: { $sum: 1 },
      },
    },
    { $sort: { totalAmount: -1 } },
    { $limit: 10 },
  ])
  .toArray();

// ✅ Indexes
await db.collection("users").createIndex({ email: 1 }, { unique: true });
await db
  .collection("events")
  .createIndex({ createdAt: 1 }, { expireAfterSeconds: 86400 });
```

---

## 🔴 Redis Patterns

### Redis Use Cases

| Pattern         | Use Case             | TTL        |
| --------------- | -------------------- | ---------- |
| **Cache**       | Database query cache | 5-60 min   |
| **Session**     | User sessions        | 24h        |
| **Rate Limit**  | API throttling       | 1 min      |
| **Leaderboard** | Sorted sets          | Persistent |
| **Pub/Sub**     | Real-time events     | N/A        |
| **Queue**       | Job queue (List)     | N/A        |
| **Lock**        | Distributed lock     | 30s        |

### Redis Node.js Patterns

```typescript
import Redis from "ioredis";

const redis = new Redis(process.env.REDIS_URL);

// ✅ Cache pattern
async function getCachedUser(userId: string) {
  const cacheKey = `user:${userId}`;

  // Try cache first
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);

  // Cache miss - fetch from DB
  const user = await db.users.findUnique({ where: { id: userId } });

  // Store in cache with TTL
  await redis.setex(cacheKey, 3600, JSON.stringify(user));

  return user;
}

// ✅ Rate limiting (sliding window)
async function checkRateLimit(ip: string, limit = 100, windowSec = 60) {
  const key = `ratelimit:${ip}`;
  const current = await redis.incr(key);

  if (current === 1) {
    await redis.expire(key, windowSec);
  }

  return current <= limit;
}

// ✅ Session storage
await redis.hset(`session:${sessionId}`, {
  userId: user.id,
  email: user.email,
  loginAt: Date.now(),
});
await redis.expire(`session:${sessionId}`, 86400); // 24h

// ✅ Leaderboard
await redis.zadd("leaderboard", score, `user:${userId}`);
const top10 = await redis.zrevrange("leaderboard", 0, 9, "WITHSCORES");

// ✅ Pub/Sub
const subscriber = redis.duplicate();
await subscriber.subscribe("notifications");
subscriber.on("message", (channel, message) => {
  console.log(`Received: ${message}`);
});

await redis.publish("notifications", JSON.stringify({ type: "new_order" }));

// ✅ Distributed lock
async function withLock<T>(key: string, fn: () => Promise<T>, ttlMs = 30000) {
  const lockKey = `lock:${key}`;
  const lockValue = crypto.randomUUID();

  const acquired = await redis.set(lockKey, lockValue, "PX", ttlMs, "NX");
  if (!acquired) throw new Error("Failed to acquire lock");

  try {
    return await fn();
  } finally {
    // Release only if we own the lock
    const script = `
      if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("del", KEYS[1])
      else
        return 0
      end
    `;
    await redis.eval(script, 1, lockKey, lockValue);
  }
}
```

---

## 🛠️ Database Tools

### Migration Tools

| Tool               | Language | Database   |
| ------------------ | -------- | ---------- |
| **Prisma Migrate** | TS/JS    | Multi      |
| **Drizzle Kit**    | TS/JS    | Multi      |
| **golang-migrate** | Go       | Multi      |
| **Alembic**        | Python   | SQLAlchemy |
| **Flyway**         | Java/CLI | Multi      |
| **Atlas**          | Go       | Multi      |

### Monitoring & GUI

| Tool                | Purpose        |
| ------------------- | -------------- |
| **pgAdmin**         | PostgreSQL GUI |
| **DBeaver**         | Universal GUI  |
| **TablePlus**       | Multi-DB GUI   |
| **Prisma Studio**   | Prisma visual  |
| **RedisInsight**    | Redis GUI      |
| **MongoDB Compass** | MongoDB GUI    |

### Connection Pooling

| Tool              | Database   |
| ----------------- | ---------- |
| **PgBouncer**     | PostgreSQL |
| **PgCat**         | PostgreSQL |
| **ProxySQL**      | MySQL      |
| **Redis Cluster** | Redis      |

---

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

## 🔌 HSA Integration

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

_DOMYH Awesome Code • Database Patterns • HSA-Powered • 2025-2026_
