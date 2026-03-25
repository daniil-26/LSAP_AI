from lsap import Lsap
from mcts import Mcts
from settings import Settings

def result(lsap: Lsap, settings: Settings) -> None:
    mcts = Mcts(
        lsap=lsap,
        settings=settings)
    print(mcts.select_actions())
