---
library: postgresql
version: 17
latest: true
category: database
official_docs: https://www.postgresql.org/docs
last_updated: 2026-03-20
last_checked: 2026-03-21
source: official docs + crawl4ai/trafilatura extraction
---

# PostgreSQL v18

> PostgreSQL — The world's most advanced open-source relational database.
> Current: v18 | Previous: v17, v16
> Docs: https://www.postgresql.org/docs

## Data Types

```sql
-- Numeric
integer, bigint, smallint, serial, bigserial
numeric(10,2), decimal, real, double precision

-- Text
varchar(255), char(10), text

-- Boolean
boolean  -- true/false/null

-- Date/Time
date, time, timestamp, timestamptz, interval

-- JSON
json, jsonb  -- jsonb is binary, indexable, preferred

-- Arrays
integer[], text[], jsonb[]

-- UUID
uuid  -- use gen_random_uuid()

-- Other
bytea, inet, cidr, macaddr, point, polygon, tsvector
```

## DDL (Schema)

```sql
-- Create table
CREATE TABLE users (
  id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  email       VARCHAR(255) NOT NULL UNIQUE,
  name        TEXT NOT NULL,
  role        VARCHAR(20) DEFAULT 'user' CHECK (role IN ('user', 'admin', 'moderator')),
  metadata    JSONB DEFAULT '{}',
  tags        TEXT[] DEFAULT '{}',
  created_at  TIMESTAMPTZ DEFAULT NOW(),
  updated_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_users_metadata ON users USING GIN (metadata);
CREATE INDEX idx_users_tags ON users USING GIN (tags);
CREATE UNIQUE INDEX idx_users_email_lower ON users (LOWER(email));

-- Partial index (only active users)
CREATE INDEX idx_active_users ON users (email) WHERE role != 'inactive';

-- Composite index
CREATE INDEX idx_users_role_created ON users (role, created_at DESC);

-- Foreign keys
CREATE TABLE posts (
  id         BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  title      TEXT NOT NULL,
  content    TEXT,
  author_id  BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  published  BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Alter table
ALTER TABLE users ADD COLUMN avatar_url TEXT;
ALTER TABLE users DROP COLUMN IF EXISTS avatar_url;
ALTER TABLE users ALTER COLUMN name SET NOT NULL;
ALTER TABLE users RENAME COLUMN name TO full_name;
ALTER TABLE users ADD CONSTRAINT check_email CHECK (email ~* '^[^@]+@[^@]+$');
```

## DML (Queries)

```sql
-- INSERT
INSERT INTO users (email, name) VALUES ('alice@example.com', 'Alice') RETURNING *;

-- INSERT multiple
INSERT INTO users (email, name) VALUES
  ('bob@example.com', 'Bob'),
  ('carol@example.com', 'Carol')
RETURNING id, email;

-- INSERT with conflict (upsert)
INSERT INTO users (email, name) VALUES ('alice@example.com', 'Alice')
ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name, updated_at = NOW()
RETURNING *;

-- ON CONFLICT DO NOTHING
INSERT INTO users (email, name) VALUES ('alice@example.com', 'Alice')
ON CONFLICT DO NOTHING;

-- SELECT
SELECT u.name, COUNT(p.id) AS post_count
FROM users u
LEFT JOIN posts p ON p.author_id = u.id
WHERE u.role = 'admin'
GROUP BY u.id
HAVING COUNT(p.id) > 5
ORDER BY post_count DESC
LIMIT 10 OFFSET 0;

-- UPDATE
UPDATE users SET name = 'Bob', updated_at = NOW() WHERE id = 1 RETURNING *;

-- UPDATE with FROM (join update)
UPDATE posts p SET published = TRUE
FROM users u
WHERE p.author_id = u.id AND u.role = 'admin';

-- DELETE
DELETE FROM users WHERE id = 1 RETURNING *;

-- JSONB queries
SELECT * FROM users WHERE metadata->>'department' = 'engineering';
SELECT * FROM users WHERE metadata @> '{"active": true}';
SELECT * FROM users WHERE metadata ? 'department';
SELECT * FROM users WHERE metadata->'address'->>'city' = 'NYC';
SELECT jsonb_agg(metadata) FROM users;

-- JSONB update
UPDATE users SET metadata = metadata || '{"verified": true}'::jsonb WHERE id = 1;
UPDATE users SET metadata = metadata - 'temporary_field' WHERE id = 1;
UPDATE users SET metadata = jsonb_set(metadata, '{address,zip}', '"10001"') WHERE id = 1;

-- Array queries
SELECT * FROM users WHERE 'admin' = ANY(tags);
SELECT * FROM users WHERE tags @> ARRAY['admin', 'active'];
SELECT * FROM users WHERE tags && ARRAY['admin', 'moderator'];
SELECT unnest(tags) AS tag, COUNT(*) FROM users GROUP BY tag;
```

## CTEs & Window Functions

```sql
-- Common Table Expression (WITH)
WITH active_users AS (
  SELECT * FROM users WHERE role != 'inactive'
),
user_stats AS (
  SELECT author_id, COUNT(*) as post_count
  FROM posts GROUP BY author_id
)
SELECT u.name, COALESCE(s.post_count, 0) AS posts
FROM active_users u
LEFT JOIN user_stats s ON s.author_id = u.id;

-- Recursive CTE (tree structures)
WITH RECURSIVE category_tree AS (
  SELECT id, name, parent_id, 0 AS depth, ARRAY[id] AS path
  FROM categories WHERE parent_id IS NULL
  UNION ALL
  SELECT c.id, c.name, c.parent_id, ct.depth + 1, ct.path || c.id
  FROM categories c JOIN category_tree ct ON c.parent_id = ct.id
  WHERE NOT c.id = ANY(ct.path)  -- prevent cycles
)
SELECT * FROM category_tree ORDER BY path;

-- Window functions
SELECT name, department,
  salary,
  ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rank,
  RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rank_with_ties,
  AVG(salary) OVER (PARTITION BY department) AS dept_avg,
  SUM(salary) OVER (ORDER BY created_at ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS rolling_sum,
  salary - LAG(salary) OVER (ORDER BY salary) AS diff_from_prev,
  LEAD(salary) OVER (ORDER BY salary) AS next_salary,
  FIRST_VALUE(name) OVER (PARTITION BY department ORDER BY salary DESC) AS top_earner
FROM employees;
```

## Views & Materialized Views

```sql
-- View (virtual table — query runs on each access)
CREATE OR REPLACE VIEW active_posts AS
SELECT p.*, u.name AS author_name
FROM posts p
JOIN users u ON u.id = p.author_id
WHERE p.published = TRUE;

-- Materialized View (cached result — must refresh)
CREATE MATERIALIZED VIEW post_stats AS
SELECT
  DATE_TRUNC('month', created_at) AS month,
  COUNT(*) AS total_posts,
  COUNT(*) FILTER (WHERE published) AS published_posts
FROM posts
GROUP BY month
ORDER BY month;

-- Refresh materialized view
REFRESH MATERIALIZED VIEW CONCURRENTLY post_stats;
```

## Functions & Triggers

```sql
-- Function
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger (auto-update updated_at)
CREATE TRIGGER trigger_update_timestamp
  BEFORE UPDATE ON users
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();

-- Audit trigger
CREATE OR REPLACE FUNCTION audit_changes()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO audit_log (table_name, record_id, action, old_data, new_data, changed_at)
  VALUES (TG_TABLE_NAME, COALESCE(NEW.id, OLD.id), TG_OP,
          CASE WHEN TG_OP != 'INSERT' THEN to_jsonb(OLD) END,
          CASE WHEN TG_OP != 'DELETE' THEN to_jsonb(NEW) END,
          NOW());
  RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_audit
  AFTER INSERT OR UPDATE OR DELETE ON users
  FOR EACH ROW EXECUTE FUNCTION audit_changes();
```

## Transactions & Concurrency

```sql
BEGIN;
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;
  UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;

-- Savepoints
BEGIN;
  INSERT INTO users (email, name) VALUES ('test@example.com', 'Test');
  SAVEPOINT my_savepoint;
  INSERT INTO posts (title, author_id) VALUES ('Hello', 999);  -- might fail
  ROLLBACK TO my_savepoint;  -- undo just the posts insert
COMMIT;

-- Advisory locks
SELECT pg_advisory_lock(42);
SELECT pg_advisory_xact_lock(42);   -- auto-release at end of transaction
SELECT pg_try_advisory_lock(42);    -- non-blocking

-- Row-level locking
SELECT * FROM orders WHERE id = 1 FOR UPDATE;
SELECT * FROM orders WHERE id = 1 FOR UPDATE SKIP LOCKED;  -- skip locked rows
SELECT * FROM orders WHERE id = 1 FOR UPDATE NOWAIT;       -- error if locked
```

## Performance

```sql
-- EXPLAIN ANALYZE
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM users WHERE email = 'alice@example.com';

-- Common EXPLAIN outputs:
-- Seq Scan         → full table scan (add index!)
-- Index Scan       → using index (good)
-- Index Only Scan  → using covering index (best)
-- Bitmap Scan      → index + heap (medium)
-- Hash Join        → join via hash table
-- Nested Loop      → join via nested iteration

-- Vacuuming
VACUUM ANALYZE users;            -- reclaim space + update statistics
VACUUM (VERBOSE) users;          -- with progress info

-- Table statistics
SELECT relname, n_live_tup, n_dead_tup, last_vacuum, last_analyze
FROM pg_stat_user_tables WHERE relname = 'users';
```

## Node.js Integration

```ts
// With pg (node-postgres)
import pg from 'pg';
const pool = new pg.Pool({ connectionString: process.env.DATABASE_URL });

const { rows } = await pool.query('SELECT * FROM users WHERE id = $1', [userId]);

// Parameterized query (ALWAYS use — prevent SQL injection)
const { rows } = await pool.query(
  'INSERT INTO users (email, name) VALUES ($1, $2) RETURNING *',
  ['alice@example.com', 'Alice']
);

// Transaction
const client = await pool.connect();
try {
  await client.query('BEGIN');
  await client.query('UPDATE accounts SET balance = balance - $1 WHERE id = $2', [100, 1]);
  await client.query('UPDATE accounts SET balance = balance + $1 WHERE id = $2', [100, 2]);
  await client.query('COMMIT');
} catch (e) {
  await client.query('ROLLBACK');
  throw e;
} finally {
  client.release();
}

// Named parameterized query (good for reuse)
const insertUser = {
  name: 'insert-user',
  text: 'INSERT INTO users (email, name) VALUES ($1, $2) RETURNING *',
  values: ['alice@example.com', 'Alice'],
};
const { rows } = await pool.query(insertUser);
```

## Full-Text Search

```sql
-- Add search column
ALTER TABLE posts ADD COLUMN search_vector tsvector;

-- Populate
UPDATE posts SET search_vector =
  to_tsvector('english', COALESCE(title, '') || ' ' || COALESCE(content, ''));

-- Index for fast search
CREATE INDEX idx_posts_search ON posts USING GIN (search_vector);

-- Search query
SELECT title, ts_rank(search_vector, query) AS rank
FROM posts, to_tsquery('english', 'react & hooks') AS query
WHERE search_vector @@ query
ORDER BY rank DESC;

-- Auto-update trigger
CREATE TRIGGER posts_search_update
  BEFORE INSERT OR UPDATE ON posts
  FOR EACH ROW EXECUTE FUNCTION
    tsvector_update_trigger(search_vector, 'pg_catalog.english', title, content);

-- Highlight matches
SELECT ts_headline('english', content, to_tsquery('react & hooks'),
  'StartSel=<mark>, StopSel=</mark>, MaxWords=35') AS snippet
FROM posts;
```

## Row-Level Security (RLS)

```sql
-- Enable RLS
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Policy: users see only their own posts
CREATE POLICY user_sees_own_posts ON posts
  FOR SELECT USING (author_id = current_setting('app.user_id')::bigint);

-- Policy: admins see all
CREATE POLICY admin_all_posts ON posts
  FOR ALL USING (current_setting('app.user_role') = 'admin');

-- Policy: users can only insert their own
CREATE POLICY user_insert_own ON posts
  FOR INSERT WITH CHECK (author_id = current_setting('app.user_id')::bigint);

-- Set user context (from app server)
SET app.user_id = '42';
SET app.user_role = 'user';

-- Force RLS for table owner too
ALTER TABLE posts FORCE ROW LEVEL SECURITY;
```

## Partitioning

```sql
-- Range partitioning (by date)
CREATE TABLE events (
  id         BIGINT GENERATED ALWAYS AS IDENTITY,
  event_type TEXT NOT NULL,
  payload    JSONB,
  created_at TIMESTAMPTZ NOT NULL
) PARTITION BY RANGE (created_at);

CREATE TABLE events_2025 PARTITION OF events
  FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
CREATE TABLE events_2026 PARTITION OF events
  FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');

-- List partitioning
CREATE TABLE orders (
  id     BIGINT GENERATED ALWAYS AS IDENTITY,
  region TEXT NOT NULL,
  amount NUMERIC
) PARTITION BY LIST (region);

CREATE TABLE orders_us PARTITION OF orders FOR VALUES IN ('us-east', 'us-west');
CREATE TABLE orders_eu PARTITION OF orders FOR VALUES IN ('eu-west', 'eu-central');

-- Default partition (catch-all)
CREATE TABLE orders_other PARTITION OF orders DEFAULT;
```

## Extensions

```sql
-- List installed extensions
SELECT * FROM pg_available_extensions WHERE installed_version IS NOT NULL;

-- Popular extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";     -- uuid_generate_v4()
CREATE EXTENSION IF NOT EXISTS "pg_trgm";       -- trigram similarity search
CREATE EXTENSION IF NOT EXISTS "citext";         -- case-insensitive text
CREATE EXTENSION IF NOT EXISTS "hstore";         -- key-value pairs
CREATE EXTENSION IF NOT EXISTS "pgcrypto";       -- gen_random_uuid(), crypt()

-- pg_trgm: fuzzy text search
CREATE INDEX idx_users_name_trgm ON users USING GIN (name gin_trgm_ops);
SELECT * FROM users WHERE name % 'alce';  -- typo-tolerant search
SELECT * FROM users ORDER BY similarity(name, 'alce') DESC LIMIT 5;
```

## Gotchas

⚠️ **`TIMESTAMPTZ`**: Always use over `TIMESTAMP` — stores UTC, converts to session timezone.

⚠️ **`JSONB` over `JSON`**: JSONB is binary, indexable, faster. JSON preserves formatting only.

⚠️ **`GENERATED ALWAYS AS IDENTITY`**: Preferred over `SERIAL` (SQL standard, more control).

⚠️ **`$1, $2` parameterized queries**: NEVER concatenate user input into SQL strings.

⚠️ **Connection pooling**: Use `pg.Pool`, not `pg.Client` — handles reconnection, limits.

⚠️ **`ON CONFLICT DO UPDATE`**: PostgreSQL's upsert. Use `EXCLUDED` to reference new values.

⚠️ **`RETURNING *`**: Get affected rows back from INSERT/UPDATE/DELETE.

⚠️ **Partial indexes**: Use `WHERE` clause on index — smaller size, faster for filtered queries.

⚠️ **`EXPLAIN ANALYZE`**: Always use to check query plans. Watch for `Seq Scan` on large tables.

⚠️ **Materialized views**: Must `REFRESH` manually — not auto-updated. Use `CONCURRENTLY` to avoid locks.
