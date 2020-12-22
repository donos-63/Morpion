import os
import random
from model import TicTacToeModel
from player import Player
from tensorflow import keras

import copy

PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = ' '
PLAYER_X_VAL = -1
PLAYER_O_VAL = 1
EMPTY_VAL = 0
HORIZONTAL_SEPARATOR = ' | '
VERTICAL_SEPARATOR = '---------------'
GAME_STATE_X = -1
GAME_STATE_O = 1
GAME_STATE_DRAW = 0
GAME_STATE_NOT_ENDED = 2
playerXWins = 0
playerOWins = 0
draws = 0
player = Player("X")
totalWins = 0
nnPlayerWins = 0
randomPlayerWins = 0
draws = 0
numberOfGames = 0


class Game:

    def __init__(self):
        self.resetBoard()
        self.trainingHistory = []
        self.player = Player("X")

    def resetBoard(self):
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self.boardHistory = []

    # Afficher la grille
    def printBoard(self):
        print(VERTICAL_SEPARATOR)
        for i in range(len(self.board)):
            print(' ', end='')
            for j in range(len(self.board[i])):
                if PLAYER_X_VAL == self.board[j][i]:
                    print(PLAYER_X, end='')
                elif PLAYER_O_VAL == self.board[j][i]:
                    print(PLAYER_O, end='')
                elif EMPTY_VAL == self.board[j][i]:
                    print(EMPTY, end='')
                print(HORIZONTAL_SEPARATOR, end='')
            print(os.linesep)
            print(VERTICAL_SEPARATOR)

    def getGameResult(self):
        finPartie = 0
        
        # Détection si un joueur a rempli une ligne, une colonne, ou une diagonale
        if (str(self.board[0][0]) == str(self.board[1][0]) and str(self.board[1][0]) == str(self.board[2][0]) and int(self.board[0][0]) != 0 and int(self.board[1][0]) != 0 and int(self.board[2][0]) != 0):
            finPartie = 1
        if (str(self.board[0][1]) == str(self.board[1][1]) and str(self.board[1][1]) == str(self.board[2][1]) and int(self.board[0][1]) != 0 and int(self.board[1][1]) != 0 and int(self.board[2][1]) != 0):
            finPartie = 1
        if (str(self.board[0][2]) == str(self.board[1][2]) and str(self.board[1][2]) == str(self.board[2][2]) and int(self.board[0][2]) != 0 and int(self.board[1][2]) != 0 and int(self.board[2][2]) != 0):
            finPartie = 1
        if (str(self.board[0][0]) == str(self.board[0][1]) and str(self.board[0][1]) == str(self.board[0][2]) and int(self.board[0][0]) != 0 and int(self.board[0][1]) != 0 and int(self.board[0][2]) != 0):
            finPartie = 1
        if (str(self.board[1][0]) == str(self.board[1][1]) and str(self.board[1][1]) == str(self.board[1][2]) and int(self.board[1][0]) != 0 and int(self.board[1][1]) != 0 and int(self.board[1][2]) != 0):
            finPartie = 1
        if (str(self.board[2][0]) == str(self.board[2][1]) and str(self.board[2][1]) == str(self.board[2][2]) and int(self.board[2][0]) != 0 and int(self.board[2][1]) != 0 and int(self.board[2][2]) != 0):
            finPartie = 1
        if (str(self.board[0][0]) == str(self.board[1][1]) and str(self.board[1][1]) == str(self.board[2][2]) and int(self.board[0][0]) != 0 and int(self.board[1][1]) != 0 and int(self.board[2][2]) != 0):
            finPartie = 1
        if (str(self.board[0][2]) == str(self.board[1][1]) and str(self.board[1][1]) == str(self.board[2][0]) and int(self.board[0][2]) != 0 and int(self.board[1][1]) != 0 and int(self.board[2][0]) != 0):
            finPartie = 1
            
        # La grille est remplie
        if (str(self.getAvailableMoves()) == "[]"):
            finPartie = 1
            
        # Lorsqu'une partie est terminée, remplissage de la grille

        if (finPartie == 1):
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    if self.board[i][j] == EMPTY_VAL:
                        if (random.randint(0, 1) == 0):
                            self.board[i][j] == "1"
                        else:
                            self.board[i][j] == "-1"
                            
        else:
            return GAME_STATE_NOT_ENDED

        # Détection par ligne
        for i in range(len(self.board)):
            candidate = self.board[i][0]
            for j in range(len(self.board[i])):
                if candidate != self.board[i][j]:
                    candidate = 0
            if candidate != 0:
                return candidate

        # Détection par colonne
        for i in range(len(self.board)):
            candidate = self.board[0][i]
            for j in range(len(self.board[i])):
                if candidate != self.board[j][i]:
                    candidate = 0
            if candidate != 0:
                return candidate

        # Diagonale 1
        candidate = self.board[0][0]
        for i in range(len(self.board)):
            if candidate != self.board[i][i]:
                candidate = 0
        if candidate != 0:
            return candidate

        # Diagonale 2
        candidate = self.board[0][2]
        for i in range(len(self.board)):
            if candidate != self.board[i][len(self.board[i]) - i - 1]:
                candidate = 0
        if candidate != 0:
            return candidate

        return GAME_STATE_DRAW


    def getAvailableMoves(self):
        availableMoves = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if (self.board[i][j]) == EMPTY_VAL:
                    availableMoves.append([i, j])
        return availableMoves

    def addToHistory(self, board):
        self.boardHistory.append(board)

    def move(self, position, player):
        availableMoves = self.getAvailableMoves()
        # Positionnement du joueur dans la grille
        for i in range(len(availableMoves)):
            if position[0] == availableMoves[i][0] and position[1] == availableMoves[i][1]:
                self.board[position[0]][position[1]] = player
                self.addToHistory(copy.deepcopy(self.board))

    # Simulation d'une partie
    def simulate(self, playerToMove):

        # La partie continue tant que la partie n'est pas terminée
        while (self.getGameResult() == GAME_STATE_NOT_ENDED):

            # Détection des mouvements disponibles
            availableMoves = self.getAvailableMoves()
            selectedMove = availableMoves[random.randrange(0, len(availableMoves))]
            
            # Changement de tour
            self.move(selectedMove, playerToMove)
            if playerToMove == PLAYER_X_VAL:
                playerToMove = PLAYER_O_VAL
            else:
                playerToMove = PLAYER_X_VAL

        # Ajout des données dans le model
        for historyItem in self.boardHistory:
            self.trainingHistory.append((self.getGameResult(), copy.deepcopy(historyItem)))

    def simulateNeuralNetwork(self, nnPlayer, model):
        playerToMove = PLAYER_X_VAL
        while (self.getGameResult() == GAME_STATE_NOT_ENDED):
            
            # L'ordinateur sélectionne une case
            if nnPlayer == PLAYER_O_VAL:
                availableMoves = self.getAvailableMoves()
                maxValue = 0
                bestMove = availableMoves[0]
                for availableMove in availableMoves:
                    boardCopy = copy.deepcopy(self.board)
                    boardCopy[availableMove[0]][availableMove[1]] = nnPlayer
                    if nnPlayer == PLAYER_X_VAL:
                        value = model.predict(boardCopy, 0)
                    else:
                        value = model.predict(boardCopy, 2)
                    if value > maxValue:
                        maxValue = value
                        bestMove = availableMove
                selectedMove = bestMove
                
            # Le joueur sélectionne une case
            if nnPlayer == PLAYER_X_VAL:
                selectedMove = ""
                while (selectedMove == ""):
                    print('Choisissez votre case :')
                    saisie = input()
                    if (saisie == "1" and self.board[0][2] == 0):
                        selectedMove = [0,2]
                    elif (saisie == "2" and self.board[1][2] == 0):
                        selectedMove = [1,2]
                    elif (saisie == "3" and self.board[2][2] == 0):
                        selectedMove = [2,2]
                    elif (saisie == "4" and self.board[0][1] == 0):
                        selectedMove = [0,1]
                    elif (saisie == "5" and self.board[1][1] == 0):
                        selectedMove = [1,1]
                    elif (saisie == "6" and self.board[2][1] == 0):
                        selectedMove = [2,1]
                    elif (saisie == "7" and self.board[0][0] == 0):
                        selectedMove = [0,0]
                    elif (saisie == "8" and self.board[1][0] == 0):
                        selectedMove = [1,0]
                    elif (saisie == "9" and self.board[2][0] == 0):
                        selectedMove = [2,0]
                    if (selectedMove == ""):
                        print('Entrée non valide')

            # Changement de tour du joueur
            self.move(selectedMove, nnPlayer)
            if nnPlayer == PLAYER_X_VAL:
                nnPlayer = PLAYER_O_VAL
            else:
                nnPlayer = PLAYER_X_VAL

            self.printBoard()

    def getTrainingHistory(self):
        return self.trainingHistory

    # Nombre de parties uniquement jouées par l'ordinateur dans le but d'entraîner le model
    def simulateManyGames(self, playerToMove, numberOfGames):
        for i in range(numberOfGames):
            self.resetBoard()
            self.simulate(playerToMove)

if __name__ == "__main__":
    game = Game()
    partie = True

    ticTacToeModel = TicTacToeModel(9, 3, 100, 32)

    # Chargement du model ou création si inexistant
    try:
        ticTacToeModel.model = keras.models.load_model("morbac.h5")
        print(ticTacToeModel.model.layers[0])
        # for historyItem in ticTacToeModel.model:
        #     self.trainingHistory.append((ticTacToeModel.model, copy.deepcopy(historyItem)))
        print("Chargement du modèle sauvegardé")
    except:
        print("Création du modèle")
        print ("J'apprends à jouer")
        game.simulateManyGames(1, 100)
        ticTacToeModel.train(game.getTrainingHistory())

    while (partie == True):

        # Sélection au sort de celui qui commmence
        print ("Le jeu commence")
        print ("Tirage au sort")
        if (random.randint(0, 1) == 0):
            player = Player(PLAYER_X_VAL)
            print ("A vous de commencer")
        else:
            player = Player(PLAYER_O_VAL)
            print ("Je commence")
        joueur = player.get_player()

        # Lancement de la partie
        game.resetBoard()
        game.simulateNeuralNetwork(joueur, ticTacToeModel)

        print("Partie terminée")

        # Vérifier qui a gagné
        if (game.getGameResult() == GAME_STATE_DRAW):
            draws = draws + 1
            print ("Egalité")
        elif (game.getGameResult() == PLAYER_X_VAL):
            nnPlayerWins = nnPlayerWins + 1
            print ("Vous avez gagné")
        elif (game.getGameResult() == PLAYER_O_VAL):
            randomPlayerWins = randomPlayerWins + 1
            print ("J'ai gagné")

        numberOfGames = numberOfGames + 1

        print ('Victoires du joueur (X)     : ' + str(int(nnPlayerWins * 100/numberOfGames)) + '%')
        print ('Victoires de la machine (O) : ' + str(int(randomPlayerWins * 100 / numberOfGames)) + '%')
        print ('Egalité                     : ' + str(int(draws * 100 / numberOfGames)) + '%')

        game.printBoard()

        # Proposer de continuer la partie
        validationChoix = ""
        while (validationChoix == ""):
            print('Voulez-vous continuer (o/n) ? :')
            choix = input()
            if (choix == "o"):
                validationChoix = "ok"
                
            if (choix == "n"):
                partie = False
                validationChoix = "ok"
                print ("Au revoir")
            if (validationChoix == ""):
                print('Choix non valide')

        # Learning et sauvegarde du model
        print ("Je réfléchis à de nouvelles stratégies")
        game.simulateManyGames(1, 100)
        ticTacToeModel.train(game.getTrainingHistory())

