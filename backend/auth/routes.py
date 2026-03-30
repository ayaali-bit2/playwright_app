from flask import Blueprint, jsonify, request, session

from backend.auth.controller import (
    DuplicateUsernameError,
    MIN_PASSWORD_LENGTH,
    authenticate_user,
    get_user_from_session,
    register_user,
)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register_route() -> tuple[dict, int]:
    payload = request.get_json(silent=True) or {}
    username = (payload.get("username") or "").strip()
    password = payload.get("password") or ""
    display_name = payload.get("display_name")

    if not username or not password:
        return {"message": "Username and password are required."}, 400

    if len(password) < MIN_PASSWORD_LENGTH:
        message = f"Password must be at least {MIN_PASSWORD_LENGTH} characters long."
        return {"message": message}, 400

    try:
        user = register_user(username, password, display_name)
    except DuplicateUsernameError:
        return {"message": "Username is already taken."}, 409

    session["user"] = user
    return {"message": "Registration successful.", "user": user}, 201


@auth_bp.route("/login", methods=["POST"])
def login_route() -> tuple[dict, int] | tuple[dict, dict]:
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
    session.pop("user", None)
    return {"message": "Logged out."}, 200


@auth_bp.route("/status", methods=["GET"])
def status_route() -> tuple[dict, int]:
    user = get_user_from_session(session)
    if not user:
        return {"authenticated": False, "message": "Not authenticated."}, 401

    return {"authenticated": True, "user": user}, 200