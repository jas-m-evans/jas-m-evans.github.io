---
layout: single
title: "Professor Oak’s SQL Notebook: Ash’s Kanto Run — 10 Window Function Concepts"
date: 2026-05-24 09:00:00 +0000
categories: [data-engineering]
excerpt: "A Pokémon-themed SQL tutorial covering every window function concept tested in interviews: SUM, PARTITION BY, frames, RANGE vs ROWS, ranking, LAG, LEAD, FIRST_VALUE, NTILE, islands-and-gaps, and CTE chaining."
---

Window functions let you compute aggregates and comparisons across rows while keeping each row visible. `GROUP BY` collapses rows. Window functions do not.

The syntax can feel strange at first:

- `OVER (...)` — defines the window the function operates on
- `PARTITION BY` — splits rows into independent groups
- `ORDER BY` — sets the sequence inside each group
- `ROWS BETWEEN` / `RANGE BETWEEN` — controls how much of the sequence each row can see

This tutorial uses one Pokémon dataset all the way through. Each section is a new lens on the same data.

**10 concepts covered:**

1. `SUM() OVER` — running totals
2. `PARTITION BY` — independent group calculations
3. `ROWS BETWEEN` — rolling windows
4. `RANGE BETWEEN` vs `ROWS BETWEEN` — value-based vs row-count-based frames
5. `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()` — tie behavior
6. `LAG()` — look back one row
7. `LEAD()` — look forward one row
8. `FIRST_VALUE()` / `LAST_VALUE()` — partition anchors (and a common trap)
9. `NTILE(n)` — bucketing into equal groups
10. Islands-and-gaps — detecting consecutive sequences

---

## The dataset: Ash’s Kanto journey

> **⚠️ Spoiler warning:** the data below reveals how Ash’s season ends. If you care about that sort of thing, consider yourself warned.

<details>
  <summary>Not a Pokémon fan? Quick context (spoilers)</summary>
  Ash Ketchum is a ten-year-old trainer who travels the Kanto region with his partner Pikachu. To qualify for the regional championship — the Indigo League — he has to defeat eight Gym Leaders and earn their badges. He wins all eight, makes it to the Indigo League, and loses to a rival named Ritchie when his own Pokémon, Charizard, refuses to battle.
</details>

That story gives us nine battles in order.

```sql
WITH kanto_battles AS (
  SELECT * FROM (
    VALUES
      (1,  'EP005', 'Pewter Gym',    'Brock',     'W', 1),
      (2,  'EP007', 'Cerulean Gym',  'Misty',     'W', 1),
      (3,  'EP014', 'Vermilion Gym', 'Lt. Surge', 'W', 1),
      (4,  'EP024', 'Celadon Gym',   'Erika',     'W', 1),
      (5,  'EP032', 'Fuchsia Gym',   'Koga',      'W', 1),
      (6,  'EP059', 'Saffron Gym',   'Sabrina',   'W', 1),
      (7,  'EP063', 'Cinnabar Gym',  'Blaine',    'W', 1),
      (8,  'EP067', 'Viridian Gym',  'Giovanni',  'W', 1),
      (9,  'EP076', 'Indigo League', 'Ritchie',   'L', 0)
  ) AS t(event_order, episode_id, event_name, opponent, result, win_flag)
)
SELECT * FROM kanto_battles;
```

| # | event_name    | opponent  | result | win_flag |
|---|---------------|-----------|--------|----------|
| 1 | Pewter Gym    | Brock     | W      | 1        |
| 2 | Cerulean Gym  | Misty     | W      | 1        |
| 3 | Vermilion Gym | Lt. Surge | W      | 1        |
| 4 | Celadon Gym   | Erika     | W      | 1        |
| 5 | Fuchsia Gym   | Koga      | W      | 1        |
| 6 | Saffron Gym   | Sabrina   | W      | 1        |
| 7 | Cinnabar Gym  | Blaine    | W      | 1        |
| 8 | Viridian Gym  | Giovanni  | W      | 1        |
| 9 | Indigo League | Ritchie   | L      | 0        |

---

## 1) Running total with `SUM() OVER`

A regular `SUM()` with `GROUP BY` collapses everything to one row. A window function keeps every row and adds a cumulative column alongside it.

```sql
SELECT
  event_order,
  event_name,
  result,
  SUM(win_flag) OVER (
    ORDER BY event_order
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_wins
FROM kanto_battles
ORDER BY event_order;
```

`UNBOUNDED PRECEDING` means start from the very first row. `CURRENT ROW` means stop here.

**Result:**

| # | event_name    | result | running_wins |
|---|---------------|--------|--------------|
| 1 | Pewter Gym    | W      | 1            |
| 2 | Cerulean Gym  | W      | 2            |
| 3 | Vermilion Gym | W      | 3            |
| 4 | Celadon Gym   | W      | 4            |
| 5 | Fuchsia Gym   | W      | 5            |
| 6 | Saffron Gym   | W      | 6            |
| 7 | Cinnabar Gym  | W      | 7            |
| 8 | Viridian Gym  | W      | 8            |
| 9 | Indigo League | L      | 8            |

Row 9 stays at 8 — the loss contributes `win_flag = 0` so it adds nothing. Compare to `GROUP BY`: you’d get one row with `total = 8`, and all per-battle detail would be gone.

---

## 2) `PARTITION BY`: independent calculations per group

`PARTITION BY` resets the window for each group. Without it, the window spans the whole table. With it, each partition runs its own independent calculation.

Here we split battles into two stages — Gym Circuit and League Stage — and track cumulative wins separately inside each one.

```sql
SELECT
  event_order,
  event_name,
  CASE
    WHEN event_name LIKE '%Gym%' THEN 'Gym Circuit'
    ELSE 'League Stage'
  END AS stage,
  win_flag,
  SUM(win_flag) OVER (
    PARTITION BY CASE WHEN event_name LIKE '%Gym%' THEN 'Gym Circuit' ELSE 'League Stage' END
    ORDER BY event_order
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS stage_wins
FROM kanto_battles
ORDER BY event_order;
```

**Result:**

| # | event_name    | stage        | win_flag | stage_wins |
|---|---------------|--------------|----------|------------|
| 1 | Pewter Gym    | Gym Circuit  | 1        | 1          |
| 2 | Cerulean Gym  | Gym Circuit  | 1        | 2          |
| 3 | Vermilion Gym | Gym Circuit  | 1        | 3          |
| 4 | Celadon Gym   | Gym Circuit  | 1        | 4          |
| 5 | Fuchsia Gym   | Gym Circuit  | 1        | 5          |
| 6 | Saffron Gym   | Gym Circuit  | 1        | 6          |
| 7 | Cinnabar Gym  | Gym Circuit  | 1        | 7          |
| 8 | Viridian Gym  | Gym Circuit  | 1        | 8          |
| 9 | Indigo League | League Stage | 0        | 0          |

Row 9 resets to 0 because it belongs to a different partition. The Gym Circuit running total of 8 is untouched — it’s a completely separate calculation.

---

## 3) `ROWS BETWEEN`: rolling windows

By default `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` makes every row look all the way back to the start. A frame clause lets you narrow that window to just the nearby rows.

This query tracks wins over only the last three battles — a "current form" stat rather than a career stat.

```sql
SELECT
  event_order,
  event_name,
  result,
  SUM(win_flag) OVER (
    ORDER BY event_order
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
  ) AS wins_last_3
FROM kanto_battles
ORDER BY event_order;
```

`2 PRECEDING` + `CURRENT ROW` = a 3-row window. At each row, SQL looks back at most 2 rows and includes the current one.

**Result:**

| # | event_name    | result | wins_last_3 |
|---|---------------|--------|-------------|
| 1 | Pewter Gym    | W      | 1           |
| 2 | Cerulean Gym  | W      | 2           |
| 3 | Vermilion Gym | W      | 3           |
| 4 | Celadon Gym   | W      | 3           |
| 5 | Fuchsia Gym   | W      | 3           |
| 6 | Saffron Gym   | W      | 3           |
| 7 | Cinnabar Gym  | W      | 3           |
| 8 | Viridian Gym  | W      | 3           |
| 9 | Indigo League | L      | 2           |

Rows 1 and 2 have fewer than 3 prior rows available so the frame shrinks to fit. Row 9 looks at battles 7, 8, 9: two wins and one loss = 2.

---

## 4) `RANGE BETWEEN` vs `ROWS BETWEEN`

These look similar but behave very differently when the `ORDER BY` column has duplicate values.

- `ROWS BETWEEN` counts **physical rows** — always the exact number of rows you specify
- `RANGE BETWEEN` counts **logical values** — it includes all rows whose `ORDER BY` value falls within the range you specify

To see the difference clearly, we order by `win_flag` which has duplicates (eight 1s and one 0):

```sql
SELECT
  event_order,
  event_name,
  win_flag,
  SUM(win_flag) OVER (
    ORDER BY win_flag
    ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
  ) AS rows_sum,
  SUM(win_flag) OVER (
    ORDER BY win_flag
    RANGE BETWEEN 1 PRECEDING AND 1 FOLLOWING
  ) AS range_sum
FROM kanto_battles
ORDER BY win_flag, event_order;
```

**Result:**

| # | event_name    | win_flag | rows_sum | range_sum |
|---|---------------|----------|----------|-----------|
| 9 | Indigo League | 0        | 1        | 8         |
| 1 | Pewter Gym    | 1        | 2        | 8         |
| 2 | Cerulean Gym  | 1        | 3        | 8         |
| 3 | Vermilion Gym | 1        | 3        | 8         |
| 4 | Celadon Gym   | 1        | 3        | 8         |
| 5 | Fuchsia Gym   | 1        | 3        | 8         |
| 6 | Saffron Gym   | 1        | 3        | 8         |
| 7 | Cinnabar Gym  | 1        | 3        | 8         |
| 8 | Viridian Gym  | 1        | 2        | 8         |

For `ROWS`: row 9 (win_flag=0) sees itself plus 1 physical row forward = sum of 0+1 = 1. Row 1 sees 1 back + itself + 1 forward = 0+1+1 = 2. The window moves like a sliding physical frame.

For `RANGE`: every row with win_flag=1 uses the range "between 0 and 2" — which includes all 9 rows in the table. So every single row returns 8 (the sum of all win_flags). `RANGE` says "find all rows whose ORDER BY value is within 1 of mine," which sweeps in every row that shares a similar value.

**When does this matter in practice?** When you’re computing a 7-day rolling window with `RANGE BETWEEN INTERVAL '6 DAYS' PRECEDING AND CURRENT ROW` on a date column — that’s a date-range frame, not a row-count frame, and it handles missing dates correctly. `ROWS BETWEEN 6 PRECEDING` always grabs exactly 7 physical rows regardless of what dates they represent.

---

## 5) Ranking functions: tie behavior matters

Three functions look nearly identical but handle ties differently. This is a frequent interview trap because the wrong choice silently produces wrong answers.

To make the tie behavior visible, we rank by `win_flag DESC` — all 8 wins tie at the top, the one loss is at the bottom.

```sql
SELECT
  event_order,
  event_name,
  win_flag,
  ROW_NUMBER() OVER (ORDER BY win_flag DESC, event_order) AS row_num,
  RANK()       OVER (ORDER BY win_flag DESC)              AS rnk,
  DENSE_RANK() OVER (ORDER BY win_flag DESC)              AS dense_rnk
FROM kanto_battles
ORDER BY event_order;
```

**Result:**

| # | event_name    | win_flag | row_num | rnk | dense_rnk |
|---|---------------|----------|---------|-----|-----------|
| 1 | Pewter Gym    | 1        | 1       | 1   | 1         |
| 2 | Cerulean Gym  | 1        | 2       | 1   | 1         |
| 3 | Vermilion Gym | 1        | 3       | 1   | 1         |
| 4 | Celadon Gym   | 1        | 4       | 1   | 1         |
| 5 | Fuchsia Gym   | 1        | 5       | 1   | 1         |
| 6 | Saffron Gym   | 1        | 6       | 1   | 1         |
| 7 | Cinnabar Gym  | 1        | 7       | 1   | 1         |
| 8 | Viridian Gym  | 1        | 8       | 1   | 1         |
| 9 | Indigo League | 0        | 9       | 9   | 2         |

Row 9 is where it diverges:

- `ROW_NUMBER`: always unique — every row gets a distinct number regardless of ties. Tie-breaking is determined by the secondary `ORDER BY event_order`.
- `RANK`: 8 rows tie for rank 1, so the next rank jumps to 9. Ranks 2–8 are skipped.
- `DENSE_RANK`: 8 rows tie for rank 1, next rank is 2. No gaps.

**Interview rule:** when a problem says "top N per group" and the dataset has ties, `RANK()` can return fewer than N results for a group if ties push the next unique rank past N. `DENSE_RANK()` is the safe default for top-N filtering.

---

## 6) `LAG()`: look at the previous row

`LAG(column)` returns the value of that column from the row immediately before the current one. The first row gets `NULL` — nothing precedes it.

```sql
SELECT
  event_order,
  event_name,
  result,
  LAG(result) OVER (ORDER BY event_order) AS prev_result,
  CASE
    WHEN LAG(result) OVER (ORDER BY event_order) = 'W' AND result = 'L' THEN 'Momentum Broken'
    WHEN LAG(result) OVER (ORDER BY event_order) = result               THEN 'Steady'
    ELSE 'Shift'
  END AS momentum_state
FROM kanto_battles
ORDER BY event_order;
```

**Result:**

| # | event_name    | result | prev_result | momentum_state  |
|---|---------------|--------|-------------|-----------------|
| 1 | Pewter Gym    | W      | NULL        | Shift           |
| 2 | Cerulean Gym  | W      | W           | Steady          |
| 3 | Vermilion Gym | W      | W           | Steady          |
| 4 | Celadon Gym   | W      | W           | Steady          |
| 5 | Fuchsia Gym   | W      | W           | Steady          |
| 6 | Saffron Gym   | W      | W           | Steady          |
| 7 | Cinnabar Gym  | W      | W           | Steady          |
| 8 | Viridian Gym  | W      | W           | Steady          |
| 9 | Indigo League | L      | W           | Momentum Broken |

Row 1 has `NULL` for `prev_result`. Rows 2–8 match the previous result so they’re `Steady`. Row 9 gets `Momentum Broken`: `LAG()` pulled the prior `W` and the `CASE` caught the W→L flip.

You can also offset further back: `LAG(result, 2)` looks back two rows. The second argument defaults to 1.

---

## 7) `LEAD()`: look at the next row

`LEAD(column)` is the forward-looking complement to `LAG()`. The last row gets `NULL` — nothing follows it.

```sql
SELECT
  event_order,
  event_name,
  opponent,
  result,
  LEAD(opponent)   OVER (ORDER BY event_order) AS next_opponent,
  LEAD(event_name) OVER (ORDER BY event_order) AS next_event
FROM kanto_battles
ORDER BY event_order;
```

**Result:**

| # | event_name    | opponent  | result | next_opponent | next_event    |
|---|---------------|-----------|--------|---------------|---------------|
| 1 | Pewter Gym    | Brock     | W      | Misty         | Cerulean Gym  |
| 2 | Cerulean Gym  | Misty     | W      | Lt. Surge     | Vermilion Gym |
| 3 | Vermilion Gym | Lt. Surge | W      | Erika         | Celadon Gym   |
| 4 | Celadon Gym   | Erika     | W      | Koga          | Fuchsia Gym   |
| 5 | Fuchsia Gym   | Koga      | W      | Sabrina       | Saffron Gym   |
| 6 | Saffron Gym   | Sabrina   | W      | Blaine        | Cinnabar Gym  |
| 7 | Cinnabar Gym  | Blaine    | W      | Giovanni      | Viridian Gym  |
| 8 | Viridian Gym  | Giovanni  | W      | Ritchie       | Indigo League |
| 9 | Indigo League | Ritchie   | L      | NULL          | NULL          |

Row 9 gets `NULL` for both forward columns — the season is over.

`LEAD()` and `LAG()` take identical arguments and work the same way in opposite directions. A common real-world use: retention analysis — `LEAD(event_date)` gives you each user’s next activity date, so you can check whether the gap to the next event is 1 day (retained) or much longer (churned).

---

## 8) `FIRST_VALUE()` and `LAST_VALUE()`: partition anchors

`FIRST_VALUE(column)` returns the first value of that column in the window. `LAST_VALUE(column)` returns the last. These are useful when you want every row to carry a reference point from the start or end of its group.

**The `LAST_VALUE` trap — the most common mistake with these functions:**

By default, every window function uses the frame `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`. For `LAST_VALUE`, this means "the last value seen so far" — which is just the current row’s value. That’s almost never what you want.

```sql
SELECT
  event_order,
  event_name,
  result,
  FIRST_VALUE(opponent) OVER (ORDER BY event_order)                                                AS first_opponent,
  LAST_VALUE(opponent)  OVER (ORDER BY event_order)                                                AS last_val_wrong,
  LAST_VALUE(opponent)  OVER (ORDER BY event_order ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_val_correct
FROM kanto_battles
ORDER BY event_order;
```

**Result:**

| # | event_name    | result | first_opponent | last_val_wrong | last_val_correct |
|---|---------------|--------|----------------|----------------|------------------|
| 1 | Pewter Gym    | W      | Brock          | Brock          | Ritchie          |
| 2 | Cerulean Gym  | W      | Brock          | Misty          | Ritchie          |
| 3 | Vermilion Gym | W      | Brock          | Lt. Surge      | Ritchie          |
| 4 | Celadon Gym   | W      | Brock          | Erika          | Ritchie          |
| 5 | Fuchsia Gym   | W      | Brock          | Koga           | Ritchie          |
| 6 | Saffron Gym   | W      | Brock          | Sabrina        | Ritchie          |
| 7 | Cinnabar Gym  | W      | Brock          | Blaine         | Ritchie          |
| 8 | Viridian Gym  | W      | Brock          | Giovanni       | Ritchie          |
| 9 | Indigo League | L      | Brock          | Ritchie        | Ritchie          |

`first_opponent` is always `Brock` — `FIRST_VALUE` works correctly with the default frame because it’s looking backward.

`last_val_wrong` just returns the current row’s opponent — it’s not looking at the last row in the partition, it’s looking at the last row *in the current frame*, which with the default frame is always the current row itself.

`last_val_correct` extends the frame to `UNBOUNDED FOLLOWING`, so every row can see to the end of the partition and correctly returns `Ritchie` everywhere.

**Practical alternative:** to avoid the trap entirely, many SQL practitioners use `FIRST_VALUE` with a reversed `ORDER BY DESC` instead of `LAST_VALUE`. Same result, no frame adjustment needed.

---

## 9) `NTILE(n)`: divide rows into equal buckets

`NTILE(n)` splits rows into n as-equal-as-possible buckets and assigns each row a bucket number. Common uses: quartile analysis, top/bottom X%, A/B test segmentation.

Here we split the nine battles into three tiers — early, mid, and late season:

```sql
SELECT
  event_order,
  event_name,
  result,
  NTILE(3) OVER (ORDER BY event_order) AS season_tier
FROM kanto_battles
ORDER BY event_order;
```

**Result:**

| # | event_name    | result | season_tier |
|---|---------------|--------|-------------|
| 1 | Pewter Gym    | W      | 1           |
| 2 | Cerulean Gym  | W      | 1           |
| 3 | Vermilion Gym | W      | 1           |
| 4 | Celadon Gym   | W      | 2           |
| 5 | Fuchsia Gym   | W      | 2           |
| 6 | Saffron Gym   | W      | 2           |
| 7 | Cinnabar Gym  | W      | 3           |
| 8 | Viridian Gym  | W      | 3           |
| 9 | Indigo League | L      | 3           |

9 rows into 3 buckets = 3 rows each, clean split. If the rows don’t divide evenly, the earlier buckets get the extra row.

A more common real-world use: `NTILE(4)` for quartiles or `NTILE(100)` as an approximation of percentile rank. If you want to filter to the top 25% of users by spend, wrap this in a CTE and `WHERE spend_quartile = 1`.

---

## 10) Islands and gaps: detecting consecutive sequences

This is the hardest and most-praised window function pattern in SQL interviews. It shows up in "find users active for N consecutive days" problems and is considered a separator between strong and weak SQL candidates.

**The core trick:** for a sequence to be consecutive, the difference between the sequence value and its row number stays constant within the same consecutive run. When there’s a gap, that difference changes.

To demonstrate, we use a training log dataset — the days in a month that Ash logged a training session:

```sql
WITH training_days AS (
  SELECT * FROM (
    VALUES (1), (2), (3), (5), (6), (10), (11), (12)
  ) AS t(day_num)
)
SELECT
  day_num,
  ROW_NUMBER() OVER (ORDER BY day_num)           AS rn,
  day_num - ROW_NUMBER() OVER (ORDER BY day_num) AS group_id
FROM training_days;
```

**Result:**

| day_num | rn | group_id |
|---------|----|----------|
| 1       | 1  | 0        |
| 2       | 2  | 0        |
| 3       | 3  | 0        |
| 5       | 4  | 1        |
| 6       | 5  | 1        |
| 10      | 6  | 4        |
| 11      | 7  | 4        |
| 12      | 8  | 4        |

Days 1, 2, 3 all produce `group_id = 0` because they’re consecutive — each day increments by 1 and so does the row number. Day 5 jumps to `group_id = 1` because there was a gap (day 4 is missing). Days 5 and 6 share `group_id = 1`. Days 10–12 share `group_id = 4`.

Now wrap that in a CTE and aggregate by `group_id` to get each streak:

```sql
WITH training_days AS (
  SELECT * FROM (
    VALUES (1), (2), (3), (5), (6), (10), (11), (12)
  ) AS t(day_num)
),
grouped AS (
  SELECT
    day_num,
    day_num - ROW_NUMBER() OVER (ORDER BY day_num) AS group_id
  FROM training_days
)
SELECT
  MIN(day_num) AS streak_start,
  MAX(day_num) AS streak_end,
  COUNT(*)     AS streak_length
FROM grouped
GROUP BY group_id
ORDER BY streak_start;
```

**Result:**

| streak_start | streak_end | streak_length |
|--------------|------------|---------------|
| 1            | 3          | 3             |
| 5            | 6          | 2             |
| 10           | 12         | 3             |

Three separate training streaks, their start and end days, and their lengths — all from a single subtraction trick.

**Why this works:** consecutive integers always maintain a constant difference to a continuously incrementing row number. A gap in the sequence breaks that constant, creating a new group. This same pattern applies directly to dates: replace `day_num` with a `DATE` column and `ROW_NUMBER()` with a row number ordered by date, and you get consecutive-day streaks.

---

## The CTE chaining rule

There is one constraint that catches people off guard in interviews: **you cannot reference a window function result in a `WHERE` or `HAVING` clause in the same query.**

This does not work:

```sql
-- INVALID: window function alias used directly in WHERE
SELECT
  event_order,
  event_name,
  DENSE_RANK() OVER (ORDER BY win_flag DESC) AS rnk
FROM kanto_battles
WHERE rnk = 1;  -- error: column "rnk" does not exist
```

The reason: SQL evaluates `WHERE` before `SELECT`, so the window function alias hasn’t been computed yet when the filter runs.

The fix is always a CTE (or subquery):

```sql
WITH ranked AS (
  SELECT
    event_order,
    event_name,
    win_flag,
    DENSE_RANK() OVER (ORDER BY win_flag DESC) AS rnk
  FROM kanto_battles
)
SELECT event_order, event_name, win_flag
FROM ranked
WHERE rnk = 1;
```

**Result:**

| # | event_name    | win_flag |
|---|---------------|----------|
| 1 | Pewter Gym    | 1        |
| 2 | Cerulean Gym  | 1        |
| 3 | Vermilion Gym | 1        |
| 4 | Celadon Gym   | 1        |
| 5 | Fuchsia Gym   | 1        |
| 6 | Saffron Gym   | 1        |
| 7 | Cinnabar Gym  | 1        |
| 8 | Viridian Gym  | 1        |

The CTE materializes the window function result first, and then the outer query’s `WHERE` can filter on it. This pattern — compute window in CTE, filter in outer query — is the standard structure for any "top-N per group" or "filter by rank" problem.

---

## Quick syntax decoder

When you see a window function:

```sql
FUNCTION(col) OVER (
  PARTITION BY x
  ORDER BY y
  ROWS BETWEEN a PRECEDING AND b FOLLOWING
)
```

Read it in this order:

1. Which group? (`PARTITION BY`)
2. What order within the group? (`ORDER BY`)
3. How much of that order can this row see? (`ROWS BETWEEN` / `RANGE BETWEEN`)
4. What calculation on that visible slice? (`FUNCTION`)

---

## Practice problems

These use the same `kanto_battles` CTE from above. All assume it is already defined. Try each one before opening the answer.

---

### Q1 ( First battle to reach 5 winsMedium) 

> Return the first battle at which Ash's cumulative win total reached exactly 5.

**How to reason through it:**

You need a running  that's `SUM(win_flag) OVER (ORDER BY event_order)`. But you can't filter on a window function alias in `WHERE` in the same query. So: compute the running total in a CTE, then filter in the outer query. Take the earliest row where `running_wins >= 5`.total 

<details>
<summary>Answer</summary>

```sql
WITH running AS (
  SELECT
    event_order,
    event_name,
    result,
    SUM(win_flag) OVER (
      ORDER BY event_order
      ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_wins
  FROM kanto_battles
)
SELECT event_order, event_name, result, running_wins
FROM running
WHERE running_wins >= 5
ORDER BY event_order
LIMIT 1;
```

**Result:**

| # | event_name   | result | running_wins |
|---|--------------|--------|--------------|
| 5 | Fuchsia Gym  | W      | 5            |

Battle 5 is the first time the running total hits 5. The CTE chaining rule is what makes this  compute first, filter second.work 

</details>

---

### Q2 ( Running win rateMedium) 

> For each battle, show the cumulative win rate as a percentage, rounded to 1 decimal place (e.g. `88.9`).

**How to reason through it:**

Win rate = wins so far        total battles so far. You have two running counts to compute: `SUM(win_flag)` for wins, and `COUNT(*) OVER (...)` for total battles. Divide them and multiply by 100. Make sure to cast to a  integer division will return 0 or 1.decimal 

<details>
<summary>Answer</summary>

```sql
SELECT
  event_order,
  event_name,
  result,
  ROUND(
    100.0
      * SUM(win_flag) OVER (ORDER BY event_order ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
      / COUNT(*)      OVER (ORDER BY event_order ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW),
    1
  ) AS win_rate_pct
FROM kanto_battles
ORDER BY event_order;
```

**Result:**

| # | event_name    | result | win_rate_pct |
|---|---------------|--------|--------------|
| 1 | Pewter Gym    | W      | 100.0        |
| 2 | Cerulean Gym  | W      | 100.0        |
| 3 | Vermilion Gym | W      | 100.0        |
| 4 | Celadon Gym   | W      | 100.0        |
| 5 | Fuchsia Gym   | W      | 100.0        |
| 6 | Saffron Gym   | W      | 100.0        |
| 7 | Cinnabar Gym  | W      | 100.0        |
| 8 | Viridian Gym  | W      | 100.0        |
| 9 | Indigo League | L      | 88.9         |

100% through battle 8, then drops to 88.9% (8 wins / 9 battles) after the loss. Two window functions in one ` each with the same `OVER()` definition, just different aggregation functions.SELECT` 

</details>

---

### Q3 (Medium- Battles where the result changedHard) 

> Return all battles where the result was different from the previous battle's result. Include the previous result in the output.

**How to reason through it:**

You need `LAG(result)` to get the previous result. Then you want to filter where `result != prev_result`. The trap: you can't put a window function in `WHERE`. Wrap in a CTE, filter in the outer query. Also exclude the first row where `prev_result IS NULL`.

<details>
<summary>Answer</summary>

```sql
WITH lagged AS (
  SELECT
    event_order,
    event_name,
    result,
    LAG(result) OVER (ORDER BY event_order) AS prev_result
  FROM kanto_battles
)
SELECT event_order, event_name, result, prev_result
FROM lagged
WHERE prev_result IS NOT NULL
  AND result != prev_result;
```

**Result:**

| # | event_name    | result | prev_result |
|---|---------------|--------|-------------|
| 9 | Indigo League | L      | W           |

Only one  the Indigo League loss is the only result change in the entire dataset. Every other battle was a win following a win. This is exactly the kind of query used in retention analysis: find the sessions where a user's behavior shifted.row 

</details>

---

### Q4 ( Longest training streakHard) 

> Using the `training_days` dataset from section 10, return each training streak ordered by streak length descending, then by start day.

**How to reason through it:**

This is the islands-and-gaps pattern. Step 1: compute `day_num - ROW_NUMBER() OVER (ORDER BY day_num)` to create a constant `group_id` for each consecutive run. Step 2: aggregate by `group_id` to get streak start, end, and length. You need two CTEs: one to compute `group_id`, one to aggregate.

<details>
<summary>Answer</summary>

```sql
WITH training_days AS (
  SELECT * FROM (
    VALUES (1), (2), (3), (5), (6), (10), (11), (12)
  ) AS t(day_num)
),
grouped AS (
  SELECT
    day_num,
    day_num - ROW_NUMBER() OVER (ORDER BY day_num) AS group_id
  FROM training_days
)
SELECT
  MIN(day_num) AS streak_start,
  MAX(day_num) AS streak_end,
  COUNT(*)     AS streak_length
FROM grouped
GROUP BY group_id
ORDER BY streak_length DESC, streak_start;
```

**Result:**

| streak_start | streak_end | streak_length |
|--------------|------------|---------------|
| 1            | 3          | 3             |
| 10           | 12         | 3             |
| 5            | 6          | 2             |

Two streaks of length 3 tied at the top, ordered by start day. The two-day streak comes last. If you only needed the single longest streak, wrap this in another CTE and `LIMIT 1`.

</details>

---

### Q5 ( Win rate by season tierHard) 

> Divide the nine battles into three equal tiers (early, mid, late season) using `NTILE(3)`. For each tier, return the tier number, battle count, win count, and win rate percentage rounded to 1 decimal.

**How to reason through it:**

`NTILE(3)` assigns a tier to each  that's a window function, so it goes in a CTE. Then the outer query does a plain `GROUP BY tier` with `COUNT`, `SUM`, and division. Two-step: window to assign tiers, aggregate to summarize them.row 

<details>
<summary>Answer</summary>

```sql
WITH tiered AS (
  SELECT
    event_order,
    event_name,
    win_flag,
    NTILE(3) OVER (ORDER BY event_order) AS tier
  FROM kanto_battles
)
SELECT
  tier,
  COUNT(*)                                     AS battles,
  SUM(win_flag)                                AS wins,
  ROUND(100.0 * SUM(win_flag) / COUNT(*), 1)  AS win_rate_pct
FROM tiered
GROUP BY tier
ORDER BY tier;
```

**Result:**

| tier | battles | wins | win_rate_pct |
|------|---------|------|--------------|
| 1    | 3       | 3    | 100.0        |
| 2    | 3       | 3    | 100.0        |
| 3    | 3       | 2    | 66.7         |

Tier 3 (battles 9: Cinnabar, Viridian, Indigo League) is the only tier with a loss. Tier 1 and 2 are both perfect. The two-step CTE + GROUP BY pattern here is the standard approach any time you need to aggregate over window-function-assigned groups.7

</details>
