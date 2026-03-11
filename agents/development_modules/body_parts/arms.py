from typing import Any, Dict


def build_arms_module(spec: Dict[str, Any]) -> Dict[str, Any]:
    """Return implementation details for upper-limb task control."""
    dof = spec.get("dof_per_arm", 5)

    return {
        "name": "arms",
        "purpose": "Arm positioning and balance-assist posture targets.",
        "robot_spec_used": {
            "dof_per_arm": dof,
            "arm_span": spec.get("arm_span", "0.45m"),
            "payload_limit": spec.get("max_payload_arm", "Approx. 2kg"),
        },
        "code_modules": [
            "agents/development_agent.py::run",
            "training/evaluate.py::evaluate",
        ],
        "functionality": [
            "Defines arm control constraints for safe posture envelopes.",
            "Supports future balancing policies where arms reduce torso oscillation.",
            "Includes hooks for arm evaluation during trained policy rollouts.",
        ],
    }
