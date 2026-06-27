import json
import logging
import re

from botocore.exceptions import BotoCoreError, ClientError

from app.dependencies.bedrock import get_bedrock_client
from app.prompts.judge import JUDGE_PROMPT

logger = logging.getLogger(__name__)

_JUDGE_MODEL_ID = "us.anthropic.claude-sonnet-4-6"
_CODE_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL)


def run_rag_eval(
    user_query: str,
    retrieved_context: str,
    generated_response: str,
) -> None:
    filled_prompt = (
        JUDGE_PROMPT
        .replace("{{USER_QUERY}}", user_query)
        .replace("{{RETRIEVED_CONTEXT}}", retrieved_context)
        .replace("{{GENERATED_RESPONSE}}", generated_response)
    )

    try:
        client = get_bedrock_client()
        response = client.invoke_model(
            modelId=_JUDGE_MODEL_ID,
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 2048,
                "system": filled_prompt,
                "messages": [{"role": "user", "content": "Evaluate."}],
            }),
            contentType="application/json",
            accept="application/json",
        )
    except (BotoCoreError, ClientError):
        logger.exception("RAG eval: Bedrock call failed — skipping eval for this transaction.")
        return

    try:
        raw_text = json.loads(response["body"].read())["content"][0]["text"]
        match = _CODE_FENCE_RE.search(raw_text)
        json_str = match.group(1) if match else raw_text
        verdict = json.loads(json_str)
    except Exception:
        logger.exception("RAG eval: failed to parse judge response.")
        return

    logger.info(
        "RAG eval — context_relevance=%.1f groundedness=%.1f answer_relevance=%.1f | verdict: %s",
        verdict.get("context_relevance", {}).get("score", -1),
        verdict.get("groundedness", {}).get("score", -1),
        verdict.get("answer_relevance", {}).get("score", -1),
        verdict.get("triad_summary_verdict", ""),
    )
    logger.debug("RAG eval full verdict: %s", json.dumps(verdict))
