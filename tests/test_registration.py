import json
import tempfile
import unittest
from pathlib import Path

from vylor.server import app as server_app


class RegistrationTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.close()
        self.storage_path = Path(temp.name)
        self.storage_path.write_text("[]", encoding="utf-8")
        server_app.config["TESTING"] = True
        server_app.config["REGISTRATION_STORAGE_PATH"] = str(self.storage_path)
        self.client = server_app.test_client()

    def tearDown(self):
        try:
            self.storage_path.unlink()
        except OSError:
            pass

    def _payload(self):
        return {
            "organization_name": "Nebula Labs",
            "organization_key": "nebula-labs",
            "owner_name": "Tara Hill",
            "owner_email": "tara@nebulalabs.com",
            "contact_email": "hello@nebulalabs.com",
            "team_size": "12",
            "notes": "Exploring how Vylor can help us ship faster.",
        }

    def _read_storage(self):
        text = self.storage_path.read_text(encoding="utf-8").strip()
        return json.loads(text or "[]")

    def _post_registration(self, overrides=None):
        payload = self._payload()
        if overrides:
            payload.update(overrides)
        return self.client.post("/api/register", json=payload)

    def test_register_success_creates_request(self):
        response = self._post_registration()
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["status"], "success")
        stored = self._read_storage()
        self.assertEqual(len(stored), 1)
        record = stored[0]
        self.assertEqual(record["organization_key"], "nebula-labs")
        self.assertEqual(record["team_size"], 12)
        self.assertEqual(record["status"], "pending")

    def test_register_duplicate_key_rejected(self):
        self._post_registration()
        response = self._post_registration()
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())
        stored = self._read_storage()
        self.assertEqual(len(stored), 1)