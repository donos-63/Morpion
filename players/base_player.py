import os
import matplotlib.pyplot as plt


class base_player():

    MODELS_FOLDER = os.path.join(os.getcwd(),"models" )

    def initialize_simulation(self, _):
        raise Exception('base_player.initialize_simulation', 'not implemented')

    def play_move(self, player, board):
        raise Exception('base_player.play_move', 'not implemented')

    def load_simulation():
        raise Exception('base_player.load_simulation', 'not implemented')

    def is_reinforcement_exists():
        raise Exception('base_player.is_reinforcement_exists', 'not implemented')

    def print_model_history(self, history):
        '''
            print model training history
        '''
        # list all data in history
        print(history.history.keys())
        # summarize history for accuracy
        plt.plot(history.history['acc'])
        plt.plot(history.history['val_acc'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()
        # summarize history for loss
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()