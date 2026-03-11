from typing import Any, Dict


def build_legs_module(spec: Dict[str, Any]) -> Dict[str, Any]:
    """Return implementation details for lower-body locomotion control."""
    dof = spec.get("dof_per_leg", 6)
    leg_length = spec.get("leg_length", "0.6m")

    return {
        "name": "legs",
        "purpose": "Bipedal locomotion and stability control.",
        "robot_spec_used": {
            "dof_per_leg": dof,
            "leg_length": leg_length,
            "knee_torque_limit": spec.get("max_torque_knee", "90N.m"),
        },
        "code_modules": [
            "envs/reward.py::compute_reward",
            "envs/humanoid_env.py::make_env",
            "training/train_ppo.py::main",
        ],
        "functionality": [
            "Shapes reward to favor forward velocity and lower energy waste.",
            "Trains PPO policy for gait and balance behavior.",
            "Uses evaluation metrics for distance, reward, and fall-rate checks.",
        ],
    }
