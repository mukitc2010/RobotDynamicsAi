from flask import Flask, render_template, jsonify, redirect, url_for
import json
import subprocess
import threading
import os

app = Flask(__name__)

STATE_FILE = os.path.join(os.path.dirname(__file__), "..", "artifacts", "state.json")


def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


@app.route("/")
def index():
    state = load_state()
    return render_template("index.html", state=state)


@app.route("/run_pipeline")
def run_pipeline():
    # run asynchronously
    def run():
        os.chdir(os.path.join(os.path.dirname(__file__), ".."))
        subprocess.run(["python3", "scripts/run_pipeline.py"])
    threading.Thread(target=run).start()
    return redirect(url_for("index"))


@app.route("/state.json")
def state_json():
    return jsonify(load_state())


if __name__ == "__main__":
    app.run(debug=True)
