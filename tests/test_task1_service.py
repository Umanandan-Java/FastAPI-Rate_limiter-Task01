from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_key_and_access_protected_resources():
    create_response = client.post("/api-key")
    assert create_response.status_code == 201
    api_key = create_response.json()["api_key"]

    headers = {"x-api-key": api_key}

    data_response = client.get("/data", headers=headers)
    assert data_response.status_code == 200

    usage = client.get("/usage", headers=headers)
    assert usage.status_code == 200
    assert usage.json()["total_requests"] >= 2


def test_invalid_key_rejected():
    response = client.get("/data", headers={"x-api-key": "bad-key"})
    assert response.status_code == 401
