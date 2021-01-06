from board import Board
from enum import Enum
from random import Random
import players.human_player as hplay
import players.random_player as rplay
import players.dnn_player as dplay
import players.min_max_player as mmplay
from player import PlayerPawn


class PlayerType(Enum):
    Human = 1
    Random = 2
    Dnn = 3
    MinMax = 4

class PlayerFactory:
    def create_player(self, type):
        if type == PlayerType.Human.value:
            print('Human player created')
            return hplay.HumanPlayer()

        if type == PlayerType.Random.value:
            print('Random player created')
            return rplay.RandomPlayer()

        if type == PlayerType.Dnn.value:
            print('DNN player created')
            b = Board(PlayerPawn.NONE.value)
            return dplay.DnnPlayer(b.get_board())

        if type == PlayerType.MinMax.value:
            print('MinMax player created')
            return mmplay.MinMaxPlayer()