from typing import Any


class TaskPlanner:
    """Creates a simple hierarchical plan from a natural-language goal."""

    def plan(self, goal: str, world: dict[str, Any]) -> list[dict[str, Any]]:
        goal_l = (goal or "").lower()
        steps: list[dict[str, Any]] = [
            {"name": "Check safety and readiness", "skill": "safety_check"},
        ]

        if "walk" in goal_l or "move" in goal_l or "navigate" in goal_l:
            steps.extend(
                [
                    {"name": "Stabilize base pose", "skill": "stand"},
                    {"name": "Execute locomotion command", "skill": "walk"},
                    {"name": "Evaluate gait stability", "skill": "evaluate"},
                ]
            )
        elif "arm" in goal_l or "grasp" in goal_l or "pick" in goal_l:
            steps.extend(
                [
                    {"name": "Move to pre-grasp posture", "skill": "arm_pose"},
                    {"name": "Apply controlled arm movement", "skill": "arm_pose"},
                    {"name": "Evaluate manipulation stability", "skill": "evaluate"},
                ]
            )
        elif "turn" in goal_l or "waist" in goal_l:
            steps.extend(
                [
                    {"name": "Stabilize base pose", "skill": "stand"},
                    {"name": "Rotate torso", "skill": "waist_angle"},
                    {"name": "Evaluate orientation stability", "skill": "evaluate"},
                ]
            )
        else:
            steps.extend(
                [
                    {"name": "Move to safe stand", "skill": "stand"},
                    {"name": "Run diagnostics", "skill": "evaluate"},
                ]
            )

        if not world.get("validated"):
            steps.append({"name": "Flag low validation confidence", "skill": "report"})

        return steps
