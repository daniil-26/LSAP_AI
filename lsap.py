import random
from scipy.optimize import linprog

from settings import MctsSettings

class Lsap:

    def __init__(self,
                 mcts_settings: MctsSettings
                 ) -> None:
        self.settings = mcts_settings
        self.matrix = [[random.random()
                        for __ in range(self.settings.dim)]
                       for _ in range(self.settings.dim)]

    def criterion(self,
                  perm: tuple[int]
                  ) -> float:
        return sum(self.matrix[i][j] for i, j in enumerate(perm))

    def normalized_criterion(self,
                             perm: tuple[int]
                             ) -> float:
        crit = self.criterion(perm)
        return 2 * pow(crit / self.settings.dim, self.settings.dim - 1) - 1

    def optimum(self) -> float:
        c = [-j for i in self.matrix for j in i]
        A_ub = [[-1 if j == i else 0 for j in range(self.settings.dim * self.settings.dim)]
                for i in range(self.settings.dim * self.settings.dim)]
        b_ub = [0 for _ in range(self.settings.dim * self.settings.dim)]
        A_eq = [[1 if j // self.settings.dim == i else 0 for j in range(self.settings.dim * self.settings.dim)]
                for i in range(self.settings.dim)] + [[1 if j % self.settings.dim == i else 0
                                               for j in range(self.settings.dim * self.settings.dim)]
                                                      for i in range(self.settings.dim)]
        b_eq = [1 for _ in range(2 * self.settings.dim)]
        l = linprog(c=c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq).fun
        return -l