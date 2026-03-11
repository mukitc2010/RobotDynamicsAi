from typing import Any

from core.intelligence.memory import MemoryStore
from core.intelligence.planner import TaskPlanner
from core.intelligence.safety_governor import SafetyGovernor
from core.intelligence.skill_router import SkillRouter
from core.intelligence.world_model import WorldModel


class IntelligenceEngine:
    """High-level decision engine combining planning, skills, memory, and safety."""

    def __init__(self):
        self.world_model = WorldModel()
        self.planner = TaskPlanner()
        self.skill_router = SkillRouter()
        self.safety = SafetyGovernor()
        self.memory = MemoryStore()

    def propose(self, goal: str, state: dict[str, Any]) -> dict[str, Any]:
        world = self.world_model.build(state)
        steps = self.planner.plan(goal, world)
        raw_command = self.skill_router.select_command(goal, steps)
        safe_command = self.safety.guard(raw_command)

        confidence = self._confidence(world)

        result = {
            "goal": goal,
            "world": world,
            "plan": steps,
            "raw_command": raw_command,
            "safe_command": safe_command,
            "confidence": confidence,
            "reasoning": self._reasoning(goal, world, safe_command),
            "recent_memory": self.memory.recent(5),
        }
        self.memory.add_event("decision", {"goal": goal, "command": safe_command, "confidence": confidence})
        return result

    def feedback(self, goal: str, success: bool, notes: str = "") -> dict[str, Any]:
        payload = {"goal": goal, "success": bool(success), "notes": notes}
        self.memory.add_event("feedback", payload)
        return payload

    def _confidence(self, world: dict[str, Any]) -> float:
        score = 0.35
        if world.get("planning_ok"):
            score += 0.2
        if world.get("development_ok"):
            score += 0.2
        if world.get("testing_ok"):
            score += 0.15
        if world.get("has_artifacts"):
            score += 0.1

        recent_failures = self.memory.recent_failures(20)
        score -= min(0.25, recent_failures * 0.05)

        return round(max(0.0, min(1.0, score)), 3)

    def _reasoning(self, goal: str, world: dict[str, Any], command: dict[str, Any]) -> str:
        if not world.get("ready"):
            return "System is not fully ready; generated conservative command for safety."
        return f"Goal '{goal}' mapped to skill '{command.get('skill')}' with safety constraints applied."
