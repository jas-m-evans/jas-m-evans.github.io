---
layout: single
title: "Professor Oak’s SQL Notebook: Ash’s Kanto Run in 5 Window Functions"
date: 2026-05-24 09:00:00 +0000
categories: [data-engineering]
excerpt: "A Pokémon-themed SQL tutorial teaching window functions with SUM(), LAG(), PARTITION BY, frames, and ranking on one dataset."
---

Window functions let you compute aggregates and comparisons across rows while keeping each row visible. `GROUP BY` collapses rows. Window functions do not.

The syntax can feel strange at first, so think of it like this:

- `OVER (...)`: your battle rules
- `PARTITION BY ...`: split matches into separate mini tournaments
- `ORDER BY ...`: the timeline inside each tournament
- `ROWS BETWEEN ...`: how many nearby matches you want to include

This tutorial uses one Pokémon dataset all the way through, so each new concept feels like a new lens on the same story.

The five concepts covered:

1. `SUM() OVER` for running totals
2. `PARTITION BY` for reset points
3. Window frames (`ROWS BETWEEN ...`) for rolling windows
4. `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()` for leaderboard behavior
5. `LAG()` for row to row comparison

---

## The dataset: Ash’s Kanto journey

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

Think of this as Professor Oak updating Ash’s badge notebook after every battle.

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

`UNBOUNDED PRECEDING` means start from Ash’s first battle. `CURRENT ROW` means stop at this battle.

So at battle 9, `running_wins` stays 8, because the league loss adds 0.

---

## 2) `PARTITION BY`: split one table into mini tournaments

`PARTITION BY` is the clause people usually find weird. Simple version: it creates separate scoreboards inside one result set.

In this story, we can split battles into:

- Gym Circuit
- League Stage

```sql
SELECT
  event_order,
  event_name,
  CASE
    WHEN event_name LIKE '%Gym%' THEN 'Gym Circuit'
    ELSE 'League Stage'
  END AS battle_stage,
  win_flag,
  SUM(win_flag) OVER (
    PARTITION BY CASE WHEN event_name LIKE '%Gym%' THEN 'Gym Circuit' ELSE 'League Stage' END
    ORDER BY event_order
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS stage_running_wins
FROM kanto_battles
ORDER BY event_order;
```

What happens:

- Rows 1 to 8 are in one partition, so that total climbs from 1 to 8
- Row 9 is in a different partition, so its running total starts fresh and is 0

Memory trick: `PARTITION BY` is like Nurse Joy opening separate boxes in the PC. Same table, separate storage boxes.

---

## 3) Window frame: local momentum instead of full history

You mentioned "quorum or something." In window function land, people often mean the frame clause, which decides how much of the timeline each row can see.

This query tracks Ash’s momentum over only the latest three battles.

```sql
SELECT
  event_order,
  event_name,
  result,
  SUM(win_flag) OVER (
    ORDER BY event_order
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
  ) AS wins_last_3_battles
FROM kanto_battles
ORDER BY event_order;
```

`2 PRECEDING` + `CURRENT ROW` means a 3-battle window.

At battle 9, SQL looks at battles 7, 8, and 9 only. Output is 2.

Memory trick: this is like a commentator saying, "Forget old seasons. Show me current form."

---

## 4) Ranking functions: tie behavior matters

A lot of harder SQL questions test tie handling. These three functions look similar but produce different ranks.

```sql
SELECT
  event_order,
  event_name,
  CASE WHEN event_name LIKE '%Gym%' THEN 1 ELSE 3 END AS stakes_level,
  ROW_NUMBER() OVER (
    ORDER BY CASE WHEN event_name LIKE '%Gym%' THEN 1 ELSE 3 END DESC, event_order
  ) AS row_num,
  RANK() OVER (
    ORDER BY CASE WHEN event_name LIKE '%Gym%' THEN 1 ELSE 3 END DESC
  ) AS rank_with_gaps,
  DENSE_RANK() OVER (
    ORDER BY CASE WHEN event_name LIKE '%Gym%' THEN 1 ELSE 3 END DESC
  ) AS dense_rank_no_gaps
FROM kanto_battles
ORDER BY event_order;
```

How to remember:

- `ROW_NUMBER()`: every row gets a unique jersey number
- `RANK()`: tied trainers share a place, next place skips a number
- `DENSE_RANK()`: tied trainers share a place, next place does not skip

Anime memory: tournament podium rules. If two trainers tie for second, `RANK()` jumps to fourth. `DENSE_RANK()` goes to third.

---

## 5) `LAG()`: compare this battle to the previous one

`LAG()` pulls data from the previous row in the same ordered window.

```sql
SELECT
  event_order,
  event_name,
  result,
  LAG(result) OVER (ORDER BY event_order) AS prev_result,
  CASE
    WHEN LAG(result) OVER (ORDER BY event_order) = 'W' AND result = 'L' THEN 'Momentum Broken'
    WHEN LAG(result) OVER (ORDER BY event_order) = result THEN 'Steady'
    ELSE 'Shift'
  END AS momentum_state
FROM kanto_battles
ORDER BY event_order;
```

Battle 1 has no previous row, so `prev_result` is `NULL`. Battle 9 becomes `Momentum Broken`.

Memory trick: `LAG()` is Brock walking behind Ash and reporting, "Last battle result was W."

---

## Fast syntax decoder for `OVER (...)`

When you see this in a problem:

```sql
FUNCTION(col) OVER (
  PARTITION BY x
  ORDER BY y
  ROWS BETWEEN a PRECEDING AND b FOLLOWING
)
```

Read it in this order:

1. Which mini tournament? (`PARTITION BY`)
2. What timeline? (`ORDER BY`)
3. How much of that timeline can this row see? (`ROWS BETWEEN ...`)
4. What math should we do on that visible slice? (`FUNCTION`)

If you decode in that order, scary window syntax becomes a repeatable checklist.
