from typing import Any, Dict, List
import yaml
from agents.base_agent import BaseAgent


class PlanningAgent(BaseAgent):
    """Robotics Product Manager: understands robot specs, generates requirements, and distributes work."""

    def run(self) -> Dict[str, Any]:
        # Load project config
        with open("configs/project.yaml") as f:
            project = yaml.safe_load(f)

        robot_spec = project.get("robot_spec", {})
        base_requirement = project.get("requirement", "")

        self.log(f"Processing robot spec for {robot_spec.get('model', 'Unknown')}")

        # Generate detailed requirements based on spec
        requirements = self._generate_requirements(robot_spec, base_requirement)

        # Break into tasks
        tasks = self._generate_tasks(robot_spec, requirements)

        milestones = [
            "Environment Setup",
            "Reward and Training Pipeline",
            "Training Execution",
            "Testing and Evaluation",
            "Documentation and Delivery"
        ]

        acceptance_criteria = [
            "G1 simulation environment initialized",
            "PPO training completes successfully",
            "Metrics meet walking stability thresholds",
            "All tests pass",
            "Documentation and reports generated"
        ]

        # Distribute work to agents
        assignments = {
            "development": [
                "Set up Gymnasium/MuJoCo environment for G1 with 23 DOF",
                "Implement custom reward function for bipedal walking",
                "Configure PPO training pipeline with Stable-Baselines3",
                "Integrate sensor data (depth camera, LiDAR) into state space",
                "Set up battery life and power constraints in simulation"
            ],
            "testing": [
                "Validate environment initialization and joint configurations",
                "Test reward function outputs for walking behaviors",
                "Evaluate trained policy on stability, distance, fall rate",
                "Run unit tests for training scripts and evaluation",
                "Measure performance against G1 specs (torque, payload)"
            ],
            "delivery": [
                "Generate technical reports on training results",
                "Update README with G1-specific instructions",
                "Create release notes for trained model",
                "Document architecture and agent workflow",
                "Prepare artifacts for deployment"
            ]
        }

        planning_documents = {
            "strategy": "docs/planning_strategy.md",
            "requirements": "docs/requirements_document.md",
            "process": "docs/planning_process.md",
        }

        self.state.update(
            {
                "robot_spec": robot_spec,
                "requirements": requirements,
                "tasks": tasks,
                "milestones": milestones,
                "acceptance_criteria": acceptance_criteria,
                "assignments": assignments,
                "planning_documents": planning_documents,
                "planning_status": "done",
            }
        )
        return self.state

    def _generate_requirements(self, spec: Dict[str, Any], base: str) -> List[str]:
        """Generate detailed requirements from robot spec."""
        reqs = [base]
        if spec.get("total_dof"):
            reqs.append(f"Handle {spec['total_dof']} degrees of freedom in simulation")
        if spec.get("max_torque_knee"):
            reqs.append(f"Respect joint torque limits (knee: {spec['max_torque_knee']})")
        if spec.get("sensors"):
            reqs.append(f"Integrate sensor inputs: {spec['sensors']}")
        if spec.get("battery_life"):
            reqs.append(f"Simulate battery constraints: {spec['battery_life']}")
        return reqs

    def _generate_tasks(self, spec: Dict[str, Any], requirements: List[str]) -> List[str]:
        """Break requirements into actionable tasks."""
        tasks = []
        for req in requirements:
            if "walk" in req.lower():
                tasks.extend([
                    "Implement bipedal walking reward shaping",
                    "Configure PPO for locomotion optimization",
                    "Set up evaluation metrics for walking stability"
                ])
            if "dof" in req.lower():
                tasks.append("Map G1 joint configurations to MuJoCo model")
            if "torque" in req.lower():
                tasks.append("Enforce joint torque constraints in environment")
            if "sensor" in req.lower():
                tasks.append("Incorporate sensor data into observation space")
            if "battery" in req.lower():
                tasks.append("Model battery depletion in training episodes")
        return tasks
