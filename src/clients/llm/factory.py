"""Factory functions for LLM and Embedding clients.

Usage (anywhere in the app):

    from clients.llm.factory import get_llm_client, get_embedding_client

    llm = get_llm_client()
    reply = await llm.chat(messages, model=settings.LLM_MODEL)

The factory reads `settings.LLM_PROVIDER` and returns the appropriate client
singleton. Switching providers is as simple as changing `LLM_PROVIDER` in `.env`.
"""
from functools import lru_cache

from clients.llm.base import EmbeddingClient, LLMClient
from clients.llm.gemini import GeminiEmbeddingClient, GeminiLLMClient
from clients.llm.ollama import OllamaEmbeddingClient, OllamaLLMClient
from clients.llm.openai_compat import OpenAICompatEmbeddingClient, OpenAICompatLLMClient
from core.settings import settings


@lru_cache()
def get_llm_client() -> LLMClient:
    """Return an LLMClient instance based on `settings.LLM_PROVIDER`."""
    provider = settings.LLM_PROVIDER.lower()
    if provider == "ollama":
        return OllamaLLMClient()
    elif provider == "openai":
        return OpenAICompatLLMClient()
    elif provider == "gemini":
        return GeminiLLMClient()
    else:
        raise ValueError(
            f"Unsupported LLM provider: '{settings.LLM_PROVIDER}'. "
            "Supported values: 'ollama', 'openai', 'gemini'."
        )


@lru_cache()
def get_embedding_client() -> EmbeddingClient:
    """Return an EmbeddingClient instance based on `settings.LLM_PROVIDER`."""
    provider = settings.LLM_PROVIDER.lower()
    if provider == "ollama":
        return OllamaEmbeddingClient()
    elif provider == "openai":
        return OpenAICompatEmbeddingClient()
    elif provider == "gemini":
        return GeminiEmbeddingClient()
    else:
        raise ValueError(
            f"Unsupported LLM provider: '{settings.LLM_PROVIDER}'. "
            "Supported values: 'ollama', 'openai', 'gemini'."
        )
