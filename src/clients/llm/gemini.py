"""Google Gemini client — remote LLM and embedding provider.

Uses the `google-genai` Python SDK (the modern unified SDK, not the
deprecated `google-generativeai` package).

Requires: GEMINI_API_KEY environment variable.

SDK docs: https://google-genai.readthedocs.io/
"""
import asyncio
from typing import AsyncGenerator, Dict, List, Optional

from google import genai
from google.genai import types
from loguru import logger

from clients.llm.base import EmbeddingClient, LLMClient
from core.settings import settings


class GeminiLLMClient(LLMClient):
    """LLM client for Google Gemini models using the modern google-genai SDK."""

    def __init__(self, api_key: Optional[str] = None):
        key = api_key or settings.GEMINI_API_KEY
        if not key:
            raise ValueError(
                "GEMINI_API_KEY is not set. Please add it to your .env file or "
                "run python setup.py to configure your credentials."
            )
        self.client = genai.Client(api_key=key)

    def _parse_messages(self, messages: List[Dict[str, str]]):
        """Extract system prompt and format remaining messages into Gemini Content objects."""
        system_instruction = None
        contents = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                system_instruction = content
            elif role in ("user", "human"):
                contents.append(types.Content(role="user", parts=[types.Part.from_text(text=content)]))
            elif role in ("assistant", "model", "ai"):
                contents.append(types.Content(role="model", parts=[types.Part.from_text(text=content)]))
        return system_instruction, contents

    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        target_model = model or settings.LLM_MODEL
        system_instruction, contents = self._parse_messages(messages)

        config_kwargs = {"temperature": temperature}
        if max_tokens:
            config_kwargs["max_output_tokens"] = max_tokens
        if system_instruction:
            config_kwargs["system_instruction"] = system_instruction

        config = types.GenerateContentConfig(**config_kwargs)

        try:
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=target_model,
                contents=contents,
                config=config,
            )
            return response.text or ""
        except Exception as err:
            logger.error(f"Gemini chat error: {err}")
            raise RuntimeError(f"Gemini API request failed: {err}") from err

    async def stream_chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> AsyncGenerator[str, None]:
        target_model = model or settings.LLM_MODEL
        system_instruction, contents = self._parse_messages(messages)

        config_kwargs = {"temperature": temperature}
        if max_tokens:
            config_kwargs["max_output_tokens"] = max_tokens
        if system_instruction:
            config_kwargs["system_instruction"] = system_instruction

        config = types.GenerateContentConfig(**config_kwargs)

        try:
            response_stream = await asyncio.to_thread(
                self.client.models.generate_content_stream,
                model=target_model,
                contents=contents,
                config=config,
            )
            for chunk in response_stream:
                if chunk.text:
                    yield chunk.text
        except Exception as err:
            logger.error(f"Gemini stream error: {err}")
            raise RuntimeError(f"Gemini streaming request failed: {err}") from err


class GeminiEmbeddingClient(EmbeddingClient):
    """Vector embedding client for Google Gemini models using the modern google-genai SDK."""

    def __init__(self, api_key: Optional[str] = None):
        key = api_key or settings.GEMINI_API_KEY
        if not key:
            raise ValueError(
                "GEMINI_API_KEY is not set. Please add it to your .env file or "
                "run python setup.py to configure your credentials."
            )
        self.client = genai.Client(api_key=key)

    async def embed_texts(
        self,
        texts: List[str],
        model: Optional[str] = None,
    ) -> List[List[float]]:
        target_model = model or settings.EMBEDDING_MODEL
        try:
            results = []
            for text in texts:
                response = await asyncio.to_thread(
                    self.client.models.embed_content,
                    model=target_model,
                    contents=text,
                )
                embedding = response.embedding.values
                results.append(list(embedding))
            return results
        except Exception as err:
            logger.error(f"Gemini embedding error: {err}")
            raise RuntimeError(f"Gemini embedding request failed: {err}") from err

    async def embed_query(
        self,
        text: str,
        model: Optional[str] = None,
    ) -> List[float]:
        embeddings = await self.embed_texts([text], model=model)
        if not embeddings:
            raise RuntimeError("Gemini returned empty embedding response.")
        return embeddings[0]
