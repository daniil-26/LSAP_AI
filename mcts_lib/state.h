#pragma once

typedef struct State {
    int perm[DIM];
    int next_perms[N_ACTIONS][DIM];

    int N_s;
    int N_s_a[N_ACTIONS];

    double P[N_ACTIONS];
    double Q[N_ACTIONS];
    double results_sum[N_ACTIONS];
} State;

State* init_state(int perm[DIM]);

void init_tables();

void next_perm(int perm[DIM], int perm_next[DIM], int a, int b);

void random_p(State* state);
