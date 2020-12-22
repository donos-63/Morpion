import os
import random
# import MinMaxScaler
from model import TicTacToeModel
from player import Player
from sklearn.preprocessing import MinMaxScaler
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
        # vierge = 0
        # for i in range(len(self.board)):
        #     for j in range(len(self.board[i])):
        #         # print(self.board[i][j])
        #         if (self.board[i][j] == 0):
        #             vierge = 1
        #         else:
        #             vierge = 0
        #             # print("acces2")
        # print("table vierge : " + str(vierge))
        # if (vierge == 0):
        if (str(self.board[0][0]) == str(self.board[1][0]) and str(self.board[1][0]) == str(self.board[2][0]) and int(self.board[0][0]) != 0 and int(self.board[1][0]) != 0 and int(self.board[2][0]) != 0):
            finPartie = 1
            # print("Résultat 1 : " + str(self.board[0][0]) + " " + str(self.board[1][0]) + " " + str(self.board[2][0]))
        if (str(self.board[0][1]) == str(self.board[1][1]) and str(self.board[1][1]) == str(self.board[2][1]) and int(self.board[0][1]) != 0 and int(self.board[1][1]) != 0 and int(self.board[2][1]) != 0):
            finPartie = 1
            # print("Résultat 2 : " + str(self.board[0][1]) + " " + str(self.board[1][1]) + " " + str(self.board[2][1]))
        if (str(self.board[0][2]) == str(self.board[1][2]) and str(self.board[1][2]) == str(self.board[2][2]) and int(self.board[0][2]) != 0 and int(self.board[1][2]) != 0 and int(self.board[2][2]) != 0):
            finPartie = 1
            # print("Résultat 3 : " + str(self.board[0][2]) + " " + str(self.board[1][2]) + " " + str(self.board[2][2]))
        if (str(self.board[0][0]) == str(self.board[0][1]) and str(self.board[0][1]) == str(self.board[0][2]) and int(self.board[0][0]) != 0 and int(self.board[0][1]) != 0 and int(self.board[0][2]) != 0):
            finPartie = 1
            # print("Résultat 4 : " + str(self.board[0][0]) + " " + str(self.board[0][1]) + " " + str(self.board[0][2]))
        if (str(self.board[1][0]) == str(self.board[1][1]) and str(self.board[1][1]) == str(self.board[1][2]) and int(self.board[1][0]) != 0 and int(self.board[1][1]) != 0 and int(self.board[1][2]) != 0):
            finPartie = 1
            # print("Résultat 5 : " + str(self.board[1][0]) + " " + str(self.board[1][1]) + " " + str(self.board[1][2]))
        if (str(self.board[2][0]) == str(self.board[2][1]) and str(self.board[2][1]) == str(self.board[2][2]) and int(self.board[2][0]) != 0 and int(self.board[2][1]) != 0 and int(self.board[2][2]) != 0):
            finPartie = 1
            # print("Résultat 6 : " + str(self.board[2][0]) + " " + str(self.board[2][1]) + " " + str(self.board[2][2]))
        if (str(self.board[0][0]) == str(self.board[1][1]) and str(self.board[1][1]) == str(self.board[2][2]) and int(self.board[0][0]) != 0 and int(self.board[1][1]) != 0 and int(self.board[2][2]) != 0):
            finPartie = 1
            # print("Résultat 7 : " + str(self.board[0][0]) + " " + str(self.board[1][1]) + " " + str(self.board[2][2]))
        if (str(self.board[0][2]) == str(self.board[1][1]) and str(self.board[1][1]) == str(self.board[2][0]) and int(self.board[0][2]) != 0 and int(self.board[1][1]) != 0 and int(self.board[2][0]) != 0):
            finPartie = 1
            # print("Résultat 8 : " + str(self.board[0][2]) + " " + str(self.board[1][1]) + " " + str(self.board[2][0]))
        # print("fin partie : " + str(finPartie))
        # print("Résultat : " + str(self.board[0][1]) + " " + str(self.board[1][1]) + " " + str(self.board[1][2]))

        # if (str(self.board[0][0]) == str(self.board[1][0]) and str(self.board[1][0]) == str(self.board[2][0])):
        #     finPartie = 1
        # if (str(self.board[0][1]) == str(self.board[1][1]) and str(self.board[1][1]) == str(self.board[2][1])):
        #     finPartie = 1
        # if (str(self.board[0][2]) == str(self.board[1][2]) and str(self.board[1][2]) == str(self.board[2][2])):
        #     finPartie = 1
        # if (str(self.board[0][0]) == str(self.board[0][1]) and str(self.board[0][1]) == str(self.board[0][2])):
        #     finPartie = 1
        # if (str(self.board[1][0]) == str(self.board[1][1]) and str(self.board[1][1]) == str(self.board[1][2])):
        #     finPartie = 1
        # if (str(self.board[2][0]) == str(self.board[2][1]) and str(self.board[2][1]) == str(self.board[2][2])):
        #     finPartie = 1
        # if (str(self.board[0][0]) == str(self.board[1][1]) and str(self.board[1][1]) == str(self.board[2][2])):
        #     finPartie = 1
        # if (str(self.board[0][2]) == str(self.board[1][1]) and str(self.board[1][1]) == str(self.board[2][0])):
        #     finPartie = 1

        if (str(self.getAvailableMoves()) == "[]"):
            finPartie = 1
            
        # print ("finPartie : " + str(finPartie))

        if (finPartie == 1):
            # print("Partie terminée")
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    if self.board[i][j] == EMPTY_VAL:
                        if (random.randint(0, 1) == 0):
                            self.board[i][j] == "1"
                        else:
                            self.board[i][j] == "-1"
            # print(str(self.board[0][0]) + " " + str(self.board[1][0]) + " " + str(self.board[2][0]))
            # print(str(self.board[0][1]) + " " + str(self.board[1][1]) + " " + str(self.board[2][1]))
            # print(str(self.board[0][2]) + " " + str(self.board[1][2]) + " " + str(self.board[2][2]))
            # print("")
        else:
            return GAME_STATE_NOT_ENDED

        # for i in range(len(self.board)):
        #     for j in range(len(self.board[i])):
        #         if self.board[i][j] == EMPTY_VAL:
        #             return GAME_STATE_NOT_ENDED

        # Rows
        for i in range(len(self.board)):
            candidate = self.board[i][0]
            for j in range(len(self.board[i])):
                if candidate != self.board[i][j]:
                    candidate = 0
            if candidate != 0:
                return candidate

        # Columns
        for i in range(len(self.board)):
            candidate = self.board[0][i]
            for j in range(len(self.board[i])):
                if candidate != self.board[j][i]:
                    candidate = 0
            if candidate != 0:
                return candidate

        # First diagonal
        candidate = self.board[0][0]
        for i in range(len(self.board)):
            if candidate != self.board[i][i]:
                candidate = 0
        if candidate != 0:
            return candidate

        # Second diagonal
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

    # def printHistory(self):
    #     print(self.boardHistory)

    def move(self, position, player):
        availableMoves = self.getAvailableMoves()
        # print ("mouvements : " + str(availableMoves))
        for i in range(len(availableMoves)):
            if position[0] == availableMoves[i][0] and position[1] == availableMoves[i][1]:
                # print(player)
                # print(str(position[0]) + "  " + str(position[1]))
                self.board[position[0]][position[1]] = player
                self.addToHistory(copy.deepcopy(self.board))


    def simulate(self, playerToMove):
        scaler = MinMaxScaler()
        while (self.getGameResult() == GAME_STATE_NOT_ENDED):
            availableMoves = self.getAvailableMoves()
            #scaler.fit(availableMoves)
            selectedMove = availableMoves[random.randrange(0, len(availableMoves))]
            # selectedMove = scaler.fit(availableMoves)
            # selectedMove = scaler.transform(selectedMove)
            # minmaxscale = MinMaxScaler().fit(availableMoves)
            
            # print(availableMoves)
            # availableMoves = minmaxscale.transform(availableMoves)
            # print(availableMoves)
            # print(random.randint(0, 9))
            self.move(selectedMove, playerToMove)
            if playerToMove == PLAYER_X_VAL:
                playerToMove = PLAYER_O_VAL
            else:
                playerToMove = PLAYER_X_VAL
        # Get the history and build the training set
        # print(self.boardHistory)
        for historyItem in self.boardHistory:
            self.trainingHistory.append((self.getGameResult(), copy.deepcopy(historyItem)))

    def simulateNeuralNetwork(self, nnPlayer, model):
        playerToMove = PLAYER_X_VAL
        while (self.getGameResult() == GAME_STATE_NOT_ENDED):
            # print (nnPlayer)
            # print (PLAYER_O_VAL)
            if nnPlayer == PLAYER_O_VAL:
                # print ("test2")
                availableMoves = self.getAvailableMoves()
                # if playerToMove == nnPlayer:
                maxValue = 0
                bestMove = availableMoves[0]
                for availableMove in availableMoves:
                    # get a copy of a board
                    boardCopy = copy.deepcopy(self.board)
                    boardCopy[availableMove[0]][availableMove[1]] = nnPlayer
                    if nnPlayer == PLAYER_X_VAL:
                        value = model.predict(boardCopy, 0)
                    else:
                        value = model.predict(boardCopy, 2)
                    if value > maxValue:
                        maxValue = value
                        bestMove = availableMove
                    # print (bestMove)
                selectedMove = bestMove
                # else:
                #     selectedMove = availableMoves[random.randrange(0, len(availableMoves))]
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
                # print ("test1")

            # print(selectedMove)
            # selectedMove = [1,1]
            # print (nnPlayer)
            # print (selectedMove)
            # print (PLAYER_X_VAL)
            # print (PLAYER_O_VAL)
            self.move(selectedMove, nnPlayer)
            if nnPlayer == PLAYER_X_VAL:
                nnPlayer = PLAYER_O_VAL
            else:
                nnPlayer = PLAYER_X_VAL
            # print (nnPlayer)

            self.printBoard()

            # print(str(self.board[0][0]) + " " + str(self.board[1][0]) + " " + str(self.board[2][0]))
            # print(str(self.board[0][1]) + " " + str(self.board[1][1]) + " " + str(self.board[2][1]))
            # print(str(self.board[0][2]) + " " + str(self.board[1][2]) + " " + str(self.board[2][2]))
            
            # print(str(self.board[0][0]) + " " + str(self.board[1][0]) + " " + str(self.board[2][0]))
            # print(str(self.board[0][1]) + " " + str(self.board[1][1]) + " " + str(self.board[2][1]))
            # print(str(self.board[0][2]) + " " + str(self.board[1][2]) + " " + str(self.board[2][2]))
            # print("")

    def getTrainingHistory(self):
        return self.trainingHistory

    def simulateManyGames(self, playerToMove, numberOfGames):
        # playerXWins = 0
        # playerOWins = 0
        # draws = 0
        for i in range(numberOfGames):
            self.resetBoard()
            self.simulate(playerToMove)
        #     if self.getGameResult() == PLAYER_X_VAL:
        #         playerXWins = playerXWins + 1
        #     elif self.getGameResult() == PLAYER_O_VAL:
        #         playerOWins = playerOWins + 1
        #     else:
        #         draws = draws + 1
        # totalWins = playerXWins + playerOWins + draws
        # print ('X Wins: ' + str(int(playerXWins * 100/totalWins)) + '%')
        # print('O Wins: ' + str(int(playerOWins * 100 / totalWins)) + '%')
        # print('Draws: ' + str(int(draws * 100 / totalWins)) + '%')

    def simulateManyNeuralNetworkGames(self, nnPlayer, numberOfGames, model, nnPlayerWins, randomPlayerWins, draws):
    # def simulateManyNeuralNetworkGames(self, nnPlayer, numberOfGames, model):
        # nnPlayerWins = 0
        # randomPlayerWins = 0
        # draws = 0
        # print ("NN player")
        # print (nnPlayer)
        # for i in range(numberOfGames):
        # partie = true
        # while (partie = true)
            # print ("Jeu numéro " + str(i))
        self.resetBoard()
        self.simulateNeuralNetwork(nnPlayer, model)
        # print(str(self.getGameResult()) + " et " + str(nnPlayer))

        print("Partie terminée")

        if (self.getGameResult() == GAME_STATE_DRAW):
            draws = draws + 1
            print ("Egalité")
        elif (self.getGameResult() == PLAYER_X_VAL):
            nnPlayerWins = nnPlayerWins + 1
            print ("Vous avez gagné")
        elif (self.getGameResult() == PLAYER_O_VAL):
            randomPlayerWins = randomPlayerWins + 1
            print ("J'ai gagné")

        numberOfGames = numberOfGames + 1

        # totalWins = playerXWins + playerOWins + draws
        # totalWins = nnPlayerWins + randomPlayerWins + draws
        print (numberOfGames)
        print (nnPlayerWins)
        print (randomPlayerWins)
        print (draws)

        print ('Victoires du joueur (X)     : ' + str(int(nnPlayerWins * 100/numberOfGames)) + '%')
        print ('Victoires de la machine (O) : ' + str(int(randomPlayerWins * 100 / numberOfGames)) + '%')
        print ('Egalité                     : ' + str(int(draws * 100 / numberOfGames)) + '%')

        # if self.getGameResult() == nnPlayer:
        #     print ("Vous avez gagné")
        #     nnPlayerWins = nnPlayerWins + 1
        # elif self.getGameResult() == GAME_STATE_DRAW:
        #     draws = draws + 1
        #     print ("Egalité")
        # else: 
        #     randomPlayerWins = randomPlayerWins + 1
        #     print ("J'ai gagné")
        self.printBoard()

            # validationChoix = ""
            # while (validationChoix == ""):
            #     print('Voulez-vous continuer (o/n) :')
            #     choix = input()
            #     if (choix == "o"):
            #         validationChoix = "ok"
            #     if (choix == "n"):
            #         partie = false
            #         validationChoix = "ok"
            #     if (validationChoix == ""):
            #         print('Choix non valide')

        # totalWins = nnPlayerWins + randomPlayerWins + draws

if __name__ == "__main__":
    game = Game()
    partie = True

    ticTacToeModel = TicTacToeModel(9, 3, 100, 32)

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
        # print ("J'apprends à jouer")
        # game.simulateManyGames(1, 100)
        # ticTacToeModel = TicTacToeModel(9, 3, 100, 32)
        # ticTacToeModel.train(game.getTrainingHistory())
        # ticTacToeModel.save("morbac.h5")

        
        # ticTacToeModel = TicTacToeModel(9, 3, 100, 32)

        # try:
        #     ticTacToeModel.model = keras.models.load_model("morbac.h5")
        #     print("Chargement du modèle sauvegardé")
        # except:
        #     print("Création du modèle")
        #     print ("J'apprends à jouer")
        #     game.simulateManyGames(1, 100)
        #     ticTacToeModel.train(game.getTrainingHistory())

        print ("Le jeu commence")
        print ("Tirage au sort")
        if (random.randint(0, 1) == 0):
            # joueur = PLAYER_X_VAL
            # player.set_player(PLAYER_X_VAL)
            player = Player(PLAYER_X_VAL)
            print ("A vous de commencer")
        else:
            # joueur = PLAYER_O_VAL
            # player.set_player(PLAYER_O_VAL)
            player = Player(PLAYER_O_VAL)
            print ("Je commence")
        joueur = player.get_player()
        # game.simulateManyNeuralNetworkGames(joueur, 100, ticTacToeModel)
        # game.simulateManyNeuralNetworkGames(joueur, numberOfGames, ticTacToeModel, nnPlayerWins, randomPlayerWins, draws)

        game.resetBoard()
        game.simulateNeuralNetwork(joueur, ticTacToeModel)

        print("Partie terminée")

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

        print (numberOfGames)
        print (nnPlayerWins)
        print (randomPlayerWins)
        print (draws)

        print ('Victoires du joueur (X)     : ' + str(int(nnPlayerWins * 100/numberOfGames)) + '%')
        print ('Victoires de la machine (O) : ' + str(int(randomPlayerWins * 100 / numberOfGames)) + '%')
        print ('Egalité                     : ' + str(int(draws * 100 / numberOfGames)) + '%')

        game.printBoard()

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

        print ("Je réfléchis à de nouvelles stratégies")
        game.simulateManyGames(1, 100)
        ticTacToeModel.train(game.getTrainingHistory())
    # print("Simulating with Neural Network as O Player:")
    # game.simulateManyNeuralNetworkGames(PLAYER_O_VAL, 10, ticTacToeModel)

