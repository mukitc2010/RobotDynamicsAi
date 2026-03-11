import pytest
from core.orchestrator import Orchestrator


def test_orchestrator_runs():
    orch = Orchestrator({"requirement": "walk"})
    state = orch.run()
    assert state.get("planning_status") == "done"
    assert state.get("development_status") == "training_completed"
    assert state.get("testing_status") == "done"
    assert state.get("delivery_status") == "done"


def test_development_agent_with_spec():
    # ensure development agent initializes environment and artifacts
    initial = {"robot_spec": {"model": "G1", "total_dof": 23}}
    from agents.development_agent import DevelopmentAgent

    agent = DevelopmentAgent(initial)
    state = agent.run()
    assert state.get("environment_initialized") is True
    assert "model_g1.zip" in state.get("artifacts", [])
    assert state.get("development_status") == "training_completed"
