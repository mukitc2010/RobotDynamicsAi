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
