import pytest

from backend.app import app
from backend.auth import controller

AUTH_BASE = "/api/auth"


@pytest.fixture(autouse=True)
def reset_users():
    original_users = [user.copy() for user in controller.USERS]
    yield
    controller.USERS[:] = original_users


@pytest.fixture
def client():
    app.config.update(TESTING=True, SECRET_KEY="pytest-secret")
    with app.test_client() as test_client:
        with test_client.session_transaction() as sess:
            sess.clear()
        yield test_client


def test_login_success_with_valid_credentials(client):
    response = client.post(
        f"{AUTH_BASE}/login",
        json={"username": "demo", "password": "demo123"},
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["message"] == "Login successful."
    assert payload["user"]["username"] == "demo"
    assert payload["user"]["display_name"] == "Demo User"


def test_login_invalid_credentials_returns_401(client):
    response = client.post(
        f"{AUTH_BASE}/login",
        json={"username": "demo", "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.get_json()["message"] == "Invalid credentials."


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"username": "demo"},
        {"password": "demo123"},
        {"username": "", "password": "demo123"},
        {"username": "demo", "password": ""},
    ],
)
def test_login_missing_required_fields_returns_400(client, payload):
    response = client.post(f"{AUTH_BASE}/login", json=payload)
    assert response.status_code == 400
    assert response.get_json()["message"] == "Username and password are required."


def test_login_non_string_inputs_are_handled_as_invalid(client):
    response = client.post(
        f"{AUTH_BASE}/login",
        json={"username": 123, "password": ["not-a-string"]},
    )
    assert response.status_code == 400
    assert response.get_json()["message"] == "Username and password are required."


def test_register_success_creates_user_and_authenticates_session(client):
    response = client.post(
        f"{AUTH_BASE}/register",
        json={
            "username": "  New.User  ",
            "password": "validPassword123",
            "display_name": "New User",
        },
    )

    assert response.status_code == 201
    payload = response.get_json()
    assert payload["message"] == "Registration successful."
    assert payload["user"]["username"] == "new.user"
    assert payload["user"]["display_name"] == "New User"
    assert payload["user"]["id"].startswith("user-")

    status_response = client.get(f"{AUTH_BASE}/status")
    assert status_response.status_code == 200
    status_payload = status_response.get_json()
    assert status_payload["authenticated"] is True
    assert status_payload["user"]["username"] == "new.user"


def test_register_duplicate_username_is_case_insensitive(client):
    response = client.post(
        f"{AUTH_BASE}/register",
        json={
            "username": "DEMO",
            "password": "anotherPass123",
            "display_name": "Duplicate User",
        },
    )

    assert response.status_code == 409
    assert response.get_json()["message"] == "Username already exists."


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"username": "newuser", "password": "valid123"},
        {"username": "newuser", "display_name": "User"},
        {"password": "valid123", "display_name": "User"},
    ],
)
def test_register_missing_required_fields_returns_400(client, payload):
    response = client.post(f"{AUTH_BASE}/register", json=payload)
    assert response.status_code == 400
    assert response.get_json()["message"] == "Username, password, and display_name are required."


def test_register_invalid_username_format_returns_400(client):
    response = client.post(
        f"{AUTH_BASE}/register",
        json={
            "username": "bad user name!",
            "password": "valid123",
            "display_name": "Bad Username",
        },
    )
    assert response.status_code == 400
    assert "Username may contain lowercase letters" in response.get_json()["message"]


@pytest.mark.parametrize(
    "password,message",
    [
        ("12345", "Password must be at least 6 characters long."),
        ("x" * 129, "Password must be at most 128 characters long."),
    ],
)
def test_register_password_boundaries(client, password, message):
    response = client.post(
        f"{AUTH_BASE}/register",
        json={
            "username": "boundaryuser",
            "password": password,
            "display_name": "Boundary User",
        },
    )

    assert response.status_code == 400
    assert response.get_json()["message"] == message