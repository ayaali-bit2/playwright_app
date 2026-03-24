from typing import Callable, Optional

from flask import Blueprint, current_app, jsonify, render_template, request
from vylor.registration.registration_service import RegistrationService
from vylor.services.sentry import get_sentry

ServiceFactory = Callable[[Optional[str]], RegistrationService]


def _default_service_factory(storage_path: Optional[str] = None) -> RegistrationService:
    return RegistrationService(storage_path=storage_path)


def create_registration_blueprint(
    service_factory: ServiceFactory = _default_service_factory,
) -> Blueprint:
    registration_bp = Blueprint("registration_bp", __name__)

    def _service() -> RegistrationService:
        storage_path = current_app.config.get("REGISTRATION_STORAGE_PATH")
        return service_factory(storage_path)

    @registration_bp.route("/register", methods=["GET"])
    def render_registration():
        return render_template("register.html"), 200

    @registration_bp.route("/api/register", methods=["POST"])
    def register():
        payload = request.get_json(silent=True)
        if payload is None:
            payload = request.form.to_dict()
        service = _service()
        try:
            registration = service.create_registration(payload or {})
            return (
                jsonify(
                    {
                        "status": "success",
                        "message": "We received your registration request.",
                        "registration": registration,
                    }
                ),
                201,
            )
        except ValueError as exc:
            return jsonify({"status": "error", "error": str(exc)}), 400
        except Exception as exc:
            get_sentry().capture_exception(exc)
            return (
                jsonify(
                    {
                        "status": "error",
                        "error": "We could not process your registration request right now.",
                    }
                ),
                500,
            )

    return registration_bp


registration_bp = create_registration_blueprint()