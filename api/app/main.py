import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv, find_dotenv
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routes import index, query

load_dotenv(find_dotenv())

app = FastAPI(title="Cadre AI API")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(index.router, prefix="/v1")
app.include_router(query.router, prefix="/v1")

@app.get("/health")
def health():
    return {"status": "ok"}

STATIC_ASSETS_PATH = os.path.join(os.path.dirname(__file__), "static")

if os.path.exists(STATIC_ASSETS_PATH):
    # 1. Mount index assets like assets/index-DI783.js or favicon images
    app.mount("/assets", StaticFiles(directory=os.path.join(STATIC_ASSETS_PATH, "assets")), name="assets")

    # 2. Catch-all fallback route to serve the SPA (Single Page Application)
    # This allows users to hit any URL path and lets React Router take over client routing.
    @app.get("/{catchall:path}")
    async def serve_react_app(catchall: str):
        # If an incoming request hits here and starts with v1/ or health,
        # it means it didn't match any valid router endpoint above.
        # Throw a proper 404 JSON error instead of crashing with None or returning index.html.
        if catchall.startswith("v1") or catchall == "health":
            raise HTTPException(status_code=404, detail="API route endpoint not found.")
            
        index_file = os.path.join(STATIC_ASSETS_PATH, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
            
        return {"error": "Frontend build files missing from static directory."}

