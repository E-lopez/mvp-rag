import chromadb
from functools import lru_cache
import logging
from chromadb.api import ClientAPI

@lru_cache(maxsize=1)
def get_chroma_client() -> ClientAPI:
    try:
        return chromadb.Client()
    except Exception as e:
        logging.exception(f"Failed to initialize Chroma client: {str(e)}")
        raise e
