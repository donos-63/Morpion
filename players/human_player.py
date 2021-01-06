import string
from players.base_player import base_player
from board import Board


class HumanPlayer(base_player):
    
    def play_move(self, _, board):
        '''
            Select move by human
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
            if self.is_move_valid(Board.get_available_moves(board), x, y):
                return x, y

            print('Mauvais emplacement, veuillez recommencer')

    def is_move_valid(self, list_available_moves, x, y):
        '''
            Check if move is possible
        '''
        return (x,y) in list_available_moves

    def __init__(self):
        self.need_reinforcement = False
        self.is_autobot = False
