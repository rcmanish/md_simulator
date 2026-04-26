// results_writer.h — automatic CSV results writer
// Every benchmark run appends one row to a CSV file.
// Schema: timestamp, experiment, N, threads_or_ranks, T_serial_s, T_parallel_s, speedup, efficiency, data_source
#pragma once
#include <fstream>
#include <string>
#include <ctime>
#include <sstream>
#include <iomanip>

class ResultsWriter {
public:
    static void append(const std::string& filepath,
                       const std::string& experiment,
                       int N,
                       int threads_or_ranks,
                       double T_serial_s,
                       double T_parallel_s,
                       const std::string& data_source = "measured") {
        double speedup   = (T_parallel_s > 0.0) ? (T_serial_s / T_parallel_s) : 1.0;
        double efficiency = speedup / threads_or_ranks;

        // Check if file exists to write header
        bool file_exists = false;
        {
            std::ifstream check(filepath);
            file_exists = check.good();
        }

        std::ofstream out(filepath, std::ios_base::app);
        if (!file_exists) {
            out << "timestamp,experiment,N,threads_or_ranks,"
                   "T_serial_s,T_parallel_s,speedup,efficiency,data_source\n";
        }

        // Timestamp
        std::time_t now = std::time(nullptr);
        std::tm* tm_info = std::localtime(&now);
        std::ostringstream ts;
        ts << std::put_time(tm_info, "%Y-%m-%dT%H:%M:%S");

        out << std::fixed << std::setprecision(6)
            << ts.str()          << ","
            << experiment        << ","
            << N                 << ","
            << threads_or_ranks  << ","
            << T_serial_s        << ","
            << T_parallel_s      << ","
            << speedup           << ","
            << efficiency        << ","
            << data_source       << "\n";
    }
};
