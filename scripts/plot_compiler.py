import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys

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

def main():
    opts = []
    times = []
    with open('compile_times.txt', 'r') as f:
        next(f) # skip header
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                # Reconstruct opt name (handles spaces like "-O3 -march=native")
                opt = " ".join(parts[:-1]).replace('"', '')
                t = float(parts[-1])
                opts.append(opt)
                times.append(t)
    
    speedups = [times[0] / t for t in times]
    
    plt.figure()
    plt.bar(opts, speedups, color='skyblue', edgecolor='black')
    plt.ylabel('Speedup relative to -O0')
    plt.xlabel('Compiler Flag')
    plt.title('Compiler Optimisation Study')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.savefig('plots/compiler_optimisation.pdf')

if __name__ == '__main__':
    main()
