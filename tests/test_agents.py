import pytest
from core.orchestrator import Orchestrator


def test_orchestrator_runs():
    orch = Orchestrator({"requirement": "walk"})
    state = orch.run()
    assert state.get("planning_status") == "done"
    assert state.get("development_status") == "training_completed"
    assert state.get("testing_status") == "done"
    assert state.get("delivery_status") == "done"
