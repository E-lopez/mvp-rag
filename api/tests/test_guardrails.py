import json
from unittest.mock import MagicMock

from app.services.guardrails import run_query_guardrails


def _stub_bedrock_response(mock_client: MagicMock, generation: str) -> None:
    mock_body = MagicMock()
    mock_body.read.return_value = json.dumps({"generation": generation}).encode()
    mock_client.invoke_model.return_value = {"body": mock_body}


def test_run_query_guardrails_returns_true_for_allowed(mock_bedrock_client):
    _stub_bedrock_response(mock_bedrock_client, "ALLOWED")
    assert run_query_guardrails("What AI services does Cadre offer?") is True
