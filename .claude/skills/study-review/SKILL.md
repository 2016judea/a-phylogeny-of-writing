---
name: study-review
description: Review and rotate Aidan's STUDY corner at aidanjude.vercel.app/study — capture his feedback on the current fields into an editorial log, archive the fields he's done with (keeping old links alive), and generate a fresh batch steered by what he liked. Use when Aidan wants to give notes/opinions on the study material, retire a batch, or "archive these N and generate N more."
---

# Study Review — feedback, archive, rotate

The STUDY corner is a *rotating* set of field notes (see the **study-guide** skill
for what one field is and the authoring contract). This skill is the lifecycle
around it: take Aidan's reactions to the live fields, retire the batch he's
finished with, and commission the next one shaped by his feedback.

The corner is intellectual stimulation he returns to — treat his notes as
editorial direction, not just praise/complaint. The whole point of rotating is
that the *next* batch is better aimed than the last.

## The three moves

### 1. Capture feedback → `study/NOTES.md`

`study/NOTES.md` is the editorial memory behind the corner (not built into the
site). It has four parts:

- **Selection guidance** — durable principles distilled from his notes (what to
  do more / less of). This is what aims the next batch.
- **Per-subject feedback** — one block per live field; quote the lines that
  landed, note what fell flat and *why*.
- **Archive log** — a dated row per retired field.
- **Batches** — what shipped together and when.

As he transcribes notes, map each to the right field **by content, not by his
numbering** (he numbers his own way). File verbatim-ish; preserve his exact
quoted passages. Patterns worth extracting into Selection guidance, learned so
far:

- He rates **hard science / physics** highest — keep ≥1 per batch, and he likes
  a field that takes a genuine *position* (e.g. he asked an AI to argue its own
  view on quantum gravity), not a neutral survey.
- **Don't restate ground he already owns.** A Nietzsche/philology field fell flat
  because he's read all of Nietzsche. The ~20% philosophy slot must reach for the
  genuinely unfamiliar (check the read shelf / to-read queue first).
- He responds to **deep-origin** framings (the American spirit; the affluent
  society; what we gave up to be governed) and to the idea that **markets are
  action/process, not product**.

### 2. Archive the old batch (keep links alive)

Mechanics live in [`build_study_guides.py`](../../../scripts/personal_corpus/build_study_guides.py):

- Set `"archived": True` on each retiring guide dict (leave its `n` as-is — the
  numbering is continuous across batches, telling the true story of a growing plan).
- The builder then:
  - renders archived fields to `study/archive/<slug>.html` (prev/next chain
    *within* the archive),
  - lists them in a navigable **"The archive"** section on `study.html`,
  - and **leaves a redirect stub at the old `study/<slug>.html`** (canonical +
    meta-refresh + JS `location.replace`) so any link already shared externally
    keeps working. **This matters — Aidan shares field URLs with people (e.g. his
    dad). Never let an old `/study/<slug>.html` 404.**

### 3. Generate the replacements

Author the new batch with the **study-guide** skill's contract (provocation →
argument → where it's contested → read further → on your shelf; ~600–750 words;
works + authors, never URLs; reuse the discipline color palette). Steer subjects
from the Selection guidance in `NOTES.md`. Number the new fields continuing from
the highest `n` (don't renumber the archive). Good batches **bridge from fields
he liked** and can quietly **rhyme with each other** (e.g. a relational-physics
field and a Nāgārjuna emptiness field referencing the same idea from two ends).

Verify facts before writing — exact titles, years, and any quoted line. (The
`gemini_search.py` helper referenced by study-guide lives in the *bricks* repo,
not here; if it's unavailable, use web search.)

## Build + publish

```bash
python3 scripts/personal_corpus/build_study_guides.py
```

Sanity-check the output: active grid shows the new batch, "The archive" section
shows the retired one, each old `study/<slug>.html` is now a redirect stub, and
prev/next chains stay within their own group. Then commit `study.html`,
`study/`, `scripts/personal_corpus/build_study_guides.py`, and `study/NOTES.md`,
and push (Vercel deploys on push). Per Aidan's standing preference for this repo,
push automatically; no preview needed.

## Done when

- `study/NOTES.md` records the feedback, refreshed selection guidance, archive
  rows, and the new batch.
- The retired fields render under `/study/archive/`, are listed in the archive
  section, and their old URLs redirect there.
- The new batch is live, argument-driven, fact-checked, and aimed by his notes.

## References

**Uses:** [[site-page]]
**See also:** [[study-guide]]
