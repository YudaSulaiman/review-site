# Parallel Frame

Personal review journal — games, visual novels, film. Built with [Eleventy](https://www.11ty.dev/).

## Commands

```bash
npm install        # once
npm run dev        # dev server at http://localhost:4173, rebuilds on save
npm run build      # static output to _site/ (deploy that folder anywhere)
```

## Publishing an article

**Standard article (Markdown, house template):** add one file —

- Review → `src/reviews/my-review.md`
- Essay → `src/essays/my-essay.md`

Front matter drives everything:

```yaml
---
title: "Game Title"
date: 2026-08-01
medium: Game            # Game | Visual Novel | Film (reviews only)
score: "8 / 10"         # reviews only; renders the verdict box
verdict: "One-line justification."
excerpt: "Card blurb on the homepage and archive."
cover: /reviews/my-review/assets/cover.jpg   # optional
featured: true          # optional: promotes to homepage hero
heroImage: /path.jpg    # optional: wide image for the hero (falls back to cover)
---
Body in Markdown…
```

Homepage grids, `/reviews/` and `/essays/` archives all update automatically.

**Art-directed article (own theme, like Clair Obscur):** create a folder
`src/reviews/my-title/` with its own `index.html` (any design, self-contained)
plus an `assets/` folder. Prepend the same front matter block, plus:

```yaml
layout: false                   # don't wrap in the house template
templateEngineOverride: false   # ship the HTML byte-for-byte
```

It gets a URL, cards, and archive listing like any other article, but keeps
its bespoke design inside. See `src/reviews/clair-obscur-expedition-33/`.

## Structure

```
src/
  _layouts/    base.njk (site chrome), article.njk (house article template)
  _includes/   card.njk (article card macro)
  assets/      site-wide CSS
  index.njk    homepage (featured hero + latest grids)
  about.md
  reviews/     reviews.json (shared defaults) + one file/folder per review
  essays/      essays.json + one file per essay
```
