#!/usr/bin/env python3
"""Rough pencil/textbook sketches for the Quantum Gravity study guide.
Black on white, hand-drawn wiggle, almost no words."""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyArrowPatch, Polygon, Arc, Circle
from matplotlib.lines import Line2D
import os

fm.fontManager.addfont("/tmp/qg_fonts/BradleyHand.ttf")
HAND = "Bradley Hand"
mpl.rcParams["font.family"] = HAND
mpl.rcParams["axes.unicode_minus"] = False

INK = "#1f1d1b"
PAPER = "#ffffff"
OUT = "/Users/aidan/Desktop/writing-topology/img/quantum-gravity/pencil"
os.makedirs(OUT, exist_ok=True)

SK = dict(scale=1.7, length=55, randomness=2)

def newfig(w=6, h=6):
    fig = plt.figure(figsize=(w, h), dpi=200)
    fig.patch.set_facecolor(PAPER)
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.96])
    ax.set_facecolor(PAPER)
    ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax

def line(ax, xs, ys, lw=1.7, ls="-", color=INK, alpha=1.0):
    ln = Line2D(xs, ys, lw=lw, ls=ls, color=color, alpha=alpha,
                solid_capstyle="round")
    ln.set_sketch_params(**SK)
    ax.add_line(ln)
    return ln

def arrow(ax, p0, p1, lw=1.7, color=INK, ms=12):
    a = FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=ms,
                        color=color, lw=lw, shrinkA=0, shrinkB=0)
    a.set_sketch_params(**SK)
    ax.add_patch(a)
    return a

def circle(ax, cx, cy, r, lw=1.7, fill=None, alpha=1.0):
    c = Circle((cx, cy), r, fill=fill is not None, fc=fill if fill else "none",
               ec=INK, lw=lw, alpha=alpha)
    c.set_sketch_params(**SK)
    ax.add_patch(c)
    return c

def label(ax, x, y, s, size=20, color=INK, ha="center", va="center", rot=0):
    ax.text(x, y, s, family=HAND, fontsize=size, color=color, ha=ha, va=va,
            rotation=rot)

def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, dpi=200, facecolor=PAPER)
    plt.close(fig)
    print("wrote", p)

# =====================================================================
# A — light cones tip into the horizon
# =====================================================================
def fig_cones():
    fig, ax = newfig(7, 6)
    # baseline (the r axis), singularity at left, horizon dashed
    y0 = 22
    x_sing, x_hor, x_right = 14, 50, 92
    line(ax, [x_sing, x_right], [y0, y0], lw=1.5)            # r axis
    arrow(ax, (x_right-2, y0), (x_right+3, y0))              # axis arrowhead is decreasing r to left though
    # singularity: jagged vertical line
    ys = np.linspace(y0, 82, 22)
    xs = x_sing + 1.4*np.sin(ys*1.3)
    line(ax, xs, ys, lw=2.0)
    # horizon: dashed vertical
    line(ax, [x_hor, x_hor], [y0, 84], lw=1.6, ls=(0,(4,3)))

    def cone(x, y, phi_deg, half=24, size=15):
        phi = np.radians(phi_deg)
        for sgn in (-1, 1):
            a = phi + sgn*np.radians(half)
            line(ax, [x, x-np.sin(a)*size], [y, y+np.cos(a)*size], lw=1.6)
        # central future tick
        arrow(ax, (x, y), (x-np.sin(phi)*size*0.7, y+np.cos(phi)*size*0.7), ms=9)

    yc = 48
    cone(x_right-8, yc, 0)      # upright, far outside
    cone(67, yc, 25)           # tilting
    cone(x_hor, yc, 45)        # at horizon
    cone(36, yc, 68)           # inside
    cone(x_sing+13, yc, 86)    # near singularity, points inward

    # sparse labels
    label(ax, x_hor, 88, "horizon", size=19)
    label(ax, x_sing+2, 86, "singularity", size=19, ha="left")
    label(ax, x_right+1, y0-5, "r", size=20, ha="right")
    label(ax, 50, 11, "inside, the future points inward", size=17, color="#555")
    save(fig, "a-lightcones.png")

# =====================================================================
# B — collapse halted twice, then not (gravity vs pressure)
# =====================================================================
def fig_collapse():
    fig, ax = newfig(9.6, 4.8)
    cxs = [18, 50, 82]
    cy = 54
    radii = [10, 7, 3.8]
    names = ["white dwarf", "neutron star", "black hole"]
    for i, (cx, r, nm) in enumerate(zip(cxs, radii, names)):
        circle(ax, cx, cy, r)
        # inward gravity arrows (always) — black, from outside pointing in
        for ang in range(30, 360, 60):
            a = np.radians(ang)
            x1, y1 = cx + (r+6)*np.cos(a), cy + (r+6)*np.sin(a)
            x2, y2 = cx + (r+1.5)*np.cos(a), cy + (r+1.5)*np.sin(a)
            arrow(ax, (x1, y1), (x2, y2), lw=1.4, ms=8)
        if i < 2:
            # outward degeneracy pressure arrows (grey, push back)
            for ang in range(0, 360, 60):
                a = np.radians(ang)
                x1, y1 = cx + (r-2.5)*np.cos(a), cy + (r-2.5)*np.sin(a)
                x2, y2 = cx + (r+3.5)*np.cos(a), cy + (r+3.5)*np.sin(a)
                arrow(ax, (x1, y1), (x2, y2), lw=1.4, ms=8, color="#888")
        else:
            # black hole: horizon ring, no outward arrows, solid core dot
            circle(ax, cx, cy, r, lw=1.4)
            circle(ax, cx, cy, 1.3, fill=INK)
        label(ax, cx, cy - r - 11, nm, size=18)
    # tiny legend so B/W reads: black = gravity in, grey = pressure out
    label(ax, 50, 90, "gravity in", size=16)
    label(ax, 50, 84, "pressure out", size=16, color="#888")
    save(fig, "b-collapse.png")

# =====================================================================
# C — what's north of the North Pole?
# =====================================================================
def fig_northpole():
    fig, ax = newfig(6, 6.4)
    cx, cy, r = 50, 44, 30
    circle(ax, cx, cy, r)
    # a few longitude arcs
    for w in (0.45, 0.0):
        th = np.linspace(-90, 90, 60)
        xs = cx + r*w*np.cos(np.radians(th))*np.sign(np.cos(np.radians(th*0+1)))
        # simple ellipse meridian
        ex = cx + r*np.sin(np.radians(th))* (w if w>0 else 0.0)
    # meridians as ellipses
    for ww in (0.5,):
        t = np.linspace(0, 2*np.pi, 120)
        line(ax, cx + r*ww*np.cos(t), cy + r*np.sin(t), lw=1.3, color="#888")
    # equator
    t = np.linspace(0, 2*np.pi, 120)
    line(ax, cx + r*np.cos(t), cy + 0.32*r*np.sin(t), lw=1.3, color="#888")
    # north pole dot
    npx, npy = cx, cy + r
    ax.add_patch(Circle((npx, npy), 1.8, fc=INK, ec=INK))
    # arrow off the pole into nothing
    arrow(ax, (npx, npy+3), (npx, npy+18))
    label(ax, npx+3, npy+6, "N", size=20, ha="left")
    label(ax, cx, npy+24, "?", size=34)
    label(ax, 50, 7, '"what\'s north of here?"', size=18, color="#555")
    save(fig, "c-north-pole.png")

# =====================================================================
# D — bead -> ripple (the particle is a field excitation)
# =====================================================================
def fig_ripple():
    fig, ax = newfig(8.4, 4.2)
    # left: a bead, crossed out
    bx, by = 22, 52
    circle(ax, bx, by, 6, fill=INK)
    # big X (black, struck out)
    line(ax, [bx-14, bx+14], [by-14, by+14], lw=2.0)
    line(ax, [bx-14, bx+14], [by+14, by-14], lw=2.0)
    label(ax, bx, by-22, "particle", size=18)

    # arrow
    arrow(ax, (40, 52), (54, 52), ms=14)

    # right: a field line with a localized ripple (wave packet)
    x = np.linspace(60, 95, 300)
    env = np.exp(-((x-77.5)/5.0)**2)
    y = 52 + 11*env*np.sin((x-77.5)*1.6)
    line(ax, x, y, lw=1.8)
    line(ax, [60, 95], [52, 52], lw=1.0, ls=(0,(2,3)), color="#999")
    label(ax, 77.5, 30, "a ripple in a field", size=18)
    save(fig, "d-bead-to-ripple.png")

if __name__ == "__main__":
    fig_cones()
    fig_collapse()
    fig_northpole()
    fig_ripple()
    print("done")
