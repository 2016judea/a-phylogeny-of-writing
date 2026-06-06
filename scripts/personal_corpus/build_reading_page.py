#!/usr/bin/env python3
"""Generate reading.html — the reading-interest progression streamgraph — for the
a-phylogeny-of-writing Vercel site. Embeds the theme matrix so the page is fully
static (no fetch). Matches the existing site's warm editorial aesthetic.

    python3 scripts/personal_corpus/build_reading_page.py /tmp/phylo/reading.html
"""
import json
import sys

DATA = json.load(open("data/personal_corpus/themes_by_year.json"))
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/phylo/reading.html"

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Reading Topology — Aidan</title>
  <meta name="description" content="An intellectual progression, 2014–2026 — how the reading moved, year by year, thread by thread." />
  <meta property="og:title" content="Reading Topology — Aidan" />
  <meta property="og:description" content="An intellectual progression, 2014–2026" />
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
    .site-header{margin-bottom:56px;display:flex;justify-content:space-between;
      align-items:baseline;gap:16px;flex-wrap:wrap}
    .brand{font-size:21px;font-weight:500;font-style:italic;letter-spacing:-.01em}
    .brand a{color:inherit;text-decoration:none}
    .nav{display:flex;gap:22px;font-family:'Geist Mono',monospace;font-size:12px;letter-spacing:.04em}
    .nav a{color:var(--text-secondary);text-decoration:none;transition:color .2s}
    .nav a:hover{color:var(--text-primary)}
    .nav a.active{color:var(--text-primary);border-bottom:1px solid var(--border-secondary)}
    .topology-header{padding:0 4px 10px;display:flex;align-items:baseline;
      justify-content:space-between;gap:16px;flex-wrap:wrap}
    .header-left{display:flex;flex-direction:column;gap:2px}
    .header-eyebrow{font-family:'Geist Mono',monospace;font-size:11px;
      color:var(--text-tertiary);letter-spacing:.12em;text-transform:lowercase}
    .header-title{font-size:24px;font-style:italic;letter-spacing:-.01em}
    .header-stats{font-family:'Geist Mono',monospace;font-size:11px;
      color:var(--text-tertiary);letter-spacing:.04em;text-align:right}
    .lede{max-width:62ch;margin:14px 4px 22px;font-size:17.5px;line-height:1.55;
      color:var(--text-secondary)}
    .lede b{color:var(--text-primary);font-weight:600}
    .chart-wrap{position:relative;border:1px solid var(--border-tertiary);
      border-radius:4px;background:var(--bg-secondary);padding:10px 6px 4px}
    svg{display:block;width:100%;height:auto;overflow:visible}
    .yr{font-family:'Geist Mono',monospace;font-size:10px;fill:var(--text-tertiary)}
    .mile-label{font-family:'Geist Mono',monospace;font-size:9.5px;fill:var(--text-tertiary)}
    .band{cursor:pointer;transition:opacity .18s}
    .legend{display:flex;flex-wrap:wrap;gap:6px 16px;margin:18px 4px 0;
      font-family:'Geist Mono',monospace;font-size:11.5px}
    .lg{display:flex;align-items:center;gap:7px;cursor:pointer;color:var(--text-secondary);
      padding:2px 0;transition:color .15s}
    .lg:hover{color:var(--text-primary)}
    .sw{width:11px;height:11px;border-radius:2px;flex:0 0 auto}
    .lg .n{font-family:'EB Garamond',serif;font-size:14px}
    .lg .c{color:var(--text-tertiary);font-size:10.5px}
    #tip{position:absolute;pointer-events:none;opacity:0;transition:opacity .12s;
      background:var(--bg-primary);border:1px solid var(--border-secondary);
      border-radius:4px;padding:10px 12px;max-width:280px;z-index:5;
      box-shadow:0 6px 24px rgba(0,0,0,.14)}
    #tip .tt{font-style:italic;font-size:16px;margin-bottom:2px}
    #tip .tm{font-family:'Geist Mono',monospace;font-size:10.5px;color:var(--text-tertiary);
      letter-spacing:.03em;margin-bottom:7px}
    #tip .ex{font-size:13px;line-height:1.45;color:var(--text-secondary)}
    .movements{margin-top:54px;border-top:1px solid var(--border-tertiary);padding-top:30px}
    .movements h2{font-size:13px;font-family:'Geist Mono',monospace;letter-spacing:.1em;
      text-transform:lowercase;color:var(--text-tertiary);margin-bottom:18px}
    .mv{display:grid;grid-template-columns:88px 1fr;gap:14px 20px;margin-bottom:14px;
      align-items:baseline}
    @media (max-width:560px){.mv{grid-template-columns:1fr;gap:2px 0;margin-bottom:18px}}
    .mv .yr2{font-family:'Geist Mono',monospace;font-size:12px;color:var(--text-tertiary)}
    .mv .tx{font-size:16.5px;line-height:1.5}
    .mv .tx b{font-weight:600}
    .site-footer{margin-top:60px;padding-top:18px;border-top:1px solid var(--border-tertiary);
      font-family:'Geist Mono',monospace;font-size:11px;color:var(--text-tertiary);
      letter-spacing:.03em;line-height:1.7}
    .site-footer a{color:var(--text-secondary);text-decoration:none}
    .site-footer a:hover{color:var(--text-primary)}
  </style>
</head>
<body>
  <div class="page">
    <header class="site-header">
      <div class="brand"><a href="/">Aidan</a></div>
      <nav class="nav">
        <a href="/">topology</a>
        <a href="/reading.html" class="active">reading</a>
        <a href="https://aidanjude.substack.com/" target="_blank" rel="noopener">substack ↗</a>
      </nav>
    </header>
    <main>
      <div class="topology-header">
        <div class="header-left">
          <span class="header-eyebrow">reading topology</span>
          <span class="header-title">an intellectual progression, 2014–2026</span>
        </div>
        <div class="header-stats" id="stats"></div>
      </div>
      <p class="lede">Every band is a thread of interest; its thickness is how many books I
        read in that vein that year. Read left to right and you can watch the mind move —
        from <b>adventure</b> into the <b>American canon</b>, down through
        <b>philosophy</b> and <b>McCarthy's grit</b>, and out toward
        <b>poetry, the sacred, and first principles</b>. Hover a band for the books in it.</p>
      <div class="chart-wrap">
        <svg id="svg" viewBox="0 0 1000 560" preserveAspectRatio="xMidYMid meet" role="img"
             aria-label="Streamgraph of reading interests by year, 2014 to 2026"></svg>
        <div id="tip"></div>
      </div>
      <div class="legend" id="legend"></div>

      <section class="movements">
        <h2>the movements</h2>
        <div class="mv"><span class="yr2">2014</span><span class="tx"><b>Story.</b> Boyhood adventure — the whole of Ranger's Apprentice. Reading for what happens next.</span></div>
        <div class="mv"><span class="yr2">2018–19</span><span class="tx"><b>Style.</b> The gateway (dystopia + pop-science) opens onto the American canon and a wall of Romantic poetry. 80 books in 2019 — aesthetic immersion.</span></div>
        <div class="mv"><span class="yr2">2020–22</span><span class="tx"><b>Ideas.</b> Modernism makes difficulty the reward; then philosophy, political economy, and Cormac McCarthy's metaphysical violence. The argument under the narrative.</span></div>
        <div class="mv"><span class="yr2">2023–24</span><span class="tx"><b>Meaning.</b> Craft, faith, and form — On Writing, Moby-Dick, Flannery O'Connor, Frankl; then noir and the philosophy of mind. The <b>Substack begins (Jan '23)</b> — the private reader goes public, and keeps a monthly dispatch running ever since.</span></div>
        <div class="mv"><span class="yr2">2025–26</span><span class="tx"><b>Practice.</b> Stoicism, Zen, Rubin's <i>The Creative Act</i> — and Socrates. Reading to live and make, not only to know.</span></div>
      </section>
    </main>
    <footer class="site-footer">
      __TOTALS__ · built with inline svg · no tracking ·
      <a href="https://github.com/2016judea/a-phylogeny-of-writing" target="_blank" rel="noopener">view source</a> ·
      a companion to the <a href="/">writing topology</a>
    </footer>
  </div>

  <script>
  const DATA = __DATA__;
  (function(){
    const years = DATA.years, threads = DATA.threads;
    const N = years.length;
    document.getElementById('stats').textContent =
      DATA.totals.books + ' books · ' + DATA.totals.threads + ' threads · ' + years[0] + '–' + years[N-1];

    const VB={w:1000,h:560}, m={l:34,r:20,t:46,b:34};
    const plotW=VB.w-m.l-m.r, plotH=VB.h-m.t-m.b;
    const X=i=>m.l+(N===1?0:i/(N-1)*plotW);
    let maxStack=0;
    for(let i=0;i<N;i++){let s=0;for(const t of threads)s+=t.counts[i];if(s>maxStack)maxStack=s;}
    const k=plotH/maxStack, midY=m.t+plotH/2;

    // silhouette baseline: center each year's stack on midY
    const lower=threads.map(()=>new Array(N)), upper=threads.map(()=>new Array(N));
    for(let i=0;i<N;i++){
      let sum=0;for(const t of threads)sum+=t.counts[i];
      let y=midY-(sum*k)/2;
      for(let b=0;b<threads.length;b++){
        lower[b][i]=y; y+=threads[b].counts[i]*k; upper[b][i]=y;
      }
    }
    // Catmull-Rom -> smooth path through (X(i), arr[i]) points
    function spline(arr,rev){
      const pts=[];for(let i=0;i<N;i++)pts.push([X(i),arr[i]]);
      if(rev)pts.reverse();
      let d='';
      for(let i=0;i<pts.length;i++){
        const [x,y]=pts[i];
        if(i===0){d+='L'+x.toFixed(1)+' '+y.toFixed(1);continue;}
        const p0=pts[i-1],p1=pts[i],p2=pts[i+1]||pts[i],pm=pts[i-2]||pts[i-1];
        const c1x=p0[0]+(p1[0]-pm[0])/6,c1y=p0[1]+(p1[1]-pm[1])/6;
        const c2x=p1[0]-(p2[0]-p0[0])/6,c2y=p1[1]-(p2[1]-p0[1])/6;
        d+='C'+c1x.toFixed(1)+' '+c1y.toFixed(1)+','+c2x.toFixed(1)+' '+c2y.toFixed(1)+','+p1[0].toFixed(1)+' '+p1[1].toFixed(1);
      }
      return d;
    }
    const NS='http://www.w3.org/2000/svg';
    const svg=document.getElementById('svg');
    function el(n,a){const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);return e;}

    // milestone vertical ticks (stagger labels so neighbours don't collide)
    DATA.milestones.forEach((ms,mi)=>{
      const i=years.indexOf(ms.year); if(i<0)return; const x=X(i);
      const ly=(mi%2===0)? m.t-26 : m.t-12;
      svg.appendChild(el('line',{x1:x,y1:ly+4,x2:x,y2:m.t+plotH+6,stroke:'var(--border-tertiary)','stroke-dasharray':'2 4'}));
      const anchor = i>=N-2 ? 'end' : (i<=1 ? 'start' : 'middle');
      const tl=el('text',{x:x,y:ly,class:'mile-label','text-anchor':anchor});tl.textContent=ms.label;svg.appendChild(tl);
    });
    // year axis
    years.forEach((y,i)=>{
      if(N>10 && (y%2!==0) && y!==years[N-1] && y!==years[0])return;
      const t=el('text',{x:X(i),y:m.t+plotH+20,class:'yr','text-anchor':'middle'});t.textContent="’"+String(y).slice(2);svg.appendChild(t);
    });

    const tip=document.getElementById('tip'), wrap=svg.parentElement;
    const bands=[];
    threads.forEach((t,b)=>{
      const d='M'+X(0)+' '+upper[b][0].toFixed(1)+spline(upper[b],false).slice(1)
              +'L'+X(N-1)+' '+lower[b][N-1].toFixed(1)+spline(lower[b],true).slice(1)+'Z';
      const p=el('path',{d:d,fill:t.color,class:'band','fill-opacity':.92,stroke:'var(--bg-secondary)','stroke-width':.6});
      const peak=t.counts.indexOf(Math.max(...t.counts));
      p.addEventListener('mousemove',ev=>{
        bands.forEach(x=>x.setAttribute('fill-opacity', x===p?.98:.28));
        const r=wrap.getBoundingClientRect();
        tip.innerHTML='<div class="tt">'+t.name+'</div><div class="tm">'+t.total+' books · peak '+years[peak]+' ('+t.counts[peak]+')</div><div class="ex">'+t.examples.join(' · ')+'</div>';
        tip.style.opacity=1;
        let x=ev.clientX-r.left+14, y=ev.clientY-r.top+12;
        if(x+290>r.width)x=ev.clientX-r.left-290;
        tip.style.left=Math.max(4,x)+'px';tip.style.top=y+'px';
      });
      p.addEventListener('mouseleave',()=>{bands.forEach(x=>x.setAttribute('fill-opacity',.92));tip.style.opacity=0;});
      svg.appendChild(p);bands.push(p);
    });

    // legend
    const lg=document.getElementById('legend');
    threads.forEach((t,b)=>{
      const d=el2('div','lg');d.innerHTML='<span class="sw" style="background:'+t.color+'"></span><span class="n">'+t.name+'</span><span class="c">'+t.total+'</span>';
      d.addEventListener('mouseenter',()=>bands.forEach((x,j)=>x.setAttribute('fill-opacity',j===b?.98:.28)));
      d.addEventListener('mouseleave',()=>bands.forEach(x=>x.setAttribute('fill-opacity',.92)));
      lg.appendChild(d);
    });
    function el2(n,c){const e=document.createElement(n);e.className=c;return e;}
  })();
  </script>
</body>
</html>
"""

html = (HTML
        .replace("__DATA__", json.dumps(DATA, ensure_ascii=False))
        .replace("__TOTALS__", f"{DATA['totals']['books']} books, {DATA['totals']['threads']} threads, {DATA['years'][0]}–{DATA['years'][-1]}"))
open(OUT, "w").write(html)
print(f"wrote {OUT} ({len(html)} bytes)")
