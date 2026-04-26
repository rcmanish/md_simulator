#include "utils.h"

#ifdef MODE_OPENMP
#include <omp.h>
#endif

#ifdef MODE_MPI
#include <mpi.h>
#endif

#include <chrono>

double get_wtime() {
#if defined(MODE_MPI) || defined(MODE_HYBRID)
    return MPI_Wtime();
#elif defined(MODE_OPENMP)
    return omp_get_wtime();
#else
    static auto start = std::chrono::steady_clock::now();
    auto now = std::chrono::steady_clock::now();
    std::chrono::duration<double> diff = now - start;
    return diff.count();
#endif
}
