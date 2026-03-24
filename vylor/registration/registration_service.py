import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4

DEFAULT_STORAGE_FILE = Path(__file__).resolve().parent / "registration_requests.json"


class RegistrationService:
    REQUIRED_FIELDS = ("organization_name", "organization_key", "owner_name", "owner_email")

    def __init__(self, storage_path: Union[str, Path, None] = None) -> None:
        self._storage_path = Path(storage_path) if storage_path else DEFAULT_STORAGE_FILE
        self._storage_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_storage()

    def create_registration(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        normalized = self._normalize_payload(payload)
        self._validate(normalized)

        registrations = self._read_registrations()
        if self._has_conflict(registrations, normalized):
            raise ValueError("An organization with that key or contact email already exists.")

        registrations.append(normalized)
        self._write_registrations(registrations)
        return normalized

    def _normalize_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        def _text(field: str) -> str:
            raw = payload.get(field, "")
            return str(raw).strip()

        organization_key_source = _text("organization_key") or _text("organization_name")
        owner_email = self._normalize_email(_text("owner_email"))
        contact_email = self._normalize_email(_text("contact_email") or owner_email)

        return {
            "request_id": str(uuid4()),
            "organization_name": _text("organization_name"),
            "organization_key": self._normalize_key(organization_key_source),
            "owner_name": _text("owner_name"),
            "owner_email": owner_email,
            "contact_email": contact_email,
            "team_size": self._normalize_team_size(payload.get("team_size")),
            "notes": _text("notes"),
            "status": "pending",
            "created_at": datetime.utcnow().isoformat() + "Z",
        }

    def _validate(self, normalized: Dict[str, Any]) -> None:
        for field in self.REQUIRED_FIELDS:
            if not normalized[field]:
                raise ValueError(f"{field.replace('_', ' ').capitalize()} is required.")

    def _has_conflict(self, registrations: List[Dict[str, Any]], normalized: Dict[str, Any]) -> bool:
        key = normalized["organization_key"]
        email = normalized["contact_email"]
        for existing in registrations:
            if existing.get("organization_key") == key or existing.get("contact_email") == email:
                return True
        return False

    def _read_registrations(self) -> List[Dict[str, Any]]:
        try:
            with self._storage_path.open("r", encoding="utf-8") as stream:
                data = json.load(stream)
                return data if isinstance(data, list) else []
        except (OSError, json.JSONDecodeError):
            return []

    def _write_registrations(self, registrations: List[Dict[str, Any]]) -> None:
        with self._storage_path.open("w", encoding="utf-8") as stream:
            json.dump(registrations, stream, indent=2)

    def _ensure_storage(self) -> None:
        if not self._storage_path.exists():
            self._write_registrations([])

    @staticmethod
    def _normalize_key(value: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "-", value.lower())
        return slug.strip("-")

    @staticmethod
    def _normalize_email(value: str) -> str:
        return value.lower()

    @staticmethod
    def _normalize_team_size(value: Any) -> Optional[int]:
        if value is None or str(value).strip() == "":
            return None
        try:
            parsed = int(str(value))
        except (TypeError, ValueError):
            raise ValueError("Team size must be a whole number.")
        if parsed <= 0:
            raise ValueError("Team size must be at least 1.")
        return parsed