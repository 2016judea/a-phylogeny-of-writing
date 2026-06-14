#!/usr/bin/env python3
"""Penrose-notebook diagrams for the Quantum Gravity study guide.
Thin confident ink, near-zero wiggle, black on near-white, sparse serif italic."""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyArrowPatch, Polygon, Circle
from matplotlib.lines import Line2D
import os

fm.fontManager.addfont("/tmp/qg_fonts/EBGaramond-Italic.ttf")
fm.fontManager.addfont("/tmp/qg_fonts/EBGaramond-Regular.ttf")
SERIF = "EB Garamond"
mpl.rcParams["font.family"] = SERIF
mpl.rcParams["mathtext.fontset"] = "cm"
mpl.rcParams["axes.unicode_minus"] = False

INK   = "#1a1815"
INK2  = "#615b52"
PAPER = "#fdfcf9"
# a whisper of hand-quality, not cartoon wiggle
SK = dict(scale=0.6, length=140, randomness=1.3)
OUT = "/Users/aidan/Desktop/writing-topology/img/quantum-gravity/penrose"
os.makedirs(OUT, exist_ok=True)

def newfig(w, h):
    fig = plt.figure(figsize=(w, h), dpi=200)
    fig.patch.set_facecolor(PAPER)
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.96])
    ax.set_facecolor(PAPER)
    ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax

def line(ax, xs, ys, lw=1.3, ls="-", color=INK, alpha=1.0, sketch=True, z=2):
    ln = Line2D(xs, ys, lw=lw, ls=ls, color=color, alpha=alpha,
                solid_capstyle="round", zorder=z)
    if sketch: ln.set_sketch_params(**SK)
    ax.add_line(ln); return ln

def axis_arrow(ax, p0, p1, lw=1.3, color=INK):
    a = FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=11,
                        color=color, lw=lw, shrinkA=0, shrinkB=0, zorder=2)
    ax.add_patch(a); return a

def lab(ax, x, y, s, size=15.5, it=True, color=INK, ha="center", va="center", rot=0, z=5):
    ax.text(x, y, s, family=SERIF, fontsize=size,
            fontstyle="italic" if it else "normal",
            color=color, ha=ha, va=va, rotation=rot, zorder=z)

def cone(ax, x, y, phi_deg, half=23, size=9, lw=1.2, fill=True):
    """future light cone; phi tips from +y (up) toward -x (inward/left)."""
    phi = np.radians(phi_deg)
    e1 = phi - np.radians(half); e2 = phi + np.radians(half)
    p1 = (x - np.sin(e1)*size, y + np.cos(e1)*size)
    p2 = (x - np.sin(e2)*size, y + np.cos(e2)*size)
    if fill:
        poly = Polygon([(x, y), p1, p2], closed=True, fc=INK, ec="none",
                       alpha=0.06, zorder=1)
        ax.add_patch(poly)
    line(ax, [x, p1[0]], [y, p1[1]], lw=lw, sketch=False)
    line(ax, [x, p2[0]], [y, p2[1]], lw=lw, sketch=False)
    # faint future direction tick
    line(ax, [x, x-np.sin(phi)*size*0.62], [y, y+np.cos(phi)*size*0.62],
         lw=0.8, color=INK2, sketch=False)

def save(fig, name):
    p = os.path.join(OUT, name); fig.savefig(p, dpi=200, facecolor=PAPER)
    plt.close(fig); print("wrote", p)

# =====================================================================
# 1 — gravitational collapse: spacetime diagram with tipping cones
# =====================================================================
def fig_collapse():
    fig, ax = newfig(6.8, 6.6)
    Ox, Oy = 15, 13
    Rmax_x, Tmax_y = 93, 92
    x_h = 45                              # horizon radius (vertical)
    # axes
    axis_arrow(ax, (Ox, Oy), (Rmax_x+3, Oy))
    axis_arrow(ax, (Ox, Oy), (Ox, Tmax_y+3))
    lab(ax, Rmax_x+4, Oy-3, "r", size=17)
    lab(ax, Ox-3, Tmax_y+3, "t", size=17)

    # horizon (vertical dashed)
    line(ax, [x_h, x_h], [Oy, 84], lw=1.1, ls=(0,(4,3)))
    lab(ax, x_h+2.5, 82, "horizon", size=14.5, ha="left", color=INK2)

    # singularity: jagged line on r = 0 for high t
    ys = np.linspace(58, 90, 26)
    xs = Ox + 1.5*np.sin(ys*1.25)
    line(ax, xs, ys, lw=2.0, sketch=False)
    lab(ax, Ox+2.5, 92, "singularity", size=15, ha="left")

    # star surface worldline: r(t) from R0 down to 0 at the singularity
    t = np.linspace(0, 1, 120)
    R0 = 72
    rr = R0 * (1 - t)**1.7
    xx = Ox + rr
    yy = Oy + t*(60 - Oy) + t**1.4*8          # rises to ~y 60 then into sing
    yy = Oy + 47*t + 12*t**2
    line(ax, xx, yy, lw=1.5)
    # faint interior fill (collapsing matter, left of surface)
    ax.fill_betweenx(yy, Ox, xx, color=INK, alpha=0.04, zorder=0)
    lab(ax, 58, 30, "star surface", size=14, rot=-34, color=INK2)

    # tipping light cones, outside -> horizon -> inside
    cone(ax, 82, 30, 0)        # far outside, upright
    cone(ax, 55, 50, 40)       # approaching horizon
    cone(ax, x_h, 60, 47)      # at horizon
    cone(ax, 30, 70, 72)       # inside, future opens toward r=0
    save(fig, "1-collapse.png")

# =====================================================================
# 2 — fusion: binding energy per nucleon, staircase to the iron peak
# =====================================================================
def fig_fusion():
    fig, ax = newfig(7.4, 5.2)
    Ox, Oy = 13, 16
    Wx, Hy = 94, 86
    axis_arrow(ax, (Ox, Oy), (Wx+2, Oy))
    axis_arrow(ax, (Ox, Oy), (Ox, Hy+3))
    lab(ax, Wx-1, Oy-4.5, "heavier nuclei →", size=13.5, ha="right", color=INK2)
    lab(ax, Ox-2, Hy+3, "binding energy", size=13.5, ha="left", color=INK2, rot=90)

    # binding-energy-per-nucleon curve: steep climb -> iron peak -> slow fall
    xc = np.linspace(0, 1, 400)
    # climb (1-exp) to peak at xpk, then gentle linear decline
    xpk = 0.46
    peak_y = 74
    climb = peak_y * (1 - np.exp(-xc/0.14))
    decline = peak_y - (xc - xpk)*26
    yc = np.where(xc <= xpk, climb, np.maximum(decline, 30))
    X = Ox + xc*(Wx-Ox-3)
    Y = Oy + yc*0.0 + yc  # yc already in plot units-ish
    Y = Oy + yc
    line(ax, X, Y, lw=1.5)

    # staircase rungs hugging the climb at fusion stages
    stages = [("H", 0.02), ("He", 0.10), ("C", 0.20), ("O", 0.28),
              ("Si", 0.37), ("Fe", xpk)]
    def yof(xv):
        return Oy + (peak_y*(1-np.exp(-xv/0.14)) if xv <= xpk else peak_y-(xv-xpk)*26)
    for nm, xv in stages:
        px = Ox + xv*(Wx-Ox-3); py = yof(xv)
        line(ax, [px, px], [Oy, py], lw=0.7, color=INK2, ls=(0,(1,3)), sketch=False)
        ax.add_patch(Circle((px, py), 0.9, fc=INK, ec="none", zorder=4))
        lab(ax, px, Oy-4, nm, size=12.5, color=INK2)
        # little step tread
        line(ax, [px-3.2, px], [py, py], lw=0.9, color=INK2, sketch=False)

    # energy-released arrow along the climb
    axis_arrow(ax, (Ox+8, yof(0.05)+5), (Ox+xpk*(Wx-Ox-3)-7, peak_y+Oy-3),
               lw=1.0, color=INK2)
    lab(ax, 30, 64, "energy released", size=13, color=INK2, rot=30)

    # iron peak: stop / wall
    fx = Ox + xpk*(Wx-Ox-3); fy = yof(xpk)
    line(ax, [fx, fx], [fy, fy+12], lw=1.6, sketch=False)         # wall
    line(ax, [fx, fx+7], [fy+12, fy+12], lw=1.6, sketch=False)
    lab(ax, fx+8.5, fy+12, "iron —", size=15, ha="left")
    lab(ax, fx+8.5, fy+7.5, "the ladder ends", size=13, ha="left", color=INK2)
    # past iron costs energy
    lab(ax, 80, 38, "past iron,\nfusion costs energy", size=12.5, color=INK2,
        ha="center")
    save(fig, "2-fusion-ladder.png")

# =====================================================================
# 3 — entanglement: blank parts, a definite relation
# =====================================================================
def fig_entangle():
    fig, ax = newfig(7.6, 4.0)
    cyA = 56
    ax_x, bx_x, r = 26, 74, 11
    # blank, dashed nodes
    for cx in (ax_x, bx_x):
        c = Circle((cx, cyA), r, fc="none", ec=INK, lw=1.3, ls=(0,(3,3)), zorder=3)
        ax.add_patch(c)
        lab(ax, cx, cyA, "?", size=30, it=False)
    # the definite relation: one firm bowed link
    t = np.linspace(0, 1, 80)
    lx = ax_x + r + (bx_x - ax_x - 2*r)*t
    ly = cyA - 7*np.sin(np.pi*t)
    line(ax, lx, ly, lw=1.8)
    # correlation marker on the link: up/down arrows
    mx = (ax_x+bx_x)/2; my = cyA - 7 - 0
    axis_arrow(ax, (mx-5, my-3.5), (mx-5, my+5.5), lw=1.2)   # up
    axis_arrow(ax, (mx+5, my+5.5), (mx+5, my-3.5), lw=1.2)   # down

    lab(ax, ax_x, cyA - r - 6, "each part alone:", size=14, color=INK2)
    lab(ax, ax_x, cyA - r - 11, "undefined", size=14)
    lab(ax, mx, cyA + 18, "the pair: definite", size=15.5)
    lab(ax, bx_x, cyA - r - 6, "each part alone:", size=14, color=INK2)
    lab(ax, bx_x, cyA - r - 11, "undefined", size=14)
    save(fig, "3-entanglement.png")

if __name__ == "__main__":
    fig_collapse()
    fig_fusion()
    fig_entangle()
    print("done")
