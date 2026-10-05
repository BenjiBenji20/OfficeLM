# OfficeLM Setup & Lifecycle Pipeline
`v1.0`

> **Core Philosophy**: **Docker is the ONLY prerequisite.** The user does not need Python, uv, pip, Git, or compilers installed on their host machine.

---

## 1. End-to-End Architecture Flow

```mermaid
flowchart TD
    subgraph Step1["1. Single Prerequisite: Docker"]
        A["User has Docker Desktop / Engine installed"] --> B["Run in empty folder:<br/><code>docker run -it --rm -v '${PWD}:/workspace' ghcr.io/benjibenji20/officelm:latest init</code>"]
    end

    subgraph Step2["2. Interactive Containerized Wizard"]
        B --> C["Docker pulls image & executes Wizard in interactive TTY"]
        C --> D{"Interactive CLI Prompts"}
        D -->|Local| E1["Pick Curated Ollama Model"]
        D -->|Remote| E2["Select OpenAI / Gemini + Enter API Key"]
        E1 --> F["Enter / Auto-generate Superadmin Account"]
        E2 --> F
        F --> G["Container ejects <code>docker-compose.yml</code>, <code>secrets.env</code>, and <code>.env</code> into host folder"]
    end

    subgraph Step3["3. Variable Splitting Architecture"]
        G --> H1["Dynamic .env<br/>• Generated Passwords & Tokens<br/>• User Model & Provider Selection<br/>• DB/Redis Passwords"]
        G --> H2["Static secrets.env<br/>• API Docs Endpoints (/docs, /redoc)<br/>• JWT Algorithms & Token Expiry<br/>• Cookie & Security Headers"]
    end

    subgraph Step4["4. One-Command Launch"]
        H1 --> I["docker compose up -d"]
        H2 --> I
        I --> J["Postgres & Redis Containers Start (Healthy)"]
        J --> K["API Entrypoint runs Alembic Migrations via asyncpg"]
        K --> L["FastAPI Server Live on http://localhost:8000"]
    end

    subgraph Step5["5. Next Flow (Application & Chat Execution)"]
        L --> M["User Accesses Web / API Client"]
        M --> N["Authenticate Superadmin / User (JWT)"]
        N --> O["Select / Create Chatroom"]
        O --> P["LLM Factory (get_llm_client) Routes to Active Provider"]
        P --> Q["Chat Stream & Async Document Generation (FileJob)"]
    end

    Step1 --> Step2
    Step2 --> Step3
    Step3 --> Step4
    Step4 --> Step5
```
---

## Connection to Next Flow (Application & Chat Engine)
1. **Authentication**: Users authenticate against `POST /auth/login` using the initial admin or registered accounts, obtaining JWT access & refresh tokens.
2. **Chatroom Management**: Users create or re-enter chatrooms (`chat.chat_rooms`).
3. **Provider-Agnostic LLM Routing**: Application services call `get_llm_client()` / `get_embedding_client()`. The factory reads `LLM_PROVIDER` from `.env` and serves streaming chat responses or vector embeddings without importing concrete provider SDKs.
4. **Document Generation**: Messages triggering document creation spawn asynchronous `FileJob` tasks for formatting and exporting Markdown, Word, Excel, and PDF files.
