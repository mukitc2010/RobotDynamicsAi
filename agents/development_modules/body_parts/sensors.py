from typing import Any, Dict


def build_sensors_module(spec: Dict[str, Any]) -> Dict[str, Any]:
    """Return implementation details for perception and state observations."""
    return {
        "name": "sensors",
        "purpose": "Observation pipeline for state estimation and QA metrics.",
        "robot_spec_used": {
            "perception": spec.get("sensors", "Depth camera + 3D LiDAR"),
            "encoders": spec.get("joint_encoders", "Dual encoders"),
        },
        "code_modules": [
            "envs/humanoid_env.py::make_env",
            "training/evaluate.py::evaluate",
            "agents/testing_agent.py::run",
        ],
        "functionality": [
            "Defines observable state channels for RL training/evaluation.",
            "Feeds telemetry into QA metrics like stability and reward.",
            "Keeps interfaces ready for future real sensor adapters.",
        ],
    }
