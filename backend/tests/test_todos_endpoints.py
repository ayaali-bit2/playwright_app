import pytest

from backend import app as app_module
from backend.app import app

USER_A = {"id": "user-a", "username": "alice", "display_name": "Alice"}
USER_B = {"id": "user-b", "username": "bob", "display_name": "Bob"}


@pytest.fixture
def client(tmp_path, monkeypatch):
    data_file = tmp_path / "todos.json"
    data_file.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(app_module, "DATA_FILE", data_file)

    app.config.update(TESTING=True, SECRET_KEY="pytest-secret")
    with app.test_client() as test_client:
        with test_client.session_transaction() as sess:
            sess.clear()
        yield test_client


def login_as(client, user):
    with client.session_transaction() as sess:
        sess["user"] = user


class TestSession:
    def test_create_session_success(self, client):
        response = client.post("/api/session", json={"username": "alice"})
        assert response.status_code == 200
        assert response.get_json()["user"]["username"] == "alice"

    def test_create_session_missing_username_returns_400(self, client):
        response = client.post("/api/session", json={})
        assert response.status_code == 400

    def test_get_session_returns_none_when_not_set(self, client):
        response = client.get("/api/session")
        assert response.status_code == 200
        assert response.get_json()["user"] is None

    def test_get_session_returns_user_when_set(self, client):
        client.post("/api/session", json={"username": "alice"})
        response = client.get("/api/session")
        assert response.get_json()["user"]["username"] == "alice"

    def test_clear_session(self, client):
        client.post("/api/session", json={"username": "alice"})
        response = client.delete("/api/session")
        assert response.status_code == 200

        follow_up = client.get("/api/session")
        assert follow_up.get_json()["user"] is None


class TestTodos:
    def test_requires_authentication(self, client):
        response = client.get("/api/todos")
        assert response.status_code == 401

    def test_create_and_list_todo(self, client):
        login_as(client, USER_A)
        create_response = client.post("/api/todos", json={"title": "Buy milk"})
        assert create_response.status_code == 201
        created = create_response.get_json()
        assert created["title"] == "Buy milk"
        assert created["completed"] is False

        list_response = client.get("/api/todos")
        assert list_response.status_code == 200
        todos = list_response.get_json()
        assert len(todos) == 1
        assert todos[0]["id"] == created["id"]

    def test_create_todo_missing_title_returns_400(self, client):
        login_as(client, USER_A)
        response = client.post("/api/todos", json={"title": ""})
        assert response.status_code == 400

    def test_update_todo(self, client):
        login_as(client, USER_A)
        created = client.post("/api/todos", json={"title": "Task"}).get_json()

        response = client.put(f"/api/todos/{created['id']}", json={"completed": True})
        assert response.status_code == 200
        assert response.get_json()["completed"] is True

    def test_update_todo_not_found_returns_404(self, client):
        login_as(client, USER_A)
        response = client.put("/api/todos/does-not-exist", json={"completed": True})
        assert response.status_code == 404

    def test_delete_todo(self, client):
        login_as(client, USER_A)
        created = client.post("/api/todos", json={"title": "Task"}).get_json()

        response = client.delete(f"/api/todos/{created['id']}")
        assert response.status_code == 200

        list_response = client.get("/api/todos")
        assert list_response.get_json() == []

    def test_user_cannot_see_other_users_todos(self, client):
        login_as(client, USER_A)
        client.post("/api/todos", json={"title": "Alice task"})

        login_as(client, USER_B)
        response = client.get("/api/todos")
        assert response.get_json() == []

    def test_user_cannot_update_other_users_todo(self, client):
        login_as(client, USER_A)
        created = client.post("/api/todos", json={"title": "Alice task"}).get_json()

        login_as(client, USER_B)
        response = client.put(f"/api/todos/{created['id']}", json={"title": "Hacked"})
        assert response.status_code == 404

    def test_user_cannot_delete_other_users_todo(self, client):
        login_as(client, USER_A)
        created = client.post("/api/todos", json={"title": "Alice task"}).get_json()

        login_as(client, USER_B)
        response = client.delete(f"/api/todos/{created['id']}")
        assert response.status_code == 404

        login_as(client, USER_A)
        list_response = client.get("/api/todos")
        assert len(list_response.get_json()) == 1
