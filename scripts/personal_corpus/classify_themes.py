#!/usr/bin/env python3
"""Classify the 310 dated Goodreads reads into thematic threads → year×theme matrix.

Each book gets ONE primary thread (first matching rule wins; rules ordered most
specific → most general). Output feeds the reading-progression streamgraph.
"""
import json
import re
from collections import defaultdict, Counter

# (thread, color, author-substrings, title-substrings). First match wins.
# Ordered so specific genres claim their authors before the broad "Canon" net.
RULES = [
    ("Science & Cosmos", "#6b8f9c",
     ["hawking", "gleick", "kip s. thorne", "hofstadter", "ashlee vance", "robin waterfield"], []),
    ("Money, Power & Polemic", "#9c7a3c",
     ["ayn rand", "bastiat", "rothbard", "niall ferguson", "michael   lewis", "michael lewis",
      "charles", "koch", "john doerr", "machiavelli", "thomas paine", "christopher hitchens",
      "malcolm gladwell", "dwight macdonald", "j.d. vance", "wendell berry"], ["the law"]),
    ("Faith & the Sacred", "#7a9c6b",
     ["c.s. lewis", "gautama buddha", "eugene vodolazkin", "christian wiman", "graham greene"],
     ["screwtape", "mere christianity", "diamond sutra", "great divorce", "abolition of man"]),
    ("Philosophy & the Examined Life", "#8c6b9c",
     ["nietzsche", "albert camus", "kierkegaard", "plato", "hegel", "david hume", "c.g. jung",
      "viktor e. frankl", "sam harris", "marcus aurelius", "sigmund freud", "jean baudrillard",
      "franz kafka", "johann wolfgang von goethe"], ["notes from underground", "white nights"]),
    ("Poetry", "#c98a6b",
     ["keats", "shelley", "byron", "wordsworth", "whitman", "sylvia plath", "t.s. eliot",
      "ezra pound", "philip larkin", "robert frost", "charles simic", "louise gl", "frank o'hara",
      "e.e. cummings", "tennyson", "rupert brooke", "hölderlin", "swinburne", "todd boss",
      "macaulay", "lana del rey", "shakespeare", "david whyte"],
     ["selected poems", "collected poems", "complete poems", "the wild iris", "poems and"]),
    ("Beats & Transgression", "#b5563c",
     ["jack kerouac", "bret easton ellis", "hubert selby", "chuck palahniuk", "john fante",
      "hunter s. thompson", "jay mcinerney", "dalton trumbo", "anthony bourdain"], []),
    ("Crime & Noir", "#5a5550",
     ["raymond chandler", "agatha christie", "vincent bugliosi", "erik larson", "steve berry",
      "dan    brown", "dan brown", "malcolm braly"], []),
    ("Southern Gothic & American Grit", "#7c4a3a",
     ["cormac mccarthy", "william gay", "denis johnson", "larry mcmurtry", "don carpenter",
      "leonard gardner", "richard brautigan", "iain banks", "flannery o'connor", "walker percy",
      "knut hamsun", "ken kesey"], []),
    ("Modernism & Experiment", "#4a6b7c",
     ["james joyce", "virginia woolf", "thomas pynchon", "william h. gass", "william faulkner",
      "vladimir nabokov", "italo calvino", "olga tokarczuk", "david foster wallace",
      "adolfo bioy casares", "louis-ferdinand", "thomas wolfe"], []),
    ("Dystopia & Speculative", "#3c6b5a",
     ["aldous huxley", "george orwell", "ray bradbury", "h.g. wells", "kazuo ishiguro",
      "orson scott card", "william golding", "kurt vonnegut", "frank patrick herbert",
      "frank herbert", "dan simmons", "anthony burgess"], []),
    ("Fantasy & Adventure", "#9c8f5a",
     ["john flanagan", "christopher paolini", "patrick rothfuss", "richard  adams",
      "kenneth grahame", "carlos ruiz", "khaled hosseini"], []),
]
CANON = ("The American Canon", "#b89a6a")  # default for unmatched literary fiction


def thread_for(title, author):
    a, t = author.lower(), title.lower()
    for name, color, auths, titles in RULES:
        if any(s in a for s in auths) or any(s in t for s in titles):
            return name, color
    return CANON


def main():
    items = [i for i in json.load(open("data/personal_corpus/goodreads_reads.json")) if i.get("read_year")]
    years = list(range(min(i["read_year"] for i in items), max(i["read_year"] for i in items) + 1))
    order = [r[0] for r in RULES] + [CANON[0]]
    colors = {r[0]: r[1] for r in RULES}; colors[CANON[0]] = CANON[1]
    counts = {th: {y: 0 for y in years} for th in order}
    examples = defaultdict(list)  # theme -> list of "Title — Author"
    for i in items:
        th, _ = thread_for(i["title"], i["author"])
        counts[th][i["read_year"]] += 1
        auth = re.sub(r"\s+", " ", i["author"]).strip()
        examples[th].append(i["title"] + " — " + auth)
    # keep threads sorted by first year of emergence, then total volume
    def emergence(th):
        for y in years:
            if counts[th][y]:
                return y
        return 9999
    # movement each thread belongs to (the 5-act arc the data revealed)
    MOVEMENT = {
        "Fantasy & Adventure": "Story", "Dystopia & Speculative": "Story", "Science & Cosmos": "Story",
        "The American Canon": "Style", "Poetry": "Style", "Modernism & Experiment": "Style",
        "Southern Gothic & American Grit": "Ideas", "Money, Power & Polemic": "Ideas",
        "Philosophy & the Examined Life": "Ideas",
        "Beats & Transgression": "Meaning", "Crime & Noir": "Meaning", "Faith & the Sacred": "Meaning",
    }
    MOVE_ORDER = {"Story": 0, "Style": 1, "Ideas": 2, "Meaning": 3}
    # marquee author per thread (most-read author within it) + book count
    marquee = {}
    for th in order:
        ac = Counter()
        for i in items:
            t2, _ = thread_for(i["title"], i["author"])
            if t2 == th:
                ac[re.sub(r"\s+", " ", i["author"]).strip()] += 1
        marquee[th] = ac.most_common(1)[0] if ac else ("", 0)

    # order threads by movement, then volume (terrain reads Story→Style→Ideas→Meaning)
    order.sort(key=lambda th: (MOVE_ORDER.get(MOVEMENT.get(th, "Ideas"), 9), -sum(counts[th].values())))
    threads = [{
        "name": th, "color": colors[th],
        "movement": MOVEMENT.get(th, "Ideas"),
        "marquee": marquee[th][0], "marquee_n": marquee[th][1],
        "total": sum(counts[th].values()),
        "counts": [counts[th][y] for y in years],
        "examples": examples[th][:6],
    } for th in order if sum(counts[th].values()) > 0]
    out = {
        "years": years,
        "threads": threads,
        "milestones": [
            {"year": 2019, "label": "canon explosion · 80"},
            {"year": 2021, "label": "McCarthy + ideology"},
            {"year": 2023, "label": "Substack begins · Jan ’23"},
            {"year": 2025, "label": "Stoicism · Zen · Rubin"},
        ],
        "totals": {"books": len(items), "threads": len(threads)},
    }
    json.dump(out, open("data/personal_corpus/themes_by_year.json", "w"), indent=2, ensure_ascii=False)
    print(f"{len(items)} books → {len(threads)} threads over {years[0]}–{years[-1]}")
    for t in threads:
        spark = "".join("▁▂▃▅▆▇█"[min(c, 6)] for c in t["counts"])
        print(f"  {t['name']:34} {t['total']:3}  {spark}")


if __name__ == "__main__":
    main()
