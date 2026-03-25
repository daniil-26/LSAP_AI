import random

from settings import Settings

class Lsap:

    def __init__(self,
                 settings: Settings
                 ) -> None:
        self.settings = settings
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

