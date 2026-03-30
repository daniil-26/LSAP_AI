import random
from statistics import mean

from libr import *


random.seed()

DIM = 6
N_ACTIONS = (1 + DIM * (DIM - 1) / 2)
MAX_DEPTH = (2 * DIM * (DIM - 1))
N_ITERS = (20 * MAX_DEPTH)
C = 1.5
IS_TEMP = False
INV_T = 0.7
IS_WITH_CYCLES = False

mcts_settings = MctsSettings(
    dim=DIM,
    max_depth=MAX_DEPTH,
    n_iters=N_ITERS,
    c=C,
    is_no_cycle=(not IS_WITH_CYCLES),
    is_use_t=IS_TEMP,
    init_inv_t=INV_T)


res = []
for i in range(100):
    print(i)
    lsap = Lsap(mcts_settings)
    res.append(result(lsap, mcts_settings) / lsap.optimum())
    #print(result(lsap, set), lsap.optimum())
print(mean(res))
