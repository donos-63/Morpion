from os import system
import platform
import numpy as np
from board import Board
from player import Player, PlayerPawn
from player_factory import PlayerFactory, PlayerType


class Morpion():


    def __init__(self):
        self.board = Board(PlayerPawn.NONE.value)
        self.factory = PlayerFactory()


    def __initialize_game(self):
        next = False
        player_types = [0,0]
        i=1
        
        for i in range(0, len(player_types)):
            while(not next):
                p = input("(Joueur {})  1:Humain - 2:mlp - 3:random - 4:Dnn - 5:MinMax  : ".format(i+1))
                if(p.isdigit() and int(p) >0 and int(p) < 6):
                    next = True
                    player_types[i] = int(p)

            next = False

        self.nb_simulation = None

        self.P1 = Player(self.factory.create_player(player_types[0]), PlayerPawn.P1.value)
        self.P2 = Player(self.factory.create_player(player_types[1]), PlayerPawn.P2.value)

        if self.P1.instance.need_reinforcement or self.P2.instance.need_reinforcement:
            next=False

            while(not next):
                self.nb_simulation  = input("Nb entraintement de l'IA  :  ")
                if(self.nb_simulation.isdigit() and int(self.nb_simulation) > 0):
                    next = True

            self.nb_simulation = int(self.nb_simulation)
            if self.P1.instance.need_reinforcement:
                self.P1.set_ia_initialisation(self.nb_simulation)
            if self.P2.instance.need_reinforcement:
                self.P2.set_ia_initialisation(self.nb_simulation)

    def __play_game(self):
               
        #todo: try/catch
        playing= True
        party_counter = 0
        while playing:
            self.board.reset_board()
            board = self.board.get_board()

            self.__print_board(board)

            finish = False
            for i in range(9):
                for p in [self.P1, self.P2]:
                    list_moves = Board.get_available_moves(board)

                    if(len(list_moves) == 0):
                        self.__print_board(board)
                        print('Pas de bol, Egalité.')
                        finish = True
                        break
                    
                    x,y = p.instance.play_move(p.pawn, self.board.get_board())
                    Morpion.clean()

                    self.board.set_move(p.pawn, x, y)

                    if(Board.isPlayerWin(self.board.get_board(), p.pawn)):
                        self.__print_board(board)
                        print('Bravo, Joueur ',p.pawn,' a gagné.')
                        p.im_winner()
                        finish = True
                        break 
                    
                    self.__print_board(board)
                
                if finish:
                    break

            party_counter += 1
            
            answer = input("play again? (y/n): ")
            if answer != "y":
                playing = False

        print("Player 1 gagnant: ", self.P1.win_count, " - Player 2 gagnant: ", self.P2.win_count, " - égalités: " , party_counter - self.P1.win_count - self.P2.win_count)

    def play(self):
        self.__initialize_game()
        self.__play_game()

    #todo : pygame?
    def __print_board(self, board):
        if(self.P1.instance.is_autobot and self.P2.instance.is_autobot):
            return
            
        print()
        print('    ','A', "|", 'B', "|", 'C')
        print("---------------")
        print('1   ',board[0][0], "|", board[0][1], "|", board[0][2])
        print("---------------")
        print('2   ',board[1][0], "|", board[1][1], "|", board[1][2])
        print("---------------")
        print('3   ',board[2][0], "|", board[2][1], "|", board[2][2])

    def clean():
        """
        Clears the console
        """
        os_name = platform.system().lower()
        if 'windows' in os_name:
            system('cls')
        else:
            system('clear')

morbac = Morpion()
morbac.play()