#!/usr/bin/env python3
"""Build the projects landing page (the new site home) from a curated set of
GitHub repos — warm-paper editorial aesthetic, matching the rest of the site.
Bakes repo data (description, language, stars, year) at build time.

Usage: build_projects_page.py [out_dir=/tmp/phylo]
"""
import json, sys, urllib.request, html as H, pathlib

USER = "2016judea"
# Curated, in display order (best / most representative first).
CURATED = [
    "tars-mini",
    "AI-screen-monitor-service",
    "edge-ai-experiment",
    "generative-ai-with-instagram",
    "Physical-Therapy-Market-Analysis",
    "literature-mutations",
    "Prose-Similarities",
    "a-phylogeny-of-writing",
]
# A one-line, plain-spoken gloss per project (mine — sits under the repo's own
# description only where it adds context; kept honest and concrete).
TAGLINE = {
    "a-phylogeny-of-writing": "This very site — three years of journals and essays, mapped.",
}
# Repos whose lang/year meta row is suppressed (e.g. the site itself).
HIDE_META = {"a-phylogeny-of-writing"}
ACR = {"ai": "AI", "tts": "TTS", "nlp": "NLP", "dow": "DOW", "cdk": "CDK", "api": "API", "rpi": "RPi"}
SMALL = {"of", "the", "and", "with", "to", "for", "a", "an", "in", "on"}
def pretty(name):
    words = name.replace("_", "-").split("-")
    out = []
    for i, w in enumerate(words):
        lw = w.lower()
        if lw in ACR: out.append(ACR[lw])
        elif i > 0 and lw in SMALL: out.append(lw)
        else: out.append(w[:1].upper() + w[1:])
    return " ".join(out)

LANG_COLOR = {
    "Python": "#3572A5", "HTML": "#e34c26", "TypeScript": "#3178c6",
    "JavaScript": "#f1e05a", "Jupyter Notebook": "#DA5B0B", "C++": "#f34b7d",
    "Shell": "#89e051", "Go": "#00ADD8", "Rust": "#dea584", "CSS": "#563d7c",
}

out_dir = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/phylo")

req = urllib.request.Request(
    f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner",
    headers={"Accept": "application/vnd.github+json", "User-Agent": "aidan-site-build"})
repos = {r["name"]: r for r in json.load(urllib.request.urlopen(req))}

cards = []
for name in CURATED:
    r = repos.get(name)
    if not r:
        print(f"  ! missing repo: {name}", file=sys.stderr); continue
    desc = (r.get("description") or "").strip()
    extra = TAGLINE.get(name, "")
    lang = r.get("language") or ""
    color = LANG_COLOR.get(lang, "#8b8478")
    stars = r.get("stargazers_count", 0)
    year = (r.get("pushed_at") or "")[:4]
    home = (r.get("homepage") or "").strip()
    title = pretty(name)
    meta_bits = []
    if lang:
        meta_bits.append(f'<span class="lang"><i style="background:{color}"></i>{H.escape(lang)}</span>')
    if stars:
        meta_bits.append(f'<span class="star">★ {stars}</span>')
    if year:
        meta_bits.append(f'<span class="yr">{year}</span>')
    blurb = f'<p class="desc">{H.escape(desc)}</p>' if desc else ""
    gloss = f'<p class="gloss">{H.escape(extra)}</p>' if extra else ""
    meta_html = f'<div class="card-meta">{"".join(meta_bits)}</div>' if (meta_bits and name not in HIDE_META) else ""
    cards.append(f"""    <a class="card" href="{H.escape(r['html_url'])}" target="_blank" rel="noopener">
      <div class="card-top"><h2>{H.escape(title)}</h2><span class="arr">↗</span></div>
      {blurb}{gloss}
      {meta_html}
    </a>""")

GRID = "\n".join(cards)
count = len(cards)

NAV = """    <nav class="nav">
      <a href="/projects.html" class="active">dev projects</a>
      <a href="/topology.html">topology</a>
      <a href="/something-western.html">writing</a>
      <a href="/reading.html">reading</a>
      <a href="/work.html">creative</a>
      <a href="https://aidanjude.substack.com/" target="_blank" rel="noopener">substack ↗</a>
    </nav>"""

HTML = f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Aidan Jude — Dev Projects</title>
<meta name="description" content="Things I've built — AI on small hardware, language turned into data, and a handful of experiments."/>
<meta property="og:site_name" content="Aidan Jude"/><meta property="og:locale" content="en_US"/>
<meta property="og:type" content="website"/><meta property="og:url" content="https://aidanjude.vercel.app/projects.html"/>
<meta property="og:title" content="Aidan Jude — Dev Projects"/>
<meta property="og:description" content="Things I've built — AI on small hardware, language turned into data, and a handful of experiments."/>
<meta property="og:image" content="https://aidanjude.vercel.app/og/projects.png"/><meta property="og:image:secure_url" content="https://aidanjude.vercel.app/og/projects.png"/><meta property="og:image:type" content="image/png"/><meta property="og:image:width" content="1200"/><meta property="og:image:height" content="630"/><meta property="og:image:alt" content="Aidan Jude — Dev Projects"/>
<meta name="twitter:card" content="summary_large_image"/><meta name="twitter:title" content="Aidan Jude — Dev Projects"/><meta name="twitter:description" content="Things I've built — AI on small hardware, language turned into data."/><meta name="twitter:image" content="https://aidanjude.vercel.app/og/projects.png"/>
<meta name="theme-color" content="#f7f3ec"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Geist+Mono:wght@300;400;500&display=swap" rel="stylesheet"/>
<style>
:root{{--bg:#f7f3ec;--bg2:#efe9dd;--ink:#1c1814;--ink2:#544e44;--faint:#8b8478;--rule:rgba(60,50,40,.16);--accent:#7c4a3a}}
@media(prefers-color-scheme:dark){{:root{{--bg:#15120f;--bg2:#1d1916;--ink:#e9e3d5;--ink2:#b3aa9a;--faint:#7d766a;--rule:rgba(230,220,200,.16);--accent:#c98a6b}}}}
*{{margin:0;padding:0;box-sizing:border-box}}html{{-webkit-text-size-adjust:100%}}
body{{background:var(--bg);color:var(--ink);font-family:'EB Garamond',Georgia,serif;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;line-height:1.5}}
.page{{max-width:60rem;margin:0 auto;padding:32px 28px 14vh}}@media(max-width:560px){{.page{{padding:22px 20px 12vh}}}}
.site-header{{display:flex;justify-content:space-between;align-items:baseline;gap:16px;flex-wrap:wrap;margin-bottom:64px}}
.brand{{font-size:21px;font-weight:500;font-style:italic}}.brand a{{color:inherit;text-decoration:none}}
.nav{{display:flex;gap:20px;flex-wrap:wrap;font-family:'Geist Mono',monospace;font-size:12px;letter-spacing:.04em}}
.nav a{{color:var(--faint);text-decoration:none;transition:color .2s}}.nav a:hover{{color:var(--ink)}}
.nav a.active{{color:var(--ink);border-bottom:1px solid var(--rule)}}
.hero{{margin-bottom:52px;max-width:42rem}}
.hero .eyebrow{{font-family:'Geist Mono',monospace;font-size:12px;letter-spacing:.28em;text-transform:uppercase;color:var(--faint);margin-bottom:18px}}
.hero h1{{font-size:clamp(38px,8vw,60px);font-weight:600;font-style:italic;letter-spacing:-.02em;line-height:1.03}}
.hero p{{margin-top:20px;font-size:21px;color:var(--ink2);line-height:1.5;max-width:36rem}}
.grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}}@media(max-width:620px){{.grid{{grid-template-columns:1fr}}}}
.card{{display:flex;flex-direction:column;background:var(--bg2);border:1px solid var(--rule);border-radius:8px;padding:22px 22px 18px;text-decoration:none;color:inherit;transition:border-color .2s,transform .2s,box-shadow .2s}}
.card:hover{{border-color:var(--accent);transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.08)}}
.card-top{{display:flex;justify-content:space-between;align-items:baseline;gap:10px}}
.card h2{{font-size:23px;font-weight:600;font-style:italic;letter-spacing:-.01em;line-height:1.1}}
.card .arr{{font-family:'Geist Mono',monospace;font-size:15px;color:var(--faint);transition:color .2s}}.card:hover .arr{{color:var(--accent)}}
.card .desc{{margin-top:11px;font-size:17px;color:var(--ink2);line-height:1.5;flex:1}}
.card .gloss{{margin-top:7px;font-size:15px;font-style:italic;color:var(--faint);line-height:1.45}}
.card-meta{{margin-top:16px;display:flex;align-items:center;gap:15px;flex-wrap:wrap;font-family:'Geist Mono',monospace;font-size:12px;letter-spacing:.02em;color:var(--faint)}}
.card-meta .lang{{display:inline-flex;align-items:center;gap:6px}}.card-meta .lang i{{width:9px;height:9px;border-radius:50%;display:inline-block}}
.card-meta .live{{margin-left:auto;color:var(--accent);text-decoration:none}}.card-meta .live:hover{{text-decoration:underline}}
.foot{{margin-top:46px;font-family:'Geist Mono',monospace;font-size:12px;letter-spacing:.03em;color:var(--faint);display:flex;gap:8px;flex-wrap:wrap;align-items:baseline}}
.foot a{{color:var(--ink2);text-decoration:none;border-bottom:1px solid var(--rule)}}.foot a:hover{{color:var(--ink)}}
</style></head>
<body>
<div class="page">
  <header class="site-header">
    <span class="brand"><a href="/">Aidan&nbsp;Jude</a></span>
{NAV}
  </header>
  <section class="hero">
    <div class="eyebrow">Aidan Jude · GitHub</div>
    <h1>These are my dev projects.</h1>
    <p>Things I've built — voice assistants on Raspberry Pis, AI that watches a screen, and a long habit of turning books and language into data.</p>
  </section>
  <main class="grid">
{GRID}
  </main>
  <div class="foot">
    <span>{count} selected · the rest live on <a href="https://github.com/{USER}" target="_blank" rel="noopener">github.com/{USER} ↗</a></span>
  </div>
</div>
</body></html>"""

(out_dir / "projects.html").write_text(HTML, encoding="utf-8")
print(f"wrote {out_dir/'projects.html'} — {count} project cards")
for name in CURATED:
    if name in repos:
        r = repos[name]
        print(f"  · {name:<34} {r.get('language') or '-':<8} ★{r.get('stargazers_count',0)} {(r.get('pushed_at') or '')[:4]}")
