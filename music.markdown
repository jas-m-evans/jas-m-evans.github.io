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
      <p class="music-kicker">Drums • 20+ years • jazz to punk</p>
      <h1>Drummer for loud rooms and locked-in songs</h1>
      <p>I've played drums for 20+ years across jazz, rock, and folk, with a natural pull toward punk rock.</p>
      <p>I care about time, feel, and parts that hit hard without getting messy.</p>
      <ul class="music-statline">
        <li>20+ years playing</li>
        <li>Jazz → rock → folk</li>
        <li>Leaning punk rock</li>
      </ul>
      <div class="music-actions">
        {% if site.spotify_url and site.spotify_url != "" %}
          <a class="btn btn--music" href="{{ site.spotify_url }}" target="_blank" rel="noopener noreferrer">Current Band</a>
        {% endif %}
        <a class="btn btn--music-outline" href="#music-contact">Gig Inquiries</a>
      </div>
    </div>

    <div class="music-hero__visual">
      <section class="music-note music-note--compact">
        <h2>Available for</h2>
        <ul class="music-list">
          <li>Gigs and fill-ins</li>
          <li>Session tracking</li>
          <li>Fast learning, solid pocket</li>
        </ul>
      </section>
      <section class="music-note music-note--compact">
        <h2>Current setup</h2>
        <p>Ludwig NeuSonic kit, Ludwig Black Beauty snare, Sabian HH hats, Sabian AAX crashes, and an XS20 ride.</p>
      </section>
    </div>
  </section>

  <section class="music-overview">
    <article class="music-card">
      <h2>20+ Years</h2>
      <p>Long enough to know when a song needs space, when it needs force, and when it needs both.</p>
    </article>
    <article class="music-card">
      <h2>Range</h2>
      <p>Jazz phrasing, rock weight, folk restraint, and punk energy all show up in the way I play.</p>
    </article>
    <article class="music-card">
      <h2>What Matters</h2>
      <p>Good pocket, clean dynamics, quick prep, and serving the song instead of crowding it.</p>
    </article>
  </section>

  <section class="music-loadout">
    <div class="music-section-heading">
      <p class="music-kicker">Gear loadout</p>
      <h2>Drum Inventory</h2>
      <p>Current gigging setup built for punch, control, and fast changeovers.</p>
    </div>
    <div class="music-inventory" aria-label="Interactive drum gear inventory">
      <details class="music-item">
        <summary class="music-item__summary">
          <span class="music-item__slot">Snare</span>
          <span class="music-item__media" aria-hidden="true">
            <img src="{{ '/assets/images/music/black-beauty-snare.svg' | relative_url }}" alt="" loading="lazy" decoding="async" width="640" height="440">
          </span>
          <span class="music-item__body">
            <span class="music-item__name">Ludwig Black Beauty</span>
            <span class="music-item__spec">6.5x14 • black nickel over brass</span>
          </span>
          <span class="music-item__hint">
            <span>Tone note</span>
            <svg class="music-item__chevron" viewBox="0 0 16 16" aria-hidden="true" focusable="false">
              <path d="M3.5 6.25 8 10.75l4.5-4.5" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75"></path>
            </svg>
          </span>
        </summary>
        <div class="music-item__details">
          <p>Sharp crack up front, full body underneath.</p>
        </div>
      </details>
      <details class="music-item">
        <summary class="music-item__summary">
          <span class="music-item__slot">Kit</span>
          <span class="music-item__media" aria-hidden="true">
            <img src="{{ '/assets/images/music/neusonic-kit.svg' | relative_url }}" alt="" loading="lazy" decoding="async" width="640" height="440">
          </span>
          <span class="music-item__body">
            <span class="music-item__name">Ludwig NeuSonic</span>
            <span class="music-item__spec">Butterscotch Pearl wrap • punchy live shells</span>
          </span>
          <span class="music-item__hint">
            <span>Tone note</span>
            <svg class="music-item__chevron" viewBox="0 0 16 16" aria-hidden="true" focusable="false">
              <path d="M3.5 6.25 8 10.75l4.5-4.5" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75"></path>
            </svg>
          </span>
        </summary>
        <div class="music-item__details">
          <p>Punchy shells that stay tight live and focused on a mic.</p>
        </div>
      </details>
      <details class="music-item">
        <summary class="music-item__summary">
          <span class="music-item__slot">Hi-Hats</span>
          <span class="music-item__media" aria-hidden="true">
            <img src="{{ '/assets/images/music/sabian-hh-hats.svg' | relative_url }}" alt="" loading="lazy" decoding="async" width="640" height="440">
          </span>
          <span class="music-item__body">
            <span class="music-item__name">Sabian HH Hats</span>
            <span class="music-item__spec">Dark bite with clear definition</span>
          </span>
          <span class="music-item__hint">
            <span>Tone note</span>
            <svg class="music-item__chevron" viewBox="0 0 16 16" aria-hidden="true" focusable="false">
              <path d="M3.5 6.25 8 10.75l4.5-4.5" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75"></path>
            </svg>
          </span>
        </summary>
        <div class="music-item__details">
          <p>Dark bite with clear definition when the part gets busy.</p>
        </div>
      </details>
      <details class="music-item">
        <summary class="music-item__summary">
          <span class="music-item__slot">Crashes</span>
          <span class="music-item__media" aria-hidden="true">
            <img src="{{ '/assets/images/music/sabian-aax-crashes.svg' | relative_url }}" alt="" loading="lazy" decoding="async" width="640" height="440">
          </span>
          <span class="music-item__body">
            <span class="music-item__name">Sabian AAX Crashes</span>
            <span class="music-item__spec">Fast attack and quick clear-out</span>
          </span>
          <span class="music-item__hint">
            <span>Tone note</span>
            <svg class="music-item__chevron" viewBox="0 0 16 16" aria-hidden="true" focusable="false">
              <path d="M3.5 6.25 8 10.75l4.5-4.5" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75"></path>
            </svg>
          </span>
        </summary>
        <div class="music-item__details">
          <p>They open fast, hit hard, and clear out quickly.</p>
        </div>
      </details>
      <details class="music-item">
        <summary class="music-item__summary">
          <span class="music-item__slot">Ride</span>
          <span class="music-item__media" aria-hidden="true">
            <img src="{{ '/assets/images/music/sabian-xs20-ride.svg' | relative_url }}" alt="" loading="lazy" decoding="async" width="640" height="440">
          </span>
          <span class="music-item__body">
            <span class="music-item__name">Sabian XS20 Ride</span>
            <span class="music-item__spec">Clear stick definition with controlled wash</span>
          </span>
          <span class="music-item__hint">
            <span>Tone note</span>
            <svg class="music-item__chevron" viewBox="0 0 16 16" aria-hidden="true" focusable="false">
              <path d="M3.5 6.25 8 10.75l4.5-4.5" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75"></path>
            </svg>
          </span>
        </summary>
        <div class="music-item__details">
          <p>Stick definition stays clear even when the wash opens up.</p>
        </div>
      </details>
      <details class="music-item">
        <summary class="music-item__summary">
          <span class="music-item__slot">Sticks</span>
          <span class="music-item__media" aria-hidden="true">
            <img src="{{ '/assets/images/music/travis-barker-sticks.svg' | relative_url }}" alt="" loading="lazy" decoding="async" width="640" height="440">
          </span>
          <span class="music-item__body">
            <span class="music-item__name">Travis Barker Zildjian</span>
            <span class="music-item__spec">White signature pair for weight and rebound</span>
          </span>
          <span class="music-item__hint">
            <span>Tone note</span>
            <svg class="music-item__chevron" viewBox="0 0 16 16" aria-hidden="true" focusable="false">
              <path d="M3.5 6.25 8 10.75l4.5-4.5" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75"></path>
            </svg>
          </span>
        </summary>
        <div class="music-item__details">
          <p>Enough weight for rimshots, enough rebound to stay loose.</p>
        </div>
      </details>
    </div>
  </section>

  <section class="music-lane">
    {% if site.spotify_embed_url and site.spotify_embed_url != "" %}
      <section class="music-embed">
        <h2>Current Band</h2>
        <iframe src="{{ site.spotify_embed_url }}" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
      </section>
    {% else %}
      <section class="music-note">
        <h2>Current Band</h2>
        <p>Add spotify_embed_url in _config.yml to activate listening embeds on this page.</p>
      </section>
    {% endif %}

    <section class="music-note music-contact" id="music-contact">
      <h2>Gig Inquiries</h2>
      <p>For gigs, fill-ins, or session work, send a quick note.</p>
      <form class="music-form" action="mailto:{{ site.email }}?subject=Music%20Inquiry" method="post" enctype="text/plain">
        <label for="music-name">Name</label>
        <input id="music-name" name="Name" type="text" autocomplete="name">

        <label for="music-contact">Email</label>
        <input id="music-contact" name="Email" type="email" autocomplete="email">

        <label for="music-message">What do you need?</label>
        <textarea id="music-message" name="Message" rows="5" placeholder="Gig date, city, set length, or anything else helpful."></textarea>

        <button class="btn btn--music" type="submit">Start Email</button>
      </form>
      <p class="music-form__note">This opens your email app with the details ready to send.</p>
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