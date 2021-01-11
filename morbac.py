from os import system
from board import Board
from player import Player, PlayerPawn
from player_factory import PlayerFactory, PlayerType
from render.graphical_manager import GraphicalManager

class Morpion():

    def __init__(self, render):
        self.board = Board(PlayerPawn.NONE.value)
        self.factory = PlayerFactory()
        GraphicalManager.initialize_instance(render)

    def __initialize_game(self):
        next = False
        player_types = [0,0]
        i=1
        
        for i in range(0, len(player_types)):
            player_types[i] = GraphicalManager.get_instance().print_main_menu(i)


        self.P1 = Player(self.factory.create_player(player_types[0]), PlayerPawn.P1.value)
        self.P2 = Player(self.factory.create_player(player_types[1]), PlayerPawn.P2.value)

        if self.P1.instance.need_reinforcement:
            self.P1.test_ia_initialisation()
        if self.P2.instance.need_reinforcement:
            self.P2.test_ia_initialisation()

    def __play_game(self):
               
        #todo: try/catch
        playing= True
        party_counter = 0
        while playing:
            self.board.reset_board()
            board = self.board.get_board()

            self.__print_board(board)

            finish = False
            for _ in range(9):
                for p in [self.P1, self.P2]:

                    if(Board.get_end_of_party(board)):
                        self.__print_board(board)
                        GraphicalManager.get_instance().end_of_party('Pas de bol, Egalité.', board)
                        
                        finish = True
                        break
                    
                    x,y = p.instance.play_move(p.pawn, self.board.get_board())

                    self.board.set_move(p.pawn, x, y)

                    if(Board.is_player_win(self.board.get_board(), p.pawn)):
                        self.__print_board(board)
                        msg = 'Bravo, Joueur {} a gagné.'.format(p.pawn)
                        GraphicalManager.get_instance().end_of_party(msg, board)

                        p.im_winner()
                        finish = True
                        break 
                    
                    self.__print_board(board)
                
                if finish:
                    break

            party_counter += 1
            
            playing = GraphicalManager.get_instance().yes_no_screen('Encore une partie?')

        GraphicalManager.get_instance().print_synthesis(self.P1.get_win_counter(), self.P2.get_win_counter(), party_counter - self.P1.get_win_counter() - self.P2.get_win_counter())

    def play(self):
        self.__initialize_game()
        self.__play_game()

    def __print_board(self, board):
        GraphicalManager.get_instance().print_board(board)