# OfficeLM — Getting Started

> **Only prerequisite: [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed.**

---

## Quick Start (3 commands)

```bash
# 1. Clone the repo
git clone https://github.com/BenjiBenji20/OfficeLM.git
cd OfficeLM/server

# 2. Run the setup wizard — answers 5 questions, generates .env
python setup.py

# 3a. Local AI mode (Ollama) — default
docker compose --profile local-llm up -d

# 3b. Remote AI mode (OpenAI / Gemini) — if you selected a remote provider
docker compose up -d
```

Then open **http://localhost:8000/docs** to see the API.

---

## What the Setup Wizard Does

`python setup.py` walks you through 5 steps:

| Step | Question | What it configures |
|------|----------|--------------------|
| 1 | Local (Ollama) or Remote (OpenAI / Gemini)? | `LLM_PROVIDER`, `EMBEDDING_PROVIDER` |
| 2 | Which AI model? | `LLM_MODEL`, `EMBEDDING_MODEL` |
| 3 | API key (remote) or GPU opt-in (local) | `OPENAI_API_KEY` / `GEMINI_API_KEY` |
| 4 | Admin username / email / password | `SEED_SUPERADMIN_*` |
| 5 | Confirm → generates `.env` | All secrets auto-generated |

All JWT secrets, DB passwords, Redis passwords, and MinIO passwords are
**auto-generated with `secrets.token_hex()`** — no hardcoded defaults in production.

---

## Supported AI Models

### Local (Ollama — free, no API key required)

| Model | Size | Notes |
|-------|------|-------|
| `llama3.1:8b` | ~4.7 GB | General-purpose — recommended default |
| `mistral:7b` | ~4.1 GB | Fast, strong instruction following |
| `phi3:mini` | ~2.3 GB | Smallest footprint, good for low-RAM machines |

**Embedding:** `nomic-embed-text` (~0.3 GB) — auto-pulled alongside the chat model.

### Remote (OpenAI API)

| Model | Notes |
|-------|-------|
| `gpt-4o-mini` | Cost-effective, 128k context — recommended |
| `gpt-4o` | Flagship quality |

**Embedding:** `text-embedding-3-small`

### Remote (Google Gemini)

| Model | Notes |
|-------|-------|
| `gemini-3.8-flash` | Latest GA Flash (Sep 2026) — recommended |
| `gemini-3.5-flash-lite` | High-volume, cost-effective |

**Embedding:** `text-embedding-004`

---

## GPU Acceleration (Optional)

If you have an NVIDIA GPU and [`nvidia-container-toolkit`](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) installed,
the setup wizard will ask if you want to enable GPU acceleration for Ollama.

To enable manually, uncomment the `deploy` block in [docker-compose.yml](docker-compose.yml) under the `ollama` service.

---

## Services & Ports

| Service | Port | Notes |
|---------|------|-------|
| **API** | `8000` | FastAPI server — `http://localhost:8000` |
| **PostgreSQL** | `5432` | Database |
| **Redis** | `6379` | Cache / session store |
| **MinIO (S3)** | `9000` | Object storage API |
| **MinIO Console** | `9001` | Web UI → `http://localhost:9001` |
| **Ollama** | `11434` | Local LLM API (local-llm profile only) |

---

## First Boot (Local Mode)

On the very first `docker compose up`, the API container will:

1. Run Alembic database migrations
2. Wait for Ollama to be ready
3. Auto-pull the configured chat model (e.g., `llama3.1:8b` — ~4.7 GB)
4. Auto-pull the embedding model (`nomic-embed-text` — ~0.3 GB)
5. Start the FastAPI server

**This takes a few minutes on first boot** depending on your internet speed.
Subsequent restarts are instant because models are cached in the `ollamadata` Docker volume.
