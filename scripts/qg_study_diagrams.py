#!/usr/bin/env python3
"""Render STUDY-styled diagrams for the Quantum Gravity study guide."""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyArrowPatch, Circle, Rectangle, FancyBboxPatch, Polygon
from matplotlib.lines import Line2D
import os

# ---- fonts ----
for p in ["/tmp/qg_fonts/EBGaramond-Regular.ttf",
          "/tmp/qg_fonts/EBGaramond-Italic.ttf",
          "/tmp/qg_fonts/GeistMono.ttf"]:
    fm.fontManager.addfont(p)
SERIF = "EB Garamond"
MONO  = "Geist Mono"
mpl.rcParams["font.family"] = SERIF
mpl.rcParams["svg.fonttype"] = "none"
mpl.rcParams["axes.unicode_minus"] = False

# ---- palette (from study.html) ----
BG      = "#f7f3ec"
BG2     = "#f1ece2"
INK     = "#1c1814"
INK2    = "#5a544a"
INK3    = "#8b8478"
BORDER  = "#d8d0c2"
ACCENT  = "#6b8f9c"   # physics slate
# confidence ramp: tested -> inferred -> mystery
L1 = "#3f6d7a"   # layer 1  tested
L2 = "#9c7a3c"   # layer 2  inferred (warm amber)
L3 = "#8c6b9c"   # layer 3  mystery (violet)
OUT = "/Users/aidan/Desktop/writing-topology/img/quantum-gravity"

def newfig(w, h):
    fig = plt.figure(figsize=(w, h), dpi=200)
    fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG)
    ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    ax.axis("off")
    return fig, ax

def eyebrow(ax, x, y, text, color=INK3, size=10.5, ha="left"):
    ax.text(x, y, text, family=MONO, fontsize=size, color=color, ha=ha,
            va="center", transform=ax.transData)

def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=200, facecolor=BG)
    plt.close(fig)
    print("wrote", path)

# small helper: capsule
def capsule(ax, x, y, w, h, fc, ec, lw=1.2, alpha=1.0, ls="-"):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=2.2",
                       fc=fc, ec=ec, lw=lw, alpha=alpha, ls=ls,
                       mutation_aspect=1)
    ax.add_patch(p)
    return p

# =====================================================================
# FIG 1 — Three layers of confidence
# =====================================================================
def fig_layers():
    fig, ax = newfig(8.4, 6.2)
    eyebrow(ax, 7, 94, "reading key", INK3, 11)
    ax.text(7, 88.5, "Three layers of confidence", family=SERIF, fontsize=27,
            style="italic", color=INK, va="center")
    ax.text(7, 82.5, "Every claim in this thread sits on one of three floors. Watch which one.",
            family=SERIF, fontsize=14.5, color=INK2, va="center")

    layers = [
        (L1, "LAYER 1", "Tested physics",
         "As tested as physics gets — the same math that\nruns your GPS. We can watch it happen.",
         "white dwarfs · neutron stars · the event horizon"),
        (L2, "LAYER 2", "Inference from theory",
         "Not observed, but forced by the structure of the\ntheories. Near-universal among physicists.",
         "“the singularity can’t be real” · GR breaks at the Planck scale"),
        (L3, "LAYER 3", "Mystery",
         "No data, and maybe never any — the horizon hides it.\nPick your story; nothing decides between them.",
         "Planck star · pre-geometric spacetime · end of time"),
    ]
    top = 72; band_h = 19; gap = 3.2
    x0 = 7; bw = 86
    for i, (c, tag, title, body, egs) in enumerate(layers):
        y = top - i * (band_h + gap)
        # fading certainty: opacity steps down
        fill_a = [0.15, 0.115, 0.075][i]
        ls = ["-", "-", (0,(4,3))][i]
        lw = [1.7, 1.5, 1.4][i]
        capsule(ax, x0, y - band_h, bw, band_h, fc=c, ec="none", alpha=fill_a)
        capsule(ax, x0, y - band_h, bw, band_h, fc="none", ec=c, lw=lw, ls=ls)
        # left rail
        ax.add_patch(Rectangle((x0, y - band_h), 1.5, band_h, fc=c, ec="none",
                               alpha=1.0))
        cy = y - band_h/2
        ax.text(x0 + 6, y - 5.0, tag, family=MONO, fontsize=11, color=c,
                va="center", weight="bold")
        ax.text(x0 + 23.5, y - 5.0, title, family=SERIF, fontsize=18.5,
                style="italic", color=INK, va="center")
        ax.text(x0 + 6, y - 11.8, body, family=SERIF, fontsize=12.6, color=INK2,
                va="center", linespacing=1.25)
        ax.text(x0 + 6, y - band_h + 2.4, egs, family=MONO, fontsize=8.6,
                color=INK3, va="center")

    # down arrow on the side: certainty fades
    ax.annotate("", xy=(96.5, 12), xytext=(96.5, 71),
                arrowprops=dict(arrowstyle="-|>", color=INK3, lw=1.3))
    ax.text(98.4, 41, "certainty fades", family=MONO, fontsize=9, color=INK3,
            rotation=90, va="center", ha="center")
    save(fig, "01-three-layers.png")

# =====================================================================
# FIG 2 — Quantum mechanics catches the collapse, twice
# =====================================================================
def fig_collapse():
    fig, ax = newfig(8.8, 6.0)
    eyebrow(ax, 6, 94, "stellar death · by remnant mass", INK3, 11)
    ax.text(6, 88, "Quantum mechanics catches the collapse — twice", family=SERIF,
            fontsize=24.5, style="italic", color=INK, va="center")
    ax.text(6, 81.5,
            "Pauli exclusion is an outward pressure with no heat behind it — pure quantum stubbornness.\nWe get to watch it win two rounds. The third happens where no one has been.",
            family=SERIF, fontsize=13.2, color=INK2, va="center", linespacing=1.3)

    # mass axis
    ax_y = 30
    x_left, x_right = 9, 92
    mmin, mmax = 0, 4.2
    def mx(m): return x_left + (m - mmin) / (mmax - mmin) * (x_right - x_left)
    ax.add_line(Line2D([x_left, x_right], [ax_y, ax_y], color=INK3, lw=1.4))
    for m in [0, 1, 2, 3, 4]:
        ax.add_line(Line2D([mx(m), mx(m)], [ax_y-1, ax_y+1], color=INK3, lw=1.1))
        ax.text(mx(m), ax_y-3.6, f"{m}", family=MONO, fontsize=9, color=INK3, ha="center")
    ax.text(x_right+1.5, ax_y-3.6, r"M$_\odot$", family=MONO, fontsize=10.5, color=INK3, ha="left")
    ax.text(x_left, ax_y-7.6, "remnant core mass  (solar masses)", family=MONO,
            fontsize=9, color=INK3, ha="left")

    # thresholds
    chandra, tov = 1.4, 3.0
    for xm, lab in [(chandra, "~1.4  Chandrasekhar"), (tov, "~3  no pressure left")]:
        ax.add_line(Line2D([mx(xm), mx(xm)], [ax_y+1, 72], color=INK3, lw=1.0,
                    ls=(0,(2,2))))
        ax.text(mx(xm), 73.5, lab, family=MONO, fontsize=8.4, color=INK3, ha="center")

    # three zones as bands above axis
    zones = [
        (0.0, chandra, L1, "WHITE DWARF", "Electron degeneracy",
         "QM wins · we watch it"),
        (chandra, tov, L1, "NEUTRON STAR", "Neutron degeneracy",
         "QM wins · a city-size ball"),
        (tov, mmax, L3, "BLACK HOLE", "No known pressure",
         "collapse compulsory · Layer 3 inside"),
    ]
    band_top, band_bot = 66, ax_y+2
    for a, b, c, name, mech, note in zones:
        xa, xb = mx(a), mx(b)
        ax.add_patch(Rectangle((xa, band_bot), xb-xa, band_top-band_bot,
                     fc=c, ec="none", alpha=0.12))
        ax.add_patch(Rectangle((xa, band_bot), xb-xa, band_top-band_bot,
                     fc="none", ec=c, lw=1.3))
        xc = (xa+xb)/2
        ax.text(xc, band_top-6, name, family=MONO, fontsize=11, color=c,
                ha="center", weight="bold")
        ax.text(xc, band_top-13.5, mech, family=SERIF, fontsize=14.5,
                style="italic", color=INK, ha="center")
        ax.text(xc, band_bot+4.5, note, family=MONO, fontsize=8.2, color=INK2,
                ha="center")

    # caption strip
    ax.text(6, 13, "ROUND 1 & 2", family=MONO, fontsize=9.5, color=L1, weight="bold")
    ax.text(23, 13, "Pauli exclusion holds gravity off — observable, Layer 1.",
            family=SERIF, fontsize=12.5, color=INK2)
    ax.text(6, 8, "ROUND 3", family=MONO, fontsize=9.5, color=L3, weight="bold")
    ax.text(23, 8, r"Past ~3 M$_\odot$ the collapse is compulsory; the rest is behind the horizon.",
            family=SERIF, fontsize=12.5, color=INK2)
    save(fig, "02-collapse-three-rounds.png")

# =====================================================================
# FIG 3 — The singularity is a moment, not a place (tipping lightcones)
# =====================================================================
def fig_lightcones():
    fig, ax = newfig(8.8, 6.4)
    eyebrow(ax, 6, 95, "inside the event horizon", INK3, 11)
    ax.text(6, 89, "The singularity is a moment, not a place", family=SERIF,
            fontsize=25, style="italic", color=INK, va="center")
    ax.text(6, 82.8,
            "Cross the horizon and the radial direction turns time-like. “Toward the center” stops\nbeing a where you could avoid and becomes a when — the last moment in your future.",
            family=SERIF, fontsize=13, color=INK2, va="center", linespacing=1.3)

    # diagram frame
    fx0, fx1 = 8, 74          # r axis region for cones
    fy0, fy1 = 12, 70
    r_sing = fx0 + 2          # singularity near left
    r_hor  = fx0 + 36         # horizon
    # axes labels
    ax.add_line(Line2D([fx0, fx1], [fy0, fy0], color=INK3, lw=1.2))
    ax.annotate("", xy=(fx0-0.2, fy1+2), xytext=(fx0-0.2, fy0),
                arrowprops=dict(arrowstyle="-|>", color=INK3, lw=1.2))
    ax.text(fx1, fy0-3.4, "<-- decreasing radius", family=MONO, fontsize=9,
            color=INK3, ha="right")
    ax.text(fx0+ (fx1-fx0)/2, fy0-6.6, "← toward the center", family=MONO,
            fontsize=9, color=INK3, ha="center")
    ax.text(fx0-2.6, (fy0+fy1)/2, "time →", family=MONO, fontsize=9, color=INK3,
            rotation=90, va="center", ha="center")

    # singularity = jagged vertical line (a moment)
    ys = np.linspace(fy0, fy1+4, 40)
    xs = r_sing + 1.1*np.sin(ys*1.4)
    ax.plot(xs, ys, color=L3, lw=2.2)
    ax.text(r_sing+0.5, fy1+7.5, "singularity", family=SERIF, fontsize=14.5,
            style="italic", color=L3, ha="left")
    ax.text(r_sing+0.5, fy1+4.0, "a time, not a place — ahead of every worldline",
            family=MONO, fontsize=8.2, color=L3, ha="left")

    # horizon
    ax.add_line(Line2D([r_hor, r_hor], [fy0, fy1+1], color=INK, lw=1.4,
                ls=(0,(5,3))))
    ax.text(r_hor, fy1+3.2, "event horizon", family=MONO, fontsize=9, color=INK,
            ha="center")

    # region tints
    ax.add_patch(Rectangle((fx0, fy0), r_hor-fx0, fy1-fy0, fc=L3, ec="none", alpha=0.07))
    ax.add_patch(Rectangle((r_hor, fy0), fx1-r_hor, fy1-fy0, fc=ACCENT, ec="none", alpha=0.05))

    # cone drawer: tip angle phi (deg) measured from +y toward -x (inward/left)
    def cone(x, y, phi_deg, half=26, size=9, color=INK):
        phi = np.radians(phi_deg)
        for sgn in (-1, 1):
            a = phi + sgn*np.radians(half)
            dx, dy = -np.sin(a)*size, np.cos(a)*size
            ax.add_line(Line2D([x, x+dx], [y, y+dy], color=color, lw=1.5))
        # fill
        a1 = phi - np.radians(half); a2 = phi + np.radians(half)
        p = Polygon([[x, y],
                     [x-np.sin(a1)*size, y+np.cos(a1)*size],
                     [x-np.sin(a2)*size, y+np.cos(a2)*size]],
                    closed=True, fc=color, ec="none", alpha=0.12)
        ax.add_patch(p)
        # central future arrow
        dx, dy = -np.sin(phi)*size*0.92, np.cos(phi)*size*0.92
        ax.add_patch(FancyArrowPatch((x, y), (x+dx, y+dy),
                     arrowstyle="-|>", mutation_scale=10, color=color, lw=1.4))

    # sample radii positions and tip angles: outside upright(0), horizon 45, inside ->85
    samples = [
        (fx1-6,  0,  ACCENT, "far outside\nfuture = straight up"),
        (r_hor+11, 22, ACCENT, "approaching"),
        (r_hor,   45, INK,    "at the horizon\ncones tip 45°"),
        (r_hor-13, 68, L3,    "inside"),
        (r_sing+9, 84, L3,    "future = toward r = 0"),
    ]
    yc = (fy0+fy1)/2 - 4
    for x, phi, c, lab in samples:
        cone(x, yc, phi, color=c)
        ax.text(x, yc-13.5, lab, family=MONO, fontsize=7.6, color=c, ha="center",
                va="top", linespacing=1.25)

    # right-side explainer card
    cx = 77.5
    ax.text(cx, 70, "OUTSIDE", family=MONO, fontsize=10, color=ACCENT, weight="bold")
    ax.text(cx, 64.5, "Free to move in space,\ndragged through time.\nYou can’t refuse Tuesday.",
            family=SERIF, fontsize=12.2, color=INK2, va="top", linespacing=1.25)
    ax.text(cx, 47, "INSIDE", family=MONO, fontsize=10, color=L3, weight="bold")
    ax.text(cx, 41.5, "Decreasing radius inherits\nthat pull. Firing rockets out\ndelays the center no more\nthan running west delays\nTuesday.",
            family=SERIF, fontsize=12.2, color=INK2, va="top", linespacing=1.25)
    ax.text(cx, 18, "“What’s at the center?”\nmay be as malformed as\n“What’s north of the\nNorth Pole?”",
            family=SERIF, fontsize=12.4, style="italic", color=INK, va="top",
            linespacing=1.28)
    save(fig, "03-singularity-is-a-moment.png")

# =====================================================================
# FIG 4 — Where the theory plants its flag (scale)
# =====================================================================
def fig_planck():
    fig, ax = newfig(8.8, 5.2)
    eyebrow(ax, 6, 93, "where the math waves a flag", INK3, 11)
    ax.text(6, 86.5, "Twenty orders of magnitude below a proton", family=SERIF,
            fontsize=24, style="italic", color=INK, va="center")
    ax.text(6, 79.5,
            "General relativity, running solo, marches the density to infinity. But the matter is quantum,\nand near the Planck length its smooth geometry must tear. The singularity is the flag, not a thing.",
            family=SERIF, fontsize=12.6, color=INK2, va="center", linespacing=1.3)

    # log axis from 10^0 to 10^-36
    y = 46
    x0, x1 = 9, 92
    emin, emax = -36, 1   # exponent range (meters)
    def ex(e): return x0 + (e - emax) / (emin - emax) * (x1 - x0)
    ax.add_line(Line2D([x0, x1], [y, y], color=INK3, lw=1.5))
    for e in range(0, -37, -5):
        ax.add_line(Line2D([ex(e), ex(e)], [y-1, y+1], color=INK3, lw=1.0))
        ax.text(ex(e), y-3.8, f"10$^{{{e}}}$", family=MONO, fontsize=8.4,
                color=INK3, ha="center")
    ax.text(x0, y-8, "size in meters  (log scale)", family=MONO, fontsize=9,
            color=INK3, ha="left")

    marks = [
        (0,   "you", "1 m", INK2, "up"),
        (-10, "atom", r"$10^{-10}$ m", INK2, "down"),
        (-15, "proton", r"$10^{-15}$ m", L1, "up"),
        (-35, "Planck length", r"$10^{-35}$ m", L3, "up"),
    ]
    for e, name, val, c, d in marks:
        x = ex(e)
        ax.add_line(Line2D([x, x], [y, y+(11 if d=="up" else -11)], color=c, lw=1.2))
        yy = y+12 if d=="up" else y-12
        va = "bottom" if d=="up" else "top"
        ax.plot([x],[y], "o", color=c, ms=5)
        ax.text(x, yy, name, family=SERIF, fontsize=13.5, style="italic",
                color=c, ha="center", va=va)
        ax.text(x, yy+(3.6 if d=="up" else -3.6), val, family=MONO, fontsize=8.4,
                color=c, ha="center", va=va)

    # bracket spanning proton -> planck = 20 orders
    bx0, bx1 = ex(-15), ex(-35)
    by = 26
    ax.annotate("", xy=(bx1, by), xytext=(bx0, by),
                arrowprops=dict(arrowstyle="<|-|>", color=INK3, lw=1.2))
    ax.text((bx0+bx1)/2, by-3.2, "20 orders of magnitude", family=MONO,
            fontsize=9, color=INK3, ha="center", va="top")

    # flag at planck: drawn pennant + centered caption (kept inside bounds)
    fx = ex(-35)
    ax.add_line(Line2D([fx, fx], [19, 25], color=L3, lw=1.6))
    ax.add_patch(Polygon([[fx, 25], [fx-5.5, 23.4], [fx, 21.8]], closed=True,
                 fc=L3, ec="none", alpha=0.85))
    ax.text(50, 11, "near the Planck length, GR plants its flag:  “I’m done — send the next theory.”",
            family=SERIF, fontsize=13, style="italic", color=L3, ha="center",
            va="center")
    save(fig, "04-planck-flag.png")

# =====================================================================
# FIG 5 — What survives a revolution (structural realism)
# =====================================================================
def fig_survives():
    fig, ax = newfig(8.8, 6.0)
    eyebrow(ax, 6, 94, "structural realism", INK3, 11)
    ax.text(6, 88, "What survives a scientific revolution", family=SERIF,
            fontsize=25, style="italic", color=INK, va="center")
    ax.text(6, 81.5,
            "The objects of physics keep getting executed. The mathematical structure keeps getting\ninherited. Maybe the structure was the real content all along — and “things” were always interface.",
            family=SERIF, fontsize=12.8, color=INK2, va="center", linespacing=1.3)

    rows = [
        ("Newton’s force", "an entity pulling masses", "dead",
         "yet his equations live inside\nEinstein’s as a limiting case"),
        ("The luminiferous ether", "the medium light waves in", "dead",
         "yet Maxwell’s wave structure\ncarried straight through"),
        ("The particle", "a tiny bead of stuff", "dead",
         "yet it’s just an excitation of\na field — a ripple, not a bead"),
    ]
    # column headers
    cx_thing, cx_struct = 30, 70
    ax.text(cx_thing, 71.5, "THE “THING”", family=MONO, fontsize=10, color=L3,
            ha="center", weight="bold")
    ax.text(cx_thing, 68.2, "executed", family=MONO, fontsize=8.6, color=INK3, ha="center")
    ax.text(cx_struct, 71.5, "THE STRUCTURE", family=MONO, fontsize=10, color=L1,
            ha="center", weight="bold")
    ax.text(cx_struct, 68.2, "inherited", family=MONO, fontsize=8.6, color=INK3, ha="center")

    top = 63; rh = 16; gap = 2.4
    for i, (name, gloss, verdict, survives) in enumerate(rows):
        ry = top - i*(rh+gap)
        cy = ry - rh/2
        # name block (left)
        ax.text(6, cy+2.2, name, family=SERIF, fontsize=15.5, style="italic",
                color=INK, va="center")
        ax.text(6, cy-3.2, gloss, family=MONO, fontsize=8.2, color=INK3, va="center")
        # thing capsule -> struck through
        capsule(ax, cx_thing-9, cy-4, 18, 8, fc=L3, ec=L3, alpha=0.12)
        capsule(ax, cx_thing-9, cy-4, 18, 8, fc="none", ec=L3, lw=1.2)
        ax.text(cx_thing, cy, verdict, family=MONO, fontsize=10.5, color=L3,
                ha="center", va="center", weight="bold")
        ax.add_line(Line2D([cx_thing-7, cx_thing+7], [cy, cy], color=L3, lw=1.4))
        # arrow
        ax.add_patch(FancyArrowPatch((cx_thing+10, cy), (cx_struct-15, cy),
                     arrowstyle="-|>", mutation_scale=12, color=INK3, lw=1.2))
        # structure capsule
        capsule(ax, cx_struct-15, cy-5.6, 38, 11.2, fc=L1, ec=L1, alpha=0.10)
        capsule(ax, cx_struct-15, cy-5.6, 38, 11.2, fc="none", ec=L1, lw=1.3)
        ax.text(cx_struct+4, cy, survives, family=SERIF, fontsize=12.2,
                color=INK, ha="center", va="center", linespacing=1.22)

    ax.text(50, 7, "the pattern: objects die · the math is inherited",
            family=MONO, fontsize=10.5, color=INK2, ha="center")
    save(fig, "05-what-survives-revolution.png")

# =====================================================================
# FIG 6 — Three staircases, one basement
# =====================================================================
def fig_staircases():
    fig, ax = newfig(8.8, 6.0)
    eyebrow(ax, 6, 94, "the recurring floor", INK3, 11)
    ax.text(6, 88, "Three staircases, one basement", family=SERIF, fontsize=25,
            style="italic", color=INK, va="center")
    ax.text(6, 81.5,
            "Start from the dying star, the black-hole interior, or the question “is anything a thing?” —\nevery staircase descends to the same floor, where data runs out and the theories contradict.",
            family=SERIF, fontsize=12.8, color=INK2, va="center", linespacing=1.3)

    stairs = [
        (18, ACCENT, "STELLAR COLLAPSE",
         ["star burns to iron", "core falls", "QM catches it twice", "past 3 suns -- no catch"]),
        (50, INK,    "BLACK-HOLE INTERIOR",
         ["cross the horizon", "radius becomes time", "tidal thrash", "the last moment"]),
        (82, L1,     "IS ANYTHING A THING?",
         ["particle → field", "observers disagree", "info in relations", "structure, not stuff"]),
    ]
    top = 72; step_w = 9.5; step_h = 7.2; n = 4
    floor_y = 18
    for cx, c, title, labels in stairs:
        ax.text(cx, 75.5, title, family=MONO, fontsize=9.6, color=c, ha="center",
                weight="bold")
        x = cx - (n*step_w)/2
        y = top
        for j, lab in enumerate(labels):
            # tread
            ax.add_patch(Rectangle((x, y-step_h), step_w, step_h*0.55, fc=c,
                         ec="none", alpha=0.16))
            ax.add_patch(Rectangle((x, y-step_h), step_w, step_h*0.55, fc="none",
                         ec=c, lw=1.1))
            ax.text(x+step_w/2, y-step_h*0.72+1.4, lab, family=MONO, fontsize=6.6,
                    color=INK2, ha="center", va="center")
            x += step_w*0.92
            y -= step_h
        # arrow down into floor
        ax.add_patch(FancyArrowPatch((x-step_w*0.45, y+1), (x-step_w*0.45, floor_y+5),
                     arrowstyle="-|>", mutation_scale=12, color=c, lw=1.5))

    # the floor
    capsule(ax, 8, floor_y-9, 84, 11, fc=L3, ec=L3, alpha=0.12)
    capsule(ax, 8, floor_y-9, 84, 11, fc="none", ec=L3, lw=1.6, ls=(0,(5,3)))
    ax.text(50, floor_y-1.4, "THE PLANCK FLOOR · LAYER 3", family=MONO,
            fontsize=10.5, color=L3, ha="center", weight="bold")
    ax.text(50, floor_y-6, "no data · may never be any · quantum mechanics and gravity both apply, and contradict",
            family=SERIF, fontsize=12.5, style="italic", color=INK, ha="center")
    save(fig, "06-mystery-floor.png")

if __name__ == "__main__":
    fig_layers()
    fig_collapse()
    fig_lightcones()
    fig_planck()
    fig_survives()
    fig_staircases()
    print("done")
