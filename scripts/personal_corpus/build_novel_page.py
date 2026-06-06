#!/usr/bin/env python3
"""Render arranged 'Something Western' -> phone-first reading page: full dreams, numbered
sections, contents drawer, auto-resume."""
import re, html as H
def read(p): return open(p, encoding="utf-8").read()
plots={n:re.sub(r"^\s*##\s*Plot\s*\d+\s*\n","",read(f"/tmp/sw_plot/Plot_{n}.md")).strip() for n in range(1,8)}
ca="Will smiled to himself once more and closed the door."; i=plots[7].find(ca); plots[7]=plots[7][:i+len(ca)]
weave=[("as the day began. Had already begun.","Chasing Comets"),("bring about the end of day and the provinces of night.","Traveling Prophet"),("hungry as all hell.","A Stone Slab"),("knew each other meant it.","Mountainside with Her"),("the restlessness that shook his soul through the passing of days.","Howl"),("to thank me for brother.","Actuated Wanderings"),("Dumb question bud.","A Higher Power"),("followed closely behind. Watching the skies.","Woman in the Woods"),("as they eased out onto the county road.","Farewell"),("said Teddy with grin and they both laughed.","Across the Creosote")]
dreams={t:re.sub(r"^\s*##\s*.*?\n","",read(f"/tmp/sw_dreams/{t}.md")).strip() for _,t in weave}
anchor_dream={a:t for a,t in weave}

def inline(s):
    s=H.escape(s)
    s=re.sub(r"\*\*(.+?)\*\*", r'<span class="lead">\1</span>', s)
    s=re.sub(r"(?<!\w)_(.+?)_(?!\w)", r"<em>\1</em>", s)
    s=re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", s)
    return s
def is_div(p): return bool(re.fullmatch(r"[\s*\-–—·]+", p))
def paras(text): return [x.strip() for x in re.split(r"\n\s*\n", text) if x.strip()]
def leadify(blk):
    """Wrap a scene-opener's first few words in a full-caps lead span (2-5 words,
    stopping at the first natural break) — matches Aidan's manual **OPENERS**."""
    pre=""
    if blk[:1] in "_*" and blk[1:2] not in "_* ":  # keep a leading italic marker outside the caps
        pre=blk[0]; blk=blk[1:]
    words=blk.split()
    n=min(5,len(words))
    for i,w in enumerate(words):
        if i>=2 and (w.endswith((",",".",";",":","—","!","?")) or i+1>=5):
            n=i+1; break
    head=" ".join(words[:n]); tail=" ".join(words[n:])
    return pre+f"**{head}**"+(" "+tail if tail else "")

plot_full="\n\n".join(plots[n] for n in range(1,8))
plot_full=re.sub(r"(?m)^[ \t]*([*\-]\s*){3,}[ \t]*$","\n* * *\n",plot_full)

out=[]; toc=[]; sec=0; first=True; open_sec=False; placed=set()
def close():
    global open_sec
    if open_sec: out.append("</section>"); open_sec=False
def opensec(snippet):
    global sec,open_sec
    sec+=1; out.append(f'<section id="s{sec}" data-n="{sec}">'); open_sec=True
    toc.append(("scene",sec,snippet))

for blk in paras(plot_full):
    if blk=="* * *" or is_div(blk):
        close(); out.append('<div class="dinkus">·&nbsp;&nbsp;·&nbsp;&nbsp;·</div>'); continue
    # journal
    if blk.startswith("**March 13, 1959**") or "March 13, 1959" in blk[:30]:
        close(); body=blk.replace("**March 13, 1959**","").strip()
        jp="".join(f"<p>{inline(x)}</p>" for x in paras(body))
        out.append(f'<div class="journal"><div class="journal-date">March 13, 1959</div>{jp}</div>'); continue
    sec_opener=False
    if not open_sec:
        snip=re.sub(r"[*_]","",re.sub(r"\*\*.+?\*\*","",blk)).strip()
        opensec(" ".join(snip.split()[:6])); sec_opener=True
    content=blk
    if sec_opener and not blk.lstrip().startswith("**") and not blk.lstrip().startswith('"'):
        content=leadify(blk)
    cls=' class="drop"' if first else ""
    out.append(f"<p{cls}>{inline(content)}</p>"); first=False
    # dream after this paragraph? (tolerate a trailing quote/space after the anchor)
    for anc,title in anchor_dream.items():
        if title not in placed and anc in blk[-(len(anc)+5):]:
            placed.add(title); close()
            dp="".join(f"<p>{inline(x)}</p>" for x in paras(dreams[title]))
            did=f"d{len([t for t in toc if t[0]=='dream'])+1}"
            out.append(f'<div class="dream" id="{did}"><h3>{H.escape(title)}</h3>{dp}</div>')
            toc.append(("dream",did,title))
            break
close()
missing=[t for _,t in weave if t not in placed]
assert not missing, f"dreams not placed: {missing}"
BODY="\n".join(out)
words=len(re.sub(r"<[^>]+>","",BODY).split()); mins=round(words/235)
TOC="".join(
 (f'<a href="#s{n}" class="toc-s"><span class="toc-n">{n}</span><span class="toc-t">{H.escape(lab)}…</span></a>'
  if kind=="scene" else
  f'<a href="#{n}" class="toc-d"><span class="toc-n">✶</span><span class="toc-t"><em>{H.escape(lab)}</em></span></a>')
 for kind,n,lab in toc)
nsec=sec

HTML=f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Something Western — Aidan Jude</title>
<meta name="description" content="A novel. Two young men, one Texas summer, 1959 — and the question of what else is out there."/>
<meta property="og:site_name" content="Aidan Jude"/><meta property="og:locale" content="en_US"/>
<meta property="og:type" content="book"/><meta property="og:url" content="https://aidanjude.vercel.app/something-western.html"/>
<meta property="og:title" content="Something Western"/><meta property="og:description" content="A novel by Aidan Jude — two young men, one Texas summer, 1959. And the question of what else is out there."/>
<meta property="og:image" content="https://aidanjude.vercel.app/og/something-western.png"/><meta property="og:image:secure_url" content="https://aidanjude.vercel.app/og/something-western.png"/><meta property="og:image:type" content="image/png"/><meta property="og:image:width" content="1200"/><meta property="og:image:height" content="630"/><meta property="og:image:alt" content="Something Western — a novel by Aidan Jude"/>
<meta name="twitter:card" content="summary_large_image"/><meta name="twitter:title" content="Something Western"/><meta name="twitter:description" content="A novel by Aidan Jude — two young men, one Texas summer, 1959."/><meta name="twitter:image" content="https://aidanjude.vercel.app/og/something-western.png"/>
<meta name="theme-color" content="#f7f3ec"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Geist+Mono:wght@300;400&display=swap" rel="stylesheet"/>
<style>
:root{{--bg:#f7f3ec;--bg2:#efe9dd;--ink:#1c1814;--ink2:#544e44;--faint:#8b8478;--rule:rgba(60,50,40,.16);--accent:#7c4a3a}}
@media(prefers-color-scheme:dark){{:root{{--bg:#15120f;--bg2:#1c1815;--ink:#e9e3d5;--ink2:#b3aa9a;--faint:#7d766a;--rule:rgba(230,220,200,.16);--accent:#c98a6b}}}}
*{{margin:0;padding:0;box-sizing:border-box}}html{{-webkit-text-size-adjust:100%;scroll-behavior:smooth}}
body{{background:var(--bg);color:var(--ink);font-family:'EB Garamond',Georgia,serif;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}}
#bar{{position:fixed;top:0;left:0;height:2px;width:0;background:var(--accent);z-index:50;transition:width .1s}}
.top{{position:fixed;top:0;left:0;right:0;display:flex;justify-content:space-between;align-items:center;padding:11px 18px;font-family:'Geist Mono',monospace;font-size:11px;letter-spacing:.04em;color:var(--faint);background:linear-gradient(var(--bg),var(--bg) 70%,transparent);z-index:40}}
.top a{{color:var(--ink2);text-decoration:none}}.top a:hover{{color:var(--ink)}}
#here{{color:var(--faint)}}
.wrap{{max-width:34rem;margin:0 auto;padding:0 24px 20vh}}@media(max-width:480px){{.wrap{{padding:0 22px 18vh}}}}
.cover{{min-height:84vh;display:flex;flex-direction:column;justify-content:center;text-align:center;padding-top:8vh}}
.cover .kicker{{font-family:'Geist Mono',monospace;font-size:11px;letter-spacing:.34em;text-transform:uppercase;color:var(--faint);margin-bottom:26px}}
.cover h1{{font-size:clamp(40px,12vw,64px);font-weight:600;font-style:italic;letter-spacing:-.02em;line-height:1.04}}
.cover .by{{margin-top:22px;font-size:19px;color:var(--ink2)}}.cover .by b{{font-weight:500;font-style:italic;color:var(--ink)}}
.cover .meta{{margin-top:30px;font-family:'Geist Mono',monospace;font-size:11px;letter-spacing:.08em;color:var(--faint)}}
.cover .scroll{{margin-top:42px;font-family:'Geist Mono',monospace;font-size:11px;color:var(--faint);animation:fade 2.4s ease-in-out infinite}}@keyframes fade{{0%,100%{{opacity:.35}}50%{{opacity:.9}}}}
.cover-nav{{display:flex;flex-wrap:wrap;justify-content:center;gap:18px;margin-bottom:40px;font-family:'Geist Mono',monospace;font-size:11px;letter-spacing:.06em}}
.cover-nav a{{color:var(--faint);text-decoration:none;transition:color .2s}}.cover-nav a:hover{{color:var(--ink2)}}.cover-nav a.active{{color:var(--ink2);border-bottom:1px solid var(--rule)}}
.text{{font-size:20.5px;line-height:1.82}}@media(max-width:480px){{.text{{font-size:19.5px;line-height:1.8}}}}
.text p{{margin:0;text-indent:1.35em;hanging-punctuation:first}}
.text section{{scroll-margin-top:54px}}
p.drop:first-letter{{initial-letter:2.6;font-weight:600;margin-right:.06em;color:var(--accent)}}p.drop{{text-indent:0}}
.dinkus{{text-align:center;color:var(--faint);letter-spacing:.5em;margin:2.2em 0;font-size:14px;user-select:none}}
.lead{{text-transform:uppercase;letter-spacing:.05em;font-weight:500}}em{{font-style:italic}}
.journal{{margin:2.4em 0;padding:1.3em 1.4em;background:var(--bg2);border-left:2px solid var(--rule);border-radius:3px}}
.journal-date{{font-family:'Geist Mono',monospace;font-size:11px;letter-spacing:.12em;color:var(--faint);margin-bottom:.7em}}
.journal p{{font-style:italic;text-indent:0;color:var(--ink2);font-size:18.5px;line-height:1.7}}.journal p+p{{margin-top:.7em}}
.dream{{margin:3.4em 0;scroll-margin-top:54px}}
.dream:before,.dream:after{{content:"·  ·  ·";display:block;text-align:center;color:var(--faint);letter-spacing:.4em;font-size:13px}}.dream:before{{margin-bottom:1.7em}}.dream:after{{margin-top:1.7em}}
.dream h3{{text-align:center;font-style:italic;font-weight:500;font-size:23px;margin-bottom:1.1em;letter-spacing:-.01em;color:var(--ink)}}
.dream p{{font-style:italic;color:var(--ink2);text-indent:1.2em;font-size:19.5px;line-height:1.78}}.dream p:first-of-type{{text-indent:0}}
.end{{text-align:center;margin:5em 0 0;font-family:'Geist Mono',monospace;font-size:11px;letter-spacing:.2em;color:var(--faint)}}
.colophon{{text-align:center;margin-top:2.4em;font-size:18px;font-style:italic;color:var(--ink2)}}.colophon a{{color:var(--ink);border-bottom:1px solid var(--rule);text-decoration:none}}
#menu{{position:fixed;bottom:20px;right:18px;z-index:45;width:46px;height:46px;border-radius:50%;background:var(--bg);border:1px solid var(--rule);color:var(--ink2);font-size:19px;cursor:pointer;box-shadow:0 4px 16px rgba(0,0,0,.12)}}
#resume{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%) translateY(80px);z-index:45;background:var(--accent);color:#fff;font-family:'Geist Mono',monospace;font-size:12px;letter-spacing:.03em;padding:11px 18px;border-radius:999px;border:none;cursor:pointer;box-shadow:0 6px 20px rgba(0,0,0,.22);transition:transform .3s;opacity:.96}}
#resume.show{{transform:translateX(-50%) translateY(0)}}
#drawer{{position:fixed;inset:0;z-index:60;background:var(--bg);opacity:0;pointer-events:none;transition:opacity .2s;overflow-y:auto;padding:64px 22px 40px}}
#drawer.open{{opacity:1;pointer-events:auto}}
#drawer .dhead{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:22px;font-family:'Geist Mono',monospace;font-size:11px;letter-spacing:.1em;color:var(--faint);text-transform:uppercase}}
#drawer .dclose{{background:none;border:none;color:var(--ink2);font-size:22px;cursor:pointer;line-height:1}}
#drawer a{{display:flex;gap:13px;align-items:baseline;padding:9px 4px;text-decoration:none;border-bottom:1px solid var(--rule);color:var(--ink2)}}
#drawer a:hover{{color:var(--ink)}}#drawer .toc-n{{font-family:'Geist Mono',monospace;font-size:12px;color:var(--faint);min-width:20px;text-align:right}}
#drawer .toc-t{{font-size:17px}}#drawer .toc-d .toc-n{{color:var(--accent)}}
#drawer .dsite{{margin-top:28px;padding-top:18px;border-top:1px solid var(--rule);display:flex;flex-wrap:wrap;gap:18px;font-family:'Geist Mono',monospace;font-size:12px;letter-spacing:.04em}}
#drawer .dsite a{{display:inline;padding:0;border:none;color:var(--faint)}}#drawer .dsite a:hover{{color:var(--ink)}}#drawer .dsite a.active{{color:var(--ink2)}}
</style></head>
<body>
<div id="bar"></div>
<div class="top"><a href="/">← Aidan</a><span id="here">Something Western</span></div>
<div class="wrap">
  <header class="cover">
    <nav class="cover-nav">
      <a href="/projects.html">dev projects</a>
      <a href="/topology.html">topology</a>
      <a href="/something-western.html" class="active">writing</a>
      <a href="/reading.html">reading</a>
      <a href="/work.html">creative</a>
      <a href="https://aidanjude.substack.com/" target="_blank" rel="noopener">substack ↗</a>
    </nav>
    <div class="kicker">a novel</div><h1>Something&nbsp;Western</h1>
    <div class="by">by <b>Aidan Jude</b></div>
    <div class="meta">Texas · 1959 · written 2023–24 · ≈{words//1000}k words · ~{mins} min · {nsec} sections</div>
    <div class="scroll">scroll to begin ↓</div>
  </header>
  <main class="text">
{BODY}
    <div class="end">· · ·</div>
    <p class="colophon">Thanks for reading. — Aidan · <a href="/">aidanjude.vercel.app</a></p>
  </main>
</div>
<button id="menu" aria-label="contents">☰</button>
<button id="resume">resume where you left off ↓</button>
<nav id="drawer"><div class="dhead"><span>Something Western · contents</span><button class="dclose" aria-label="close">×</button></div>{TOC}<div class="dsite"><a href="/projects.html">dev projects</a><a href="/topology.html">topology</a><a href="/something-western.html" class="active">writing</a><a href="/reading.html">reading</a><a href="/work.html">creative</a><a href="https://aidanjude.substack.com/" target="_blank" rel="noopener">substack ↗</a></div></nav>
<script>
const KEY='sw-pos';const bar=document.getElementById('bar'),here=document.getElementById('here');
const secs=[...document.querySelectorAll('main section, .dream')];
function curLabel(){{let c=null;for(const s of secs){{if(s.getBoundingClientRect().top<80)c=s;}}if(!c)return'Something Western';return c.classList.contains('dream')?'✶ '+c.querySelector('h3').textContent:'§ '+c.dataset.n;}}
let t;addEventListener('scroll',()=>{{const h=document.documentElement;const p=h.scrollTop/(h.scrollHeight-h.clientHeight);bar.style.width=(p*100)+'%';here.textContent=curLabel();clearTimeout(t);t=setTimeout(()=>localStorage.setItem(KEY,h.scrollTop),250);}},{{passive:true}});
// resume
const saved=parseInt(localStorage.getItem(KEY)||'0',10);
if(saved>600){{const r=document.getElementById('resume');r.classList.add('show');r.onclick=()=>{{scrollTo({{top:saved,behavior:'smooth'}});r.classList.remove('show');}};addEventListener('scroll',()=>r.classList.remove('show'),{{once:true,passive:true}});setTimeout(()=>r.classList.remove('show'),9000);}}
// drawer
const dr=document.getElementById('drawer');
document.getElementById('menu').onclick=()=>dr.classList.add('open');
dr.querySelector('.dclose').onclick=()=>dr.classList.remove('open');
dr.querySelectorAll('a').forEach(a=>a.onclick=()=>dr.classList.remove('open'));
</script></body></html>"""
open("/tmp/phylo/something-western.html","w",encoding="utf-8").write(HTML)
ndr=len([t for t in toc if t[0]=='dream'])
print(f"words {words} | sections {nsec} | dreams {ndr}")
# verify full dreams present
import sys
ac=re.search(r'<h3>Across the Creosote</h3>(.*?)</div>\s*<', HTML, re.S)
print("Across the Creosote rendered words:", len(re.sub('<[^>]+>','',ac.group(1)).split()) if ac else "NOT FOUND", "(source has 1384)")
