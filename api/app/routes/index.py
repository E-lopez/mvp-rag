import json
import logging
import pathlib

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from chromadb.api import ClientAPI

from app.dependencies.chroma import ChromaCollectionDep, get_chroma_client
from app.functions.embeddings import embed_text

router = APIRouter()
logger = logging.getLogger(__name__)

_KB_PATH = pathlib.Path(__file__).parent.parent / "data" / "cadre_kb.json"
_COLLECTION_NAME = "cadre_kb"


class IndexResponse(BaseModel):
    indexed: int
    message: str


@router.post("/create-index", response_model=IndexResponse)
def create_index(collection: ChromaCollectionDep):
    try:
        with open(_KB_PATH) as f:
            documents = json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Knowledge base file not found.")

    chroma = get_chroma_client()
    collection = chroma.get_or_create_collection(
        name=_COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    for doc in documents:
        embedding = embed_text(doc["title"] + " " + doc["content"])
        collection.upsert(
            ids=[doc["id"]],
            embeddings=[embedding],
            documents=[doc["content"]],
            metadatas=[{"title": doc["title"], "category": doc["category"]}],
        )
        logger.info("Indexed document: %s", doc["id"])

    return IndexResponse(indexed=len(documents), message="Index created successfully.")
