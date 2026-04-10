# jas-m-evans.github.io

Personal portfolio site for Jason Evans — Data Engineer · M.Sc. CS · Drummer.

Built with Jekyll + Minimal Mistakes, deployed via GitHub Pages.

---

## Taste Bridge Chat

**Live demo:** <https://jas-m-evans.github.io/wave-defect-demo/>

### What it is

Taste Bridge is an interactive realtime music recommendation experience built on top of the [Wave·Defect / wave2vector](https://github.com/jas-m-evans/wave2vector) project. It replaces the old debug-console transport log with a polished two-user recommendation UI.

Two listeners enter a shared room. The system computes a **bridge recommendation** — one track that sits meaningfully between both taste profiles — and explains its reasoning in plain language.

### Architecture

| Layer | Technology |
|---|---|
| Auth | Spotify PKCE OAuth (read-only, no data stored) |
| Taste profile | Real Spotify audio-features API (energy, valence, danceability, acousticness, instrumentalness, speechiness, tempo) |
| Candidate pool | User's real top tracks + 12 curated mock tracks |
| Recommender | Deterministic weighted-similarity engine (ported from `app/recommender.py`) |
| Commentary | Rule-based explanation engine (ported from `app/commentary.py`) |
| Demo mode | Deterministic xorshift32 profile seeded from a visitor's name — no Spotify needed |
| Realtime layer | LiveKit (simulated in the static demo; connects to deployed backend when `BACKEND_URL` is set) |

### Recommender engine

The recommender is a **pure function** — no randomness, fully reproducible for the same inputs:

1. **Target profile** — blend of both users' feature vectors, shifted by preference knobs (`balanceBias`, `energyBias`, `moodBias`, `noveltyBias`).
2. **Score each candidate** — weighted combination of:
   - Similarity to target (35 %)
   - Bridge quality = mean fit to both users (25 %)
   - Fairness = how evenly it fits both users (20 %)
   - Novelty = distance from users' own taste (20 %, scaled by `noveltyBias`)
3. **Diversity penalty** — previous recommendation gets a 0.65× score multiplier to encourage variety.

### Preference knobs

Users can steer the recommendation via chat commands or natural language:

| Command | Effect |
|---|---|
| `/balanced` | Equal weight to both taste profiles |
| `/more-me` | Lean toward Jason's profile |
| `/more-them` | Lean toward the guest's profile |
| `/weirder` | Increase novelty bias |
| `/safer` | Decrease novelty bias |
| `/moodier` | Push toward darker/more emotional sounds |
| `/more-energy` | Push toward higher-energy tracks |
| `/next` | Force a different recommendation |
| `/why` | Explain the current recommendation |

Natural language nudges are also parsed — e.g. *"something darker"*, *"more energy"*, *"give us a left turn"*.

### UI

- **Left panel** — Bridge recommendation card: Shared Vibe, Biggest Contrast, bridge track, Why This Track, Confidence bar, per-dimension score grid.
- **Right panel** — Live chat with slash-command shortcuts and NLP nudge support.
- **Collapsible System Console** — raw event log moved out of the main UX.
- **Compatibility strip** — cosine similarity between both taste profiles, shown as a progress bar.

### Two explicit modes

| Mode | How to enter | Taste profile source |
|---|---|---|
| **Spotify** (primary) | Click **Connect Spotify** | Real Spotify audio-features API — if this fails, an error is shown and you cannot proceed until resolved |
| **Demo** (secondary) | Click **Try Demo** and enter a name | Deterministic profile derived from your name (xorshift32) — clearly labelled in the UI |

There is **no silent fallback**: if Spotify is chosen but audio features cannot be fetched, the app shows an error banner with a **Retry** and **Re-authenticate** link instead of quietly generating a demo profile.

### Demo mode

Anyone can try the experience without connecting Spotify. Clicking **Try Demo** and entering a name generates a deterministic taste profile from that name string (xorshift32 seeded from the name hash), then runs the full recommender against Jason's real profile. Demo mode is clearly labelled with a **Demo Mode** badge in the top bar and a notice banner in the room — it never shows the Spotify Connected badge.

### Backend integration

This static demo runs entirely in the browser. To connect it to the full [wave2vector](https://github.com/jas-m-evans/wave2vector) FastAPI backend (with real LiveKit rooms, persistence, and multi-user support), set `BACKEND_URL` at the top of the script block in `wave-defect-demo.html` to your deployed backend URL.

---

## Real User Sync Prototype Mode

> **Goal:** Record a convincing demo with two real Spotify accounts showing a full taste-profile comparison.

### How it works

When a real user authenticates with Spotify, the app performs a **one-time initial sync** that pulls as much useful music-profile data as Spotify's API allows, then persists it to `localStorage` (keyed by Spotify user ID). No backend is required.

#### Data fetched per user

| Data | Endpoint | Scope |
|---|---|---|
| User profile | `/me` | `user-read-private` |
| Top tracks — short / medium / long term | `/me/top/tracks` | `user-top-read` |
| Top artists — short / medium / long term | `/me/top/artists` | `user-top-read` |
| Recently played | `/me/player/recently-played` | `user-read-recently-played` |
| Saved tracks (up to 200) | `/me/tracks` | `user-library-read` |
| Followed artists | `/me/following` | `user-follow-read` |
| Playlists (up to 20) | `/me/playlists` | `user-read-private` |
| Playlist tracks (first 5 owned, up to 100 each) | `/playlists/{id}/tracks` | `user-read-private` |
| Audio features (all unique top tracks) | `/audio-features` | `user-top-read` |

#### Derived taste profile (`derived` field)

Each synced profile also stores a derived artifact:

- **`taste_profile`** — averaged audio features (energy, valence, danceability, acousticness, instrumentalness, speechiness, tempo_norm)
- **`taste_vector`** — numeric array for cosine similarity
- **`genre_distribution`** — genre scores weighted by artist rank
- **`top_genres`** — top 12 genres
- **`favorite_artists`** — scored across time ranges
- **`popularity_summary`** — average track popularity
- **`decade_distribution`** — which decades dominate the library
- **`summary_text`** — one-sentence human-readable taste description

#### Sync constants

These can be adjusted at the top of the script block in `wave-defect-demo.html`:

```js
const MAX_TOP_ITEMS       = 50;   // tracks/artists per time range
const MAX_PLAYLISTS       = 20;   // playlists to fetch
const MAX_PLAYLIST_TRACKS = 100;  // tracks per playlist
const MAX_SAVED_TRACKS    = 200;  // saved-library pages
const MAX_RECENTLY_PLAYED = 50;   // recently-played events
const SYNC_TTL_MS         = 60 * 60 * 1000; // re-use cache for 1 hour
```

### Two-user comparison

When a second user authenticates and their profile is synced:

1. The app detects the previously stored profile in `localStorage`.
2. A **Taste Comparison** panel appears in the room showing:
   - Overall match percentage (weighted cosine + genre + artist overlap)
   - Taste horoscope ("music soulmates" / "interesting overlap" / etc.)
   - Shared artists, shared genres, shared top tracks
   - "Only A likes" / "Only B likes" artist lists
   - Up to 5 bridge tracks scored against the midpoint taste profile
   - Audio feature similarity, genre overlap, and overall match scores

### Running a two-person demo locally

1. Person A opens the page and clicks **Connect Spotify** → authenticates → full sync runs → profile saved to `localStorage`.
2. Person B (in the **same browser**) opens the page and clicks **Connect Spotify** → authenticates with a different Spotify account → full sync runs → comparison panel appears automatically.

> Both profiles are stored in the browser's `localStorage`. They persist across page reloads but are **never sent to any server** — visible only in your browser.

### Managing stored profiles

- The **Synced Profiles** section on the landing page shows all stored profiles with their summary, top genres, and a **Remove** button.
- A **Clear All** button resets all stored profiles.
- To force a re-sync (bypassing the 1-hour cache), remove your profile via the landing page and re-authenticate.

### Scopes required

Add all of the following to your Spotify app's **Redirect URIs** and **Scopes** in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard):

```
user-top-read
user-read-recently-played
user-read-currently-playing
user-read-playback-state
user-read-private
user-library-read
user-follow-read
```

