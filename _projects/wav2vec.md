---
title: "Wave·Defect: Live Music Intelligence with Spotify × LiveKit"
description: "A public-facing demo combining Spotify OAuth, real-time music recommendations, and LiveKit data channels — connect your Spotify and see your taste alongside Jason's, live. (Formerly Wave2Vector Lab.)"
layout: project
image: "/assets/images/projects/wav2vec-audio-lab.svg"
---

## Try the Live Demo

[**→ Open the Wave·Defect Demo**](/wave-defect-demo/){: .btn .btn--primary}
{: style="margin-bottom:1.2rem"}

Authenticate with your Spotify account and see your music profile alongside Jason's pre-loaded recommendations — delivered live over a LiveKit data channel. No backend, no account needed beyond Spotify.

---

## What This Is Now

Wave·Defect (formerly Wave2Vector Lab) started as an audio similarity lab (MFCC embeddings, nearest-neighbor retrieval). It has evolved into a shareable **music intelligence demo** that connects two ideas:

1. **Personal music taste is data.** Spotify's API exposes rich listening history, top tracks, and genre signals that can be compared and visualized in real time.

2. **Real-time infrastructure makes it interesting.** LiveKit's data channels can broadcast structured music data between participants without a complex backend — making the experience feel live rather than static.

The demo makes both ideas tangible in a single sharable URL.

## How the Demo Works

When a guest opens the link and authenticates with Spotify:

1. **Spotify PKCE OAuth** runs entirely in the browser — no secrets, no server round-trip.
2. The guest's **top tracks and listening profile** are fetched from the Spotify Web API.
3. **Jason's pre-stored recommendations** (saved in the Wave·Defect database) load immediately — no re-authentication required.
4. A simulated **LiveKit room** (`wave-defect-lab`) shows both participants, a live data channel streaming track metadata, and real-time latency metrics.
5. A **"Now Playing" panel** polls the guest's current Spotify playback and updates live.
6. The guest sees a **side-by-side profile comparison**: Jason's taste vs. their own.

The whole experience runs on GitHub Pages as a static HTML file backed by client-side JavaScript.

## Why LiveKit

LiveKit provides the real-time data transport layer. In a full production deployment, the architecture would look like this:

- A **LiveKit room** per listening session
- **Data channels** broadcasting track embeddings and similarity scores between participants
- **Server-side agents** generating recommendations using audio feature vectors
- **Live metrics** (latency, bandwidth, participant count) surfaced in the UI

The demo simulates this architecture visually and functionally to show what the integration point looks like before a server is provisioned.

## Original Audio-Similarity Pipeline

The underlying retrieval engine remains intact:

1. Decode audio with `librosa`
2. Extract MFCCs (`n_mfcc=20`)
3. Build a 40-D embedding from mean + std statistics
4. Store metadata and vectors in SQLite via SQLModel
5. Compute nearest neighbors with cosine distance

The pivot is in the data source: instead of user-uploaded `.wav` files, the vectors now represent Spotify track features, enabling cross-listener comparisons with minimal friction.

## Tech Stack

**Demo frontend (this page)**
- Vanilla HTML/CSS/JS — runs on GitHub Pages
- Spotify Web API + PKCE OAuth (client-side)
- LiveKit JS design patterns (data channel simulation)

**Core application (wave2vector)**
- Python, FastAPI, Jinja2
- SQLModel + SQLite
- librosa + NumPy + Matplotlib
- Web Audio API (real-time playback visualizer)

## Repository

- GitHub: [jas-m-evans/wave2vector](https://github.com/jas-m-evans/wave2vector)

## Sources

1. Spotify Web API reference: <https://developer.spotify.com/documentation/web-api>
2. LiveKit documentation: <https://docs.livekit.io>
3. OAuth 2.0 PKCE flow: <https://datatracker.ietf.org/doc/html/rfc7636>
4. Librosa documentation: <https://librosa.org/doc/latest/index.html>

## Policy Note

This writeup focuses on architecture, methods, and product-facing behavior. It does not reproduce external proprietary content. Spotify API usage follows Spotify's Developer Policy. LiveKit is used as a referenced integration point.
