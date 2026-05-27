---
layout: single
title: "Professor Oak’s SQL Notebook: Ash’s Kanto Run in 2 Window Functions"
date: 2026-05-24 09:00:00 +0000
categories: [data-engineering]
excerpt: "A Pokémon-themed SQL story that teaches window functions with Ash’s Kanto badge journey, momentum swings, and Indigo League ending."
---

Most window function tutorials start with sales tables.

This one starts in Pallet Town.

Professor Oak is reviewing Ash Ketchum’s Kanto season and asks a simple question:

> Can we measure Ash’s progress like a sports analyst, episode by episode, without losing the story?

We only need two window ideas to do that:

1. Running total (`SUM() OVER`) to track the badge climb
2. Previous row comparison (`LAG()`) to show momentum swings

That is enough to tell a complete arc:

- **Start**: Episode 1, Ash and Pikachu are chaos.
- **Middle**: Gym battles from Brock to Giovanni build momentum.
- **End**: Indigo League loss to Ritchie, where Charizard’s disobedience crashes the run.

## The storyline dataset

We model only the moments that move the plot.

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

## 1) Running total: the badge chase arc

This is the cleanest window concept for beginners:

- every row keeps episode-level detail
- but we also layer in Ash’s cumulative progression

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

Narrative payoff:

- After Brock, `badges_collected = 1`
- By Viridian, `badges_collected = 8`
- At Indigo League, the running story is still visible on the same row where it ends

That is why windows work so well for storytelling analytics: no `GROUP BY` collapse, no lost context.

## 2) `LAG()`: the momentum break at Indigo

Now we compare each battle to the battle immediately before it.

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

Narrative payoff:

- The prior row before Ritchie is a win.
- `LAG()` makes the emotional drop measurable: the season was climbing, then momentum snapped.
- In story terms: Charizard’s disobedience was not just “a loss,” it was a break in trend at the worst possible time.

## Why this version is easier to remember

If window functions feel abstract, anchor them to a progression you already know:

- **Running total** = Ash’s badge climb
- **LAG()** = “what changed from last battle?”

One hero, one season, one rise, one collapse.

And that is enough to make window SQL stick.
