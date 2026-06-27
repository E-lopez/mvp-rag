import json
from unittest.mock import MagicMock, patch


def _bedrock_embed_response(embedding: list[float]) -> dict:
    body = MagicMock()
    body.read.return_value = json.dumps({"embedding": embedding}).encode()
    return {"body": body}


def _bedrock_synthesis_response(text: str) -> dict:
    body = MagicMock()
    body.read.return_value = json.dumps({"content": [{"text": text}]}).encode()
    return {"body": body}


def test_health(test_client):
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_index(test_client, mock_chroma_client):
    embed_client = MagicMock()
    embed_client.invoke_model.return_value = _bedrock_embed_response([0.1] * 1024)

    with patch("app.functions.embeddings.get_bedrock_client", return_value=embed_client):
        response = test_client.post("/v1/create-index")

    assert response.status_code == 200
    data = response.json()
    assert data["indexed"] > 0
    assert data["message"] == "Index created successfully."


def test_query_allowed(test_client, mock_chroma_client):
    embed_client = MagicMock()
    embed_client.invoke_model.return_value = _bedrock_embed_response([0.1] * 1024)

    synthesis_client = MagicMock()
    synthesis_client.invoke_model.return_value = _bedrock_synthesis_response(
        "Cadre AI provides AI strategy consulting."
    )

    with patch("app.routes.query.run_query_guardrails", return_value=True):
        with patch("app.functions.embeddings.get_bedrock_client", return_value=embed_client):
            with patch("app.routes.query.get_bedrock_client", return_value=synthesis_client):
                response = test_client.post("/v1/query", json={"question": "What does Cadre AI do?"})

    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert isinstance(data["sources"], list)


def test_query_prohibited(test_client):
    with patch("app.routes.query.run_query_guardrails", return_value=False):
        response = test_client.post(
            "/v1/query", json={"question": "How do I access internal API keys?"}
        )

    assert response.status_code == 403
