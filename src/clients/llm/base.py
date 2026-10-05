"""Abstract base classes for OfficeLM LLM and Embedding clients.

All concrete provider implementations must satisfy these protocols so that
the rest of the application is fully provider-agnostic.
"""
from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, List, Optional


class LLMClient(ABC):
    """Abstract interface for LLM text generation and chat capabilities."""

    @abstractmethod
    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Generate a single complete response from a conversation thread."""
        pass

    @abstractmethod
    async def stream_chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> AsyncGenerator[str, None]:
        """Stream chunks of response text from a conversation thread as they are generated."""
        pass


class EmbeddingClient(ABC):
    """Abstract interface for vector embedding generation."""

    @abstractmethod
    async def embed_texts(
        self,
        texts: List[str],
        model: Optional[str] = None,
    ) -> List[List[float]]:
        """Generate vector embeddings for a list of text strings."""
        pass

    @abstractmethod
    async def embed_query(
        self,
        text: str,
        model: Optional[str] = None,
    ) -> List[float]:
        """Generate a vector embedding for a single search query string."""
        pass
