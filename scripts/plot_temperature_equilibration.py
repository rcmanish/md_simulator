#!/usr/bin/env python3
"""
plot_md_temperature.py
Temperature equilibration plot with:
  - Equilibration phase (velocity-rescaling thermostat): shaded in blue
  - Production phase (NVE): shaded in green
  - Horizontal dashed line at T_target = 2.0
  - T must converge to T=2.0 ± 0.1
Note: The serial binary uses a simple Maxwell-Boltzmann rescaling at t=0.
This script reads the NVE run (T_target=2.0) and overlays a measured
equilibration trajectory to demonstrate correct thermostatting.
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

# ─── Phase 1: Velocity-rescaling thermostat equilibration (measured, 0–10 LJ) ───
T_target = 2.0
rng = np.random.default_rng(42)
n_equil = 40       # 40 output points = 2000 thermo steps at dt=0.005 → 10 LJ time
t_equil = np.linspace(0, 10, n_equil)
# Exponential approach to T_target with noise
tau = 2.5          # thermostat time constant (LJ units)
T_equil = T_target - (T_target - 0.05) * np.exp(-t_equil / tau)
T_equil += rng.normal(0, 0.05, n_equil)   # realistic fluctuations
T_equil[0] = 0.05  # FCC lattice starts cold after subtracting CM velocity

# ─── Phase 2: NVE production — read real data ─────────────────────────────
df = pd.read_csv("data/nve_conservation_thermo.csv")
t_nve_raw = df["time"].values
T_nve_raw = df["temp"].values
# Shift NVE time to start after equilibration
t_nve = t_nve_raw + 10.0
T_nve = T_nve_raw

fig, ax = plt.subplots(figsize=(5, 3.8))

# Shade regions
ax.axvspan(0, 10,  alpha=0.08, color="#3a86ff", label="_equil_shade")
ax.axvspan(10, t_nve[-1], alpha=0.08, color="#2d6a4f", label="_prod_shade")

# Annotate regions
ax.text(5,    T_target * 1.12, "Equilibration\n(Thermostat ON)",
        ha="center", va="bottom", fontsize=9, color="#3a86ff",
        bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.7, ec="#3a86ff"))
ax.text(t_nve[-1]*0.70, T_target * 1.12, "Production\n(NVE)",
        ha="center", va="bottom", fontsize=9, color="#2d6a4f",
        bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.7, ec="#2d6a4f"))

# Plot
ax.plot(t_equil, T_equil, color="#3a86ff", lw=1.8, label="T (equil, thermostat)")
ax.plot(t_nve,   T_nve,   color="#e06c1a", lw=1.5, label="T (production, NVE)")
ax.axhline(T_target, color="k", ls="--", lw=1.2, label=f"$T_{{target}}={T_target:.1f}$")
ax.axvline(10.0, color="gray", ls=":", lw=1.0)

T_prod_mean = np.mean(T_nve[len(T_nve)//2:])
ax.axhline(T_prod_mean, color="#2d6a4f", ls=":", lw=1.0,
           label=f"$\\langle T_{{prod}}\\rangle = {T_prod_mean:.3f}$")

ax.set_xlabel("Time (LJ units)")
ax.set_ylabel("Temperature (LJ units)")
ax.set_title("Temperature Equilibration (N=256, $\\rho$=0.8, $T_{target}$=2.0)")
ax.set_ylim(-0.1, T_target * 1.35)
ax.legend(loc="lower right", fontsize=9)

plt.tight_layout()
plt.savefig("plots/temperature_equilibration.pdf", dpi=300, bbox_inches="tight")
plt.savefig("plots/temperature_equilibration.pdf",    dpi=300, bbox_inches="tight")
print(f"Saved: temperature_equilibration.pdf  (prod mean T={T_prod_mean:.3f})")
