---
layout: single
title: "Professor Oak’s SQL Notebook: Ash’s Kanto Run in 2 Window Functions"
date: 2026-05-24 09:00:00 +0000
categories: [data-engineering]
excerpt: "A Pokémon-themed SQL tutorial teaching window functions with SUM() OVER and LAG() against a real dataset."
---

Window functions let you compute aggregates and comparisons across rows — without collapsing your result set the way `GROUP BY` does. The syntax looks unfamiliar at first: `FUNCTION() OVER (ORDER BY ...)` is not something you encounter in basic SQL, and the frame clause (`ROWS BETWEEN ...`) can feel arbitrary until you see it in action.

This tutorial works through two of the most useful window functions using a single dataset. Every query runs against the same table, and every query shows the actual output so you can see exactly what each clause is doing.

The two functions covered:

1. `SUM() OVER` — running totals
2. `LAG()` — comparing each row to the previous one

---

## The dataset: Ash’s Kanto gym run

*Not a Pokémon fan? Here’s what you need to know:* Pokémon is a long-running Nintendo franchise. In the original anime, a ten-year-old kid named Ash Ketchum leaves his hometown with his partner Pokémon (Pikachu) and travels the Kanto region. To qualify for the regional championship (the Indigo League), he has to defeat eight Gym Leaders — each one a specialist trainer controlling a specific gym.

<details>
  <summary>Spoiler details for the Indigo League arc</summary>
  He wins all eight badges, goes to the Indigo League, and loses to a rival named Ritchie in a match where his own Pokémon, Charizard, refuses to battle.
</details>

That arc — eight straight wins followed by one loss at the worst possible moment — is the dataset.

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

Nine rows. Each represents one meaningful battle. `win_flag` is 1 for a win and 0 for a loss — that’s the column the window functions will operate on.

---

## 1) Running total with `SUM() OVER`

A regular `SUM()` with `GROUP BY` would collapse all rows into one number. A window function keeps every row intact and adds a cumulative column alongside it.

The key syntax is `OVER (ORDER BY ... ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`. This tells SQL: for each row, sum everything from the first row up to and including this one.

```sql
SELECT
  event_order,
  event_name,
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

| # | event_name    | result | running_wins | badges_collected |
|---|---------------|--------|--------------|-----------------|
| 1 | Pewter Gym    | W      | 1            | 1               |
| 2 | Cerulean Gym  | W      | 2            | 2               |
| 3 | Vermilion Gym | W      | 3            | 3               |
| 4 | Celadon Gym   | W      | 4            | 4               |
| 5 | Fuchsia Gym   | W      | 5            | 5               |
| 6 | Saffron Gym   | W      | 6            | 6               |
| 7 | Cinnabar Gym  | W      | 7            | 7               |
| 8 | Viridian Gym  | W      | 8            | 8               |
| 9 | Indigo League | L      | 8            | 8               |

Row 9 is the one to look at: the loss does not decrement `running_wins` — it stays at 8 because `win_flag` is 0 for that row, so it contributes nothing to the sum. Each row keeps its full detail while the cumulative column reflects everything up to that point. Compare this to `GROUP BY`: you would get a single row with a total, and all per-event detail would be gone.

---

## 2) Row comparison with `LAG()`

`LAG(column)` returns the value of that column from the previous row, based on your `ORDER BY`. The first row gets `NULL` because there is no row before it.

This is useful any time you want to compare a current value to what came immediately before it — detecting changes, streaks, or breaks in trend.

```sql
SELECT
  event_order,
  event_name,
  result,
  LAG(result) OVER (ORDER BY event_order) AS prev_result,
  CASE
    WHEN LAG(result) OVER (ORDER BY event_order) = 'W' AND result = 'L' THEN 'Momentum Broken'
    WHEN LAG(result) OVER (ORDER BY event_order) = result          THEN 'Steady'
    ELSE 'Shift'
  END AS momentum_state
FROM kanto_battles
ORDER BY event_order;
```

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

Row 1 has `NULL` for `prev_result` — there is no prior row. Rows 2–8 are all `Steady`: the result matches the previous result. Row 9 is the break: `LAG()` pulled the prior `W`, and the `CASE` detected the W→L transition. This is the trend break in a column — eight battles of upward momentum ending at the worst possible moment.
