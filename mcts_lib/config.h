#pragma once

#define DIM 6
#define N_ACTIONS (1 + DIM * (DIM - 1) / 2)
#define MAX_DEPTH (2 * DIM * (DIM - 1))
#define N_ITERS (20 * MAX_DEPTH)
#define C 1.5
#define IS_TEMP 0
#define INV_T 0.7
#define IS_WITH_CYCLES 0
