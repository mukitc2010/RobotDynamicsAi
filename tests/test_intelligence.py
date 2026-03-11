from core.intelligence.engine import IntelligenceEngine
from frontend.app import app


def test_intelligence_engine_walk_plan():
    engine = IntelligenceEngine()
    state = {
        "planning_status": "done",
        "development_status": "training_completed",
        "testing_status": "done",
        "artifacts": ["model_g1.zip"],
        "robot_spec": {"model": "G1", "total_dof": 23},
    }

    result = engine.propose("walk forward safely", state)
    assert result["safe_command"]["type"] == "set_walk_velocity"
    assert result["safe_command"]["params"]["vx"] <= 0.8
    assert result["confidence"] > 0.5


def test_intelligence_api_endpoints():
    client = app.test_client()

    status = client.get("/api/intelligence/status")
    assert status.status_code == 200

    plan = client.post("/api/intelligence/plan", json={"goal": "turn waist left"})
    assert plan.status_code == 200
    data = plan.get_json()
    assert "safe_command" in data

    feedback = client.post(
        "/api/intelligence/feedback",
        json={"goal": "turn waist left", "success": True, "notes": "stable"},
    )
    assert feedback.status_code == 200

    memory = client.get("/api/intelligence/memory?limit=5")
    assert memory.status_code == 200
    assert "events" in memory.get_json()
