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
    <p>Current setup: Ludwig NeuSonic series kit, Ludwig Black Beauty snare, Sabian AAX crashes, Sabian HH hi-hats, and an XS20 ride.</p>
    <p>Drumming and building software systems scratch the same itch for me. In both, the challenge is not just doing something flashy once. The harder problem is building repeatable control under pressure, staying locked in when conditions get messy, and making the final output feel clean even when the process definitely was not.</p>
    <p>That same mindset has shaped my recent project work too, from <a href="/projects/autonomous-drone-slam.html">drone SLAM</a> and <a href="/projects/ml4t-strategy-learner.html">strategy learning systems</a> to representation-learning experiments like <a href="/projects/wav2vec.html">Wave2Vector</a>. Building those felt a lot like drumming in a new room: listen first, find the tempo, adapt quickly, and keep the whole system locked together.</p>
    <div class="music-actions">
      {% if site.spotify_url and site.spotify_url != "" %}
        <a class="btn btn--music" href="{{ site.spotify_url }}" target="_blank" rel="noopener noreferrer">Spotify Profile</a>
      {% endif %}
      <a class="btn btn--light-outline" href="/projects/">Related Projects</a>
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

  <section class="music-grid">
    <article class="music-card">
      <h2>Performance Focus</h2>
      <p>Live groove consistency, fast dynamic control, and clean transitions in high-noise environments.</p>
    </article>
    <article class="music-card">
      <h2>Practice Loop</h2>
      <p>Subdivision timing, metronome displacement drills, and short endurance blocks with recording review.</p>
    </article>
    <article class="music-card">
      <h2>Studio Mindset</h2>
      <p>Build tight takes under pressure, make intentional choices early, and leave room for the song to breathe.</p>
    </article>
  </section>

  {% if site.spotify_embed_url and site.spotify_embed_url != "" %}
    <section class="music-embed">
      <h2>Listening</h2>
      <iframe src="{{ site.spotify_embed_url }}" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
    </section>
  {% else %}
    <section class="music-note">
      Add spotify_embed_url in _config.yml to activate listening embeds on this page.
    </section>
  {% endif %}

  {% if site.spotify_prev_embed_url and site.spotify_prev_embed_url != "" %}
    <section class="music-embed">
      <h2>Previous Project</h2>
      <iframe src="{{ site.spotify_prev_embed_url }}" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
    </section>
  {% endif %}
</div>