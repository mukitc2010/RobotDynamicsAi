import yaml
from stable_baselines3 import PPO
from envs.humanoid_env import make_env


def load_config(path="configs/training.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def evaluate(model_path: str, episodes: int = 5):
    cfg = load_config()
    env = make_env()
    model = PPO.load(model_path, env=env)
    results = []
    for _ in range(episodes):
        obs, _ = env.reset()
        done = False
        total_reward = 0
        while not done:
            action, _ = model.predict(obs)
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            total_reward += reward
        results.append(total_reward)
    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--episodes", type=int, default=5)
    args = parser.parse_args()
    print(evaluate(args.model, args.episodes))
