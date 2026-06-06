#!/usr/bin/env python3
"""Regenerate the data behind topology.html — "a phylogeny of writing" — from the
real corpus instead of the old hand-faked ~43-node snapshot. Every Substack essay
(real titles + dates, from substack_all.json) plus the poems (from
writing_corpus.json) are clustered into the page's six idea-themes, sized by form,
and threaded with cross-theme links derived from shared vocabulary.

This is an in-place transform: it reads topology.html, swaps the CORPUS and
CROSS_LINKS arrays (and freshens the colophon), and leaves the canvas engine and
the six THEMES untouched. Stats + legend recompute themselves from CORPUS.

    python3 scripts/personal_corpus/build_topology_page.py [topology.html]
"""
import json
import re
import sys
from collections import defaultdict

PAGE = sys.argv[1] if len(sys.argv) > 1 else "topology.html"
ESSAYS = json.load(open("data/personal_corpus/substack_all.json"))
CORPUS_JSON = json.load(open("data/personal_corpus/writing_corpus.json"))

# Six themes already defined in the page (ids must match):
#   reaching · mind · inner · time · place · examined

# --- essays: slug -> theme (read from content; the 2023–24 issues are
# multi-topic and filed by dominant current) -----------------------------------
ESSAY_THEME = {
    "january-part-1": "examined", "january-part-2": "examined", "february": "examined",
    "march": "examined", "april": "examined", "june": "examined", "july": "examined",
    "august": "examined", "february-24": "examined", "april-24": "examined",
    "oct-25": "examined", "monopolistic-behavior-in-modern-business": "examined",
    "april-25": "examined", "the-stoddard-temple-is-a-threat-to": "examined",
    "opinions-on-the-stock-market": "examined",
    "may": "reaching", "february-25": "reaching", "june-25": "reaching",
    "august-25": "reaching", "publishing-a-newspaper": "reaching",
    "september": "mind", "november": "mind", "december-24": "mind",
    "titans-and-transformers": "mind", "deepseek": "mind", "the-ai-bubble": "mind",
    "september-25": "mind", "apr-26": "mind", "working-wclaude-code": "mind",
    "thought-experiment": "mind",
    "december": "time", "march-24": "time", "sept-25-pt2": "time", "dec-25": "time",
    "primitive-anthropology": "time", "mar-25": "time", "apr-25": "time",
    "october": "inner", "january": "inner", "may-24": "inner", "august-24": "inner",
    "october-24": "inner", "november-24": "inner", "january-25": "inner",
    "dec-25-pt2": "inner", "feb-26": "inner", "physical-media-journal": "inner",
    "soulful": "inner", "appreciative": "inner", "something-greek": "inner",
    "south-africa": "place", "italia": "place", "nyc": "place",
}

POEM_THEME = {
    "Ad Astra": "reaching", "Ambition": "reaching", "Tumbling Astronauts": "reaching",
    "The Merchant Ship": "reaching", "Portal": "reaching", "Your Morning Halo": "reaching",
    "Hang High the Roof Beams": "reaching", "Move Cross Country": "reaching",
    "After Dark": "inner", "For Tiera": "inner", "Let's Get Sentimental Babe": "inner",
    "Purple Pettled Peonies": "inner", "Rainbow Trout": "inner", "Maple Leaves": "inner",
    "Big Sky": "place", "One Mountain, Four Angels": "place", "Parallel Rails": "place",
    "The Fair": "place",
    "These Stones": "time", "The Flood": "time",
    "Like An American": "examined",
}

STOP = set("""the a an and or but of to in on at for with from by as is are was were be
been being this that these those it its their his her our your my we you they i he she
about into over under again more most some such only own same so than too very can will
just dont don't im i'm theres there's what when where which who whom how why all any each
few other out off up down then once here there one two three new like get got way thing
things people make made even still back much many how also because while which whats""".split())


def tokens(text):
    return {w for w in re.findall(r"[a-z]{5,}", text.lower()) if w not in STOP}


def main():
    nodes = []
    # essays — newest data already sorted oldest->newest
    for i, e in enumerate(ESSAYS, 1):
        slug = e["url"].rstrip("/").split("/")[-1]
        theme = ESSAY_THEME.get(slug, "examined")
        nodes.append({
            "id": f"s{i}", "title": e["title"], "theme": theme,
            "source": "substack", "date": e["date"], "weight": 4,
            "_tok": tokens(e["title"] + " " + e["excerpt"]),
        })
    # poems — no reliable dates (corpus carries the import sentinel), so omit date
    poems = [p for p in CORPUS_JSON if p.get("category") == "Poetry"]
    for j, p in enumerate(poems, 1):
        name = p["name"].replace(".md", "").strip()
        theme = POEM_THEME.get(name, "inner")
        nodes.append({
            "id": f"p{j}", "title": name, "theme": theme,
            "source": "poetry", "date": "", "weight": 3,
            "_tok": tokens(name + " " + (p.get("text") or "")),
        })

    # cross-theme links from shared vocabulary; cap degree so the canopy breathes
    scored = []
    for a in range(len(nodes)):
        for b in range(a + 1, len(nodes)):
            na, nb = nodes[a], nodes[b]
            if na["theme"] == nb["theme"]:
                continue
            shared = na["_tok"] & nb["_tok"]
            if len(shared) >= 2:
                scored.append((len(shared), na["id"], nb["id"]))
    scored.sort(reverse=True)
    deg = defaultdict(int)
    links = []
    for _, a, b in scored:
        if deg[a] < 2 and deg[b] < 2:
            links.append((a, b))
            deg[a] += 1
            deg[b] += 1
        if len(links) >= 24:
            break

    # --- render the two JS arrays ---------------------------------------------
    def node_line(n):
        title = json.dumps(n["title"], ensure_ascii=False)
        date = json.dumps(n["date"])
        return (f"      {{ id: '{n['id']}', title: {title}, theme: '{n['theme']}', "
                f"source: '{n['source']}', date: {date}, weight: {n['weight']} }},")

    by_theme = defaultdict(list)
    for n in nodes:
        by_theme[n["theme"]].append(n)
    order = ["reaching", "mind", "inner", "time", "place", "examined"]
    corpus_lines = []
    for th in order:
        corpus_lines.append(f"      // {th}")
        corpus_lines += [node_line(n) for n in by_theme[th]]
    corpus_block = ("    const CORPUS = [\n" + "\n".join(corpus_lines) + "\n    ];")

    link_lines = ", ".join(f"['{a}', '{b}']" for a, b in links)
    links_block = ("    const CROSS_LINKS = [\n      " + link_lines + ",\n    ];")

    # --- splice into the page --------------------------------------------------
    html = open(PAGE, encoding="utf-8").read()
    html = re.sub(r"    const CORPUS = \[.*?\n    \];", corpus_block, html, count=1, flags=re.S)
    html = re.sub(r"    const CROSS_LINKS = \[.*?\n    \];", links_block, html, count=1, flags=re.S)

    # honest colophon: it's now every essay + the poems (not journals/notes)
    html = re.sub(
        r"What you're looking at is a map of .*?association\.",
        "What you're looking at is a map of every Substack essay I've published "
        "since 2023 — threaded with the poems between them — clustered by theme, "
        "linked by association.",
        html, count=1, flags=re.S)
    html = html.replace(
        'The full essays live on <a href="https://aidanjude.substack.com/" target="_blank" rel="noopener">my Substack</a>.',
        'The full essays live in <a href="/essays.html">the archive</a> '
        '(and on <a href="https://aidanjude.substack.com/" target="_blank" rel="noopener">Substack</a>).')

    open(PAGE, "w", encoding="utf-8").write(html)
    counts = {th: len(by_theme[th]) for th in order}
    print(f"{PAGE}: {len(nodes)} nodes ({sum(1 for n in nodes if n['source']=='substack')} essays "
          f"+ {sum(1 for n in nodes if n['source']=='poetry')} poems), {len(links)} cross-links")
    print("  " + "  ".join(f"{th}:{counts[th]}" for th in order))


if __name__ == "__main__":
    main()
