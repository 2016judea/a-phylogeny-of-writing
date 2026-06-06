#!/usr/bin/env python3
"""Deep quantitative analysis of Aidan's reading + writing corpus. Prints findings."""
import json, re, statistics as st
from collections import Counter, defaultdict
from datetime import datetime

MON = {m: i+1 for i, m in enumerate(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])}
def parse(s):
    m = re.search(r"(\d{1,2})\s+([A-Za-z]{3})\s+(20\d\d)", s or "")
    return datetime(int(m.group(3)), MON[m.group(2)], int(m.group(1))) if m else None

books = json.load(open("data/personal_corpus/goodreads_reads.json"))
dated = []
for b in books:
    d = parse(b.get("read_date",""))
    if d and b.get("read_year"):
        dated.append({**b, "dt": d, "author": re.sub(r"\s+"," ",b["author"]).strip()})
dated.sort(key=lambda x: x["dt"])

print("="*70); print("READING CADENCE")
print(f"  dated reads: {len(dated)} of {len(books)} shelved   span {dated[0]['dt'].date()} → {dated[-1]['dt'].date()}")
byyear = Counter(b["read_year"] for b in dated)
for y in sorted(byyear): print(f"    {y}: {byyear[y]}")
# peak pace + droughts (gaps between consecutive finishes)
gaps = [(dated[i]["dt"]-dated[i-1]["dt"]).days for i in range(1,len(dated))]
print(f"  2019 pace: {byyear[2019]} books = one every {365/byyear[2019]:.1f} days")
# longest drought
gi = max(range(len(gaps)), key=lambda i: gaps[i])
print(f"  longest gap: {gaps[gi]} days ({dated[gi]['dt'].date()} '{dated[gi]['title'][:30]}' → {dated[gi+1]['dt'].date()} '{dated[gi+1]['title'][:30]}')")
# median days/book by year (acceleration)
print("  median days between finishes, by year:")
for y in sorted(byyear):
    yb = [b for b in dated if b["read_year"]==y]
    if len(yb)<2: continue
    g = [(yb[i]['dt']-yb[i-1]['dt']).days for i in range(1,len(yb))]
    print(f"    {y}: {st.median(g):.0f}d")

print("="*70); print("SEASONALITY (which months he finishes books)")
bymon = Counter(b["dt"].month for b in dated)
names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
for mo in range(1,13):
    bar = "█"*round(bymon[mo]/max(bymon.values())*24)
    print(f"    {names[mo-1]} {bymon[mo]:3} {bar}")
winter = sum(bymon[m] for m in (12,1,2)); summer = sum(bymon[m] for m in (6,7,8))
print(f"  winter(DJF) {winter}  vs  summer(JJA) {summer}")

print("="*70); print("AUTHOR OBSESSIONS")
auth = Counter(b["author"] for b in dated)
print(f"  distinct authors: {len(auth)}   top 10 = {sum(c for _,c in auth.most_common(10))/len(dated)*100:.0f}% of all reading")
for a,c in auth.most_common(16):
    yrs = sorted({b['read_year'] for b in dated if b['author']==a})
    print(f"    {c:2}  {a:24}  {yrs[0]}–{yrs[-1]} ({yrs[-1]-yrs[0]}y span)")

print("="*70); print("BINGES (consecutive same-author reads)")
runs=[]; i=0
while i < len(dated):
    j=i
    while j+1<len(dated) and dated[j+1]["author"]==dated[i]["author"]: j+=1
    if j>i: runs.append((dated[i]["author"], j-i+1, dated[i]["dt"].date(), dated[j]["dt"].date()))
    i=j+1
for a,n,d0,d1 in sorted(runs,key=lambda x:-x[1])[:8]:
    print(f"    {n} in a row  {a:24} {d0} → {d1} ({(parse(None) or 0) if False else (d1-d0).days}d)")

print("="*70); print("RE-READS (same title twice)")
seen=defaultdict(list)
for b in dated: seen[b["title"].lower().split(":")[0].strip()].append(b)
for t,lst in seen.items():
    if len(lst)>1: print(f"    {lst[0]['title'][:40]}  ×{len(lst)}  ({', '.join(str(x['read_year']) for x in lst)})")

print("="*70); print("PROSE FINGERPRINT (his own writing)")
wc = json.load(open("data/personal_corpus/writing_corpus.json"))
text = " ".join(w["text"] for w in wc if not w["text"].startswith("[ERR"))
toks = re.findall(r"[a-zA-Z']+", text.lower())
print(f"  total words written (Dropbox corpus): {len(toks):,} across {len(wc)} pieces")
STOP=set("the a an and or but of to in on at by for with from as is are was were be been being it its this that these those i you he she we they his her their my your our me him them us not no so if then than too very can could would should will just have has had do does did about into out up down over under after before".split())
content=[t for t in toks if t not in STOP and len(t)>2]
print("  most-used content words:")
for w,c in Counter(content).most_common(30): print(f"    {c:3} {w}")
MOTIF={
 "cosmos/celestial":"star stars sky skies heaven heavens cosmos celestial moon sun sunset dawn satellite satellites galaxy universe astronaut rocket".split(),
 "rural/west/land":"dirt road roads gravel mountain mountains field fields creek river rivers prairie ranch cattle orchard pine valley wheat".split(),
 "longing/memory":"dream dreams memory remember nostalgic forget regret lost longing sentimental".split(),
 "religion/sacred":"god gods heaven prophet sacred soul souls prayer divine eternal".split(),
 "light":"light golden glow gleam shine luminous bright shadow dark darkness".split(),
 "water/flux":"water waves ocean sea flow gurgle drift float tide stream".split(),
}
print("  motif density (word hits):")
fset=Counter(toks)
for k,ws in MOTIF.items():
    tot=sum(fset[w] for w in ws)
    print(f"    {tot:4}  {k}")
# sentence length
sents=[s for s in re.split(r"[.!?]+", text) if len(s.split())>1]
slen=[len(s.split()) for s in sents]
print(f"  sentences: {len(sents)}   mean {st.mean(slen):.1f} words, median {st.median(slen)}")

print("="*70); print("READING → WRITING LAG")
rd=json.load(open("data/personal_corpus/themes_by_year.json"))
wr=json.load(open("data/personal_corpus/writing_by_year.json"))
years=rd["years"]
sg=next(t for t in rd["threads"] if "Southern Gothic" in t["name"])["counts"]
nv=next((t for t in wr["threads"] if t["name"]=="Novel"),{"counts":[0]*len(years)})["counts"]
def xcorr(a,b,lag):
    n=len(a); s=0
    for i in range(n):
        if 0<=i-lag<n: s+=a[i-lag]*b[i]
    return s
print("  Southern-Gothic reading vs Novel writing — overlap by lag:")
for lag in range(0,5):
    print(f"    lag {lag}y: {xcorr(sg,nv,lag)}")
print(f"    SG reading peak year: {years[sg.index(max(sg))]}   Novel writing peak: {years[nv.index(max(nv))]}")

print("="*70); print("SUBSTACK WORD-COUNT DECAY")
sp=json.load(open("data/personal_corpus/substack_posts.json"))
byy=defaultdict(list)
for p in sp:
    if p.get("wordcount"): byy[p["date"][:4]].append(p["wordcount"])
for y in sorted(byy):
    print(f"    {y}: {len(byy[y])} posts, avg {st.mean(byy[y]):.0f} words (median {st.median(byy[y]):.0f})")
