---
layout: single
title: "Professor Oak’s SQL Notebook: Ash’s Kanto Run in 6 Window Functions"
date: 2026-05-24 09:00:00 +0000
categories: [data-engineering]
excerpt: "A Pokémon-themed SQL tutorial teaching window functions with SUM(), PARTITION BY, frames, ranking, LAG(), and LEAD() on one dataset."
---

Window functions let you compute aggregates and comparisons across rows while keeping each row visible. `GROUP BY` collapses rows. Window functions do not.

The syntax can feel strange at first, so think of it like this:

- `OVER (...)`: your battle rules
- `PARTITION BY ...`: split rows into separate mini-tournaments
- `ORDER BY ...`: the timeline inside each tournament
- `ROWS BETWEEN ...`: how many nearby rows each row can see

This tutorial uses one Pokémon dataset all the way through, so each new concept is a new lens on the same story.

The six concepts covered:

1. `SUM() OVER` — running totals
2. `PARTITION BY` — reset points
3. Window frames (`ROWS BETWEEN`) — rolling windows
4. `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()` — tie behavior
5. `LAG()` — look back one row
6. `LEAD()` — look forward one row

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
      (1,  'EP005', 'Pewter Gym',    'Brock',    'W', 1),
      (2,  'EP007', 'Cerulean Gym',  'Misty',    'W', 1),
      (3,  'EP014', 'Vermilion Gym', 'Lt. Surge','W', 1),
      (4,  'EP024', 'Celadon Gym',   'Erika',    'W', 1),
      (5,  'EP032', 'Fuchsia Gym',   'Koga',     'W', 1),
      (6,  'EP059', 'Saffron Gym',   'Sabrina',  'W', 1),
      (7,  'EP063', 'Cinnabar Gym',  'Blaine',   'W', 1),
      (8,  'EP067', 'Viridian Gym',  'Giovanni', 'W', 1),
      (9,  'EP076', 'Indigo League', 'Ritchie',  'L', 0)
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

A regular `SUM()` with `GROUP BY` collapses everything into one row. A window function keeps every row and adds a cumulative column alongside it.

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

Row 9 stays at 8 — the loss contributes `win_flag = 0`, so it adds nothing. Each row keeps its detail while the cumulative reflects everything up to that point.

---

## 2) `PARTITION BY`: separate scoreboards inside one result

`PARTITION BY` resets the window calculation for each group. Without it, the window spans the entire table. With it, each partition gets its own independent calculation.

Here we split battles into two stages — Gym Circuit and League Stage — and run a separate cumulative win count inside each one.

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

Row 9 resets to 0 because it’s in a different partition. The Gym Circuit total of 8 is unaffected — it belongs to a completely separate calculation.

---

## 3) Window frames: controlling how much each row can see

By default, `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` means every row sees everything from the start. A frame clause lets you narrow that window to just the nearby rows.

This query tracks wins over only the last three battles instead of the full history.

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

Rows 1 and 2 have fewer than 3 prior rows available, so the frame shrinks to fit. Row 9 looks at battles 7, 8, 9: two wins and one loss = 2.

The difference from section 1: section 1 is total career wins. This is current form over the last three outings. A commentator stat, not a career stat.

---

## 4) Ranking functions: tie behavior matters

Three functions look nearly identical but handle ties differently. This trips people up on SQL interviews.

To make the tie behavior visible, we order by `win_flag DESC` — which puts all 8 wins at the top tied together, and the one loss at the bottom.

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

The difference shows up on row 9:

- `ROW_NUMBER`: always unique — gives every row a distinct number (1–9), ties broken by `event_order`
- `RANK`: 8 rows tie for rank 1, so the next rank jumps to 9 (skips 2–8)
- `DENSE_RANK`: 8 rows tie for rank 1, next rank is 2 (no gap)

Interview rule of thumb: if the prompt says “top N per group” and ties matter, the choice between `RANK` and `DENSE_RANK` changes your output.

---

## 5) `LAG()`: look at the previous row

`LAG(column)` returns the value of that column from the row immediately before the current one (by your `ORDER BY`). The first row gets `NULL` — nothing comes before it.

```sql
SELECT
  event_order,
  event_name,
  result,
  LAG(result) OVER (ORDER BY event_order) AS prev_result,
  CASE
    WHEN LAG(result) OVER (ORDER BY event_order) = 'W' AND result = 'L' THEN 'Momentum Broken'
    WHEN LAG(result) OVER (ORDER BY event_order) = result                  THEN 'Steady'
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

Row 1 has `NULL` — no prior row exists. Rows 2–8 match the previous result so they’re `Steady`. Row 9 gets `Momentum Broken`: `LAG()` pulled the prior `W`, and the `CASE` caught the W→L flip.

---

## 6) `LEAD()`: look at the next row

`LEAD(column)` is the forward-looking complement to `LAG()`. Instead of looking back one row, it looks ahead. The last row gets `NULL` — nothing comes after it.

A practical use: knowing what’s coming next lets you flag transitions before they happen. Here we use it to show Ash what opponent is coming up.

```sql
SELECT
  event_order,
  event_name,
  opponent,
  result,
  LEAD(opponent) OVER (ORDER BY event_order) AS next_opponent,
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

Row 9 has `NULL` for both forward-looking columns — the season is over, there is no next event.

`LEAD()` and `LAG()` take the same arguments and work identically, just in opposite directions. You can also pass an offset: `LAG(result, 2)` looks back two rows, `LEAD(result, 2)` looks forward two.

---

## Quick syntax decoder

When you see a window function in the wild:

```sql
FUNCTION(col) OVER (
  PARTITION BY x
  ORDER BY y
  ROWS BETWEEN a PRECEDING AND b FOLLOWING
)
```

Read it in this order:

1. Which group? (`PARTITION BY`)
2. What order? (`ORDER BY`)
3. How much of that order can this row see? (`ROWS BETWEEN`)
4. What calculation on that slice? (`FUNCTION`)
