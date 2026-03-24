from flask import Blueprint, jsonify, request
import bcrypt
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from vylor.authentication.mysql_service import MySQLService

auth_bp = Blueprint("auth", __name__)
mysql_service = MySQLService()


def _bad_request(message: str):
    return jsonify({"error": message}), 400


@auth_bp.route("/register", methods=["POST"])
def register():
    payload = request.get_json(silent=True)
    if not payload:
        return _bad_request("Request body must be JSON.")
    name = payload.get("name")
    email = payload.get("email")
    password = payload.get("password")
    if not name or not email or not password:
        return _bad_request("Name, email, and password are required.")

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    session = mysql_service.get_session()
    try:
        session.execute(
            text(
                "INSERT INTO users (name, email, password) VALUES (:name, :email, :password)"
            ),
            {"name": name, "email": email, "password": hashed_password},
        )
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        error_message = str(getattr(exc, "orig", exc))
        if "Duplicate entry" in error_message or "1062" in error_message:
            return (
                jsonify({"error": "A user with that email already exists."}),
                409,
            )
        raise
    finally:
        session.close()

    return jsonify({"message": "User registered successfully."}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    payload = request.get_json(silent=True)
    if not payload:
        return _bad_request("Request body must be JSON.")
    email = payload.get("email")
    password = payload.get("password")
    if not email or not password:
        return _bad_request("Email and password are required.")

    session = mysql_service.get_session()
    try:
        result = session.execute(
            text(
                "SELECT id, name, email, password FROM users WHERE email = :email LIMIT 1"
            ),
            {"email": email},
        )
        user = result.mappings().first()
        if not user or not bcrypt.checkpw(
            password.encode("utf-8"), user["password"].encode("utf-8")
        ):
            return jsonify({"error": "Invalid email or password."}), 401

        safe_user = {"id": user["id"], "name": user["name"], "email": user["email"]}
        return jsonify({"message": "Login successful.", "user": safe_user}), 200
    finally:
        session.close()