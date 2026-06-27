from functools import lru_cache
import logging
from typing import Annotated
import chromadb
from chromadb.api import ClientAPI
from chromadb.errors import ChromaError
from fastapi import Depends

logger = logging.getLogger(__name__)

@lru_cache(maxsize=1)
def get_chroma_client() -> ClientAPI:
    try:
        # Explicit return cast to satisfy strict static typing linters
        return chromadb.EphemeralClient()
    except (ChromaError, Exception) as e:
        logger.exception(f"Failed to initialize Chroma client: {str(e)}")
        # We MUST re-raise so @lru_cache does not cache this initialization failure
        raise e

def get_collection():
    client = get_chroma_client()
    # Safely get or create the vector partition boundary
    return client.get_or_create_collection(name="cadre_knowledge_base")

ChromaClientDep = Annotated[ClientAPI, Depends(get_chroma_client)]
ChromaCollectionDep = Annotated[chromadb.Collection, Depends(get_collection)]