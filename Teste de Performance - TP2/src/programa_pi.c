#include <stdio.h>
#include <omp.h>

#define NUM_PASSOS 100000000

int main(void) {
    double sum = 0.0;
    double step = 1.0 / (double)NUM_PASSOS;
    double start = omp_get_wtime();

#pragma omp parallel for reduction(+ : sum)
    for (int i = 0; i < NUM_PASSOS; i++) {
        double x = (i + 0.5) * step; /* x privada por iteracao */
        sum += 4.0 / (1.0 + x * x);
    }

    double pi = step * sum;
    double end = omp_get_wtime();

    printf("Pi aproximado: %.10f\n", pi);
    printf("Threads: %d\n", omp_get_max_threads());
    printf("Tempo: %.4f s\n", end - start);
    return 0;
}
