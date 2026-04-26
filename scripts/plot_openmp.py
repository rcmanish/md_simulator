import pandas as pd
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

def plot_scaling():
    threads = []
    times = []
    with open('omp_scaling.txt', 'r') as f:
        next(f)
        for line in f:
            parts = line.strip().split()
            threads.append(int(parts[0]))
            times.append(float(parts[1]))
            
    t1 = times[0]
    speedup = [t1 / t for t in times]
    efficiency = [s / p for s, p in zip(speedup, threads)]
    
    plt.figure()
    plt.plot(threads, speedup, marker='o', label='Measured Speedup')
    plt.plot(threads, threads, linestyle='--', color='k', label='Ideal Speedup')
    plt.xlabel('Number of Threads')
    plt.ylabel('Speedup')
    plt.title('OpenMP Strong Scaling Speedup')
    plt.legend()
    plt.grid(True)
    plt.savefig('plots/openmp_speedup.pdf')
    
    plt.figure()
    plt.plot(threads, efficiency, marker='s', color='g', label='Efficiency')
    plt.axhline(1.0, linestyle='--', color='k')
    plt.xlabel('Number of Threads')
    plt.ylabel('Efficiency')
    plt.title('OpenMP Strong Scaling Efficiency')
    plt.legend()
    plt.grid(True)
    plt.savefig('plots/openmp_efficiency.pdf')

def plot_schedule():
    scheds = []
    times = []
    with open('omp_schedule.txt', 'r') as f:
        next(f)
        for line in f:
            parts = line.strip().split()
            scheds.append(parts[0])
            times.append(float(parts[1]))
            
    plt.figure()
    plt.bar(scheds, times, color=['blue', 'orange', 'green'])
    plt.xlabel('Schedule Type')
    plt.ylabel('Execution Time (s)')
    plt.title('OpenMP Schedule Comparison (8 Threads)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('plots/openmp_schedule_comparison.pdf')

if __name__ == '__main__':
    plot_scaling()
    plot_schedule()
