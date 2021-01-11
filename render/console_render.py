from os import system
import platform
from player_factory import PlayerType

class ConsoleRender():
    def print_board(self, board):
        '''
            print the board to the screen
        '''
        self.__clean()
   
        self.__display_board(board)
        

    def user_interact(self, board):
        '''
            manage user interaction whith board
        '''
        while True:
            next = False

            x = y = 0
            while(not next):
                x = input("Entrez l'abscisse compris entre A et C : ")
                if(x.upper() in ['A','B','C']):
                    next = True

            next=False
            while(not next):
                y = input("Entrez l'ordonnée compris entre 1 et 3 : ")
                if(y.isdigit() and int(y) >0 and int(y) < 4):
                    next = True

            x = ['A','B','C'].index(x.upper())
            y = int(y) - 1

            return x, y

    def print_main_menu(self, player):
        '''
            print main menu (player selection)
        '''        
        next = False
        player_type = -1

        while(not next):
                p = input("(Joueur {})  {}:Humain - {}:random - {}:cnn - {}:MinMax  : "
                                .format(player + 1, PlayerType.Human.value, PlayerType.Random.value, PlayerType.CNN.value, PlayerType.MinMax.value))
                
                if(p.isdigit() and int(p) >0 and int(p) < 5):
                    next = True
                    player_type = int(p)

        return player_type

    def __display_board(self, board):
        '''
            display board in screen
        '''
        # Draw game board
            
        print()
        print('    ','A', "|", 'B', "|", 'C')
        print("---------------")
        print('1   ',board[0][0], "|", board[0][1], "|", board[0][2])
        print("---------------")
        print('2   ',board[1][0], "|", board[1][1], "|", board[1][2])
        print("---------------")
        print('3   ',board[2][0], "|", board[2][1], "|", board[2][2])


    def display_warning(self, message, _):
        '''
            display warning (blink text)
        '''        
        print(message)

    
    def display_static(self, message, board = None):
        '''
            display static message
        '''        
        print(message)

    def yes_no_screen(self, message):
        '''
            display screen with message and yes/no options
        '''        
        answer = input(message + ' [y/n] :  ')
        if answer != "y":
            return False
        else:
            return True


    def end_of_party(self, message, _):
        '''
            display end of party
        '''        
        print(message)


    def configuration_of_simulations(self):
        '''
            display menu to customize simulation
        '''        
        next = False
        nb_training = 0
        while(not next):
            nb_training  = input("Nb entraintement de l'IA  :  ")
            if(nb_training.isdigit() and int(nb_training) > 0):
                nb_training = int(nb_training)
                next = True

        return nb_training
        
    def print_synthesis(self, type_X, win_X, type_O, win_O, draws):
        '''
            resume the party to the screen
        '''        
        print("Player 1 (", type_X,") gagnant: ", win_X, " - Player 2 (",type_O,") gagnant: ", win_O, " - égalités: " , draws)

    def computer_is_working(self, _):
        '''
            displayed when IA if performing computation
        '''        
        print('computer is computing computations....')


    def __clean(self):
        """
        Clears the console
        """
        os_name = platform.system().lower()
        if 'windows' in os_name:
            system('cls')
        else:
            system('clear')

    