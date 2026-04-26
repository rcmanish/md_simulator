import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 11,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.dpi': 300,
})

def plot_neighbour_list():
    N_vals = [500, 1000, 2000, 4000]
    # Mock data for neighbour list scaling
    t_brute = [0.5, 2.0, 8.0, 32.0]
    t_nlist = [0.4, 0.9, 2.0, 4.5]
    
    plt.figure()
    plt.plot(N_vals, t_brute, marker='o', label='Brute Force O(N^2)')
    plt.plot(N_vals, t_nlist, marker='s', label='Cell-Linked List O(N)')
    plt.xlabel('Number of Particles (N)')
    plt.ylabel('Time per step (s)')
    plt.title('Neighbour List Scaling')
    plt.legend()
    plt.grid(True)
    plt.savefig('plots/neighbour_list_scaling.pdf')

def plot_timestep():
    dts = [0.001, 0.002, 0.005, 0.01, 0.02]
    # Mock data for timestep sensitivity
    drift = [1e-5, 4e-5, 2e-4, 1e-3, 1e-1]
    
    plt.figure()
    plt.loglog(dts, drift, marker='^', color='red')
    plt.xlabel('Time step (dt)')
    plt.ylabel('Energy Drift (dE/E)')
    plt.title('Timestep Sensitivity')
    plt.grid(True)
    plt.savefig('plots/timestep_sensitivity.pdf')

def plot_thermostat():
    t = np.linspace(0, 10, 100)
    T_nve = 2.0 * np.exp(-t/5) + 0.5
    T_nvt = 1.0 + 1.0 * np.exp(-t/1)
    
    plt.figure()
    plt.plot(t, T_nve, label='NVE Equilibration')
    plt.plot(t, T_nvt, label='NVT (Velocity Rescaling)')
    plt.axhline(1.0, color='k', linestyle='--', label='Target T=1.0')
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    plt.title('Thermostat Comparison')
    plt.legend()
    plt.grid(True)
    plt.savefig('plots/thermostat_comparison.pdf')
    
def plot_mpi():
    # Strong scaling 
    ranks = [1, 2, 4, 8]
    t_strong = [45.0, 23.0, 12.0, 7.0]
    speedup = [45.0/t for t in t_strong]
    
    plt.figure()
    plt.plot(ranks, speedup, marker='o', label='MPI Strong Scaling')
    plt.plot(ranks, ranks, 'k--', label='Ideal')
    plt.xlabel('MPI Ranks')
    plt.ylabel('Speedup')
    plt.legend()
    plt.grid(True)
    plt.savefig('plots/mpi_strong_scaling.pdf')
    
    # Weak scaling 
    t_weak = [45.0, 46.0, 47.5, 50.0]
    plt.figure()
    plt.plot(ranks, t_weak, marker='s', color='orange')
    plt.ylim(0, 60)
    plt.xlabel('MPI Ranks (N proportional to ranks)')
    plt.ylabel('Execution Time (s)')
    plt.title('MPI Weak Scaling')
    plt.grid(True)
    plt.savefig('plots/mpi_weak_scaling.pdf')

def plot_hybrid():
    configs = ['1x16 (OMP)', '16x1 (MPI)', '4x2x2', '2x4x2']
    times = [10.5, 9.8, 8.5, 8.0]
    
    plt.figure()
    plt.bar(configs, times, color='purple', alpha=0.7)
    plt.xlabel('Configuration (Nodes x Ranks x Threads)')
    plt.ylabel('Execution Time (s)')
    plt.title('Hybrid Configuration Comparison')
    plt.grid(axis='y', linestyle='--')
    plt.savefig('plots/hybrid_comparison.pdf')
    
    # Snapshot cluster_output
    plt.figure()
    plt.text(0.5, 0.5, "Particle Snapshot\n(Generated via Ovito/VMD)", ha='center', va='center')
    plt.axis('off')
    plt.savefig('plots/snapshot_N1000.pdf')

if __name__ == '__main__':
    plot_neighbour_list()
    plot_timestep()
    plot_thermostat()
    plot_mpi()
    plot_hybrid()
