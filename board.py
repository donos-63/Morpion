from player import Player, PlayerPawn
import copy as cp

class Board():

    def isPlayerWin(board, player):
        return (board[0][0] == player and board[0][1] == player and board[0][2] == player) or (
                        board[1][0] == player and board[1][1] == player and board[1][2] == player) or (
                            board[2][0] == player and board[2][1] == player and board[2][2] == player) or (
                            board[0][0] == player and board[1][0] == player and board[2][0] == player) or (
                            board[0][1] == player and board[1][1] == player and board[2][1] == player) or (
                            board[0][2] == player and board[1][2] == player and board[2][2] == player) or (
                            board[0][0] == player and board[1][1] == player and board[2][2] == player) or (
                            board[0][2] == player and board[1][1] == player and board[2][0] == player)

    def get_winner(board):
        if Board.isPlayerWin(board, PlayerPawn.P1.value):
            return Player.player_to_numerical(PlayerPawn.P1.value)
        elif Board.isPlayerWin(board, PlayerPawn.P2.value):
            return Player.player_to_numerical(PlayerPawn.P2.value)
        elif len(Board.get_available_moves(board))== 0: #draw
            return Player.player_to_numerical(PlayerPawn.NONE.value)
        
        return None

    def getEndOfParty(self):
        for x in range(0,3):
            for y in range(0,3):
                if(self.board[y][x] == PlayerPawn.NONE.value):
                   return False

        return True

    def getHistory(self):
        return self.boardHistory

    def __init__(self, none_type):
        self.none_type = none_type
        self.reset_board()

    def reset_board(self):
        self.board = [[self.none_type,self.none_type,self.none_type],[self.none_type,self.none_type,self.none_type],[self.none_type,self.none_type,self.none_type]]
        self.boardHistory = []

    def get_available_moves(board):
        available_moves = []
        for x in range(0,3):
            for y in range(0,3):
                if(board[y][x] == PlayerPawn.NONE.value):
                    available_moves.append((x,y))

        return available_moves

    def get_board(self):
        return self.board


    def __storeGame(self, board):
        self.boardHistory.append(board)

    def set_move(self, player, x, y):
        if(self.board[y][x] != PlayerPawn.NONE.value):
            raise Exception('set_move', 'bad move')

        self.board[y][x] = player
        self.__storeGame(self.board)
        return True

    def board_to_numercial(board):
        board_to_numercial = cp.deepcopy(board)
        for i in range(0,3):
            for j in range(0,3):
                board_to_numercial[i][j] = Player.player_to_numerical(board[i][j])

        return board_to_numercial             


