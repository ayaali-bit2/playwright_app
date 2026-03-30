from typing import Dict
from uuid import uuid4

USERS = [
    {
        "id": "user-1",
        "username": "demo",
        "password": "demo123",
        "display_name": "Demo User",
    },
    {
        "id": "user-2",
        "username": "tester",
        "password": "tester123",
        "display_name": "Playwright Tester",
    },
]

MIN_PASSWORD_LENGTH = 6


class DuplicateUsernameError(ValueError):
    """Raised when a registration request references a username that already exists."""


def _normalize_username(username: str) -> str:
    return (username or "").strip().lower()


def _resolve_display_name(display_name: str | None, normalized_username: str) -> str:
    trimmed = (display_name or "").strip()
    return trimmed if trimmed else normalized_username


def _find_raw_user(username: str) -> Dict[str, str] | None:
    normalized = _normalize_username(username)
    return next((user for user in USERS if user["username"] == normalized), None)


def authenticate_user(username: str, password: str) -> Dict[str, str] | None:
    candidate = _find_raw_user(username)
    if not candidate or candidate["password"] != password:
        return None

    return {
        "id": candidate["id"],
        "username": candidate["username"],
        "display_name": candidate["display_name"],
    }


def register_user(
    username: str, password: str, display_name: str | None = None
) -> Dict[str, str]:
    normalized_username = _normalize_username(username)
    if _find_raw_user(normalized_username):
        raise DuplicateUsernameError("Username already exists.")

    new_user = {
        "id": f"user-{uuid4().hex}",
        "username": normalized_username,
        "password": password,
        "display_name": _resolve_display_name(display_name, normalized_username),
    }
    USERS.append(new_user)

    return {
        "id": new_user["id"],
        "username": new_user["username"],
        "display_name": new_user["display_name"],
    }


def get_user_from_session(session_data: dict) -> Dict[str, str] | None:
    user = session_data.get("user")
    if not isinstance(user, dict):
        return None
    return {
        "id": user.get("id"),
        "username": user.get("username"),
        "display_name": user.get("display_name"),
    }