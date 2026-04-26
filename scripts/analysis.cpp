#include "analysis.h"
#include <cmath>
#include <fstream>

void RDF::sample(const System& sys) {
    for (int i = 0; i < sys.N - 1; ++i) {
        for (int j = i + 1; j < sys.N; ++j) {
            double dx = sys.rx[i] - sys.rx[j];
            double dy = sys.ry[i] - sys.ry[j];
            double dz = sys.rz[i] - sys.rz[j];
            
            double half_L = 0.5 * sys.L;
            if (dx > half_L) dx -= sys.L; else if (dx < -half_L) dx += sys.L;
            if (dy > half_L) dy -= sys.L; else if (dy < -half_L) dy += sys.L;
            if (dz > half_L) dz -= sys.L; else if (dz < -half_L) dz += sys.L;
            
            double r = std::sqrt(dx*dx + dy*dy + dz*dz);
            if (r < max_r) {
                int bin = static_cast<int>(r / bin_size);
                if (bin >= 0 && bin < n_bins) {
                    histogram[bin] += 2.0; // i-j and j-i
                }
            }
        }
    }
    samples++;
}

void RDF::save(const std::string& filename, double rho, int N) {
    std::ofstream out(filename);
    out << "r,g(r)\n";
    
    double ideal_density = rho;
    for (int i = 0; i < n_bins; ++i) {
        double r_inner = i * bin_size;
        double r_outer = (i + 1) * bin_size;
        double shell_volume = (4.0 / 3.0) * M_PI * (r_outer * r_outer * r_outer - r_inner * r_inner * r_inner);
        double expected_particles = ideal_density * shell_volume;
        
        double r_center = r_inner + 0.5 * bin_size;
        double g_r = 0.0;
        if (samples > 0 && expected_particles > 0) {
            double avg_particles = histogram[i] / (N * samples);
            g_r = avg_particles / expected_particles;
        }
        out << r_center << "," << g_r << "\n";
    }
}
