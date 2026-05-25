---
layout: single
title: "Data Engineering"
permalink: /data-engineering/
author_profile: true
---

## Data Engineering Blog

Profesionally I've been working in tech for over 12 years, and as a data engineer for 6 of them. This space is where I talk about data engineering concepts I've found interesting.

{% assign de_posts = site.categories.data-engineering | sort: 'date' | reverse %}

{% if de_posts and de_posts.size > 0 %}
{% for post in de_posts %}
### [{{ post.title }}]({{ post.url | relative_url }})

*{{ post.date | date: "%B %-d, %Y" }}*

{{ post.excerpt | strip_html | truncate: 260 }}

[Read post →]({{ post.url | relative_url }})

---
{% endfor %}
{% else %}
No posts yet. New entries are on the way.
{% endif %}
