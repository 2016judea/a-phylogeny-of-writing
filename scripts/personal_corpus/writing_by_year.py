#!/usr/bin/env python3
"""Pull the real writing-production-by-year matrix from the Notion writing_library.

The Dropbox files were undated (2024-12-31 bulk-import sentinel), but Aidan's own
writing_library sync carries real per-piece dates. We read those: per type
(substack / novel / short_story / poetry / journal) per year, deduped by title,
excluding the import sentinel and the high-volume daily "notes". Feeds the
WRITING (production) half of the diverging streamgraph.

    export $(grep -v ^# .env | xargs)
    python3 scripts/personal_corpus/writing_by_year.py
"""
import json
import os
import urllib.request
from collections import defaultdict, Counter

DB = "5d2055b9-74dd-4bf4-bb96-7ce211b898be"
# bottom-half order = center outward; warm→cool to sit under the reading palette
TYPES = [
    ("substack", "Substack essays", "#b5563c"),
    ("novel", "Novel", "#7c4a3a"),
    ("short_story", "Prose & short stories", "#9c7a3c"),
    ("poetry", "Poetry", "#c98a6b"),
    ("journal", "Journals", "#4a6b7c"),
]
SENTINEL = "2024-12-31"


def _q(path, body=None):
    tok = os.environ["NOTION_TOKEN"].strip()
    data = json.dumps(body).encode() if body else None
    r = urllib.request.Request("https://api.notion.com/v1" + path, data=data,
        headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json",
                 "Notion-Version": "2022-06-28"}, method="POST")
    return json.loads(urllib.request.urlopen(r, timeout=30).read())


def main():
    rows, cursor = [], None
    while True:
        b = {"page_size": 100}
        if cursor:
            b["start_cursor"] = cursor
        res = _q(f"/databases/{DB}/query", b)
        for pg in res["results"]:
            pr = pg["properties"]
            src = (pr.get("source", {}).get("select") or {}).get("name")
            d = (pr.get("entry_date", {}).get("date") or {}).get("start")
            title = "".join(t["plain_text"] for t in pr.get("Name", {}).get("title", []))
            rows.append((src, d, title))
        if not res.get("has_more"):
            break
        cursor = res["next_cursor"]

    seen = set()
    counts = {k: Counter() for k, _, _ in TYPES}
    examples = defaultdict(list)
    for src, d, title in rows:
        if src not in counts or not d or d.startswith(SENTINEL):
            continue
        key = (src, title.strip().lower())
        if key in seen:
            continue
        seen.add(key)
        y = int(d[:4])
        counts[src][y] += 1
        if len(examples[src]) < 7:
            examples[src].append(title.strip())

    years = list(range(2014, 2027))  # share the reading axis
    threads = [{
        "name": label, "color": color, "key": key,
        "total": sum(counts[key].values()),
        "counts": [counts[key].get(y, 0) for y in years],
        "examples": examples[key][:6],
    } for key, label, color in TYPES if sum(counts[key].values()) > 0]

    out = {"years": years, "threads": threads,
           "total": sum(t["total"] for t in threads),
           "first_year": min((y for t in TYPES for y in counts[t[0]]), default=None)}
    json.dump(out, open("data/personal_corpus/writing_by_year.json", "w"), indent=2, ensure_ascii=False)
    print(f"writing production: {out['total']} dated pieces, first {out['first_year']}")
    for t in threads:
        spark = "".join("·▁▂▃▅▆▇█"[min(c, 7)] for c in t["counts"])
        print(f"  {t['name']:22} {t['total']:3}  {spark}")


if __name__ == "__main__":
    main()
