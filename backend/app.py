from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List
from uuid import uuid4

from flask import Flask, abort, jsonify, request
from flask_cors import CORS

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "todos.json"
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
CORS(app)


def read_todos() -> List[Dict[str, Any]]:
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError:
        logging.warning("Unable to parse todos.json, resetting data store to an empty list.")
        return []


def persist_todos(todos: List[Dict[str, Any]]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as handle:
        json.dump(todos, handle, indent=2)


def find_todo(todos: List[Dict[str, Any]], todo_id: str) -> Dict[str, Any] | None:
    return next((item for item in todos if item["id"] == todo_id), None)


@app.route("/api/todos", methods=["GET"])
def list_todos() -> Any:
    return jsonify(read_todos())


@app.route("/api/todos", methods=["POST"])
def create_todo() -> Any:
    payload = request.get_json(silent=True) or {}
    title = (payload.get("title") or "").strip()
    if not title:
        return jsonify({"message": "Title is required."}), 400

    description = (payload.get("description") or "").strip()
    todos = read_todos()
    new_task = {
        "id": str(uuid4()),
        "title": title,
        "description": description,
        "completed": False,
    }
    todos.append(new_task)
    persist_todos(todos)
    return jsonify(new_task), 201


@app.route("/api/todos/<todo_id>", methods=["PUT"])
def update_todo(todo_id: str) -> Any:
    payload = request.get_json(silent=True) or {}
    todos = read_todos()
    todo = find_todo(todos, todo_id)
    if not todo:
        abort(404, description="Task not found")

    if "title" in payload:
        title = (payload.get("title") or "").strip()
        if not title:
            return jsonify({"message": "Title cannot be empty."}), 400
        todo["title"] = title
    if "description" in payload:
        todo["description"] = (payload.get("description") or "").strip()
    if "completed" in payload:
        todo["completed"] = bool(payload["completed"])

    persist_todos(todos)
    return jsonify(todo)


@app.route("/api/todos/<todo_id>", methods=["DELETE"])
def delete_todo(todo_id: str) -> Any:
    todos = read_todos()
    filtered = [item for item in todos if item["id"] != todo_id]
    if len(filtered) == len(todos):
        abort(404, description="Task not found")

    persist_todos(filtered)
    return jsonify({"message": "Task deleted."})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
