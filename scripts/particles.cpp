#include "particles.h"
#include <cmath>
#include <random>

void initialize_fcc(System& sys, double rho, double T_target) {
    // Determine number of unit cells in each dimension
    int nc = std::ceil(std::pow(sys.N / 4.0, 1.0 / 3.0));
    sys.L = std::pow(sys.N / rho, 1.0 / 3.0);
    double a = sys.L / nc; // lattice constant
    
    int p = 0;
    for (int ix = 0; ix < nc; ++ix) {
        for (int iy = 0; iy < nc; ++iy) {
            for (int iz = 0; iz < nc; ++iz) {
                double basex = ix * a;
                double basey = iy * a;
                double basez = iz * a;
                
                // 4 particles per FCC unit cell
                double pos[4][3] = {
                    {0.0, 0.0, 0.0},
                    {0.5, 0.5, 0.0},
                    {0.5, 0.0, 0.5},
                    {0.0, 0.5, 0.5}
                };
                
                for (int i = 0; i < 4; ++i) {
                    if (p < sys.N) {
                        sys.rx[p] = basex + pos[i][0] * a;
                        sys.ry[p] = basey + pos[i][1] * a;
                        sys.rz[p] = basez + pos[i][2] * a;
                        p++;
                    }
                }
            }
        }
    }

    // Assign Maxwell-Boltzmann velocities
    std::mt19937 gen(42); // fixed seed for reproducibility
    std::normal_distribution<double> dist(0.0, 1.0);
    
    double v_cm[3] = {0.0, 0.0, 0.0};
    for (int i = 0; i < sys.N; ++i) {
        sys.vx[i] = dist(gen);
        sys.vy[i] = dist(gen);
        sys.vz[i] = dist(gen);
        
        v_cm[0] += sys.vx[i];
        v_cm[1] += sys.vy[i];
        v_cm[2] += sys.vz[i];
    }
    
    // Remove center of mass velocity
    v_cm[0] /= sys.N; v_cm[1] /= sys.N; v_cm[2] /= sys.N;
    
    double ekin = 0.0;
    for (int i = 0; i < sys.N; ++i) {
        sys.vx[i] -= v_cm[0];
        sys.vy[i] -= v_cm[1];
        sys.vz[i] -= v_cm[2];
        
        ekin += 0.5 * sys.mass[i] * (sys.vx[i]*sys.vx[i] + sys.vy[i]*sys.vy[i] + sys.vz[i]*sys.vz[i]);
    }
    
    // Rescale to target temperature
    double current_temp = 2.0 * ekin / (3.0 * sys.N);
    double scale = std::sqrt(T_target / current_temp);
    
    for (int i = 0; i < sys.N; ++i) {
        sys.vx[i] *= scale;
        sys.vy[i] *= scale;
        sys.vz[i] *= scale;
    }
}

void apply_pbc(System& sys) {
    for (int i = 0; i < sys.N; ++i) {
        if (sys.rx[i] < 0.0) sys.rx[i] += sys.L;
        if (sys.rx[i] >= sys.L) sys.rx[i] -= sys.L;
        
        if (sys.ry[i] < 0.0) sys.ry[i] += sys.L;
        if (sys.ry[i] >= sys.L) sys.ry[i] -= sys.L;
        
        if (sys.rz[i] < 0.0) sys.rz[i] += sys.L;
        if (sys.rz[i] >= sys.L) sys.rz[i] -= sys.L;
    }
}
