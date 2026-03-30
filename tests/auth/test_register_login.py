import pytest

from backend.app import app as flask_app
from backend.auth import controller as auth_controller

BASE_URL = "/api/auth"


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client_instance:
        yield client_instance


@pytest.fixture(autouse=True)
def restore_users():
    original_users = [user.copy() for user in auth_controller.USERS]
    yield
    auth_controller.USERS.clear()
    auth_controller.USERS.extend(user.copy() for user in original_users)


def test_register_successful(client):
    payload = {
        "username": "new-user",
        "password": "ComplexPass123!",
        "display_name": "New User",
    }
    normalized = payload["username"].strip().lower()
    response = client.post(f"{BASE_URL}/register", json=payload)

    assert response.status_code == 201
    body = response.get_json()
    assert body["message"] == "Registration successful."
    assert body["user"]["username"] == normalized
    assert body["user"]["display_name"] == payload["display_name"]
    assert any(user["username"] == normalized for user in auth_controller.USERS)


def test_register_missing_username(client):
    response = client.post(
        f"{BASE_URL}/register", json={"password": "ComplexPass123!"}
    )
    assert response.status_code == 400
    assert response.get_json()["message"] == "Username and password are required."


def test_register_missing_password(client):
    response = client.post(f"{BASE_URL}/register", json={"username": "unique-user"})
    assert response.status_code == 400
    assert response.get_json()["message"] == "Username and password are required."


def test_register_weak_password(client):
    response = client.post(
        f"{BASE_URL}/register",
        json={"username": "weak-user", "password": "123"},
    )
    assert response.status_code == 400
    assert response.get_json()["message"] == (
        f"Password must be at least {auth_controller.MIN_PASSWORD_LENGTH} characters long."
    )


def test_register_duplicate_username(client):
    response = client.post(
        f"{BASE_URL}/register",
        json={"username": "Demo", "password": "DemoPass123!"},
    )
    assert response.status_code == 409
    assert response.get_json()["message"] == "Username is already taken."


def test_register_trims_inputs_and_defaults_display_name(client):
    response = client.post(
        f"{BASE_URL}/register",
        json={
            "username": "  TrimmedUser  ",
            "password": "TrimPass123!",
            "display_name": "   ",
        },
    )
    assert response.status_code == 201
    body = response.get_json()
    assert body["user"]["username"] == "trimmeduser"
    assert body["user"]["display_name"] == "trimmeduser"


def test_register_then_login(client):
    payload = {
        "username": "followup-user",
        "password": "Followup123!",
        "display_name": "Follow Up",
    }
    client.post(f"{BASE_URL}/register", json=payload)
    login_response = client.post(
        f"{BASE_URL}/login",
        json={"username": payload["username"], "password": payload["password"]},
    )
    assert login_response.status_code == 200
    body = login_response.get_json()
    assert body["user"]["username"] == payload["username"].strip().lower()


def test_login_successful_with_existing_user(client):
    response = client.post(
        f"{BASE_URL}/login",
        json={"username": "demo", "password": "demo123"},
    )
    assert response.status_code == 200
    assert response.get_json()["message"] == "Login successful."
    assert response.get_json()["user"]["username"] == "demo"


def test_login_is_case_insensitive(client):
    response = client.post(
        f"{BASE_URL}/login",
        json={"username": "DEMO", "password": "demo123"},
    )
    assert response.status_code == 200
    assert response.get_json()["user"]["username"] == "demo"


def test_login_invalid_credentials(client):
    response = client.post(
        f"{BASE_URL}/login",
        json={"username": "demo", "password": "wrong"},
    )
    assert response.status_code == 401
    assert response.get_json()["message"] == "Invalid credentials."


def test_login_missing_password(client):
    response = client.post(f"{BASE_URL}/login", json={"username": "demo"})
    assert response.status_code == 400
    assert response.get_json()["message"] == "Username and password are required."


def test_login_missing_username(client):
    response = client.post(f"{BASE_URL}/login", json={"password": "demo123"})
    assert response.status_code == 400
    assert response.get_json()["message"] == "Username and password are required."