# Robolog AI Lab

A professional multi-agent robotics AI platform for training humanoid
locomotion using reinforcement learning. The system simulates a robotic
engineering company with distinct agents for planning, development, testing,
and delivery.

## Overview

- **Project Name:** robolog.us
- **Repository:** robolog-ai-lab
- **Vision:** Collaborative agents design, implement, and deliver robot
  locomotion pipelines using Gymnasium, MuJoCo, and Stable-Baselines3.

## Architecture
See `docs/architecture.md` for a detailed description.

## Agent Roles
- **PlanningAgent:** Defines tasks and milestones from requirements and distributes work among the other agents (development, testing, delivery).
- **DevelopmentAgent:** Sets up environment and runs PPO training.
- **TestingAgent:** Evaluates trained policies and records metrics.
- **DeliveryAgent:** Generates documentation and release reports.

## Installation

```bash
git clone <repo-url>
cd robolog-ai-lab
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Training

```bash
python scripts/run_training.py
```

Configuration is stored in `configs/training.yaml`.

## Evaluation

```bash
python scripts/run_evaluation.py --model artifacts/model.zip --episodes 5
```

## Running the full pipeline

```bash
python scripts/run_pipeline.py
```

## Dashboard

A simple Flask-based front end is available under `frontend/`:

```bash
cd frontend
pip install flask
python app.py
```

Visit http://localhost:5000 to view the project state and start the pipeline.

## Testing

```bash
pytest -q
```

## Future Roadmap
1. Integrate real MuJoCo assets and reward functions.
2. Expand PlanningAgent to read natural language requirements.
3. Add CI for model validation and artifact versioning.
4. Deploy orchestration to cloud with containerized agents.
