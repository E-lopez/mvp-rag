import json
import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient


@pytest.fixture
def test_client():
    from app.main import app
    return TestClient(app)


@pytest.fixture
def mock_bedrock_client():
    """Patches the bedrock client in the guardrails service."""
    mock_client = MagicMock()
    with patch("app.services.guardrails.get_bedrock_client", return_value=mock_client):
        yield mock_client


@pytest.fixture
def mock_chroma_collection():
    collection = MagicMock()
    collection.query.return_value = {
        "documents": [["Cadre AI helps businesses implement AI strategies."]],
        "metadatas": [[{"title": "What Cadre AI Does", "category": "general"}]],
    }
    return collection


@pytest.fixture
def mock_chroma_client(mock_chroma_collection):
    mock_client = MagicMock()
    mock_client.get_or_create_collection.return_value = mock_chroma_collection
    mock_client.get_collection.return_value = mock_chroma_collection
    with patch("app.routes.index.get_chroma_client", return_value=mock_client):
        with patch("app.routes.query.get_chroma_client", return_value=mock_client):
            yield mock_client
