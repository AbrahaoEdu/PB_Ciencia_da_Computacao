#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define N 10000

int main(void) {
    int **matrix = (int **)malloc(N * sizeof(int *));
    for (int i = 0; i < N; i++) {
        matrix[i] = (int *)malloc(N * sizeof(int));
        for (int j = 0; j < N; j++) {
            matrix[i][j] = rand() % 256;
        }
    }

    int brightness = 10;
    double t0 = omp_get_wtime();

#pragma omp parallel for shared(matrix)
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            int v = matrix[i][j] + brightness;
            matrix[i][j] = v > 255 ? 255 : v;
        }
    }

    double t1 = omp_get_wtime();
    printf("Matriz %dx%d ajustada. Threads=%d Tempo=%.4fs\n",
           N, N, omp_get_max_threads(), t1 - t0);
    printf("Amostra [0][0]=%d\n", matrix[0][0]);

    for (int i = 0; i < N; i++)
        free(matrix[i]);
    free(matrix);
    return 0;
}
