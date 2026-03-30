import random

from settings import MctsSettings


class State:

    def __init__(self,
                 settings: MctsSettings,
                 perm: tuple[int]) -> None:

        self.perm = perm

        self.next_perms: list[tuple[int]] = [self.perm] * settings.n_actions
        for a in range(settings.dim):
            for b in range(a):
                id = int((a + 1) * a / 2 - b)
                perm = list(self.perm)
                perm[a], perm[b] = perm[b], perm[a]
                self.next_perms[id] = tuple(perm)

        self.N_s: int = 0
        self.N_s_a: list[int] = [0] * settings.n_actions

        self.P: list[float] = [random.random() for _ in range(settings.n_actions)]
        self.Q: list[float] = [0] * settings.n_actions
        self.results_sum: list[float] = [0] * settings.n_actions

    def print(self) -> None:
        print(f'perm: {self.perm} | N_s: {self.N_s} | N_s_a: {self.N_s_a}')