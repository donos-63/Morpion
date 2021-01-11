from board import Board
from enum import Enum
import players.human_player as hplay
import players.random_player as rplay
import players.cnn_player as dplay
import players.min_max_player as mmplay
from player import PlayerPawn


class PlayerType(Enum):
    Human = 1
    Random = 2
    CNN = 3
    MinMax = 4

class PlayerFactory:
    def create_player(self, type):
        '''
            Python factory to create player
        '''
        if type == PlayerType.Human.value:
            print('Human player created')
            return hplay.HumanPlayer()

        if type == PlayerType.Random.value:
            print('Random player created')
            return rplay.RandomPlayer()

        if type == PlayerType.CNN.value:
            print('CNN player created')
            b = Board(PlayerPawn.NONE.value)
            return dplay.CNNPlayer(b.get_board())

        if type == PlayerType.MinMax.value:
            print('MinMax player created')
            return mmplay.MinMaxPlayer()