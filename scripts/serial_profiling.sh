#!/bin/bash
#SBATCH --job-name=md_serial_profile
#SBATCH --partition=serial
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=02:00:00
#SBATCH --output=logs/md_serial_%j.out

# MD Serial profiling — runs for each N without --array (serial queue restriction)
module load gcc || true

mkdir -p results/md

export OMP_NUM_THREADS=1

# Profiling: N = 100..2000, 500 steps each
for N in 100 200 500 1000 2000; do
    echo "=== Profiling N=$N ==="
    ./md_serial -N $N -steps 500 -dt 0.005 -T_target 1.0 -rho 0.8 \
        -out data/prof_N${N}
done
echo "Serial profiling complete."
