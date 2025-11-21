#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#include "config.h"
#include "node.h"


Node* init_node() {
    Node* node = malloc(sizeof(Node));
    node->state = NULL;
    for (int i = 0; i < DIM; i++)
        node->next[i] = NULL;
    return node;
}

Node* get_node(Node* root, int perm[DIM]) {
    for (int i = 0; i < DIM; i++) {
        if (root->next[perm[i]] == NULL)
            root->next[perm[i]] = init_node();
        root = root->next[perm[i]];
    }
    return root;
}
