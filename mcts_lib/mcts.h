#pragma once

#include "node.h"


void init_tables();

void next_perm(int perm[DIM], int perm_next[DIM], int a, int b);

int ucb_index(State* state);

int nsa_index(int N_s_a[N_ACTIONS]);

double select_actions();

void iterations(State* base_state, Node* root, int depth_limit, State* steps[MAX_DEPTH + 1], int steps_n);

void backpropagation(State* sequence[MAX_DEPTH + 1], int actions[MAX_DEPTH], int last);
