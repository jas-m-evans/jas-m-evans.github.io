---
layout: single
title: "Partition By Tutorial: What Should You Partition a Delta Table By?"
date: 2026-05-21 09:00:00 +0000
categories: [data-engineering]
excerpt: "A practical guide to picking table partitions in Delta Lake, and the common mistakes that hurt query speed and cost."
---

If you have ever opened a Delta table and wondered, "Should I partition this by date, country, tenant, or something else?" you are already asking the right question.

Partitioning is one of those decisions that can help your platform feel fast and cheap, or quietly make everything slower and harder to maintain.

## What partitioning actually does

In Delta Lake, a partition creates physical folders by key values. If you partition by `event_date`, you get folder paths like:

```text
event_date=2026-05-21/
event_date=2026-05-22/
```

When your query includes that field in a filter, Spark can skip unrelated folders. That skip is where most of the benefit comes from.

## The first rule: partition for filter patterns

Start with how people query the data, not how the source system is modeled.

If most reads are:

```sql
SELECT *
FROM silver.orders
WHERE order_date BETWEEN '2026-05-01' AND '2026-05-07'
```

Then partitioning by `order_date` is usually a strong choice.

If most reads are tenant specific and each tenant is large:

```sql
SELECT *
FROM silver.orders
WHERE tenant_id = 'acme'
  AND order_date >= '2026-05-01'
```

Then a tenant focused design may be useful, but only if cardinality and file size stay healthy.

## What to avoid

### 1) Very high cardinality keys

Partitioning by `user_id` with millions of values usually creates too many tiny directories and tiny files.

### 2) Low value partitions

Partitioning by `is_active` (true/false) gives only two folders and usually does not help enough.

### 3) Partitioning by a field no one filters on

If nobody filters on `region`, a region partition mostly adds operational complexity.

## Quick checklist I use in practice

1. Is this column used in common `WHERE` filters?
2. Is the cardinality reasonable for folder management?
3. Will writes land in a manageable number of partitions each batch?
4. Will each partition hold enough data to avoid tiny files?
5. Will this still make sense six months from now?

## Databricks specific considerations

- Use partitioning for coarse pruning, then `OPTIMIZE` for compact files.
- Use `ZORDER` for secondary skipping on high value columns that are filtered often but not good partition keys.
- Watch skew. One hot partition can destroy parallelism.
- Revisit partition choices as traffic and access patterns change.

A useful mental model is this: partition by the broad dimension that helps skip big chunks, then use table maintenance features to fine tune.

## A practical default

For many event style tables, partitioning by date is still the safest default because:

- Most analytical reads are time bounded
- Retention and backfills are easier to manage
- File growth is naturally segmented

It is not always perfect, but it is often a better starting point than chasing clever partition keys too early.

Partitioning is less about finding a magical column and more about matching storage layout to real query behavior. If you do that, performance usually follows.
