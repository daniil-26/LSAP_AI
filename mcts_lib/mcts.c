#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "config.h"
#include "State.h"
#include "Node.h"
#include "mcts.h"
#include "lsap.h"


int ucb_index(State* state) {
    int index = 0, max_n = 0, i;
    double max = -1, u;
    double us[N_ACTIONS];

    for (i = 0; i < N_ACTIONS; i++) {
        u = state->Q[i] + C * state->P[i] * sqrt(state->N_s) / (1 + state->N_s_a[i]);
        if (u > max) {
            max = u;
            max_n = 1;
            index = i;
        }
        else if (u == max)
            max_n++;
        us[i] = u;
    }
    if (max_n == 1)
        return index;
    index = rand() % max_n;
    for (i = 0; i < N_ACTIONS; i++) {
        if (us[i] == max) {
            if (index == 0)
                break;
            index--;
        }
    }
    return i;
}

int is_perms_eq(int x[DIM], int y[DIM]) {
    for (int i = 0; i < DIM; i++)
        if (y[i] != x[i])
            return 0;
    return 1;
}

int is_perm_not_in_sequence(int perm[DIM], State* sequence[MAX_DEPTH], int depth) {
    for (int i = 0; i < depth; i++)
        if (is_perms_eq(perm, sequence[i]->perm))
            return 0;
    return 1;
}

int ucb_index_no_cycle(State* state, State* sequence[MAX_DEPTH], int depth, State* steps[MAX_DEPTH + 1], int steps_n) {
    int index = -1, max_n = 0, i;
    double max = -1, u;
    double us[N_ACTIONS];
    for (i = 0; i < N_ACTIONS; i++) {
        if (is_perm_not_in_sequence(state->next_perms[i], sequence, depth) && is_perm_not_in_sequence(state->next_perms[i], steps, steps_n)) {
            u = state->Q[i] + C * state->P[i] * sqrt(state->N_s) / (1 + state->N_s_a[i]);
            if (u > max) {
                max = u;
                max_n = 1;
                index = i;
            }
            else if (u == max)
                max_n++;
            us[i] = u;
        }
    }
    if (max_n == 1)
        return index;
    index = rand() % max_n;
    for (i = 0; i < N_ACTIONS; i++) {
        if (us[i] == max) {
            if (index == 0)
                break;
            index--;
        }
    }
    return i;
}

int nsa_index(int N_s_a[N_ACTIONS]) {
    if (IS_TEMP) {
        double weights[N_ACTIONS];
        for (int i = 0; i < N_ACTIONS; i++)
            weights[i] = pow(N_s_a[i], INV_T);
        double r = rand() / (double) RAND_MAX;
        double cumulative = 0;
        for (int i = 0; i < N_ACTIONS; i++) {
            cumulative += weights[i];
            if (cumulative >= r)
                return i;
        }
    }
    int max = 0, index = 0;
    for (int i = 0; i < N_ACTIONS; i++) {
        if (N_s_a[i] > max) {
            max = N_s_a[i];
            index = i;
        }
    }
    return index;
}

double select_actions() {
    int perm[DIM];
    for (int i = 0; i < DIM; i++)
        perm[i] = i;
    State* current = init_state(perm);
    Node* root = init_node();
    get_node(root, perm)->state = current;

    State* steps[MAX_DEPTH + 1];
    steps[0] = current;
    int index;
    for (int i = 0; i < MAX_DEPTH; i++) {
        iterations(current, root, MAX_DEPTH - i, steps, i + 1);
        index = nsa_index(current->N_s_a);
        current = get_node(root, current->next_perms[index])->state;
        steps[i + 1] = current;
    }
    double max_crit = 0;
    for (int i = 0; i <= MAX_DEPTH; i++)
        if (criterion(steps[i]->perm) > max_crit)
            max_crit = criterion(steps[i]->perm);
    return max_crit;
}

void iterations(State* base_state, Node* root, int depth_limit, State* steps[MAX_DEPTH + 1], int steps_n) {
    for (int i = 0; i < N_ITERS; i++) {
        Node* current_node;
        State* current = base_state;
        State* sequence[MAX_DEPTH + 1];
        int actions[MAX_DEPTH];

        sequence[0] = current;
        int j = 0;
        int index;
        while (j < depth_limit) {
            j++;
            index = IS_WITH_CYCLES ? ucb_index(current) : ucb_index_no_cycle(current, sequence, j, steps, steps_n);
            actions[j - 1] = index;
            current->N_s_a[index]++;

            current_node = get_node(root, current->next_perms[index]);
            if (current_node->state == NULL) {
                current_node->state = init_state(current->next_perms[index]);
                sequence[j] = current_node->state;
                break;
            }
            current = current_node->state;
            sequence[j] = current;
        }
        backpropagation(sequence, actions, j);
    }
}

void backpropagation(State* sequence[MAX_DEPTH + 1], int actions[MAX_DEPTH], int last) {
    double crit = normalized_criterion(sequence[last]->perm);
    for (int i = 0; i <= last; i++)
        sequence[i]->N_s++;
    int action;
    for (int i = 0; i < last; i++) {
        action = actions[i];
        sequence[i]->results_sum[action] += crit;
        sequence[i]->Q[action] = sequence[i]->results_sum[action] / sequence[i]->N_s_a[action];
    }
}
