## 🐘 PostgreSQL 17/18 (2024-2025)

### Version Comparison

| Feature                   | PG 17 (2024) | PG 18 (2025) |
| ------------------------- | ------------ | ------------ |
| JSON_TABLE()              | ✅          | ✅          |
| Incremental Backup        | ✅          | ✅          |
| MERGE + RETURNING         | ✅          | ✅          |
| Asynchronous I/O (AIO)    | ❌           | ✅ NEW      |
| Skip Scan (B-tree)        | ❌           | ✅ NEW      |
| RETURNING OLD/NEW         | ❌           | ✅ NEW      |
| UUIDv7                    | ❌           | ✅ NEW      |
| Virtual Generated Columns | ❌           | ✅ NEW      |
| NOT NULL (NOT VALID)      | ❌           | ✅ NEW      |

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
