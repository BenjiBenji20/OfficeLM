## Project overview

OfficeLM is a self-hostable, multi-user, multi-room chat AI companion for office
environments, similar to NotebookLM. It runs as a private server
(Windows-first, cross-platform capable). Teams ingest corporate documents and
query them together (RAG), and the assistant generates real, downloadable
office files from chat requests.

**How it differs from NotebookLM**
- Self-hostable: data never has to leave the organization's infrastructure.
- Acts, not just answers: chat intent produces real office files.
- Shared by design: multiple users and rooms, not per-user notebooks.

**Model support (deliberately limited scope)**
- Built for local use; the local model family is Llama.
- Optional hosted providers via SDK: OpenAI and Gemini only (for now).
- Do not add other providers or SDKs unless asked.

**What it is not**
- Not a SaaS or cloud-first product.
- Not a per-user notebook app.
- Not a general-purpose chatbot.

**What this means for you**
- Treat data privacy as a hard requirement: no code path should send documents
  or chat content to an external service unless a hosted provider is explicitly configured.

## Tech Stack
* **Python**: 3.11+ managed via `uv`.
* **Framework**: FastAPI.
* **Database**: PostgreSQL.
* **Cache & Session**: Redis.
* **Migrations**: Alembic.
* **LLM Clients**: Gemini, Ollama, and OpenAI-compatible providers.
* **Full Dependencies**: Check `pyproject.toml` for complete libraries and exact pinned versions.

## Repo Map
* `src/`: Core backend application code, domain modules (auth, chat, profile, session), and shared utilities.
* `base/`: Abstract base classes for repositories and schemas.
  * `clients/`: Database connectors (PostgreSQL, Redis) and LLM provider clients.
  * `core/`: Global application settings, configuration, and logging setup.
  * `db/`: Database session management, declarative models, and cache pools.
  * `dependencies/`: Injected FastAPI dependencies (e.g., current user, rate limiting).
  * `exceptions/`: Custom domain exceptions and global error handlers.
  * `middlewares/`: Request lifecycle interceptors like JWT validation.
  * `modules/`: Domain feature slices (authentication, chat, profile, session).
  * `shares/`: Shared application enums, constants, and shared types.
  * `utils/`: Reusable helpers, response formatting, and cache key utilities.
* `alembic/`: Database migration revision files, environment configuration, and data seeders.
* `tests/`: Unit and integration test suites.
* `docs/`: Technical documentation and `.http` API request files.
* `.agents/`: Agent operational workflows and system prompt instructions.

## Context map: read before you act
Detailed guidance lives in `.agents/`. Do not rely on memory or general
knowledge of a technology when a file here covers it. Load only what the
current task needs, not everything.

If skills prompt not found, follow the existing code pattern use of that skill.

* `.agents/system_flow/`: All system flow that defines how data process, project setups, and how system interacts with each other.
* `.agents/skills/`: (how to use each technology) One file per tech stack. Read these to understand **how we use a tool here**, including conventions and pitfalls.
 <!-- TODO: To add more as project goes larger. -->
