#!/usr/bin/env python3
"""Pull the Dropbox /Writing corpus via the Dropbox API.

The local files are Dropbox "online-only" placeholders (0 bytes on disk), and a
2024-12 bulk import flattened the local mtimes. The API is the source of truth:
it returns real content plus client_modified timestamps (the ~19 post-import
pieces keep their true 2025-2026 dates; the rest carry the import stamp).

Needs DROPBOX_APP_KEY / DROPBOX_APP_SECRET / DROPBOX_REFRESH_TOKEN in .env.

Usage:
    export $(grep -v ^# .env | xargs)
    python3 scripts/personal_corpus/dropbox_writing_pull.py \
        [--folder /Writing] [--out data/personal_corpus/writing_corpus.json]
"""
import argparse
import json
import os
import urllib.parse
import urllib.request


def _access_token() -> str:
    data = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "client_id": os.environ["DROPBOX_APP_KEY"],
        "client_secret": os.environ["DROPBOX_APP_SECRET"],
        "refresh_token": os.environ["DROPBOX_REFRESH_TOKEN"],
    }).encode()
    req = urllib.request.Request(
        "https://api.dropbox.com/oauth2/token", data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    return json.loads(urllib.request.urlopen(req, timeout=20).read())["access_token"]


def _rpc(tok, ep, arg):
    req = urllib.request.Request(
        "https://api.dropboxapi.com/2/" + ep, data=json.dumps(arg).encode(),
        headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())


def _download(tok, path) -> str:
    req = urllib.request.Request(
        "https://content.dropboxapi.com/2/files/download",
        headers={"Authorization": "Bearer " + tok,
                 "Dropbox-API-Arg": json.dumps({"path": path})})
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")


def pull(folder="/Writing"):
    tok = _access_token()
    res = _rpc(tok, "files/list_folder", {"path": folder, "recursive": True})
    entries = res["entries"]
    while res.get("has_more"):
        res = _rpc(tok, "files/list_folder/continue", {"cursor": res["cursor"]})
        entries += res["entries"]
    files = [e for e in entries
             if e[".tag"] == "file" and e["name"].lower().endswith((".md", ".txt"))]
    out = []
    for e in files:
        try:
            text = _download(tok, e["path_lower"])
        except Exception as ex:
            text = f"[ERR {ex}]"
        parts = e["path_display"].strip("/").split("/")
        out.append({
            "path": e["path_display"],
            "category": parts[1] if len(parts) > 2 else "(root)",
            "name": e["name"],
            "date": e["client_modified"][:10],
            "words": len(text.split()),
            "text": text,
        })
    out.sort(key=lambda r: (r["category"], r["name"]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--folder", default="/Writing")
    ap.add_argument("--out", default="data/personal_corpus/writing_corpus.json")
    args = ap.parse_args()
    rows = pull(args.folder)
    with open(args.out, "w") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    from collections import Counter
    c = Counter(r["category"] for r in rows)
    print(f"Wrote {len(rows)} files -> {args.out}")
    for cat, n in c.most_common():
        print(f"  {cat}: {n}")


if __name__ == "__main__":
    main()
