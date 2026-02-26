# Database — Advanced Patterns

> DOMYH Awesome Code — Tier 3 Reference

## Table of Contents

- [Query Optimization Deep Dive](#query-optimization-deep-dive)
- [Advanced Indexing](#advanced-indexing)
- [Partitioning Strategies](#partitioning-strategies)
- [Replication & High Availability](#replication--high-availability)
- [Time-Series Data](#time-series-data)
- [Full-Text Search](#full-text-search)
- [Database Migrations](#database-migrations)

---

## Query Optimization Deep Dive

### EXPLAIN ANALYZE Interpretation

```sql
-- Full analysis with buffers and timing
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.id, u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.created_at > NOW() - INTERVAL '30 days'
GROUP BY u.id
ORDER BY order_count DESC
LIMIT 100;

-- Key metrics to watch:
-- • "Seq Scan" → Consider adding index
-- • "Nested Loop" with high rows → Consider HASH JOIN
-- • "Rows Removed by Filter" high → Index not selective enough
-- • "Buffers: read" → Disk I/O (cache miss)
-- • "Buffers: hit" → Memory cache hit
```

### CTE Materialization Control

```sql
-- MATERIALIZED: Force materialization (temporary table)
-- Use when CTE is used multiple times
WITH active_users AS MATERIALIZED (
    SELECT id, email FROM users WHERE status = 'active'
)
SELECT * FROM active_users
UNION ALL
SELECT * FROM active_users WHERE email LIKE '%@company.com';

-- NOT MATERIALIZED: Inline into main query
-- Use when CTE is used once, optimizer can push predicates
WITH recent_orders AS NOT MATERIALIZED (
    SELECT user_id, SUM(total) as total
    FROM orders
    WHERE created_at > NOW() - INTERVAL '7 days'
    GROUP BY user_id
)
SELECT u.email, COALESCE(o.total, 0)
FROM users u
LEFT JOIN recent_orders o ON o.user_id = u.id
WHERE u.id = 123;  -- Predicate can be pushed down
```

### Batch Processing Patterns

```sql
-- Process large tables in batches (avoid locks)
DO $$
DECLARE
    batch_size INT := 1000;
    affected INT;
BEGIN
    LOOP
        WITH batch AS (
            SELECT id FROM large_table
            WHERE processed = FALSE
            LIMIT batch_size
            FOR UPDATE SKIP LOCKED
        )
        UPDATE large_table
        SET processed = TRUE,
            processed_at = NOW()
        WHERE id IN (SELECT id FROM batch);

        GET DIAGNOSTICS affected = ROW_COUNT;

        COMMIT;

        IF affected = 0 THEN EXIT; END IF;

        PERFORM pg_sleep(0.1);  -- Brief pause
    END LOOP;
END $$;
```

---

## Advanced Indexing

### Index Type Selection

| Index Type  | Best For                       | Example              |
| ----------- | ------------------------------ | -------------------- |
| **B-tree**  | Equality, range, ORDER BY      | `id = ?`, `date > ?` |
| **Hash**    | Equality only (rarely needed)  | `id = ?`             |
| **GIN**     | Arrays, JSONB, full-text       | `tags @> '{a,b}'`    |
| **GiST**    | Geometric, range, full-text    | Spatial queries      |
| **BRIN**    | Time-series, naturally ordered | Large tables by date |
| **SP-GiST** | Non-balanced structures        | IP ranges            |

### Composite Index Design

```sql
-- Index column order matters!
-- Rule: Most selective → Equality → Range → ORDER BY

-- Good: user_id (equality) then created_at (range/sort)
CREATE INDEX idx_orders_optimal
ON orders(user_id, created_at DESC);

-- Works for:
-- WHERE user_id = ? ORDER BY created_at DESC  ✅
-- WHERE user_id = ?                           ✅
-- WHERE user_id = ? AND created_at > ?        ✅

-- Does NOT work for:
-- WHERE created_at > ?  ❌ (skips first column)
-- ORDER BY created_at DESC  ❌ (skips first column)
```

### Covering Indexes (INCLUDE)

```sql
-- Include columns to avoid table lookup (Index-Only Scan)
CREATE INDEX idx_orders_covering
ON orders(user_id, status)
INCLUDE (total, created_at);

-- This query uses Index-Only Scan (no table access needed)
SELECT user_id, status, total, created_at
FROM orders
WHERE user_id = 123 AND status = 'completed';
```

### Partial Indexes

```sql
-- Index only specific rows (smaller, faster)
CREATE INDEX idx_orders_pending
ON orders(user_id, created_at)
WHERE status = 'pending';

-- Great for:
-- • Status flags (only active records)
-- • Recent data (last 30 days)
-- • Soft deletes (WHERE deleted_at IS NULL)
```

### Expression Indexes

```sql
-- Index computed values
CREATE INDEX idx_users_email_lower
ON users (LOWER(email));

-- Query must match expression exactly
SELECT * FROM users WHERE LOWER(email) = 'alice@example.com';

-- JSON path expression
CREATE INDEX idx_events_type
ON events ((data->>'type'));

SELECT * FROM events WHERE data->>'type' = 'purchase';
```

---

## Partitioning Strategies

### Range Partitioning (Time-Series)

```sql
-- Create partitioned table
CREATE TABLE events (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    event_type TEXT NOT NULL,
    data JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
) PARTITION BY RANGE (created_at);

-- Create partitions (monthly)
CREATE TABLE events_2025_01 PARTITION OF events
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

CREATE TABLE events_2025_02 PARTITION OF events
    FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');

-- Automatic partition creation (pg_partman or scheduled job)
-- Or use DEFAULT partition for overflow
CREATE TABLE events_default PARTITION OF events DEFAULT;
```

### List Partitioning (Multi-Tenant)

```sql
-- Partition by tenant
CREATE TABLE orders (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    tenant_id TEXT NOT NULL,
    total NUMERIC(10,2),
    created_at TIMESTAMPTZ DEFAULT NOW()
) PARTITION BY LIST (tenant_id);

CREATE TABLE orders_tenant_a PARTITION OF orders
    FOR VALUES IN ('tenant_a');

CREATE TABLE orders_tenant_b PARTITION OF orders
    FOR VALUES IN ('tenant_b');
```

### PostgreSQL 17: MERGE PARTITIONS

```sql
-- PG 17: Merge partitions
ALTER TABLE events MERGE PARTITIONS (
    events_2024_01, events_2024_02, events_2024_03
) INTO events_2024_q1;

-- PG 17: Split partition
ALTER TABLE events SPLIT PARTITION events_2024_q1 INTO (
    PARTITION events_2024_01 FOR VALUES FROM ('2024-01-01') TO ('2024-02-01'),
    PARTITION events_2024_02 FOR VALUES FROM ('2024-02-01') TO ('2024-03-01'),
    PARTITION events_2024_03 FOR VALUES FROM ('2024-03-01') TO ('2024-04-01')
);
```

---

## Replication & High Availability

### Logical Replication Setup

```sql
-- Publisher (source)
CREATE PUBLICATION my_publication FOR TABLE users, orders;

-- Subscriber (target)
CREATE SUBSCRIPTION my_subscription
CONNECTION 'host=source dbname=mydb user=repl password=xxx'
PUBLICATION my_publication;
```

### Read Replica Pattern

```typescript
// Prisma with read replicas
const prisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_URL,
    },
  },
});

// Extension for read replicas
import { PrismaClient as ReplicaClient } from "@prisma/client";

const readReplica = new ReplicaClient({
  datasources: {
    db: { url: process.env.DATABASE_REPLICA_URL },
  },
});

// Use primary for writes, replica for reads
async function getUser(id: string) {
  return readReplica.user.findUnique({ where: { id } });
}

async function updateUser(id: string, data: UpdateUserDto) {
  return prisma.user.update({ where: { id }, data });
}
```

### PgBouncer Configuration

```ini
; /etc/pgbouncer/pgbouncer.ini

[databases]
mydb = host=126.3.9.1 port=5432 dbname=mydb

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = scram-sha-256
auth_file = /etc/pgbouncer/userlist.txt

; Pool modes: session, transaction, statement
pool_mode = transaction

; Connection limits
max_client_conn = 1000
default_pool_size = 25
min_pool_size = 5
reserve_pool_size = 5
reserve_pool_timeout = 3

; Connection lifecycle
server_lifetime = 3600
server_idle_timeout = 600
server_connect_timeout = 5

; Logging
log_connections = 1
log_disconnections = 1
log_pooler_errors = 1

; Stats
stats_period = 60
```

---

## Time-Series Data

### TimescaleDB Pattern

```sql
-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Create hypertable
CREATE TABLE metrics (
    time TIMESTAMPTZ NOT NULL,
    device_id TEXT NOT NULL,
    temperature DOUBLE PRECISION,
    humidity DOUBLE PRECISION
);

-- Convert to hypertable (auto-partitions by time)
SELECT create_hypertable('metrics', 'time');

-- Add compression (for old data)
ALTER TABLE metrics SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'device_id'
);

-- Continuous aggregates (pre-computed rollups)
CREATE MATERIALIZED VIEW metrics_hourly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', time) AS bucket,
    device_id,
    AVG(temperature) AS avg_temp,
    MAX(temperature) AS max_temp,
    MIN(temperature) AS min_temp
FROM metrics
GROUP BY bucket, device_id;

-- Refresh policy
SELECT add_continuous_aggregate_policy('metrics_hourly',
    start_offset => INTERVAL '1 week',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 hour');
```

---

## Full-Text Search

### PostgreSQL Full-Text Search

```sql
-- Create tsvector column
ALTER TABLE products ADD COLUMN search_vector TSVECTOR;

-- Populate with weighted search content
UPDATE products SET search_vector =
    setweight(to_tsvector('english', COALESCE(name, '')), 'A') ||
    setweight(to_tsvector('english', COALESCE(description, '')), 'B') ||
    setweight(to_tsvector('english', COALESCE(tags::TEXT, '')), 'C');

-- Create GIN index
CREATE INDEX idx_products_search ON products USING GIN(search_vector);

-- Trigger to maintain
CREATE OR REPLACE FUNCTION products_search_trigger() RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('english', COALESCE(NEW.name, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.description, '')), 'B');
    RETURN NEW;
END $$ LANGUAGE plpgsql;

CREATE TRIGGER products_search_update
BEFORE INSERT OR UPDATE ON products
FOR EACH ROW EXECUTE FUNCTION products_search_trigger();

-- Search query with ranking
SELECT id, name, ts_rank(search_vector, query) AS rank
FROM products,
     plainto_tsquery('english', 'gaming laptop') AS query
WHERE search_vector @@ query
ORDER BY rank DESC
LIMIT 20;
```

---

## Database Migrations

### Migration Best Practices

```sql
-- ✅ Safe migration patterns

-- 1. Add column (non-blocking)
ALTER TABLE users ADD COLUMN phone TEXT;

-- 2. Add NOT NULL with default (PG 11+, instant)
ALTER TABLE users ADD COLUMN status TEXT NOT NULL DEFAULT 'active';

-- 3. Add index concurrently (non-blocking)
CREATE INDEX CONCURRENTLY idx_users_phone ON users(phone);

-- ⚠️ Careful migration patterns

-- 4. Add NOT NULL to existing column (PG 18+ with NOT VALID)
ALTER TABLE users ADD CONSTRAINT users_phone_not_null
    CHECK (phone IS NOT NULL) NOT VALID;
-- Later, validate without exclusive lock:
ALTER TABLE users VALIDATE CONSTRAINT users_phone_not_null;

-- 5. Rename column (requires code change coordination)
-- Use alias approach:
ALTER TABLE users RENAME COLUMN old_name TO new_name;
-- Update application in parallel

-- ❌ Dangerous patterns (avoid in production)

-- Lock entire table (blocks all operations)
ALTER TABLE users ALTER COLUMN status TYPE VARCHAR(100);

-- Rewrite entire table
ALTER TABLE orders SET (autovacuum_enabled = false);
```

### Zero-Downtime Migration Strategy

```
1. Deploy new code that reads BOTH old and new columns
2. Run migration to add new column
3. Backfill new column from old column
4. Deploy code that writes to BOTH columns
5. Verify data consistency
6. Deploy code that reads ONLY from new column
7. Remove old column (optional, can defer)
```

---
