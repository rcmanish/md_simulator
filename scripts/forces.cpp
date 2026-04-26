#include "forces.h"
#include <cmath>

#ifdef MODE_OPENMP
#include <omp.h>
#endif

void compute_forces(System& sys) {
    sys.epot = 0.0;
    sys.virial = 0.0;
    
    // Reset forces
    for (int i = 0; i < sys.N; ++i) {
        sys.fx[i] = 0.0;
        sys.fy[i] = 0.0;
        sys.fz[i] = 0.0;
    }
    
    double rc2 = sys.r_cutoff * sys.r_cutoff;
    double local_epot = 0.0;
    double local_virial = 0.0;
    
#ifdef MODE_OPENMP
    #pragma omp parallel
    {
        int nthreads = omp_get_num_threads();
        int tid = omp_get_thread_num();
        
        std::vector<double> thread_fx(sys.N, 0.0);
        std::vector<double> thread_fy(sys.N, 0.0);
        std::vector<double> thread_fz(sys.N, 0.0);
        
        double thread_epot = 0.0;
        double thread_virial = 0.0;

        #pragma omp for schedule(runtime)
        for (int i = 0; i < sys.N - 1; ++i) {
            for (int j = i + 1; j < sys.N; ++j) {
                double dx = sys.rx[i] - sys.rx[j];
                double dy = sys.ry[i] - sys.ry[j];
                double dz = sys.rz[i] - sys.rz[j];
                
                double half_L = 0.5 * sys.L;
                if (dx > half_L) dx -= sys.L; else if (dx < -half_L) dx += sys.L;
                if (dy > half_L) dy -= sys.L; else if (dy < -half_L) dy += sys.L;
                if (dz > half_L) dz -= sys.L; else if (dz < -half_L) dz += sys.L;
                
                double r2 = dx*dx + dy*dy + dz*dz;
                
                if (r2 < rc2) {
                    double r2inv = 1.0 / r2;
                    double r6inv = r2inv * r2inv * r2inv;
                    double r12inv = r6inv * r6inv;
                    
                    thread_epot += 4.0 * (r12inv - r6inv);
                    double force_mag = 24.0 * r2inv * (2.0 * r12inv - r6inv);
                    
                    double fx = force_mag * dx;
                    double fy = force_mag * dy;
                    double fz = force_mag * dz;
                    
                    thread_fx[i] += fx;
                    thread_fy[i] += fy;
                    thread_fz[i] += fz;
                    
                    thread_fx[j] -= fx;
                    thread_fy[j] -= fy;
                    thread_fz[j] -= fz;
                    
                    thread_virial += force_mag * r2;
                }
            }
        }
        
        #pragma omp critical
        {
            local_epot += thread_epot;
            local_virial += thread_virial;
            for (int i = 0; i < sys.N; ++i) {
                sys.fx[i] += thread_fx[i];
                sys.fy[i] += thread_fy[i];
                sys.fz[i] += thread_fz[i];
            }
        }
    }
    sys.epot = local_epot;
    sys.virial = local_virial;
#else
    for (int i = 0; i < sys.N - 1; ++i) {
        for (int j = i + 1; j < sys.N; ++j) {
            double dx = sys.rx[i] - sys.rx[j];
            double dy = sys.ry[i] - sys.ry[j];
            double dz = sys.rz[i] - sys.rz[j];
            
            double half_L = 0.5 * sys.L;
            if (dx > half_L) dx -= sys.L; else if (dx < -half_L) dx += sys.L;
            if (dy > half_L) dy -= sys.L; else if (dy < -half_L) dy += sys.L;
            if (dz > half_L) dz -= sys.L; else if (dz < -half_L) dz += sys.L;
            
            double r2 = dx*dx + dy*dy + dz*dz;
            
            if (r2 < rc2) {
                double r2inv = 1.0 / r2;
                double r6inv = r2inv * r2inv * r2inv;
                double r12inv = r6inv * r6inv;
                
                sys.epot += 4.0 * (r12inv - r6inv);
                double force_mag = 24.0 * r2inv * (2.0 * r12inv - r6inv);
                
                double fx = force_mag * dx;
                double fy = force_mag * dy;
                double fz = force_mag * dz;
                
                sys.fx[i] += fx;
                sys.fy[i] += fy;
                sys.fz[i] += fz;
                
                sys.fx[j] -= fx;
                sys.fy[j] -= fy;
                sys.fz[j] -= fz;
                
                sys.virial += force_mag * r2;
            }
        }
    }
#endif
}
