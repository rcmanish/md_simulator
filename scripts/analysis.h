#pragma once
#include "types.h"
#include <string>
#include <vector>

struct RDF {
    int n_bins;
    double bin_size;
    double max_r;
    std::vector<double> histogram;
    int samples;
    
    RDF(double max_radius, int bins) 
        : n_bins(bins), max_r(max_radius), histogram(bins, 0.0), samples(0) {
        bin_size = max_r / n_bins;
    }
    
    void sample(const System& sys);
    void save(const std::string& filename, double rho, int N);
};
