---
layout: single
title: "Music"
permalink: /music/
author_profile: true
---

<div class="music-shell">
  <section class="music-hero">
    <h1>Music</h1>
    <p>I play drums professionally: gigs, rehearsals, writing, load-ins, and all the glamorous hardware hauling in between. Drumming is my favorite kind of system under pressure, where timing, control, and energy have to be right in real time.</p>
    <p>Current setup: Ludwig NeuSonic series kit, Sabian AAX crashes, Sabian HH hi-hats, and an XS20 ride.</p>
    <div class="music-actions">
      {% if site.spotify_url != "" %}
        <a href="{{ site.spotify_url }}" class="btn btn--primary">Spotify Profile</a>
      {% endif %}
      {% if site.spotify_prev_url != "" %}
        <a href="{{ site.spotify_prev_url }}" class="btn btn--light-outline">Previous Work</a>
      {% endif %}
    </div>
    <div class="music-wave" aria-hidden="true">
      <span style="height: 46%"></span>
      <span style="height: 78%"></span>
      <span style="height: 60%"></span>
      <span style="height: 92%"></span>
      <span style="height: 52%"></span>
      <span style="height: 86%"></span>
      <span style="height: 38%"></span>
      <span style="height: 72%"></span>
      <span style="height: 58%"></span>
      <span style="height: 88%"></span>
      <span style="height: 44%"></span>
      <span style="height: 66%"></span>
    </div>
  </section>

  {% if site.spotify_embed_url != "" %}
    <section class="music-embed">
      <h2>Previous Work I</h2>
      <iframe src="{{ site.spotify_embed_url }}" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
    </section>
  {% else %}
    <section class="music-note">
      Add Spotify URLs in the site config to activate listening embeds on this page.
    </section>
  {% endif %}

  {% if site.spotify_prev_embed_url != "" %}
    <section class="music-embed">
      <h2>Previous Work II</h2>
      <iframe src="{{ site.spotify_prev_embed_url }}" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
    </section>
  {% endif %}
</div>