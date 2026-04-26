#pragma once
#include "types.h"

// Half-step velocity update
void velocity_verlet_half(System& sys);

// Full position + second half-step
void velocity_verlet_full(System& sys);

// Compute KE = 0.5 * sum(m * v^2)
void compute_kinetic_energy(System& sys);

// Compute T = 2*KE / (3*N*k_B)  (k_B = 1)
void compute_temperature(System& sys);

// Compute pressure via Virial theorem
void compute_pressure(System& sys, double rho);
