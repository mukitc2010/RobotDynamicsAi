from typing import Any


class SafetyGovernor:
    """Constrains commands into safe operational ranges."""

    def guard(self, command: dict[str, Any]) -> dict[str, Any]:
        cmd = {
            "type": command.get("type"),
            "params": dict(command.get("params", {})),
            "skill": command.get("skill", "unknown"),
        }

        if cmd["type"] == "set_walk_velocity":
            vx = float(cmd["params"].get("vx", 0.0))
            vy = float(cmd["params"].get("vy", 0.0))
            wz = float(cmd["params"].get("wz", 0.0))
            cmd["params"]["vx"] = max(min(vx, 0.8), -0.8)
            cmd["params"]["vy"] = max(min(vy, 0.5), -0.5)
            cmd["params"]["wz"] = max(min(wz, 1.0), -1.0)

        if cmd["type"] == "set_waist_angle":
            angle = float(cmd["params"].get("angle_deg", 0.0))
            cmd["params"]["angle_deg"] = max(min(angle, 45.0), -45.0)

        if cmd["type"] == "set_arm_pose":
            joints = list(cmd["params"].get("joints", []))
            safe_joints = [max(min(float(v), 2.0), -2.0) for v in joints][:10]
            if len(safe_joints) < 10:
                safe_joints.extend([0.0] * (10 - len(safe_joints)))
            cmd["params"]["joints"] = safe_joints

        return cmd
