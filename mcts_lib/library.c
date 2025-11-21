#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "library.h"
#include "config.h"
#include "State.h"
#include "mcts.h"
#include "lsap.h"

double result(double m[DIM][DIM]) {
    srand(time(NULL));
    init_matrix(m);
    init_tables();
    return select_actions();
}