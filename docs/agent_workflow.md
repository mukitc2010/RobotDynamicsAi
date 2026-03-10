# Agent Workflow

1. **PlanningAgent** reads requirements and populates tasks, milestones, and
   acceptance criteria.
2. **DevelopmentAgent** initializes the simulation environment and starts the
   PPO training pipeline, producing models and logs.
3. **TestingAgent** evaluates the trained policy against predefined metrics.
4. **DeliveryAgent** compiles documentation, release notes, and final reports.

Each agent updates the shared `ProjectState` which is passed by the
`Orchestrator`. This creates a linear lifecycle mirroring a robotics project.
