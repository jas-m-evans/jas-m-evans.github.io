---
layout: single
title: "Music"
permalink: /music/
author_profile: true
classes: music-page
---

<div class="music-shell">
  <section class="music-hero">
    <h1>Music Lab</h1>
    <p>Live drums are my favorite real-time systems problem: listen fast, lock in hard, and keep control when the room gets chaotic.</p>
    <p>Current rig: Ludwig NeuSonic kit, Ludwig Black Beauty snare, Sabian AAX crashes, Sabian HH hats, XS20 ride.</p>
    <p>This page is intentionally dark and pixel-styled to match the vibe: arcade energy, tight timing, no fluff.</p>
    <div class="music-actions">
      {% if site.spotify_url and site.spotify_url != "" %}
        <a class="btn btn--music" href="{{ site.spotify_url }}" target="_blank" rel="noopener noreferrer">Current Band</a>
      {% endif %}
      <a class="btn btn--music-outline" href="/projects/">Related Projects</a>
    </div>
  </section>

  <section class="music-pixel-stage">
    <article class="music-pixel-card">
      <h2>Pixel Me</h2>
      <svg class="pixel-svg" viewBox="0 0 16 16" role="img" aria-label="Pixel portrait of Jason with drumsticks">
        <rect width="16" height="16" fill="#10141f"/>
        <rect x="5" y="1" width="6" height="2" fill="#1f2535"/>
        <rect x="4" y="3" width="8" height="1" fill="#2b3248"/>
        <rect x="4" y="4" width="8" height="4" fill="#f6c58e"/>
        <rect x="5" y="5" width="1" height="1" fill="#232738"/>
        <rect x="10" y="5" width="1" height="1" fill="#232738"/>
        <rect x="6" y="7" width="4" height="1" fill="#e7a96f"/>
        <rect x="3" y="8" width="10" height="4" fill="#6b79ff"/>
        <rect x="2" y="10" width="2" height="4" fill="#f6c58e"/>
        <rect x="12" y="10" width="2" height="4" fill="#f6c58e"/>
        <rect x="1" y="9" width="4" height="1" fill="#d7b173"/>
        <rect x="11" y="9" width="4" height="1" fill="#d7b173"/>
        <rect x="5" y="12" width="2" height="3" fill="#2e3a58"/>
        <rect x="9" y="12" width="2" height="3" fill="#2e3a58"/>
      </svg>
    </article>

    <article class="music-pixel-card">
      <h2>Pixel Drum Gear</h2>
      <svg class="pixel-svg pixel-svg--wide" viewBox="0 0 24 16" role="img" aria-label="Pixel drum kit with cymbals">
        <rect width="24" height="16" fill="#10141f"/>
        <rect x="2" y="3" width="4" height="1" fill="#f8c44f"/>
        <rect x="18" y="3" width="4" height="1" fill="#f8c44f"/>
        <rect x="3" y="4" width="2" height="5" fill="#8fa2c4"/>
        <rect x="19" y="4" width="2" height="5" fill="#8fa2c4"/>
        <rect x="8" y="6" width="8" height="5" fill="#d55572"/>
        <rect x="9" y="7" width="6" height="3" fill="#ff7892"/>
        <rect x="5" y="8" width="3" height="3" fill="#4f5f88"/>
        <rect x="16" y="8" width="3" height="3" fill="#4f5f88"/>
        <rect x="10" y="11" width="4" height="4" fill="#4f5f88"/>
        <rect x="11" y="12" width="2" height="3" fill="#2d3856"/>
      </svg>
    </article>
  </section>

  <section class="music-grid">
    <article class="music-card">
      <h2>Live Focus</h2>
      <p>Groove consistency, sharp dynamics, and clean transitions in loud, messy rooms.</p>
    </article>
    <article class="music-card">
      <h2>Practice Loop</h2>
      <p>Subdivision work, displacement drills, and short recording/review cycles.</p>
    </article>
    <article class="music-card">
      <h2>Studio Mindset</h2>
      <p>Fast intentional choices, tight takes, and enough space for songs to breathe.</p>
    </article>
  </section>

  {% if site.spotify_embed_url and site.spotify_embed_url != "" %}
    <section class="music-embed">
      <h2>Now Playing</h2>
      <iframe src="{{ site.spotify_embed_url }}" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
    </section>
  {% else %}
    <section class="music-note">
      Add spotify_embed_url in _config.yml to activate listening embeds on this page.
    </section>
  {% endif %}

  {% comment %}
    Previous artist visual embed intentionally disabled (no image panel wanted on this page).
    {% if site.spotify_prev_embed_url and site.spotify_prev_embed_url != "" %}
      <section class="music-embed">
        <h2>Previous Project</h2>
        <iframe src="{{ site.spotify_prev_embed_url }}" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
      </section>
    {% endif %}
  {% endcomment %}

  {% if site.spotify_prev_url and site.spotify_prev_url != "" %}
    <section class="music-note">
      <h2>Previous Band</h2>
      <p>Old project link only, no picture embed:</p>
      <a class="btn btn--music-outline" href="{{ site.spotify_prev_url }}" target="_blank" rel="noopener noreferrer">Open Previous Band on Spotify</a>
    </section>
  {% endif %}
</div>