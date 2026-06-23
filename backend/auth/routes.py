from __future__ import annotations

import re

from flask import Blueprint, request, session

from backend.auth.controller import authenticate_user, get_user_from_session, register_user

auth_bp = Blueprint("auth", __name__)

USERNAME_PATTERN = re.compile(r"^[a-z0-9_.-]+$")


def _clean_text(value: object) -> str:
    if isinstance(value, str):
        return value.strip()
    return ""


@auth_bp.route("/register", methods=["POST"])
def register_route() -> tuple[dict, int]:
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return {"message": "Invalid JSON payload."}, 400

    username = _clean_text(payload.get("username")).lower()
    password = _clean_text(payload.get("password"))
    display_name = _clean_text(payload.get("display_name"))

    if not username or not password or not display_name:
        return {"message": "Username, password, and display_name are required."}, 400

    if len(username) < 3 or len(username) > 50:
        return {"message": "Username must be between 3 and 50 characters."}, 400
    if not USERNAME_PATTERN.fullmatch(username):
        return {"message": "Username may contain lowercase letters, numbers, '.', '_' and '-' only."}, 400

    if len(password) < 6:
        return {"message": "Password must be at least 6 characters long."}, 400
    if len(password) > 128:
        return {"message": "Password must be at most 128 characters long."}, 400

    if len(display_name) > 80:
        return {"message": "Display name must be at most 80 characters long."}, 400

    user, error = register_user(username=username, password=password, display_name=display_name)
    if error:
        return {"message": error}, 409

    session["user"] = user
    return {"message": "Registration successful.", "user": user}, 201


@auth_bp.route("/login", methods=["POST"])
def login_route() -> tuple[dict, int]:
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return {"message": "Invalid JSON payload."}, 400

    username = _clean_text(payload.get("username")).lower()
    password = _clean_text(payload.get("password"))

    if not username or not password:
        return {"message": "Username and password are required."}, 400

    user = authenticate_user(username, password)
    if not user:
        return {"message": "Invalid credentials."}, 401

    session["user"] = user
    return {"message": "Login successful.", "user": user}, 200


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