#!/usr/bin/env python3
"""Full-fidelity sync of the personal corpus into Notion (verbatim, no truncation).

Reads the local JSON in data/personal_corpus/ and writes COMPLETE bodies into the
Notion writing_library DB as paragraph blocks (chunked to Notion's 2000-char limit).
Idempotent: matches existing pages by source_url (substack) or file_path (Dropbox);
updates their body in place, or creates the page if missing. Reading rows are
metadata-only (no body) and are upserted by title|read_date.

Uses NOTION_TOKEN from .env (internal integration already shared into both DBs).

    export $(grep -v ^# .env | xargs)
    python3 scripts/personal_corpus/notion_push.py --writing     # full bodies
    python3 scripts/personal_corpus/notion_push.py --reading     # book rows
    python3 scripts/personal_corpus/notion_push.py --all
"""
import argparse
import json
import os
import re
import time
import urllib.request

API = "https://api.notion.com/v1"
READING_DB = "c06f03ec-b284-43cc-807a-6dc775c23b64"
WRITING_DB = "5d2055b9-74dd-4bf4-bb96-7ce211b898be"
SMAP = {"Poetry": "poetry", "Assorted Prose": "short_story", "Reflections": "notes",
        "Journal Transcriptions": "journal", "European Journal -- 2024": "journal",
        "(root)": "notes", "Projects": "novel"}


def _hdr():
    return {"Authorization": "Bearer " + os.environ["NOTION_TOKEN"],
            "Content-Type": "application/json", "Notion-Version": "2022-06-28"}


def _req(method, path, body=None, _tries=4):
    data = json.dumps(body).encode() if body is not None else None
    for attempt in range(_tries):
        try:
            req = urllib.request.Request(API + path, data=data, headers=_hdr(), method=method)
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code in (409, 429, 502, 503) and attempt < _tries - 1:
                time.sleep(1.5 * (attempt + 1)); continue
            raise
    return None


def _rt(text):
    return [{"type": "text", "text": {"content": text[:1900]}}]


def _blocks(text):
    """Full body → paragraph blocks, preserving blank-line paragraphs, ≤1900 chars each."""
    out = []
    for para in re.split(r"\n\s*\n", (text or "").replace("\r\n", "\n").strip()):
        para = para.rstrip()
        if not para.strip():
            continue
        for i in range(0, len(para), 1900):
            out.append({"object": "block", "type": "paragraph",
                        "paragraph": {"rich_text": [{"type": "text",
                                      "text": {"content": para[i:i + 1900]}}]}})
    return out


def _existing(db, keyprops):
    """Map dedup-key -> page_id for all (non-archived) pages in db."""
    m, cursor = {}, None
    while True:
        body = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        res = _req("POST", f"/databases/{db}/query", body)
        for pg in res["results"]:
            pr = pg["properties"]
            parts = []
            for p in keyprops:
                v = pr.get(p, {}) or {}
                t = v.get("type")
                if t == "title":
                    parts.append("".join(x["plain_text"] for x in v["title"]))
                elif t == "url":
                    parts.append(v.get("url") or "")
                elif t == "rich_text":
                    parts.append("".join(x["plain_text"] for x in v["rich_text"]))
                elif t == "date":
                    parts.append((v.get("date") or {}).get("start") or "")
            m["|".join(parts)] = pg["id"]
        if not res.get("has_more"):
            break
        cursor = res["next_cursor"]
    return m


def _clear_body(page_id):
    cursor = None
    while True:
        q = f"/blocks/{page_id}/children?page_size=100" + (f"&start_cursor={cursor}" if cursor else "")
        res = _req("GET", q)
        for b in res["results"]:
            _req("DELETE", f"/blocks/{b['id']}")
            time.sleep(0.2)
        if not res.get("has_more"):
            break
        cursor = res["next_cursor"]


def _append(page_id, blocks):
    for i in range(0, len(blocks), 100):
        _req("PATCH", f"/blocks/{page_id}/children", {"children": blocks[i:i + 100]})
        time.sleep(0.34)


def _props(row):
    p = {"Name": {"title": _rt(row["name"])},
         "source": {"select": {"name": row["source"]}},
         "entry_date": {"date": {"start": row["date"]}}}
    if row.get("url"):
        p["source_url"] = {"url": row["url"]}
    if row.get("fp"):
        p["file_path"] = {"rich_text": _rt(row["fp"])}
    return p


def push_writing():
    rows = []
    sub = "data/personal_corpus/substack_posts.json"
    if os.path.exists(sub):
        for p in json.load(open(sub)):
            rows.append({"name": p["title"], "source": "substack", "date": p["date"],
                         "url": p["url"], "fp": "", "body": p.get("body", "")})
    wc = "data/personal_corpus/writing_corpus.json"
    if os.path.exists(wc):
        for r in json.load(open(wc)):
            rows.append({"name": r["name"].replace(".md", ""),
                         "source": SMAP.get(r["category"], "notes"), "date": r["date"],
                         "url": "", "fp": r["path"], "body": r["text"]})
    existing = _existing(WRITING_DB, ["source_url", "file_path"])
    upd = new = 0
    for r in rows:
        key = f"{r.get('url','')}|{r.get('fp','')}"
        blocks = _blocks(r["body"])
        pid = existing.get(key)
        if pid:
            _clear_body(pid)
            _append(pid, blocks)
            _req("PATCH", f"/pages/{pid}", {"properties": _props(r)})
            upd += 1
        else:
            created = _req("POST", "/pages", {"parent": {"database_id": WRITING_DB},
                       "properties": _props(r), "children": blocks[:100]})
            if len(blocks) > 100:
                _append(created["id"], blocks[100:])
            new += 1
        time.sleep(0.34)
        print(f"  {'upd' if pid else 'new'}  {r['source']:11} {r['name'][:50]}")
    print(f"writing_library: updated {upd}, created {new} (full bodies)")


def push_reading(path="data/personal_corpus/goodreads_reads.json"):
    items = [i for i in json.load(open(path)) if i.get("read_year")]
    have = _existing(READING_DB, ["Name", "read_date"])
    added = 0
    MON = {m: k + 1 for k, m in enumerate(
        ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])}
    for i in items:
        m = re.search(r"(\d{1,2})\s+([A-Za-z]{3})\s+(20\d\d)", i.get("read_date", "") or "")
        rd = f"{m.group(3)}-{MON[m.group(2)]:02d}-{int(m.group(1)):02d}" if m else ""
        if f"{i['title']}|{rd}" in have:
            continue
        props = {"Name": {"title": _rt(i["title"])},
                 "author": {"rich_text": _rt(i.get("author", ""))},
                 "read_year": {"number": i["read_year"]},
                 "source": {"select": {"name": "goodreads"}},
                 "shelf": {"select": {"name": "read"}}}
        if rd:
            props["read_date"] = {"date": {"start": rd}}
        _req("POST", "/pages", {"parent": {"database_id": READING_DB}, "properties": props})
        added += 1
        time.sleep(0.34)
    print(f"reading_library: +{added} new (of {len(items)})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reading", action="store_true")
    ap.add_argument("--writing", action="store_true")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    if a.all or a.reading:
        push_reading()
    if a.all or a.writing:
        push_writing()
    if not (a.all or a.reading or a.writing):
        ap.print_help()


if __name__ == "__main__":
    main()
