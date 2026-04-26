// timer.h — high-resolution wall-clock timer
// Used in ALL benchmarks to ensure consistent timing
#pragma once
#include <chrono>

struct Timer {
    using Clock = std::chrono::high_resolution_clock;
    std::chrono::time_point<Clock> start_;
    void start() { start_ = Clock::now(); }
    double elapsed_ms() const {
        return std::chrono::duration<double, std::milli>(
            Clock::now() - start_).count();
    }
    double elapsed_s() const { return elapsed_ms() / 1000.0; }
};
