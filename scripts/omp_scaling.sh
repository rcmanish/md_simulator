#!/bin/bash
#SBATCH --job-name=md_omp_scale
#SBATCH --partition=cpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --time=04:00:00
#SBATCH --output=logs/md_omp_%j.out

# MD OpenMP strong scaling — loops per thread count, NOT job array
module load gcc || true

mkdir -p results/md

for T in 1 2 4 8 16; do
    export OMP_NUM_THREADS=$T
    echo "=== OMP threads=$T ==="
    ./md_openmp -N 2000 -steps 500 -dt 0.005 -T_target 1.0 -rho 0.8 \
        -out data/omp_T${T}
done

echo "OpenMP scaling complete."
