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

DevelopmentAgent body-part implementation reference:
- `docs/development_body_parts.md`

PlanningAgent documentation:
- `docs/planning_strategy.md`
- `docs/requirements_document.md`
- `docs/planning_process.md`

## Agent Roles
- **PlanningAgent:** Defines tasks and milestones from requirements and distributes work among the other agents (development, testing, delivery).
- **DevelopmentAgent:** Sets up environment and runs PPO training.
  It now reads the robot specification (G1) and initializes a custom
  MuJoCo environment before simulating training.
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

### Notes
The environment initialization step prints output such as
`[env] Creating environment for G1 (23 DOF)` when a robot spec is provided.

## Testing

```bash
pytest -q
```

## Future Roadmap
1. Integrate real MuJoCo assets and reward functions.
2. Expand PlanningAgent to read natural language requirements.
3. Add CI for model validation and artifact versioning.
4. Deploy orchestration to cloud with containerized agents.

## Intelligence Engine

The project now includes a high-level robot intelligence layer under
`core/intelligence/` with:

- `WorldModel`: summarizes readiness and robot context from state.
- `TaskPlanner`: converts natural-language goals into a multi-step plan.
- `SkillRouter`: maps goals to executable robot commands.
- `SafetyGovernor`: clamps commands to safe limits.
- `MemoryStore`: stores decision and feedback events.

### Intelligence API

Available from the Flask dashboard server:

- `GET /api/intelligence/status`
- `POST /api/intelligence/plan`
- `POST /api/intelligence/feedback`
- `GET /api/intelligence/memory`

Example plan request:

```bash
curl -X POST http://127.0.0.1:5000/api/intelligence/plan \
  -H "Content-Type: application/json" \
  -d '{"goal":"walk forward safely"}'
```
