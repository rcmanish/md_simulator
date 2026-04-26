#!/usr/bin/env python3
"""
plot_md_serial_n2_scaling.py
Log-log plot of serial wall time vs N with:
  - O(N²) reference line
  - Power-law fit to extract exponent α
"""
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
from scipy.stats import linregress

mpl.rcParams.update({
    'font.family': 'serif', 'font.size': 11,
    'axes.labelsize': 11, 'axes.titlesize': 11,
    'xtick.labelsize': 10, 'ytick.labelsize': 10,
    'legend.fontsize': 10, 'lines.linewidth': 1.5,
    'lines.markersize': 5, 'figure.dpi': 300,
    'savefig.bbox': 'tight', 'savefig.dpi': 300,
    'axes.grid': True, 'grid.alpha': 0.3, 'grid.linestyle': '--',
})

df = pd.read_csv("data/serial_n2_scaling.csv")
N  = df["N"].values.astype(float)
T  = df["T_wall_s"].values.astype(float)

# Power-law fit in log space
slope, intercept, r, _, _ = linregress(np.log10(N), np.log10(T))
alpha = slope
C = 10**intercept

N_fit = np.logspace(np.log10(N.min()), np.log10(N.max()*1.2), 200)
T_fit = C * N_fit**alpha

# O(N²) reference
C_ref = T[-1] / N[-1]**2
T_ref = C_ref * N_fit**2

fig, ax = plt.subplots(figsize=(5, 3.8))
ax.loglog(N, T, "o", color="#3a86ff", ms=8, label="Measured")
ax.loglog(N_fit, T_fit, "-",  color="#3a86ff", lw=2.0,
          label=f"Fit: $T \\propto N^{{{alpha:.2f}}}$ ($R^2={r**2:.4f}$)")
ax.loglog(N_fit, T_ref, "r--", lw=1.5, alpha=0.7, label="$O(N^2)$ reference")

ax.set_xlabel("Number of Particles $N$")
ax.set_ylabel("Wall Time $T$ (s)   [100 steps]")
ax.set_title(f"Serial Complexity Verification\n($T \\propto N^{{{alpha:.3f}}}$, expected $N^2$)")
ax.legend(fontsize=9)

plt.tight_layout()
plt.savefig("plots/serial_n2_scaling.pdf", dpi=300, bbox_inches="tight")
print(f"Saved: serial_n2_scaling.pdf  (fitted alpha = {alpha:.4f})")
