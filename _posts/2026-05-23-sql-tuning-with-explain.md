---
layout: single
title: "SQL Tuning with EXPLAIN: What to Optimize First in Lakehouse SQL"
date: 2026-05-23 09:00:00 +0000
categories: [data-engineering]
excerpt: "How to use EXPLAIN in modern warehouses and lakehouses, plus a simple order-of-execution guide that makes tuning easier."
---

If you tune SQL by guessing, you waste time. If you tune SQL with `EXPLAIN`, you usually find the real bottleneck fast.

## The execution order that helps you reason clearly

We write SQL in one order, but engines reason in another logical order:

1. `FROM` and `JOIN`
2. `WHERE`
3. `GROUP BY`
4. `HAVING`
5. `SELECT`
6. `ORDER BY`
7. `LIMIT`

This order gives a useful tuning mindset: reduce rows as early as possible.

## A fun example

Imagine a clickstream table with billions of rows:

```sql
SELECT c.customer_tier, COUNT(*) AS purchase_events
FROM bronze.clickstream e
JOIN dim.customers c
  ON e.customer_id = c.customer_id
WHERE e.event_type = 'purchase'
  AND e.event_ts >= '2026-05-01'
GROUP BY c.customer_tier
ORDER BY purchase_events DESC;
```

Looks simple, but it can run slowly if the engine scans too much data or shuffles too much during join and aggregation.

## Use EXPLAIN before touching code

Run:

```sql
EXPLAIN
SELECT ...
```

Then check for these first:

- Full table scans where partition pruning should happen
- Huge shuffles before filters are applied
- Expensive joins caused by missing selective predicates
- Repeated scans of the same heavy subquery

## What to tune first

### 1) Filter selectivity and pushdown

Make sure your most selective filters are present and aligned with partitioned or indexed data.

In lakehouse tables, time filters are often your biggest win.

### 2) Join strategy

Confirm join keys are correct types, not casted on the fly, and use broadcast joins when one side is small enough.

### 3) Data pruning and file layout

For Delta style systems, good partitioning and clustering reduce scanned files significantly.

### 4) Aggregation pressure

Pre-aggregate earlier where possible if cardinality is exploding.

## A better shaped version

```sql
WITH purchases AS (
  SELECT customer_id
  FROM bronze.clickstream
  WHERE event_type = 'purchase'
    AND event_ts >= '2026-05-01'
)
SELECT c.customer_tier, COUNT(*) AS purchase_events
FROM purchases p
JOIN dim.customers c
  ON p.customer_id = c.customer_id
GROUP BY c.customer_tier
ORDER BY purchase_events DESC;
```

This makes row reduction explicit before the dimension join. Depending on optimizer behavior, this can reduce work and make the plan easier to reason about.

## My practical rule

When a query is slow, I ask:

- Did I reduce data early enough?
- Did I force unnecessary shuffle?
- Did I join too much before filtering?

`EXPLAIN` answers those questions better than intuition.
