#!/usr/bin/env python3
"""
plot_md_omp_schedule_comparison.py
Bar chart comparison of OpenMP scheduling strategies.
Real data: N=2000, 8 threads, 500 steps.
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

df = pd.read_csv("data/schedule_comparison.csv")
scheds = df["schedule"].values
times  = df["T_wall_s"].values
speedups = df["speedup_vs_static"].values

colors = {"static": "#3a86ff", "dynamic": "#e06c1a", "guided": "#2d6a4f"}
bar_colors = [colors.get(s, "gray") for s in scheds]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.5, 3.5))

# Wall time
bars = ax1.bar(scheds, times, color=bar_colors, edgecolor="k", linewidth=0.7, width=0.5)
for bar, t in zip(bars, times):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
             f"{t:.3f}s", ha="center", va="bottom", fontsize=10)
ax1.set_xlabel("OpenMP Schedule")
ax1.set_ylabel("Wall Time (s)")
ax1.set_title("Wall Time by Schedule\n(N=2000, 8 threads, 500 steps)")
ax1.grid(axis="y", alpha=0.3, ls="--")
ax1.grid(axis="x", visible=False)

# Speedup vs static
bars2 = ax2.bar(scheds, speedups, color=bar_colors, edgecolor="k", linewidth=0.7, width=0.5)
for bar, s in zip(bars2, speedups):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
             f"{s:.3f}×", ha="center", va="bottom", fontsize=10)
ax2.axhline(1.0, color="k", ls="--", lw=1.0, alpha=0.6, label="Static baseline")
ax2.set_xlabel("OpenMP Schedule")
ax2.set_ylabel("Speedup vs static")
ax2.set_title("Relative Speedup vs Static\n(N=2000, 8 threads, 500 steps)")
ax2.grid(axis="y", alpha=0.3, ls="--")
ax2.grid(axis="x", visible=False)
ax2.legend(fontsize=9)

# Physical explanation as figure note
fig.text(0.5, -0.04,
         "Note: dynamic fastest due to non-uniform row lengths in upper-triangle N(N-1)/2 loop.\n"
         "Static has slight load imbalance; guided overhead dominates over static gains.",
         ha="center", fontsize=8, color="gray")

plt.tight_layout()
plt.savefig("plots/omp_schedule_comparison.pdf", dpi=300, bbox_inches="tight")
plt.savefig("plots/openmp_schedule_comparison.pdf",  dpi=300, bbox_inches="tight")
print("Saved: omp_schedule_comparison.pdf")
