from fastapi import FastAPI
from dotenv import load_dotenv, find_dotenv

from app.routes import index, query

load_dotenv(find_dotenv())

app = FastAPI(title="Cadre AI API")

app.include_router(index.router, prefix="/v1")
app.include_router(query.router, prefix="/v1")


@app.get("/health")
def health():
    return {"status": "ok"}
