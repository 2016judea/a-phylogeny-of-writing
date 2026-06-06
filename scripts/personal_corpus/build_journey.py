#!/usr/bin/env python3
"""Build the 'path of exploration' SVG — a winding journey down through the genres
Aidan explored, bubble size = books read there (time spent), subgenres branching off.
Emits an SVG fragment that build_reading_3d.py injects into reading.html.

    python3 scripts/personal_corpus/build_journey.py   # -> data/personal_corpus/journey.svg
"""
import json
import math

reading = json.load(open("data/personal_corpus/themes_by_year.json"))
COLOR = {t["name"]: t["color"] for t in reading["threads"]}

# Movement palette (era tint for the small caption pill)
MOVE = {
    "Story": "#9c8f5a", "Style": "#b89a6a", "Ideas": "#8c6b9c",
    "Meaning": "#b5563c", "Making": "#3c6b5a",
}

# The path — chronological-ish genre stations. books = bubble size (real totals).
# subs = the subgenres/voices explored there.
STATIONS = [
    {"label": "Fantasy & Adventure", "year": "2014", "books": 18, "move": "Story",
     "blurb": "where it starts — reading for what happens next",
     "subs": ["Ranger's Apprentice", "Eragon", "Rothfuss"]},
    {"label": "Dystopia & the Sciences", "year": "2018", "books": 24, "move": "Story",
     "blurb": "the gateway — ideas as warning, science as awe",
     "subs": ["Huxley · Orwell", "Bradbury · Wells", "Hawking · Gleick"]},
    {"label": "The American Canon", "year": "2019", "books": 93, "move": "Style",
     "blurb": "the long dwelling — 80 books in a year",
     "subs": ["Fitzgerald", "Steinbeck", "Hemingway", "Faulkner"]},
    {"label": "Romantic → Plain Poetry", "year": "2019–23", "books": 25, "move": "Style",
     "blurb": "a parallel trail that plainens over time",
     "subs": ["Keats · Shelley", "Whitman · Eliot", "Larkin · Frost"]},
    {"label": "Modernism & Experiment", "year": "2020", "books": 24, "move": "Ideas",
     "blurb": "difficulty becomes the reward",
     "subs": ["Joyce", "Woolf", "Pynchon"]},
    {"label": "Southern Gothic & Grit", "year": "2021", "books": 35, "move": "Ideas",
     "blurb": "the McCarthy years — the throughline of the whole map",
     "subs": ["Cormac McCarthy", "William Gay", "Denis Johnson"]},
    {"label": "Money, Power & Polemic", "year": "2021", "books": 25, "move": "Ideas",
     "blurb": "a sharp side-quest into ideology & economics",
     "subs": ["Rand", "Bastiat · Rothbard", "Ferguson"]},
    {"label": "Philosophy & the Examined Life", "year": "2022", "books": 27, "move": "Ideas",
     "blurb": "the argument under the narrative",
     "subs": ["Nietzsche", "Camus · Kierkegaard", "Dostoevsky"]},
    {"label": "Beats & Transgression", "year": "2022–25", "books": 20, "move": "Meaning",
     "blurb": "the restless, road-bound, nihilist vein",
     "subs": ["Bret Easton Ellis", "Kerouac", "Fante"]},
    {"label": "Faith, Noir & Craft", "year": "2023–24", "books": 27, "move": "Meaning",
     "blurb": "meaning, form, and how-to-write",
     "subs": ["O'Connor · Frankl", "Chandler (noir)", "On Writing"]},
    {"label": "Stoicism, Zen & First Principles", "year": "2025–26", "books": 20, "move": "Making",
     "blurb": "reading to live and make — and back to Socrates",
     "subs": ["Marcus Aurelius", "Buddha · Rubin", "Plato · Paine"]},
]

W, TOP, STEP = 1000, 92, 150
H = TOP + STEP * (len(STATIONS) - 1) + 120
CX, AMP = 500, 150


def rad(books):
    return 15 + 3.1 * math.sqrt(books)


def pos(i):
    # serpentine: alternate sides, smooth
    return CX + AMP * math.sin(i * 0.9), TOP + i * STEP


def smooth_path(pts):
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(1, len(pts)):
        x0, y0 = pts[i - 1]; x1, y1 = pts[i]
        my = (y0 + y1) / 2
        d += f" C{x0:.1f} {my:.1f},{x1:.1f} {my:.1f},{x1:.1f} {y1:.1f}"
    return d


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


def build():
    pts = [pos(i) for i in range(len(STATIONS))]
    out = [f'<svg viewBox="0 0 {W} {H}" class="journey-svg" role="img" '
           f'aria-label="The path of reading — genres explored over time, bubble size = books read">']
    # the trail
    out.append(f'<path d="{smooth_path(pts)}" fill="none" stroke="var(--border-secondary)" '
               f'stroke-width="2.5" stroke-dasharray="1 7" stroke-linecap="round" opacity="0.8"/>')
    for i, st in enumerate(STATIONS):
        x, y = pts[i]; r = rad(st["books"]); col = COLOR.get(st["label"], "#b89a6a")
        left = x < CX
        out.append(f'<g class="station">')
        # subgenre satellites on the outer side
        n = len(st["subs"])
        for j, sub in enumerate(st["subs"]):
            ang = (math.pi * (0.62 + 0.52 * (j / max(1, n - 1) - 0.5))) * (1 if left else -1) + (math.pi if left else 0)
            sx = x + math.cos(ang) * (r + 46)
            sy = y + math.sin(ang) * (r + 30) - 6 + j * 4
            out.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{sx:.1f}" y2="{sy:.1f}" stroke="{col}" stroke-width="1" opacity="0.4"/>')
            out.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="4.5" fill="{col}" opacity="0.6"/>')
            anchor = "end" if left else "start"
            tx = sx + (-9 if left else 9)
            out.append(f'<text x="{tx:.1f}" y="{sy+3.5:.1f}" text-anchor="{anchor}" class="j-sub">{esc(sub)}</text>')
        # main bubble
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{col}" fill-opacity="0.9" stroke="var(--bg-secondary)" stroke-width="2"/>')
        out.append(f'<text x="{x:.1f}" y="{y+5:.1f}" text-anchor="middle" class="j-books">{st["books"]}</text>')
        # label block on outer side of the bubble
        lx = x + (-(r + 60) if left else (r + 60)); anchor = "end" if left else "start"
        out.append(f'<text x="{lx:.1f}" y="{y-6:.1f}" text-anchor="{anchor}" class="j-label">{esc(st["label"])}</text>')
        out.append(f'<text x="{lx:.1f}" y="{y+12:.1f}" text-anchor="{anchor}" class="j-meta">{st["year"]} · {st["move"].lower()}</text>')
        out.append(f'<text x="{lx:.1f}" y="{y+28:.1f}" text-anchor="{anchor}" class="j-blurb">{esc(st["blurb"])}</text>')
        out.append('</g>')
    out.append('</svg>')
    return "\n".join(out)


if __name__ == "__main__":
    svg = build()
    open("data/personal_corpus/journey.svg", "w").write(svg)
    print(f"wrote data/personal_corpus/journey.svg ({len(svg)} bytes, {len(STATIONS)} stations)")
