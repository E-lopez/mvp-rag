import json
import logging

from botocore.exceptions import BotoCoreError, ClientError
from fastapi import HTTPException

from app.dependencies.bedrock import get_bedrock_client
from app.prompts.guardrails import GUARDRAIL_PROHIBITED_PROMPT

logger = logging.getLogger(__name__)

_MODEL_ID = "meta.llama3-8b-instruct-v1:0"

_PROMPT_TEMPLATE = (
    "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
    "{system_prompt}"
    "<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"
    "{query}"
    "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
)


def run_query_guardrails(query: str) -> bool:
    client = get_bedrock_client()

    prompt = _PROMPT_TEMPLATE.format(
        system_prompt=GUARDRAIL_PROHIBITED_PROMPT,
        query=query,
    )

    try:
        response = client.invoke_model(
            modelId=_MODEL_ID,
            body=json.dumps({"prompt": prompt, "max_gen_len": 10, "temperature": 0.0}),
            contentType="application/json",
            accept="application/json",
        )
    except (BotoCoreError, ClientError) as e:
        raise HTTPException(status_code=502, detail="Upstream model call failed.") from e

    result = json.loads(response["body"].read())
    verdict = result.get("generation", "PROHIBITED").strip().upper()

    logger.info("Guardrail verdict: %s", verdict)

    return verdict == "ALLOWED"
