#!/usr/bin/env python3
"""
plot_md_energy_conservation.py
Fixed energy conservation plot with:
  - KE, PE, E_total on separate y-axes so KE is visible
  - Inset showing total energy drift percentage
  - Proper axis labels
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

df = pd.read_csv("data/nve_conservation_thermo.csv")
t   = df["time"].values
ke  = df["ke"].values
pe  = df["pe"].values
et  = df["etot"].values
N   = 256  # particles used in run

# Per-particle energies
ke_pp = ke / N
pe_pp = pe / N
et_pp = et / N

fig, ax1 = plt.subplots(figsize=(5, 3.8))

color_ke = "#e06c1a"
color_pe = "#3a86ff"
color_et = "#2d6a4f"

ax1.set_xlabel("Time (LJ units)")
ax1.set_ylabel("KE / N  (LJ units)", color=color_ke)
line_ke, = ax1.plot(t, ke_pp, color=color_ke, lw=1.5, label="KE/N")
ax1.tick_params(axis="y", labelcolor=color_ke)
ax1.set_ylim(0, max(ke_pp) * 1.4)

ax2 = ax1.twinx()
ax2.set_ylabel("PE/N, E$_{tot}$/N  (LJ units)", color=color_pe)
line_pe, = ax2.plot(t, pe_pp, color=color_pe, lw=1.5, label="PE/N")
line_et, = ax2.plot(t, et_pp, color=color_et, lw=2.0, ls="-", label="E$_{tot}$/N")
ax2.tick_params(axis="y", labelcolor=color_pe)

# Energy drift inset
e_mean = np.mean(et_pp)
drift_pct = (np.max(et_pp) - np.min(et_pp)) / np.abs(e_mean) * 100.0
inset = ax1.inset_axes([0.55, 0.72, 0.42, 0.25])
et_drift = (et_pp - np.mean(et_pp)) / np.abs(np.mean(et_pp)) * 100.0
inset.plot(t, et_drift, color=color_et, lw=1.0)
inset.axhline(0, color="k", lw=0.5, ls="--")
inset.set_xlabel("t", fontsize=8)
inset.set_ylabel("ΔE/|Ē| (%)", fontsize=8)
inset.tick_params(labelsize=7)
inset.set_title(f"Drift={drift_pct:.4f}%", fontsize=8)
inset.grid(True, alpha=0.3, ls="--")

lines = [line_ke, line_pe, line_et]
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc="lower right", fontsize=9)
ax1.set_title(f"NVE Energy Conservation  (N={N}, dt=0.005, T$_{{target}}$=2.0)")

plt.tight_layout()
plt.savefig("plots/energy_conservation.pdf", dpi=300, bbox_inches="tight")
plt.savefig("plots/energy_conservation.pdf",    dpi=300, bbox_inches="tight")
print(f"Saved: energy_conservation.pdf  (drift={drift_pct:.5f}%)")
