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

### Demo mode

Anyone can try the experience without connecting Spotify. Entering a name generates a deterministic taste profile from that name string (xorshift32 seeded from the name hash), then runs the full recommender against Jason's real profile.

### Backend integration

This static demo runs entirely in the browser. To connect it to the full [wave2vector](https://github.com/jas-m-evans/wave2vector) FastAPI backend (with real LiveKit rooms, persistence, and multi-user support), set `BACKEND_URL` at the top of the script block in `wave-defect-demo.html` to your deployed backend URL.
