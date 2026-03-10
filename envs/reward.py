import numpy as np
from gymnasium import spaces


def compute_reward(obs, action):
    # placeholder reward: encourage forward motion
    vel = obs[17] if len(obs) > 17 else 0.0
    return float(vel) - 0.1 * np.square(action).sum()
