# Planning Process - Robotic Framework Build

Owner: PlanningAgent

## Process Overview
PlanningAgent runs at the start of every pipeline cycle and drives the implementation plan for the robotics framework.

## Step-by-Step Planning Flow
1. Collect inputs
- Read product requirement from project config/state.
- Read robot constraints (G1 specs when available).

2. Generate requirements
- Translate high-level goal into explicit technical requirements.
- Capture constraints for locomotion, stability, and evaluation.

3. Build task breakdown
- Convert requirements into actionable implementation tasks.
- Group tasks by delivery stream: development, testing, delivery.

4. Define milestones
- Environment setup
- Reward and training pipeline
- Training execution
- Testing and evaluation
- Documentation and delivery

5. Define acceptance criteria
- Set completion conditions for each milestone.
- Ensure criteria are measurable and testable.

6. Assign work to agents
- DevelopmentAgent: environment, training, artifact generation.
- TestingAgent: validation and metrics.
- DeliveryAgent: reports and release documentation.

7. Publish planning outputs
- Write tasks, milestones, acceptance criteria, and assignments into shared state.
- Handoff to DevelopmentAgent through orchestrator sequence.

## Framework Build Mapping
- Planning outputs drive `agents/development_agent.py` and body-part module planning docs.
- Testing criteria drive `agents/testing_agent.py` metrics and test coverage.
- Delivery goals drive report/document generation.

## Review Cadence
Per iteration:
- Recheck requirement changes.
- Reprioritize tasks from latest metrics.
- Update acceptance criteria before next run.
