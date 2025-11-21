#include <math.h>
#include <stdio.h>
#include <string.h>

#include "config.h"
#include "lsap.h"


double M[DIM][DIM];

void init_matrix(double matrix[DIM][DIM]) {
    memcpy(M, matrix, sizeof(M));
}

void load_matrix(int n) {
    char filename[100];
    sprintf(filename, "C:\\Users\\PAYK\\CLionProjects\\mcts_lsap_\\%d.txt", n);
    FILE* file = fopen(filename, "r");
    for (int i = 0; i < DIM; i++)
        for (int j = 0; j < DIM; j++)
            fscanf(file, "%lf\n", &M[i][j]);
}

double criterion(int perm[DIM]) {
    double sum = 0;
    for (int i = 0; i < DIM; i++)
        sum += M[i][perm[i]];
    return sum;
}

double normalized_criterion(int perm[DIM]) {
    return 2 * pow(criterion(perm) / DIM, DIM - 1) - 1;
}
