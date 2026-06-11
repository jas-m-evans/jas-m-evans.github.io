---
layout: single
title: "Professor Oak’s SQL Notebook: A Window into Ash’s Kanto Season"
date: 2026-05-24 09:00:00 +0000
categories: [data-engineering]
excerpt: "Professor Oak kept meticulous records of Ash Ketchum’s Kanto journey. Here are those records — and the ten window function queries that turn raw battle data into a complete story."
---

> **⚠️ Spoiler warning:** this post follows Ash’s Kanto journey from start to finish, including the Indigo League.

<details markdown="1">
  <summary>Never seen Pokémon? Start here (spoilers inside)</summary>

  Ash Ketchum is a ten-year-old kid from Pallet Town with one dream: become a Pokémon Master. On his first day as a trainer, he shows up late to Professor Oak’s lab and the only Pokémon left is a stubborn, half-feral Pikachu who won’t go near his Poké Ball.

  They don’t get along at first.

  But Ash throws himself in front of a flock of Spearow to protect Pikachu, and that changes everything. From that moment forward, they travel Kanto together — through mountain passes and forest routes, through gym after gym, collecting eight badges that earn them a spot in the Indigo League.

  They make it all the way to the Top 16. And then Charizard — Ash’s most powerful Pokémon, and also his most difficult one — refuses to battle. Ash loses to a rival named Ritchie. The season ends not with a championship, but with a stubborn fire-type lying down in the middle of a battle.

  That’s the arc. Eight badges earned, one title lost. A journey worth every episode.

</details>

---

Professor Oak kept meticulous records.

Every gym battle, every road encounter, every Pokémon caught — logged in a notebook that grew thicker with each passing episode. By the time Ash arrived at the Indigo Plateau, Oak had enough data to run a full season retrospective.

The problem wasn’t the data. It was the SQL.

Standard aggregates kept collapsing the story. `GROUP BY` could tell you Ash won 8 of 9 major battles, but it couldn’t tell you *how* he won them — the streak, the momentum, the moment the tide turned. To keep the story alive inside the query results, Oak needed window functions.

This is what he found.

---

## Chapter 1: The Badge Climb

*`SUM() OVER` — running totals*

Ash left Pallet Town with nothing but Pikachu and a backpack. Professor Oak’s first dataset was simple: one row per gym, in order.

```sql
WITH badge_journey AS (
  SELECT * FROM (
    VALUES
      (1, 'EP005', 'Pewter Gym',    'Brock',     'Boulder Badge', 1),
      (2, 'EP007', 'Cerulean Gym',  'Misty',     'Cascade Badge', 1),
      (3, 'EP014', 'Vermilion Gym', 'Lt. Surge', 'Thunder Badge', 1),
      (4, 'EP024', 'Celadon Gym',   'Erika',     'Rainbow Badge', 1),
      (5, 'EP032', 'Fuchsia Gym',   'Koga',      'Soul Badge',    1),
      (6, 'EP059', 'Saffron Gym',   'Sabrina',   'Marsh Badge',   1),
      (7, 'EP063', 'Cinnabar Gym',  'Blaine',    'Volcano Badge', 1),
      (8, 'EP067', 'Viridian Gym',  'Giovanni',  'Earth Badge',   1),
      (9, 'EP079', 'Indigo League', 'Ritchie',   NULL,              0)
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

Oak’s first instinct was `GROUP BY`. `SUM(win_flag)` would tell him Ash won 8 battles. But that collapses the entire journey into a single number. The story disappears.

A window function keeps every row intact and adds the cumulative total alongside it. `UNBOUNDED PRECEDING` means start from the very first row. `CURRENT ROW` means stop here.

```sql
SELECT
  battle_id,
  venue,
  opponent,
  SUM(win_flag) OVER (
    ORDER BY battle_id
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS badges_so_far
FROM badge_journey
ORDER BY battle_id;
```

**Result:**

| # | venue          | opponent  | badges_so_far |
|---|----------------|-----------|---------------|
| 1 | Pewter Gym     | Brock     | 1             |
| 2 | Cerulean Gym   | Misty     | 2             |
| 3 | Vermilion Gym  | Lt. Surge | 3             |
| 4 | Celadon Gym    | Erika     | 4             |
| 5 | Fuchsia Gym    | Koga      | 5             |
| 6 | Saffron Gym    | Sabrina   | 6             |
| 7 | Cinnabar Gym   | Blaine    | 7             |
| 8 | Viridian Gym   | Giovanni  | 8             |
| 9 | Indigo League  | Ritchie   | 8             |

Row 9 is the one to watch. Ash lost to Ritchie, but `badges_so_far` doesn’t drop. It stays at 8 — because the loss contributes `win_flag = 0`, which adds nothing to the sum. The journey’s full arc is visible in a single column: a steady climb to 8, then silence.

That’s what running totals are for. Not a final score. A story unfolding row by row.

---

## Chapter 2: The Team Behind the Badges

*`PARTITION BY` — independent calculations per group*

Ash didn’t win those badges alone.

By mid-Kanto, his team had grown to four main fighters: Pikachu, Bulbasaur, Squirtle, and Charizard. Oak wanted a win count for each Pokémon — not a single total, but separate tallies that climbed independently as each fighter added to their record.

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

Without `PARTITION BY`, a running total rolls across all twelve rows as one continuous count. With it, the window resets for each Pokémon — Pikachu’s tally starts at 0, Bulbasaur’s starts at 0, each one building independently.

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

Pikachu ends at 5. Bulbasaur at 3. Squirtle at 2. Charizard at 1 — one win, one loss, and that loss is the one that ends the season.

Row 12 is the quiet disaster in this dataset. Charizard fought Zippo at the Indigo League, disobeyed, and cost Ash the match. The `pokemon_wins` column stays at 1 because the loss adds nothing. But the story is there if you know where to look.

---

## Chapter 3: The Roads In Between

*`ROWS BETWEEN` — rolling windows*

The gym badges get the headlines. But most of Ash’s growth happened on the roads between cities — scrappy encounters with random trainers on Route 3 and Route 7, where no badge was on the line and no one was watching.

Oak logged those too.

```sql
WITH road_encounters AS (
  SELECT * FROM (
    VALUES
      (1,  'EP002', 'Route 1',        'Bug Catcher', 'W', 1),
      (2,  'EP003', 'Viridian Forest', 'Youngster',   'W', 1),
      (3,  'EP006', 'Mt. Moon',        'Rocket Grunt','W', 1),
      (4,  'EP008', 'Route 3',         'Lass',        'L', 0),
      (5,  'EP009', 'Route 3',         'Bug Catcher', 'W', 1),
      (6,  'EP010', 'Route 4',         'Youngster',   'W', 1),
      (7,  'EP016', 'Route 6',         'Hiker',       'L', 0),
      (8,  'EP017', 'Route 7',         'Lass',        'W', 1),
      (9,  'EP020', 'Route 8',         'Youngster',   'W', 1),
      (10, 'EP025', 'Route 9',         'Hiker',       'W', 1),
      (11, 'EP033', 'Route 15',        'Bird Keeper', 'L', 0),
      (12, 'EP040', 'Route 16',        'Bug Catcher', 'W', 1)
  ) AS t(enc_id, episode, route, trainer_class, result, win_flag)
)
SELECT * FROM road_encounters;
```

Oak wasn’t interested in Ash’s all-time road record. He wanted to know *current form* — the kind of stat a commentator uses: "How has he done in his last three fights?"

That’s a rolling window. `2 PRECEDING` + `CURRENT ROW` means: for each row, look at the two battles before it plus this one. A 3-battle moving snapshot.

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

**Result:**

| # | route           | trainer_class | result | wins_last_3 |
|---|-----------------|---------------|--------|-------------|
| 1 | Route 1         | Bug Catcher   | W      | 1           |
| 2 | Viridian Forest | Youngster     | W      | 2           |
| 3 | Mt. Moon        | Rocket Grunt  | W      | 3           |
| 4 | Route 3         | Lass          | L      | 2           |
| 5 | Route 3         | Bug Catcher   | W      | 2           |
| 6 | Route 4         | Youngster     | W      | 2           |
| 7 | Route 6         | Hiker         | L      | 2           |
| 8 | Route 7         | Lass          | W      | 2           |
| 9 | Route 8         | Youngster     | W      | 2           |
| 10| Route 9         | Hiker         | W      | 3           |
| 11| Route 15        | Bird Keeper   | L      | 2           |
| 12| Route 16        | Bug Catcher   | W      | 2           |

Ash opens strong — three wins, `wins_last_3` hits 3 at Mt. Moon. Then Route 3 brings his first road loss and the window slides to 2. He recovers, loses again to the Hiker on Route 6, bounces back. By Route 9 he’s back to 3 out of 3 for the first time since the start. Then Route 15 dips him again.

The career record is fine. The form graph tells a different story: Ash struggles in the middle of the journey, stabilizes, and arrives at the Indigo League on decent recent form. The frame clause is what makes that visible.

Rows 1 and 2 have fewer than 3 prior rows available, so the window shrinks to fit. SQL doesn’t error out — it just uses what’s there.

---

## Chapter 4: Difficulty, Grouped Two Ways

*`RANGE BETWEEN` vs `ROWS BETWEEN`*

Before the Indigo League, Oak categorized the gym battles by era: Brock, Misty, and Lt. Surge were early Kanto (tier 1), Erika and Koga were mid-journey (tier 2), and Sabrina through Ritchie were the late-season gauntlet (tier 3).

The same nine battles, viewed through a difficulty lens.

```sql
WITH gym_tiers AS (
  SELECT * FROM (
    VALUES
      (1, 'EP005', 'Brock',     1, 1),
      (2, 'EP007', 'Misty',     1, 1),
      (3, 'EP014', 'Lt. Surge', 1, 1),
      (4, 'EP024', 'Erika',     2, 1),
      (5, 'EP032', 'Koga',      2, 1),
      (6, 'EP059', 'Sabrina',   3, 1),
      (7, 'EP063', 'Blaine',    3, 1),
      (8, 'EP067', 'Giovanni',  3, 1),
      (9, 'EP079', 'Ritchie',   3, 0)
  ) AS t(battle_id, episode, opponent, difficulty_tier, win_flag)
)
SELECT * FROM gym_tiers;
```

Oak ran two versions of a neighborhood sum — one using `ROWS BETWEEN`, one using `RANGE BETWEEN` — to understand the difference. Both say "1 preceding, 1 following," but they measure that distance completely differently.

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

**`rows_sum`** counts physical rows: Brock sits at the top with no preceding row, so his window only reaches 2. The frame slides down the table one row at a time regardless of what difficulty tier the rows belong to.

**`range_sum`** counts logical values: for a tier-2 opponent like Erika, the range "1 preceding, 1 following" means "include all rows with `difficulty_tier` between 1 and 3" — every row in the table. All 9 rows, 8 wins. Hence `range_sum = 8` for every tier-2 row. For tier-1 opponents, the range is 0 to 2, capturing tiers 1 and 2 (5 wins). For tier-3, tiers 2 through 4 (one loss in the mix = 5 wins).

Every row within the same tier gets the same `range_sum` because they all share the same `ORDER BY` value. `rows_sum` varies by position even within a tier. This is the core distinction: **RANGE is value-aware, ROWS is position-aware.**

This matters most with date columns. `RANGE BETWEEN INTERVAL '6 DAYS' PRECEDING AND CURRENT ROW` sweeps in all rows from the past 6 calendar days regardless of gaps. `ROWS BETWEEN 6 PRECEDING` grabs exactly 7 physical rows regardless of what dates they cover. Same words, completely different results on sparse data.

---

## Chapter 5: Who Was the Hardest Fight?

*`ROW_NUMBER()`, `RANK()`, `DENSE_RANK()` — tie behavior*

Late in the season, Oak sat down to rank every gym leader and the Indigo League opponent by how hard Ash had to work to beat them. He scored each one — a subjective difficulty score from 3 to 9 — and immediately ran into the classic tie problem.

Blaine and Ritchie both scored 7. Brock and Misty both scored 4.

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

Giovanni is unchallengeable at the top. Sabrina second. Then Blaine and Ritchie share the third spot — and here’s where the three functions diverge.

**`ROW_NUMBER`** breaks every tie with a secondary sort. Blaine gets 3, Ritchie gets 4. Always unique, never ambiguous.

**`RANK`** lets them both be 3rd — but then jumps to 5 for Koga, skipping rank 4 entirely. Two trainers tied for third means nobody gets fourth.

**`DENSE_RANK`** also puts them both at 3rd, but Koga becomes 4th instead of 5th. No gaps in the sequence.

The interview trap: if the question asks for "top 3 hardest battles" and you use `RANK`, you might get no row at position 3 for some groups — because ties can push the next distinct rank past N. `DENSE_RANK` is the safe default any time ties should be allowed through the filter.

---

## Chapter 6: The Toll on Pikachu

*`LAG()` — look back one row*

Pikachu fought in almost every significant battle. Oak had been quietly logging his HP after each fight, and the numbers told a story no win/loss column could.

```sql
WITH pikachu_battles AS (
  SELECT * FROM (
    VALUES
      (1, 'EP001', 'Route 1',       'Spearow flock', 'W', 45),
      (2, 'EP005', 'Pewter Gym',    'Onix',           'W', 20),
      (3, 'EP007', 'Cerulean Gym',  'Starmie',        'L',  0),
      (4, 'EP014', 'Vermilion Gym', 'Raichu',         'W', 15),
      (5, 'EP032', 'Fuchsia Gym',   'Electrode',      'W', 30),
      (6, 'EP059', 'Saffron Gym',   'Kadabra',        'W', 25),
      (7, 'EP067', 'Viridian Gym',  'Rhyhorn',        'W', 38),
      (8, 'EP079', 'Indigo League', 'Sparky',         'W',  8)
  ) AS t(battle_id, episode, location, opponent, result, hp_after)
)
SELECT * FROM pikachu_battles;
```

`LAG(column)` returns the value of that column from the previous row — the battle that came just before this one. The first row gets `NULL` because there’s nothing before it. Every other row can look back one step and compare.

```sql
SELECT
  battle_id,
  location,
  result,
  hp_after,
  LAG(hp_after) OVER (ORDER BY battle_id)                    AS prev_hp,
  hp_after - LAG(hp_after) OVER (ORDER BY battle_id)         AS hp_change,
  CASE
    WHEN LAG(hp_after) OVER (ORDER BY battle_id) IS NULL     THEN 'First Battle'
    WHEN hp_after > LAG(hp_after) OVER (ORDER BY battle_id)  THEN 'Recovered'
    ELSE 'Drained'
  END AS condition
FROM pikachu_battles
ORDER BY battle_id;
```

**Result:**

| # | location      | result | hp_after | prev_hp | hp_change | condition    |
|---|---------------|--------|----------|---------|-----------|--------------|
| 1 | Route 1       | W      | 45       | NULL    | NULL      | First Battle |
| 2 | Pewter Gym    | W      | 20       | 45      | -25       | Drained      |
| 3 | Cerulean Gym  | L      | 0        | 20      | -20       | Drained      |
| 4 | Vermilion Gym | W      | 15       | 0       | +15       | Recovered    |
| 5 | Fuchsia Gym   | W      | 30       | 15      | +15       | Recovered    |
| 6 | Saffron Gym   | W      | 25       | 30      | -5        | Drained      |
| 7 | Viridian Gym  | W      | 38       | 25      | +13       | Recovered    |
| 8 | Indigo League | W      | 8        | 38      | -26       | Drained      |

Brock’s Onix hits Pikachu hard: -25 HP even in a winning battle. Cerulean drops him to zero — the only loss. He bounces back across Vermilion and Fuchsia, peaks at 38 HP after Giovanni, and then the Indigo League final against Ritchie’s Sparky costs him 26 HP in a single fight.

He wins that one, barely. Row 8 is the worst HP drain of the season, and also a win.

`LAG()` also accepts an offset. `LAG(hp_after, 2)` looks back two battles instead of one. The second argument defaults to 1.

---

## Chapter 7: The Road Ahead

*`LEAD()` — look forward one row*

While `LAG()` looks backward, `LEAD()` looks forward. Oak used it to map out the next stop on the journey — what was coming after each location, before Ash ever arrived.

```sql
WITH kanto_route AS (
  SELECT * FROM (
    VALUES
      (1,  'EP001', 'Pallet Town',     'Receives Pikachu from Prof. Oak'),
      (2,  'EP001', 'Route 1',         'First wild Pokémon encounter'),
      (3,  'EP003', 'Viridian Forest', 'Catches Caterpie and Pidgeotto'),
      (4,  'EP005', 'Pewter City',     'Earns Boulder Badge from Brock'),
      (5,  'EP006', 'Mt. Moon',        'Battles Team Rocket at Moon Stone'),
      (6,  'EP007', 'Cerulean City',   'Earns Cascade Badge from Misty'),
      (7,  'EP014', 'Vermilion City',  'Earns Thunder Badge from Lt. Surge'),
      (8,  'EP024', 'Celadon City',    'Earns Rainbow Badge from Erika'),
      (9,  'EP032', 'Fuchsia City',    'Earns Soul Badge from Koga'),
      (10, 'EP059', 'Saffron City',    'Earns Marsh Badge from Sabrina'),
      (11, 'EP063', 'Cinnabar Island', 'Earns Volcano Badge from Blaine'),
      (12, 'EP067', 'Viridian City',   'Earns Earth Badge from Giovanni'),
      (13, 'EP079', 'Indigo Plateau',  'Loses to Ritchie in Top 16')
  ) AS t(stop_order, episode, location, key_event)
)
SELECT * FROM kanto_route;
```

`LEAD(column)` returns the value from the row immediately after the current one. The last row — Indigo Plateau — gets `NULL` for both forward columns. There is no next stop. The journey ends there.

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

| # | location        | key_event                          | next_stop       | next_ep |
|---|-----------------|------------------------------------|-----------------|---------|
| 1 | Pallet Town     | Receives Pikachu from Prof. Oak    | Route 1         | EP001   |
| 2 | Route 1         | First wild Pokémon encounter          | Viridian Forest | EP003   |
| 3 | Viridian Forest | Catches Caterpie and Pidgeotto     | Pewter City     | EP005   |
| 4 | Pewter City     | Earns Boulder Badge from Brock     | Mt. Moon        | EP006   |
| 5 | Mt. Moon        | Battles Team Rocket at Moon Stone  | Cerulean City   | EP007   |
| 6 | Cerulean City   | Earns Cascade Badge from Misty     | Vermilion City  | EP014   |
| 7 | Vermilion City  | Earns Thunder Badge from Lt. Surge | Celadon City    | EP024   |
| 8 | Celadon City    | Earns Rainbow Badge from Erika     | Fuchsia City    | EP032   |
| 9 | Fuchsia City    | Earns Soul Badge from Koga         | Saffron City    | EP059   |
| 10| Saffron City    | Earns Marsh Badge from Sabrina     | Cinnabar Island | EP063   |
| 11| Cinnabar Island | Earns Volcano Badge from Blaine    | Viridian City   | EP067   |
| 12| Viridian City   | Earns Earth Badge from Giovanni    | Indigo Plateau  | EP079   |
| 13| Indigo Plateau  | Loses to Ritchie in Top 16         | NULL            | NULL    |

Every stop carries knowledge of where it leads. Pallet Town already knows Route 1 is next. Viridian City already knows Indigo Plateau is coming. And Indigo Plateau knows nothing — because after the season ends, the data runs out.

`LEAD()` takes the same arguments as `LAG()`. `LEAD(location, 2)` returns the stop two rows ahead. The second argument defaults to 1.

---

## Chapter 8: The First and the Last

*`FIRST_VALUE()` / `LAST_VALUE()` — partition anchors*

Oak wanted to track something specific: for every Pokémon on Ash’s team, which was caught first and which was caught last? He needed every row to carry those two reference points simultaneously.

```sql
WITH pokemon_team AS (
  SELECT * FROM (
    VALUES
      (1, 'EP001', 'Pikachu',    'Pallet Town',        'Electric'),
      (2, 'EP003', 'Caterpie',   'Viridian Forest',    'Bug'),
      (3, 'EP003', 'Pidgeotto',  'Viridian Forest',    'Flying'),
      (4, 'EP010', 'Bulbasaur',  'Melanie\'s Village', 'Grass'),
      (5, 'EP011', 'Charmander', 'Route 24',            'Fire'),
      (6, 'EP012', 'Squirtle',   'Vermilion City',     'Water'),
      (7, 'EP029', 'Primeape',   'Route 23',            'Fighting'),
      (8, 'EP031', 'Muk',        'Gringey City',        'Poison')
  ) AS t(catch_order, episode, pokemon, location, type)
)
SELECT * FROM pokemon_team;
```

`FIRST_VALUE(pokemon)` returns the first Pokémon in the ordered window — Pikachu, always, anchored at the beginning. `LAST_VALUE(pokemon)` is trickier.

**The `LAST_VALUE` trap** — the most common mistake with these functions:

The default frame is `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`. For `LAST_VALUE`, this means "the last value seen so far" — which is always just the current row itself. Not the last in the partition. The current row.

```sql
SELECT
  catch_order,
  pokemon,
  location,
  FIRST_VALUE(pokemon) OVER (ORDER BY catch_order)                                                         AS first_catch,
  LAST_VALUE(pokemon)  OVER (ORDER BY catch_order)                                                         AS last_wrong,
  LAST_VALUE(pokemon)  OVER (ORDER BY catch_order ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_correct
FROM pokemon_team
ORDER BY catch_order;
```

**Result:**

| # | pokemon    | location           | first_catch | last_wrong | last_correct |
|---|------------|--------------------|-------------|------------|--------------|
| 1 | Pikachu    | Pallet Town        | Pikachu     | Pikachu    | Muk          |
| 2 | Caterpie   | Viridian Forest    | Pikachu     | Caterpie   | Muk          |
| 3 | Pidgeotto  | Viridian Forest    | Pikachu     | Pidgeotto  | Muk          |
| 4 | Bulbasaur  | Melanie's Village | Pikachu     | Bulbasaur  | Muk          |
| 5 | Charmander | Route 24           | Pikachu     | Charmander | Muk          |
| 6 | Squirtle   | Vermilion City     | Pikachu     | Squirtle   | Muk          |
| 7 | Primeape   | Route 23           | Pikachu     | Primeape   | Muk          |
| 8 | Muk        | Gringey City       | Pikachu     | Muk        | Muk          |

`first_catch` is always Pikachu — `FIRST_VALUE` works correctly with the default frame because it anchors at the start and never moves.

`last_wrong` just mirrors the current row’s Pokémon. It’s not looking at the end of the partition; it’s looking at the end of the current frame, which with the default definition is always right here.

`last_correct` extends the frame to `UNBOUNDED FOLLOWING`, so every row can see all the way to the end of the window. Muk — the last Pokémon Ash caught in Kanto — appears on every row, as intended.

The practical fix: most SQL writers avoid `LAST_VALUE` entirely and use `FIRST_VALUE` with a reversed `ORDER BY DESC` instead. Same answer, no frame adjustment needed.

---

## Chapter 9: The Power Rankings

*`NTILE(n)` — bucketing into equal groups*

End of season. Oak pulled Ash’s eight main Pokémon and their full-season battle records, then divided the team into four performance tiers by total wins.

```sql
WITH team_power AS (
  SELECT * FROM (
    VALUES
      ('Pikachu',    'Electric', 28, 21),
      ('Charizard',  'Fire',     15, 10),
      ('Bulbasaur',  'Grass',    12,  8),
      ('Squirtle',   'Water',     9,  7),
      ('Primeape',   'Fighting',  6,  5),
      ('Pidgeotto',  'Flying',    8,  5),
      ('Butterfree', 'Bug',       7,  4),
      ('Muk',        'Poison',    5,  3)
  ) AS t(pokemon, type, battles, wins)
)
SELECT * FROM team_power;
```

`NTILE(4)` divides rows into 4 as-equal-as-possible buckets ordered by the column you specify. 8 Pokémon into 4 tiers = 2 per tier.

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

Tier 1: the carries. Pikachu with 21 wins and Charizard with 10 — the two Pokémon Ash relied on most in the biggest fights. Tier 4: Butterfree and Muk, role players who showed up when called but rarely led a match.

Primeape and Pidgeotto tied at 5 wins, but `NTILE` doesn’t care about ties the way `RANK` does. It just fills buckets evenly. Both land in tier 3.

If the rows don’t divide evenly, the earlier buckets get the extra row. A common real-world use: `NTILE(100)` as an approximation of percentile rank. Wrap in a CTE and filter `WHERE power_tier = 1` to get the top quarter.

---

## Chapter 10: The Training Log

*Islands and gaps — detecting consecutive sequences*

Before the Indigo League, Ash trained. Not every day — travel days between towns broke the streak — but consistently enough that Oak could map out the rhythm.

Oak logged the days of October when Ash completed a formal training session.

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

Days 4, 7, 8, and 9 are missing. Three separate stretches of consecutive training, separated by gaps. The question is: can SQL find them?

This is the hardest window function pattern — and the one interviewers reach for when they want to separate candidates who truly understand window functions from those who merely know the syntax.

**The trick:** for a sequence to be consecutive, the difference between the value and its row number stays constant within the same run. The moment there’s a gap, that constant shifts.

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

Days 1, 2, 3: each day increments by 1 and so does the row number. Difference stays 0. Day 4 is missing — day 5 arrives as row 4, making the difference jump to 1. Days 10–12 share `group_id = 4` for the same reason.

Now group by that constant to surface each streak:

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

Three streaks. The first three days of October, then two days after a gap, then three more to close out the prep period.

The same pattern on a `DATE` column with `ROW_NUMBER() OVER (ORDER BY date)` gives you consecutive-day user activity streaks — exactly the query behind every “N consecutive active days” interview problem.

---

## The CTE Chaining Rule

Before Oak could filter on any window function result, he had to learn the hardest SQL rule that nobody writes down clearly:

**You cannot reference a window function result in a `WHERE` or `HAVING` clause in the same query.**

This fails:

```sql
-- INVALID
SELECT
  battle_id,
  opponent,
  DENSE_RANK() OVER (ORDER BY difficulty_score DESC) AS rnk
FROM gym_rankings
WHERE rnk <= 3;  -- error: "rnk" does not exist at this stage
```

SQL evaluates `WHERE` before `SELECT`. The window function alias hasn’t been computed yet when the filter runs. The column doesn’t exist yet.

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

Four rows, not three — because Blaine and Ritchie both scored 7 and both rank 3rd. `DENSE_RANK` doesn’t skip after a tie, so both clear the `rnk <= 3` filter.

The CTE computes the window result first. The outer query filters on it second. This two-step structure is the standard pattern for any "top-N" query in SQL.

---

## Quick Syntax Decoder

When you encounter a window function in the wild:

```sql
FUNCTION(col) OVER (
  PARTITION BY x
  ORDER BY y
  ROWS BETWEEN a PRECEDING AND b FOLLOWING
)
```

Read it in this order:

1. **Which group?** (`PARTITION BY`) — resets the calculation per group
2. **What order within the group?** (`ORDER BY`) — defines the timeline
3. **How much of that timeline can this row see?** (`ROWS`/`RANGE BETWEEN`) — the frame
4. **What calculation on that visible slice?** (`FUNCTION`) — the actual math

---

## Practice: Professor Oak’s Exam

*Five questions from Oak’s notebook. Try each before opening the answer.*

---

### Q1 (Medium) — When did Ash’s team debut?

> Ash called on each Pokémon for the first time at a specific moment in the journey. Using `team_battles`, return the first battle each Pokémon participated in: the Pokémon name, episode, opponent, and result.

**How to reason through it:**

First row per group is `ROW_NUMBER() OVER (PARTITION BY pokemon ORDER BY battle_id)`. Filter to `rn = 1`. Window function aliases can’t be referenced in `WHERE` — wrap in a CTE.

<details markdown="1">
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

Every first battle was a win. Pikachu’s debut was the flock of Spearow on Route 1 — the battle that forged their bond. This "first row per group" pattern is one of the most common in real data work: first purchase per customer, first login per user, first event per session.

</details>

---

### Q2 (Medium) — Ash’s win rate, battle by battle

> Using `badge_journey`, show the cumulative win rate as a percentage (rounded to 1 decimal) after each gym battle and the Indigo League final.

**How to reason through it:**

Win rate = wins so far ÷ battles so far. Two running window functions: `SUM(win_flag)` and `COUNT(*)`, same `OVER()` clause. Divide and multiply by 100. Force decimal division with `100.0`.

<details markdown="1">
<summary>Answer</summary>

```sql
WITH badge_journey AS (
  SELECT * FROM (
    VALUES
      (1, 'EP005', 'Pewter Gym',    'Brock',     'Boulder Badge', 1),
      (2, 'EP007', 'Cerulean Gym',  'Misty',     'Cascade Badge', 1),
      (3, 'EP014', 'Vermilion Gym', 'Lt. Surge', 'Thunder Badge', 1),
      (4, 'EP024', 'Celadon Gym',   'Erika',     'Rainbow Badge', 1),
      (5, 'EP032', 'Fuchsia Gym',   'Koga',      'Soul Badge',    1),
      (6, 'EP059', 'Saffron Gym',   'Sabrina',   'Marsh Badge',   1),
      (7, 'EP063', 'Cinnabar Gym',  'Blaine',    'Volcano Badge', 1),
      (8, 'EP067', 'Viridian Gym',  'Giovanni',  'Earth Badge',   1),
      (9, 'EP079', 'Indigo League', 'Ritchie',   NULL,              0)
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

100% right up until the last row. Then 88.9%. Two window functions in one `SELECT`, same `OVER()` definition, different aggregation functions. The `100.0 *` cast forces float division — without it, integer division returns 0 or 1.

</details>

---

### Q3 (Medium) — Where did Ash come from, and where is he going?

> Using `kanto_route`, show each stop with the location before it and the location after it, all in a single query.

**How to reason through it:**

`LAG(location)` for the previous stop, `LEAD(location)` for the next. Both use `ORDER BY stop_order`. Both live in the same `SELECT`. First row gets `NULL` for prev; last row gets `NULL` for next.

<details markdown="1">
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
  LAG(location)  OVER (ORDER BY stop_order) AS came_from,
  location                                   AS current_stop,
  LEAD(location) OVER (ORDER BY stop_order) AS heading_to
FROM kanto_route
ORDER BY stop_order;
```

**Result (first 5 and last 3 rows):**

| # | came_from       | current_stop    | heading_to      |
|---|-----------------|-----------------|-----------------|
| 1 | NULL            | Pallet Town     | Route 1         |
| 2 | Pallet Town     | Route 1         | Viridian Forest |
| 3 | Route 1         | Viridian Forest | Pewter City     |
| 4 | Viridian Forest | Pewter City     | Mt. Moon        |
| 5 | Pewter City     | Mt. Moon        | Cerulean City   |
| 11| Saffron City    | Cinnabar Island | Viridian City   |
| 12| Cinnabar Island | Viridian City   | Indigo Plateau  |
| 13| Viridian City   | Indigo Plateau  | NULL            |

Pallet Town knows where it’s sending Ash. Indigo Plateau doesn’t know what comes next, because the data ends there. The same query structure in production: each user session beside the session before it and the one after.

</details>

---

### Q4 (Hard) — Pikachu’s recovery between battles

> Using `pikachu_battles`, show the HP change from the previous battle and classify each battle as `Recovered`, `Drained`, or `First Battle`. Use a CTE so `LAG(hp_after)` is computed once and reused.

**How to reason through it:**

Compute `prev_hp` with `LAG()` in a CTE. Then in the outer query, subtract for `hp_change` and use a `CASE` to classify. The CTE avoids calling `LAG()` twice in the same `SELECT` — cleaner and safer.

<details markdown="1">
<summary>Answer</summary>

```sql
WITH pikachu_battles AS (
  SELECT * FROM (
    VALUES
      (1, 'Route 1',       'Spearow flock', 'W', 45),
      (2, 'Pewter Gym',    'Onix',           'W', 20),
      (3, 'Cerulean Gym',  'Starmie',        'L',  0),
      (4, 'Vermilion Gym', 'Raichu',         'W', 15),
      (5, 'Fuchsia Gym',   'Electrode',      'W', 30),
      (6, 'Saffron Gym',   'Kadabra',        'W', 25),
      (7, 'Viridian Gym',  'Rhyhorn',        'W', 38),
      (8, 'Indigo League', 'Sparky',         'W',  8)
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
    WHEN prev_hp IS NULL    THEN 'First Battle'
    WHEN hp_after > prev_hp THEN 'Recovered'
    ELSE 'Drained'
  END AS condition
FROM with_lag
ORDER BY battle_id;
```

**Result:**

| # | location      | result | hp_after | prev_hp | hp_change | condition    |
|---|---------------|--------|----------|---------|-----------|--------------|
| 1 | Route 1       | W      | 45       | NULL    | NULL      | First Battle |
| 2 | Pewter Gym    | W      | 20       | 45      | -25       | Drained      |
| 3 | Cerulean Gym  | L      | 0        | 20      | -20       | Drained      |
| 4 | Vermilion Gym | W      | 15       | 0       | +15       | Recovered    |
| 5 | Fuchsia Gym   | W      | 30       | 15      | +15       | Recovered    |
| 6 | Saffron Gym   | W      | 25       | 30      | -5        | Drained      |
| 7 | Viridian Gym  | W      | 38       | 25      | +13       | Recovered    |
| 8 | Indigo League | W      | 8        | 38      | -26       | Drained      |

The CTE computes `prev_hp` once. The outer query uses that alias for both the subtraction and the `CASE` — no repeated `LAG()` call, no risk of inconsistency if the window definition changes.

</details>

---

### Q5 (Hard) — Find every training streak of at least 2 days

> Using `training_sessions`, return each streak of consecutive training days that lasted at least 2 days. Show the start day, end day, and streak length, ordered by start.

**How to reason through it:**

Islands-and-gaps: `day_num - ROW_NUMBER() OVER (ORDER BY day_num)` produces a constant `group_id` for each consecutive run. Group by it, aggregate with `MIN`/`MAX`/`COUNT`. Use `HAVING COUNT(*) >= 2` to filter short streaks. `HAVING` runs after `GROUP BY` so it can reference `COUNT(*)` directly.

<details markdown="1">
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

All three qualify. To narrow to 3+ day streaks, change `HAVING COUNT(*) >= 2` to `>= 3` — which would exclude the days-5-to-6 run and return only the first and last streak.

`HAVING` works here because it runs after `GROUP BY` and after aggregates are computed. `WHERE` would not — it runs too early, before grouping.

</details>
