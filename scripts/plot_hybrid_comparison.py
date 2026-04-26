#!/usr/bin/env python3
"""
plot_md_hybrid_comparison.py
Bar chart: Speedup for 5 hybrid MPI+OpenMP configurations.
Y-axis = speedup (not raw time) relative to serial baseline.
"""
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd

mpl.rcParams.update({
    'font.family': 'serif', 'font.size': 11,
    'axes.labelsize': 11, 'axes.titlesize': 11,
    'xtick.labelsize': 9, 'ytick.labelsize': 10,
    'legend.fontsize': 10, 'lines.linewidth': 1.5,
    'lines.markersize': 5, 'figure.dpi': 300,
    'savefig.bbox': 'tight', 'savefig.dpi': 300,
    'axes.grid': True, 'grid.alpha': 0.3, 'grid.linestyle': '--',
})

df = pd.read_csv("data/hybrid_comparison.csv")
configs  = df["config"].values
speedups = df["speedup"].values.astype(float)

palette = ["#3a86ff", "#e06c1a", "#2d6a4f", "#8338ec", "#fb5607"]
best_idx = np.argmax(speedups)

fig, ax = plt.subplots(figsize=(7.5, 3.8))

bars = ax.bar(range(len(configs)), speedups, color=palette,
              edgecolor="k", linewidth=0.7, width=0.6)

# Highlight best
bars[best_idx].set_edgecolor("gold")
bars[best_idx].set_linewidth(2.5)

for bar, s in zip(bars, speedups):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
            f"{s:.2f}×", ha="center", va="bottom", fontsize=10, fontweight="bold")

ax.set_xticks(range(len(configs)))
ax.set_xticklabels(configs, rotation=20, ha="right", fontsize=9)
ax.set_ylabel("Speedup vs Serial Baseline (1r×1t)")
ax.set_title("Hybrid MPI+OpenMP Configuration Comparison\n(N=2000, 500 steps, measured cluster_output)")
ax.grid(axis="y", alpha=0.3, ls="--")
ax.grid(axis="x", visible=False)
ax.set_ylim(0, max(speedups) * 1.25)

# Winner annotation
ax.annotate(f"Best: {configs[best_idx]}\n({speedups[best_idx]:.2f}×)",
            xy=(best_idx, speedups[best_idx]),
            xytext=(best_idx + 0.5, speedups[best_idx] * 1.12),
            fontsize=9, color="darkgreen",
            arrowprops=dict(arrowstyle="->", color="darkgreen"))

fig.text(0.5, -0.04,
         "Config C (4r×4t) wins: fewer MPI ranks reduce Allreduce overhead;\n"
         "4 OMP threads per rank saturate shared L3 cache efficiently.",
         ha="center", fontsize=8, color="gray")

plt.tight_layout()
plt.savefig("plots/hybrid_speedup_comparison.pdf", dpi=300, bbox_inches="tight")
plt.savefig("plots/hybrid_comparison.pdf",            dpi=300, bbox_inches="tight")
print("Saved: hybrid_speedup_comparison.pdf")
