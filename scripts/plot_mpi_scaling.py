#!/usr/bin/env python3
"""
plot_md_mpi_scaling.py
Two-panel plot:
  - Left:  MPI strong scaling speedup + efficiency
  - Right: MPI weak scaling (E_weak vs ranks)
"""
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd

mpl.rcParams.update({
    'font.family': 'serif', 'font.size': 11,
    'axes.labelsize': 11, 'axes.titlesize': 11,
    'xtick.labelsize': 10, 'ytick.labelsize': 10,
    'legend.fontsize': 10, 'lines.linewidth': 1.5,
    'lines.markersize': 5, 'figure.dpi': 300,
    'savefig.bbox': 'tight', 'savefig.dpi': 300,
    'axes.grid': True, 'grid.alpha': 0.3, 'grid.linestyle': '--',
})

# ── Strong scaling ─────────────────────────────────────────────────────────
ds = pd.read_csv("data/mpi_strong.csv")
P  = ds["ranks"].values.astype(float)
S  = ds["speedup"].values.astype(float)
E  = ds["efficiency"].values.astype(float)

# ── Weak scaling ───────────────────────────────────────────────────────────
dw = pd.read_csv("data/mpi_weak.csv")
Pw = dw["ranks"].values.astype(float)
Ew = dw["efficiency_weak"].values.astype(float)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.5, 3.5))

# ── Strong speedup + efficiency (twin axes) ────────────────────────────────
color_S = "#3a86ff"
color_E = "#e06c1a"

ax1.plot(P, P, "k--", alpha=0.5, lw=1.2, label="Ideal speedup")
line_S = ax1.plot(P, S, "o-", color=color_S, lw=2.0, ms=7, label="Speedup $S(P)$")
ax1.set_xlabel("MPI Ranks $P$")
ax1.set_ylabel("Speedup $S(P)$", color=color_S)
ax1.tick_params(axis="y", labelcolor=color_S)
ax1.set_xticks(P)

ax1b = ax1.twinx()
line_E = ax1b.plot(P, E, "s--", color=color_E, lw=1.8, ms=6, label="Efficiency $E(P)$")
ax1b.axhline(1.0, color=color_E, ls=":", alpha=0.4, lw=0.8)
ax1b.set_ylabel("Efficiency $E(P) = S/P$", color=color_E)
ax1b.tick_params(axis="y", labelcolor=color_E)
ax1b.set_ylim(0, 1.15)

lines_all  = line_S + line_E
labels_all = [l.get_label() for l in lines_all]
ax1.legend(lines_all + [plt.Line2D([],[],color="k",ls="--",lw=1.2,alpha=0.5)],
           labels_all + ["Ideal speedup"], loc="upper left", fontsize=9)
ax1.set_title("MPI Strong Scaling\n(N=2000, 500 steps, measured cluster_output)")

# ── Weak scaling ───────────────────────────────────────────────────────────
ax2.axhline(1.0, color="k", ls="--", alpha=0.5, lw=1.2, label="Ideal ($E_w=1$)")
ax2.plot(Pw, Ew, "D-", color="#2d6a4f", lw=2.0, ms=7, label="Weak efficiency")
ax2.set_xlabel("MPI Ranks $P$")
ax2.set_ylabel("Weak Scaling Efficiency $E_w = T_1/T_P$")
ax2.set_title("MPI Weak Scaling\n($N=500 \\times P$, measured cluster_output)")
ax2.set_xticks(Pw)
ax2.set_ylim(0, 1.15)
ax2.legend(fontsize=9)

plt.tight_layout()
plt.savefig("plots/mpi_strong_efficiency.pdf", dpi=300, bbox_inches="tight")
plt.savefig("plots/mpi_weak_scaling.pdf",      dpi=300, bbox_inches="tight")
plt.savefig("plots/mpi_strong_scaling.pdf",        dpi=300, bbox_inches="tight")
plt.savefig("plots/mpi_weak_scaling.pdf",          dpi=300, bbox_inches="tight")
print("Saved: mpi_strong_efficiency.pdf, mpi_weak_scaling.pdf")
