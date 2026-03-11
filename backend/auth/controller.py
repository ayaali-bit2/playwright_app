from typing import Dict

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


def authenticate_user(username: str, password: str) -> Dict[str, str] | None:
    normalized = username.strip().lower()
    candidate = next(
        (
            user
            for user in USERS
            if user["username"] == normalized and user["password"] == password
        ),
        None,
    )
    if not candidate:
        return None

    return {
        "id": candidate["id"],
        "username": candidate["username"],
        "display_name": candidate["display_name"],
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
