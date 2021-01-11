import string
from players.base_player import base_player
from board import Board
from render.graphical_manager import GraphicalManager


class HumanPlayer(base_player):
    
    def play_move(self, _, board):
        '''
            Select move by human
        '''
        while True:
            x, y = GraphicalManager.get_instance().user_interact(board)

            if self.is_move_valid(Board.get_available_moves(board), x, y):
                return x, y

            GraphicalManager.get_instance().display_warning('Mauvais emplacement, veuillez recommencer', board)

    def is_move_valid(self, list_available_moves, x, y):
        '''
            Check if move is possible
        '''
        return (x,y) in list_available_moves

    def __init__(self):
        self.is_need_reinforcement = False
        self.is_autobot = False
