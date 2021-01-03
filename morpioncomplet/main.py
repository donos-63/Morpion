from game import Game
from players.agent import Agent

import matplotlib.pyplot as plt
import numpy as np


def train_IA(nb_episode, env):
    loss = []
    # max_step = 10

    for e in range(nb_episode):
        env.start()
        print("episode: {}/{}, score: {} et {} pour {} et {}".format(e+1, nb_episode, p1.score, p2.score, p1.sign, p2.sign))
        env.reset()

    return loss

if __name__ == '__main__':
    p1 = Agent('O')
    p2 = Agent('X')
    env = Game(p1, p2, verbose = False)
    np.random.seed(0)
    
    nb_episode = 1000

    train_IA(nb_episode, env)
    
    p1.plot(nb_episode)
    p2.plot(nb_episode)