from gymnasium import Env
from gymnasium.core import ActType, ObsType

from envs.reward import compute_reward


class RewardWrapper(Env):
    def __init__(self, env: Env):
        self.env = env
        self.action_space = env.action_space
        self.observation_space = env.observation_space

    def step(self, action: ActType) -> tuple[ObsType, float, bool, bool, dict]:
        obs, reward, terminated, truncated, info = self.env.step(action)
        custom_reward = compute_reward(obs, action)
        return obs, custom_reward, terminated, truncated, info

    def reset(self, **kwargs):
        return self.env.reset(**kwargs)

    def render(self, mode="human"):
        return self.env.render(mode)

    def close(self):
        return self.env.close()
