---
name: corpus-refresh
description: Re-pull Aidan's personal corpus (Goodreads reads, Substack posts, Dropbox /Writing) and upsert it into the Notion databases so Claude (web/mobile/desktop) always has current data. Use to refresh the reading/writing intelligence store.
---

# Corpus Refresh

Keeps the personal-corpus store current end to end:

```
Goodreads RSS ─┐
Substack API  ─┼─▶  data/personal_corpus/*.json  ─▶  Notion (reading_library + writing_library)
Dropbox /Writing┘                                       ▲ queryable from Claude web/mobile
```

The Notion DBs are the **delivery layer** — they're what Claude on the phone
(via the Notion connector) actually reads. The JSON files in
`data/personal_corpus/` are the local source of truth and a backup.

## Step 1 — pull the sources

```bash
cd /Users/aidan/Desktop/writing-topology
export $(grep -v ^# .env | xargs)
python3 scripts/personal_corpus/goodreads_fetch.py        # → goodreads_reads.json
python3 scripts/personal_corpus/substack_export.py        # → substack_posts.json
python3 scripts/personal_corpus/dropbox_writing_pull.py   # → writing_corpus.json (needs DROPBOX_* in .env; see dropbox-token)
```

Dropbox files are **online-only placeholders** locally (0 bytes), so always pull
content + real `client_modified` dates through the API — never read them off disk.
See [[goodreads-fetch]], [[substack-export]], and the dropbox-token skill.

## Step 2 — upsert into Notion

Two ways, pick one:

**A. Programmatic (preferred, idempotent).** Needs a Notion **internal
integration** token in `.env` as `NOTION_TOKEN`, with the integration shared into
both DBs (open each DB → ⋯ → Connections → add it). Then:

```bash
python3 scripts/personal_corpus/notion_push.py --all   # dedups; only adds what's new
```

**B. Via the Notion MCP (no token setup).** Read the JSON files and create pages
with `notion-create-pages`. The live targets:
- `reading_library` data source — `2fa6f097-cf64-48e6-acae-b59ec661f52e`
  (props: Name, author, read_year, source=`goodreads`, shelf=`read`, `date:read_date:start`)
- `writing_library` data source — `9bc53c27-ec17-43f7-93fb-41430532add7`
  (props: Name, source∈{substack,poetry,short_story,journal,novel,notes},
  `date:entry_date:start`, source_url, file_path; put the body in page content)

Only push rows whose dedup key isn't already present (reading = title|read_date;
writing = source_url or file_path) so you don't duplicate.

## Databases (created 2026-06-04, under the "Journal Index" page)

- **reading_library** — `c06f03ec-b284-43cc-807a-6dc775c23b64` — 310 dated reads (2014→).
- **writing_library** — `5d2055b9-74dd-4bf4-bb96-7ce211b898be` — journals + substack +
  poetry + prose + novel index. Pre-existed; we add the substack/Dropbox rows to it.

## Step 3 — rebuild the public 3D topography pages (optional)

The Vercel site `a-phylogeny-of-writing.vercel.app` (repo
`2016judea/a-phylogeny-of-writing`) has TWO data pages, each a single-range
Three.js ridgeline terrain:
- **/reading.html** — research & interests: 12 reading themes + reading "by the
  numbers" + the to-read queue.
- **/work.html** — creative ideation: 5 writing forms + prose-fingerprint stats.

Regenerate + redeploy after a refresh:

```bash
python3 scripts/personal_corpus/classify_themes.py      # reading themes_by_year.json (+ movement, marquee author)
python3 scripts/personal_corpus/writing_by_year.py      # writing_by_year.json (needs NOTION_TOKEN)
python3 scripts/personal_corpus/build_topography.py /path/to/phylo    # writes BOTH reading.html + work.html
# git -C /path/to/phylo commit -am "refresh topography" && git push   → Vercel auto-deploys
```

## Step 4 — rebuild the essays archive (after new Substack posts)

`/essays.html` is the full Substack archive (every dispatch since 2023), grouped
into three voices. It builds straight from the repo (run from the site root):

```bash
export $(grep -v ^# .env | xargs)                          # NOTION_TOKEN
python3 scripts/personal_corpus/substack_all_export.py     # → substack_all.json (all 53)
python3 scripts/personal_corpus/build_essays_page.py       # → essays.html
# git commit -am "essays: refresh archive" && git push     → Vercel auto-deploys
```

`build_essays_page.py` holds a manual `slug → voice` map (the 2023–24 issues are
multi-topic, so each is filed by dominant voice); **new posts not in the map fall
back to keyword scoring** — add a slug to `THEME` to override. See
[[substack-export]] for the export details.

## Step 5 — rebuild the idea topology (after new posts/poems)

`/topology.html` ("a phylogeny of writing") is the drifting canopy: every Substack
essay + the poems, clustered into six idea-themes. `build_topology_page.py` is an
**in-place transform** — it reads topology.html, swaps the `CORPUS` + `CROSS_LINKS`
arrays (stats/legend recompute themselves) and freshens the colophon, leaving the
canvas engine + the six `THEMES` untouched:

```bash
python3 scripts/personal_corpus/substack_all_export.py   # if essays changed
python3 scripts/personal_corpus/build_topology_page.py    # → topology.html (74 nodes)
```

Essays carry real dates; **poems have none** (writing_corpus dates are the import
sentinel) so they render undated. Theme assignment is a manual `ESSAY_THEME` /
`POEM_THEME` map (slugs/titles → one of reaching·mind·inner·time·place·examined);
unmapped essays fall back to `examined`. Cross-links are derived from shared
vocabulary (degree-capped at 2, ≤24 total).

The "by the numbers" stats are hand-curated in `build_topography.py` from
`analyze_corpus.py` output — re-run that and update the stat cards if the data
shifts materially. Writing dates come from `writing_library` (real per-piece
dates; the Dropbox 2024-12-31 import sentinel and the high-volume `notes` source
are excluded). To-read shelf: `goodreads_fetch.py` with `shelf=to-read`.

**Goodreads gotchas** (see [[reference-corpus-fetch-methods]]): the RSS feed has
no read-count (can't detect re-reads) and logging only starts ~2018 — never
narrate the 2014→2018 gap as a reading hiatus.

## Done when

`reading_library` ≈ Goodreads dated-read count, `writing_library` contains the
latest Substack post and any new Dropbox writing. Spot-check the newest entries
in Notion. For the analysis pass over this data, see [[intellectual-history-analysis]].

## References

**Uses:** [[goodreads-fetch]], [[substack-export]]
**See also:** [[intellectual-history-analysis]]
