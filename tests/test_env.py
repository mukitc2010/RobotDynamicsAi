import gymnasium as gym
from envs.humanoid_env import make_env


def test_env_creation():
    # default environment
    env = make_env()
    assert hasattr(env, "step")
    assert hasattr(env, "reset")
    env.close()

    # environment with a robot spec should also initialize
    spec = {"model": "G1", "total_dof": 23}
    env2 = make_env(spec)
    assert hasattr(env2, "step")
    env2.close()
