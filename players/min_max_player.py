import os
import pandas as pd
from enum import Enum
from board import Board
import copy as cp
from math import inf as infinity
from player import Player, PlayerPawn
from players.base_player import base_player

class MinMaxPlayer(base_player):

    MODEL_FILEPATH = base_player.MODELS_FOLDER + os.sep + 'minmax.saves'

    class MinMaxResult(Enum):
        WIN = +1
        LOSS = -1
        DRAW = 0
        
    def __minmax(self, player, board):
        '''
            Minmax algorithm
        '''
        best_move = [-1, -1]
        best_score = -infinity if player == self.me else +infinity

        if Board.is_player_win(board, self.me):
            return best_move, self.MinMaxResult.WIN.value   #ia win
        elif Board.is_player_win(board, Player.get_oponnent_for(self.me)):
            return best_move, self.MinMaxResult.LOSS.value    #ia loose
        elif Board.get_end_of_party(board): #draw
            return best_move, self.MinMaxResult.DRAW.value

        for x, y in Board.get_available_moves(board):
            boardWithNewMove = cp.deepcopy(board)

            boardWithNewMove[y][x] = player
            move, score = self.__minmax(Player.get_oponnent_for(player), boardWithNewMove)
            boardWithNewMove[y][x] = Player.player_to_numerical(PlayerPawn.NONE)
            move = x, y

            if (player == self.me and score > best_score) \
                or (player != self.me and score < best_score):
                    #min or max value (min if oponent player, else max)
                    best_score = score
                    best_move = move

        return best_move, best_score    

    def play_move(self, player, board):
        '''
            Compute move using minmax algorithm
        '''
        self.me = player

        #To save time, we check if the game turn as not been yet computed - usefull for first game turn
        #can bee reseted by deleting models/minmax.saves
        exists, move = self.test_state(board)

        if not exists:
            move, _ = self.__minmax(player, cp.deepcopy(board))
            self.store_move(board, move)
    
        return move

    def test_state(self, board):
        '''
            Test if move already computed
        '''
        game_turn = Board.get_flatten_board(board)
        history = self.history[(self.history['state']==game_turn)]
        if not history.empty:
            return True, [history['x'].iloc[0], history['y'].iloc[0]]

        return False, None


    def store_move(self, board, move):
        '''
            Save move played (and result computed)
        '''
        game_turn = Board.get_flatten_board(board)

        self.history = self.history.append({'x': move[0], 'y' : move[1], 'state' : game_turn}, ignore_index=True)
        self.history.to_csv(MinMaxPlayer.MODEL_FILEPATH, index=False, encoding='utf-8', sep=';')
        
    def load_pre_calculated_moves(self):
        '''
            Load list of move already played and computed
        '''        
        columns = ['x', 'y', 'state']
        self.history = pd.DataFrame(columns=columns)
        if(os.path.exists(MinMaxPlayer.MODEL_FILEPATH)):
            self.history = pd.read_csv(MinMaxPlayer.MODEL_FILEPATH, encoding='utf-8', sep=';')

    def __init__(self):
        self.need_reinforcement = False
        self.is_autobot = True
        self.load_pre_calculated_moves()




