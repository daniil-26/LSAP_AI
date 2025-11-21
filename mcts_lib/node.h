#pragma once

#include "state.h"


typedef struct Node {
    State* state;
    struct Node* next[DIM];
} Node;

Node* init_node();

Node* get_node(Node* current, int perm[]);
