from os import system
import sys
import pygame
from itertools import cycle

class GraphicalRender():
    __instance = None

    def get_instance():
        if(GraphicalRender.__instance == None):
            __instance = GraphicalRender()
        
        return __instance

    def __init__(self):
                      
        pygame.init()
        self.size = self.width, self.height = 600, 400

        # Colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.orange = (255,69,0)
        self.blue = (40, 120, 230)

        self.screen = pygame.display.set_mode(self.size)

        self.mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
        self.largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
        self.smallFont = pygame.font.Font("OpenSans-Regular.ttf", 16)
        self.moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)


    #todo : pygame?
    def print_board(self, board):
        '''
            print the board to the screen
        '''
        self.__display_board(board)

        pygame.display.flip()


    def user_interact(self, board):
        while True:
            
            tiles  = self.__display_board(board)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # Check for a user move
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse = pygame.mouse.get_pos()
                    for i in range(3):
                        for j in range(3):
                            if (tiles[i][j].collidepoint(mouse)):
                                return j, i

            pygame.display.flip()

    def print_main_menu(self, player):
        while(True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            # Draw game board
            tile_size = 240
            tile_origin = (self.width / 2 - tile_size - 20,
                        self.height / 2 - tile_size / 2 - 20)
            tiles = []
            
            self.display_static('Selection joueur {}'.format( player + 1))

            users = ['Human', 'Random', 'Dnn', 'MinMax']

            menu_index = 0
            for i in range(2):
                row = []
                for j in range(2):
                    rect = pygame.Rect(
                        tile_origin[0] + j * tile_size + j * 40,
                        tile_origin[1] + i * tile_size / 2 + i * 40,
                        tile_size, tile_size / 2
                    )
                    pygame.draw.rect(self.screen, self.white, rect, 3)

                    move = self.moveFont.render(users[menu_index], True, self.white)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    self.screen.blit(move, moveRect)
                    row.append(rect)
                    menu_index += 1
                tiles.append(row)

            # Check for a user selection
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse = pygame.mouse.get_pos()
                    for i in range(2):
                        for j in range(2):
                            if (tiles[i][j].collidepoint(mouse)):
                                return j + (i * 2) + 1

            pygame.display.flip()


    def __display_board(self, board):
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

                    move = self.moveFont.render(board[i][j], True, self.white)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    self.screen.blit(move, moveRect)
                    row.append(rect)
                tiles.append(row)

            return tiles

    def display_warning(self, message, board):
        BLINK_EVENT = pygame.USEREVENT + 0
        clock = pygame.time.Clock()
        pygame.time.set_timer(BLINK_EVENT, 300)
        on_text_surface = self.smallFont.render(
            message, True, self.orange
        )
        blink_rect = on_text_surface.get_rect()
        blink_rect.center = (self.width / 2, 350)
        off_text_surface = pygame.Surface(blink_rect.size)
        blink_surfaces = cycle([on_text_surface, off_text_surface])
        blink_surface = next(blink_surfaces)

        end_warn = False
        blink_counter = 0
        while not end_warn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == BLINK_EVENT:
                    blink_surface = next(blink_surfaces)
                    if(blink_counter < 4):
                        blink_counter += 1
                    else :
                        end_warn = True

            self.__display_board(board)
            self.screen.blit(blink_surface, blink_rect)
            pygame.display.update()
            clock.tick(60)

    
    def display_static(self, message, board = None):
        if( board != None):
            self.__display_board(board)
        title = self.smallFont.render(message, True, self.blue)
        titleRect = title.get_rect()
        titleRect.center = ((self.width / 2), 30)
        self.screen.blit(title, titleRect)
        pygame.display.flip()

    def yes_no_screen(self, message):
        while True:
            self.display_static(message)
            # Draw buttons
            tile_size = 60
            tile_origin = (self.width / 2 - (1.5 * tile_size),
                            200)
            column = []
            again = ['Oui', 'Non']
            for i in range(0, 2):
                rect = pygame.Rect(
                        tile_origin[0] + i * tile_size + i * 60,
                        tile_origin[1],
                        tile_size, tile_size
                    )
                pygame.draw.rect(self.screen, self.white, rect, 3)
                move = self.smallFont.render(again[i], True, self.white)
                moveRect = move.get_rect()
                moveRect.center = rect.center
                self.screen.blit(move, moveRect)
                column.append(rect)

            # Check for end of party
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse = pygame.mouse.get_pos()
                    for i in range(2):
                            if (column[i].collidepoint(mouse)):
                                return i == 0

            pygame.display.flip()


    def end_of_party(self, message, board):
        while True:
            self.display_static(message)
            self.__display_board(board)

            # Draw game board
            tile_size = 80
            tile_origin = (self.width / 2 - (0.5 * tile_size),
                            340)

            rect = pygame.Rect(
                        tile_origin[0],
                        tile_origin[1],
                        tile_size, tile_size / 2
                    )
            pygame.draw.rect(self.screen, self.white, rect, 3)
            move = self.smallFont.render('Suivant', True, self.white)
            moveRect = move.get_rect()
            moveRect.center = rect.center
            self.screen.blit(move, moveRect)

            # Check for end of party
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse = pygame.mouse.get_pos()
                    for i in range(2):
                            if (rect.collidepoint(mouse)):
                                return i == 0

            pygame.display.flip()

    def configuration_of_simulations(self):
        center_x, center_y = (self.width / 2 - 50, self.height / 2)
        prompt = self.smallFont.render('Entrez un nombre : ', True, self.white)
        prompt_rect = prompt.get_rect(center=(center_x, center_y))
        
        user_input_value = ""
        user_input = self.smallFont.render(user_input_value, True, self.orange)
        user_input_rect = user_input.get_rect(topleft=prompt_rect.topright)
        clock = pygame.time.Clock()
        next = False
        
        while not next:
            self.display_static("Nb entraintement de l'IA:")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    continuer = False
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        next = True
                        break
                    elif event.key == pygame.K_BACKSPACE:
                        user_input_value = user_input_value[:-1]
                    elif event.unicode.isdigit() and len(user_input_value) < 5:
                        user_input_value += event.unicode
                    user_input = self.smallFont.render(user_input_value, True, self.white)
                    user_input_rect = user_input.get_rect(topleft=prompt_rect.topright)
        
            clock.tick(30)
        
            self.screen.fill(0)
            self.screen.blit(prompt, prompt_rect)
            self.screen.blit(user_input, user_input_rect)
            pygame.display.flip()
        
        return int(user_input_value)
        
    def print_synthesis(self, player_X, player_O, draws):
        while True:
            self.display_static('Résumé des parties')

            results = ['Joueur X gagnant: {}'.format(player_X), 'Joueur 0 gagnant: {}'.format(player_O),
                        'Egalités: {}'.format(draws)]

            for i in range(0, 3):
                title = self.smallFont.render(results[i], True, self.white)
                titleRect = title.get_rect()
                titleRect.center = ((self.width / 2), 130 + i * 50)
                self.screen.blit(title, titleRect)

            # finish button
            tile_size = 80
            tile_origin = (self.width / 2 - (0.5 * tile_size),
                            340)

            rect = pygame.Rect(
                        tile_origin[0],
                        tile_origin[1],
                        tile_size, tile_size / 2
                    )
            pygame.draw.rect(self.screen, self.white, rect, 3)
            move = self.smallFont.render('Terminer', True, self.white)
            moveRect = move.get_rect()
            moveRect.center = rect.center
            self.screen.blit(move, moveRect)

            # Check for end of party
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse = pygame.mouse.get_pos()
                    for i in range(2):
                            if (rect.collidepoint(mouse)):
                                return i == 0

            pygame.display.flip()
