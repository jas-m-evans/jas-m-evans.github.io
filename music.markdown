---
layout: single
title: "Music"
permalink: /music/
author_profile: true
---

<div class="music-shell">
  <section class="music-hero">
    <h1>Music</h1>
    <p>I play drums professionally, which is a very efficient way to combine timing, controlled violence, logistics, and problem-solving into one activity. My current band is <strong>Plotting</strong>, I play gigs, I get paid, I haul hardware around, and I keep writing new music because apparently I do not know how to relax in a normal way.</p>
    <p>There are obvious differences between engineering and drumming, but not as many as you would think. The challenge is not just hitting things hard. The harder problem is consistency, feel, dynamics, restraint, and making the whole thing lock in without sounding like you are doing calculus at the kit. That part takes work.</p>
    <div class="music-actions">
      {% if site.spotify_url != "" %}
        <a href="{{ site.spotify_url }}" class="btn btn--primary">Listen to Plotting</a>
      {% endif %}
      <a href="https://open.spotify.com/artist/6A0yJMXzU5N9a7vXe9hCuG" class="btn btn--light-outline">Spotify Artist Page</a>
      <a href="mailto:{{ site.email }}" class="btn btn--light-outline">Get in touch</a>
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
      <h2>What This Actually Means</h2>
      <p>I am not using “music” here to mean I casually enjoy albums while coding. I mean I play drums in real bands, show up to gigs, rehearse seriously, and build songs with other people in rooms that are usually too loud and occasionally too cold.</p>
    </article>
    <article class="music-card">
      <h2>Why It Fits Here</h2>
      <p>A lot of my school and engineering work is about iteration, structure, signal vs. noise, and keeping systems stable under pressure. Drumming is weirdly similar, except the feedback is immediate and if the system fails, everyone in the room notices faster.</p>
    </article>
    <article class="music-card">
      <h2>Current Focus</h2>
      <p>Right now the center of gravity is Plotting, plus new writing and recording work in the background. I have also played in other bands that landed on Spotify, which is nice because it means there is permanent evidence that I spent years learning how to hit drums in time.</p>
    </article>
  </section>

  <section class="music-grid">
    <article class="music-card">
      <h2>Current Setup</h2>
      <p><strong>Kit:</strong> Ludwig NeuSonic series kit.</p>
      <p><strong>Cymbals:</strong> Sabian AAX crashes, Sabian HH hi-hats, and what appears to be a Sabian XS20 ride, which feels right both sonically and morally.</p>
    </article>
    <article class="music-card">
      <h2>Playing Style</h2>
      <p>Most of what I care about behind the kit is pocket, energy, and making heavy music feel alive instead of stiff. Fast is useful. Loud is useful. But groove is the thing that actually pays rent.</p>
    </article>
    <article class="music-card">
      <h2>Professional Summary</h2>
      <p>If you want the short version: I am a drummer who likes aggressive music, good arrangement choices, and not overplaying. I enjoy writing parts that serve the song, then occasionally ignoring that principle for one fill when the moment is right.</p>
    </article>
  </section>

  {% if site.spotify_embed_url != "" %}
    <section class="music-embed">
      <iframe src="{{ site.spotify_embed_url }}" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
    </section>
  {% else %}
    <section class="music-note">
      Add Spotify URLs in the site config to activate listening embeds on this page.
    </section>
  {% endif %}

  <section class="music-note">
    Music is in here for the same reason the project pages are in here: it is real work, it reflects how I think, and it has taken a lot of repetition, failure, tuning, and stubbornness to get good enough to do professionally.
  </section>
</div>