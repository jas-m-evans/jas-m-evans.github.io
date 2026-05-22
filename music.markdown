---
layout: single
title: "Music"
permalink: /music/
author_profile: true
classes: music-page
---

<div class="music-shell">
  <section class="music-hero">
    <div class="music-hero__copy">
      <p class="music-kicker">Live drums • heavy pocket • sharp edges</p>
      <h1>Music // Live System</h1>
      <p>Drums are the part of the stack where instinct, timing, and control all have to survive impact. I like loud rooms, hard transitions, and parts that still breathe under pressure.</p>
      <p>The current setup centers on a Ludwig NeuSonic kit with a Ludwig Black Beauty snare, Sabian HH hats, Sabian AAX crashes, and an XS20 ride.</p>
      <ul class="music-statline">
        <li>Live-ready timing</li>
        <li>Aggressive dynamics</li>
        <li>Studio-tight choices</li>
      </ul>
      <div class="music-actions">
        {% if site.spotify_url and site.spotify_url != "" %}
          <a class="btn btn--music" href="{{ site.spotify_url }}" target="_blank" rel="noopener noreferrer">Current Band</a>
        {% endif %}
        <a class="btn btn--music-outline" href="/projects/">Related Projects</a>
      </div>
    </div>

    <div class="music-hero__visual">
      <div class="music-portrait">
        <img src="/assets/images/me.jpeg" alt="Portrait of Jason Evans" loading="eager" decoding="async">
      </div>
      <div class="music-sprite-card music-sprite-card--player" aria-hidden="true">
        <span class="music-sprite-card__tag">PLAYER 01</span>
        <span class="music-sprite music-sprite--player"></span>
      </div>
      <div class="music-sprite-card music-sprite-card--kit" aria-hidden="true">
        <span class="music-sprite-card__tag">KIT LOAD</span>
        <span class="music-sprite music-sprite--kit"></span>
      </div>
    </div>
  </section>

  <section class="music-overview">
    <article class="music-card">
      <h2>Live Focus</h2>
      <p>Groove consistency first, then the dynamic hits. The goal is to make heavy songs feel locked instead of loose.</p>
    </article>
    <article class="music-card">
      <h2>Practice Loop</h2>
      <p>Subdivision work, displacement drills, and short record-review cycles keep the details honest.</p>
    </article>
    <article class="music-card">
      <h2>Studio Mindset</h2>
      <p>Fast intentional choices, clean takes, and just enough air around the part to let the song hit harder.</p>
    </article>
  </section>

  <section class="music-loadout">
    <div class="music-section-heading">
      <p class="music-kicker">Gear loadout</p>
      <h2>Drum Arsenal</h2>
      <p>A darker, game-inventory view of the pieces I actually lean on.</p>
    </div>
    <div class="music-loadout-grid">
      <article class="music-slot">
        <span class="music-slot__label">Snare</span>
        <h3>Ludwig Black Beauty</h3>
        <p>Fast crack, dense body, and enough cut to stay present when the room gets ugly.</p>
      </article>
      <article class="music-slot">
        <span class="music-slot__label">Kit</span>
        <h3>Ludwig NeuSonic</h3>
        <p>The center of the setup: punchy shells that stay controlled live and focused on a mic.</p>
      </article>
      <article class="music-slot">
        <span class="music-slot__label">Hi-Hats</span>
        <h3>Sabian HH Hats</h3>
        <p>Dark bite with clear definition for tight openings, ghost-note detail, and fast foot work.</p>
      </article>
      <article class="music-slot">
        <span class="music-slot__label">Crashes</span>
        <h3>Sabian AAX</h3>
        <p>Quick response and bright attack for the accents that need to jump out instantly.</p>
      </article>
      <article class="music-slot">
        <span class="music-slot__label">Ride</span>
        <h3>Sabian XS20</h3>
        <p>Solid stick definition with enough wash to open up without losing the pulse.</p>
      </article>
      <article class="music-slot">
        <span class="music-slot__label">Hardware</span>
        <h3>Locked-In Stands</h3>
        <p>Stability matters. If the hardware moves, the pocket moves with it.</p>
      </article>
      <article class="music-slot">
        <span class="music-slot__label">Sticks</span>
        <h3>Attack Layer</h3>
        <p>The last part of the chain: rebound, weight, and consistency that keep the whole kit speaking evenly.</p>
      </article>
      <article class="music-slot">
        <span class="music-slot__label">Mode</span>
        <h3>Stage Pressure</h3>
        <p>Play hard, stay in control, and leave enough headroom for the song to breathe.</p>
      </article>
    </div>
  </section>

  <section class="music-lane">
    {% if site.spotify_embed_url and site.spotify_embed_url != "" %}
      <section class="music-embed">
        <h2>Now Playing</h2>
        <iframe src="{{ site.spotify_embed_url }}" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
      </section>
    {% else %}
      <section class="music-note">
        <h2>Now Playing</h2>
        <p>Add spotify_embed_url in _config.yml to activate listening embeds on this page.</p>
      </section>
    {% endif %}

    <section class="music-note">
      <h2>Stage Notes</h2>
      <p>This page is meant to feel like a dark menu screen instead of a stack of disconnected widgets: one lane for the current band, one for the rig, one for the mentality behind it.</p>
      <p>The floating character cards keep the game influence, but the page now leads with cleaner visuals and a tighter flow.</p>
    </section>
  </section>

  {% comment %}
    Dead Pixel / previous band section intentionally removed from the page.

    {% if site.spotify_prev_embed_url and site.spotify_prev_embed_url != "" %}
      <section class="music-embed">
        <h2>Previous Project</h2>
        <iframe src="{{ site.spotify_prev_embed_url }}" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
      </section>
    {% endif %}

    {% if site.spotify_prev_url and site.spotify_prev_url != "" %}
      <section class="music-note">
        <h2>Previous Band</h2>
        <p>Old project link only, no picture embed:</p>
        <a class="btn btn--music-outline" href="{{ site.spotify_prev_url }}" target="_blank" rel="noopener noreferrer">Open Previous Band on Spotify</a>
      </section>
    {% endif %}
  {% endcomment %}
</div>