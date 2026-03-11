from __future__ import annotations

import json
import logging
import os
from functools import wraps
from pathlib import Path
from typing import Any, Dict, List
from uuid import uuid4

from flask import Flask, abort, jsonify, request, session
from flask_cors import CORS

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "todos.json"
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-insecure-secret")

_default_origins = ["http://localhost:3000", "http://localhost:4173"]
frontend_origins = [
    origin.strip()
    for origin in os.environ.get("FRONTEND_ORIGINS", ",".join(_default_origins)).split(",")
    if origin.strip()
]
session_cookie_name = os.environ.get("FLASK_SESSION_COOKIE_NAME", "session")
session_cookie_samesite = os.environ.get("FLASK_SESSION_COOKIE_SAMESITE", "None")
session_cookie_secure = os.environ.get("FLASK_SESSION_COOKIE_SECURE", "False").lower() in {
    "1",
    "true",
    "yes",
}

app.config.update(
    {
        "SESSION_COOKIE_NAME": session_cookie_name,
        "SESSION_COOKIE_HTTPONLY": True,
        "SESSION_COOKIE_SAMESITE": session_cookie_samesite,
        "SESSION_COOKIE_SECURE": session_cookie_secure,
        "SESSION_REFRESH_EACH_REQUEST": True,
    }
)
CORS(app, supports_credentials=True, origins=frontend_origins or _default_origins)

SESSION_USER_KEY = "user"


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not session.get(SESSION_USER_KEY):
            abort(401, description="Authentication is required to access this resource.")
        return view(*args, **kwargs)

    return wrapper


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


def _resolve_username(payload: Dict[str, Any]) -> str | None:
    username = payload.get("username") or payload.get("email")
    if username and isinstance(username, str):
        trimmed = username.strip()
        if trimmed:
            return trimmed
    return None


@app.route("/api/session", methods=["POST"])
def create_session() -> Any:
    payload = request.get_json(silent=True) or {}
    username = _resolve_username(payload)
    if not username:
        return jsonify({"message": "Provide a username or email to start a session."}), 400

    session[SESSION_USER_KEY] = {"username": username}
    session.permanent = True
    return jsonify({"user": session[SESSION_USER_KEY]})


@app.route("/api/session", methods=["GET"])
def get_session() -> Any:
    return jsonify({"user": session.get(SESSION_USER_KEY)})


@app.route("/api/session", methods=["DELETE"])
def clear_session() -> Any:
    session.pop(SESSION_USER_KEY, None)
    return jsonify({"message": "Session cleared."})


@app.route("/api/todos", methods=["GET"])
@login_required
def list_todos() -> Any:
    return jsonify(read_todos())


@app.route("/api/todos", methods=["POST"])
@login_required
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
@login_required
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
@login_required
def delete_todo(todo_id: str) -> Any:
    todos = read_todos()
    filtered = [item for item in todos if item["id"] != todo_id]
    if len(filtered) == len(todos):
        abort(404, description="Task not found")

    persist_todos(filtered)
    return jsonify({"message": "Task deleted."})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)