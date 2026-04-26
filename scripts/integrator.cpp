#include "integrator.h"
#include "particles.h"
#include "forces.h"

void velocity_verlet_half(System& sys) {
    double dt_half = 0.5 * sys.dt;
    for (int i = 0; i < sys.N; ++i) {
        double m_inv = 1.0 / sys.mass[i];
        sys.vx[i] += sys.fx[i] * m_inv * dt_half;
        sys.vy[i] += sys.fy[i] * m_inv * dt_half;
        sys.vz[i] += sys.fz[i] * m_inv * dt_half;
    }
}

#include "utils.h"

extern double t_forces;
extern double t_verlet;
extern double t_pbc;

void velocity_verlet_full(System& sys) {
    double t0 = get_wtime();
    // 1. First half-step velocity update & position update
    double dt_half = 0.5 * sys.dt;
    for (int i = 0; i < sys.N; ++i) {
        double m_inv = 1.0 / sys.mass[i];
        sys.vx[i] += sys.fx[i] * m_inv * dt_half;
        sys.vy[i] += sys.fy[i] * m_inv * dt_half;
        sys.vz[i] += sys.fz[i] * m_inv * dt_half;
        
        sys.rx[i] += sys.vx[i] * sys.dt;
        sys.ry[i] += sys.vy[i] * sys.dt;
        sys.rz[i] += sys.vz[i] * sys.dt;
    }
    double t1 = get_wtime();
    t_verlet += (t1 - t0);
    
    // 2. Apply PBC
    apply_pbc(sys);
    double t2 = get_wtime();
    t_pbc += (t2 - t1);
    
    // 3. Compute forces
    compute_forces(sys);
    double t3 = get_wtime();
    t_forces += (t3 - t2);
    
    // 4. Second half-step velocity update
    for (int i = 0; i < sys.N; ++i) {
        double m_inv = 1.0 / sys.mass[i];
        sys.vx[i] += sys.fx[i] * m_inv * dt_half;
        sys.vy[i] += sys.fy[i] * m_inv * dt_half;
        sys.vz[i] += sys.fz[i] * m_inv * dt_half;
    }
    double t4 = get_wtime();
    t_verlet += (t4 - t3);
}

void compute_kinetic_energy(System& sys) {
    sys.ekin = 0.0;
    for (int i = 0; i < sys.N; ++i) {
        sys.ekin += 0.5 * sys.mass[i] * (sys.vx[i]*sys.vx[i] + sys.vy[i]*sys.vy[i] + sys.vz[i]*sys.vz[i]);
    }
}

void compute_temperature(System& sys) {
    sys.temp = 2.0 * sys.ekin / (3.0 * sys.N);
}

void compute_pressure(System& sys, double rho) {
    double vol = sys.L * sys.L * sys.L;
    sys.press = rho * sys.temp + sys.virial / (3.0 * vol);
}
