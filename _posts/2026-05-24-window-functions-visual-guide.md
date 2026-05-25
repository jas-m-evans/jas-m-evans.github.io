---
layout: single
title: "Window Functions, Explained with a Silly Visual That Actually Helps"
date: 2026-05-24 09:00:00 +0000
categories: [data-engineering]
excerpt: "A visual memory trick for window functions, plus side by side SQL and PySpark examples for rank, lag, and running totals."
---

Window functions can feel weird because the names are not words we use in daily conversation. "Partition," "frame," and "lag" can blur together if you do not use them every day.

So here is the silly analogy I use.

## Imagine a school hallway photo board

You are organizing student photos on a hallway wall.

- **Partition** = split the wall into sections by class (Grade 9, Grade 10)
- **Order** = arrange each section by score or timestamp
- **Window frame** = choose which nearby photos each student can compare against

Each student keeps their own row, but they can look around within their section.

That is a window function.

## Memory trick for the terms

- **PARTITION BY**: "Put me in my group"
- **ORDER BY**: "Line us up"
- **ROWS BETWEEN**: "Who can I look at"
- **LAG/LEAD**: "Who is behind me or ahead of me"

If you remember group, line, and look, most window SQL becomes easier.

## SQL examples

### 1) Rank sales per region

```sql
SELECT
  region,
  salesperson,
  revenue,
  DENSE_RANK() OVER (
    PARTITION BY region
    ORDER BY revenue DESC
  ) AS revenue_rank
FROM sales;
```

### 2) Previous month revenue in same region

```sql
SELECT
  region,
  month,
  revenue,
  LAG(revenue, 1) OVER (
    PARTITION BY region
    ORDER BY month
  ) AS prev_revenue
FROM monthly_sales;
```

### 3) Running total by account

```sql
SELECT
  account_id,
  txn_ts,
  amount,
  SUM(amount) OVER (
    PARTITION BY account_id
    ORDER BY txn_ts
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_balance
FROM transactions;
```

## PySpark equivalents

```python
from pyspark.sql import functions as F
from pyspark.sql.window import Window

w_rank = Window.partitionBy("region").orderBy(F.col("revenue").desc())
ranked = sales_df.withColumn("revenue_rank", F.dense_rank().over(w_rank))

w_lag = Window.partitionBy("region").orderBy("month")
with_prev = monthly_df.withColumn("prev_revenue", F.lag("revenue", 1).over(w_lag))

w_running = (
    Window
    .partitionBy("account_id")
    .orderBy("txn_ts")
    .rowsBetween(Window.unboundedPreceding, Window.currentRow)
)
with_running = txn_df.withColumn("running_balance", F.sum("amount").over(w_running))
```

## Final takeaway

A window function does not collapse rows like `GROUP BY`. It adds context to each row while keeping row level detail.

When I forget syntax, I go back to the hallway wall image: group them, line them up, define how far they can look.
