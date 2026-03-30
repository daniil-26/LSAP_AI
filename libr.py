from lsap import Lsap
from mcts import Mcts
from settings import MctsSettings

def result(lsap: Lsap, settings: MctsSettings) -> float:
    mcts = Mcts(
        lsap=lsap,
        mcts_settings=settings)

    steps = mcts.select_actions()
    vals = [lsap.criterion(perm) for perm in steps]

    return max(vals)
