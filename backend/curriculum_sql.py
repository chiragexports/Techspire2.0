# -*- coding: utf-8 -*-
"""
Curriculum definition for Master SQL & Relational Database Architecture.
Comprehensive 10-module curriculum covering relational database theory, SQL fundamentals,
advanced analytics, query tuning, indexing, ACID transactions, and database administration.
"""

SQL_COURSE = {
    "title": "Master SQL & Relational Database Architecture",
    "slug": "master-sql-relational-database-architecture",
    "description": "Architect robust relational databases, master complex queries, window functions, query execution planning, indexes, and transaction isolation.",
    "category": "database",
    "level": "intermediate",
    "duration_weeks": 10,
    "thumbnail_gradient": "from-cyan-600 via-blue-700 to-indigo-900",
    "is_featured": True,
    "modules": [
        {
            "order": 1,
            "title": "Relational Model & Relational Algebra",
            "description": "Foundations of relational database management systems, relational algebra, and ANSI SQL standards.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Database Architecture & The Relational Engine",
                    "description": "Explore client-server database architecture, query parser, planner, optimizer, and storage engines.",
                    "duration_minutes": 35,
                    "content": """# Database Architecture & The Relational Engine

Modern Relational Database Management Systems (RDBMS) like PostgreSQL, MySQL, and Oracle separate logical query processing from physical storage management.

## 1. Core Architectural Components

1. **Connection Manager / Listener**: Handles incoming TCP connections, authentication, and session pooling.
2. **Parser & Lexer**: Converts SQL text strings into Abstract Syntax Trees (AST) and validates syntax.
3. **Query Rewriter / Resolver**: Validates table/column identifiers against system catalogs, applies view definitions, and checks user permissions.
4. **Query Optimizer / Planner**: Evaluates multiple execution trees, uses table statistics (histograms), and calculates cost-based execution plans.
5. **Execution Engine**: Executes physical operators (Seq Scan, Index Scan, Hash Join, Merge Join) using volcano/iterator processing.
6. **Storage Engine / Buffer Manager**: Manages memory cache (Buffer Pool / Shared Buffers), Write-Ahead Logging (WAL), and disk block I/O.

```sql
-- Checking the database engine version and active connection parameters
SELECT version();
SHOW work_mem;
SHOW shared_buffers;
```

## Key Takeaways
- SQL is a declarative language: you specify *what* data you need, and the query optimizer determines *how* to retrieve it efficiently.
- Storage engines rely on memory buffer pools and Write-Ahead Logging (WAL) to guarantee durability and high throughput."""
                },
                {
                    "order": 2,
                    "title": "Relational Algebra Foundations",
                    "description": "Map relational algebra operators (Selection, Projection, Cartesian Product, Join) to SQL statements.",
                    "duration_minutes": 30,
                    "content": """# Relational Algebra Foundations

Relational Algebra is the formal mathematical foundation underpinning SQL queries.

## 1. Fundamental Relational Operators

- **Selection (σ)**: Filters rows satisfying a predicate $\sigma_{\\text{age} > 21}(R) \\rightarrow$ `SELECT * FROM R WHERE age > 21`.
- **Projection (π)**: Extracts specific columns $\pi_{\\text{id, name}}(R) \\rightarrow$ `SELECT id, name FROM R`.
- **Cartesian Product (×)**: Combines every tuple from $R$ with every tuple from $S \\rightarrow$ `SELECT * FROM R CROSS JOIN S`.
- **Set Difference (−)**: Tuples in $R$ not in $S \\rightarrow$ `SELECT * FROM R EXCEPT SELECT * FROM S`.
- **Union (∪)**: Set of all distinct tuples in $R$ or $S \\rightarrow$ `SELECT * FROM R UNION SELECT * FROM S`.

```sql
-- Relational Selection and Projection Example
SELECT 
    student_id, 
    first_name, 
    gpa
FROM students
WHERE gpa >= 3.8 AND status = 'active';
```

## Key Takeaways
- Every SQL `SELECT` statement corresponds to a composition of relational algebra operations.
- Algebraic query transformation rules allow optimizers to push selections down before joins to minimize memory consumption."""
                }
            ]
        },
        {
            "order": 2,
            "title": "Data Definition Language (DDL) & Normalization",
            "description": "Schema definition, constraints, primary/foreign keys, and 1NF through BCNF normalization.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Table Creation, Data Types & Integrity Constraints",
                    "description": "Design normalized tables with rigorous constraints (NOT NULL, CHECK, UNIQUE, FOREIGN KEY).",
                    "duration_minutes": 40,
                    "content": """# Table Creation, Data Types & Integrity Constraints

DDL establishes the structural integrity of your schema through strong typing and declarative integrity constraints.

```sql
-- Creating an e-commerce schema with strict integrity rules
CREATE TABLE categories (
    category_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    product_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    category_id INT NOT NULL REFERENCES categories(category_id) ON DELETE RESTRICT,
    sku VARCHAR(64) NOT NULL UNIQUE,
    title VARCHAR(255) NOT NULL,
    price_cents INT NOT NULL CHECK (price_cents >= 0),
    stock_quantity INT NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    order_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_email VARCHAR(255) NOT NULL,
    total_amount NUMERIC(12, 2) NOT NULL CHECK (total_amount >= 0),
    order_status VARCHAR(32) NOT NULL CHECK (order_status IN ('pending', 'paid', 'shipped', 'cancelled')),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
```

## Key Takeaways
- Use integer/cents representation or `NUMERIC`/`DECIMAL` for currency to prevent floating-point rounding errors.
- Declarative `CHECK` constraints prevent corrupted states directly at the database engine level."""
                },
                {
                    "order": 2,
                    "title": "Database Normalization (1NF to BCNF)",
                    "description": "Eliminate data anomalies and redundancies using systematic normalization techniques.",
                    "duration_minutes": 45,
                    "content": """# Database Normalization (1NF to BCNF)

Normalization decomposes tables to eliminate update, insertion, and deletion anomalies while maintaining data lossless-join decomposition.

## Normal Forms Summary

1. **1NF (First Normal Form)**:
   - Each column contains atomic (indivisible) values.
   - Each record has a unique identifier (Primary Key).
   - No repeating groups or comma-separated lists.

2. **2NF (Second Normal Form)**:
   - Must satisfy 1NF.
   - No partial functional dependencies: all non-key attributes must depend on the *entire* composite primary key.

3. **3NF (Third Normal Form)**:
   - Must satisfy 2NF.
   - No transitive dependencies: non-key attributes must not depend on other non-key attributes ($X \\rightarrow Y, Y \\rightarrow Z$).

4. **BCNF (Boyce-Codd Normal Form)**:
   - For every functional dependency $X \\rightarrow Y$, $X$ must be a superkey.

## Key Takeaways
- OLTP (Transactional) systems thrive on 3NF/BCNF to prevent anomaly bugs.
- OLAP (Analytical) data warehouses often use denormalized Star or Snowflake schemas to optimize read throughput."""
                }
            ]
        },
        {
            "order": 3,
            "title": "Data Query Language (DQL): Filtering & Sorting",
            "description": "Master SQL SELECT statement execution order, pattern matching, null handling, and pagination.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Logical Query Processing Order",
                    "description": "Understand the exact order of clauses executed by the SQL engine.",
                    "duration_minutes": 35,
                    "content": """# Logical Query Processing Order

While SQL is written starting with `SELECT`, the database execution engine evaluates clauses in a strict logical order:

## Execution Sequence

1. `FROM` (including `JOIN` and `ON` evaluation)
2. `WHERE` (row-level filtering)
3. `GROUP BY` (aggregation grouping)
4. `HAVING` (group-level filtering)
5. `SELECT` (evaluating expressions and column projections)
6. `DISTINCT` (deduplicating rows)
7. `ORDER BY` (sorting output)
8. `LIMIT` / `OFFSET` (paging results)

```sql
SELECT 
    department_id,
    COUNT(*) AS total_employees,
    ROUND(AVG(salary), 2) AS avg_salary
FROM employees
WHERE is_active = TRUE
GROUP BY department_id
HAVING COUNT(*) > 5
ORDER BY avg_salary DESC
LIMIT 10;
```

## Key Takeaways
- You cannot refer to a column alias defined in `SELECT` inside the `WHERE` clause because `WHERE` runs before `SELECT`!
- `ORDER BY` runs after `SELECT`, which is why aliases are permitted in `ORDER BY`."""
                },
                {
                    "order": 2,
                    "title": "Three-Valued Logic & NULL Handling",
                    "description": "Master SQL NULL semantics, IS NULL, COALESCE, NULLIF, and boolean truth tables.",
                    "duration_minutes": 30,
                    "content": """# Three-Valued Logic & NULL Handling

SQL implements Three-Valued Logic: a boolean expression evaluates to `TRUE`, `FALSE`, or `UNKNOWN`.

## 1. Comparing with NULL

`NULL = NULL` is **NOT** `TRUE`; it evaluates to `UNKNOWN`!

```sql
-- Correct NULL checks
SELECT * FROM users WHERE phone_number IS NULL;
SELECT * FROM users WHERE phone_number IS NOT NULL;

-- Safe fallback using COALESCE
SELECT 
    user_id,
    COALESCE(display_name, username, 'Anonymous User') AS visible_name
FROM users;

-- NULLIF: returns NULL if arguments are equal (prevents division by zero)
SELECT 
    total_sales / NULLIF(total_orders, 0) AS average_order_value
FROM store_summaries;
```

## Key Takeaways
- Never use `= NULL` or `!= NULL`; always use `IS NULL` or `IS NOT NULL`.
- In `NOT IN (SELECT subquery)` clauses, if the subquery contains a single `NULL` value, the entire predicate evaluates to `UNKNOWN` and returns zero rows! Always use `NOT EXISTS` instead."""
                }
            ]
        },
        {
            "order": 4,
            "title": "Mastering Joins & Set Operations",
            "description": "Inner joins, outer joins, cross joins, self joins, and set operations (UNION, INTERSECT, EXCEPT).",
            "chapters": [
                {
                    "order": 1,
                    "title": "Inner, Left, Right & Full Outer Joins",
                    "description": "Synthesize multi-table relationships with precision joining strategies.",
                    "duration_minutes": 45,
                    "content": """# Inner, Left, Right & Full Outer Joins

Joins allow querying normalized relational models by connecting tables on matching predicate keys.

```sql
-- 1. INNER JOIN: Only records with matches in both tables
SELECT 
    c.customer_name,
    o.order_id,
    o.total_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;

-- 2. LEFT OUTER JOIN: All customers, with order data if present (or NULLs)
SELECT 
    c.customer_id,
    c.customer_name,
    o.order_id
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;

-- 3. FULL OUTER JOIN: All rows from both sides
SELECT 
    e.employee_name,
    d.department_name
FROM employees e
FULL OUTER JOIN departments d ON e.department_id = d.department_id;
```

## Join Algorithms Used by Engines
- **Nested Loop Join**: Ideal for small tables with indexed lookups.
- **Hash Join**: In-memory hash table on the smaller table, scanning the larger table.
- **Merge Join**: Both inputs sorted on the join key, merging in $O(N + M)$ time."""
                },
                {
                    "order": 2,
                    "title": "Self Joins & Hierarchical Tree Queries",
                    "description": "Query employee-manager hierarchies, parent-child taxonomies, and graph trees.",
                    "duration_minutes": 40,
                    "content": """# Self Joins & Hierarchical Tree Queries

A self-join joins a table to itself using distinct aliases to represent hierarchical or temporal relationships.

```sql
-- Self Join for Organizational Structure
SELECT 
    emp.employee_id,
    emp.full_name AS employee_name,
    emp.job_title,
    mgr.full_name AS manager_name
FROM employees emp
LEFT JOIN employees mgr ON emp.manager_id = mgr.employee_id;

-- Finding products in the same category (Pairs)
SELECT 
    p1.product_name AS product_a,
    p2.product_name AS product_b,
    p1.category_id
FROM products p1
INNER JOIN products p2 
    ON p1.category_id = p2.category_id 
    AND p1.product_id < p2.product_id;
```

## Key Takeaways
- Use `p1.id < p2.id` rather than `!=` to eliminate redundant reversed pairs and self-pairings."""
                }
            ]
        },
        {
            "order": 5,
            "title": "Aggregation, Grouping & Advanced Filtering",
            "description": "Aggregate functions (SUM, AVG, MIN, MAX, COUNT), GROUP BY, HAVING, and GROUPING SETS.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Aggregate Functions & The HAVING Clause",
                    "description": "Perform robust multi-dimensional summarization and conditional filtering.",
                    "duration_minutes": 40,
                    "content": """# Aggregate Functions & The HAVING Clause

Aggregate functions compute a single scalar value from a set of rows.

```sql
-- Comprehensive Sales Performance Analysis
SELECT 
    p.category_id,
    COUNT(oi.order_item_id) AS items_sold,
    SUM(oi.quantity * oi.unit_price) AS gross_revenue,
    ROUND(AVG(oi.unit_price), 2) AS avg_unit_price,
    MIN(oi.unit_price) AS min_price,
    MAX(oi.unit_price) AS max_price
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category_id
HAVING SUM(oi.quantity * oi.unit_price) > 50000
ORDER BY gross_revenue DESC;
```

## Conditional Aggregation (Filter Clause / CASE)
```sql
SELECT 
    department_id,
    COUNT(*) AS total_staff,
    COUNT(*) FILTER (WHERE salary > 100000) AS high_earners_pg,
    SUM(CASE WHEN gender = 'F' THEN 1 ELSE 0 END) AS female_staff
FROM employees
GROUP BY department_id;
```

## Key Takeaways
- `WHERE` filters rows *before* aggregation; `HAVING` filters groups *after* aggregation."""
                },
                {
                    "order": 2,
                    "title": "CUBE, ROLLUP & GROUPING SETS",
                    "description": "Generate multi-level subtotal reporting in a single query pass.",
                    "duration_minutes": 35,
                    "content": """# CUBE, ROLLUP & GROUPING SETS

Rather than combining multiple queries with `UNION ALL`, `GROUPING SETS` efficiently compute aggregations across multiple grouping dimensions.

```sql
-- Multi-tier Sales Reporting with ROLLUP
SELECT 
    COALESCE(region, 'All Regions') AS region,
    COALESCE(country, 'All Countries') AS country,
    SUM(sales_amount) AS total_sales
FROM sales
GROUP BY ROLLUP (region, country);

-- Explicit GROUPING SETS
SELECT 
    region,
    product_category,
    SUM(sales_amount) AS revenue
FROM sales
GROUP BY GROUPING SETS (
    (region, product_category),
    (region),
    (product_category),
    ()
);
```

## Key Takeaways
- `ROLLUP` produces hierarchical sub-totals (e.g. Year > Quarter > Month > Grand Total).
- `CUBE` produces all possible permutations of groupings ($2^N$)."""
                }
            ]
        },
        {
            "order": 6,
            "title": "Subqueries & Common Table Expressions (CTEs)",
            "description": "Scalar, correlated subqueries, EXISTS vs IN, and Recursive CTEs for graph traversal.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Correlated Subqueries & Predicate Evaluation",
                    "description": "Leverage scalar subqueries, correlated inner-references, and EXISTS vs IN performance.",
                    "duration_minutes": 40,
                    "content": """# Correlated Subqueries & Predicate Evaluation

A correlated subquery references columns from the outer query, evaluating once per outer candidate row.

```sql
-- Find employees who earn more than the average salary of their department
SELECT 
    e.employee_id,
    e.full_name,
    e.department_id,
    e.salary
FROM employees e
WHERE e.salary > (
    SELECT AVG(d.salary)
    FROM employees d
    WHERE d.department_id = e.department_id
);

-- Efficient EXISTS predicate vs IN
SELECT c.customer_id, c.customer_name
FROM customers c
WHERE EXISTS (
    SELECT 1 
    FROM orders o 
    WHERE o.customer_id = c.customer_id 
      AND o.order_date >= CURRENT_DATE - INTERVAL '30 days'
);
```

## Key Takeaways
- `EXISTS` terminates scanning immediately upon encountering the first matching record (early exit short-circuit), outperforming `IN` for large datasets."""
                },
                {
                    "order": 2,
                    "title": "Recursive CTEs & Graph Traversal",
                    "description": "Traverse tree hierarchies, bill-of-materials, and linked network graphs using WITH RECURSIVE.",
                    "duration_minutes": 45,
                    "content": """# Recursive CTEs & Graph Traversal

Recursive CTEs consist of an Anchor Query, a Recursive Union Member, and a Termination Condition.

```sql
-- Recursively traversing organizational hierarchy tree
WITH RECURSIVE OrgChart AS (
    -- 1. Anchor Member: Top-level CEO (manager_id IS NULL)
    SELECT 
        employee_id, 
        full_name, 
        manager_id, 
        1 AS depth_level,
        CAST(full_name AS TEXT) AS hierarchy_path
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- 2. Recursive Member: Direct reports
    SELECT 
        e.employee_id, 
        e.full_name, 
        e.manager_id, 
        o.depth_level + 1,
        o.hierarchy_path || ' -> ' || e.full_name
    FROM employees e
    INNER JOIN OrgChart o ON e.manager_id = o.employee_id
)
SELECT * FROM OrgChart ORDER BY depth_level, full_name;
```

## Key Takeaways
- Recursive CTEs enable graph and tree traversal in standard ANSI SQL without requiring procedural code or external graph databases."""
                }
            ]
        },
        {
            "order": 7,
            "title": "Window Functions & Advanced Analytics",
            "description": "ROW_NUMBER, RANK, DENSE_RANK, NTILE, LAG, LEAD, and sliding window frames.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Ranking & Distribution Functions",
                    "description": "Partition data and compute analytical rankings without collapsing rows.",
                    "duration_minutes": 45,
                    "content": """# Ranking & Distribution Functions

Window functions operate on a set of rows (a partition) and return a scalar value for each individual row without collapsing the result set.

```sql
-- Top 3 highest earning employees per department
WITH RankedStaff AS (
    SELECT 
        employee_id,
        full_name,
        department_id,
        salary,
        ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS row_num,
        RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rank_val,
        DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS dense_rank_val,
        NTILE(4) OVER (ORDER BY salary DESC) AS salary_quartile
    FROM employees
)
SELECT * 
FROM RankedStaff 
WHERE row_num <= 3;
```

## Key Differences Between Ranking Functions
- `ROW_NUMBER()`: Always returns unique sequential integers (1, 2, 3, 4).
- `RANK()`: Assigns identical ranks to tied values, skipping subsequent positions (1, 2, 2, 4).
- `DENSE_RANK()`: Assigns identical ranks to tied values without gaps (1, 2, 2, 3)."""
                },
                {
                    "order": 2,
                    "title": "Offset Functions & Moving Averages (Sliding Frames)",
                    "description": "Calculate Month-over-Month growth, churn rates, and 7-day moving averages.",
                    "duration_minutes": 45,
                    "content": """# Offset Functions & Moving Averages (Sliding Frames)

```sql
-- Month-over-Month Revenue Growth with LAG()
SELECT 
    date_trunc('month', order_date)::DATE AS sales_month,
    SUM(total_amount) AS current_month_revenue,
    LAG(SUM(total_amount), 1) OVER (
        ORDER BY date_trunc('month', order_date)
    ) AS prev_month_revenue,
    ROUND(
        (SUM(total_amount) - LAG(SUM(total_amount), 1) OVER (ORDER BY date_trunc('month', order_date)))
        / LAG(SUM(total_amount), 1) OVER (ORDER BY date_trunc('month', order_date)) * 100, 2
    ) AS mom_growth_pct
FROM orders
GROUP BY date_trunc('month', order_date);

-- 7-Day Rolling Moving Average
SELECT 
    recorded_date,
    daily_revenue,
    ROUND(AVG(daily_revenue) OVER (
        ORDER BY recorded_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ), 2) AS rolling_7day_avg
FROM daily_sales_metrics;
```

## Key Takeaways
- `ROWS BETWEEN N PRECEDING AND CURRENT ROW` defines physical row-based window boundaries.
- `RANGE BETWEEN` defines value-based logical interval boundaries."""
                }
            ]
        },
        {
            "order": 8,
            "title": "Data Manipulation (DML) & ACID Transactions",
            "description": "INSERT ON CONFLICT (Upsert), RETURNING, Transaction Isolation levels, and Deadlocks.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Advanced DML & Atomic UPSERTs",
                    "description": "Perform idempotent data ingestion with INSERT ON CONFLICT DO UPDATE.",
                    "duration_minutes": 35,
                    "content": """# Advanced DML & Atomic UPSERTs

Modern DML enables atomic upserting and pipeline chaining using `RETURNING`.

```sql
-- Atomic PostgreSQL Upsert (Merge Pattern)
INSERT INTO product_inventory (sku, warehouse_id, quantity, last_restocked_at)
VALUES ('SKU-10023', 1, 50, CURRENT_TIMESTAMP)
ON CONFLICT (sku, warehouse_id) 
DO UPDATE SET 
    quantity = product_inventory.quantity + EXCLUDED.quantity,
    last_restocked_at = EXCLUDED.last_restocked_at
RETURNING inventory_id, sku, quantity;

-- Modifying data using a CTE pipeline
WITH archived_orders AS (
    DELETE FROM orders
    WHERE order_status = 'cancelled' 
      AND created_at < CURRENT_DATE - INTERVAL '1 year'
    RETURNING *
)
INSERT INTO order_audit_archive
SELECT * FROM archived_orders;
```

## Key Takeaways
- `ON CONFLICT` prevents race conditions and eliminates client-side SELECT-then-INSERT anti-patterns."""
                },
                {
                    "order": 2,
                    "title": "ACID Properties & Transaction Isolation Levels",
                    "description": "Analyze Dirty Reads, Non-Repeatable Reads, Phantom Reads, and Serialization Anomalies.",
                    "duration_minutes": 50,
                    "content": """# ACID Properties & Transaction Isolation Levels

ACID guarantees database reliability:
- **Atomicity**: All changes commit, or all roll back.
- **Consistency**: All integrity constraints hold before and after execution.
- **Isolation**: Concurrent transactions do not interfere with each other.
- **Durability**: Committed data persists across crashes via WAL.

## ANSI SQL Isolation Levels

| Isolation Level | Dirty Read | Non-Repeatable Read | Phantom Read | Serialization Anomaly |
| :--- | :--- | :--- | :--- | :--- |
| **Read Uncommitted** | Possible | Possible | Possible | Possible |
| **Read Committed** | Prevented | Possible | Possible | Possible |
| **Repeatable Read** | Prevented | Prevented | Prevented (in PG MVCC) | Possible |
| **Serializable** | Prevented | Prevented | Prevented | Prevented |

```sql
-- Explicit Transaction Control
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;

UPDATE accounts SET balance = balance - 500 WHERE account_id = 101;
UPDATE accounts SET balance = balance + 500 WHERE account_id = 202;

COMMIT;
```

## Key Takeaways
- PostgreSQL uses Multi-Version Concurrency Control (MVCC) where readers never block writers and writers never block readers."""
                }
            ]
        },
        {
            "order": 9,
            "title": "Indexing Architecture & Query Optimization",
            "description": "B-Trees, Hash, GiST, GIN, BRIN, EXPLAIN ANALYZE, and Execution Plan tuning.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Index Structures (B-Tree, GIN, BRIN, Partial & Covering)",
                    "description": "Choose optimal index types for point lookups, ranges, full text, and JSONB.",
                    "duration_minutes": 50,
                    "content": """# Index Structures & Selection

Indexes speed up read operations at the cost of additional disk space and write overhead.

```sql
-- 1. Standard Composite B-Tree (Order matters: Equality first, Range second)
CREATE INDEX idx_orders_customer_date 
ON orders (customer_id, created_at DESC);

-- 2. Covering Index (Index-Only Scan with INCLUDE)
CREATE INDEX idx_users_email_covering 
ON users (email) 
INCLUDE (first_name, last_name, is_active);

-- 3. Partial Index (Saves memory for sparse subsets)
CREATE INDEX idx_orders_unprocessed 
ON orders (created_at) 
WHERE order_status = 'pending';

-- 4. GIN Index on JSONB document attributes
CREATE INDEX idx_products_metadata_gin 
ON products USING GIN (metadata);
```

## Key Takeaways
- In composite indexes `(A, B, C)`, queries filtering on `A` or `(A, B)` use the index; queries filtering only on `B` or `C` cannot use the index efficiently (Leftmost Prefix Rule)."""
                },
                {
                    "order": 2,
                    "title": "Reading EXPLAIN ANALYZE & Query Tuning",
                    "description": "Diagnose sequential scans, expensive joins, sort spills to disk, and index misuse.",
                    "duration_minutes": 45,
                    "content": """# Reading EXPLAIN ANALYZE & Query Tuning

`EXPLAIN (ANALYZE, BUFFERS, COSTS)` runs the query, measures actual execution time, and displays memory buffer statistics.

```sql
EXPLAIN (ANALYZE, BUFFERS, TIMING)
SELECT 
    u.user_id,
    u.email,
    COUNT(o.order_id) AS total_orders
FROM users u
LEFT JOIN orders o ON u.user_id = o.customer_id
WHERE u.created_at >= '2024-01-01'
GROUP BY u.user_id, u.email;
```

## Plan Red Flags to Watch For
1. **Seq Scan on Large Tables**: Missing index or predicate prevents index utilization (e.g. `WHERE UPPER(email) = '...'` without an expression index).
2. **Sort Method: external merge Disk**: `work_mem` is too low for the sort operation, forcing temp disk I/O.
3. **Huge discrepancy between `rows` estimated and `actual rows`**: Outdated statistics. Run `ANALYZE table_name;` to update planner histograms."""
                }
            ]
        },
        {
            "order": 10,
            "title": "Stored Procedures, Triggers & Database Security",
            "description": "PL/pgSQL stored procedures, triggers, row-level security (RLS), and connection pooling.",
            "chapters": [
                {
                    "order": 1,
                    "title": "PL/pgSQL Functions & Event Triggers",
                    "description": "Implement transactional business logic, auditing logs, and automatic timestamp triggers.",
                    "duration_minutes": 45,
                    "content": """# PL/pgSQL Functions & Event Triggers

Triggers execute automatically in response to DML events (`BEFORE` or `AFTER` `INSERT`, `UPDATE`, `DELETE`).

```sql
-- Audit Log Trigger Function
CREATE OR REPLACE FUNCTION log_employee_salary_update()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.salary <> OLD.salary THEN
        INSERT INTO salary_audit_log (
            employee_id,
            old_salary,
            new_salary,
            changed_by,
            changed_at
        ) VALUES (
            OLD.employee_id,
            OLD.salary,
            NEW.salary,
            CURRENT_USER,
            CURRENT_TIMESTAMP
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_salary_audit
BEFORE UPDATE ON employees
FOR EACH ROW
EXECUTE FUNCTION log_employee_salary_update();
```

## Key Takeaways
- Triggers guarantee auditability even when database records are modified through direct database connections."""
                },
                {
                    "order": 2,
                    "title": "Row Level Security (RLS) & Role-Based Access Control",
                    "description": "Enforce multi-tenant data isolation and defense-in-depth using PostgreSQL RLS policies.",
                    "duration_minutes": 40,
                    "content": """# Row Level Security (RLS) & Role-Based Access Control

Row Level Security restricts which table rows an authenticated user can select or modify.

```sql
-- Enable RLS on multi-tenant documents table
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see documents belonging to their tenant organization
CREATE POLICY tenant_isolation_policy ON documents
FOR ALL
TO application_user
USING (tenant_id = NULLIF(current_setting('app.current_tenant_id', true), '')::UUID);

-- Setting session variable in application middleware
SET LOCAL app.current_tenant_id = 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11';
SELECT * FROM documents; -- Automatically filtered to tenant!
```

## Key Takeaways
- RLS enforces multi-tenant security at the database engine level, preventing accidental data leaks even if application code omits a `WHERE tenant_id = ...` clause."""
                }
            ]
        }
    ],
    "assessment": {
        "title": "SQL & Relational Database Architecture Certification Exam",
        "description": "Evaluate your mastery of relational algebra, ACID transaction isolation, window functions, indexing, and query optimization.",
        "passing_score": 70,
        "time_limit_minutes": 25,
        "questions": [
            {
                "question_text": "Which clause in an SQL statement is evaluated logically FIRST by the database execution engine?",
                "question_type": "single",
                "explanation": "The FROM clause (including JOINs) is evaluated first to establish the working dataset before WHERE filtering, GROUP BY, and SELECT projections.",
                "points": 20,
                "options": [
                    {"text": "SELECT", "is_correct": False},
                    {"text": "WHERE", "is_correct": False},
                    {"text": "FROM", "is_correct": True},
                    {"text": "ORDER BY", "is_correct": False}
                ]
            },
            {
                "question_text": "What is the result of evaluating `NULL = NULL` in standard ANSI SQL three-valued logic?",
                "question_type": "single",
                "explanation": "In SQL three-valued logic, comparing NULL with anything (including another NULL) yields UNKNOWN, not TRUE.",
                "points": 20,
                "options": [
                    {"text": "TRUE", "is_correct": False},
                    {"text": "FALSE", "is_correct": False},
                    {"text": "UNKNOWN / NULL", "is_correct": True},
                    {"text": "Syntax Error", "is_correct": False}
                ]
            },
            {
                "question_text": "Which ANSI SQL isolation level prevents Dirty Reads and Non-Repeatable Reads, but may still allow Phantom Reads under lock-based implementations?",
                "question_type": "single",
                "explanation": "Repeatable Read prevents non-repeatable reads by keeping read locks until transaction completion, but phantom rows can appear in range queries without serializable predicate locking.",
                "points": 20,
                "options": [
                    {"text": "Read Committed", "is_correct": False},
                    {"text": "Repeatable Read", "is_correct": True},
                    {"text": "Read Uncommitted", "is_correct": False},
                    {"text": "Snapshot Isolation", "is_correct": False}
                ]
            },
            {
                "question_text": "How does DENSE_RANK() differ from RANK() when ranking rows with tied values?",
                "question_type": "single",
                "explanation": "DENSE_RANK() does not leave gaps in numbering following ties (e.g. 1, 2, 2, 3), whereas RANK() skips positions (1, 2, 2, 4).",
                "points": 20,
                "options": [
                    {"text": "DENSE_RANK() does not skip rank numbers after a tie", "is_correct": True},
                    {"text": "RANK() does not skip rank numbers after a tie", "is_correct": False},
                    {"text": "DENSE_RANK() can only be used with numbers", "is_correct": False},
                    {"text": "There is no difference", "is_correct": False}
                ]
            },
            {
                "question_text": "Under the Leftmost Prefix Rule for a composite B-Tree index on (A, B, C), which WHERE clause can efficiently use the index?",
                "question_type": "single",
                "explanation": "Queries filtering on column A or (A, B) utilize the leftmost prefix of the composite index, whereas filtering exclusively on B and C without A cannot use the index root.",
                "points": 20,
                "options": [
                    {"text": "WHERE B = 10 AND C = 20", "is_correct": False},
                    {"text": "WHERE A = 5 AND B = 10", "is_correct": True},
                    {"text": "WHERE C = 20", "is_correct": False},
                    {"text": "WHERE B = 10", "is_correct": False}
                ]
            }
        ]
    }
}
