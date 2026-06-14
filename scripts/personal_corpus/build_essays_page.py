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
    "study-guide-quantum-gravity": "ideas",
    # The Founder
    "march": "founder", "july": "founder", "august": "founder", "december-24": "founder",
    "titans-and-transformers": "founder", "deepseek": "founder", "february-25": "founder",
    "april-25": "founder", "monopolistic-behavior-in-modern-business": "founder",
    "june-25": "founder", "august-25": "founder", "oct-25": "founder",
    "the-ai-bubble": "founder", "apr-26": "founder", "working-wclaude-code": "founder",
    "thought-experiment": "founder", "publishing-a-newspaper": "founder",
    "opinions-on-the-stock-market": "founder",
    "rodent-inspections-archive": "founder",
    # Field Notes
    "august-24": "journal", "january-25": "journal", "south-africa": "journal",
    "dec-25-pt2": "journal", "italia": "journal", "nyc": "journal",
    "physical-media-journal": "journal", "soulful": "journal", "appreciative": "journal",
    "something-greek": "journal",
    "jun-26": "journal", "feb-26-archive": "journal", "astroid-trails": "journal",
    "last-night-there-was-a-huge-storm": "journal",
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

    /* ---- idea topology — migrated from the old /topology page ---- */
    .topo-embed{margin-bottom:54px}
    @media (max-width:720px){.topo-embed{margin-bottom:36px}}
.topology-header {
      padding: 0 4px 12px;
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
    }

    @media (max-width: 720px) {
      .topology-header { gap: 8px; }
      .topology-header .header-stats { text-align: left; font-size: 11px; }
    }

    .header-left { display: flex; flex-direction: column; gap: 2px; }

    .header-eyebrow {
      font-family: 'Geist Mono', monospace;
      font-size: 11px;
      color: var(--text-tertiary);
      letter-spacing: 0.12em;
      text-transform: uppercase;
    }

    .header-title {
      font-family: 'EB Garamond', Georgia, serif;
      font-size: 34px;
      font-style: italic;
      font-weight: 500;
      color: var(--text-primary);
      letter-spacing: -0.01em;
      line-height: 1.15;
    }

    @media (max-width: 720px) {
      .header-title { font-size: 24px; line-height: 1.2; }
    }

    .header-stats {
      font-family: 'Geist Mono', monospace;
      font-size: 12px;
      color: var(--text-secondary);
      text-align: right;
      line-height: 1.6;
    }

    .stat-num { color: var(--text-primary); font-weight: 500; }

    .legend {
      display: flex;
      gap: 18px;
      padding: 0 4px 18px;
      flex-wrap: wrap;
    }

    @media (max-width: 720px) {
      .legend { gap: 10px 14px; padding-bottom: 14px; }
    }

    .legend-item {
      display: flex;
      align-items: center;
      gap: 7px;
      font-family: 'Geist Mono', monospace;
      font-size: 11px;
      color: var(--text-secondary);
      cursor: pointer;
      user-select: none;
      transition: opacity 0.2s;
      letter-spacing: 0.02em;
    }

    .legend-item.dim { opacity: 0.35; }

    .legend-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      flex-shrink: 0;
    }

    .canvas-wrap {
      position: relative;
      width: 100%;
      height: min(82vh, 880px);
      min-height: 600px;
    }

    @media (max-width: 720px) {
      /* Square-ish canvas on phones — the topology is round, vertical aspect wastes space */
      .canvas-wrap {
        height: min(110vw, 90vh);
        min-height: 380px;
        max-height: 640px;
      }
    }

    .recenter-btn {
      position: absolute;
      top: 14px;
      left: 14px;
      background: var(--bg-primary);
      border: 0.5px solid var(--border-secondary);
      border-radius: 999px;
      padding: 7px 16px 7px 13px;
      font-family: 'EB Garamond', Georgia, serif;
      font-style: italic;
      font-size: 14px;
      color: var(--text-secondary);
      cursor: pointer;
      opacity: 0;
      pointer-events: none;
      transform: translateY(-4px);
      transition: opacity 0.3s, transform 0.3s, color 0.2s, border-color 0.2s;
      z-index: 5;
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }

    .recenter-btn.visible {
      opacity: 1;
      pointer-events: auto;
      transform: translateY(0);
    }

    .recenter-btn:hover {
      color: var(--text-primary);
      border-color: var(--text-secondary);
    }

    .recenter-arrow {
      font-family: 'Geist Mono', monospace;
      font-size: 13px;
      font-style: normal;
    }

    canvas { display: block; width: 100%; height: 100%; }

    .tooltip {
      position: absolute;
      pointer-events: none;
      opacity: 0;
      transition: opacity 0.18s;
      background: var(--bg-primary);
      border: 0.5px solid var(--border-secondary);
      border-radius: 8px;
      padding: 12px 16px;
      max-width: 260px;
      font-family: 'EB Garamond', Georgia, serif;
      z-index: 10;
    }

    @media (max-width: 720px) {
      .tooltip { max-width: 200px; padding: 10px 12px; }
      .tooltip-title { font-size: 15px; }
    }

    .tooltip.visible { opacity: 1; }

    .tooltip-title {
      font-size: 18px;
      font-weight: 500;
      color: var(--text-primary);
      line-height: 1.25;
      margin-bottom: 6px;
      font-style: italic;
    }

    .tooltip-meta {
      font-size: 12px;
      font-family: 'Geist Mono', monospace;
      color: var(--text-secondary);
      letter-spacing: 0.02em;
    }

    .tooltip-source {
      display: inline-block;
      padding: 2px 7px;
      margin-right: 6px;
      border-radius: 3px;
      font-size: 10px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }

    .footer-bar {
      padding: 14px 4px 0;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: 'Geist Mono', monospace;
      font-size: 11px;
      color: var(--text-tertiary);
      letter-spacing: 0.04em;
      border-top: 0.5px solid var(--border-tertiary);
      margin-top: 10px;
    }

    @media (max-width: 720px) {
      .footer-bar { flex-direction: column; gap: 6px; align-items: flex-start; font-size: 10px; }
      .footer-tip { font-size: 13px; }
    }

    .footer-tip {
      font-style: italic;
      font-family: 'EB Garamond', serif;
      font-size: 14px;
      color: var(--text-secondary);
    }

    .colophon {
      margin-top: 96px;
      padding-top: 36px;
      border-top: 0.5px solid var(--border-tertiary);
      font-family: 'EB Garamond', Georgia, serif;
      font-size: 17px;
      line-height: 1.7;
      color: var(--text-secondary);
      max-width: 680px;
    }

    @media (max-width: 720px) {
      .colophon { margin-top: 56px; padding-top: 28px; font-size: 15px; line-height: 1.65; }
    }

    .colophon p { margin-bottom: 16px; }

    .colophon a {
      color: var(--text-primary);
      text-decoration: underline;
      text-decoration-thickness: 0.5px;
      text-underline-offset: 3px;
      text-decoration-color: var(--border-secondary);
      transition: text-decoration-color 0.2s;
    }

    .colophon a:hover { text-decoration-color: var(--text-primary); }

    .colophon-meta {
      font-family: 'Geist Mono', monospace;
      font-size: 11px;
      color: var(--text-tertiary);
      letter-spacing: 0.04em;
      margin-top: 28px;
    }

    .colophon-meta a {
      color: var(--text-secondary);
      text-decoration: underline;
      text-decoration-thickness: 0.5px;
      text-underline-offset: 2px;
      text-decoration-color: var(--border-secondary);
      transition: color 0.2s, text-decoration-color 0.2s;
    }

    .colophon-meta a:hover {
      color: var(--text-primary);
      text-decoration-color: var(--text-primary);
    }
  </style>
</head>
<body>
<div class="page">
  <header class="site-header">
    <div class="brand"><a href="/">Aidan</a></div>
    <nav class="nav">
      <a href="/projects.html">dev projects</a>
      <a href="/research.html">research</a>
      <a href="/something-western.html">novel</a>
      <a href="/reading.html">reading</a>
      <a href="/study.html">study</a>
      <a href="/essays.html" class="active">essays</a>
      <a href="/photography.html">35mm photography</a>
      <a href="/glean/">glean</a>
    </nav>
  </header>
  <main>
    <section class="topo-embed">
<div class="topology-header">
        <div class="header-left">
          <span class="header-eyebrow">idea topology</span>
          <span class="header-title">a phylogeny of writing, 2023–2026</span>
        </div>
        <div class="header-stats" id="stats"></div>
      </div>

      <div class="legend" id="legend"></div>

      <div class="canvas-wrap">
        <canvas id="c"></canvas>
        <button class="recenter-btn" id="recenter-btn" aria-label="Return to overview">
          <span class="recenter-arrow">←</span> back to aidan
        </button>
        <div class="tooltip" id="tip">
          <div class="tooltip-title" id="tip-title"></div>
          <div class="tooltip-meta" id="tip-meta"></div>
        </div>
      </div>

      <div class="footer-bar">
        <span>hover · drift · let the canopy breathe</span>
        <span class="footer-tip">click a theme to focus</span>
      </div>
    </section>
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
<script src="/topology-viz.js"></script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
