from os import system
from render.pygame_render import PygameRender
from songs.song_manager import SongManager
from board import Board
from player import Player, PlayerPawn
from player_factory import PlayerFactory
from time import sleep
from render.graphical_manager import GraphicalManager

class Morpion():

    def __init__(self, render):
        self.board = Board(PlayerPawn.NONE.value)
        self.factory = PlayerFactory()

        #instanciate interface
        GraphicalManager.initialize_instance(render)

        #activate sound if graphical interface
        activate_sound = isinstance(render, PygameRender)
        SongManager.get_instance().activate_songs(activate_sound)

    def __initialize_instance(self):
        '''
            Initialize instance of Morpion
        '''
        player_types = [0,0]
        
        SongManager.get_instance().menu_song()
        #instanciate players (2)
        for i in range(0, len(player_types)):
            player_types[i] = GraphicalManager.get_instance().print_main_menu(i)

        self.P1 = Player(self.factory.create_player(player_types[0]), PlayerPawn.P1.value)
        self.P2 = Player(self.factory.create_player(player_types[1]), PlayerPawn.P2.value)

        if self.P1.instance.is_need_reinforcement:
            self.P1.test_ia_initialisation()
        if self.P2.instance.is_need_reinforcement:
            self.P2.test_ia_initialisation()

    def __play_game(self):
        '''
            Start play
        '''
        #todo: try/catch
        playing= True
        party_counter = 0
        while playing:
            SongManager.get_instance().fight()

            self.board.reset_board()
            board = self.board.get_board()

            GraphicalManager.get_instance().print_board(board)

            finish = False
            for _ in range(9):
                for p in [self.P1, self.P2]:

                    if(Board.get_end_of_party(board)):
                        GraphicalManager.get_instance().print_board(board)
                        SongManager.get_instance().game_over(False)
                        GraphicalManager.get_instance().end_of_party('Pas de bol, Egalité.', board)
                        
                        finish = True
                        break
                    
                    if p.instance.is_autobot:
                        sleep(1)
                    x,y = p.instance.play_move(p.pawn, self.board.get_board())
                    SongManager.get_instance().user_play_notification(p.pawn)
                    self.board.set_move(p.pawn, x, y)

                    if(Board.is_player_win(self.board.get_board(), p.pawn)):
                        GraphicalManager.get_instance().print_board(board)
                        SongManager.get_instance().game_over(True)
                        msg = 'Bravo, Joueur {} a gagné.'.format(p.pawn)
                        GraphicalManager.get_instance().end_of_party(msg, board)

                        p.im_winner()
                        finish = True
                        break 
                    
                    GraphicalManager.get_instance().print_board(board)

                if finish:
                    break

            party_counter += 1
            
            SongManager.get_instance().end_of_party()
            playing = GraphicalManager.get_instance().yes_no_screen('Encore une partie?')

        GraphicalManager.get_instance().print_synthesis(type(self.P1.instance).__name__, self.P1.get_win_counter(), type(self.P2.instance).__name__, self.P2.get_win_counter(), party_counter - self.P1.get_win_counter() - self.P2.get_win_counter())
        
        
    def play(self):
        self.__initialize_instance()
        self.__play_game()
