#!/bin/bash
#SBATCH --job-name=md_mpi_weak
#SBATCH --partition=mpi
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=04:00:00
#SBATCH --output=logs/md_mpi_weak_%j.out

# MD MPI weak scaling: N = 500 * P — loops per rank count, NOT job array
module load gcc openmpi || true

mkdir -p results/md

for P in 1 2 4 8; do
    N=$((500 * P))
    echo "=== MPI weak P=$P N=$N ==="
    mpirun -np $P ./md_mpi -N $N -steps 500 -dt 0.005 -T_target 1.0 -rho 0.8 \
        -out data/mpi_weak_P${P}
done

echo "MPI weak scaling complete."
