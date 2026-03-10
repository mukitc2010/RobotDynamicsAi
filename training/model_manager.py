from stable_baselines3 import PPO


def save_model(model: PPO, path: str) -> None:
    model.save(path)


def load_model(path: str, env=None) -> PPO:
    return PPO.load(path, env=env)
