from gym.envs.registration import register

register(
    id='game-2048-v0',
    entry_point='gym_2048.envs:Game2048',
)
