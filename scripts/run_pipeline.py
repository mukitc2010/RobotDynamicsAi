from core.orchestrator import Orchestrator
import yaml


def load_project(path="configs/project.yaml"):
    with open(path) as f:
        return yaml.safe_load(f)


def main():
    proj = load_project()
    state = {"requirement": proj.get("requirement")}
    orch = Orchestrator(state)
    final_state = orch.run()
    print("Final state:", final_state)


if __name__ == "__main__":
    main()
