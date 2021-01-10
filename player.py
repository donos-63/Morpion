from enum import Enum
from graphical_render import GraphicalRender

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
        if self.instance.need_reinforcement:
            if self.instance.is_reinforcement_exists():
                # answer = input("Simulation exists. Force new? [y/n]: ")
                # if answer.lower() != "y":
                #     force = False

                force = GraphicalRender.get_instance().yes_no_screen('Simulation exists. Force new?')
                if not force:
                    self.instance.load_simulation()
                    return

                # answer = input("Simulation exists. Force new? [y/n]: ")
                # if answer.lower() != "y":
                #     self.instance.load_simulation()
                #     return

            next = False
            nb_training = 0
            nb_training = GraphicalRender.get_instance().configuration_of_simulations()
            # while(not next):
            #     nb_training  = input("Nb entraintement de l'IA  :  ")
            #     if(nb_training.isdigit() and int(nb_training) > 0):
            #         nb_training = int(nb_training)
            #         next = True

            self.instance.initialize_simulation(nb_training)

    def im_winner(self):
        self.__win_count += 1

    def get_win_counter(self):
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




