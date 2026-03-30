

class MctsSettings:

    def __init__(self,
                 dim: int,
                 max_depth: int = None,
                 n_iters: int = None,
                 c: float = 1.5,
                 is_no_cycle: bool = True,
                 is_use_t: bool = False,
                 init_inv_t: float = 0.7
                 ) -> None:

        self.dim = dim
        self.n_actions: int = int(1 + dim * (dim - 1) / 2)

        self.max_depth = 2 * dim * (dim - 1) if max_depth is None else max_depth
        self.n_iters = 20 * self.max_depth if n_iters is None else n_iters
        self.c = c
        self.is_no_cycle = is_no_cycle
        self.is_use_t = is_use_t
        self.init_inv_t = init_inv_t


class NetworkSettings:

    def __init__(self,
                 channels_n: int = 256,
                 blocks_n: int = 8,
                 is_softmax: bool = False
                 ) -> None:

        self.channels_n = channels_n
        self.blocks_n = blocks_n
        self.is_softmax = is_softmax

