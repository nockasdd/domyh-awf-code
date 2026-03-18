# SQL — Advanced Patterns

## Table of Contents

- [Window Functions](#window-functions)
- [CTEs & Recursive Queries](#ctes--recursive-queries)
- [Indexing Strategy](#indexing-strategy)
- [Query Optimization](#query-optimization)
- [JSON Operations](#json-operations)

---

## Window Functions

```sql
-- Running total + rank
SELECT
  id, amount, created_at,
  SUM(amount) OVER (ORDER BY created_at) AS running_total,
  ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) AS rn,
  RANK() OVER (ORDER BY amount DESC) AS amount_rank,
  LAG(amount) OVER (ORDER BY created_at) AS prev_amount,
  amount - LAG(amount) OVER (ORDER BY created_at) AS diff
FROM orders;

-- Moving average (last 7 days)
SELECT
  date, revenue,
  AVG(revenue) OVER (
    ORDER BY date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) AS moving_avg_7d
FROM daily_stats;

-- Percentile
SELECT
  name, salary,
  PERCENT_RANK() OVER (ORDER BY salary) AS percentile,
  NTILE(4) OVER (ORDER BY salary) AS quartile
FROM employees;
```

---

## CTEs & Recursive Queries

```sql
-- Recursive: org hierarchy
WITH RECURSIVE org_tree AS (
  SELECT id, name, manager_id, 0 AS depth
  FROM employees WHERE manager_id IS NULL

  UNION ALL

  SELECT e.id, e.name, e.manager_id, t.depth + 1
  FROM employees e
  JOIN org_tree t ON e.manager_id = t.id
  WHERE t.depth < 10  -- Safety limit
)
SELECT * FROM org_tree ORDER BY depth, name;

-- CTE for readability
WITH
  active_users AS (
    SELECT * FROM users WHERE status = 'active' AND last_login > NOW() - INTERVAL '30 days'
  ),
  user_orders AS (
    SELECT user_id, COUNT(*) as order_count, SUM(total) as total_spent
    FROM orders
    WHERE created_at > NOW() - INTERVAL '90 days'
    GROUP BY user_id
  )
SELECT u.name, u.email, COALESCE(o.order_count, 0), COALESCE(o.total_spent, 0)
FROM active_users u
LEFT JOIN user_orders o ON u.id = o.user_id
ORDER BY o.total_spent DESC NULLS LAST;
```

---

## Indexing Strategy

```yaml
index_types:
  btree: "Default. Good for: =, <, >, BETWEEN, ORDER BY"
  hash: "Only for equality (=). Faster than btree for exact match"
  gin: "Inverted index. Good for: JSONB, arrays, full-text search"
  gist: "Geometric/range types. Good for: PostGIS, @>, &&"
  brin: "Block range. Good for: large tables with natural ordering (timestamps)"

rules:
  - "Index columns used in WHERE, JOIN, ORDER BY"
  - "Composite index: most selective column first"
  - "Partial index for common filters: WHERE status = 'active'"
  - "Covering index (INCLUDE) to avoid table lookup"
  - "Never index low-cardinality columns alone (boolean, status)"

examples: |
  -- Composite index
  CREATE INDEX idx_orders_user_date ON orders(user_id, created_at DESC);

  -- Partial index
  CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';

  -- Covering index (PostgreSQL)
  CREATE INDEX idx_orders_cover ON orders(user_id) INCLUDE (total, status);

  -- GIN for JSONB
  CREATE INDEX idx_meta ON products USING GIN (metadata jsonb_path_ops);
```

---

## Query Optimization

```sql
-- EXPLAIN ANALYZE (always check)
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM orders WHERE user_id = 123 ORDER BY created_at DESC LIMIT 20;

-- ❌ Slow: function on indexed column
SELECT * FROM users WHERE LOWER(email) = 'test@example.com';
-- ✅ Fast: expression index
CREATE INDEX idx_email_lower ON users(LOWER(email));

-- ❌ Slow: SELECT *
SELECT * FROM orders JOIN users ON orders.user_id = users.id;
-- ✅ Fast: select only needed columns
SELECT o.id, o.total, u.name FROM orders o JOIN users u ON o.user_id = u.id;

-- Batch insert (PostgreSQL)
INSERT INTO events (type, data, created_at)
SELECT unnest($1::text[]), unnest($2::jsonb[]), NOW();
```

---

## JSON Operations

```sql
-- PostgreSQL JSONB
SELECT
  data->>'name' AS name,           -- Text extraction
  data->'address'->>'city' AS city, -- Nested
  data @> '{"role": "admin"}',     -- Containment
  jsonb_array_length(data->'tags') -- Array length
FROM users
WHERE data @> '{"status": "active"}'
  AND data->'tags' ? 'premium';    -- Array contains

-- JSON aggregation
SELECT
  department,
  jsonb_agg(jsonb_build_object('name', name, 'salary', salary)) AS employees
FROM employees
GROUP BY department;
```

---
