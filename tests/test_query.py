from fastapi.testclient import TestClient

from app.main import app
from app.routers import query as query_router


client = TestClient(app)


def test_query_success(monkeypatch):

    async def fake_answer_question(
        question: str,
        namespace: str,
    ):
        return {
            "answer": "RAG stands for Retrieval-Augmented Generation.",
            "sources": [
                {
                    "id": "sample.txt#chunk-0",
                    "filename": "sample.txt",
                    "chunk_index": 0,
                    "score": 0.35,
                }
            ],
        }

    monkeypatch.setattr(
        query_router,
        "answer_question",
        fake_answer_question,
    )

    response = client.post(
        "/tenants/acme/query",
        json={
            "question": "What is RAG?"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == (
        "RAG stands for Retrieval-Augmented Generation."
    )

    assert len(data["sources"]) == 1

    assert data["sources"][0]["filename"] == "sample.txt"


def test_query_missing_question():

    response = client.post(
        "/tenants/acme/query",
        json={},
    )

    assert response.status_code == 422