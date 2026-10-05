"""Model registry for OfficeLM.

Defines the curated, tested set of chat and embedding models that OfficeLM
supports. Any model added here must be explicitly validated against
OfficeLM's chat and document-generation workflows before release.

Provider mapping rules:
- OLLAMA  → runs locally via the Ollama container
- OPENAI  → calls the OpenAI REST API (or any OpenAI-compatible endpoint)
- GEMINI  → calls the Google Gemini API via the google-genai SDK
"""
from enum import Enum


# ─── Chat Models ─────────────────────────────────────────────────────────────

class SupportedChatModel(str, Enum):
    """Curated chat models supported by OfficeLM."""

    # ── Local (Ollama) ─────────────────────────────────────────────────────
    # Small / medium models that run reliably on consumer hardware (8-16 GB RAM).
    # All have been verified to follow plain-text / Markdown formatting instructions.
    LLAMA3_8B   = "llama3.1:8b"    # ~4.7 GB  — strong general-purpose default
    MISTRAL_7B  = "mistral:7b"     # ~4.1 GB  — fast, instruction-tuned
    PHI3_MINI   = "phi3:mini"      # ~2.3 GB  — Microsoft, smallest footprint

    # ── Remote (OpenAI API) ────────────────────────────────────────────────
    GPT4O_MINI  = "gpt-4o-mini"    # Cost-effective, fast, 128 k context
    GPT4O       = "gpt-4o"         # Flagship quality

    # ── Remote (Google Gemini) ─────────────────────────────────────────────
    GEMINI_38_FLASH      = "gemini-3.8-flash"       # Latest flagship Flash (GA Sep 2026)
    GEMINI_35_FLASH_LITE = "gemini-3.5-flash-lite"  # Cost-effective, high-volume


# ─── Embedding Models ─────────────────────────────────────────────────────────

class SupportedEmbeddingModel(str, Enum):
    """Curated embedding models supported by OfficeLM."""

    # ── Local (Ollama) ─────────────────────────────────────────────────────
    NOMIC_EMBED_TEXT = "nomic-embed-text"  # ~0.3 GB, 8192-token ctx, community default

    # ── Remote (OpenAI API) ────────────────────────────────────────────────
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"  # 1536-dim, cheap & good
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"  # 3072-dim, highest quality

    # ── Remote (Google Gemini) ─────────────────────────────────────────────
    GEMINI_EMBEDDING = "text-embedding-004"  # 768-dim, strong multilingual


# ─── Provider Mapping ─────────────────────────────────────────────────────────

class ModelProvider(str, Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"
    GEMINI = "gemini"


CHAT_MODEL_PROVIDER_MAP: dict[SupportedChatModel, ModelProvider] = {
    SupportedChatModel.LLAMA3_8B:          ModelProvider.OLLAMA,
    SupportedChatModel.MISTRAL_7B:         ModelProvider.OLLAMA,
    SupportedChatModel.PHI3_MINI:          ModelProvider.OLLAMA,
    SupportedChatModel.GPT4O_MINI:         ModelProvider.OPENAI,
    SupportedChatModel.GPT4O:              ModelProvider.OPENAI,
    SupportedChatModel.GEMINI_38_FLASH:    ModelProvider.GEMINI,
    SupportedChatModel.GEMINI_35_FLASH_LITE: ModelProvider.GEMINI,
}

EMBEDDING_MODEL_PROVIDER_MAP: dict[SupportedEmbeddingModel, ModelProvider] = {
    SupportedEmbeddingModel.NOMIC_EMBED_TEXT:       ModelProvider.OLLAMA,
    SupportedEmbeddingModel.TEXT_EMBEDDING_3_SMALL: ModelProvider.OPENAI,
    SupportedEmbeddingModel.TEXT_EMBEDDING_3_LARGE: ModelProvider.OPENAI,
    SupportedEmbeddingModel.GEMINI_EMBEDDING:       ModelProvider.GEMINI,
}


# ─── Metadata (used by setup CLI to show human-readable descriptions) ─────────

CHAT_MODEL_METADATA: dict[SupportedChatModel, dict] = {
    SupportedChatModel.LLAMA3_8B:   {"size": "~4.7 GB", "provider": "Ollama (local)", "notes": "General-purpose, recommended default"},
    SupportedChatModel.MISTRAL_7B:  {"size": "~4.1 GB", "provider": "Ollama (local)", "notes": "Fast, strong instruction following"},
    SupportedChatModel.PHI3_MINI:   {"size": "~2.3 GB", "provider": "Ollama (local)", "notes": "Smallest footprint, good for low-RAM machines"},
    SupportedChatModel.GPT4O_MINI:  {"size": "API",     "provider": "OpenAI",          "notes": "Cost-effective, fast, 128k context"},
    SupportedChatModel.GPT4O:       {"size": "API",     "provider": "OpenAI",          "notes": "Flagship quality"},
    SupportedChatModel.GEMINI_38_FLASH:      {"size": "API", "provider": "Google Gemini", "notes": "Latest GA Flash model (Sep 2026)"},
    SupportedChatModel.GEMINI_35_FLASH_LITE: {"size": "API", "provider": "Google Gemini", "notes": "High-volume, cost-effective"},
}
