from enum import Enum
from players.base_player import base_player
from board import Board
import copy as cp
from math import inf as infinity
from player import Player, PlayerPawn

class MinMaxPlayer(base_player):

    class MinMaxResult(Enum):
        WIN = +1
        LOSS = -1
        DRAW = 0
        
    def __minmax(self, player, board):
        best_move = [-1, -1]
        best_score = -infinity if player == self.me else +infinity

        if Board.isPlayerWin(board, self.me):
            return best_move, self.MinMaxResult.WIN   #ia win
        elif Board.isPlayerWin(board, Player.get_oponnent_for(self.me)):
            return best_move, self.MinMaxResult.LOSS    #ia loose
        elif len(Board.get_available_moves(board))== 0: #draw
            return best_move, self.MinMaxResult.DRAW

        for x, y in Board.get_available_moves(board):
            boardWithNewMove = cp.deepcopy(board)

            boardWithNewMove[y][x] = player
            move, score = self.__minmax(Player.get_oponnent_for(player), boardWithNewMove)
            boardWithNewMove[y][x] = Player.player_to_numerical(PlayerPawn.NONE)
            move = x, y

            if (player == self.me and score > best_score) or (player != self.me and score < best_score):
                    #min or max value
                    best_score = score
                    best_move = move


        return best_move, best_score    

    def play_move(self, player, board):
        self.me = player
        move, _ = self.__minmax(player, cp.deepcopy(board))
        return move


    def __init__(self):
        self.need_reinforcement = False
        self.is_autobot = True




