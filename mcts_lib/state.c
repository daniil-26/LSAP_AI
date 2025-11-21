#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "config.h"
#include "state.h"


int id_to_ab[N_ACTIONS][2];
int ab_to_id[DIM][DIM];

#define id_by_perm (a, b) = ((a + 1) * a / 2 - b)


State* init_state(int perm[DIM]) {
    State* state = malloc(sizeof(State));

    state->N_s = 0;
    for (int i = 0; i < N_ACTIONS; i++) {
        state->N_s_a[i] = 0;
        state->Q[i] = 0;
        state->results_sum[i] = 0;
        next_perm(perm, state->next_perms[i], id_to_ab[i][0],id_to_ab[i][1]);
    }

    for (int i = 0; i < DIM; i++)
        state->perm[i] = perm[i];

    random_p(state);

    return state;
}

void init_tables() {
    int id = 0;
    ab_to_id[0][0] = id;
    id_to_ab[id][0] = 0;
    id_to_ab[id][1] = 0;
    for (int a = 0; a < DIM; a++) {
        for (int b = 0; b < a; b++) {
            id = (a + 1) * a / 2 - b;
            ab_to_id[a][b] = id;
            id_to_ab[id][0] = a;
            id_to_ab[id][1] = b;
        }
    }
}

void next_perm(int perm[DIM], int perm_next[DIM], int a, int b) {
    for (int i = 0; i < DIM; i++)
        perm_next[i] = perm[i];
    perm_next[a] = perm[b];
    perm_next[b] = perm[a];
}

void random_p(State* state) {
    for (int i = 0; i < N_ACTIONS; i++)
        state->P[i] = (double)rand() / RAND_MAX;
}
