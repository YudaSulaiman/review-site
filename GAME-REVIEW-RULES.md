# Game & Visual Novel Review Production Rules

How to turn a written review into (1) an editorial web page and (2) an Instagram
carousel. Distilled from the Clair Obscur: Expedition 33 session (July 2026). When a new
review is requested, follow this drill and only ask about things this file doesn't answer.

**Scope:** applies to **game reviews and visual novel reviews** alike (and any future
interactive-fiction medium). Everything here is medium-agnostic unless marked; VN-specific
adaptations are in §10. The web page is an article of the Parallel Frame site
(`review-site/`) — see §1 and §6 for how the deliverables fit that structure, and
`.claude/CLAUDE.md` (drafting brief) for the front-matter schema and session roles.

---

## 0. Inputs & scope

- The user supplies the **review text** and (usually) a **rating**. Ask for the rating if a
  verdict section exists without one — never invent a score.
- Confirm nothing else up front; sensible defaults below.

## 1. Directory layout — never mix deliverables

Each reviewed title gets ONE **series directory** at `review-site/drafts/<slug>/` (tracked
in git — drafts are committed) holding both deliverables as siblings:

```
review-site/drafts/<slug>/       # series directory — drafting session writes HERE
  index.html                     # art-directed web page, front matter on top (see below)
  assets/css/style.css           # ALL page CSS lives here — see the no-inline-CSS rule
  assets/images/*.jpg            # official images, named by content (hero, gommage, parry…)
  assets/fonts/*.woff2           # local font files
  instagram/                     # social version, inside the same series directory
    build.py                     # generates slides + exports PNGs (single source of truth)
    slides/*.html                # generated, one file per slide
    export/*.png                 # final 1080x1350 deliverables
    caption.txt                  # ready-to-paste post caption + hashtags
    assets/                      # own copy of images/fonts (no ../ up into the web page's)
review-site/src/reviews/<slug>/  # anchor session moves index.html + assets/ here on
                                 # integration; instagram/ stays in the series directory
```

- **HTML and CSS are separate files — never blend them.** The page links
  `assets/css/style.css` (post-integration path `/reviews/<slug>/assets/css/style.css`);
  no `<style>` blocks in `index.html` beyond nothing, no inline `style=""` attributes
  except trivial one-offs. `@font-face` (data URIs allowed) lives in the CSS file. Same
  discipline for slide HTML in `instagram/`.
- Metadata lives in a **sidecar data file** `index.11tydata.json` next to the page — the
  same fields as the front-matter schema in `.claude/CLAUDE.md` (title, subtitle, date,
  medium, score, excerpt, cover, coverAlt, heroImage, featured) plus `"layout": false`.
  Do NOT put YAML front matter inside the HTML: the raw `---` block renders as visible
  text noise whenever the file is opened outside Eleventy. Because
  `templateEngineOverride` cannot be set from a data file, the HTML/CSS must contain no
  `{{` or `{%` sequences — grep for them before integrating.
- All asset references use the post-integration absolute paths
  (`/reviews/<slug>/assets/…`) so integration is a pure move.
- No `../` escapes out of the article folder; deliverables stay self-contained
  (`instagram/` keeps its own asset copies).
- A separate `source.html`/`index.html` split is no longer needed — Eleventy ships the
  folder as-is, so `index.html` **is** the editable source. Inlining assets as data URIs is
  only for an optional Artifact copy (§6).

## 2. Review text is sacred

- Reproduce the user's text **verbatim** on the web page — typos, caps (ZERO PUNISHING
  MECHANICS), quirks and all. Never "fix" their writing.
- Allowed formatting (not text changes): paragraph splits at sentence boundaries, rendering
  run-together numbered lists as `<ol>`, styling a sentence as a set-off quote **in reading
  sequence** (never duplicated as a pull-quote).
- For Instagram: text should be **near-original with light trims** — the user rejects both
  heavy rephrasing and invented lines. Reuse their exact phrases wherever possible.

## 3. Image sourcing — official only, matched to text

- **No AI-generated images.** Source from the game's official press/media page (usually
  `<official-site>/media` or a press kit), Steam CDN, or publisher assets.
- Workflow: scrape the media page for all image URLs → download all at ~960px → build
  contact sheets (Pillow in a scratch venv; no ImageMagick on this Mac) → **visually
  inspect** and map each image to the passage it illustrates. Never pair blindly by filename.
- Every section gets ≥1 image whose content genuinely matches the adjacent text (e.g. the
  parry critique gets the screenshot with Parry/Dodge prompts visible). Never pad with a
  loosely-related image just to fill a slot — a placeholder is better than a wrong image.
- Re-download chosen images at final sizes (hero ~1920w q70, columns ~1300w q74).
- Credit the source once (e.g. in a footer or caption file): "© <Developer> · <Publisher>".

### Placeholders when no relevant image exists (expected for niche games)

- If web research finds no official image that matches a passage, **generate a template
  placeholder image file** and wire it in exactly like a real image — the layout must look
  finished, and the user replaces the file later.
- Make the placeholder in the page's own identity so the design still reads as intentional:
  ink/panel background, the thin gilt frame, a centered ◆ (or the game's motif), a small
  uppercase label `IMAGE PLACEHOLDER`, and one line describing **what should go here**
  (e.g. "combat screenshot showing the parry prompt"). Render it with Pillow or headless
  Chrome at the slot's real dimensions.
- Save it as a normal asset with a self-explanatory name:
  `assets/images/placeholder-<section>.jpg` — the user overwrites that file with their own
  screenshot (keeping the filename) and reruns the build; nothing else needs editing.
- Give the `<img>` an `alt` that describes the intended content, not the placeholder.
- At handoff, list every placeholder and what it's waiting for (a short `PLACEHOLDERS.md`
  in the project root, or a list in the final message), plus the rebuild command.
- Same rule applies to carousel slides: a placeholder file in
  `instagram/assets/images/` (inside the series directory), referenced from `build.py`;
  overwrite + rerun `python3 build.py` regenerates the PNGs.

## 4. Design identity — derived from the game

- Build the identity from the game's own visual language: palette, era, UI motifs,
  typography. For E33 that meant ink/ivory/gilt/crimson, a didone (Playfair Display), petal
  and lozenge (◆) motifs, and the Gommage countdown as section numerals. For another game,
  derive equivalents — the page must feel like it could only exist for that game.
- Pick **one structural motif** from the game's fiction (numerals, sigils, phases) and use it
  as section markers. Structure must encode something true.
- Embed webfonts as **data URIs** (Artifact CSP blocks all external hosts). Google Fonts
  woff2 via curl with a Chrome UA; variable fonts cover multiple weights in one file.
- Include `<meta charset="utf-8">` first — local preview servers send no charset header.

## 5. Web page layout rules (user-validated)

- Centered container ~1140px; consistent horizontal padding `clamp(20px,5vw,48px)`.
- Two-column rows (text ~6.5fr / image ~5.5fr), alternating sides; stack on mobile ≤860px.
- Prose inside image rows: ~680px measure. **Standalone prose blocks (no image beside them)
  fill the container** at ~18px/1.85 — the user dislikes a wide dark gap on the right.
- Image frames: thin gilt border + small padding; no rounded corners unless the game calls
  for it; preserve aspect ratios.
- Hero: full-bleed key art, scrim gradient, kicker with strong text-shadow (bright art kills
  low-contrast labels), title, and a meta line in label/value form:
  `Developer / Publisher: … ◆ Platform(s): … ◆ Release year: … ◆ Hours played: …`.
- **No image captions**, **no full-bleed "interlude" images**, **no footer page** — the user
  removed all three. End the page on the verdict with generous bottom padding on `<main>`.
- **Typography — romanized Japanese**: every Japanese term written in Latin script is
  *italic* — genre/jargon terms
  (*nakige*, *moege*, *seiyuu*), studio or in-world terms. Applies to web page, carousel
  slides, and captions. Proper nouns used as plain English brand names stay roman.
- **"Final Verdict" gets a clear divider**: a full-width horizontal rule in the page's
  identity (e.g. gilt hairline, or the game's motif centered on a rule) separating it from
  the preceding section — the verdict must read as its own closing act, not a continuation.
- Verdict: a single gilt-bordered panel — big rating (e.g. "3 / 5" in the display face) with
  filled/hollow ◆ diamonds on the left, verdict text on the right, hairline divider between;
  stacks rating-first on mobile. Keep the rating stack tight: small grid gap (~2px),
  `line-height:1` and a small negative margin on the score (didone line boxes create fake
  gaps), diamonds with their own top margin.
- Reveal-on-scroll: use a **position-based scroll/interval check**, not IntersectionObserver
  (throttled in some embedded viewers → invisible content). Reveal anything whose top is
  above ~94% of viewport height, including content jumped past. Respect
  `prefers-reduced-motion`.

## 6. Build & publish pipeline (web)

- Edit `index.html` in the article folder directly (full doctype document; Eleventy passes
  it through byte-for-byte thanks to `layout: false` + `templateEngineOverride: false`).
- **Publishing = integration into the site** (anchor session): copy `index.html` +
  `assets/` from the series directory to `src/reviews/<slug>/` (`instagram/` stays in the
  series directory — it is not site content), run the dev server (`npm run dev`, port
  4173 — the `review-site` entry in `StudioProjects/.claude/launch.json`), verify the
  article page AND its card/hero on the homepage and `/reviews/` archive. **Never commit
  or push — the user commits manually after reviewing.** Site deploys are just
  `npm run build` → `_site/`.
- Verify before declaring done: screenshot desktop (~1280) and mobile (375); check console
  for errors.
- **Optional Artifact copy** (only if the user asks for a shareable artifact): build a
  self-contained variant by inlining assets as base64 data URIs (python script; assert no
  leftover `assets/` refs), then strip the doctype/html/head/body wrapper (the Artifact host
  adds its own skeleton). Publish with the Artifact tool; **redeploy to the existing URL
  with the `url` parameter** — a fresh session otherwise mints a duplicate artifact.

## 7. Instagram carousel rules

- Format: **1080×1350** (4:5) PNGs, generated from per-slide HTML by `build.py` and exported
  with headless Chrome (`--headless --screenshot --window-size=1080,1350
  --force-device-scale-factor=1`). Chrome lives at
  `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`.
- Same identity as the web page: plate border (1px gilt, inset 36px), stroked slide numeral,
  small uppercase gilt label, hairline rule, gilt-framed image, serif copy, footer with brand
  line + `NN / TOTAL` index.
- **Cover**: key art full-bleed, kicker `"<Studio> · Game Review"` only (no award/tagline
  decks), title, meta row (platforms · year · hours). Nothing else.
- **No slide titles** — numeral + small label only ("The World", "Gameplay · II").
- Slide structure (~14 slides), written for someone who has never heard of the game:
  1 cover · 2 intro (who made it, setting, release/awards) · 3 world/premise ·
  4 mission/protagonists · 5–6 narrative (structure, then ending) · 7 flavor/tropes ·
  8 art · 9 sound/cinematics · 10–13 gameplay (how it plays → core problem → punishment/
  difficulty → the mechanic that works) · 14 verdict (big rating, centered, auto-margins to
  truly center between top and footer).
- Gameplay deserves **multiple slides** — don't compress the review's main argument.
- Text sits a fixed ~52px under the image (never `margin-top:auto` on copy — the leftover
  space goes between copy and footer). Two short paragraphs max per slide, 29px/1.66 serif.
- `caption.txt`: short summary in the review's voice + "swipe" hook + credit line + hashtags.

## 8. Verification discipline

- Always view what was built: contact-sheet the sourced images, screenshot the rendered page
  at two widths, and Read the exported PNGs before declaring done.
- Screenshots of preview tabs can go black after deep programmatic scrolls — restart the
  preview server/tab rather than fighting it; layout metrics via `preview_eval` are the
  ground truth.

## 9. Iteration etiquette

- Every text/design tweak goes into the **source** (`source.html` / `build.py`), then
  rebuild — never hand-edit generated `index.html` or `export/*.png`.
- Keep artifact URL stable across revisions; label each deploy.
- The user gives fix-lists ("fix these: 1…5") — apply all, verify each visually, and report
  per-item.

## 10. Visual novel adaptations

Everything above applies; adjust only these:

- **Front matter**: `medium: Visual Novel`.
- **Hero/cover meta**: VNs do NOT use the game meta line. Games keep the single
  ◆-separated line from §5:

  > **Developer / Publisher:** Sandfall Team ◆ **Platform(s):** PC/PS5 ◆
  > **Release year:** 2025 ◆ **Hours played:** ~70h

  VNs instead get a **stacked stat block** (VNDB-style label/value rows, one per line) in
  the hero or directly beneath it:

  > **Title:** アンラベル・トリガー · Unravel trigger *(original + romanized/localized,
  > stacked if long)*
  > **Aliases:** アントリ, Antori
  > **Developer / Publisher:** Archive
  > **Release year:** 2024
  > **Language(s):** 🇯🇵 *(flag(s) of available languages; add 🇬🇧 etc. when localized)*
  > **Playtime:** Long (30–50h) *(VNDB length category + hour range)*
  > **Age Ratings:** 18+

  Omit a row only when it's genuinely N/A (e.g. no aliases). `Hours played` (the user's
  own count) may be added as a final row when they provide it — never in place of
  `Playtime`.
- **Package artwork in the hero**: include the VN's package/cover artwork (from its vndb
  entry) somewhere in the hero section as a clean framed image — **no text overlapping or
  overlaid on it**, no caption. Typical placement: beside the stat block, or as a floating
  plate over the key-art backdrop; keep title/kicker text on the backdrop, never on the
  package art itself. Save it as `assets/images/package.jpg`.
- **Primary metadata source: [vndb.org](https://vndb.org)** — browse it first when
  starting any VN review. It is the authority for the stat block above (original/romanized
  titles, aliases, staff/developer, release dates, length category, language releases, age
  rating) and for discovering official sites, store links, and screenshots. Cross-check
  the developer's official site for anything marketing-sensitive.
- **Image sourcing**: official site galleries, store pages (Steam/JAST/MangaGamer/DLsite),
  press kits, and vndb screenshot listings (use them to *find* official images; prefer
  safe-tagged shots and re-source from the official/store page at full quality when
  possible). Prefer key art, sprites-on-background shots, and UI/screenshot stills.
  **CG rules**: only CGs the marketing itself uses; never late-route or ending CGs — treat
  CG choice as a spoiler decision, matching each image to the passage exactly as §3 demands.
  Expect placeholders more often for niche VNs; that's what the §3 placeholder drill is for.
- **Design identity**: derive from the VN's own art — its textbox/UI chrome, palette, and
  era of production are the equivalents of a game's UI motifs. The structural motif (§4) can
  come from its fiction: route names, chapter cards, in-world dates or symbols.
- **Slide structure (§7)**: the ~14-slide skeleton holds, but the 4-slide gameplay block
  becomes the **narrative-craft block**: how it reads (pacing, structure/route system) →
  the core problem → prose/translation quality → the element that works (a twist framed
  spoiler-free, a standout route). Art and sound slides usually deserve more weight than in
  a game review. Spoiler discipline on slides is stricter than on the web page — assume the
  reader hasn't played and never will forgive a spoiled twist.
- **Spoiler policy (web)**: mark late-game/route discussion with an inline warning line in
  the page's own identity before the offending section; never in the excerpt, cover, or
  carousel.
