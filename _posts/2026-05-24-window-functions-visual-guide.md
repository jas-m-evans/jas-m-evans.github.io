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

Each section below uses a **different dataset** pulled from Ash’s Kanto journey. Same story, ten different lenses.

**10 concepts covered:**

1. `SUM() OVER` — running totals (`badge_journey`)
2. `PARTITION BY` — independent group calculations (`team_battles`)
3. `ROWS BETWEEN` — rolling windows (`road_encounters`)
4. `RANGE BETWEEN` vs `ROWS BETWEEN` — value vs row-count frames (`gym_tiers`)
5. `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()` — tie behavior (`gym_rankings`)
6. `LAG()` — look back one row (`pikachu_battles`)
7. `LEAD()` — look forward one row (`kanto_route`)
8. `FIRST_VALUE()` / `LAST_VALUE()` — partition anchors (`pokemon_team`)
9. `NTILE(n)` — bucketing into equal groups (`team_power`)
10. Islands and gaps — detecting consecutive sequences (`training_sessions`)

---

> **⚠️ Spoiler warning:** the datasets below reveal how Ash’s Kanto season ends.

<details>
  <summary>Not a Pokémon fan? Quick context (spoilers)</summary>
  Ash Ketchum is a ten-year-old trainer who travels the Kanto region with his partner Pikachu. To qualify for the regional championship — the Indigo League — he has to defeat eight Gym Leaders and earn their badges. He wins all eight, makes it to the Indigo League, and loses to a rival named Ritchie when his own Pokémon, Charizard, refuses to battle.
</details>

---

## 1) Running total with `SUM() OVER`

**Dataset: `badge_journey`** — Ash’s eight gym battles plus the Indigo League final. One row per match.

```sql
WITH badge_journey AS (
  SELECT * FROM (
    VALUES
      (1, 'EP005', 'Pewter Gym',    'Brock',    'Boulder Badge', 1),
      (2, 'EP007', 'Cerulean Gym',  'Misty',    'Cascade Badge', 1),
      (3, 'EP014', 'Vermilion Gym', 'Lt. Surge','Thunder Badge', 1),
      (4, 'EP024', 'Celadon Gym',   'Erika',    'Rainbow Badge', 1),
      (5, 'EP032', 'Fuchsia Gym',   'Koga',     'Soul Badge',    1),
      (6, 'EP059', 'Saffron Gym',   'Sabrina',  'Marsh Badge',   1),
      (7, 'EP063', 'Cinnabar Gym',  'Blaine',   'Volcano Badge', 1),
      (8, 'EP067', 'Viridian Gym',  'Giovanni', 'Earth Badge',   1),
      (9, 'EP079', 'Indigo League', 'Ritchie',  NULL,             0)
  ) AS t(battle_id, episode, venue, opponent, badge_earned, win_flag)
)
SELECT * FROM badge_journey;
```

| # | venue          | opponent  | badge_earned  | win_flag |
|---|----------------|-----------|---------------|----------|
| 1 | Pewter Gym     | Brock     | Boulder Badge | 1        |
| 2 | Cerulean Gym   | Misty     | Cascade Badge | 1        |
| 3 | Vermilion Gym  | Lt. Surge | Thunder Badge | 1        |
| 4 | Celadon Gym    | Erika     | Rainbow Badge | 1        |
| 5 | Fuchsia Gym    | Koga      | Soul Badge    | 1        |
| 6 | Saffron Gym    | Sabrina   | Marsh Badge   | 1        |
| 7 | Cinnabar Gym   | Blaine    | Volcano Badge | 1        |
| 8 | Viridian Gym   | Giovanni  | Earth Badge   | 1        |
| 9 | Indigo League  | Ritchie   | NULL          | 0        |

A regular `SUM()` with `GROUP BY` collapses all rows into one total. A window function keeps every row and adds a cumulative column alongside it.

```sql
SELECT
  battle_id,
  venue,
  opponent,
  result,
  SUM(win_flag) OVER (
    ORDER BY battle_id
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS badges_so_far
FROM badge_journey
ORDER BY battle_id;
```

`UNBOUNDED PRECEDING` means start from the very first row. `CURRENT ROW` means stop here. For every row, SQL sums `win_flag` from row 1 up to and including the current row.

**Result:**

| # | venue          | opponent  | result | badges_so_far |
|---|----------------|-----------|--------|---------------|
| 1 | Pewter Gym     | Brock     | W      | 1             |
| 2 | Cerulean Gym   | Misty     | W      | 2             |
| 3 | Vermilion Gym  | Lt. Surge | W      | 3             |
| 4 | Celadon Gym    | Erika     | W      | 4             |
| 5 | Fuchsia Gym    | Koga      | W      | 5             |
| 6 | Saffron Gym    | Sabrina   | W      | 6             |
| 7 | Cinnabar Gym   | Blaine    | W      | 7             |
| 8 | Viridian Gym   | Giovanni  | W      | 8             |
| 9 | Indigo League  | Ritchie   | L      | 8             |

Row 9: the Indigo League loss adds `win_flag = 0` so `badges_so_far` stays at 8. Every row keeps its full context — you can see the badge name, the opponent, and the running total all on the same row.

---

## 2) `PARTITION BY`: independent calculations per group

**Dataset: `team_battles`** — selected battles from Ash’s four main Pokémon across the journey, ordered by episode.

```sql
WITH team_battles AS (
  SELECT * FROM (
    VALUES
      (1,  'EP001', 'Pikachu',   'Spearow', 'W', 1),
      (2,  'EP005', 'Pikachu',   'Onix',    'W', 1),
      (3,  'EP007', 'Bulbasaur', 'Staryu',  'W', 1),
      (4,  'EP011', 'Pikachu',   'Rhyhorn', 'W', 1),
      (5,  'EP014', 'Pikachu',   'Raichu',  'W', 1),
      (6,  'EP024', 'Bulbasaur', 'Gloom',   'W', 1),
      (7,  'EP032', 'Bulbasaur', 'Koffing', 'W', 1),
      (8,  'EP059', 'Squirtle',  'Haunter', 'W', 1),
      (9,  'EP063', 'Charizard', 'Magmar',  'W', 1),
      (10, 'EP067', 'Squirtle',  'Rhyhorn', 'W', 1),
      (11, 'EP079', 'Pikachu',   'Sparky',  'W', 1),
      (12, 'EP079', 'Charizard', 'Zippo',   'L', 0)
  ) AS t(battle_id, episode, pokemon, opponent, result, win_flag)
)
SELECT * FROM team_battles;
```

`PARTITION BY` resets the window calculation for each group. Without it, a running total spans the whole table. With it, each Pokémon gets its own independent count.

```sql
SELECT
  battle_id,
  pokemon,
  opponent,
  result,
  SUM(win_flag) OVER (
    PARTITION BY pokemon
    ORDER BY battle_id
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS pokemon_wins
FROM team_battles
ORDER BY battle_id;
```

**Result:**

| # | pokemon   | opponent | result | pokemon_wins |
|---|-----------|----------|--------|--------------|
| 1 | Pikachu   | Spearow  | W      | 1            |
| 2 | Pikachu   | Onix     | W      | 2            |
| 3 | Bulbasaur | Staryu   | W      | 1            |
| 4 | Pikachu   | Rhyhorn  | W      | 3            |
| 5 | Pikachu   | Raichu   | W      | 4            |
| 6 | Bulbasaur | Gloom    | W      | 2            |
| 7 | Bulbasaur | Koffing  | W      | 3            |
| 8 | Squirtle  | Haunter  | W      | 1            |
| 9 | Charizard | Magmar   | W      | 1            |
| 10| Squirtle  | Rhyhorn  | W      | 2            |
| 11| Pikachu   | Sparky   | W      | 5            |
| 12| Charizard | Zippo    | L      | 1            |

Each Pokémon’s `pokemon_wins` counter resets independently. Pikachu climbs from 1 to 5. Bulbasaur goes 1–2–3. Charizard’s loss on row 12 adds nothing — it stays at 1. Without `PARTITION BY`, Charizard’s wins would be added to the global running total and you’d lose the per-Pokémon breakdown.

---

## 3) `ROWS BETWEEN`: rolling windows

**Dataset: `road_encounters`** — Ash’s trainer battles on the roads between gyms, in episode order.

```sql
WITH road_encounters AS (
  SELECT * FROM (
    VALUES
      (1,  'EP002', 'Route 1',       'Bug Catcher', 'W', 1),
      (2,  'EP003', 'Viridian Forest','Youngster',   'W', 1),
      (3,  'EP006', 'Mt. Moon',      'Rocket Grunt','W', 1),
      (4,  'EP008', 'Route 3',       'Lass',        'L', 0),
      (5,  'EP009', 'Route 3',       'Bug Catcher', 'W', 1),
      (6,  'EP010', 'Route 4',       'Youngster',   'W', 1),
      (7,  'EP016', 'Route 6',       'Hiker',       'L', 0),
      (8,  'EP017', 'Route 7',       'Lass',        'W', 1),
      (9,  'EP020', 'Route 8',       'Youngster',   'W', 1),
      (10, 'EP025', 'Route 9',       'Hiker',       'W', 1),
      (11, 'EP033', 'Route 15',      'Bird Keeper', 'L', 0),
      (12, 'EP040', 'Route 16',      'Bug Catcher', 'W', 1)
  ) AS t(enc_id, episode, route, trainer_class, result, win_flag)
)
SELECT * FROM road_encounters;
```

By default `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` makes every row look all the way back to the start. Changing the frame lets you narrow that to just the nearby rows — a “current form” stat rather than a career stat.

```sql
SELECT
  enc_id,
  route,
  trainer_class,
  result,
  SUM(win_flag) OVER (
    ORDER BY enc_id
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
  ) AS wins_last_3
FROM road_encounters
ORDER BY enc_id;
```

`2 PRECEDING` + `CURRENT ROW` = a 3-row window. At each row, SQL sums at most 2 rows back plus the current one.

**Result:**

| # | route          | trainer_class | result | wins_last_3 |
|---|----------------|---------------|--------|-------------|
| 1 | Route 1        | Bug Catcher   | W      | 1           |
| 2 | Viridian Forest| Youngster     | W      | 2           |
| 3 | Mt. Moon       | Rocket Grunt  | W      | 3           |
| 4 | Route 3        | Lass          | L      | 2           |
| 5 | Route 3        | Bug Catcher   | W      | 2           |
| 6 | Route 4        | Youngster     | W      | 2           |
| 7 | Route 6        | Hiker         | L      | 2           |
| 8 | Route 7        | Lass          | W      | 2           |
| 9 | Route 8        | Youngster     | W      | 2           |
| 10| Route 9        | Hiker         | W      | 3           |
| 11| Route 15       | Bird Keeper   | L      | 2           |
| 12| Route 16       | Bug Catcher   | W      | 2           |

Rows 1 and 2 have fewer than 3 prior rows so the frame shrinks to fit. Row 3 is the first to see a full 3-battle window (all wins = 3). Row 10 is the next clean 3 after the mid-journey slump. Row 11’s loss pulls `wins_last_3` back to 2.

---

## 4) `RANGE BETWEEN` vs `ROWS BETWEEN`

**Dataset: `gym_tiers`** — the same nine battles as `badge_journey`, but now each battle has a `difficulty_tier` (1 = early Kanto, 2 = mid, 3 = late/final).

```sql
WITH gym_tiers AS (
  SELECT * FROM (
    VALUES
      (1, 'EP005', 'Brock',    1, 1),
      (2, 'EP007', 'Misty',    1, 1),
      (3, 'EP014', 'Lt. Surge',1, 1),
      (4, 'EP024', 'Erika',    2, 1),
      (5, 'EP032', 'Koga',     2, 1),
      (6, 'EP059', 'Sabrina',  3, 1),
      (7, 'EP063', 'Blaine',   3, 1),
      (8, 'EP067', 'Giovanni', 3, 1),
      (9, 'EP079', 'Ritchie',  3, 0)
  ) AS t(battle_id, episode, opponent, difficulty_tier, win_flag)
)
SELECT * FROM gym_tiers;
```

`ROWS BETWEEN` counts **physical rows**. `RANGE BETWEEN` counts **logical values** — it includes all rows whose `ORDER BY` value falls within a numeric range of the current row’s value. The difference is invisible when `ORDER BY` has no duplicates. When it does, they behave very differently.

```sql
SELECT
  opponent,
  difficulty_tier,
  win_flag,
  SUM(win_flag) OVER (
    ORDER BY difficulty_tier
    ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
  ) AS rows_sum,
  SUM(win_flag) OVER (
    ORDER BY difficulty_tier
    RANGE BETWEEN 1 PRECEDING AND 1 FOLLOWING
  ) AS range_sum
FROM gym_tiers
ORDER BY difficulty_tier, battle_id;
```

**Result:**

| opponent  | difficulty_tier | win_flag | rows_sum | range_sum |
|-----------|-----------------|----------|----------|-----------|
| Brock     | 1               | 1        | 2        | 5         |
| Misty     | 1               | 1        | 3        | 5         |
| Lt. Surge | 1               | 1        | 3        | 5         |
| Erika     | 2               | 1        | 3        | 8         |
| Koga      | 2               | 1        | 3        | 8         |
| Sabrina   | 3               | 1        | 3        | 5         |
| Blaine    | 3               | 1        | 3        | 5         |
| Giovanni  | 3               | 1        | 2        | 5         |
| Ritchie   | 3               | 0        | 1        | 5         |

**`rows_sum`** moves like a sliding physical window of 3 rows. Brock has no preceding row so it starts at 2. Giovanni and Ritchie trail off at the end.

**`range_sum`** uses the difficulty_tier value itself. For a tier-2 row, `RANGE BETWEEN 1 PRECEDING AND 1 FOLLOWING` means: include all rows where `difficulty_tier` is between 1 and 3 — that’s every row in the table (9 rows, 8 wins). For a tier-1 row the range is 0–2, capturing tiers 1 and 2 (5 rows, all wins = 5). For tier-3, it’s 2–4, capturing tiers 2 and 3 (6 rows, one loss = 5).

Notice `range_sum` is the same for every row **within the same tier** because they all share the same `ORDER BY` value. `rows_sum` varies by physical position. This is the core distinction: RANGE is group-aware, ROWS is position-aware.

**When this matters in practice:** rolling 7-day windows on date columns. `RANGE BETWEEN INTERVAL '6 DAYS' PRECEDING AND CURRENT ROW` includes all rows within the past 6 calendar days regardless of gaps. `ROWS BETWEEN 6 PRECEDING` always grabs exactly 7 physical rows regardless of what dates they cover.

---

## 5) Ranking functions: tie behavior matters

**Dataset: `gym_rankings`** — the nine battles rated by `difficulty_score`, a subjective measure of how hard each fight was. Brock and Misty share a score of 4; Blaine and Ritchie share 7.

```sql
WITH gym_rankings AS (
  SELECT * FROM (
    VALUES
      (1, 'EP005', 'Brock',     'Rock',     4, 1),
      (2, 'EP007', 'Misty',     'Water',    4, 1),
      (3, 'EP014', 'Lt. Surge', 'Electric', 5, 1),
      (4, 'EP024', 'Erika',     'Grass',    3, 1),
      (5, 'EP032', 'Koga',      'Poison',   6, 1),
      (6, 'EP059', 'Sabrina',   'Psychic',  8, 1),
      (7, 'EP063', 'Blaine',    'Fire',     7, 1),
      (8, 'EP067', 'Giovanni',  'Ground',   9, 1),
      (9, 'EP079', 'Ritchie',   'Mixed',    7, 0)
  ) AS t(battle_id, episode, opponent, specialty, difficulty_score, win_flag)
)
SELECT * FROM gym_rankings;
```

```sql
SELECT
  opponent,
  specialty,
  difficulty_score,
  ROW_NUMBER() OVER (ORDER BY difficulty_score DESC, battle_id) AS row_num,
  RANK()       OVER (ORDER BY difficulty_score DESC)            AS rnk,
  DENSE_RANK() OVER (ORDER BY difficulty_score DESC)            AS dense_rnk
FROM gym_rankings
ORDER BY difficulty_score DESC, battle_id;
```

**Result:**

| opponent  | specialty | score | row_num | rnk | dense_rnk |
|-----------|-----------|-------|---------|-----|-----------|
| Giovanni  | Ground    | 9     | 1       | 1   | 1         |
| Sabrina   | Psychic   | 8     | 2       | 2   | 2         |
| Blaine    | Fire      | 7     | 3       | 3   | 3         |
| Ritchie   | Mixed     | 7     | 4       | 3   | 3         |
| Koga      | Poison    | 6     | 5       | 5   | 4         |
| Lt. Surge | Electric  | 5     | 6       | 6   | 5         |
| Brock     | Rock      | 4     | 7       | 7   | 6         |
| Misty     | Water     | 4     | 8       | 7   | 6         |
| Erika     | Grass     | 3     | 9       | 9   | 7         |

Two sets of ties expose the difference clearly:

**Blaine and Ritchie (score=7):** `RANK` gives both a 3, then jumps to 5 for Koga (rank 4 is skipped). `DENSE_RANK` gives both a 3, then 4 for Koga (no gap).

**Brock and Misty (score=4):** `RANK` gives both a 7, then jumps to 9 for Erika (rank 8 skipped). `DENSE_RANK` gives both a 6, then 7.

`ROW_NUMBER` always produces a unique number — it uses the secondary `ORDER BY battle_id` to break ties, so Blaine (EP063) gets 3 and Ritchie (EP079) gets 4.

**Interview rule:** when a problem says “top N per group,” the wrong choice silently produces wrong output. If two opponents tie for 3rd and the question asks for top-3, `RANK` may return no row at position 3 for some groups if ties push it past N. `DENSE_RANK` is the safe default.

---

## 6) `LAG()`: look at the previous row

**Dataset: `pikachu_battles`** — Pikachu’s key battles across the Kanto season, tracking HP remaining after each fight.

```sql
WITH pikachu_battles AS (
  SELECT * FROM (
    VALUES
      (1, 'EP001', 'Route 1',      'Spearow flock','W', 45),
      (2, 'EP005', 'Pewter Gym',   'Onix',         'W', 20),
      (3, 'EP007', 'Cerulean Gym', 'Starmie',      'L',  0),
      (4, 'EP014', 'Vermilion Gym','Raichu',       'W', 15),
      (5, 'EP032', 'Fuchsia Gym',  'Electrode',    'W', 30),
      (6, 'EP059', 'Saffron Gym',  'Kadabra',      'W', 25),
      (7, 'EP067', 'Viridian Gym', 'Rhyhorn',      'W', 38),
      (8, 'EP079', 'Indigo League','Sparky',       'W',  8)
  ) AS t(battle_id, episode, location, opponent, result, hp_after)
)
SELECT * FROM pikachu_battles;
```

`LAG(column)` returns the value of that column from the previous row. The first row gets `NULL` — nothing precedes it.

```sql
SELECT
  battle_id,
  location,
  result,
  hp_after,
  LAG(hp_after) OVER (ORDER BY battle_id)                   AS prev_hp,
  hp_after - LAG(hp_after) OVER (ORDER BY battle_id)        AS hp_change,
  CASE
    WHEN LAG(hp_after) OVER (ORDER BY battle_id) IS NULL    THEN 'First Battle'
    WHEN hp_after > LAG(hp_after) OVER (ORDER BY battle_id) THEN 'Recovered'
    ELSE 'Drained'
  END AS condition
FROM pikachu_battles
ORDER BY battle_id;
```

**Result:**

| # | location      | result | hp_after | prev_hp | hp_change | condition   |
|---|---------------|--------|----------|---------|-----------|-------------|
| 1 | Route 1       | W      | 45       | NULL    | NULL      | First Battle|
| 2 | Pewter Gym    | W      | 20       | 45      | -25       | Drained     |
| 3 | Cerulean Gym  | L      | 0        | 20      | -20       | Drained     |
| 4 | Vermilion Gym | W      | 15       | 0       | +15       | Recovered   |
| 5 | Fuchsia Gym   | W      | 30       | 15      | +15       | Recovered   |
| 6 | Saffron Gym   | W      | 25       | 30      | -5        | Drained     |
| 7 | Viridian Gym  | W      | 38       | 25      | +13       | Recovered   |
| 8 | Indigo League | W      | 8        | 38      | -26       | Drained     |

Row 1 has `NULL` because there is no prior battle. The worst single-battle HP drop (-26) happens at the Indigo League final — the toughest fight even though Pikachu wins. Row 3 (Cerulean) drops to 0, the only loss.

`LAG()` also accepts an offset: `LAG(hp_after, 2)` looks back two rows. The second argument defaults to 1.

---

## 7) `LEAD()`: look at the next row

**Dataset: `kanto_route`** — every major stop on Ash’s journey through Kanto, in travel order.

```sql
WITH kanto_route AS (
  SELECT * FROM (
    VALUES
      (1,  'EP001', 'Pallet Town',    'Receives Pikachu from Prof. Oak'),
      (2,  'EP001', 'Route 1',        'First wild Pokémon encounter'),
      (3,  'EP003', 'Viridian Forest','Catches Caterpie and Pidgeotto'),
      (4,  'EP005', 'Pewter City',    'Earns Boulder Badge from Brock'),
      (5,  'EP006', 'Mt. Moon',       'Battles Team Rocket at Moon Stone'),
      (6,  'EP007', 'Cerulean City',  'Earns Cascade Badge from Misty'),
      (7,  'EP014', 'Vermilion City', 'Earns Thunder Badge from Lt. Surge'),
      (8,  'EP024', 'Celadon City',   'Earns Rainbow Badge from Erika'),
      (9,  'EP032', 'Fuchsia City',   'Earns Soul Badge from Koga'),
      (10, 'EP059', 'Saffron City',   'Earns Marsh Badge from Sabrina'),
      (11, 'EP063', 'Cinnabar Island','Earns Volcano Badge from Blaine'),
      (12, 'EP067', 'Viridian City',  'Earns Earth Badge from Giovanni'),
      (13, 'EP079', 'Indigo Plateau', 'Loses to Ritchie in Top 16')
  ) AS t(stop_order, episode, location, key_event)
)
SELECT * FROM kanto_route;
```

`LEAD(column)` returns the value from the row immediately after the current one. The last row gets `NULL` — nothing follows it. It is the forward-looking complement to `LAG()`.

```sql
SELECT
  stop_order,
  location,
  key_event,
  LEAD(location)  OVER (ORDER BY stop_order) AS next_stop,
  LEAD(episode)   OVER (ORDER BY stop_order) AS next_episode
FROM kanto_route
ORDER BY stop_order;
```

**Result:**

| # | location       | key_event                         | next_stop       | next_episode |
|---|----------------|-----------------------------------|-----------------|--------------|
| 1 | Pallet Town    | Receives Pikachu from Prof. Oak   | Route 1         | EP001        |
| 2 | Route 1        | First wild Pokémon encounter          | Viridian Forest | EP003        |
| 3 | Viridian Forest| Catches Caterpie and Pidgeotto    | Pewter City     | EP005        |
| 4 | Pewter City    | Earns Boulder Badge from Brock    | Mt. Moon        | EP006        |
| 5 | Mt. Moon       | Battles Team Rocket at Moon Stone | Cerulean City   | EP007        |
| 6 | Cerulean City  | Earns Cascade Badge from Misty    | Vermilion City  | EP014        |
| 7 | Vermilion City | Earns Thunder Badge from Lt. Surge| Celadon City    | EP024        |
| 8 | Celadon City   | Earns Rainbow Badge from Erika    | Fuchsia City    | EP032        |
| 9 | Fuchsia City   | Earns Soul Badge from Koga        | Saffron City    | EP059        |
| 10| Saffron City   | Earns Marsh Badge from Sabrina    | Cinnabar Island | EP063        |
| 11| Cinnabar Island| Earns Volcano Badge from Blaine   | Viridian City   | EP067        |
| 12| Viridian City  | Earns Earth Badge from Giovanni   | Indigo Plateau  | EP079        |
| 13| Indigo Plateau | Loses to Ritchie in Top 16        | NULL            | NULL         |

Row 13 gets `NULL` for both forward columns — the journey is over. `LEAD()` takes the same arguments as `LAG()`. `LEAD(location, 2)` would return the stop two rows ahead.

---

## 8) `FIRST_VALUE()` and `LAST_VALUE()`: partition anchors

**Dataset: `pokemon_team`** — every Pokémon Ash caught during Kanto, in the order he caught them.

```sql
WITH pokemon_team AS (
  SELECT * FROM (
    VALUES
      (1, 'EP001', 'Pikachu',   'Pallet Town',     'Electric'),
      (2, 'EP003', 'Caterpie',  'Viridian Forest', 'Bug'),
      (3, 'EP003', 'Pidgeotto', 'Viridian Forest', 'Flying'),
      (4, 'EP010', 'Bulbasaur', 'Melanie\'s Village','Grass'),
      (5, 'EP011', 'Charmander','Route 24',         'Fire'),
      (6, 'EP012', 'Squirtle',  'Vermilion City',  'Water'),
      (7, 'EP029', 'Primeape',  'Route 23',         'Fighting'),
      (8, 'EP031', 'Muk',       'Gringey City',     'Poison')
  ) AS t(catch_order, episode, pokemon, location, type)
)
SELECT * FROM pokemon_team;
```

`FIRST_VALUE(column)` returns the first value of that column in the window. `LAST_VALUE(column)` returns the last.

**The `LAST_VALUE` trap — the most common mistake with these functions:**

The default frame is `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`. For `LAST_VALUE` this means “the last value seen so far” which is always just the current row. That’s almost never what you want.

```sql
SELECT
  catch_order,
  pokemon,
  location,
  FIRST_VALUE(pokemon) OVER (ORDER BY catch_order)                                                    AS first_catch,
  LAST_VALUE(pokemon)  OVER (ORDER BY catch_order)                                                    AS last_val_wrong,
  LAST_VALUE(pokemon)  OVER (ORDER BY catch_order ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_val_correct
FROM pokemon_team
ORDER BY catch_order;
```

**Result:**

| # | pokemon    | location          | first_catch | last_val_wrong | last_val_correct |
|---|------------|-------------------|-------------|----------------|------------------|
| 1 | Pikachu    | Pallet Town       | Pikachu     | Pikachu        | Muk              |
| 2 | Caterpie   | Viridian Forest   | Pikachu     | Caterpie       | Muk              |
| 3 | Pidgeotto  | Viridian Forest   | Pikachu     | Pidgeotto      | Muk              |
| 4 | Bulbasaur  | Melanie's Village| Pikachu     | Bulbasaur      | Muk              |
| 5 | Charmander | Route 24          | Pikachu     | Charmander     | Muk              |
| 6 | Squirtle   | Vermilion City    | Pikachu     | Squirtle       | Muk              |
| 7 | Primeape   | Route 23          | Pikachu     | Primeape       | Muk              |
| 8 | Muk        | Gringey City      | Pikachu     | Muk            | Muk              |

`first_catch` is always `Pikachu` — `FIRST_VALUE` works correctly with the default frame because it’s anchored at the start.

`last_val_wrong` just returns the current row’s Pokémon — not the last in the partition but the last in the current frame, which with the default frame is always the current row itself.

`last_val_correct` extends the frame to `UNBOUNDED FOLLOWING` so every row can see the entire partition and correctly returns `Muk` everywhere.

**Practical alternative:** to avoid the trap, use `FIRST_VALUE` with a reversed `ORDER BY DESC` instead of `LAST_VALUE`. Same result, no frame adjustment needed.

---

## 9) `NTILE(n)`: divide rows into equal buckets

**Dataset: `team_power`** — Ash’s eight Kanto Pokémon with their end-of-season battle records.

```sql
WITH team_power AS (
  SELECT * FROM (
    VALUES
      ('Pikachu',   'Electric', 28, 21),
      ('Charizard', 'Fire',     15, 10),
      ('Bulbasaur', 'Grass',    12,  8),
      ('Squirtle',  'Water',     9,  7),
      ('Primeape',  'Fighting',  6,  5),
      ('Pidgeotto', 'Flying',    8,  5),
      ('Butterfree','Bug',       7,  4),
      ('Muk',       'Poison',    5,  3)
  ) AS t(pokemon, type, battles, wins)
)
SELECT * FROM team_power;
```

`NTILE(n)` splits rows into n as-equal-as-possible buckets and assigns each row a bucket number. Here we divide the team into four tiers by total wins.

```sql
SELECT
  pokemon,
  type,
  battles,
  wins,
  NTILE(4) OVER (ORDER BY wins DESC) AS power_tier
FROM team_power
ORDER BY wins DESC;
```

**Result:**

| pokemon    | type     | battles | wins | power_tier |
|------------|----------|---------|------|------------|
| Pikachu    | Electric | 28      | 21   | 1          |
| Charizard  | Fire     | 15      | 10   | 1          |
| Bulbasaur  | Grass    | 12      | 8    | 2          |
| Squirtle   | Water    | 9       | 7    | 2          |
| Primeape   | Fighting | 6       | 5    | 3          |
| Pidgeotto  | Flying   | 8       | 5    | 3          |
| Butterfree | Bug      | 7       | 4    | 4          |
| Muk        | Poison   | 5       | 3    | 4          |

8 rows into 4 buckets = 2 per tier, clean split. Tier 1 is the carry duo (Pikachu and Charizard). Tier 4 is the support pair. Primeape and Pidgeotto tie at 5 wins but NTILE doesn’t care about ties the way `RANK` does — it just fills buckets evenly.

If the rows don’t divide evenly, the earlier buckets get the extra row. A common real-world use: `NTILE(100)` as an approximation of percentile rank, or wrapping in a CTE and filtering `WHERE power_tier = 1` to get the top 25%.

---

## 10) Islands and gaps: detecting consecutive sequences

**Dataset: `training_sessions`** — the days in October that Ash logged a training session. Gaps represent travel days between towns where no formal training happened.

```sql
WITH training_sessions AS (
  SELECT * FROM (
    VALUES (1), (2), (3), (5), (6), (10), (11), (12)
  ) AS t(day_num)
)
SELECT * FROM training_sessions;
```

| day_num |
|---------|
| 1       |
| 2       |
| 3       |
| 5       |
| 6       |
| 10      |
| 11      |
| 12      |

This is the hardest and most-praised window function pattern in SQL interviews. The question is: find each consecutive training streak.

**The core trick:** for a sequence to be consecutive, the difference between the value and its row number stays constant within the same run. When there’s a gap, that constant changes.

```sql
WITH training_sessions AS (
  SELECT * FROM (
    VALUES (1), (2), (3), (5), (6), (10), (11), (12)
  ) AS t(day_num)
)
SELECT
  day_num,
  ROW_NUMBER() OVER (ORDER BY day_num)           AS rn,
  day_num - ROW_NUMBER() OVER (ORDER BY day_num) AS group_id
FROM training_sessions;
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

Days 1, 2, 3 all produce `group_id = 0` — consecutive days increment by 1 and so does the row number, so the difference stays constant. Day 5 jumps to `group_id = 1` because day 4 is missing. Days 10–12 share `group_id = 4`.

Now aggregate by `group_id` to get each streak:

```sql
WITH training_sessions AS (
  SELECT * FROM (
    VALUES (1), (2), (3), (5), (6), (10), (11), (12)
  ) AS t(day_num)
),
grouped AS (
  SELECT
    day_num,
    day_num - ROW_NUMBER() OVER (ORDER BY day_num) AS group_id
  FROM training_sessions
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

Three separate training streaks. The same pattern applied to a `DATE` column with `ROW_NUMBER()` ordered by date gives you consecutive-day streaks per user — the exact query structure behind “N consecutive active days” interview problems.

---

## The CTE chaining rule

**You cannot reference a window function result in a `WHERE` or `HAVING` clause in the same query.** This catches people off guard in interviews.

This does not work:

```sql
-- INVALID
SELECT
  battle_id,
  opponent,
  DENSE_RANK() OVER (ORDER BY difficulty_score DESC) AS rnk
FROM gym_rankings
WHERE rnk <= 3;  -- error: column "rnk" does not exist at this stage
```

The reason: SQL evaluates `WHERE` before `SELECT`, so the window function alias hasn’t been computed yet when the filter runs.

The fix is always a CTE:

```sql
WITH ranked AS (
  SELECT
    battle_id,
    opponent,
    difficulty_score,
    DENSE_RANK() OVER (ORDER BY difficulty_score DESC) AS rnk
  FROM gym_rankings
)
SELECT battle_id, opponent, difficulty_score
FROM ranked
WHERE rnk <= 3;
```

**Result:**

| battle_id | opponent | difficulty_score |
|-----------|----------|-----------------|
| 8         | Giovanni | 9               |
| 6         | Sabrina  | 8               |
| 7         | Blaine   | 7               |
| 9         | Ritchie  | 7               |

Four rows returned, not three — because Blaine and Ritchie both score 7 and both rank 3rd. `DENSE_RANK` does not skip a rank after a tie, so both qualify for `rnk <= 3`. This is the correct behavior for a “top-3 difficulty” query.

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

Each problem uses one of the datasets from above. Try it before opening the answer.

---

### Q1 (Medium) — First battle per Pokémon

> Using `team_battles`, return the first battle Ash had with each Pokémon. Return the Pokémon name, episode, opponent, and result.

**How to reason through it:**

You need “first row per group” — that’s `ROW_NUMBER() OVER (PARTITION BY pokemon ORDER BY battle_id)`. Filter to `rn = 1`. You can’t filter on a window function alias in `WHERE`, so wrap in a CTE first.

<details>
<summary>Answer</summary>

```sql
WITH team_battles AS (
  SELECT * FROM (
    VALUES
      (1,  'EP001', 'Pikachu',   'Spearow', 'W', 1),
      (2,  'EP005', 'Pikachu',   'Onix',    'W', 1),
      (3,  'EP007', 'Bulbasaur', 'Staryu',  'W', 1),
      (4,  'EP011', 'Pikachu',   'Rhyhorn', 'W', 1),
      (5,  'EP014', 'Pikachu',   'Raichu',  'W', 1),
      (6,  'EP024', 'Bulbasaur', 'Gloom',   'W', 1),
      (7,  'EP032', 'Bulbasaur', 'Koffing', 'W', 1),
      (8,  'EP059', 'Squirtle',  'Haunter', 'W', 1),
      (9,  'EP063', 'Charizard', 'Magmar',  'W', 1),
      (10, 'EP067', 'Squirtle',  'Rhyhorn', 'W', 1),
      (11, 'EP079', 'Pikachu',   'Sparky',  'W', 1),
      (12, 'EP079', 'Charizard', 'Zippo',   'L', 0)
  ) AS t(battle_id, episode, pokemon, opponent, result, win_flag)
),
ranked AS (
  SELECT
    pokemon, episode, opponent, result,
    ROW_NUMBER() OVER (PARTITION BY pokemon ORDER BY battle_id) AS rn
  FROM team_battles
)
SELECT pokemon, episode, opponent, result
FROM ranked
WHERE rn = 1
ORDER BY episode;
```

**Result:**

| pokemon   | episode | opponent | result |
|-----------|---------|----------|--------|
| Pikachu   | EP001   | Spearow  | W      |
| Bulbasaur | EP007   | Staryu   | W      |
| Squirtle  | EP059   | Haunter  | W      |
| Charizard | EP063   | Magmar   | W      |

This is the “latest/earliest row per group” pattern. It appears in nearly every real data interview in some form: first purchase per customer, first login per user, first event per session.

</details>

---

### Q2 (Medium) — Running win rate

> Using `badge_journey`, show the cumulative win rate as a percentage (rounded to 1 decimal) after each battle.

**How to reason through it:**

Win rate = wins so far ÷ battles so far. You need two running counts: `SUM(win_flag)` for wins and `COUNT(*)` for total battles. Both use the same `OVER()` clause. Divide and multiply by 100. Make sure to force decimal division.

<details>
<summary>Answer</summary>

```sql
WITH badge_journey AS (
  SELECT * FROM (
    VALUES
      (1, 'EP005', 'Pewter Gym',    'Brock',    'Boulder Badge', 1),
      (2, 'EP007', 'Cerulean Gym',  'Misty',    'Cascade Badge', 1),
      (3, 'EP014', 'Vermilion Gym', 'Lt. Surge','Thunder Badge', 1),
      (4, 'EP024', 'Celadon Gym',   'Erika',    'Rainbow Badge', 1),
      (5, 'EP032', 'Fuchsia Gym',   'Koga',     'Soul Badge',    1),
      (6, 'EP059', 'Saffron Gym',   'Sabrina',  'Marsh Badge',   1),
      (7, 'EP063', 'Cinnabar Gym',  'Blaine',   'Volcano Badge', 1),
      (8, 'EP067', 'Viridian Gym',  'Giovanni', 'Earth Badge',   1),
      (9, 'EP079', 'Indigo League', 'Ritchie',  NULL,             0)
  ) AS t(battle_id, episode, venue, opponent, badge_earned, win_flag)
)
SELECT
  battle_id,
  venue,
  opponent,
  ROUND(
    100.0
      * SUM(win_flag) OVER (ORDER BY battle_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
      / COUNT(*)      OVER (ORDER BY battle_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW),
    1
  ) AS win_rate_pct
FROM badge_journey
ORDER BY battle_id;
```

**Result:**

| # | venue          | opponent  | win_rate_pct |
|---|----------------|-----------|--------------|
| 1 | Pewter Gym     | Brock     | 100.0        |
| 2 | Cerulean Gym   | Misty     | 100.0        |
| 3 | Vermilion Gym  | Lt. Surge | 100.0        |
| 4 | Celadon Gym    | Erika     | 100.0        |
| 5 | Fuchsia Gym    | Koga      | 100.0        |
| 6 | Saffron Gym    | Sabrina   | 100.0        |
| 7 | Cinnabar Gym   | Blaine    | 100.0        |
| 8 | Viridian Gym   | Giovanni  | 100.0        |
| 9 | Indigo League  | Ritchie   | 88.9         |

Two window functions in one `SELECT` using the same `OVER()` definition. The `100.0 *` cast forces float division — without it, integer division would return 0 or 1.

</details>

---

### Q3 (Medium) — Previous and next stop in one query

> Using `kanto_route`, show each stop with both the location that came before it and the location coming up next, all in a single query.

**How to reason through it:**

`LAG(location)` for the previous stop, `LEAD(location)` for the next stop. Both use `ORDER BY stop_order`. Both can live in the same `SELECT`. The first row gets `NULL` for `prev_stop`, the last row gets `NULL` for `next_stop`.

<details>
<summary>Answer</summary>

```sql
WITH kanto_route AS (
  SELECT * FROM (
    VALUES
      (1,  'Pallet Town'),    (2,  'Route 1'),
      (3,  'Viridian Forest'),(4,  'Pewter City'),
      (5,  'Mt. Moon'),       (6,  'Cerulean City'),
      (7,  'Vermilion City'), (8,  'Celadon City'),
      (9,  'Fuchsia City'),   (10, 'Saffron City'),
      (11, 'Cinnabar Island'),(12, 'Viridian City'),
      (13, 'Indigo Plateau')
  ) AS t(stop_order, location)
)
SELECT
  stop_order,
  LAG(location)  OVER (ORDER BY stop_order) AS prev_stop,
  location                                   AS current_stop,
  LEAD(location) OVER (ORDER BY stop_order) AS next_stop
FROM kanto_route
ORDER BY stop_order;
```

**Result (first 5 and last 3 rows shown):**

| # | prev_stop       | current_stop    | next_stop       |
|---|-----------------|-----------------|-----------------|
| 1 | NULL            | Pallet Town     | Route 1         |
| 2 | Pallet Town     | Route 1         | Viridian Forest |
| 3 | Route 1         | Viridian Forest | Pewter City     |
| 4 | Viridian Forest | Pewter City     | Mt. Moon        |
| 5 | Pewter City     | Mt. Moon        | Cerulean City   |
| 11| Saffron City    | Cinnabar Island | Viridian City   |
| 12| Cinnabar Island | Viridian City   | Indigo Plateau  |
| 13| Viridian City   | Indigo Plateau  | NULL            |

`LAG` and `LEAD` can both live in the same `SELECT` with no conflict. A real-world version of this query: show each user session alongside the session before it and the session after it.

</details>

---

### Q4 (Hard) — Pikachu’s HP by battle within partition

> Using `pikachu_battles`, extend the LAG query: show the HP change from the previous battle AND classify it as `Recovered` (positive change), `Drained` (negative change), or `First Battle` (no prior data).

**How to reason through it:**

`LAG(hp_after)` gives you the previous HP. Subtract to get the change. Use a `CASE` to classify. You need `LAG` twice in the same `SELECT` — or compute it once in a CTE and reuse the alias. Using a CTE avoids repeating the `LAG()` call in the `CASE`.

<details>
<summary>Answer</summary>

```sql
WITH pikachu_battles AS (
  SELECT * FROM (
    VALUES
      (1, 'Route 1',       'Spearow flock','W', 45),
      (2, 'Pewter Gym',    'Onix',          'W', 20),
      (3, 'Cerulean Gym',  'Starmie',       'L',  0),
      (4, 'Vermilion Gym', 'Raichu',        'W', 15),
      (5, 'Fuchsia Gym',   'Electrode',     'W', 30),
      (6, 'Saffron Gym',   'Kadabra',       'W', 25),
      (7, 'Viridian Gym',  'Rhyhorn',       'W', 38),
      (8, 'Indigo League', 'Sparky',        'W',  8)
  ) AS t(battle_id, location, opponent, result, hp_after)
),
with_lag AS (
  SELECT
    battle_id, location, result, hp_after,
    LAG(hp_after) OVER (ORDER BY battle_id) AS prev_hp
  FROM pikachu_battles
)
SELECT
  battle_id,
  location,
  result,
  hp_after,
  prev_hp,
  hp_after - prev_hp AS hp_change,
  CASE
    WHEN prev_hp IS NULL          THEN 'First Battle'
    WHEN hp_after > prev_hp       THEN 'Recovered'
    ELSE 'Drained'
  END AS condition
FROM with_lag
ORDER BY battle_id;
```

**Result:**

| # | location      | result | hp_after | prev_hp | hp_change | condition   |
|---|---------------|--------|----------|---------|-----------|-------------|
| 1 | Route 1       | W      | 45       | NULL    | NULL      | First Battle|
| 2 | Pewter Gym    | W      | 20       | 45      | -25       | Drained     |
| 3 | Cerulean Gym  | L      | 0        | 20      | -20       | Drained     |
| 4 | Vermilion Gym | W      | 15       | 0       | +15       | Recovered   |
| 5 | Fuchsia Gym   | W      | 30       | 15      | +15       | Recovered   |
| 6 | Saffron Gym   | W      | 25       | 30      | -5        | Drained     |
| 7 | Viridian Gym  | W      | 38       | 25      | +13       | Recovered   |
| 8 | Indigo League | W      | 8        | 38      | -26       | Drained     |

The CTE computes `prev_hp` once. The outer query reuses it for both the arithmetic and the `CASE` without repeating the `LAG()` call. This is cleaner and avoids the risk of the two `LAG()` calls returning different results if the window definition ever changes.

</details>

---

### Q5 (Hard) — Streaks of at least 2 consecutive training days

> Using `training_sessions`, return each training streak that lasted at least 2 consecutive days. Show the start day, end day, and streak length.

**How to reason through it:**

Islands-and-gaps: compute `day_num - ROW_NUMBER() OVER (ORDER BY day_num)` as `group_id`. Rows in the same consecutive run share the same `group_id`. Then `GROUP BY group_id`, aggregate with `MIN`, `MAX`, `COUNT`. Filter with `HAVING COUNT(*) >= 2`.

<details>
<summary>Answer</summary>

```sql
WITH training_sessions AS (
  SELECT * FROM (
    VALUES (1), (2), (3), (5), (6), (10), (11), (12)
  ) AS t(day_num)
),
grouped AS (
  SELECT
    day_num,
    day_num - ROW_NUMBER() OVER (ORDER BY day_num) AS group_id
  FROM training_sessions
)
SELECT
  MIN(day_num) AS streak_start,
  MAX(day_num) AS streak_end,
  COUNT(*)     AS streak_length
FROM grouped
GROUP BY group_id
HAVING COUNT(*) >= 2
ORDER BY streak_start;
```

**Result:**

| streak_start | streak_end | streak_length |
|--------------|------------|---------------|
| 1            | 3          | 3             |
| 5            | 6          | 2             |
| 10           | 12         | 3             |

All three streaks qualify — the minimum is 2 days. If the question asked for streaks of 3+ days, change `HAVING COUNT(*) >= 2` to `HAVING COUNT(*) >= 3`, which would exclude the 5–6 streak and return only rows 1 and 3.

The `HAVING` filter runs after `GROUP BY` and after the aggregate functions are evaluated, so you can reference `COUNT(*)` there directly. This is why `HAVING` works here but `WHERE` would not.

</details>
