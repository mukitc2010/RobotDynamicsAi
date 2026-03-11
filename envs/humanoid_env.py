import gymnasium as gym
from envs.wrappers import RewardWrapper
import yaml


def make_env(spec: dict = None):
    """Return a wrapped environment.

    When provided a robot specification, attempt to configure a custom
    MuJoCo model.  For now the function logs the incoming spec and falls back
    to the standard `Humanoid-v4` environment.  This stub can later be
    replaced with real mjcf generation or file loading logic.

    Args:
        spec: dictionary describing robot characteristics (DOF, sensors, etc.)

    Returns:
        An environment instance wrapped with `RewardWrapper`.
    """

    if spec:
        model_name = spec.get("model", "G1")
        dof = spec.get("total_dof")
        # placeholder logic - real environment would use these values
        print(f"[env] Creating environment for {model_name} ({dof} DOF)")
        env_id = "Humanoid-v4"
    else:
        env_id = "Humanoid-v4"

    env = gym.make(env_id)
    env = RewardWrapper(env)
    return env
