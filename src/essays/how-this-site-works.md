---
title: How this site works (sample article)
date: 2026-07-10
excerpt: A living demo of the Markdown article workflow — copy this file to start a new piece.
---

This page is a normal Markdown file at `src/essays/how-this-site-works.md`. Publishing a new essay is: copy this file, rename it, edit the front matter, write. The homepage, the essays archive, and the card grids all update automatically on the next build.

## The front matter

Every article declares its metadata at the top of the file:

- `title` — shown on cards and the article page
- `date` — controls ordering everywhere
- `excerpt` — the card blurb
- `cover` / `coverAlt` — card and page image (optional; cards render a neutral placeholder without one)
- `featured: true` — promotes it to the homepage hero
- `score` and `verdict` — reviews only; adds the verdict box below the prose

Reviews additionally set `medium: Game`, `Visual Novel`, or `Film` — the tag on the card.

> Pull quotes are plain Markdown blockquotes, styled by the house template.

## Two kinds of article

Markdown files like this one get the neutral house template. But a fully art-directed page — like the Clair Obscur review — can be dropped in as its own `index.html` with its own CSS, and the site treats it as a first-class article: it appears on cards, in archives, and can be featured, while keeping its bespoke design inside.
