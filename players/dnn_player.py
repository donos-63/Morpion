from os import system
from players.base_player import base_player
import sys
import random
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.backend import reshape
from keras.utils.np_utils import to_categorical 
import numpy as np
from player import Player, PlayerPawn
import copy as cp
import players.random_player as rplay
from board import Board
import players.min_max_player as mmplay

class DnnPlayer(base_player):
    # Get best next move for the given player at the given board position
    def play_move(self, player, board):
        scores = []
        
        moves = Board.get_available_moves(board)
        player = Player.player_to_numerical(player)
            
        # Make predictions for each possible move
        for x,y in Board.get_available_moves(board):
            board_numerical = Board.board_to_numercial(board)
            boardWithNewMove = np.array(board_numerical)
            boardWithNewMove[y,x] = player

            prediction = self.model.predict(boardWithNewMove.reshape((-1, 9)))[0]

            winPrediction = prediction[1]
            lossPrediction = prediction[2]
            drawPrediction = prediction[0]
            if winPrediction - lossPrediction > 0:
                scores.append(winPrediction - lossPrediction)
            else:
                scores.append(drawPrediction - lossPrediction)

        bestMoves = np.flip(np.argsort(scores))
        x = int(moves[bestMoves[0]][0])
        y = int(moves[bestMoves[0]][1])
        return x, y

    # Simulate a game
    def simulateGame(self):
        good_trainer = mmplay.MinMaxPlayer()
        random_trainer = rplay.RandomPlayer()

        history = []
        board = Board(PlayerPawn.NONE.value)

        firstplayer = random.randint(1,2)
        playerToMove = self.me.value #dnn ia start
        if firstplayer == 2:
            playerToMove = Player.get_oponnent_for(self.me) #oponnent start

        while Board.get_winner(board.get_board()) == None:
            
            # Chose a move 
            if playerToMove == self.me.value:
                x, y = random_trainer.play_move(playerToMove, board.get_board())
            else:
                #x, y = good_trainer.play_move(Player.get_oponnent_for(self.me.value), board.get_board())
                x, y = random_trainer.play_move(playerToMove, board.get_board())
            
            # Make the move
            board.set_move(playerToMove, x, y)
            
            # Add the move to the history
            history.append((playerToMove, [x,y]))
            
            # Switch the active player
            playerToMove = Player.get_oponnent_for(playerToMove)
            
        return history
    

    # Reconstruct the board from the move list
    def movesToBoard(self, moves, convert_to_numerical = False):
        board = cp.deepcopy( self.initial_board)
        if(convert_to_numerical):
            board = Board.board_to_numercial(board)

        for move in moves:
            player = move[0]
            coords = move[1]
            
            if convert_to_numerical:
                board[coords[0]][coords[1]] = 1 if player == self.me.value else -1
            else:
                board[coords[0]][coords[1]] =player

        return board

    def gamesToWinLossData(self, games):
        X = []
        y = []
        for game in games:
            winner = Board.get_winner(self.movesToBoard(game))
            for move in range(len(game)):
                X.append(self.movesToBoard(game[:(move + 1)], True))
                y.append(winner)

        X = np.array(X).reshape((-1, 9))
        y = np.array(y)
        y = to_categorical(y - y.min()) # draw, X-wins, O-wins to 0, 1, 2
        
        # Return an appropriate train/test split
        trainNum = int(len(X) * 0.8)
        return (X[:trainNum], X[trainNum:], y[:trainNum], y[trainNum:])

    def __init__(self, board):
        self.need_reinforcement = True
        self.is_autobot = True
        self.initial_board = cp.deepcopy(board)

    def initialize_simulation(self, nb_training_loop):
        print('prepare IA with ', nb_training_loop, ' trains')
        self.me = PlayerPawn.P1

        games = []
        print("Start simulation of %s" % (nb_training_loop))
        for i in range(0, nb_training_loop):
            games.append(self.simulateGame())
            done = int(100 * i / nb_training_loop)
            sys.stdout.write("\r[%s%s] %s/%s" % ('=' * done, ' ' * (100-done), i, nb_training_loop)) 
            sys.stdout.flush()

        print('', end = "\r\n")
        print('Simulation completed')
      
        self.model = self.getModel()
        X_train, X_test, y_train, y_test = self.gamesToWinLossData(games)
        history = self.model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=50, batch_size=64)

        print(self.model.summary())


    def getModel(self):
        outcomes = 3 # draw, X-wins, O-wins
        model = Sequential()
        model.add(Dense(200, activation='relu', input_shape=(9, )))
        model.add(Dropout(0.2))
        model.add(Dense(125, activation='relu'))
        model.add(Dense(75, activation='relu'))
        model.add(Dropout(0.1))
        model.add(Dense(25, activation='relu'))
        model.add(Dense(outcomes, activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['acc'])
        return model

