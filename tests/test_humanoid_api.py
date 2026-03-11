from frontend.app import app


def test_humanoid_functions_list_and_execute():
    c = app.test_client()

    funcs = c.get("/api/humanoid/functions")
    assert funcs.status_code == 200
    payload = funcs.get_json()
    assert "walk" in payload["functions"]

    execute = c.post(
        "/api/humanoid/functions/walk/execute",
        json={"params": {"vx": 5.0, "vy": 2.0, "wz": 5.0}},
    )
    assert execute.status_code == 200
    result = execute.get_json()
    assert result["accepted"] is True
    assert result["params"]["vx"] == 0.8
    assert result["params"]["vy"] == 0.5
    assert result["params"]["wz"] == 1.2


def test_humanoid_program_create_and_run():
    c = app.test_client()

    create = c.post(
        "/api/humanoid/programs",
        json={
            "name": "walk_and_turn",
            "steps": [
                {"function": "stand", "params": {}},
                {"function": "walk", "params": {"vx": 0.4, "vy": 0.0, "wz": 0.0}},
                {"function": "turn", "params": {"angle_deg": 30}},
            ],
        },
    )
    assert create.status_code == 201
    program = create.get_json()

    run = c.post(f"/api/humanoid/programs/{program['id']}/run")
    assert run.status_code == 200
    run_payload = run.get_json()
    assert run_payload["executed_steps"] == 3
