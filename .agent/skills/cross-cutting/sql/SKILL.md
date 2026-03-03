---
name: sql
description: "SQL patterns for queries, optimization, and database operations. Use when writing SQL or working with relational databases."
detect: ["*.sql", "migrations/*.sql", "*.pgsql"]
category: database
tier: 1
---

# SQL Patterns — DOMYH Awesome Code

> **Version**: PostgreSQL 18, MySQL 8.4+
> **Focus**: Query optimization, migrations, performance
> **Philosophy**: Declarative, set-based thinking

---

## 🎯 When to Use This Skill

Use for: Database queries, data analysis, migrations, reporting.
**NOT for**: Application logic (→ go/python), UI (→ react).

---

## 📦 What's New in PostgreSQL 18 (2025)

| Feature                       | Description                     |
| ----------------------------- | ------------------------------- |
| **Async I/O (AIO)**           | Revolutionary performance boost |
| **uuidv7()**                  | Timestamp-ordered UUIDs         |
| **Virtual Generated Columns** | Computed on read                |
| **Skip Scan**                 | B-tree optimization             |
| **pg_stat_io**                | I/O monitoring                  |
| **NOT NULL/FK enhancements**  | Data integrity                  |

---

## 📦 Database Comparison

| Feature   | PostgreSQL 18  | MySQL 8.4+ | SQLite    |
| --------- | -------------- | ---------- | --------- |
| Async I/O | ✅ AIO 🏆      | Partial    | ❌        |
| JSON      | JSONB 🏆       | JSON       | JSON1     |
| UUIDv7    | ✅ Built-in 🏆 | Plugin     | ❌        |
| CTEs      | Recursive      | Recursive  | Recursive |
| Window    | Full           | Full       | Basic     |
| Best for  | Complex apps   | Web apps   | Embedded  |

---

## 🔄 Query Patterns

### Modern SELECT with CTEs

```sql
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
  u.id, u.name, u.email,
  ur.order_count, ur.total_spent, ur.spending_rank
FROM users u
JOIN user_ranks ur ON u.id = ur.user_id
WHERE ur.percentile >= 0.9
ORDER BY ur.spending_rank;
```

### 🆕 UUIDv7 (PostgreSQL 18)

```sql
-- Timestamp-ordered UUIDs (better for indexing)
CREATE TABLE orders (
  id UUID PRIMARY KEY DEFAULT uuidv7(),
  user_id UUID NOT NULL,
  total DECIMAL(10,2),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- UUIDv7 sorts chronologically!
SELECT * FROM orders ORDER BY id;
```

### 🆕 Virtual Generated Columns

```sql
-- Computed on read (no storage)
ALTER TABLE users
ADD COLUMN full_name TEXT GENERATED ALWAYS AS (first_name || ' ' || last_name) VIRTUAL;

-- vs STORED (computed on write)
ALTER TABLE orders
ADD COLUMN tax DECIMAL GENERATED ALWAYS AS (total * 0.1) STORED;
```

### Window Functions

```sql
-- Running totals with moving average
SELECT
  date,
  amount,
  SUM(amount) OVER (ORDER BY date) AS running_total,
  AVG(amount) OVER (
    ORDER BY date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) AS moving_avg_7d
FROM daily_sales;

-- Ranking with gap detection
SELECT
  department,
  employee_name,
  salary,
  ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rank,
  salary - LAG(salary) OVER (PARTITION BY department ORDER BY salary DESC) AS gap
FROM employees;
```

### Recursive CTEs

```sql
WITH RECURSIVE org_tree AS (
  SELECT id, name, manager_id, 1 AS level, ARRAY[id] AS path
  FROM employees
  WHERE manager_id IS NULL

  UNION ALL

  SELECT e.id, e.name, e.manager_id, ot.level + 1, ot.path || e.id
  FROM employees e
  JOIN org_tree ot ON e.manager_id = ot.id
  WHERE NOT e.id = ANY(ot.path)
)
SELECT REPEAT('  ', level - 1) || name AS hierarchy, level
FROM org_tree
ORDER BY path;
```

---

## ⚡ Performance Optimization

### Index Strategy

```sql
-- Partial index (filtered)
CREATE INDEX CONCURRENTLY idx_orders_active
ON orders (user_id, status)
WHERE status != 'cancelled';

-- Covering index (includes columns)
CREATE INDEX idx_orders_covering
ON orders (user_id, created_at)
INCLUDE (total, status);

-- GIN for JSONB
CREATE INDEX idx_products_attrs
ON products USING GIN (attributes jsonb_path_ops);

-- Full-text search
CREATE INDEX idx_posts_search
ON posts USING GIN (to_tsvector('english', title || ' ' || body));
```

### 🆕 pg_stat_io Monitoring (PostgreSQL 18)

```sql
-- I/O statistics per backend type
SELECT
  backend_type,
  object,
  context,
  reads,
  writes,
  extends,
  fsyncs
FROM pg_stat_io
WHERE reads > 0 OR writes > 0;
```

### Query Analysis

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM orders WHERE user_id = 123;

-- Watch for:
-- - Seq Scan on large tables → Need index
-- - Nested Loop with high rows → Consider hash join
-- - Buffers: shared hit vs read → Cache efficiency
```

---

## 🔒 JSONB Patterns

```sql
-- Query JSONB
SELECT * FROM products
WHERE attributes->>'color' = 'red'
  AND (attributes->>'price')::numeric < 100;

-- Update JSONB field
UPDATE products
SET attributes = jsonb_set(
  attributes, '{discount}', '"20%"'::jsonb
)
WHERE id = 1;

-- Aggregate to JSONB
SELECT jsonb_agg(
  jsonb_build_object('id', id, 'name', name, 'total', total)
  ORDER BY total DESC
) AS top_customers
FROM customers
LIMIT 10;
```

---

## 📦 Migration Patterns

```sql
-- Add column with default (non-blocking in PG 11+)
ALTER TABLE users
ADD COLUMN preferences JSONB DEFAULT '{}'::jsonb;

-- Create index concurrently (non-blocking)
CREATE INDEX CONCURRENTLY idx_users_email
ON users (email);

-- Safe column removal (3-step)
-- Step 1: Stop writing
-- Step 2: Deploy code that doesn't read
-- Step 3: Drop column
ALTER TABLE users DROP COLUMN deprecated_field;
```

---

## ✅ Production Checklist

### Performance

- [ ] EXPLAIN ANALYZE on all queries
- [ ] Proper indexes exist
- [ ] No SELECT \* in production
- [ ] Pagination with keyset (not OFFSET)
- [ ] pg_stat_io monitored

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

## 🔌 HSA Integration

Data powered by HSA BM25 search engine:

| Domain    | Query Examples                      |
| --------- | ----------------------------------- |
| Query     | "window function ranking partition" |
| Index     | "partial covering GIN index"        |
| PG18      | "uuidv7 virtual generated columns"  |
| Migration | "safe column removal ALTER TABLE"   |

---
