import json

from botocore.exceptions import BotoCoreError, ClientError
from fastapi import HTTPException

from app.dependencies.bedrock import get_bedrock_client

_EMBED_MODEL_ID = "amazon.titan-embed-text-v2:0"


def embed_text(text: str) -> list[float]:
    client = get_bedrock_client()
    try:
        response = client.invoke_model(
            modelId=_EMBED_MODEL_ID,
            body=json.dumps({"inputText": text}),
            contentType="application/json",
            accept="application/json",
        )
    except (BotoCoreError, ClientError) as e:
        raise HTTPException(status_code=502, detail="Upstream model call failed.") from e
    return json.loads(response["body"].read())["embedding"]
