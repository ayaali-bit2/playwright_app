from flask import Blueprint, jsonify, request, session

from backend.auth.controller import authenticate_user, get_user_from_session

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login_route() -> tuple[dict, int] | tuple[dict, dict]:
    """Authenticate a user and store their identity in the session."""

    payload = request.get_json(silent=True) or {}
    username = (payload.get("username") or "").strip().lower()
    password = (payload.get("password") or "").strip()

    if not username or not password:
        return {"message": "Username and password are required."}, 400

    user = authenticate_user(username, password)
    if not user:
        return {"message": "Invalid credentials."}, 401

    session["user"] = user
    return {"message": "Login successful.", "user": user}


@auth_bp.route("/logout", methods=["POST"])
def logout_route() -> tuple[dict, int]:
    """Clear the session to log the user out of the application."""

    session.pop("user", None)
    return {"message": "Logged out."}, 200


@auth_bp.route("/status", methods=["GET"])
def status_route() -> tuple[dict, int]:
    """Return the current authentication status with the stored user info."""

    user = get_user_from_session(session)
    if not user:
        return {"authenticated": False, "message": "Not authenticated."}, 401

    return {"authenticated": True, "user": user}, 200
