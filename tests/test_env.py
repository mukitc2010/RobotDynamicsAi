import gymnasium as gym
from envs.humanoid_env import make_env


def test_env_creation():
    env = make_env()
    assert hasattr(env, "step")
    assert hasattr(env, "reset")
    env.close()
