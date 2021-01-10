from os import system
import platform
from board import Board
from player import Player, PlayerPawn
from player_factory import PlayerFactory, PlayerType
from graphical_render import GraphicalRender

class Morpion():

    def __init__(self):
        self.board = Board(PlayerPawn.NONE.value)
        self.factory = PlayerFactory()

    def __initialize_game(self):
        next = False
        player_types = [0,0]
        i=1
        
        for i in range(0, len(player_types)):
            player_types[i] = GraphicalRender.get_instance().print_main_menu(i)
        # for i in range(0, len(player_types)):
        #     while(not next):
        #         p = input("(Joueur {})  {}:Humain - {}:random - {}:cnn - {}:MinMax  : "
        #                         .format(i+1, PlayerType.Human.value, PlayerType.Random.value, PlayerType.Dnn.value, PlayerType.MinMax.value))
                
        #         if(p.isdigit() and int(p) >0 and int(p) < 5):
        #             next = True
        #             player_types[i] = int(p)

        #     next = False

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

            #self.__print_board(board)

            finish = False
            for i in range(9):
                for p in [self.P1, self.P2]:
                    list_moves = Board.get_available_moves(board)

                    if(Board.get_end_of_party(board)):
                        self.__print_board(board)
                        #GraphicalRender.get_instance().display_static('Pas de bol, Egalité.', board)
                        GraphicalRender.get_instance().end_of_party('Pas de bol, Egalité.', board)
                        
                        finish = True
                        break
                    
                    x,y = p.instance.play_move(p.pawn, self.board.get_board())
                    Morpion.clean()

                    self.board.set_move(p.pawn, x, y)

                    if(Board.is_player_win(self.board.get_board(), p.pawn)):
                        self.__print_board(board)
                        msg = 'Bravo, Joueur {} a gagné.'.format(p.pawn)
                        GraphicalRender.get_instance().end_of_party(msg, board)

                        p.im_winner()
                        finish = True
                        break 
                    
                    self.__print_board(board)
                
                if finish:
                    break

            party_counter += 1
            
            playing = GraphicalRender.get_instance().yes_no_screen('Encore une partie?')
            # answer = input("play again? [y/n]: ")
            # if answer != "y":
            #     playing = False


        #print("Player 1 gagnant: ", self.P1.get_win_counter(), " - Player 2 gagnant: ", self.P2.get_win_counter(), " - égalités: " , party_counter - self.P1.get_win_counter() - self.P2.get_win_counter())
        GraphicalRender.get_instance().print_synthesis(self.P1.get_win_counter(), self.P2.get_win_counter(), party_counter - self.P1.get_win_counter() - self.P2.get_win_counter())

    def play(self):
        self.__initialize_game()
        self.__play_game()

    #todo : pygame?
    def __print_board(self, board):
        GraphicalRender.get_instance().print_board(board)
       

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