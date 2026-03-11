from typing import Any, Dict


def build_waist_module(spec: Dict[str, Any]) -> Dict[str, Any]:
    """Return implementation details for torso yaw and core stabilization."""
    return {
        "name": "waist",
        "purpose": "Core orientation control and heading stability.",
        "robot_spec_used": {
            "dof_waist": spec.get("dof_waist", 1),
            "waist_range": spec.get("waist_rom", "Z +-155deg"),
        },
        "code_modules": [
            "envs/wrappers.py::RewardWrapper.step",
            "training/callbacks.py::SaveOnBestTrainingRewardCallback",
        ],
        "functionality": [
            "Tracks torso orientation through wrapped reward computation.",
            "Supports heading-correction behavior in policy optimization.",
            "Logs improved training checkpoints when stability rises.",
        ],
    }
