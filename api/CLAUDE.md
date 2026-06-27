# API Package (Python / FastAPI)

## Module Commands
Run these commands from inside this subdirectory:
- **Run Local API:** `uvicorn app.main:app --reload`
- **Run Test Suite:** `pytest`
- **Run Specific Test:** `pytest tests/test_endpoints.py -k "test_name"`

## Domain Standards
- **Schemas:** Rely strictly on Pydantic v2 models for incoming requests and outgoing validation schemas.
- **Vector Database:** Use an in-memory, ephemeral ChromaDB client instance (`chromadb.EphemeralClient()`). Do not attempt to spin up a standalone Chroma server, Docker containers, or persist data to disk unless explicitly requested.
- **LLM calls:** Use boto3 to call bedrock using env variables for aws access keys.
- **LLM models:** 
  * **Embeddings:** Use `amazon.titan-embed-text-v2:0`
  * **Generative Synthesis and LLMaaJ:** Use `us.anthropic.claude-sonnet-4-6` via cross-region inference profiles.
  * **Topic Recognition:** Use `meta.llama3-8b-instruct-v1:0`
- **Mocking:** Structure third-party HTTP integrations or downstream dependencies using standard `unittest.mock` fixtures inside `conftest.py`.
- **Routing:** use a `main.py` entry-point that imports specific routers for subdomains from the folder `routers`
- **Prompt Engineering:** explicit prompts are found at `api/prompts` grouped by domain, when creating new prompts use that folder and structure

## Coding Guidelines
- **Naming Conventions:** Use lowercase `snake_case` for all Python function names, variables, files, and endpoint paths.
- **Routing:** Locate structural endpoint logic cleanly inside the `app/routes/` folder.
- **Utility Extraction:** Isolate core calculations, financial models, or heavy data wrangling logic into the `app/functions/` directory, cleanly split by domain context.
- **Environment Imports:** Adhere strictly to the project's absolute importing style. Do not dynamically manipulate `sys.path` unless structurally unavoidable.

## Testing Guidelines
- **Requirement:** Write comprehensive regression or unit tests under the `tests/` directory concurrently as new features or system routes are engineered.

## Custom Commands
- `/test-api`: `pytest`
- `/test-endpoint`: `pytest tests/test_endpoints.py`
- `run-api`: `uvicorn app.main:app --app-dir api --reload`