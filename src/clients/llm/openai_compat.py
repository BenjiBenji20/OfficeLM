"""OpenAI-compatible client — remote LLM and embedding provider.

Uses the `openai` Python SDK which works with the official OpenAI API and
any compatible endpoint (Groq, Together, Mistral, Azure OpenAI, etc.).
The base URL is configurable via `settings.OPENAI_BASE_URL`.
"""
from typing import AsyncGenerator, Dict, List, Optional

from loguru import logger
from openai import AsyncOpenAI

from clients.llm.base import EmbeddingClient, LLMClient
from core.settings import settings


class OpenAICompatLLMClient(LLMClient):
    """LLM client for OpenAI and OpenAI-compatible providers."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        key = api_key or settings.OPENAI_API_KEY
        url = base_url or settings.OPENAI_BASE_URL
        if not key:
            raise ValueError(
                "OPENAI_API_KEY is not set. Please add it to your .env file or "
                "run python setup.py to configure your credentials."
            )
        self.client = AsyncOpenAI(api_key=key, base_url=url)

    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        target_model = model or settings.LLM_MODEL
        try:
            kwargs = {
                "model": target_model,
                "messages": messages,
                "temperature": temperature,
            }
            if max_tokens:
                kwargs["max_tokens"] = max_tokens

            response = await self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.content or ""
        except Exception as err:
            logger.error(f"OpenAI chat error: {err}")
            raise RuntimeError(f"OpenAI API request failed: {err}") from err

    async def stream_chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> AsyncGenerator[str, None]:
        target_model = model or settings.LLM_MODEL
        try:
            kwargs = {
                "model": target_model,
                "messages": messages,
                "temperature": temperature,
                "stream": True,
            }
            if max_tokens:
                kwargs["max_tokens"] = max_tokens

            stream = await self.client.chat.completions.create(**kwargs)
            async for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    yield delta
        except Exception as err:
            logger.error(f"OpenAI stream error: {err}")
            raise RuntimeError(f"OpenAI streaming request failed: {err}") from err


class OpenAICompatEmbeddingClient(EmbeddingClient):
    """Vector embedding client for OpenAI and OpenAI-compatible providers."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        key = api_key or settings.OPENAI_API_KEY
        url = base_url or settings.OPENAI_BASE_URL
        if not key:
            raise ValueError(
                "OPENAI_API_KEY is not set. Please add it to your .env file or "
                "run python setup.py to configure your credentials."
            )
        self.client = AsyncOpenAI(api_key=key, base_url=url)

    async def embed_texts(
        self,
        texts: List[str],
        model: Optional[str] = None,
    ) -> List[List[float]]:
        target_model = model or settings.EMBEDDING_MODEL
        try:
            response = await self.client.embeddings.create(
                model=target_model,
                input=texts,
            )
            return [data.embedding for data in response.data]
        except Exception as err:
            logger.error(f"OpenAI embedding error: {err}")
            raise RuntimeError(f"OpenAI embedding request failed: {err}") from err

    async def embed_query(
        self,
        text: str,
        model: Optional[str] = None,
    ) -> List[float]:
        embeddings = await self.embed_texts([text], model=model)
        if not embeddings:
            raise RuntimeError("OpenAI returned empty embedding response.")
        return embeddings[0]
