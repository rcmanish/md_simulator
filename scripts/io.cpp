#include "io.h"
#include <fstream>
#include <iostream>
#include <iomanip>

void write_xyz(const System& sys, int step, const std::string& filename) {
    std::ofstream out(filename, std::ios_base::app);
    out << sys.N << "\n";
    out << "Step " << step << "\n";
    for (int i = 0; i < sys.N; ++i) {
        out << "Ar " 
            << sys.rx[i] << " " 
            << sys.ry[i] << " " 
            << sys.rz[i] << "\n";
    }
}

void write_thermo(const System& sys, int step, double time, const std::string& filename) {
    bool file_exists = false;
    std::ifstream check(filename);
    if (check.good()) file_exists = true;
    check.close();

    std::ofstream out(filename, std::ios_base::app);
    if (!file_exists) {
        out << "step,time,temp,ke,pe,etot,press\n";
    }
    
    double etot = sys.ekin + sys.epot;
    
    out << std::scientific << std::setprecision(6)
        << step << ","
        << time << ","
        << sys.temp << ","
        << sys.ekin << ","
        << sys.epot << ","
        << etot << ","
        << sys.press << "\n";
}
