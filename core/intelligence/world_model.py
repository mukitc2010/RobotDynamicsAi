from typing import Any


class WorldModel:
    """Extracts a compact world-state summary for high-level planning."""

    def build(self, state: dict[str, Any]) -> dict[str, Any]:
        planning_ok = state.get("planning_status") == "done"
        dev_ok = state.get("development_status") == "training_completed"
        test_ok = state.get("testing_status") == "done"

        metrics = state.get("metrics", {})
        robot_spec = state.get("robot_spec", {})

        return {
            "ready": planning_ok and dev_ok,
            "validated": test_ok,
            "planning_ok": planning_ok,
            "development_ok": dev_ok,
            "testing_ok": test_ok,
            "robot_model": robot_spec.get("model", "unknown"),
            "total_dof": robot_spec.get("total_dof", 0),
            "distance_traveled": metrics.get("distance_traveled", 0.0),
            "stability_score": metrics.get("stability_score", 0.0),
            "fall_rate": metrics.get("fall_rate", 0.0),
            "has_artifacts": bool(state.get("artifacts")),
        }
