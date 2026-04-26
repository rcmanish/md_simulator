#include "types.h"
#include "particles.h"
#include "forces.h"
#include "integrator.h"
#include "io.h"
#include "utils.h"
#include "analysis.h"

#include <iostream>
#include <string>
#include <cstdlib>
#include <cmath>

double t_forces = 0.0;
double t_verlet = 0.0;
double t_pbc = 0.0;
double t_io = 0.0;

int main(int argc, char** argv) {
    // Default parameters
    int N = 256;
    double rho = 0.8;
    double T_target = 1.0;
    double dt = 0.005;
    int n_steps = 10000;
    double r_cutoff = 2.5;
    std::string out_prefix = "md";
    bool test_verlet = false;
    bool compute_rdf = false;

    // Parse command line arguments
    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "-N" && i + 1 < argc) N = std::stoi(argv[++i]);
        else if (arg == "-steps" && i + 1 < argc) n_steps = std::stoi(argv[++i]);
        else if (arg == "-dt" && i + 1 < argc) dt = std::stod(argv[++i]);
        else if (arg == "-rho" && i + 1 < argc) rho = std::stod(argv[++i]);
        else if (arg == "-T_target" && i + 1 < argc) T_target = std::stod(argv[++i]);
        else if (arg == "-rc" && i + 1 < argc) r_cutoff = std::stod(argv[++i]);
        else if (arg == "-out" && i + 1 < argc) out_prefix = argv[++i];
        else if (arg == "-test_verlet") test_verlet = true;
        else if (arg == "-rdf") compute_rdf = true;
    }

    std::cout << "--- MD Simulator Setup ---\n";
    std::cout << "N = " << N << "\n";
    std::cout << "rho = " << rho << "\n";
    std::cout << "T_target = " << T_target << "\n";
    std::cout << "dt = " << dt << "\n";
    std::cout << "steps = " << n_steps << "\n";
    std::cout << "r_cutoff = " << r_cutoff << "\n";
    
    // Setup system
    double box_length = std::pow(N / rho, 1.0 / 3.0);
    System sys(N, box_length, dt, r_cutoff);
    
    std::cout << "Box Length L = " << box_length << "\n";

    if (test_verlet) {
        std::cout << "--- Running Velocity Verlet Accuracy Test ---\n";
        // Single particle, harmonic oscillator F = -k*x
        sys.N = 1;
        sys.rx[0] = 1.0; sys.ry[0] = 0.0; sys.rz[0] = 0.0;
        sys.vx[0] = 0.0; sys.vy[0] = 0.0; sys.vz[0] = 0.0;
        sys.fx[0] = -1.0 * sys.rx[0]; sys.fy[0] = 0.0; sys.fz[0] = 0.0; // k=1
        
        double t = 0.0;
        for (int step = 1; step <= n_steps; ++step) {
            double dt_half = 0.5 * sys.dt;
            sys.vx[0] += sys.fx[0] * dt_half;
            sys.rx[0] += sys.vx[0] * sys.dt;
            
            // new force
            sys.fx[0] = -1.0 * sys.rx[0];
            
            sys.vx[0] += sys.fx[0] * dt_half;
            t += sys.dt;
        }
        double exact_x = std::cos(t);
        double err = std::abs(sys.rx[0] - exact_x);
        std::cout << "dt=" << dt << " steps=" << n_steps << " final_t=" << t 
                  << " num_x=" << sys.rx[0] << " exact_x=" << exact_x 
                  << " error=" << err << "\n";
        return 0;
    }

    // Initialize particles
    initialize_fcc(sys, rho, T_target);
    apply_pbc(sys);
    
    // Initial forces and properties
    compute_forces(sys);
    compute_kinetic_energy(sys);
    compute_temperature(sys);
    compute_pressure(sys, rho);
    
    std::string thermo_file = out_prefix + "_thermo.csv";
    write_thermo(sys, 0, 0.0, thermo_file);

    RDF rdf(sys.L / 2.0, 100);

    std::cout << "Starting simulation loop...\n";
    double start_time = get_wtime();

    // Main loop
    for (int step = 1; step <= n_steps; ++step) {
        velocity_verlet_full(sys);
        
        if (step % 100 == 0) {
            double io_start = get_wtime();
            compute_kinetic_energy(sys);
            compute_temperature(sys);
            compute_pressure(sys, rho);
            write_thermo(sys, step, step * dt, thermo_file);
            t_io += (get_wtime() - io_start);
        }
        
        if (compute_rdf && step > n_steps / 2 && step % 10 == 0) {
            double io_start = get_wtime();
            rdf.sample(sys);
            t_io += (get_wtime() - io_start);
        }
    }

    double end_time = get_wtime();
    double total_time = end_time - start_time;
    std::cout << "Simulation completed in " << total_time << " seconds.\n";

    std::cout << "--- Profiling Table ---\n";
    std::cout << "Function         | Time (s) | % of total\n";
    std::cout << "----------------------------------------\n";
    std::cout << "compute_forces   | " << t_forces << " | " << (t_forces/total_time)*100.0 << "%\n";
    std::cout << "velocity_verlet  | " << t_verlet << " | " << (t_verlet/total_time)*100.0 << "%\n";
    std::cout << "apply_pbc        | " << t_pbc << " | " << (t_pbc/total_time)*100.0 << "%\n";
    std::cout << "I/O & Thermo     | " << t_io << " | " << (t_io/total_time)*100.0 << "%\n";
    
    if (compute_rdf) {
        rdf.save(out_prefix + "_rdf.csv", rho, sys.N);
        std::cout << "RDF saved to " << out_prefix << "_rdf.csv\n";
    }

    return 0;
}
