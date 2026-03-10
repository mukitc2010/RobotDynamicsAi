# Robolog.ai Architecture

The system is organized into agents, core orchestration, environment wrappers,
training pipelines, and supporting scripts. Agents correspond to roles in a
robotics engineering team. The orchestrator runs agents in sequence, passing a
shared project state object.

- **agents/**: contains planning, development, testing, delivery classes.
- **core/**: state management, task models, logger, and orchestrator.
- **envs/**: gymnasium environment loader, reward logic, wrappers.
- **training/**: training and evaluation scripts for PPO using Stable-Baselines3.
- **scripts/**: utility entry points for running the pipeline, training, evaluation,
  and report generation.
- **configs/**: YAML configuration files for training parameters and project.
