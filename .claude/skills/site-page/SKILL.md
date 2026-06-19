---
name: site-page
description: Add or update a top-level page on Aidan's personal site (aidanjude.vercel.app) — the static HTML in the writing-topology repo. Handles the shared page template, the sitewide nav (which lives in many files, including a hidden drawer nav), and the Open Graph link-preview card. Use when adding a new page (e.g. a "research" or "talks" page), renaming/reordering nav, or refreshing a page's OG image.
---

# Site page — add or update a page on aidanjude.vercel.app

The site is **hand-authored static HTML** in the `writing-topology` repo (no
framework, no build step at deploy — Vercel serves the files as-is). Each page is
a self-contained `.html` file at the repo root with inline `<style>`. Pushing to
`main` deploys.

This is personal-site work in a literary/editorial register — **not** a Brick &
Mortar deliverable. Match the voice of `reading.html` / `research.html`, never a
sales mailer.

## The three things a new page needs

1. The page file itself (`<slug>.html`), matching the shared template.
2. The **nav link added to every page** (see the footgun list below).
3. An **OG card** at `og/<slug>.png` so link previews aren't broken.

Do all three, then preview, then commit + push (Aidan wants every change pushed —
see the `always-push-to-git` memory).

## 1 · Page template

Copy a recent sibling page (`research.html` is the cleanest reference) and keep
these invariants:

- **Fonts:** EB Garamond (serif body, italic headings) + Geist Mono (eyebrows /
  nav / meta). Same Google Fonts `<link>` as every page.
- **Theme tokens** — light + dark, in `:root`:
  ```
  --bg:#f7f3ec --bg2:#efe9dd --ink:#1c1814 --ink2:#544e44 --faint:#8b8478
  --rule:rgba(60,50,40,.16) --accent:#7c4a3a
  dark: --bg:#15120f --bg2:#1d1916 --ink:#e9e3d5 --ink2:#b3aa9a --faint:#7d766a
        --rule:rgba(230,220,200,.16) --accent:#c98a6b
  ```
  The accent may shift per page (projects/topology warm `#7c4a3a`; research cool
  `#3a5a7c` / dark `#7ea6c9`). Pick one that suits the page's hero art.
- **Structure:** `.page` (max-width 60rem) › `.site-header` (`.brand` + `.nav`) ›
  a hero (full-bleed `*-band` with a framed `.plate` image is the house style) ›
  content › `.foot`.
- **Head meta:** title `Aidan Jude — <Page>`, description, the full OG +
  Twitter-card block pointing at `https://aidanjude.vercel.app/og/<slug>.png`
  (1200×630), and `theme-color`.
- Images use **root-absolute paths** (`/img/...`, `/og/...`) — so file:// preview
  is broken; serve over HTTP (see §4).

## 2 · Nav — update EVERY copy (the footgun)

The nav is duplicated in each page's HTML. When adding/removing/reordering a link
you must edit **all** of these — miss one and that page's nav goes stale:

- `index.html` — the dark cover page; its own `<nav>` (different styling).
- `projects.html`, `research.html`, `topology.html`, `reading.html`,
  `study.html` — the standard `.nav` in `.site-header`.
- `something-western.html` — has **two** navs: the cover `.cover-nav` **and** an
  inline reading-drawer nav (`<div class="dsite">…`) far down the file.
- `scripts/personal_corpus/build_projects_page.py` — the projects page is
  generated; its `TEMPLATE` contains the nav too. Update it or a regen reverts you.

Current canonical order & hrefs:
```
dev projects   /projects.html
research       /research.html
topology       /topology.html
novel          /something-western.html
reading        /reading.html
study          /study.html
essays         /essays.html
35mm photography  https://www.instagram.com/_aidan_jude/  (target=_blank rel=noopener)
```
Rules: the **current page's** link gets `class="active"`; preserve each file's
existing indentation; the Instagram link keeps `target/rel`. After editing, sanity
check: `grep -l '/<slug>.html' *.html | wc -l` should equal the page count.

## 3 · OG link-preview card

Cards are generated, not hand-drawn:

1. Add an entry to `CARDS` in `scripts/personal_corpus/build_og_cards.py`:
   ```python
   "<slug>": dict(accent="#3a5a7c", tsize=84, kicker="Aidan Jude · <Section>",
       title="<Headline>",
       sub="<one–two sentence subhead>",
       fl="<bottom-left, e.g. github.com/2016judea>", fr="<bottom-right tag>"),
   ```
   `tsize` is the title font px — shrink it for longer titles (80–104 typical).
2. Render the card HTML: `python3 scripts/personal_corpus/build_og_cards.py`
   (writes `/tmp/og_cards/<slug>.html`; the GLEAN step may error — ignore it).
3. Screenshot to a real PNG at 1200×630 with headless Chrome:
   ```bash
   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
     --headless --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
     --window-size=1200,630 \
     --screenshot=og/<slug>.png /tmp/og_cards/<slug>.html
   ```
4. Open `og/<slug>.png` to confirm fonts loaded and text didn't clip.

## 4 · Preview before committing

Pages use root-absolute asset paths, so preview over a local server:
```bash
python3 -m http.server 8899 >/dev/null 2>&1 &   # from repo root
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless \
  --disable-gpu --hide-scrollbars --window-size=1100,2200 \
  --screenshot=/tmp/preview.png "http://localhost:8899/<slug>.html"
kill %1
```
Check the hero image resolves, the grid/sections look right, and the nav shows the
new link. Headless Chrome renders the **dark** theme by default — eyeball light
mode too if the design is sensitive to it.

## 5 · Ship

`git add -A && commit && push origin main`. Vercel auto-deploys `main`. Verify the
live page and its `og:image` after deploy.

## House patterns worth reusing

- **Hero = framed plate of real art.** projects.html uses the *Ubik* cover;
  research.html uses the actual `literature-mutations` network graph
  (`/img/literature-network.png`). Prefer a genuine artifact over decoration.
- **Card grid** (`.grid` of `.card`) with `.card-meta` rows: language dots
  (`<i style="background:COLOR">` + name), optional `★ N`, and a `.yr`. Language
  colors: Python `#3572A5`, Shell `#111111`, HTML `#e34c26`, CSS `#563d7c`,
  TypeScript `#a3e635`, JavaScript `#f1e05a`.
- The projects page is **generator-driven** (`build_projects_page.py`, data in
  `PROJECTS`) and reproduces `projects.html` byte-for-byte — edit the data + regen,
  don't hand-edit that one page.

## References

**See also:** [[glean-issue]]
**Used by:** [[study-guide]], [[study-review]]
