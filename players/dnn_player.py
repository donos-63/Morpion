import os

from players.base_player import base_player
import sys
import random
from tensorflow.python.keras import Sequential, models
from tensorflow.python.keras.layers import Dense, Dropout
from tensorflow.python.keras.utils import to_categorical 
import numpy as np
from player import Player, PlayerPawn
import copy as cp
import players.random_player as rplay
from board import Board
import players.min_max_player as mmplay

class DnnPlayer(base_player):

    MODEL_FILEPATH = os.path.join(base_player.MODELS_FOLDER,'cnn.model')

    # Get best next move for the given player at the given board position
    def play_move(self, player, board):
        '''
            Compute move using cnn
        '''
        scores = []
        
        moves = Board.get_available_moves(board)
        player = Player.player_to_numerical(player)
            
        # Make predictions for each possible move
        for x,y in Board.get_available_moves(board):
            board_numerical = Board.board_to_numercial(board)
            board_with_new_move = np.array(board_numerical)
            board_with_new_move[y,x] = player

            prediction = self.model.predict(board_with_new_move.reshape((-1, 9)))[0]

            win_prediction = prediction[1]
            loss_prediction = prediction[2]
            draw_prediction = prediction[0]

            #give priority to the most offensive result
            #commentaire fr : pas trouvé la solution parfaite pour exploiter le résultat du cnn
            if win_prediction - loss_prediction > 0:
                scores.append(win_prediction - loss_prediction)
            else:
                scores.append(draw_prediction - loss_prediction)

        best_moves = np.flip(np.argsort(scores))
        x = int(moves[best_moves[0]][0])
        y = int(moves[best_moves[0]][1])
        return x, y

    # Simulate a game
    def simulate_game(self):
        '''
            Simulate a game between 2 bots randoms
        '''
        good_trainer = mmplay.MinMaxPlayer() #finally, random vs minmax always loose, cannot build a model from only 2d shape
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
    

    def moves_to_board(self, moves, convert_to_numerical = False):
        '''
            Reconstruct the board from the move list
        '''
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

    def games_to_win_loss_data(self, games):
        '''
            from list of games history, create train and test datasets
        '''
        X = []
        y = []
        for game in games:
            winner = Board.get_winner(self.moves_to_board(game))
            for move in range(len(game)):
                X.append(self.moves_to_board(game[:(move + 1)], True))
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
        '''
            Train cnn from random bots then instanciate model
        '''
        print('prepare IA with ', nb_training_loop, ' trains')
        self.me = PlayerPawn.P1

        games = []
        x_wins, o_wins, draws = 0, 0, 0
        print("Start simulation of %s" % (nb_training_loop))
        for i in range(0, nb_training_loop):
            game = self.simulate_game()
            games.append(game)
            winner = Board.get_winner(self.moves_to_board(game))
            winner = Player.player_from_numerical(winner)
            if winner == PlayerPawn.P1.value:
                x_wins += 1
            elif winner == PlayerPawn.P2.value:
                o_wins += 1
            else : 
                draws += 1

            done = int(100 * i / nb_training_loop)
            sys.stdout.write("\r[%s%s] %s/%s" % ('=' * done, ' ' * (100-done), i, nb_training_loop)) 
            sys.stdout.flush()

        print('', end = "\r\n")
        print('Simulation completed')
        print('X wins:{} - O wins:{} - Draws:{}'.format(x_wins, o_wins, draws))
              
        X_train, X_test, y_train, y_test = self.games_to_win_loss_data(games)
        self.model = self.get_model()
        history = self.model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=50, batch_size=64)

        self.model.save(DnnPlayer.MODEL_FILEPATH, save_format='h5')
        print(self.model.summary())
        self.print_model_history(history)

    def is_reinforcement_exists(self):
        '''
            check if reinforcement model exists
        '''
        return os.path.exists(DnnPlayer.MODEL_FILEPATH)

    def load_simulation(self):
        '''
            load model
        '''
        self.model = models.load_model(DnnPlayer.MODEL_FILEPATH)

    def get_model(self):
        outcomes = 3 # draw, X-wins, O-wins
        #pas d'analyse du modèle fait, pas compris comment faire
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

