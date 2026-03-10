import gymnasium as gym
from envs.wrappers import RewardWrapper


def make_env():
    env = gym.make("Humanoid-v4")
    env = RewardWrapper(env)
    return env
