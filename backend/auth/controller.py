from __future__ import annotations

from typing import Dict
from uuid import uuid4

from werkzeug.security import check_password_hash, generate_password_hash

USERS = [
    {
        "id": "user-1",
        "username": "demo",
        "password_hash": generate_password_hash("demo123"),
        "display_name": "Demo User",
    },
    {
        "id": "user-2",
        "username": "tester",
        "password_hash": generate_password_hash("tester123"),
        "display_name": "Playwright Tester",
    },
]


def _normalize_username(username: str) -> str:
    return username.strip().lower()


def _to_public_user(user: dict) -> Dict[str, str]:
    return {
        "id": user["id"],
        "username": user["username"],
        "display_name": user["display_name"],
    }


def authenticate_user(username: str, password: str) -> Dict[str, str] | None:
    normalized = _normalize_username(username)
    candidate = next(
        (user for user in USERS if user["username"] == normalized),
        None,
    )
    if not candidate or not check_password_hash(candidate["password_hash"], password):
        return None
    return _to_public_user(candidate)


def register_user(username: str, password: str, display_name: str) -> tuple[Dict[str, str] | None, str | None]:
    normalized = _normalize_username(username)
    existing = next((user for user in USERS if user["username"] == normalized), None)
    if existing:
        return None, "Username already exists."

    created = {
        "id": f"user-{uuid4()}",
        "username": normalized,
        "password_hash": generate_password_hash(password),
        "display_name": display_name.strip(),
    }
    USERS.append(created)
    return _to_public_user(created), None


def get_user_from_session(session_data: dict) -> Dict[str, str] | None:
    user = session_data.get("user")
    if not isinstance(user, dict):
        return None

    user_id = user.get("id")
    username = user.get("username")
    display_name = user.get("display_name")
    if not all(isinstance(value, str) and value for value in [user_id, username, display_name]):
        return None

    return {
        "id": user_id,
        "username": username,
        "display_name": display_name,
    }
