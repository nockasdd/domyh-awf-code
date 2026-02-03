---
name: sql
detect: ["*.sql", "migrations/*.sql", "*.pgsql"]
version: "6.0.0"
category: database
tier: 1
---

# SQL Patterns — DOMYH Awesome Code v5.5

> **Version**: PostgreSQL 16+, MySQL 8.4+
> **Focus**: Query optimization, migrations, performance
> **Philosophy**: Declarative, set-based thinking

---

## 🎯 When to Use This Skill

Use for: Database queries, data analysis, migrations, reporting.
**NOT for**: Application logic (→ go/python), UI (→ react).

---

## 📦 Database Comparison

| Feature      | PostgreSQL   | MySQL        | SQLite      |
| ------------ | ------------ | ------------ | ----------- |
| JSON support | JSONB 🏆     | JSON         | JSON1 ext   |
| Full-text    | Built-in     | Full-text    | FTS5        |
| CTEs         | Recursive    | Recursive    | Recursive   |
| Window funcs | Full         | Full         | Basic       |
| UPSERT       | ON CONFLICT  | ON DUPLICATE | ON CONFLICT |
| Best for     | Complex apps | Web apps     | Embedded    |

---

## 🔄 Query Patterns

### Modern SELECT

```sql
-- ✅ Use CTEs for readability
WITH active_orders AS (
  SELECT
    user_id,
    COUNT(*) AS order_count,
    SUM(total) AS total_spent
  FROM orders
  WHERE status = 'completed'
    AND created_at >= CURRENT_DATE - INTERVAL '30 days'
  GROUP BY user_id
),
user_ranks AS (
  SELECT
    *,
    RANK() OVER (ORDER BY total_spent DESC) AS spending_rank,
    PERCENT_RANK() OVER (ORDER BY total_spent) AS percentile
  FROM active_orders
)
SELECT
  u.id,
  u.name,
  u.email,
  ur.order_count,
  ur.total_spent,
  ur.spending_rank
FROM users u
JOIN user_ranks ur ON u.id = ur.user_id
WHERE ur.percentile >= 0.9  -- Top 10%
ORDER BY ur.spending_rank;
```

### Window Functions

```sql
-- Running totals
SELECT
  date,
  amount,
  SUM(amount) OVER (ORDER BY date) AS running_total,
  AVG(amount) OVER (
    ORDER BY date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) AS moving_avg_7d
FROM daily_sales;

-- Ranking within groups
SELECT
  department,
  employee_name,
  salary,
  ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rank,
  salary - LAG(salary) OVER (PARTITION BY department ORDER BY salary DESC) AS gap_to_higher
FROM employees;

-- Lead/Lag for comparisons
SELECT
  month,
  revenue,
  LAG(revenue, 1) OVER (ORDER BY month) AS prev_month,
  revenue - LAG(revenue, 1) OVER (ORDER BY month) AS growth,
  ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month)) /
        LAG(revenue) OVER (ORDER BY month), 2) AS growth_pct
FROM monthly_revenue;
```

### Recursive CTEs

```sql
-- Hierarchical data (org chart)
WITH RECURSIVE org_tree AS (
  -- Base case: top-level managers
  SELECT
    id,
    name,
    manager_id,
    1 AS level,
    ARRAY[id] AS path
  FROM employees
  WHERE manager_id IS NULL

  UNION ALL

  -- Recursive case: subordinates
  SELECT
    e.id,
    e.name,
    e.manager_id,
    ot.level + 1,
    ot.path || e.id
  FROM employees e
  JOIN org_tree ot ON e.manager_id = ot.id
  WHERE NOT e.id = ANY(ot.path)  -- Prevent cycles
)
SELECT
  REPEAT('  ', level - 1) || name AS hierarchy,
  level
FROM org_tree
ORDER BY path;
```

---

## ⚡ Performance Optimization

### Index Strategy

```sql
-- ✅ Create indexes for common queries
CREATE INDEX CONCURRENTLY idx_orders_user_status
ON orders (user_id, status)
WHERE status != 'cancelled';  -- Partial index

-- ✅ Covering index (includes all needed columns)
CREATE INDEX idx_orders_covering
ON orders (user_id, created_at)
INCLUDE (total, status);

-- ✅ GIN index for JSONB
CREATE INDEX idx_products_attrs
ON products USING GIN (attributes jsonb_path_ops);

-- ✅ Full-text search index
CREATE INDEX idx_posts_search
ON posts USING GIN (to_tsvector('english', title || ' ' || body));
```

### Query Analysis

```sql
-- Always check query plans
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM orders WHERE user_id = 123;

-- Key metrics to watch:
-- - Seq Scan on large tables → Need index
-- - Nested Loop with high row count → Consider hash join
-- - Buffers: shared hit vs read → Cache efficiency
```

### Batch Operations

```sql
-- ✅ Batch inserts
INSERT INTO logs (user_id, action, created_at)
SELECT
  user_id,
  'migration_complete',
  NOW()
FROM users
WHERE migrated = false
ON CONFLICT (user_id, action) DO NOTHING;

-- ✅ Batch updates with LIMIT
WITH to_update AS (
  SELECT id
  FROM orders
  WHERE status = 'pending'
    AND created_at < NOW() - INTERVAL '7 days'
  LIMIT 1000
  FOR UPDATE SKIP LOCKED
)
UPDATE orders
SET status = 'expired'
WHERE id IN (SELECT id FROM to_update);
```

---

## 🔒 JSONB Patterns (PostgreSQL)

```sql
-- Query JSONB
SELECT * FROM products
WHERE attributes->>'color' = 'red'
  AND (attributes->>'price')::numeric < 100;

-- Update JSONB field
UPDATE products
SET attributes = jsonb_set(
  attributes,
  '{discount}',
  '"20%"'::jsonb
)
WHERE id = 1;

-- Append to JSONB array
UPDATE products
SET attributes = jsonb_set(
  attributes,
  '{tags}',
  (attributes->'tags') || '["sale"]'::jsonb
)
WHERE id = 1;

-- Aggregate to JSONB
SELECT jsonb_agg(
  jsonb_build_object(
    'id', id,
    'name', name,
    'total', total
  ) ORDER BY total DESC
) AS top_customers
FROM customers
LIMIT 10;
```

---

## 📦 Migration Patterns

```sql
-- ✅ Add column with default (non-blocking in PG 11+)
ALTER TABLE users
ADD COLUMN preferences JSONB DEFAULT '{}'::jsonb;

-- ✅ Create index concurrently (non-blocking)
CREATE INDEX CONCURRENTLY idx_users_email
ON users (email);

-- ✅ Rename with backward compatibility
ALTER TABLE old_orders RENAME TO orders_archive;
CREATE VIEW old_orders AS SELECT * FROM orders_archive;

-- ✅ Safe column removal
-- Step 1: Stop writing
-- Step 2: Deploy code that doesn't read
-- Step 3: Drop column
ALTER TABLE users DROP COLUMN deprecated_field;
```

---

## 🧪 Testing Queries

```sql
-- Test with transaction rollback
BEGIN;

-- Your test INSERT/UPDATE
INSERT INTO orders (user_id, total) VALUES (1, 99.99);

-- Verify
SELECT * FROM orders WHERE user_id = 1;

-- Always rollback in tests
ROLLBACK;
```

---

## ✅ Production Checklist

### Performance

- [ ] EXPLAIN ANALYZE on all queries
- [ ] Proper indexes exist
- [ ] No SELECT \* in production
- [ ] Pagination with keyset (not OFFSET)

### Safety

- [ ] Transactions for multi-statement ops
- [ ] ON CONFLICT for upserts
- [ ] Parameterized queries (no injection)
- [ ] Timeouts configured

### Monitoring

- [ ] Slow query log enabled
- [ ] pg_stat_statements for analysis
- [ ] Connection pool limits

---

_DOMYH Awesome Code v6.0.0 • SQL PostgreSQL 16+_
