import random

from libr import *


random.seed(0)

set = Settings(
    dim=4,
    max_depth=6,
    n_iters=8,
    c=1.5,
    is_no_cycle=True,
    is_use_t=False,
    init_inv_t=0.7)

lsap = Lsap(set)

result(lsap, set)
