#!/bin/bash
#SBATCH --job-name=md_omp_sched
#SBATCH --partition=cpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=01:00:00
#SBATCH --output=logs/md_omp_sched_%j.out

# OpenMP schedule comparison: N=2000, 8 threads — loops, NOT array
module load gcc || true

mkdir -p results/md

export OMP_NUM_THREADS=8

for SCHED in static dynamic guided; do
    export OMP_SCHEDULE=$SCHED
    echo "=== Schedule=$SCHED ==="
    ./md_openmp -N 2000 -steps 500 -dt 0.005 -T_target 1.0 -rho 0.8 \
        -out data/sched_${SCHED}
done

echo "Schedule comparison complete."
