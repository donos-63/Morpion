from board import Board
import random
class RandomPlayer():

    def play_move(self, _, board):
        '''
            Compute move using random choice in available moves
        '''
        list_available_moves = Board.get_available_moves(board)

        if( len(list_available_moves)>1):
            indice_mvt=random.randint(0,len(list_available_moves)-1)
            return list_available_moves[indice_mvt]
        else :
            return list_available_moves[0] 

    def __init__(self):
        self.is_need_reinforcement = False
        self.is_autobot = True
