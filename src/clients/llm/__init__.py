"""LLM client package for OfficeLM.

Exports the provider-agnostic factory function `get_llm_client` and
`get_embedding_client` so the rest of the application never imports a
concrete provider directly.
"""
from clients.llm.factory import get_embedding_client, get_llm_client

__all__ = ["get_llm_client", "get_embedding_client"]
