from flask import Flask, render_template, jsonify, redirect, url_for, request
import json
import subprocess
import threading
import os
import sys
import platform
import shutil
from datetime import datetime
from typing import Optional
from copy import deepcopy

app = Flask(__name__)

STATE_FILE = os.path.join(os.path.dirname(__file__), "..", "artifacts", "state.json")
ROOT_DIR = os.path.join(os.path.dirname(__file__), "..")
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from core.intelligence import IntelligenceEngine

AGENTS = [
    {
        "name": "PlanningAgent",
        "role": "Robotics Product Manager",
        "mission": "Define requirements, milestones, and assignment plan.",
        "outputs": "tasks, milestones, acceptance criteria",
    },
    {
        "name": "DevelopmentAgent",
        "role": "Robotics Software Engineer",
        "mission": "Build environment, training pipeline, and artifacts.",
        "outputs": "trained model, logs, experiment artifacts",
    },
    {
        "name": "APIDeveloperAgent",
        "role": "Robotics API Engineer",
        "mission": "Design and maintain humanoid control APIs for functions and programs.",
        "outputs": "function endpoints, program APIs, execution logs",
    },
    {
        "name": "TestingAgent",
        "role": "Robotics QA Engineer",
        "mission": "Validate runtime behavior and evaluation metrics.",
        "outputs": "QA summary, metrics report",
    },
    {
        "name": "DeliveryAgent",
        "role": "DevOps and Documentation Engineer",
        "mission": "Ship release reports, docs, and deployment notes.",
        "outputs": "reports, release artifacts",
    },
]

DOC_PATHS = {
    "strategy": "docs/planning_strategy.md",
    "requirements": "docs/requirements_document.md",
    "process": "docs/planning_process.md",
}

BODY_MODULE_SOURCE_PATHS = {
    "legs": "agents/development_modules/body_parts/legs.py",
    "arms": "agents/development_modules/body_parts/arms.py",
    "waist": "agents/development_modules/body_parts/waist.py",
    "sensors": "agents/development_modules/body_parts/sensors.py",
}

INTELLIGENCE = IntelligenceEngine()

FUNCTION_CATALOG = {
    "stand": {
        "description": "Move robot to stable standing pose.",
        "defaults": {},
    },
    "walk": {
        "description": "Set walk velocity command.",
        "defaults": {"vx": 0.4, "vy": 0.0, "wz": 0.0},
    },
    "stop": {
        "description": "Stop all current motion.",
        "defaults": {},
    },
    "squat": {
        "description": "Run squat motion with target depth from 0 to 1.",
        "defaults": {"depth": 0.6},
    },
    "wave": {
        "description": "Wave selected arm.",
        "defaults": {"arm": "right", "cycles": 3},
    },
    "turn": {
        "description": "Turn torso or heading by target angle.",
        "defaults": {"angle_deg": 25.0},
    },
    "reach": {
        "description": "Reach pose toward target point.",
        "defaults": {"x": 0.45, "y": 0.0, "z": 1.05},
    },
    "set_arm_pose": {
        "description": "Direct arm joint command for both arms.",
        "defaults": {"joints": [0.5, -0.3, 1.0, 0.0, 0.0, 0.3, -0.2, 0.8, 0.0, 0.0]},
    },
    "set_waist_angle": {
        "description": "Set waist yaw angle in degrees.",
        "defaults": {"angle_deg": 20.0},
    },
}

PROGRAM_STORE: dict[str, dict] = {}
PROGRAM_COUNTER = 0


def _doc_exists(rel_path: str) -> bool:
    return os.path.exists(os.path.join(ROOT_DIR, rel_path))


def runtime_health(state: dict) -> dict:
    environment_error = state.get("environment_error")
    npm_path = shutil.which("npm")
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "python_version": platform.python_version(),
        "npm_installed": bool(npm_path),
        "npm_path": npm_path or "not installed",
        "environment_error": environment_error,
        "pipeline_ready": environment_error is None,
    }


def planning_docs(state: dict) -> list[dict]:
    docs = state.get("planning_documents", {})
    ordered = [
        ("Strategy", docs.get("strategy", "docs/planning_strategy.md")),
        ("Requirements", docs.get("requirements", "docs/requirements_document.md")),
        ("Process", docs.get("process", "docs/planning_process.md")),
    ]
    return [
        {
            "name": name,
            "path": path,
            "exists": _doc_exists(path),
        }
        for name, path in ordered
    ]


def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def read_doc(rel_path: str) -> Optional[str]:
    full_path = os.path.join(ROOT_DIR, rel_path)
    if not os.path.exists(full_path):
        return None
    with open(full_path, encoding="utf-8") as f:
        return f.read()


def read_source(rel_path: str) -> Optional[str]:
    full_path = os.path.join(ROOT_DIR, rel_path)
    if not os.path.exists(full_path):
        return None
    with open(full_path, encoding="utf-8") as f:
        return f.read()


def _safe_program_name(raw: str) -> str:
    cleaned = (raw or "").strip()
    return cleaned or "unnamed_program"


def _normalize_function_params(function_name: str, params: dict) -> dict:
    defaults = FUNCTION_CATALOG[function_name]["defaults"]
    out = dict(defaults)
    out.update(params or {})

    if function_name == "walk":
        out["vx"] = max(min(float(out.get("vx", 0.0)), 0.8), -0.8)
        out["vy"] = max(min(float(out.get("vy", 0.0)), 0.5), -0.5)
        out["wz"] = max(min(float(out.get("wz", 0.0)), 1.2), -1.2)
    elif function_name == "squat":
        out["depth"] = max(min(float(out.get("depth", 0.6)), 1.0), 0.0)
    elif function_name == "wave":
        arm = str(out.get("arm", "right")).lower()
        out["arm"] = "left" if arm == "left" else "right"
        out["cycles"] = max(min(int(out.get("cycles", 3)), 20), 1)
    elif function_name in ("turn", "set_waist_angle"):
        out["angle_deg"] = max(min(float(out.get("angle_deg", 0.0)), 45.0), -45.0)
    elif function_name == "set_arm_pose":
        joints = out.get("joints", [])
        if not isinstance(joints, list):
            joints = []
        safe_joints = [max(min(float(v), 2.0), -2.0) for v in joints[:10]]
        if len(safe_joints) < 10:
            safe_joints.extend([0.0] * (10 - len(safe_joints)))
        out["joints"] = safe_joints

    return out


def execute_humanoid_function(function_name: str, params: Optional[dict] = None) -> dict:
    if function_name not in FUNCTION_CATALOG:
        raise ValueError("Unsupported humanoid function")

    safe_params = _normalize_function_params(function_name, params or {})
    result = {
        "accepted": True,
        "function": function_name,
        "params": safe_params,
        "detail": f"{function_name} command prepared",
    }
    INTELLIGENCE.memory.add_event("humanoid_function_exec", result)
    return result


def _next_program_id() -> str:
    global PROGRAM_COUNTER
    PROGRAM_COUNTER += 1
    return f"program-{PROGRAM_COUNTER:04d}"


@app.route("/")
def index():
    state = load_state()
    return render_template(
        "index.html",
        state=state,
        health=runtime_health(state),
        docs=planning_docs(state),
        body_modules=state.get("body_part_modules", []),
        agents=AGENTS,
    )


@app.route("/run_pipeline")
def run_pipeline():
    # run asynchronously
    def run():
        root = os.path.join(os.path.dirname(__file__), "..")
        env = os.environ.copy()
        env["PYTHONPATH"] = env.get("PYTHONPATH", ".")
        subprocess.run(["python3", "scripts/run_pipeline.py"], cwd=root, env=env)
    threading.Thread(target=run).start()
    return redirect(url_for("index"))


@app.route("/api/health")
def api_health():
    state = load_state()
    return jsonify(runtime_health(state))


@app.route("/api/state")
def api_state():
    return jsonify(load_state())


@app.route("/api/agents")
def api_agents():
    return jsonify({"agents": AGENTS})


@app.route("/api/body-modules")
def api_body_modules():
    state = load_state()
    return jsonify({"body_modules": state.get("body_part_modules", [])})


@app.route("/api/body-modules/source/<part_name>")
def api_body_module_source(part_name: str):
    key = part_name.lower()
    if key not in BODY_MODULE_SOURCE_PATHS:
        return jsonify({"error": "Invalid part. Use legs, arms, waist, or sensors."}), 404

    rel_path = BODY_MODULE_SOURCE_PATHS[key]
    source = read_source(rel_path)
    if source is None:
        return jsonify({"part": key, "path": rel_path, "available": False}), 404

    return jsonify({"part": key, "path": rel_path, "available": True, "source": source})


@app.route("/api/planning-docs")
def api_planning_docs():
    state = load_state()
    return jsonify({"documents": planning_docs(state)})


@app.route("/api/planning-docs/<doc_key>")
def api_planning_doc_content(doc_key: str):
    if doc_key not in DOC_PATHS:
        return jsonify({"error": "Invalid document key. Use strategy, requirements, or process."}), 404

    rel_path = DOC_PATHS[doc_key]
    content = read_doc(rel_path)
    if content is None:
        return jsonify({"key": doc_key, "path": rel_path, "available": False}), 404

    return jsonify(
        {
            "key": doc_key,
            "path": rel_path,
            "available": True,
            "content": content,
        }
    )


@app.route("/api/pipeline/run", methods=["POST"])
def api_run_pipeline():
    # Optional simple token guard for local scripting.
    token = request.headers.get("X-Run-Token")
    expected = os.environ.get("ROBOLOG_RUN_TOKEN")
    if expected and token != expected:
        return jsonify({"error": "Unauthorized"}), 401

    def run():
        root = os.path.join(os.path.dirname(__file__), "..")
        env = os.environ.copy()
        env["PYTHONPATH"] = env.get("PYTHONPATH", ".")
        subprocess.run(["python3", "scripts/run_pipeline.py"], cwd=root, env=env)

    threading.Thread(target=run).start()
    return jsonify({"status": "started"})


@app.route("/api/dashboard")
def api_dashboard():
    state = load_state()
    return jsonify(
        {
            "health": runtime_health(state),
            "documents": planning_docs(state),
            "agents": AGENTS,
            "body_modules": state.get("body_part_modules", []),
            "state": state,
        }
    )


@app.route("/api/developer/assignments")
def api_developer_assignments():
    state = load_state()
    assignments = state.get("assignments", {})
    api_tasks = [
        "Create API endpoints for humanoid base functions (stand, walk, turn, stop)",
        "Create API endpoints for manipulation functions (arm pose, reach, wave)",
        "Create API program endpoints for multi-step humanoid routines",
        "Add execution logging and validation for every humanoid function request",
    ]
    return jsonify(
        {
            "developer": "APIDeveloperAgent",
            "development_assignments": assignments.get("development", []),
            "api_assignments": api_tasks,
        }
    )


@app.route("/api/humanoid/functions")
def api_humanoid_functions():
    return jsonify({"functions": FUNCTION_CATALOG})


@app.route("/api/humanoid/functions/<function_name>")
def api_humanoid_function_detail(function_name: str):
    key = function_name.lower()
    if key not in FUNCTION_CATALOG:
        return jsonify({"error": "Unknown humanoid function"}), 404
    return jsonify({"name": key, "meta": FUNCTION_CATALOG[key]})


@app.route("/api/humanoid/functions/<function_name>/execute", methods=["POST"])
def api_humanoid_function_execute(function_name: str):
    key = function_name.lower()
    try:
        payload = request.get_json(silent=True) or {}
        params = payload.get("params", {})
        return jsonify(execute_humanoid_function(key, params))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404


@app.route("/api/humanoid/programs", methods=["GET", "POST"])
def api_humanoid_programs():
    if request.method == "GET":
        return jsonify({"programs": list(PROGRAM_STORE.values())})

    payload = request.get_json(silent=True) or {}
    steps = payload.get("steps", [])
    if not isinstance(steps, list) or not steps:
        return jsonify({"error": "Program requires non-empty steps list"}), 400

    normalized_steps = []
    for idx, step in enumerate(steps):
        if not isinstance(step, dict):
            return jsonify({"error": f"Invalid step at index {idx}"}), 400
        func = str(step.get("function", "")).lower()
        if func not in FUNCTION_CATALOG:
            return jsonify({"error": f"Unknown function in step {idx}: {func}"}), 400
        params = step.get("params", {}) if isinstance(step.get("params", {}), dict) else {}
        normalized_steps.append({"function": func, "params": params})

    program_id = _next_program_id()
    program = {
        "id": program_id,
        "name": _safe_program_name(payload.get("name", "")),
        "steps": normalized_steps,
    }
    PROGRAM_STORE[program_id] = program
    INTELLIGENCE.memory.add_event("humanoid_program_create", {"id": program_id, "name": program["name"]})
    return jsonify(program), 201


@app.route("/api/humanoid/programs/<program_id>")
def api_humanoid_program_detail(program_id: str):
    program = PROGRAM_STORE.get(program_id)
    if not program:
        return jsonify({"error": "Program not found"}), 404
    return jsonify(program)


@app.route("/api/humanoid/programs/<program_id>/run", methods=["POST"])
def api_humanoid_program_run(program_id: str):
    program = PROGRAM_STORE.get(program_id)
    if not program:
        return jsonify({"error": "Program not found"}), 404

    execution_log = []
    for step in program["steps"]:
        result = execute_humanoid_function(step["function"], step.get("params", {}))
        execution_log.append(result)

    out = {
        "program_id": program_id,
        "program_name": program["name"],
        "executed_steps": len(execution_log),
        "results": execution_log,
    }
    INTELLIGENCE.memory.add_event("humanoid_program_run", {"id": program_id, "steps": len(execution_log)})
    return jsonify(out)


@app.route("/api/intelligence/status")
def api_intelligence_status():
    return jsonify(
        {
            "enabled": True,
            "modules": [
                "world_model",
                "planner",
                "skill_router",
                "safety_governor",
                "memory",
            ],
            "memory_events": len(INTELLIGENCE.memory.recent(1000)),
        }
    )


@app.route("/api/intelligence/plan", methods=["POST"])
def api_intelligence_plan():
    payload = request.get_json(silent=True) or {}
    goal = payload.get("goal", "stand safely and run diagnostics")
    context = payload.get("context", {})
    state = load_state()
    if isinstance(context, dict):
        merged_state = dict(state)
        merged_state.update(context)
    else:
        merged_state = state

    decision = INTELLIGENCE.propose(goal, merged_state)
    return jsonify(decision)


@app.route("/api/intelligence/feedback", methods=["POST"])
def api_intelligence_feedback():
    payload = request.get_json(silent=True) or {}
    goal = payload.get("goal", "")
    success = bool(payload.get("success", False))
    notes = payload.get("notes", "")
    event = INTELLIGENCE.feedback(goal, success, notes)
    return jsonify({"saved": True, "event": event})


@app.route("/api/intelligence/memory")
def api_intelligence_memory():
    limit = request.args.get("limit", default=20, type=int)
    return jsonify({"events": INTELLIGENCE.memory.recent(limit)})


@app.route("/state.json")
def state_json():
    return jsonify(load_state())


if __name__ == "__main__":
    app.run(debug=True)
