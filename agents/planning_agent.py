from typing import Any, Dict, List

from agents.base_agent import BaseAgent


class PlanningAgent(BaseAgent):
    """Robotics Product Manager responsible for breaking requirements into tasks."""

    def run(self) -> Dict[str, Any]:
        requirement = self.state.get("requirement", "")
        self.log(f"Processing requirement: {requirement}")

        # simple placeholder logic to split into tasks
        tasks = [f"Implement {part.strip()}" for part in requirement.split(",") if part.strip()]
        milestones = ["milestone1", "milestone2"]
        acceptance = ["Tasks complete", "Tests passing"]

        # simple assignment of work categories to downstream agents
        assignments = {
            "development": [t for t in tasks],
            "testing": ["verify environment", "evaluate policy"],
            "delivery": ["write docs", "prepare release notes"],
        }

        self.state.update(
            {
                "tasks": tasks,
                "milestones": milestones,
                "acceptance_criteria": acceptance,
                "assignments": assignments,
                "planning_status": "done",
            }
        )
        return self.state
