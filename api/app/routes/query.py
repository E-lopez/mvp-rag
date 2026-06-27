import json
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.dependencies.bedrock import get_bedrock_client
from app.dependencies.chroma import get_chroma_client
from app.functions.embeddings import embed_text
from app.services.guardrails import run_query_guardrails

router = APIRouter()
logger = logging.getLogger(__name__)

_COLLECTION_NAME = "cadre_kb"
_SYNTHESIS_MODEL_ID = "us.anthropic.claude-sonnet-4-6"
_TOP_K = 3


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[str]


def _synthesize(question: str, context_chunks: list[str]) -> str:
    client = get_bedrock_client()
    context = "\n\n".join(context_chunks)
    response = client.invoke_model(
        modelId=_SYNTHESIS_MODEL_ID,
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "You are a helpful Cadre AI assistant. "
                        "Answer the question using only the context below.\n\n"
                        f"Context:\n{context}\n\n"
                        f"Question: {question}"
                    ),
                }
            ],
        }),
        contentType="application/json",
        accept="application/json",
    )
    result = json.loads(response["body"].read())
    return result["content"][0]["text"]


@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    if not run_query_guardrails(request.question):
        raise HTTPException(status_code=403, detail="Query contains prohibited content.")

    chroma = get_chroma_client()
    try:
        collection = chroma.get_collection(name=_COLLECTION_NAME)
    except Exception:
        raise HTTPException(status_code=503, detail="Index not found. Run /v1/create-index first.")

    query_embedding = embed_text(request.question)
    results = collection.query(query_embeddings=[query_embedding], n_results=_TOP_K)

    context_chunks = results["documents"][0]
    sources = [m["title"] for m in results["metadatas"][0]]

    answer = _synthesize(request.question, context_chunks)
    return QueryResponse(answer=answer, sources=sources)
