from os import system
import sys
import pygame
import platform
import numpy as np
from board import Board
from player import Player, PlayerPawn
from player_factory import PlayerFactory, PlayerType


class MorpionGraphical():


    def __init__(self):
        self.board = Board(PlayerPawn.NONE.value)
        self.factory = PlayerFactory()
                
        pygame.init()
        self.size = self.width, self.height = 600, 400

        # Colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

        self.screen = pygame.display.set_mode(self.size)

        self.mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
        self.largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
        self.moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)


    def __initialize_game(self):
        next = False
        player_types = [0,0]
        i=1
        
        for i in range(0, len(player_types)):
            while(not next):
                p = input("(Joueur {})  {}:Humain - {}:random - {}:cnn - {}:MinMax  : "
                                .format(i+1, PlayerType.Human.value, PlayerType.Random.value, PlayerType.Dnn.value, PlayerType.MinMax.value))
                
                if(p.isdigit() and int(p) >0 and int(p) < 5):
                    next = True
                    player_types[i] = int(p)

            next = False

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
            for i in range(9):
                for p in [self.P1, self.P2]:
                    list_moves = Board.get_available_moves(board)

                    if(Board.get_end_of_party(board)):
                        self.__print_board(board)
                        print('Pas de bol, Egalité.')
                        finish = True
                        break
                    
                    x,y = p.instance.play_move(p.pawn, self.board.get_board())
                    MorpionGraphical.clean()

                    self.board.set_move(p.pawn, x, y)

                    if(Board.is_player_win(self.board.get_board(), p.pawn)):
                        self.__print_board(board)
                        print('Bravo, Joueur ',p.pawn,' a gagné.')
                        p.im_winner()
                        finish = True
                        break 
                    
                    self.__print_board(board)
                
                if finish:
                    break

            party_counter += 1
            
            answer = input("play again? [y/n]: ")
            if answer != "y":
                playing = False

        print("Player 1 gagnant: ", self.P1.get_win_counter(), " - Player 2 gagnant: ", self.P2.get_win_counter(), " - égalités: " , party_counter - self.P1.get_win_counter() - self.P2.get_win_counter())

    def play(self):
        self.__initialize_game()
        self.__play_game()

    #todo : pygame?
    def __print_board(self, board):
        '''
            print the board to the screen
        '''
        if(self.P1.instance.is_autobot and self.P2.instance.is_autobot):
            return
            
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Draw game board
            tile_size = 80
            tile_origin = (self.width / 2 - (1.5 * tile_size),
                        self.height / 2 - (1.5 * tile_size))
            tiles = []
            for i in range(3):
                row = []
                for j in range(3):
                    rect = pygame.Rect(
                        tile_origin[0] + j * tile_size,
                        tile_origin[1] + i * tile_size,
                        tile_size, tile_size
                    )
                    pygame.draw.rect(self.screen, self.white, rect, 3)

                    if board[i][j] != PlayerPawn.NONE:
                        move = self.moveFont.render(board[i][j], True, self.white)
                        moveRect = move.get_rect()
                        moveRect.center = rect.center
                        self.screen.blit(move, moveRect)
                    row.append(rect)
                tiles.append(row)
            # Check for a user move
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                for i in range(3):
                    for j in range(3):
                        if (tiles[i][j].collidepoint(mouse)):
                            u= (i, j)

            pygame.display.flip()



    def clean():
        """
        Clears the console
        """
        os_name = platform.system().lower()
        if 'windows' in os_name:
            system('cls')
        else:
            system('clear')

morbac = MorpionGraphical()
morbac.play()