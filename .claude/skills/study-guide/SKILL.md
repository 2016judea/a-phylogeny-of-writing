---
name: study-guide
description: Author and publish a new "field" in Aidan's STUDY corner at aidanjude.vercel.app/study — a self-contained ~3-min, argument-driven primer on a non-fiction subject adjacent to his reading but not yet crossed. Use when Aidan wants a new study guide / curated read, or to refresh the study index.
---

# Study Guide — a field in the STUDY corner

The STUDY corner (`aidanjude.vercel.app/study`) is a small, growing set of
**field notes**: original ~3-minute primers, each built around a single
*argument*, on non-fiction ground Aidan's reading hasn't reached yet. It's a
place he returns to for intellectual stimulation — not a blog, not a survey, not
homework.

This is personal-site work, not a Brick & Mortar deliverable. **Do not apply the
B&M sales `copy-voice` here.** The register is literary and essayistic — the
voice of `reading.html` and `something-western.html`, not a mailer.

## What one field is

A hybrid: write the primer yourself, link out **only** when a source genuinely
says it better than you can. Every field has this fixed shape:

1. **The provocation** — one paragraph that makes the question feel alive (rendered as a drop-cap lead).
2. **The argument** — the original primer, 2–3 paragraphs. This is the meat. It must be an *argument*, not a tour of a field.
3. **Where it's contested** — the tension that keeps it stimulating: what's attacked, what's unsettled, what the strong vs. deep version of the claim is. Never let a field read as settled lecture.
4. **Read further** — the canonical work + one strong modern book. **Names and authors only — no hyperlinks.** Aidan does not want reference links on his site; list the works as a plain reading list (`Title — Author (year)`).
5. **On your shelf** — one paragraph tying the subject back to a book Aidan has actually read (or has queued). This is what makes it *his*.

Length target: ~600–750 words of body, a true 3–4 minute read.

## Subject selection

Pick subjects **adjacent to his interests but not yet crossed**. His read shelf
is heavy in: the American canon, Southern Gothic / grit (McCarthy), modernism,
poetry, philosophy (Nietzsche), money/power/polemic (Rand), Beats, dystopia. Thin
or absent: economics-as-a-discipline, history proper, anthropology, hard science.

Rules of thumb:
- **Non-fiction. Essays. Arguments.** Not fiction, not surveys.
- **Discipline mix:** roughly 20% philosophy/philology, the rest spread across
  economics, history, anthropology, physics/space/gravity.
- **Each subject should bridge from something he already loves** (e.g. Hayek
  bridges from Rand; Turner's frontier thesis bridges from McCarthy and his own
  *something-western*; gravity-as-geometry bridges from his Hawking reading).
- Check `data/personal_corpus/themes_by_year.json` and
  `goodreads_reads.json` for what he's read; the reading page's "to-read queue"
  is a good source of adjacency.

## Research (get the facts right)

The prose must be accurate — right dates, right quotes, right attributions. Use the
`gemini-web-search` skill to verify the canonical work, its year, any direct quote
you use, and the strongest modern critique/explainer to name under "Read further."
We cite **works and authors, never URLs**, so research is for correctness and for
picking the right two books — not for harvesting links.

```bash
cd /Users/aidan/Desktop/writing-topology && export $(grep -v ^# .env | xargs)
.venv/bin/python scripts/gemini_search.py "verify: <claim/quote/date> for <subject>; canonical work + strongest modern critique"
```

## Authoring + building

The engine is [scripts/personal_corpus/build_study_guides.py](../../../scripts/personal_corpus/build_study_guides.py).
Content lives in the `GUIDES` list at the top of that file. To add a field:

1. Append one dict to `GUIDES` with keys:
   `n` (next field number), `slug`, `discipline`, `color`, `title`, `dek`,
   `hook` (one line for the index card), `read` (minutes), `provocation` (str),
   `argument` (list of HTML paras), `tension` (list of HTML paras),
   `deeper` (list of `{label, note}` — `label` is `Title — Author (year)`, no URLs), `shelf` (str).
   - Optional `archived` (bool) — set `True` to retire a field. The builder then
     renders it to `study/archive/<slug>.html`, lists it in the index's "Archive"
     section, and leaves a redirect stub at the old `study/<slug>.html` so shared
     links keep working. Retiring/rotating a batch is the **study-review** skill.
   - Inline `<i>`/`<b>` are fine in prose fields. Use real curly quotes.
   - `color` — reuse the site's thread palette so each discipline reads
     consistently: economics `#9c7a3c`, history `#b89a6a`, anthropology
     `#7a9c6b`, physics `#6b8f9c`, philosophy/philology `#8c6b9c`.
2. Build (writes into the site repo; default `~/Desktop/writing-topology`):
   ```bash
   python3 scripts/personal_corpus/build_study_guides.py [SITE_DIR]
   ```
   This regenerates `study.html` (the index) and every `study/<slug>.html`,
   wiring prev/next links automatically.
3. The site nav already carries a `study` link (`dev projects · topology ·
   writing · reading · study · substack`). If the site's nav structure changes,
   update the `nav()` function in the builder to match, and re-add the `study`
   link to any new page.

## Publish

The site (`a-phylogeny-of-writing` repo) deploys to Vercel on `git push` — never
install the Vercel CLI. Confirm with Aidan before pushing (it's outward-facing).

```bash
git -C ~/Desktop/writing-topology add study.html study/ <edited-nav-pages>
git -C ~/Desktop/writing-topology commit -m "study: add field NN — <title>"
git -C ~/Desktop/writing-topology push
```

## Done when

- `study.html` lists every field as a card with the right discipline color + read time.
- Each `study/<slug>.html` renders: drop-cap provocation, argument, "where it's
  contested," a "read further" list (works + authors, no links), and an "on your shelf" tie-back.
- Nav shows `study` on every page; prev/next links work between fields.
- Pushed only after Aidan's go-ahead; live at `aidanjude.vercel.app/study`.

## Gotchas

- **Don't `cd` the shell into the site repo** when working from the bricks repo —
  the bricks hooks resolve via `$CLAUDE_PROJECT_DIR`, but a drifted cwd is still
  confusing. Use absolute paths / `git -C`.
- A **concurrent Claude session** may be editing the same site repo. Re-read a
  page's nav region right before editing it; if an Edit fails with "file modified
  since read," re-read and retry.
- Reuse the discipline color palette so the index stays visually coherent as it grows.