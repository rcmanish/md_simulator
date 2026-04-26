#!/bin/bash
#SBATCH --job-name=md_n2_scaling
#SBATCH --partition=serial
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=01:00:00
#SBATCH --output=logs/md_n2scale_%j.out

# MD Serial N² scaling — loops over N values, NOT a job array
module load gcc || true

mkdir -p results/md

export OMP_NUM_THREADS=1

for N in 100 200 500 1000 2000 3000 5000; do
    echo "=== N²-scaling N=$N ==="
    START=$(date +%s%N)
    ./md_serial -N $N -steps 100 -dt 0.005 -T_target 1.0 -rho 0.8 \
        -out data/n2scale_N${N}
    END=$(date +%s%N)
    ELAPSED=$(echo "scale=6; ($END - $START) / 1000000000" | bc)
    echo "N=$N T_wall=${ELAPSED}s" >> data/serial_n2_scaling_cluster.txt
done

echo "N² scaling complete."
