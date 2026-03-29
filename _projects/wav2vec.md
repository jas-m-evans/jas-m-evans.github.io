---
title: "Wave2Vector Lab: Listening for Similarity"
description: "An interactive audio similarity lab for uploads, MFCC embeddings, live playback visualization, and nearest-neighbor discovery."
layout: project
---

## The Problem: Audio Search Usually Feels Invisible

When most people hear "audio ML," they expect a black box:

Upload file in.
Get score out.

That works for demos, but not for intuition.

This project asks a more practical question:

**Can audio similarity feel inspectable, interactive, and understandable to a user in real time?**

Instead of starting with labels, this system starts with signal structure: waveform, spectrum, embedding, and distance.

## Project Direction

Wave2Vector Lab is not a speech-to-text model. It is an audio retrieval and exploration tool.

Users can:

- Upload clips (`.wav`, `.mp3`, `.m4a`)
- Generate MFCC-based embeddings and plot artifacts
- Play clips directly in the browser
- Inspect nearest neighbors with match bars and distance values
- Watch a live playback visualizer with real-time metrics

The point is to make similarity *auditable* instead of magical.

## Why This Is Interesting

The fun part is the bridge between DSP and UX.

Most feature extraction projects stop at "vector computed."
This one keeps going and asks:

- What does this clip look like?
- What does it sound like right now?
- Why did this neighbor rank near the top?
- Is my sample quality hurting the comparison?

That led to three design choices:

1. **Feature transparency**
	 Surface vectors, summary stats, and dominant components.

2. **Playback-first analysis**
	 Every major view includes audio controls and contextual visuals.

3. **Low-friction exploration**
	 A demo seeding flow adds starter clips so users can test neighbors immediately.

## Core Pipeline

At upload time, the app:

1. Decodes audio with `librosa`
2. Extracts MFCCs (`n_mfcc=20`)
3. Builds a 40-D embedding from mean+std statistics
4. Saves waveform and spectrogram plots
5. Stores metadata and vectors in SQLite via SQLModel
6. Computes nearest neighbors with cosine distance

On the clip detail page, the real-time visualizer uses the Web Audio API analyzer node to render:

- Time-domain waveform traces
- Frequency bars
- Live metrics: clock, RMS, peak, and spectral centroid

## UX and Product Lessons

Two practical insights emerged while building:

- **Interpretability changes trust**
	Users engage more when they can hear, see, and inspect why a match appears.

- **Cold-start matters more than algorithm purity**
	Demo seeding and built-in playback remove the "upload five files first" friction.

- **Small quality signals improve behavior**
	Sample-rate quality labels steer expectations and explain noisy comparisons.

## Repository

- GitHub: https://github.com/jas-m-evans/wave2vector

## Tech Stack

- Python, FastAPI, Jinja2
- SQLModel + SQLite
- librosa + NumPy + Matplotlib
- HTML/CSS/JS + Web Audio API (front-end visualizer)

## Current Status

Project is fully functional and actively evolving.

Current implementation includes:

- Bold, responsive UI
- Clip-level audio playback
- Real-time creative visualizer during playback
- Nearest-neighbor cards with similarity graphics
- Duplicate-safe demo seeding workflow

## Artifacts and Provenance

- App repository: https://github.com/jas-m-evans/wave2vector
- Main web service: `app/main.py`
- Templates: `app/templates/index.html`, `app/templates/clip_detail.html`
- Styling: `app/static/styles.css`
- Data model: `app/models.py`, `app/schemas.py`

## Sources

1. Librosa documentation: https://librosa.org/doc/latest/index.html
2. FastAPI documentation: https://fastapi.tiangolo.com/
3. Web Audio API reference: https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API
4. scikit-learn cosine similarity reference (conceptual): https://scikit-learn.org/stable/modules/metrics.html#cosine-similarity

## Reader-Friendly TL;DR

This is an audio similarity lab, not a transcription model.

You upload sound, the system turns it into a feature vector, and then you can explore what is close, why it is close, and how the signal behaves while it plays.

## Policy Note

This writeup focuses on architecture, methods, and product-facing behavior. It does not reproduce external proprietary content.
