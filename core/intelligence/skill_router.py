from typing import Any


class SkillRouter:
    """Maps a goal and plan steps to an executable low-level command."""

    def select_command(self, goal: str, steps: list[dict[str, Any]]) -> dict[str, Any]:
        goal_l = (goal or "").lower()

        if "walk" in goal_l or "move" in goal_l or "navigate" in goal_l:
            return {
                "type": "set_walk_velocity",
                "params": {"vx": 0.5, "vy": 0.0, "wz": 0.0},
                "skill": "walk",
            }

        if "arm" in goal_l or "grasp" in goal_l or "pick" in goal_l:
            return {
                "type": "set_arm_pose",
                "params": {"joints": [0.5, -0.5, 1.0, 0.0, 0.0, 0.3, -0.2, 0.8, 0.0, 0.0]},
                "skill": "arm_pose",
            }

        if "turn" in goal_l or "waist" in goal_l:
            return {
                "type": "set_waist_angle",
                "params": {"angle_deg": 25.0},
                "skill": "waist_angle",
            }

        return {
            "type": "stand",
            "params": {},
            "skill": "stand",
        }
