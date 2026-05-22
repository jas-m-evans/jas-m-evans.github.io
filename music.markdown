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
      <p>Hover or click a slot for the short version.</p>
    </div>
    <div class="music-inventory" aria-label="Interactive drum gear inventory">
      <article class="music-item">
        <button type="button" class="music-item__button" aria-describedby="music-item-snare-tip">
          <span class="music-item__slot">Snare</span>
          <span class="music-pixel music-pixel--snare" aria-hidden="true"></span>
          <span class="music-item__name">Black Beauty</span>
        </button>
        <div class="music-item__tooltip" id="music-item-snare-tip">
          <strong>Ludwig Black Beauty</strong>
          <span>Sharp crack up front, full body underneath.</span>
        </div>
      </article>
      <article class="music-item">
        <button type="button" class="music-item__button" aria-describedby="music-item-kit-tip">
          <span class="music-item__slot">Kit</span>
          <span class="music-pixel music-pixel--kit" aria-hidden="true"></span>
          <span class="music-item__name">NeuSonic</span>
        </button>
        <div class="music-item__tooltip" id="music-item-kit-tip">
          <strong>Ludwig NeuSonic</strong>
          <span>Punchy shells that stay tight live and focused on a mic.</span>
        </div>
      </article>
      <article class="music-item">
        <button type="button" class="music-item__button" aria-describedby="music-item-hats-tip">
          <span class="music-item__slot">Hi-Hats</span>
          <span class="music-pixel music-pixel--hats" aria-hidden="true"></span>
          <span class="music-item__name">Sabian HH</span>
        </button>
        <div class="music-item__tooltip" id="music-item-hats-tip">
          <strong>Sabian HH Hats</strong>
          <span>Dark bite with clear definition when the part gets busy.</span>
        </div>
      </article>
      <article class="music-item">
        <button type="button" class="music-item__button" aria-describedby="music-item-crash-tip">
          <span class="music-item__slot">Crashes</span>
          <span class="music-pixel music-pixel--crash" aria-hidden="true"></span>
          <span class="music-item__name">Sabian AAX</span>
        </button>
        <div class="music-item__tooltip" id="music-item-crash-tip">
          <strong>Sabian AAX</strong>
          <span>They open fast, hit hard, and clear out quickly.</span>
        </div>
      </article>
      <article class="music-item">
        <button type="button" class="music-item__button" aria-describedby="music-item-ride-tip">
          <span class="music-item__slot">Ride</span>
          <span class="music-pixel music-pixel--ride" aria-hidden="true"></span>
          <span class="music-item__name">XS20</span>
        </button>
        <div class="music-item__tooltip" id="music-item-ride-tip">
          <strong>Sabian XS20 Ride</strong>
          <span>Stick definition stays clear even when the wash opens up.</span>
        </div>
      </article>
      <article class="music-item">
        <button type="button" class="music-item__button" aria-describedby="music-item-sticks-tip">
          <span class="music-item__slot">Sticks</span>
          <span class="music-pixel music-pixel--sticks" aria-hidden="true"></span>
          <span class="music-item__name">Wood Tip Pair</span>
        </button>
        <div class="music-item__tooltip" id="music-item-sticks-tip">
          <strong>Stick Choice</strong>
          <span>Enough weight for rimshots, enough rebound to stay loose.</span>
        </div>
      </article>
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