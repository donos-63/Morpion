# Class Game - Gestion du tableau de jeu
from copy import Error
from players.agent import Agent
from players.player import Player
from board import Board

from random import shuffle

class Game:

    PENALTY = -2
    NEUTRAL = 0
    REWARD = 1

    BOARD_SIZE = 3

    def __init__(self, player1, player2, verbose = True):

        self.__players = [player1, player2]

        self.verbose = verbose

        self.done = False
        self.__board = Board(Game.BOARD_SIZE, self.verbose)

    def is_valid_action(self, coord):
        ligne, col = coord
        return self.__board.is_valid_action(ligne, col)

    def reset(self):
        self.done = False
        self.__board = Board(Game.BOARD_SIZE, self.verbose)

        for player in self.__players:
            if type(player) is Agent: 
                player.reset(self.get_state(player.sign))

    def get_state(self, player_sign):
        """
            Renvoie l'etat du jeu a la demande d'un joueur 
            dont le signe est passe en parametre

            Un emplacement vide vaut 0
            Un emplacement adverse vaut 0.5
            Un emplacement du joueur vaut 1
        """
        tot = []
        for ligne in self.__board.table:
            for element in ligne:
                if element is False:
                    tot.append(0)
                elif element != player_sign:
                    tot.append(0.5)
                elif element == player_sign:
                    tot.append(1)
        return tot

    def start(self):
        while not self.done:
            #Change aleatoirement le premier joueur
            shuffle(self.__players)
            for player in self.__players:
                self.__play(player)

                if self.__win():
                    self.__endGame(player)

                    for p in self.__players:
                        if p == player:
                            # params de remember:  game, reward, done
                            p.remember(
                                self.get_state(p.sign), #state
                                Game.REWARD, #reward
                                self.done # done
                            )
                        else: #perdant
                            p.remember(
                                self.get_state(p.sign), #state
                                Game.PENALTY, #reward
                                self.done # done
                            )
                    break

                elif self.__board.full():
                    self.__endGame(player)
                    
                    for p in self.__players:
                        p.remember(
                            self.get_state(p.sign), #state
                            Game.NEUTRAL, #reward
                            self.done # done
                        )
                    break

                else:
                    
                    player.remember(
                        self.get_state(player.sign), #state
                        Game.NEUTRAL, #reward
                        self.done # done
                    )
                    continue

    def __play(self, player):
        accepted = False
        
        if self.verbose:
            print(f"\nAu tour de {player.sign}.")
            self.__board.show()

        while not accepted:
            ligne, col = player.play(self)
            accepted = self.__board.placer(ligne, col, player.sign)
            if self.verbose: print(f'Valeur entre 1 et {self.BOARD_SIZE}')

    def __endGame(self, player):
        if self.verbose:
            if self.__board.full():
                print('Match nul !')
            else:
                print(f"{player.sign} a gagne !")

            self.__board.show()

        self.done = True

    def __win(self):
        return self.__board.ligne() or self.__board.col() or self.__board.diagonale()

if __name__ == '__main__':
    p1 = Player('O')
    p2 = Player('X')
    game = Game(p1, p2)
    game.start()
