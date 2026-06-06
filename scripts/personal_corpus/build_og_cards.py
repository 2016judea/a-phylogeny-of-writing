#!/usr/bin/env python3
"""Emit 1200x630 link-preview (Open Graph) card HTML for each site page, in the
warm-paper editorial aesthetic. Screenshot each to /tmp/phylo/og/<slug>.png."""
import html as H, pathlib

CARD = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500;1,600&family=Geist+Mono:wght@400&display=swap" rel="stylesheet"/>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1200px;height:630px}}
body{{background:#f7f3ec;color:#1c1814;font-family:'EB Garamond',Georgia,serif;
 padding:66px 76px;display:flex;flex-direction:column;justify-content:space-between;
 position:relative;overflow:hidden;-webkit-font-smoothing:antialiased}}
body:before{{content:"";position:absolute;inset:20px;border:1px solid rgba(60,50,40,.20);border-radius:7px}}
body:after{{content:"";position:absolute;left:0;top:0;bottom:0;width:8px;background:{accent}}}
.top{{display:flex;justify-content:space-between;align-items:baseline;position:relative}}
.brand{{font-size:31px;font-style:italic;font-weight:500;letter-spacing:-.01em}}
.url{{font-family:'Geist Mono',monospace;font-size:16px;letter-spacing:.06em;color:#8b8478}}
.mid{{position:relative}}
.kicker{{font-family:'Geist Mono',monospace;font-size:18px;letter-spacing:.36em;text-transform:uppercase;color:{accent};margin-bottom:24px}}
.title{{font-size:{tsize}px;font-weight:600;font-style:italic;line-height:1.0;letter-spacing:-.02em;max-width:1010px}}
.sub{{margin-top:28px;font-size:30px;line-height:1.42;color:#544e44;max-width:900px}}
.bot{{display:flex;align-items:center;gap:20px;position:relative}}
.rule{{height:1px;flex:1;background:rgba(60,50,40,.22)}}
.foot{{font-family:'Geist Mono',monospace;font-size:15px;letter-spacing:.1em;text-transform:uppercase;color:#8b8478}}
</style></head><body>
<div class="top"><div class="brand">Aidan&nbsp;Jude</div><div class="url">aidanjude.vercel.app</div></div>
<div class="mid"><div class="kicker">{kicker}</div><div class="title">{title}</div><div class="sub">{sub}</div></div>
<div class="bot"><div class="foot">{fl}</div><div class="rule"></div><div class="foot">{fr}</div></div>
</body></html>"""

CARDS = {
 "home": dict(accent="#7c4a3a", tsize=80, kicker="Aidan Jude",
   title="These are my ideas.",
   sub="Dev projects, a novel, a decade of reading, and the threads between them. Feel free to have a look around.",
   fl="have a look around", fr="aidanjude.vercel.app"),
 "projects": dict(accent="#7c4a3a", tsize=92, kicker="Aidan Jude · Code",
   title="Dev Projects",
   sub="Things I've built — AI on small hardware, language turned into data, and a handful of experiments.",
   fl="github.com/2016judea", fr="mostly python"),
 "research": dict(accent="#3a5a7c", tsize=84, kicker="Aidan Jude · Research",
   title="Literature, read by machine.",
   sub="Turning books into data — NLP and network analysis applied to prose, voice, and the shape of genre. Including primary research at Columbia.",
   fl="github.com/2016judea", fr="nlp · networks"),
 "topology": dict(accent="#7c4a3a", tsize=80, kicker="Idea Topology",
   title="A Phylogeny of Writing",
   sub="A living, interactive map of how my reading and my writing connect — 2023–2026.",
   fl="interactive", fr="reading · writing · substack"),
 "something-western": dict(accent="#7c4a3a", tsize=104, kicker="A Novel",
   title="Something Western",
   sub="Two young men, one Texas summer — 1959. And the question of what else is out there.",
   fl="by Aidan Jude", fr="≈26k words · ~115 min"),
 "reading": dict(accent="#4a5a3a", tsize=82, kicker="Research &amp; Interests",
   title="What I Read For",
   sub="The questions pulling me through the books — a decade of reading, 2014–2026.",
   fl="topology", fr="what I read"),
 "work": dict(accent="#3a4a6a", tsize=88, kicker="Creative Ideation",
   title="What I Made",
   sub="Poetry, prose, and the novel — and what the writing keeps reaching toward.",
   fl="topology", fr="2022–2026"),
}

out = pathlib.Path("/tmp/og_cards"); out.mkdir(exist_ok=True)
for slug, c in CARDS.items():
    (out / f"{slug}.html").write_text(CARD.format(**c), encoding="utf-8")
    print("wrote", out / f"{slug}.html")

# GLEAN has its own identity (dark, Bodoni Moda, orange accent) — its own card,
# featuring the real Issue №1 cover on the left.
GLEAN_COVER = "/tmp/phylo/glean/issue-01/cover.webp"
GLEAN_CARD = """<!DOCTYPE html><html><head><meta charset="utf-8"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,700;0,6..96,900;1,6..96,500&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<style>
*{margin:0;padding:0;box-sizing:border-box}html,body{width:1200px;height:630px}
body{background:#0b0b0c;color:#ece7dd;font-family:'Bodoni Moda',Georgia,serif;display:flex;overflow:hidden}
.cover{width:392px;height:630px;background:#141416 url('file://__COVER__') center/cover no-repeat;border-right:3px solid #e8542b;flex-shrink:0}
.right{flex:1;display:flex;flex-direction:column;justify-content:space-between;padding:60px 66px}
.kick{font-family:'Geist Mono',monospace;font-size:17px;letter-spacing:.18em;text-transform:uppercase;color:#8b867d}
.mast{font-weight:900;font-size:150px;line-height:.86;letter-spacing:-.02em}
.mast .dot{color:#e8542b}
.tag{font-style:italic;font-size:36px;color:#b8b2a6;margin-top:14px}
.foot{font-family:'Geist Mono',monospace;font-size:15px;letter-spacing:.1em;text-transform:uppercase;color:#8b867d}
.foot b{color:#e8542b;font-weight:500}
</style></head><body>
<div class="cover"></div>
<div class="right">
  <div class="kick">Issue №1 · Spring 2026 · 20 pages</div>
  <div><div class="mast">GLEAN<span class="dot">.</span></div><div class="tag">a field journal</div></div>
  <div class="foot">read online · <b>aidanjude.vercel.app/glean</b></div>
</div>
</body></html>"""
(out / "glean.html").write_text(GLEAN_CARD.replace("__COVER__", GLEAN_COVER), encoding="utf-8")
print("wrote", out / "glean.html")
print("\nNext: screenshot each /tmp/og_cards/<slug>.html at 1200x630 -> /tmp/phylo/og/<slug>.png")
