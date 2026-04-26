#pragma once
#include "types.h"
#include <string>

// Write particle positions in XYZ format for visualisation
void write_xyz(const System& sys, int step, const std::string& filename);

// Append timestep, T, KE, PE, E_total, P to CSV
void write_thermo(const System& sys, int step, double time, const std::string& filename);
