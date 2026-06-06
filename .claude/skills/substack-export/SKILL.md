---
name: substack-export
description: Export every post (titles, dates, word counts, full body text) from Aidan's public Substack (aidanjude.substack.com) via its archive API — no login. Use to pull or refresh the newsletter.
---

# Substack Export

Substack exposes a **public JSON archive API** per publication. No auth, no
scraping HTML.

```
https://<sub>.substack.com/api/v1/archive?sort=new&limit=50&offset=N   # metadata, paginated
https://<sub>.substack.com/api/v1/posts/<slug>                          # full body_html
```

## Run it

```bash
cd /Users/aidan/Desktop/writing-topology
python3 scripts/personal_corpus/substack_export.py
# → data/personal_corpus/substack_posts.json  (with stripped plain-text bodies)
```

Default publication is `aidanjude`; override with `--sub`.

## What you get

`{title, subtitle, date, slug, wordcount, id, url, audience, body}` per post,
sorted oldest→newest.

**Important — the public archive API only returns currently-public posts.** As of
2026-06 that's ~23 (back to Aug 2025). The newsletter actually **began Jan 2023**
and runs ~53 unique posts; the earlier ones were archived/deleted from public view
but were captured by Aidan's own sync and live in the Notion `writing_library`
(source = `substack`, dates 2023-01→). For the true start date / full history,
read writing_library, not this feed.

## Full history (all 53, since 2023)

To get the **complete** run — not just the public 23 — pull from the Notion
`writing_library` instead. This is what the public essays archive page is built
from:

```bash
export $(grep -v ^# .env | xargs)               # needs NOTION_TOKEN
python3 scripts/personal_corpus/substack_all_export.py
# → data/personal_corpus/substack_all.json  (53 deduped: 23 public + 30 archived)
```

Each row: `{title, subtitle, date, url, public, wordcount, excerpt}`. It dedupes
the duplicate writing_library rows (Aidan's sync + notion_push both push the
recent posts) by url, prefers the public copy, and enriches public posts with the
precise subtitle/wordcount from `substack_posts.json`. The `public` flag marks
which still resolve on Substack vs. which are archived out of public view. To
render the grouped archive page from this, see [[corpus-refresh]] Step 3
(`build_essays_page.py` → `essays.html`).

The newsletter is a monthly dispatch (3.5 years and counting) that braids three voices: literature
(epigraphs from McCarthy / Rand / the Greeks), the founder (AI, markets, Claude
Code), and the photographer (physical-media journals). Word counts trend *down*
over time — long essays → terse aphorisms.

## Notes

- To load posts into the Notion `writing_library` DB (source = `substack`), see
  [[corpus-refresh]].
- Related: [[goodreads-fetch]], [[intellectual-history-analysis]].