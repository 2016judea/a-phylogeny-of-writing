#!/usr/bin/env python3
"""Generate essays.html — an archive of the full Substack run (every dated essay
since Jan 2023), grouped into the three voices the newsletter braids: Literature &
Ideas, the Founder (AI & markets), and the Photographer (journals). Our own static
preview cards — works for archived issues the public Substack API no longer lists.

Data: data/personal_corpus/substack_all.json  (built by substack_all_export.py)

    python3 scripts/personal_corpus/build_essays_page.py [out.html]
"""
import html
import json
import sys
from datetime import datetime

DATA = json.load(open("data/personal_corpus/substack_all.json"))
OUT = sys.argv[1] if len(sys.argv) > 1 else "essays.html"

# --- the three voices ---------------------------------------------------------
VOICES = [
    ("ideas", "Literature &amp; Ideas", "#8c6b9c",
     "Epigraphs and arguments — McCarthy, Rand, the Greeks, Freud, Hegel. The reader thinking out loud."),
    ("founder", "The Founder", "#4a6b7c",
     "AI, markets, and the operator's notebook — Claude Code, the bubble, antitrust, the stock that got away."),
    ("journal", "Field Notes", "#b5563c",
     "The photographer's voice — travel, film stock, dream diaries, and gratitude. Physical-media journals."),
]
VLABEL = {k: l for k, l, _, _ in VOICES}

# Manual classification (slug -> voice). The 2023–24 issues are multi-topic
# "magazine" dispatches; each is filed under its dominant voice. New posts not
# listed here fall back to keyword scoring below.
THEME = {
    # Literature & Ideas
    "january-part-1": "ideas", "january-part-2": "ideas", "february": "ideas",
    "april": "ideas", "may": "ideas", "june": "ideas", "september": "ideas",
    "october": "ideas", "november": "ideas", "december": "ideas", "january": "ideas",
    "february-24": "ideas", "march-24": "ideas", "april-24": "ideas", "may-24": "ideas",
    "october-24": "ideas", "november-24": "ideas", "september-25": "ideas",
    "sept-25-pt2": "ideas", "dec-25": "ideas", "primitive-anthropology": "ideas",
    "feb-26": "ideas", "mar-25": "ideas", "apr-25": "ideas",
    "the-stoddard-temple-is-a-threat-to": "ideas",
    # The Founder
    "march": "founder", "july": "founder", "august": "founder", "december-24": "founder",
    "titans-and-transformers": "founder", "deepseek": "founder", "february-25": "founder",
    "april-25": "founder", "monopolistic-behavior-in-modern-business": "founder",
    "june-25": "founder", "august-25": "founder", "oct-25": "founder",
    "the-ai-bubble": "founder", "apr-26": "founder", "working-wclaude-code": "founder",
    "thought-experiment": "founder", "publishing-a-newspaper": "founder",
    "opinions-on-the-stock-market": "founder",
    # Field Notes
    "august-24": "journal", "january-25": "journal", "south-africa": "journal",
    "dec-25-pt2": "journal", "italia": "journal", "nyc": "journal",
    "physical-media-journal": "journal", "soulful": "journal", "appreciative": "journal",
    "something-greek": "journal",
}
KW = {
    "founder": ["ai", "claude", "chatgpt", "llm", "agent", "model", "startup", "stock",
                "market", "invest", "econom", "bank", "datacenter", "data center", "mcp",
                "business", "antitrust", "monopol", "deepseek", "nvidia", "google",
                "valuation", "bubble", "deepmind", "transformer", "tech "],
    "journal": ["photo", "film", "camera", "shot ", "exposure", "lomography", "journal",
                "dream", "travel", "trip", "italy", "italia", "cape town", "africa",
                "beach", "yoga", "grateful", "appreciat", "hostel", "flight", "peony"],
    "ideas": ["rand", "mccarthy", "hegel", "plato", "socrates", "cicero", "homer",
              "shakespeare", "milton", "nietzsche", "freud", "philosoph", "poem",
              "poetry", "greek", "athens", "myth", "anthropolog", "novel", "literature"],
}


def voice_of(slug, text):
    if slug in THEME:
        return THEME[slug]
    t = text.lower()
    best, score = "ideas", -1
    for k, words in KW.items():
        s = sum(t.count(w) for w in words)
        if s > score:
            best, score = k, s
    return best


def fmt_date(d):
    return datetime.strptime(d, "%Y-%m-%d").strftime("%b %Y")


def readtime(words):
    return max(1, round(words / 200))


def card(p):
    slug = p["url"].rstrip("/").split("/")[-1]
    sub = p["subtitle"] or ""
    teaser = sub if sub else p["excerpt"][:150].rsplit(" ", 1)[0] + "…"
    pill = "" if p["public"] else '<span class="pill">older issue</span>'
    return f"""      <a class="card" href="{html.escape(p['url'])}" target="_blank" rel="noopener">
        <div class="c-top"><span class="c-date">{fmt_date(p['date'])}</span>{pill}</div>
        <h3 class="c-title">{html.escape(p['title'])}</h3>
        <p class="c-teaser">{html.escape(teaser)}</p>
        <div class="c-foot"><span>{readtime(p['wordcount'])} min</span><span class="c-go">read on Substack&nbsp;↗</span></div>
      </a>"""


def main():
    for p in DATA:
        p["voice"] = voice_of(p["url"].rstrip("/").split("/")[-1],
                              p["title"] + " " + p["excerpt"])
    public_n = sum(1 for p in DATA if p["public"])

    sections = []
    chips = []
    for key, label, color, blurb in VOICES:
        items = sorted([p for p in DATA if p["voice"] == key],
                       key=lambda p: p["date"], reverse=True)
        chips.append(f'<button class="chip" data-v="{key}"><i style="background:{color}"></i>{label} <b>{len(items)}</b></button>')
        cards = "\n".join(card(p) for p in items)
        sections.append(f"""    <section class="voice" id="{key}" style="--accent:{color}">
      <div class="v-head"><h2>{label}</h2><span class="v-count">{len(items)} essays</span></div>
      <p class="v-blurb">{blurb}</p>
      <div class="grid">
{cards}
      </div>
    </section>""")

    page = TEMPLATE
    for k, v in {
        "%%total%%": str(len(DATA)), "%%public_n%%": str(public_n),
        "%%first%%": DATA[0]["date"][:4], "%%last%%": DATA[-1]["date"][:4],
        "%%chips%%": "\n      ".join(chips),
        "%%sections%%": "\n".join(sections),
    }.items():
        page = page.replace(k, v)
    open(OUT, "w").write(page)
    counts = {k: sum(1 for p in DATA if p["voice"] == k) for k, *_ in VOICES}
    print(f"{OUT}: {len(DATA)} essays  ({public_n} public)  -> " +
          "  ".join(f"{VLABEL[k]}:{counts[k]}" for k in counts))


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Essays — Aidan</title>
  <meta name="description" content="A monthly Substack dispatch since 2023, braiding three voices — literature & ideas, the founder, the photographer. The full archive." />
  <meta property="og:title" content="Essays — Aidan" />
  <meta property="og:description" content="The full Substack archive — %%total%% essays since %%first%%, in three voices." />
  <meta property="og:type" content="website" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Geist+Mono:wght@300;400;500&display=swap" rel="stylesheet" />
  <style>
    :root{
      --bg-primary:#f7f3ec;--bg-secondary:#f1ece2;--text-primary:#1c1814;
      --text-secondary:#5a544a;--text-tertiary:#8b8478;
      --border-tertiary:rgba(60,50,40,.12);--border-secondary:rgba(60,50,40,.22);
    }
    @media (prefers-color-scheme:dark){:root{
      --bg-primary:#1a1714;--bg-secondary:#221e1a;--text-primary:#e8e2d4;
      --text-secondary:#b8b0a0;--text-tertiary:#807a6d;
      --border-tertiary:rgba(230,220,200,.12);--border-secondary:rgba(230,220,200,.22);
    }}
    *{box-sizing:border-box;margin:0;padding:0}
    html,body{background:var(--bg-primary);color:var(--text-primary);
      font-family:'EB Garamond',Georgia,serif;min-height:100vh;
      -webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}
    .page{max-width:1100px;margin:0 auto;padding:56px 40px 80px}
    @media (max-width:720px){.page{padding:28px 16px 48px}}
    .site-header{margin-bottom:44px;display:flex;justify-content:space-between;align-items:baseline;gap:16px;flex-wrap:wrap}
    .brand{font-size:21px;font-weight:500;font-style:italic;letter-spacing:-.01em}
    .brand a{color:inherit;text-decoration:none}
    .nav{display:flex;gap:22px;font-family:'Geist Mono',monospace;font-size:12px;letter-spacing:.04em;flex-wrap:wrap}
    .nav a{color:var(--text-secondary);text-decoration:none;transition:color .2s}
    .nav a:hover{color:var(--text-primary)}
    .nav a.active{color:var(--text-primary);border-bottom:1px solid var(--border-secondary)}
    .hero{padding:0 4px;margin-bottom:30px}
    .hero .eyebrow{font-family:'Geist Mono',monospace;font-size:11px;color:var(--text-tertiary);letter-spacing:.12em;text-transform:lowercase}
    .hero h1{font-size:clamp(30px,6vw,44px);font-weight:600;font-style:italic;letter-spacing:-.02em;margin:6px 0 0}
    .lede{max-width:64ch;margin:16px 0 0;font-size:17.5px;line-height:1.55;color:var(--text-secondary)}
    .lede b{color:var(--text-primary);font-weight:600}
    .meta-line{font-family:'Geist Mono',monospace;font-size:11px;color:var(--text-tertiary);letter-spacing:.05em;margin-top:14px}
    .chips{display:flex;gap:10px;flex-wrap:wrap;margin:26px 4px 8px}
    .chip{font-family:'Geist Mono',monospace;font-size:12px;letter-spacing:.03em;color:var(--text-secondary);
      background:var(--bg-secondary);border:1px solid var(--border-tertiary);border-radius:999px;
      padding:7px 14px;cursor:pointer;display:flex;align-items:center;gap:8px;transition:.18s}
    .chip i{width:9px;height:9px;border-radius:50%;display:inline-block}
    .chip b{font-family:'EB Garamond',serif;font-weight:600;color:var(--text-tertiary)}
    .chip:hover{color:var(--text-primary);border-color:var(--border-secondary)}
    .chip.off{opacity:.4}
    .voice{margin-top:52px;scroll-margin-top:20px}
    .v-head{display:flex;align-items:baseline;gap:14px;border-bottom:2px solid var(--accent);padding-bottom:8px}
    .v-head h2{font-size:25px;font-style:italic;font-weight:600;letter-spacing:-.01em}
    .v-count{font-family:'Geist Mono',monospace;font-size:11px;color:var(--text-tertiary);letter-spacing:.05em;margin-left:auto}
    .v-blurb{max-width:60ch;margin:12px 0 22px;font-size:15.5px;line-height:1.5;color:var(--text-secondary)}
    .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}
    .card{display:flex;flex-direction:column;text-decoration:none;color:inherit;
      background:var(--bg-secondary);border:1px solid var(--border-tertiary);
      border-left:3px solid var(--accent);border-radius:5px;padding:16px 16px 14px;
      transition:transform .16s,border-color .16s,box-shadow .16s}
    .card:hover{transform:translateY(-2px);border-color:var(--border-secondary);box-shadow:0 8px 26px rgba(0,0,0,.10)}
    .c-top{display:flex;align-items:center;gap:8px;margin-bottom:8px}
    .c-date{font-family:'Geist Mono',monospace;font-size:10.5px;color:var(--text-tertiary);letter-spacing:.06em;text-transform:uppercase}
    .pill{font-family:'Geist Mono',monospace;font-size:9px;letter-spacing:.06em;text-transform:uppercase;
      color:var(--text-tertiary);border:1px solid var(--border-tertiary);border-radius:3px;padding:1px 5px;margin-left:auto}
    .c-title{font-size:19px;font-weight:600;line-height:1.18;letter-spacing:-.01em;margin-bottom:7px}
    .c-teaser{font-size:14.5px;line-height:1.45;color:var(--text-secondary);flex:1;
      display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
    .c-foot{display:flex;justify-content:space-between;align-items:center;margin-top:13px;
      font-family:'Geist Mono',monospace;font-size:10.5px;color:var(--text-tertiary);letter-spacing:.04em}
    .c-go{color:var(--accent);opacity:0;transform:translateX(-4px);transition:.18s}
    .card:hover .c-go{opacity:1;transform:none}
    .site-footer{margin-top:64px;padding-top:20px;border-top:1px solid var(--border-tertiary);
      font-family:'Geist Mono',monospace;font-size:11px;color:var(--text-tertiary);letter-spacing:.04em}
    .site-footer a{color:inherit;border-bottom:1px solid var(--border-secondary);text-decoration:none}
    body.filtered .voice{display:none}
    body.filtered .voice.show{display:block}
  </style>
</head>
<body>
<div class="page">
  <header class="site-header">
    <div class="brand"><a href="/">Aidan</a></div>
    <nav class="nav">
      <a href="/projects.html">dev projects</a>
      <a href="/research.html">research</a>
      <a href="/topology.html">topology</a>
      <a href="/something-western.html">novel</a>
      <a href="/reading.html">reading</a>
      <a href="/study.html">study</a>
      <a href="/essays.html" class="active">essays</a>
      <a href="/photography.html">35mm photography</a>
    </nav>
  </header>
  <main>
    <div class="hero">
      <span class="eyebrow">the substack archive</span>
      <h1>Essays</h1>
      <p class="lede">A monthly dispatch since <b>January 2023</b> — %%total%% essays and counting, braiding three voices: <b>literature &amp; ideas</b>, <b>the founder</b>, and <b>the photographer</b>. Grouped by voice below; each card opens the piece on Substack.</p>
      <p class="meta-line">%%total%% essays · 3 voices · %%first%%–%%last%% · %%public_n%% live on Substack, the rest earlier issues</p>
    </div>
    <div class="chips" id="chips">
      <button class="chip chip-all" data-v="all">all</button>
      %%chips%%
    </div>
%%sections%%
  </main>
  <footer class="site-footer">aidanjude.substack.com · a monthly dispatch since 2023 · <a href="https://aidanjude.substack.com/" target="_blank" rel="noopener">subscribe ↗</a></footer>
</div>
<script>
  const chips=[...document.querySelectorAll('.chip')];
  chips.forEach(c=>c.addEventListener('click',()=>{
    const v=c.dataset.v;
    if(v==='all'){document.body.classList.remove('filtered');chips.forEach(x=>x.classList.remove('off'));return;}
    document.body.classList.add('filtered');
    document.querySelectorAll('.voice').forEach(s=>s.classList.toggle('show',s.id===v));
    chips.forEach(x=>x.classList.toggle('off',x.dataset.v!==v&&x.dataset.v!=='all'));
  }));
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
