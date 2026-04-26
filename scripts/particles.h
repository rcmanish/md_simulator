#pragma once
#include "types.h"

// Place particles on FCC lattice and assign Maxwell-Boltzmann velocities
void initialize_fcc(System& sys, double rho, double T_target);

// Wrap positions into periodic box
void apply_pbc(System& sys);
