#!/usr/bin/env python3
"""Export every post from a public Substack via its archive API — no login.

    https://<sub>.substack.com/api/v1/archive   (metadata, paginated)
    https://<sub>.substack.com/api/v1/posts/<slug>  (full body_html)

Usage:
    python3 scripts/personal_corpus/substack_export.py \
        [--sub aidanjude] [--out data/personal_corpus/substack_posts.json] [--bodies]

With --bodies it also fetches and strips each post's HTML to plain text.
"""
import argparse
import html
import json
import re
import urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36")


def _get(url: str) -> bytes:
    return urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30).read()


def _strip(h: str) -> str:
    h = re.sub(r"<[^>]+>", " ", h or "")
    return re.sub(r"\s+", " ", html.unescape(h)).strip()


def export(sub: str = "aidanjude", bodies: bool = True):
    base = f"https://{sub}.substack.com/api/v1"
    posts, off = [], 0
    while True:
        chunk = json.loads(_get(f"{base}/archive?sort=new&limit=50&offset={off}"))
        if not chunk:
            break
        posts += chunk
        off += len(chunk)
        if len(chunk) < 50:
            break
    rows = []
    for p in posts:
        row = {
            "title": p.get("title"),
            "subtitle": p.get("subtitle"),
            "date": (p.get("post_date") or "")[:10],
            "slug": p.get("slug"),
            "wordcount": p.get("wordcount"),
            "id": p.get("id"),
            "url": p.get("canonical_url"),
            "audience": p.get("audience"),
        }
        if bodies and p.get("slug"):
            try:
                d = json.loads(_get(f"{base}/posts/{p['slug']}"))
                row["body"] = _strip(d.get("body_html") or "")
            except Exception as e:
                row["body"] = f"[ERR {e}]"
        rows.append(row)
    rows.sort(key=lambda r: r["date"])
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sub", default="aidanjude")
    ap.add_argument("--out", default="data/personal_corpus/substack_posts.json")
    ap.add_argument("--bodies", action="store_true", default=True)
    args = ap.parse_args()
    rows = export(args.sub, args.bodies)
    with open(args.out, "w") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(rows)} posts -> {args.out}")
    for r in rows:
        print(f"  {r['date']}  {str(r['wordcount'] or '?'):>5}w  {r['title']}")


if __name__ == "__main__":
    main()
