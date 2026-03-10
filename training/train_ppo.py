import yaml
from stable_baselines3 import PPO
from envs.humanoid_env import make_env


def load_config(path="configs/training.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def main():
    cfg = load_config()
    env = make_env()
    model = PPO(cfg["policy"], env, verbose=1)
    model.learn(total_timesteps=cfg["total_timesteps"])
    model.save(cfg["save_path"])


if __name__ == "__main__":
    main()
