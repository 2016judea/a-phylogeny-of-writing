#!/usr/bin/env python3
"""Build the dev-projects page (projects.html) from a curated, hand-tuned list.

The page is intentionally NOT derived from the GitHub API: titles, descriptions,
years, and language mixes are all hand-curated (the API's pushed_at year and
one-line description don't match the editorial copy). So this is the source of
truth — edit PROJECTS below and re-run to regenerate.

Literary-analysis repos (Prose-Similarities, Quotable_NLP_Synset, Novel_NLP_Analyzer,
literature-mutations) live on the Research page (build via the site-page skill),
not here.

Usage: build_projects_page.py [out_dir]   # default: the site repo root (writes in place)
"""
import sys, pathlib

USER = "2016judea"
GH = f"https://github.com/{USER}"

# GitHub's language-bar colors, overridden where the site uses its own (Shell black,
# TypeScript lime — matching the rest of the site).
LANG_COLOR = {
    "Python": "#3572A5", "Shell": "#111111", "HTML": "#e34c26",
    "CSS": "#563d7c", "TypeScript": "#a3e635", "JavaScript": "#f1e05a",
}

# Curated, in display order (best / most representative first).
# langs: in display order. star/gloss optional.
PROJECTS = [
    dict(repo="tars-mini", title="Tars Mini", year="2026", langs=["Python", "Shell"],
         desc="TARS-inspired voice assistant for Raspberry Pi — wake word → Whisper → Claude → Piper TTS"),
    dict(repo="AI-screen-monitor-service", title="AI Screen Monitor Service", year="2025", langs=["Python"],
         desc="Running a local AI agent that is capable of answering questions related to your screen activity."),
    dict(repo="edge-ai-experiment", title="Edge AI Experiment", year="2025", langs=["Python"], star=1,
         desc="Running a lightweight AI model on a Raspberry Pi"),
    dict(repo="generative-ai-with-instagram", title="Generative AI with Instagram", year="2024",
         langs=["Python", "CSS", "HTML"],
         desc="This project joins the power of the GPT-4V LLM with the popular social media platform Instagram."),
    dict(repo="Physical-Therapy-Market-Analysis", title="Physical Therapy Market Analysis", year="2026",
         langs=["Python"],
         desc="Data pipeline to aggregate payer reimbursement data from Transparency in Coverage (TiC) machine-readable files. Filtered to PT-relevant CPT codes. For contract negotiation analysis."),
    dict(repo="a-phylogeny-of-writing", title="A Phylogeny of Writing", year="2026", langs=["HTML"],
         desc="Connected three years of journal entries and substack essays to Claude. Had it generate a toplogy of self.",
         gloss="This very site — three years of journals and essays, mapped."),
    dict(repo="small-group-mobile", title="Small Group Mobile", year="2023", langs=["TypeScript"],
         desc="An Expo / React Native mobile app for organizing and running small groups."),
    dict(repo="small-group-cdk", title="Small Group CDK", year="2023", langs=["TypeScript"],
         desc="The AWS CDK package — cloud infrastructure behind the Small Group app."),
    dict(repo="Single-Camera-Based-Package-Counting", title="Single-Camera Package Counting", year="2023",
         langs=["Python"],
         desc="Counts packages of varying types through a single camera-based visual interface."),
    dict(repo="Goodreads_Audiobook_Matchmaker", title="Goodreads Audiobook Matchmaker", year="2019",
         langs=["Python"],
         desc='Matches your Goodreads "want to read" shelf to downloadable audiobook links — a web crawler plus the Goodreads API.'),
    dict(repo="Spotify_User_Playlists", title="Spotify User Playlists", year="2019", langs=["Python"],
         desc="Views the playlists — and the songs in each — for any given Spotify user."),
    dict(repo="Referral_System", title="Referral System", year="2019", langs=["HTML", "Python", "JavaScript"],
         desc="A referral system built for The News Memo."),
    dict(repo="Quotable", title="Quotable", year="2019", langs=["Python"],
         desc="A bot that texts you quotes from favorite authors, scraped with BeautifulSoup."),
    dict(repo="DOW_Watchdog", title="DOW Watchdog", year="2018", langs=["Python"],
         desc="Monitors a selection of stocks and sends SMS alerts when they cross preset thresholds."),
]


def card(p):
    meta = "".join(
        f'<span class="lang"><i style="background:{LANG_COLOR.get(l, "#8b8478")}"></i>{l}</span>'
        for l in p["langs"])
    if p.get("star"):
        meta += f'<span class="star">★ {p["star"]}</span>'
    meta += f'<span class="yr">{p["year"]}</span>'
    descblock = f'<p class="desc">{p["desc"]}</p>'
    if p.get("gloss"):
        descblock += f'<p class="gloss">{p["gloss"]}</p>'
    return (f'    <a class="card" href="{GH}/{p["repo"]}" target="_blank" rel="noopener">\n'
            f'      <div class="card-top"><h2>{p["title"]}</h2><span class="arr">↗</span></div>\n'
            f'      {descblock}\n'
            f'      <div class="card-meta">{meta}</div>\n'
            f'    </a>')


GRID = "\n".join(card(p) for p in PROJECTS)

# Everything outside the card grid is static chrome (head/styles/Ubik hero/nav/footer).
# %%GRID%% is the only substitution — keep this template in sync with the page design.
TEMPLATE = r'''<!DOCTYPE html><html lang="en"><head>
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
:root{--bg:#f7f3ec;--bg2:#efe9dd;--ink:#1c1814;--ink2:#544e44;--faint:#8b8478;--rule:rgba(60,50,40,.16);--accent:#7c4a3a}
@media(prefers-color-scheme:dark){:root{--bg:#15120f;--bg2:#1d1916;--ink:#e9e3d5;--ink2:#b3aa9a;--faint:#7d766a;--rule:rgba(230,220,200,.16);--accent:#c98a6b}}
*{margin:0;padding:0;box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{background:var(--bg);color:var(--ink);font-family:'EB Garamond',Georgia,serif;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;line-height:1.5}
.page{max-width:60rem;margin:0 auto;padding:32px 28px 14vh}@media(max-width:560px){.page{padding:22px 20px 12vh}}
.site-header{display:flex;justify-content:space-between;align-items:baseline;gap:16px;flex-wrap:wrap;margin-bottom:64px}
.brand{font-size:21px;font-weight:500;font-style:italic}.brand a{color:inherit;text-decoration:none}
.nav{display:flex;gap:20px;flex-wrap:wrap;font-family:'Geist Mono',monospace;font-size:12px;letter-spacing:.04em}
.nav a{color:var(--faint);text-decoration:none;transition:color .2s}.nav a:hover{color:var(--ink)}
.nav a.active{color:var(--ink);border-bottom:1px solid var(--rule)}
html,body{overflow-x:clip}
/* Ubik hero — full-bleed band washed in the art's own colors, with a framed plate */
.ubik-band{position:relative;width:100vw;margin-left:calc(50% - 50vw);margin-bottom:52px;
  background:
    radial-gradient(70% 130% at 86% 20%, rgba(230,150,54,.26), rgba(230,150,54,0) 58%),
    radial-gradient(66% 120% at 8% 98%, rgba(45,104,101,.22), rgba(45,104,101,0) 60%),
    var(--bg2);
  border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}
.ubik-inner{max-width:60rem;margin:0 auto;padding:46px 28px;display:grid;grid-template-columns:1.15fr .85fr;gap:48px;align-items:center}
.ubik-inner .eyebrow{font-family:'Geist Mono',monospace;font-size:12px;letter-spacing:.28em;text-transform:uppercase;color:var(--faint);margin-bottom:18px}
.ubik-inner h1{font-size:clamp(38px,8vw,60px);font-weight:600;font-style:italic;letter-spacing:-.02em;line-height:1.03}
.ubik-inner p.lede{margin-top:20px;font-size:21px;color:var(--ink2);line-height:1.5;max-width:34rem}
.ubik-fig{margin:0;justify-self:center;width:100%;max-width:340px}
.plate{margin:0;background:#fbf8f1;padding:13px;border:1px solid var(--rule);border-radius:4px;box-shadow:0 22px 54px rgba(20,12,4,.24),0 2px 6px rgba(20,12,4,.12)}
.plate img{width:100%;height:auto;display:block;border-radius:2px}
.plate-cap{margin-top:12px;text-align:center;font-family:'Geist Mono',monospace;font-size:11px;letter-spacing:.04em;color:var(--faint);line-height:1.5}
.plate-cap em{font-family:'EB Garamond',Georgia,serif;font-style:italic;letter-spacing:0}
@media(prefers-color-scheme:dark){.plate{background:#211d18}}
@media(max-width:680px){.ubik-inner{grid-template-columns:1fr;gap:28px;padding:34px 24px}.ubik-fig{max-width:330px;margin:6px auto 0}}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}@media(max-width:620px){.grid{grid-template-columns:1fr}}
.card{display:flex;flex-direction:column;background:var(--bg2);border:1px solid var(--rule);border-radius:8px;padding:22px 22px 18px;text-decoration:none;color:inherit;transition:border-color .2s,transform .2s,box-shadow .2s}
.card:hover{border-color:var(--accent);transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.08)}
.card-top{display:flex;justify-content:space-between;align-items:baseline;gap:10px}
.card h2{font-size:23px;font-weight:600;font-style:italic;letter-spacing:-.01em;line-height:1.1}
.card .arr{font-family:'Geist Mono',monospace;font-size:15px;color:var(--faint);transition:color .2s}.card:hover .arr{color:var(--accent)}
.card .desc{margin-top:11px;font-size:17px;color:var(--ink2);line-height:1.5;flex:1}
.card .gloss{margin-top:7px;font-size:15px;font-style:italic;color:var(--faint);line-height:1.45}
.card-meta{margin-top:16px;display:flex;align-items:center;gap:15px;flex-wrap:wrap;font-family:'Geist Mono',monospace;font-size:12px;letter-spacing:.02em;color:var(--faint)}
.card-meta .lang{display:inline-flex;align-items:center;gap:6px}.card-meta .lang i{width:10px;height:10px;border-radius:50%;display:inline-block;box-shadow:0 0 0 1px rgba(120,120,120,.35)}
.card-meta .live{margin-left:auto;color:var(--accent);text-decoration:none}.card-meta .live:hover{text-decoration:underline}
.foot{margin-top:46px;font-family:'Geist Mono',monospace;font-size:12px;letter-spacing:.03em;color:var(--faint);display:flex;gap:8px;flex-wrap:wrap;align-items:baseline}
.foot a{color:var(--ink2);text-decoration:none;border-bottom:1px solid var(--rule)}.foot a:hover{color:var(--ink)}
</style></head>
<body>
<div class="page">
  <header class="site-header">
    <span class="brand"><a href="/">Aidan&nbsp;Jude</a></span>
    <nav class="nav">
      <a href="/projects.html" class="active">dev projects</a>
      <a href="/research.html">research</a>
      <a href="/topology.html">topology</a>
      <a href="/something-western.html">novel</a>
      <a href="/reading.html">reading</a>
      <a href="/study.html">study</a>
      <a href="/essays.html">essays</a>
      <a href="/photography.html">35mm photography</a>
    </nav>
  </header>
  <section class="ubik-band">
    <div class="ubik-inner">
      <div>
        <div class="eyebrow">Aidan Jude · GitHub</div>
        <h1>These are my dev projects.</h1>
        <p class="lede">Things I've built — voice assistants on Raspberry Pis, AI that watches a screen, and a long habit of turning books and language into data.</p>
      </div>
      <figure class="ubik-fig">
        <div class="plate"><img src="/img/ubik.webp" width="739" height="889" alt="Bob Pepper's cover illustration for Philip K. Dick's Ubik — a skeleton with a television-screen face holding a spray can labeled UBIK." loading="eager"/></div>
        <figcaption class="plate-cap">Bob Pepper · cover art for Philip&nbsp;K.&nbsp;Dick's <em>Ubik</em></figcaption>
      </figure>
    </div>
  </section>
  <main class="grid">
%%GRID%%
  </main>
  <div class="foot">
    <span>My literary-analysis work lives on the <a href="/research.html">research page</a> · all of it on <a href="https://github.com/2016judea" target="_blank" rel="noopener">github.com/2016judea ↗</a></span>
  </div>
</div>
</body></html>'''

HTML = TEMPLATE.replace("%%GRID%%", GRID)

out_dir = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parents[2]
dest = out_dir / "projects.html"
dest.write_text(HTML, encoding="utf-8")
print(f"wrote {dest} — {len(PROJECTS)} project cards")
