#!/usr/bin/env python3
"""Pull a Goodreads "read" shelf via the PUBLIC RSS feed — no login required.

Goodreads blocks unauthenticated HTML scraping of review lists (it redirects to
sign-in), but the per-shelf RSS feed is public and carries the real read dates.

    https://www.goodreads.com/review/list_rss/<USER_ID>?shelf=read

Usage:
    python3 scripts/personal_corpus/goodreads_fetch.py [--user-id 86865482] \
        [--out data/personal_corpus/goodreads_reads.json]

Writes a JSON list of {title, author, read_date, read_year, date_added}.
Only books with a real user_read_at date are counted toward the per-year arc;
the rest are undated shelf backlog (reported separately).
"""
import argparse
import html
import json
import re
import sys
import urllib.request

DEFAULT_USER = "86865482"  # Aidan Jude
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36")


def _year(s: str):
    m = re.search(r"\b(20\d\d)\b", s or "")
    return int(m.group(1)) if m else None


def _tag(block: str, tag: str) -> str:
    m = re.search(rf"<{tag}>(.*?)</{tag}>", block, re.S)
    if not m:
        m = re.search(rf"<{tag}><!\[CDATA\[(.*?)\]\]></{tag}>", block, re.S)
    if not m:
        return ""
    val = re.sub(r"<!\[CDATA\[|\]\]>", "", m.group(1)).strip()
    return html.unescape(val)


def fetch(user_id: str = DEFAULT_USER, max_pages: int = 12):
    base = (f"https://www.goodreads.com/review/list_rss/{user_id}"
            "?shelf=read&sort=date_read&order=d&per_page=100&page=")
    items = []
    for page in range(1, max_pages + 1):
        req = urllib.request.Request(base + str(page), headers={"User-Agent": UA})
        xml = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
        blocks = re.findall(r"<item>(.*?)</item>", xml, re.S)
        if not blocks:
            break
        for b in blocks:
            read = _tag(b, "user_read_at")
            added = _tag(b, "user_date_added")
            pub = _tag(b, "book_published")
            pages = _tag(b, "num_pages")
            items.append({
                "title": re.sub(r"\s*\(.*?\)\s*$", "", _tag(b, "title")).strip(),
                "author": _tag(b, "author_name").strip(),
                "read_date": read,
                "read_year": _year(read),
                "date_added": added,
                "published": int(pub) if pub.lstrip("-").isdigit() else None,
                "pages": int(pages) if pages.isdigit() else None,
            })
        if len(blocks) < 100:
            break
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user-id", default=DEFAULT_USER)
    ap.add_argument("--out", default="data/personal_corpus/goodreads_reads.json")
    args = ap.parse_args()

    items = fetch(args.user_id)
    dated = [i for i in items if i["read_year"]]
    with open(args.out, "w") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

    from collections import Counter
    by_year = Counter(i["read_year"] for i in dated)
    print(f"Wrote {len(items)} shelf items ({len(dated)} with real read-dates) -> {args.out}")
    for y in sorted(by_year):
        print(f"  {y}: {by_year[y]}")
    print(f"  undated backlog: {len(items) - len(dated)}")


if __name__ == "__main__":
    main()
