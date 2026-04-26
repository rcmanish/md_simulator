#!/usr/bin/env python3
"""
plot_md_omp_speedup_efficiency.py
Two-panel plot:
  - Left:  Speedup S(p) vs p with Amdahl fit
  - Right: Efficiency E(p) = S(p)/p vs p
"""
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

mpl.rcParams.update({
    'font.family': 'serif', 'font.size': 11,
    'axes.labelsize': 11, 'axes.titlesize': 11,
    'xtick.labelsize': 10, 'ytick.labelsize': 10,
    'legend.fontsize': 10, 'lines.linewidth': 1.5,
    'lines.markersize': 5, 'figure.dpi': 300,
    'savefig.bbox': 'tight', 'savefig.dpi': 300,
    'axes.grid': True, 'grid.alpha': 0.3, 'grid.linestyle': '--',
})

df = pd.read_csv("data/omp_scaling.csv")
p  = df["threads"].values.astype(float)
S  = df["speedup"].values.astype(float)
E  = df["efficiency"].values.astype(float)

# Amdahl's law fit:  S(p) = 1 / (f + (1-f)/p)
def amdahl(p_arr, f):
    return 1.0 / (f + (1.0 - f) / p_arr)

popt, _ = curve_fit(amdahl, p, S, p0=[0.05], bounds=(0, 0.99))
f_serial = popt[0]
S_max    = 1.0 / f_serial

p_fit = np.linspace(1, 20, 200)
S_fit = amdahl(p_fit, f_serial)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.5, 3.5))

# ── Speedup panel ──────────────────────────────────────────────────────────
ax1.plot(p, p, "k--", alpha=0.5, lw=1.2, label="Ideal (linear)")
ax1.plot(p_fit, S_fit, "r-", lw=1.5, alpha=0.8,
         label=f"Amdahl fit\n$f_{{ser}}$={f_serial*100:.1f}%, $S_{{max}}$={S_max:.1f}×")
ax1.plot(p, S, "o-", color="#3a86ff", lw=2.0, ms=7, label="Measured")
ax1.set_xlabel("Threads $p$")
ax1.set_ylabel("Speedup $S(p)$")
ax1.set_title("OpenMP Strong Scaling Speedup\n(N=2000, steps=500)")
ax1.set_xticks(p)
ax1.legend(fontsize=9)

# ── Efficiency panel ───────────────────────────────────────────────────────
ax2.axhline(1.0, color="k", ls="--", alpha=0.5, lw=1.2, label="Ideal (E=1)")
E_amdahl = amdahl(p_fit, f_serial) / p_fit
ax2.plot(p_fit, E_amdahl, "r-", lw=1.5, alpha=0.8, label="Amdahl fit")
ax2.plot(p, E, "s-", color="#e06c1a", lw=2.0, ms=7, label="Measured")
ax2.set_xlabel("Threads $p$")
ax2.set_ylabel("Efficiency $E(p) = S(p)/p$")
ax2.set_title("OpenMP Parallel Efficiency\n(N=2000, steps=500)")
ax2.set_xticks(p)
ax2.set_ylim(0, 1.15)
ax2.legend(fontsize=9)

plt.tight_layout()
plt.savefig("plots/omp_speedup_efficiency.pdf", dpi=300, bbox_inches="tight")
plt.savefig("plots/openmp_efficiency.pdf",          dpi=300, bbox_inches="tight")
print(f"Saved: omp_speedup_efficiency.pdf")
print(f"Amdahl: f_serial = {f_serial*100:.2f}%, S_max = {S_max:.2f}x")
