from training.evaluate import evaluate


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, help="Path to model")
    parser.add_argument("--episodes", type=int, default=5)
    args = parser.parse_args()
    print(evaluate(args.model, args.episodes))
