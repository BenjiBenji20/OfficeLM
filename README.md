# OfficeLM

OfficeLM is a multi-user, multi-room chat AI companion for office environments — a self-hostable, NotebookLM-style tool. It runs as a private server (Windows-first, cross-platform capable), lets teams collectively query ingested corporate documents (RAG), and generates real office files (.md now (for demo)) from chat requests.

## Quick Start

> **Prerequisites**: [Docker](https://www.docker.com/) & Docker Compose installed. No Python, Git, or compilers required.

### 1. Initialize Configuration
In an empty directory, run the initialization command:

```bash
docker run -it --rm -v "${PWD}:/workspace" ghcr.io/benjibenji20/officelm:latest init
```
Follow the interactive setup wizard in your terminal to configure your environment.

### 2. Launch
```bash
docker compose up -d
```
Access the service at `http://localhost:8000` (API & Swagger Docs at `/docs`).
