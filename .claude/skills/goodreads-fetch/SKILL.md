---
name: goodreads-fetch
description: Pull Aidan's Goodreads "read" shelf (titles, authors, real read-dates) via the public RSS feed — no login or scraping. Use when you need his reading history, per-year book lists, or to refresh the reading data.
---

# Goodreads Fetch

Goodreads blocks unauthenticated HTML scraping of review lists (it redirects any
`/review/list/...` request to a sign-in page). The **public per-shelf RSS feed**
is NOT behind that wall and carries the real `user_read_at` dates, so it's the
reliable way in — no login, no Selenium, no Outscraper.

## Run it

```bash
cd /Users/aidan/Desktop/writing-topology
python3 scripts/personal_corpus/goodreads_fetch.py
# → data/personal_corpus/goodreads_reads.json  (+ per-year counts printed)
```

User id is `86865482` (Aidan Jude); override with `--user-id`. The feed paginates
100/page; the script walks all pages.

## What you get

A JSON list of `{title, author, read_date, read_year, date_added}`. Only ~310 of
the ~480 shelved books carry a real read-date — those are the timeline. The rest
are undated shelf backlog (bulk-added, mostly stamped 2018); don't treat their
dates as real. The script reports both counts.

## Notes / gotchas (learned the hard way — don't repeat)

- **No read-count field → CANNOT detect re-reads.** One `<item>` per book. Never
  claim "0 re-reads" / "never re-reads" from this feed; that's a method artifact
  (Aidan HAS re-read books). True counts need the Goodreads CSV export.
- **Logging only effectively starts ~2018.** Aidan wasn't on Goodreads 2014–2017,
  so the 2014→2018 "gap" is a tracking gap, NOT a reading hiatus. Don't read
  meaning into pre-2018 sparseness.
- Earlier-year reads often have only a year in `user_read_at` → date lands on
  `YYYY-01-01` (inflates January in month histograms). `read_year` is trustworthy.
- The feed DOES carry `book_published` + `num_pages` — use them (~92k pages read;
  median pub-year ~1964 — he reads the dead).
- To push the result into the Notion `reading_library` DB, see [[corpus-refresh]].
- For the trend/synthesis read of this data, see [[intellectual-history-analysis]].
