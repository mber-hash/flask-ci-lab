import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_hello_status_code(client):
    response = client.get("/")
    assert response.status_code == 200


def test_hello_message(client):
    response = client.get("/")
    assert response.get_json()["message"] == "Hello, DevOps!"


def test_health_status_code(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_health_response(client):
    response = client.get("/health")
    assert response.get_json()["status"] == "healthy"


def test_info_default_values(client):
    response = client.get("/info")
    data = response.get_json()
    assert data["version"] == "1.0.0"
    assert data["environment"] == "development"


def test_info_custom_env(client, monkeypatch):
    monkeypatch.setenv("APP_VERSION", "2.5.0")
    monkeypatch.setenv("ENVIRONMENT", "production")
    data = client.get("/info").get_json()
    assert data["version"] == "2.5.0"
    assert data["environment"] == "production"


def test_not_found(client):
    assert client.get("/nonexistent").status_code == 404


def test_method_not_allowed(client):
    assert client.post("/").status_code == 405


def test_calc_success(client):
    response = client.get("/api/calc?a=10&b=3&op=add")
    assert response.status_code == 200
    assert response.get_json() == {"result": 13.0, "operation": "add"}


def test_calc_missing_param(client):
    response = client.get("/api/calc?a=10&op=add")
    assert response.status_code == 400
    assert response.get_json() == {"error": "missing parameters"}


def test_calc_invalid_op(client):
    response = client.get("/api/calc?a=10&b=3&op=div")
    assert response.status_code == 400
    assert response.get_json() == {"error": "unknown operation"}


def test_calc_invalid_number(client):
    response = client.get("/api/calc?a=ten&b=3&op=add")
    assert response.status_code == 400
    assert response.get_json() == {"error": "invalid number"}
