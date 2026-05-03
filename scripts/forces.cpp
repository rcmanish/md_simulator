#include "forces.h"
#include <cmath>
#include <vector>

#ifdef MODE_OPENMP
#include <omp.h>
#endif

void compute_forces(System& sys) {
    sys.epot = 0.0;
    sys.virial = 0.0;
    
    for (int i = 0; i < sys.N; ++i) {
        sys.fx[i] = 0.0;
        sys.fy[i] = 0.0;
        sys.fz[i] = 0.0;
    }
    
    double rc2 = sys.r_cutoff * sys.r_cutoff;
    double local_epot = 0.0;
    double local_virial = 0.0;
    
    int nc = std::floor(sys.L / sys.r_cutoff);
    if (nc < 3) nc = 3; // Ensure at least 3 cells for PBC
    double lc = sys.L / nc;
    
    std::vector<int> head(nc * nc * nc, -1);
    std::vector<int> lscl(sys.N, -1);
    
    double half_L = 0.5 * sys.L;
    
    // Build Cell-Linked List
    for (int i = 0; i < sys.N; ++i) {
        int cx = std::floor((sys.rx[i] + half_L) / lc);
        int cy = std::floor((sys.ry[i] + half_L) / lc);
        int cz = std::floor((sys.rz[i] + half_L) / lc);
        
        if (cx < 0) cx = 0; if (cx >= nc) cx = nc - 1;
        if (cy < 0) cy = 0; if (cy >= nc) cy = nc - 1;
        if (cz < 0) cz = 0; if (cz >= nc) cz = nc - 1;
        
        int c = cx + cy * nc + cz * nc * nc;
        lscl[i] = head[c];
        head[c] = i;
    }

#ifdef MODE_OPENMP
    #pragma omp parallel
    {
        std::vector<double> thread_fx(sys.N, 0.0);
        std::vector<double> thread_fy(sys.N, 0.0);
        std::vector<double> thread_fz(sys.N, 0.0);
        
        double thread_epot = 0.0;
        double thread_virial = 0.0;

        #pragma omp for schedule(dynamic)
        for (int i = 0; i < sys.N; ++i) {
            int cx = std::floor((sys.rx[i] + half_L) / lc);
            int cy = std::floor((sys.ry[i] + half_L) / lc);
            int cz = std::floor((sys.rz[i] + half_L) / lc);
            
            if (cx < 0) cx = 0; if (cx >= nc) cx = nc - 1;
            if (cy < 0) cy = 0; if (cy >= nc) cy = nc - 1;
            if (cz < 0) cz = 0; if (cz >= nc) cz = nc - 1;
            
            for (int dx_c = -1; dx_c <= 1; ++dx_c) {
                for (int dy_c = -1; dy_c <= 1; ++dy_c) {
                    for (int dz_c = -1; dz_c <= 1; ++dz_c) {
                        int nx = (cx + dx_c + nc) % nc;
                        int ny = (cy + dy_c + nc) % nc;
                        int nz = (cz + dz_c + nc) % nc;
                        
                        int c_adj = nx + ny * nc + nz * nc * nc;
                        int j = head[c_adj];
                        
                        while (j != -1) {
                            if (i < j) { // Newton's 3rd law
                                double dx = sys.rx[i] - sys.rx[j];
                                double dy = sys.ry[i] - sys.ry[j];
                                double dz = sys.rz[i] - sys.rz[j];
                                
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
                            j = lscl[j];
                        }
                    }
                }
            }
        }
        
        #pragma omp critical
        {
            local_epot += thread_epot;
            local_virial += thread_virial;
            for (int k = 0; k < sys.N; ++k) {
                sys.fx[k] += thread_fx[k];
                sys.fy[k] += thread_fy[k];
                sys.fz[k] += thread_fz[k];
            }
        }
    }
    sys.epot = local_epot;
    sys.virial = local_virial;
#else
    for (int i = 0; i < sys.N; ++i) {
        int cx = std::floor((sys.rx[i] + half_L) / lc);
        int cy = std::floor((sys.ry[i] + half_L) / lc);
        int cz = std::floor((sys.rz[i] + half_L) / lc);
        
        if (cx < 0) cx = 0; if (cx >= nc) cx = nc - 1;
        if (cy < 0) cy = 0; if (cy >= nc) cy = nc - 1;
        if (cz < 0) cz = 0; if (cz >= nc) cz = nc - 1;
        
        for (int dx_c = -1; dx_c <= 1; ++dx_c) {
            for (int dy_c = -1; dy_c <= 1; ++dy_c) {
                for (int dz_c = -1; dz_c <= 1; ++dz_c) {
                    int nx = (cx + dx_c + nc) % nc;
                    int ny = (cy + dy_c + nc) % nc;
                    int nz = (cz + dz_c + nc) % nc;
                    
                    int c_adj = nx + ny * nc + nz * nc * nc;
                    int j = head[c_adj];
                    
                    while (j != -1) {
                        if (i < j) {
                            double dx = sys.rx[i] - sys.rx[j];
                            double dy = sys.ry[i] - sys.ry[j];
                            double dz = sys.rz[i] - sys.rz[j];
                            
                            if (dx > half_L) dx -= sys.L; else if (dx < -half_L) dx += sys.L;
                            if (dy > half_L) dy -= sys.L; else if (dy < -half_L) dy += sys.L;
                            if (dz > half_L) dz -= sys.L; else if (dz < -half_L) dz += sys.L;
                            
                            double r2 = dx*dx + dy*dy + dz*dz;
                            
                            if (r2 < rc2) {
                                double r2inv = 1.0 / r2;
                                double r6inv = r2inv * r2inv * r2inv;
                                double r12inv = r6inv * r6inv;
                                
                                local_epot += 4.0 * (r12inv - r6inv);
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
                                
                                local_virial += force_mag * r2;
                            }
                        }
                        j = lscl[j];
                    }
                }
            }
        }
    }
    sys.epot = local_epot;
    sys.virial = local_virial;
#endif
}
