from player import Player, PlayerPawn
import copy as cp
import numpy as np

class Board():

    def is_player_win(board, player):
        '''
            check if the given player win the game
        '''
        return (board[0][0] == player and board[0][1] == player and board[0][2] == player) or (
                        board[1][0] == player and board[1][1] == player and board[1][2] == player) or (
                            board[2][0] == player and board[2][1] == player and board[2][2] == player) or (
                            board[0][0] == player and board[1][0] == player and board[2][0] == player) or (
                            board[0][1] == player and board[1][1] == player and board[2][1] == player) or (
                            board[0][2] == player and board[1][2] == player and board[2][2] == player) or (
                            board[0][0] == player and board[1][1] == player and board[2][2] == player) or (
                            board[0][2] == player and board[1][1] == player and board[2][0] == player)

    def get_winner(board):
        '''
            Return the winner, as numerical value
        '''
        if Board.is_player_win(board, PlayerPawn.P1.value):
            return Player.player_to_numerical(PlayerPawn.P1.value)
        elif Board.is_player_win(board, PlayerPawn.P2.value):
            return Player.player_to_numerical(PlayerPawn.P2.value)
        elif Board.get_end_of_party(board): #draw
            return Player.player_to_numerical(PlayerPawn.NONE.value)
        
        return None

    def get_end_of_party(board):
        '''
            check if the party ended
        '''
        return len(Board.get_available_moves(board))== 0

    def __init__(self, none_type):
        self.none_type = none_type
        self.reset_board()

    def reset_board(self):
        '''
            reset the board to default value
        '''
        self.board = [[self.none_type,self.none_type,self.none_type],[self.none_type,self.none_type,self.none_type],[self.none_type,self.none_type,self.none_type]]
        self.boardHistory = []

    def get_available_moves(board):
        '''
            get list of available moves
        '''
        available_moves = []
        for x in range(0,3):
            for y in range(0,3):
                if(board[y][x] == PlayerPawn.NONE.value):
                    available_moves.append((x,y))

        return available_moves

    def get_board(self):
        '''
            return the board of the instance
        '''
        return self.board

    def get_flatten_board(board):
        '''
            return a board as a string
            ex : ---XO--X-
        '''
        board_copy = np.array(board, copy=True)
        game_turn = board_copy.flatten()
        #concat to string (ex : ---XO--X-)
        return ''.join(game_turn)

    def __store_game(self, board):
        self.boardHistory.append(board)

    def set_move(self, player, x, y):
        '''
            apply a move to the board
        '''
        if(self.board[y][x] != PlayerPawn.NONE.value):
            raise Exception('set_move', 'bad move')

        self.board[y][x] = player
        self.__store_game(self.board)
        return True

    def board_to_numercial(board):
        '''
            convert a board to numericals values, for DL
        '''
        board_to_numercial = cp.deepcopy(board)
        for i in range(0,3):
            for j in range(0,3):
                board_to_numercial[i][j] = Player.player_to_numerical(board[i][j])

        return board_to_numercial             


