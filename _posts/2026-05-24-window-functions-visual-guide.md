---
layout: single
title: "Professor Oak’s SQL Notebook: Ash’s Kanto Run in 2 Window Functions"
date: 2026-05-24 09:00:00 +0000
categories: [data-engineering]
excerpt: "A Pokémon-themed SQL tutorial teaching window functions with SUM() OVER and LAG() against a real dataset."
---

Window functions let you compute aggregates and comparisons across rows — without collapsing your result set the way `GROUP BY` does. The syntax looks unfamiliar at first: `FUNCTION() OVER (ORDER BY ...)` is not something you encounter in basic SQL, and the frame clause (`ROWS BETWEEN ...`) can feel arbitrary until you see it in action.

This tutorial works through two of the most useful window functions using a single dataset: Ash Ketchum’s Kanto gym run. Every query runs against the same table, and every query includes the actual output so you can see exactly what each clause is doing.

The two functions covered:

1. `SUM() OVER` — running totals
2. `LAG()` — comparing each row to the previous one

## The dataset

The table tracks each of Ash’s significant battles in order — eight gym wins followed by his Indigo League loss to Ritchie.

```sql
WITH kanto_battles AS (
  SELECT * FROM (
    VALUES
      (1,  'EP005', 'Pewter Gym',   'Brock',    'W', 1),
      (2,  'EP007', 'Cerulean Gym', 'Misty',    'W', 1),
      (3,  'EP014', 'Vermilion Gym','Lt. Surge','W', 1),
      (4,  'EP024', 'Celadon Gym',  'Erika',    'W', 1),
      (5,  'EP032', 'Fuchsia Gym',  'Koga',     'W', 1),
      (6,  'EP059', 'Saffron Gym',  'Sabrina',  'W', 1),
      (7,  'EP063', 'Cinnabar Gym', 'Blaine',   'W', 1),
      (8,  'EP067', 'Viridian Gym', 'Giovanni', 'W', 1),
      (9,  'EP076', 'Indigo League','Ritchie',  'L', 0)
  ) AS t(event_order, episode_id, event_name, opponent, result, win_flag)
)
SELECT * FROM kanto_battles;
```

**Result:**

| event_order | episode_id | event_name    | opponent  | result | win_flag |
|-------------|------------|---------------|-----------|--------|----------|
| 1           | EP005      | Pewter Gym    | Brock     | W      | 1        |
| 2           | EP007      | Cerulean Gym  | Misty     | W      | 1        |
| 3           | EP014      | Vermilion Gym | Lt. Surge | W      | 1        |
| 4           | EP024      | Celadon Gym   | Erika     | W      | 1        |
| 5           | EP032      | Fuchsia Gym   | Koga      | W      | 1        |
| 6           | EP059      | Saffron Gym   | Sabrina   | W      | 1        |
| 7           | EP063      | Cinnabar Gym  | Blaine    | W      | 1        |
| 8           | EP067      | Viridian Gym  | Giovanni  | W      | 1        |
| 9           | EP076      | Indigo League | Ritchie   | L      | 0        |

## 1) Running total with `SUM() OVER`

A regular `SUM()` with `GROUP BY` would collapse all rows into one number. A window function keeps every row intact and adds a cumulative column alongside it.

The key syntax is `OVER (ORDER BY ... ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`. This tells SQL: for each row, sum everything from the first row up to and including this one.

```sql
SELECT
  event_order,
  episode_id,
  event_name,
  opponent,
  result,
  SUM(win_flag) OVER (
    ORDER BY event_order
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_wins,
  SUM(CASE WHEN event_name LIKE '%Gym%' AND result = 'W' THEN 1 ELSE 0 END) OVER (
    ORDER BY event_order
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS badges_collected
FROM kanto_battles
ORDER BY event_order;
```

**Result:**

| event_order | episode_id | event_name    | opponent  | result | running_wins | badges_collected |
|-------------|------------|---------------|-----------|--------|--------------|-----------------|
| 1           | EP005      | Pewter Gym    | Brock     | W      | 1            | 1               |
| 2           | EP007      | Cerulean Gym  | Misty     | W      | 2            | 2               |
| 3           | EP014      | Vermilion Gym | Lt. Surge | W      | 3            | 3               |
| 4           | EP024      | Celadon Gym   | Erika     | W      | 4            | 4               |
| 5           | EP032      | Fuchsia Gym   | Koga      | W      | 5            | 5               |
| 6           | EP059      | Saffron Gym   | Sabrina   | W      | 6            | 6               |
| 7           | EP063      | Cinnabar Gym  | Blaine    | W      | 7            | 7               |
| 8           | EP067      | Viridian Gym  | Giovanni  | W      | 8            | 8               |
| 9           | EP076      | Indigo League | Ritchie   | L      | 8            | 8               |

Row 9 is the key one to look at: the loss does not decrement `running_wins` — it stays at 8 because `win_flag` is 0 for that row. Each row keeps its full episode detail while the cumulative column reflects all prior rows. Compare this to `GROUP BY`: you would get a single row with a total, and all per-episode context would be gone.

## 2) Row comparison with `LAG()`

`LAG(column)` returns the value of that column from the previous row, based on your `ORDER BY`. The first row gets `NULL` because there is no row before it.

This is useful any time you want to compare a current value to what came immediately before it — detecting changes, streaks, or breaks in trend.

```sql
SELECT
  event_order,
  episode_id,
  event_name,
  opponent,
  result,
  LAG(result) OVER (
    ORDER BY event_order
  ) AS previous_result,
  CASE
    WHEN LAG(result) OVER (ORDER BY event_order) = 'W' AND result = 'L' THEN 'Momentum Broken'
    WHEN LAG(result) OVER (ORDER BY event_order) = result THEN 'Steady'
    ELSE 'Shift'
  END AS momentum_state
FROM kanto_battles
ORDER BY event_order;
```

**Result:**

| event_order | episode_id | event_name    | opponent  | result | previous_result | momentum_state  |
|-------------|------------|---------------|-----------|--------|-----------------|-----------------|
| 1           | EP005      | Pewter Gym    | Brock     | W      | NULL            | Shift           |
| 2           | EP007      | Cerulean Gym  | Misty     | W      | W               | Steady          |
| 3           | EP014      | Vermilion Gym | Lt. Surge | W      | W               | Steady          |
| 4           | EP024      | Celadon Gym   | Erika     | W      | W               | Steady          |
| 5           | EP032      | Fuchsia Gym   | Koga      | W      | W               | Steady          |
| 6           | EP059      | Saffron Gym   | Sabrina   | W      | W               | Steady          |
| 7           | EP063      | Cinnabar Gym  | Blaine    | W      | W               | Steady          |
| 8           | EP067      | Viridian Gym  | Giovanni  | W      | W               | Steady          |
| 9           | EP076      | Indigo League | Ritchie   | L      | W               | Momentum Broken |

Row 1 has `NULL` for `previous_result` — there is no prior row to look back at. Rows 2–8 all show `Steady` because the result matches the previous result. Row 9 shows `Momentum Broken`: `LAG()` pulled the prior `W`, and the `CASE` statement detected the W→L transition.
