---
title: "Puck Edge: Fantasy Hockey Lineup Optimizer"
description: "A commercial-quality web app that analyzes your fantasy hockey roster and recommends the optimal weekly move — leveraging off-night schedule advantages, waiver wire intelligence, and real NHL schedule data."
layout: project
image: "/assets/images/projects/puck-edge-lineup-lab.svg"
link: "https://puck-edge.vercel.app"
github: "https://github.com/jas-m-evans/puck-edge"
---

## The Problem: Information Asymmetry in Fantasy Hockey

Fantasy hockey rewards managers who understand NHL scheduling better than their opponents. Every week, two to three nights have fewer than ten teams playing — "off-nights" where restful goalies start and rested skaters produce at elevated rates. Managers who deliberately stream roster spots on these nights gain a measurable statistical edge.

Most fantasy tools tell you a player's stats. None tell you *when* to play them this specific week.

Puck Edge bridges that gap: paste your Yahoo, ESPN, or Fantrax roster, and get an actionable recommendation — hold, start, bench, or stream — with explicit reasoning tied to the upcoming schedule.

## Architecture

The project is built as a Next.js 16 application (App Router, TypeScript strict mode) with a clean domain-driven architecture separating scheduling logic from UI concerns.

### Schedule Analysis Pipeline

The core analysis runs in five stages:

1. **Parse** — A regex + Levenshtein fuzzy-matching parser converts raw roster paste text into structured player records, tolerating common name variations and typos.

2. **Schedule fetch** — An `IScheduleProvider` abstraction fetches the week's game data, with both a live NHL API implementation calling `api-web.nhle.com/v1` and a deterministic mock for testing.

3. **Off-night detection** — Nights where fewer than 10 of 32 NHL teams are playing are flagged. Streaming on these nights carries a 1.25× score multiplier in the waiver ranker.

4. **Waiver ranking** — Free agents are scored using a formula that weights games played per window, off-night timing, player tier, and injury status. This surfaces pickups that are genuinely worth the roster churn.

5. **Recommendation generation** — A single `hold | start | bench | stream | drop` action is generated with confidence level, human-readable reasoning, and alternative options.

### Technical Highlights

- **Zero-dependency schedule logic** — The domain layer (`src/domain/`) has no runtime dependencies. Pure TypeScript functions that are easy to test and extend.
- **Optimistic UI state machine** — The analyzer page uses an explicit `idle → loading → done | error` state machine with no external state library.
- **Graceful degradation** — Upstash Redis caching is fully optional; the app falls back to uncached NHL API calls when credentials are absent.
- **24 unit tests** — Vitest covers the parser, schedule engine, and analysis orchestrator with focused, fast tests.

## Engineering Decisions

**Why Next.js App Router over a separate frontend/backend?** For a solo-built MVP, colocating the API routes with the rendering layer eliminates deployment complexity. The data layer is designed as pure functions (`IScheduleProvider`) that could be extracted to a standalone service if traffic warranted it.

**Why fastest-levenshtein over a fuzzy matching library?** Fantasy hockey roster paste text is predictably structured. The only fuzzy matching needed is player name normalization, where Levenshtein distance on a bounded player database is both faster and more deterministic than general-purpose fuzzy matching.

**Why Tailwind CSS v4?** The v4 CSS-based config (`@import "tailwindcss"` + `@theme` blocks) eliminates the need for a separate config file and makes the design system easier to inspect in DevTools.

## Stack

| Layer | Technology |
|-------|-----------|
| Framework | Next.js 16, TypeScript strict |
| Styling | Tailwind CSS v4 |
| Validation | Zod + @t3-oss/env-nextjs |
| Fuzzy matching | fastest-levenshtein |
| Cache | Upstash Redis (optional) |
| Tests | Vitest 4 + Playwright |
| Deploy | Vercel |
| Data | NHL public API (`api-web.nhle.com/v1`) |
