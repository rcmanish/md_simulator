#pragma once
#include <vector>
#include <string>

struct System {
    int N;
    double L;
    double dt;
    double r_cutoff;
    double T_target;
    
    // Arrays of Structure vs Structure of Arrays (SoA is better for vectorization/MPI)
    std::vector<double> rx, ry, rz;
    std::vector<double> vx, vy, vz;
    std::vector<double> fx, fy, fz;
    std::vector<double> mass;
    
    // Observables
    double epot;
    double ekin;
    double temp;
    double press;
    double virial;

    System(int num_particles, double box_length, double time_step, double rc)
        : N(num_particles), L(box_length), dt(time_step), r_cutoff(rc),
          rx(N), ry(N), rz(N), vx(N), vy(N), vz(N), fx(N), fy(N), fz(N), mass(N, 1.0),
          epot(0.0), ekin(0.0), temp(0.0), press(0.0), virial(0.0) {}
};
