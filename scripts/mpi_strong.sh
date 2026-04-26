#!/bin/bash
#SBATCH --job-name=md_mpi_strong
#SBATCH --partition=mpi
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=04:00:00
#SBATCH --output=logs/md_mpi_strong_%j.out

# MD MPI strong scaling — loops per rank count, NOT job array
module load gcc openmpi || true

mkdir -p results/md

for P in 1 2 4 8; do
    echo "=== MPI strong P=$P ==="
    mpirun -np $P ./md_mpi -N 2000 -steps 500 -dt 0.005 -T_target 1.0 -rho 0.8 \
        -out data/mpi_strong_P${P}
done

echo "MPI strong scaling complete."
