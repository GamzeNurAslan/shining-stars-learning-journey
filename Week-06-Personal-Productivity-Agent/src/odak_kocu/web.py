"""OdakKoçu'nun küçük web sunucusu."""

from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory

from .agent import FocusAgent

WEB_DIR = Path(__file__).resolve().parents[2] / "web"
load_dotenv()
app = Flask(__name__, static_folder=str(WEB_DIR), static_url_path="")
agent = FocusAgent()


def snapshot() -> dict:
    timer = agent.toolbox.timer_status()
    tasks = agent.toolbox.list_tasks(True)
    summary = agent.toolbox.daily_summary()
    notes = agent.toolbox.list_notes()
    reminders = agent.toolbox.list_reminders()
    sessions = [{"index": index, **session} for index, session in enumerate(agent.toolbox.store.load().get("sessions", []))]
    return {"timer": timer, "tasks": tasks["tasks"], "summary": summary, "routine": summary["routine"], "notes": notes["notes"], "reminders": reminders["reminders"], "sessions": sessions[-8:]}


@app.get("/")
def index():
    return send_from_directory(WEB_DIR, "index.html")


@app.get("/api/state")
def state():
    return jsonify(snapshot())


@app.post("/api/command")
def command():
    body = request.get_json(silent=True) or {}
    message = str(body.get("message", "")).strip()
    if not message:
        return jsonify({"error": "Komut boş olamaz."}), 400
    result = agent.run(message)
    return jsonify({"answer": result.answer, "tool_calls": result.tool_calls, "mode": result.mode, "state": snapshot()})


@app.post("/api/tasks")
def create_task():
    body = request.get_json(silent=True) or {}
    title = str(body.get("title", "")).strip()
    if not title:
        return jsonify({"error": "Görev adı boş olamaz."}), 400
    try:
        minutes = int(body.get("minutes", 25))
    except (TypeError, ValueError):
        minutes = 25
    task = agent.toolbox.add_task(title, minutes, str(body.get("priority", "normal")))
    return jsonify({"task": task, "state": snapshot()})


@app.delete("/api/sessions/<int:session_index>")
def delete_session(session_index: int):
    result = agent.toolbox.delete_session(session_index)
    if result.get("error"):
        return jsonify(result), 404
    return jsonify({"deleted": result["deleted"], "state": snapshot()})


def main() -> None:
    app.run(host="127.0.0.1", port=8000, debug=False)


if __name__ == "__main__":
    main()
