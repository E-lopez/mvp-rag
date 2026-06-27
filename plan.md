# Engineering Plan: [Project Name]

> **What we are building:** A monorepo containing a FastAPI backend and a React frontend.
> **How we are working with AI:** We are keeping the AI on a short leash by separating frontend and backend context so it doesn't waste tokens, using shortcodes for tests, and logging when it spawns sub-tasks.

---

## 1. Project Folders & AI Context Boundaries
To stop the AI from getting confused or reading files it shouldn't be touching, we strictly isolate its memory using our folder setups. 

* **Backend Apps:** Located in `api/app/`. The AI only reads backend rules here.
* **Frontend Apps:** Located in `ui/src/`. The AI only reads UI rules here.

---

## 2. Step-by-Step Implementation

### Phase 1: Backend Setup
*Goal: set up the backend structure and external clients*
- [X] **Milestone 1: Core API**
  * **Setup Clients:** 
    - AWS Bedrock client using `boto3` (authenticating via local `.env` access keys).
    - In-memory ChromaDB instance (`chromadb.EphemeralClient()`) for vector storage.
- [X] **Milestone 2: Core API**
  * **Guardrails Services** (`app/services/guardrails.py`)
    - Build `run_query_guardrails(query: str) -> bool` pipeline.
    - Use `GUARDRAIL_PROHIBITED_PROMPT` from `app/prompts/guardrails.py` to model `meta.llama3-8b-instruct-v1:0`.
    - Stub the function to return `True` (ALLOWED) for this milestone's boilerplate test.
- [X] **Milestone 3: Core API**
  * **Endpoints to Build:**
    - GET `/health` -> Simple uptime status check.
    - POST `/v1/create-index` -> Reads and indexes the raw JSON data located at `api/app/data/cadre_kb.json`.
    - POST `/v1/query` -> Accepts a question, uses `run_query_guardrails()`to identify restricted questions in it, if the returned value is `ALLOWED` then it embeds it via Bedrock Titan, searches ChromaDB using cosine similarity, and synthesizes a response using Claude Sonnet 4.6.
  * **Context Boundary:** All changes isolated inside `api/app/`.

  * **Planned File Structure:**
    `app/main.py` - Application entry point and router inclusion, includes GET /health endpoint.
    `app/dependencies/bedrock.py` - Independent AWS Bedrock client initialization using boto3.
    `app/dependencies/chroma.py` - Independent in-memory ChromaDB EphemeralClient initialization.
    `app/routes/query.py` - POST /v1/query endpoint with the guardrail logic wrapper. This endpoint will use the 'prohibited topics guardrail' as defined by `GUARDRAIL_PROHIBITED_PROMPT` from `app/functions/prompts.py` to model `meta.llama3-8b-instruct-v1:0`.
    `app/routes/index.py` - POST /v1/create-index endpoint.
    `app/prompts/prompts.py` - Llama 3 guardrail prompt constants.

### Phase 2: Frontend Implementation
*Goal: set up the client-side user interface and integrate end-to-end RAG state workflows*
- [ ] **Milestone 1: State Architecture & Skeleton Layout**
  * **Setup Context & Reducers:**
    - App state manager (`ui/src/context/AppStateContext.tsx`) using `useContext` and `useReducer`.
    - State schema containing trackable keys: `loading`, `indexCreated`, `answer`, `sources`, and `error`.
    - Actions to implement: `START_QUERY`, `SET_QUERY_RESPONSE`, `SET_INDEX_STATUS`, `SET_ERROR`.
  * **UI Layout Structure:**
    - Render a simple, centered interface shell with an input form field (`<SearchForm />`).
    - Build a content display container box positioned directly below the input bar (`<ResponseDisplay />`).

- [ ] **Milestone 2: Lifecycle Anchors & API Integration**
  * **On-Mount Initialization:**
    - Configure a root-level `useEffect` hook to fire immediately when the interface mounts.
    - Hook dispatches an asynchronous call directly to the backend endpoint `POST /v1/create-index`.
    - On a successful network transaction, updates the application state property `indexCreated: true`.
  * **Search Interaction:**
    - Wire the form submit/search button to trigger an authorized call to `POST /v1/query`.
    - Prevent parallel click events by forcing a loading barrier state while a request is in flight.

- [ ] **Milestone 3: Presentation & Markdown Rendering**
  * **Formatted Output Rendering:**
    - Connect the dynamic response box below the input bar to parse and display the RAG-generated content cleanly.
    - Implement a safe rich-text renderer (e.g., `react-markdown`) wrapped in a Tailwind CSS Typography container (`prose`) to parse bold phrases, bullet items, and structural text directly from the API string.
  * **Source Attribution:**
    - Map over the array returned in the `sources` parameter to display crisp lookup tags or citations at the foot of the answer box.
    - Gracefully map backend network validation or guardrail failures to an error presentation box without crashing the active UI layout.

  * **Planned File Structure:**
    `ui/src/context/AppStateContext.tsx` - Holds the global application state, useReducer handles, and Context Provider wrappers.
    `ui/src/components/SearchForm.tsx` - Input element field and search submission action button; dispatches to the backend.
    `ui/src/components/ResponseDisplay.tsx` - Content presentation box with markdown rendering and dynamic error blocks.
    `ui/src/components/SourceTags.tsx` - Renders lists of reference files or text chunks mapped from the API data array.
    `ui/src/App.tsx` - Application bootstrap container that hosts layout components and fires the on-mount index generation script.

### Phase 3: Guardrailing and Evals

### Phase 4: 

---

## 4. Work Log & AI Context Notes
*This is where we log any time the AI shifts strategy, runs into an error, or spawns an independent sub-task to solve a problem.*

* **[2026-06-27]** Initialized repository structure and set up folder-level rules.
- **Manual Edits**: 
  - Manually wrapped AWS Bedrock, ChromaDB client initialization (`get_bedrock_client`) in a `try/except` block.
  - Augments synthesis prompt to comply estrict formatting compatible with UI and safety.
