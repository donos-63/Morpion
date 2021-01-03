from paddle import Paddle
from DQN_agent import DQN

import matplotlib.pyplot as plt
import numpy as np

env = Paddle()
np.random.seed(0)

def train_dqn(episode):
    
    loss = []

    action_space = 3
    state_space = 5
    max_steps = 1000

    agent = DQN(action_space, state_space)
    for e in range(episode):
        state = env.reset()
        state = np.reshape(state, (1, state_space))
        score = 0
        for i in range(max_steps):
            action = agent.act(state)
            reward, next_state, done = env.step(action)
            score += reward
            next_state = np.reshape(next_state, (1, state_space))
            agent.remember(state, action, reward, next_state, done)
            
            state = next_state
            agent.replay()
            if done:
                print("episode: {}/{}, score: {}".format(e, episode, score))
                break
        loss.append(score)
    return loss


if __name__ == '__main__':

    ep = 2
    loss = train_dqn(ep)
    print(loss)
    plt.plot([i for i in range(ep)], loss)
    plt.xlabel('episodes')
    plt.ylabel('reward')
    plt.show()
