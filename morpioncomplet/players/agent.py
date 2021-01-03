from players.player import Player

import random
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

from keras import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

class Agent(Player):

    def __init__(self, sign, nb_action = 9, nb_etat = 9):
        super().__init__(sign)

        self.action = -1
        # Previous state et state sont utilise pour l'apprentissage

        self.loss = []
        self.score = 0

        self.nb_action = nb_action
        self.nb_etat = nb_etat
        self.epsilon = 1
        self.gamma = .95
        self.batch_size = 64
        self.epsilon_min = .01
        self.epsilon_decay = .995
        self.learning_rate = 0.001
        
        self.memory = deque(maxlen=10000)
        self.model = self.__build_model()
    
    def reset(self, state):
        state = np.reshape(state, (1, self.nb_etat))
        self.previous_state = state
        
        self.loss.append(self.score)
        self.score = 0

    def plot(self, nb_episode):
        plt.plot([i for i in range(nb_episode)], self.loss)
        plt.title(f'Joueur {self.sign}')
        plt.xlabel('episodes')
        plt.ylabel('reward')
        plt.show()

    def play(self, game):
        state = game.get_state(self.sign)
        state = np.reshape(state, (1, self.nb_etat))

        self.previous_state = state

        if np.random.rand() <= self.epsilon:
            self.action = random.randrange(self.nb_action)
        else:
            act_values = self.model.predict(state)
            # self.action = np.argmax(act_values[0])
            
            actions = act_values[0]

            i = 0
            save_actions = actions
            while not game.is_valid_action( Agent.action_to_coord(game, np.argmax(actions)) ):
                actions[np.argmax(actions)] = -10
                if i > 10:
                    print("Boucle infinie, aucune action valide: ", save_actions, actions)
            self.action = np.argmax(actions)

        return Agent.action_to_coord(game, self.action)
        
    def action_to_coord(game, action):
        return (
                int(action/game.BOARD_SIZE), 
                action%game.BOARD_SIZE
            )


    def remember(self, state, reward, done):
        self.score += reward
        state = np.reshape(state, (1, self.nb_etat))

        self.memory.append(
            (self.previous_state, self.action, reward, state, done)
        )

        self.__replay()

    def __replay(self):
        """
            Coeur de l'apprentissage bien que je ne saisisse pas tres bien
        """
    
        if len(self.memory) < self.batch_size:
            return

        minibatch = random.sample(self.memory, self.batch_size)
        states = np.array([i[0] for i in minibatch])
        actions = np.array([i[1] for i in minibatch])
        rewards = np.array([i[2] for i in minibatch])
        next_states = np.array([i[3] for i in minibatch])
        dones = np.array([i[4] for i in minibatch])

        states = np.squeeze(states)
        next_states = np.squeeze(next_states)

        targets = rewards + self.gamma*(np.amax(self.model.predict_on_batch(next_states), axis=1))*(1-dones)
        targets_full = self.model.predict_on_batch(states)

        ind = np.array([i for i in range(self.batch_size)])
        targets_full[[ind], [actions]] = targets

        self.model.fit(states, targets_full, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def __build_model(self):
        model = Sequential()
        model.add(Dense(64, input_shape=(self.nb_etat,), activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(self.nb_action, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

if __name__ == '__main__':
    ia = Agent('O')
