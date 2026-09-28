from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Omnibound RAG API is running"


def test_query_validation():
    response = client.post(
        "/tenants/acme/query",
        json={},
    )

    assert response.status_code == 422


def test_query_invalid_body():
    response = client.post(
        "/tenants/acme/query",
        json={
            "wrong_field": "What is RAG?"
        },
    )

    assert response.status_code == 422