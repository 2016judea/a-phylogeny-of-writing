#!/usr/bin/env python3
"""Export the FULL Substack history (every dated essay since 2023) from the Notion
writing_library — not just the ~23 currently-public posts the archive API returns.

The public archive API (see substack_export.py) only lists currently-public posts.
The complete run lives in the Notion writing_library (source = "substack", 66 rows
back to 2023-01), each carrying title, entry_date, source_url, and a `content`
body proxy. Where a row matches a currently-public post we also have a precise
wordcount + subtitle from substack_posts.json, so we merge those in.

    export $(grep -v ^# .env | xargs)
    python3 scripts/personal_corpus/substack_all_export.py
    # -> data/personal_corpus/substack_all.json  (oldest -> newest)
"""
import json
import os
import re
import urllib.request

DB = "5d2055b9-74dd-4bf4-bb96-7ce211b898be"
OUT = "data/personal_corpus/substack_all.json"
PUBLIC = "data/personal_corpus/substack_posts.json"


def _q(path, body=None):
    tok = os.environ["NOTION_TOKEN"].strip()
    data = json.dumps(body).encode() if body else None
    r = urllib.request.Request("https://api.notion.com/v1" + path, data=data,
        headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json",
                 "Notion-Version": "2022-06-28"}, method="POST")
    return json.loads(urllib.request.urlopen(r, timeout=30).read())


def _rt(prop):
    if prop.get("type") == "rich_text":
        return "".join(x["plain_text"] for x in prop["rich_text"])
    return ""


def main():
    # currently-public posts -> precise subtitle + wordcount, keyed by url
    pub = {}
    if os.path.exists(PUBLIC):
        for p in json.load(open(PUBLIC)):
            pub[p["url"].rstrip("/")] = p

    # writing_library carries duplicate rows for recent posts (Aidan's own sync +
    # notion_push.py). Dedupe by url (fall back to title|date), keeping the row
    # with the richest content / a precise wordcount.
    by_key, cursor = {}, None
    while True:
        b = {"page_size": 100}
        if cursor:
            b["start_cursor"] = cursor
        res = _q(f"/databases/{DB}/query", b)
        for pg in res["results"]:
            pr = pg["properties"]
            if (pr.get("source", {}).get("select") or {}).get("name") != "substack":
                continue
            date = (pr.get("entry_date", {}).get("date") or {}).get("start")
            title = "".join(t["plain_text"] for t in pr.get("Name", {}).get("title", []))
            url = (pr.get("source_url", {}) or {}).get("url") or ""
            content = re.sub(r"\s+", " ", _rt(pr.get("content", {}))).strip()
            if not date:
                continue
            p = pub.get(url.rstrip("/"), {})
            row = {
                "title": title.strip(),
                "subtitle": (p.get("subtitle") or "").strip(),
                "date": date,
                "url": url,
                "public": url.rstrip("/") in pub,
                "wordcount": p.get("wordcount") or len(content.split()),
                "excerpt": content[:600],
            }
            key = url.rstrip("/") or f"{title.strip().lower()}|{date}"
            prev = by_key.get(key)
            if prev is None or len(row["excerpt"]) > len(prev["excerpt"]):
                by_key[key] = row

    rows = sorted(by_key.values(), key=lambda r: r["date"])
    json.dump(rows, open(OUT, "w"), indent=2, ensure_ascii=False)
    pubn = sum(1 for r in rows if r["public"])
    print(f"{OUT}: {len(rows)} essays  {rows[0]['date']} -> {rows[-1]['date']}  "
          f"({pubn} public, {len(rows) - pubn} archived)")


if __name__ == "__main__":
    main()
