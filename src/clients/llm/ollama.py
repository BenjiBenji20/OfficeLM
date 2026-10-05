"""Ollama client — local LLM and embedding provider.

Communicates with the Ollama HTTP API running inside the `ollama` Docker
service on the internal compose network. Requires no API key.

Docs: https://github.com/ollama/ollama/blob/main/docs/api.md
"""
from typing import AsyncGenerator, Dict, List, Optional

import httpx
from loguru import logger

from clients.llm.base import EmbeddingClient, LLMClient
from core.settings import settings


class OllamaLLMClient(LLMClient):
    """Local LLM client using Ollama's HTTP API."""

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = (base_url or settings.OLLAMA_BASE_URL).rstrip("/")

    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        target_model = model or settings.LLM_MODEL
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": target_model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature},
        }
        if max_tokens:
            payload["options"]["num_predict"] = max_tokens

        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get("message", {}).get("content", "")
            except httpx.HTTPError as err:
                logger.error(f"Ollama chat error: {err}")
                raise RuntimeError(f"Ollama API request failed: {err}") from err

    async def stream_chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> AsyncGenerator[str, None]:
        target_model = model or settings.LLM_MODEL
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": target_model,
            "messages": messages,
            "stream": True,
            "options": {"temperature": temperature},
        }
        if max_tokens:
            payload["options"]["num_predict"] = max_tokens

        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                async with client.stream("POST", url, json=payload) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if not line:
                            continue
                        import json
                        chunk = json.loads(line)
                        content = chunk.get("message", {}).get("content", "")
                        if content:
                            yield content
            except httpx.HTTPError as err:
                logger.error(f"Ollama stream error: {err}")
                raise RuntimeError(f"Ollama streaming API request failed: {err}") from err


class OllamaEmbeddingClient(EmbeddingClient):
    """Local vector embedding client using Ollama's embeddings API."""

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = (base_url or settings.OLLAMA_BASE_URL).rstrip("/")

    async def embed_texts(
        self,
        texts: List[str],
        model: Optional[str] = None,
    ) -> List[List[float]]:
        target_model = model or settings.EMBEDDING_MODEL
        url = f"{self.base_url}/api/embed"
        payload = {
            "model": target_model,
            "input": texts,
        }
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get("embeddings", [])
            except httpx.HTTPError as err:
                logger.error(f"Ollama batch embedding error: {err}")
                raise RuntimeError(f"Ollama embedding request failed: {err}") from err

    async def embed_query(
        self,
        text: str,
        model: Optional[str] = None,
    ) -> List[float]:
        embeddings = await self.embed_texts([text], model=model)
        if not embeddings:
            raise RuntimeError("Ollama returned empty embedding response.")
        return embeddings[0]
