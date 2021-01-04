from enum import Enum

class PlayerPawn(Enum):
    P1 = 'X'
    P2 = 'O'
    NONE = '-'

class Player():

    def __init__(self, player, pawn):
        self.instance = player
        self.pawn = pawn
        self.win_count = 0

    def set_ia_initialisation(self, nb_training):
        if self.instance.need_reinforcement:
                self.instance.initialize_simulation(nb_training)

    def im_winner(self):
        self.win_count += 1

    def reinit_win_counter(self):
        self.win_count = 0

    def get_oponnent_for(player):
        return PlayerPawn.P1.value if player == PlayerPawn.P2.value else PlayerPawn.P2.value

    def player_to_numerical(player):
        if(player == PlayerPawn.P1.value):
            return 1
        if(player == PlayerPawn.P2.value):
            return -1
        if(player == PlayerPawn.NONE.value):
            return 0           




