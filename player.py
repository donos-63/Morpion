from enum import Enum
from render.graphical_manager import GraphicalManager

class PlayerPawn(Enum):
    P1 = 'X'
    P2 = 'O'
    NONE = '-'

class Player():

    def __init__(self, player, pawn):
        self.instance = player
        self.pawn = pawn
        self.__win_count = 0

    def test_ia_initialisation(self):
        '''
            check if current instance of player need simulation, then launch
        '''
        if self.instance.is_need_reinforcement:
            if self.instance.is_reinforcement_exists():

                force = GraphicalManager.get_instance().yes_no_screen('Une simulation existe. Forcer une nouvelle?')
                if not force:
                    self.instance.load_simulation()
                    return

            nb_training = 0
            nb_training = GraphicalManager.get_instance().configuration_of_simulations()

            self.instance.initialize_simulation(nb_training)

    def im_winner(self):
        '''
            increment number of party won
        '''
        self.__win_count += 1

    def get_win_counter(self):
        '''
            return number of party won
        '''
        return self.__win_count

    def get_oponnent_for(player):
        '''
            get oponnent for the given player
        '''
        return PlayerPawn.P1.value if player == PlayerPawn.P2.value else PlayerPawn.P2.value

    def player_to_numerical(player):
        '''
            Convert a player pawn to a number
        '''
        if(player == PlayerPawn.P1.value):
            return 1
        if(player == PlayerPawn.P2.value):
            return -1
        if(player == PlayerPawn.NONE.value):
            return 0       

    def player_from_numerical(player):
        '''
            Convert a numeric to a player pawn
        '''
        if(player == 1):
            return PlayerPawn.P1.value
        if(player == -1):
            return PlayerPawn.P2.value
        if(player == 0):
            return PlayerPawn.NONE.value           




