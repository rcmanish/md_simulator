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

def plot_nve():
    df = pd.read_csv('verify_nve_thermo.csv')
    plt.figure()
    plt.plot(df['time'], df['pe'], label='Potential Energy')
    plt.plot(df['time'], df['ke'], label='Kinetic Energy')
    plt.plot(df['time'], df['etot'], label='Total Energy')
    plt.xlabel('Time')
    plt.ylabel('Energy')
    plt.title('Energy Conservation (NVE)')
    plt.legend()
    plt.savefig('plots/energy_conservation.pdf')

def plot_equil():
    df = pd.read_csv('verify_equil_thermo.csv')
    plt.figure()
    plt.plot(df['time'], df['temp'], label='Temperature')
    plt.axhline(2.0, color='r', linestyle='--', label='Target T=2.0')
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    plt.title('Temperature Equilibration')
    plt.legend()
    plt.savefig('plots/temperature_equilibration.pdf')

def plot_rdf():
    df = pd.read_csv('verify_rdf_rdf.csv')
    plt.figure()
    plt.plot(df['r'], df['g(r)'])
    plt.xlabel('r')
    plt.ylabel('g(r)')
    plt.title('Radial Distribution Function')
    plt.savefig('plots/rdf.pdf')

def plot_verlet():
    dts = []
    errors = []
    with open('verify_verlet.txt', 'r') as f:
        for line in f:
            if "error=" in line:
                parts = line.split()
                dt = float(parts[0].split('=')[1])
                err = float(parts[-1].split('=')[1])
                dts.append(dt)
                errors.append(err)
    plt.figure()
    plt.loglog(dts, errors, marker='o', label='Measured Error')
    
    # Reference 2nd order convergence line
    dts = np.array(dts)
    ref = errors[0] * (dts / dts[0])**2
    plt.loglog(dts, ref, linestyle='--', color='k', label='O(dt^2)')
    
    plt.xlabel('Time step (dt)')
    plt.ylabel('Position Error')
    plt.title('Velocity Verlet Convergence')
    plt.legend()
    plt.savefig('plots/timestep_convergence.pdf')

if __name__ == '__main__':
    plot_nve()
    plot_equil()
    plot_rdf()
    plot_verlet()
