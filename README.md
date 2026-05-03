# 3D Lennard-Jones Molecular Dynamics Simulator

This repository contains a high-performance 3D Molecular Dynamics (MD) simulator implemented in C++ with OpenMP and MPI parallelisation. It evaluates $O(N^2)$ pairwise Lennard-Jones interactions and uses velocity Verlet integration.

## Repository Structure
- `/scripts/`: Core C++ source code, headers, Python plotting scripts, and SLURM job submission scripts.
- `/plots/`: Generated publication-quality visualizations.
- `/reports/`: LaTeX source and compiled PDF for the technical white paper.
- `/data/`: Performance and validation metrics (CSVs).

## Prerequisites
- **Compiler**: GCC with C++17 support (`g++`)
- **Parallelization**: OpenMP (built into GCC), MPI (`mpicxx`, e.g., OpenMPI)
- **Plotting**: Python 3 with `matplotlib`, `numpy`, and `pandas`

## Build and Run Instructions

### 1. Local Execution (Serial & OpenMP)
To build and run the simulator locally on your machine:
```bash
cd scripts
# Compile the serial and OpenMP versions
g++ -O3 -std=c++17 -fopenmp main.cpp forces.cpp particles.cpp integrator.cpp io.cpp utils.cpp analysis.cpp -o md_sim

# Run the simulation (e.g., N=1000, 500 steps, 4 threads)
OMP_NUM_THREADS=4 ./md_sim 1000 500
```

### 2. Cluster Execution (SLURM)
To execute the benchmarking suite on an HPC cluster managed by SLURM:
```bash
cd scripts
# The repository provides dedicated batch scripts for each study:
sbatch mpi_strong.sh
sbatch mpi_weak.sh
sbatch omp_scaling.sh
sbatch hybrid_study.sh
```
*Note: Make sure to load the required modules (e.g., `module load gcc openmpi`) before submitting jobs.*

## Reproducing Figures
All figures in the technical report are generated from the CSV data in `/data/`. To reproduce the plots:
```bash
cd scripts
# Generate all OpenMP, MPI, and Hybrid scaling plots
python3 plot_md_corrected.py

# Generate physical verification plots
python3 plot_energy_conservation.py
python3 plot_temperature_equilibration.py
python3 plot_verification.py
```
The resulting PDF files will be saved directly into the `/plots/` directory.
