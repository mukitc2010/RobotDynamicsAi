import numpy as np
from envs.reward import compute_reward


def test_reward_basic():
    obs = np.zeros(20)
    action = np.zeros(17)
    r = compute_reward(obs, action)
    assert isinstance(r, float)
