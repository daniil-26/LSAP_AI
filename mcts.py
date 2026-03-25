from math import *
import random

from state import State
from lsap import Lsap
from settings import Settings


class Mcts:

    def __init__(self,
                 lsap: Lsap,
                 settings: Settings,
                 ) -> None:
        self.lsap = lsap
        self.settings = settings

        self.inv_t = settings.init_inv_t

        self.states: dict[tuple[int], State] = {}
        self.steps: list[tuple[int]] = []

    def select_actions(self
                       ) -> list[tuple[int]]:
        '''Выбор действия на основе вероятностей N_s_a ^ inv_t'''

        current = State(self.settings, tuple(range(self.settings.dim)))
        self.states[current.perm] = current
        self.steps.append(current.perm)

        print()

        for i in range(self.settings.max_depth):
            self.iterations(current, self.settings.max_depth - i)
            index = self.nsa_index(current.N_s_a)
            next_perm = current.next_perms[index]
            current = self.states[next_perm]
            self.steps.append(next_perm)

        return self.steps

    def iterations(self,
                   base_state: State, depth_limit: int
                   ) -> None:
        '''Обновляет N_s, N_s_a, Q'''

        for i in range(self.settings.n_iters):
            current = base_state
            sequence: list[tuple[int]] = [current.perm]
            actions: list[int] = []

            for j in range(depth_limit):
                index = self.ucb_index(current, sequence) # random.randint(0, self.settings.n_actions - 1) # self.ucb_index(current, sequence)
                actions.append(index)
                current.N_s_a[index] += 1

                next_perm = current.next_perms[index]
                if next_perm not in self.states:
                    self.states[next_perm] = State(self.settings, next_perm)
                    sequence.append(current.perm) ###########################################################################
                    break
                current = self.states[next_perm]
                sequence.append(current.perm)

            self.backpropagation(sequence, actions)

    def backpropagation(self,
                        sequence: list[tuple[int]], actions: list[int]
                        ) -> None:
        crit = self.lsap.normalized_criterion(sequence[-1])
        for p in sequence:
            self.states[p].N_s += 1
        for p, action in zip(sequence[::-1], actions):
            st = self.states[p]
            st.results_sum[action] += crit
            st.Q[action] = 0 if st.N_s_a[action] == 0 else st.results_sum[action] / st.N_s_a[action] ########################################################

    def nsa_index(self,
                  N_s_a: list[int]
                  ) -> int:
        if self.settings.is_use_t:
            weights = [pow(x, self.inv_t) for x in N_s_a]
            return random.choices(N_s_a, weights, k=1)[0]
        else:
            return N_s_a.index(max(N_s_a)) ##################################################################################

    def ucb_index(self,
                  st: State,
                  sequence: list[tuple[int]] = None
                  ) -> int:
        ucb = self.__ucb__(st, sequence)
        max_value = max(ucb)
        indeces = [i for i, val in enumerate(ucb) if val == max_value]
        if len(indeces) == 1:
            return indeces[0]
        else:
            return random.choice(indeces)

    def __ucb__(self,
                st: State,
                sequence: list[tuple[int]] = None
                ) -> list[float]:
        if not self.settings.is_no_cycle:
            sequence = []
        ret = [
            st.Q[i] + self.settings.c * st.P[i] * sqrt(st.N_s) / (1 + st.N_s_a[i])
            if st.next_perms[i] not in self.steps and st.next_perms[i] not in sequence
            else float("-inf")
            for i in range(self.settings.n_actions)
        ]
        return ret



