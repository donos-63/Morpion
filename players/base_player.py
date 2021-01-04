class base_player():

    def initialize_simulation(self, _):
        raise Exception('base_player.initialize_simulation', 'not implemented')

    def play_move(self, player, board):
        raise Exception('base_player.play_move', 'not implemented')
