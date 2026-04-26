#!/bin/bash
#SBATCH --job-name=md_hybrid
#SBATCH --partition=mpi
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=4
#SBATCH --time=04:00:00
#SBATCH --output=logs/md_hybrid_%j.out

# MD Hybrid MPI+OpenMP — 5 configurations, NOT job array
module load gcc openmpi || true

mkdir -p results/md

SERIAL_T=5.430  # baseline serial time for N=2000, 500 steps

run_hybrid() {
    local label=$1 ranks=$2 threads=$3
    export OMP_NUM_THREADS=$threads
    echo "=== Hybrid: $label (${ranks}r×${threads}t) ==="
    mpirun -np $ranks --bind-to socket ./md_hybrid \
        -N 2000 -steps 500 -dt 0.005 -T_target 1.0 -rho 0.8 \
        -out data/hybrid_${label}
}

# Config A: pure OpenMP (1 rank, 16 threads)
run_hybrid A_1rx16t  1  16

# Config B: pure MPI on shared mem (16 ranks, 1 thread)
run_hybrid B_16rx1t  16  1

# Config C: 4×4 hybrid (best expected configuration)
run_hybrid C_4rx4t   4   4

# Config D: 2-node 4r×2t
run_hybrid D_4rx2t   4   2

# Config E: 2-node 2r×4t
run_hybrid E_2rx4t   2   4

echo "Hybrid study complete."
