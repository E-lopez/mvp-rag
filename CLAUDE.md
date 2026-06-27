# Monorepo Core Rules

## Global Commands

## Multi-Package Strategy
This repository layers specific rules across separate directories. Do not load UI conventions into backend files.
- See `@api/CLAUDE.md` for api framework constraints.
- See `@ui/CLAUDE.md` for ui component standards.

## Universal Requirements
- **Git Workflow:** Use descriptive branch names (`feature/`, `bugfix/`).
- **Commit Convention:** Must follow this explicit format: `[ui|api] [feature|bugfix|test|refactor]: description`
- **Secrets Protection:** Never commit plaintext keys, environment variables, or mock test tokens. Use local `.env` files exclusively.

## Architectural Guidelines
- **Single Responsibility Principle:** Keep functions, modules, and components tightly scoped to a single purpose.
- **Performance:** Keep code clean. Avoid deeply nested loops or conditional branches. Target optimal time complexity ($O(n \log n)$ or better where applicable).
- **DRY Principle:** Reuse utility functions. Do not duplicate similar logic across files.
- **Changelog Maintenance:** Upon successful completion of a feature, module, or major phase, update `changelog.md` at the project root. Format entries succinctly: `[YYYY-MM-DD HH:mm] [ui|api] - Summary of changes`.

### 🛠️ AI & Data Layer Boundaries
- **Vector Database:** Use an in-memory, ephemeral ChromaDB client instance (`chromadb.EphemeralClient()`). Do not attempt to spin up a standalone Chroma server, Docker containers, or persist data to disk unless explicitly requested.
- **Model Strategy:**
  * **Embedding Model:** Use `amazon.titan-embed-text-v2:0` (via bedrock) to vectorize local markdown context documents before storing them in ChromaDB and user query for similarity search.
  * **Generative Model and LLMaaJ:** Use `us.anthropic.claude-sonnet-4-6` to handle conversational synthesis based on the retrieved context chunks.
  * **Topic Recognition:** Use `meta.llama3-8b-instruct-v1:0` to identify prohibited or violatory topics in user query.
- **Cost Control:** Always prioritize low-cost, fast inference models (`-mini` or `-haiku` variants) for text processing tasks to minimize token overhead.