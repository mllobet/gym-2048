import gym
import sys
from gym import error, spaces, utils, Space, spaces
from gym.utils import seeding
from gym_2048.engine import Engine

import random
import six
import numpy as np

class Game2048(gym.Env):
    metadata = {'render.modes': ['human']}

    def flatten(self, l):
        return [item for sublist in l for item in sublist]

    def __init__(self, seed=None):
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Discrete(12*4*4)
        self.reward_range = (0,np.inf)
        self._seed = seed
        self.env = Engine(seed=seed)
        self.env.reset_game()

    def _step(self, action):
        assert self.action_space.contains(action)

        reward, ended = self.env.move(action)
        return self.env.get_board(), reward, ended, {'score': self.env.score, 'won': self.env.won}

    def _reset(self):
        self.env.reset_game()
        return self.env.get_board()

    def _render(self, mode='human', close=False):
        outfile = StringIO() if mode == 'ansi' else sys.stdout
        outfile.write(str(self.env))

    def moves_available(self):
        return self.env.moves_available()
