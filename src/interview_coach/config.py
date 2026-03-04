"""Configuration and settings for the AI Interview Coach."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


# ── Provider base URLs ───────────────────────────────────────────────────────

PROVIDER_BASE_URLS: dict[str, str] = {
    "openrouter": "https://openrouter.ai/api/v1",
    "groq": "https://api.groq.com/openai/v1",
}

PROVIDER_DEFAULT_MODELS: dict[str, str] = {
    "openrouter": "meta-llama/llama-4-maverick:free",
    "groq": "llama-3.3-70b-versatile",
}


@dataclass(frozen=True)
class ModelConfig:
    """LLM provider model configuration."""

    model_name: str = "meta-llama/llama-4-maverick:free"
    base_url: str = "https://openrouter.ai/api/v1"
    api_key: str = field(default_factory=lambda: os.getenv("OPENROUTER_API_KEY", ""))
    temperature: float = 0.7
    max_tokens: int = 2048
    provider: str = "openrouter"


@dataclass(frozen=True)
class InterviewConfig:
    """Interview session configuration."""

    max_questions: int = 10
    difficulty_levels: tuple[str, ...] = ("easy", "medium", "hard")
    default_difficulty: str = "medium"


# Available interview domains with descriptions
INTERVIEW_DOMAINS: dict[str, str] = {
    "python": "Python Programming - Core concepts, data structures, OOP, decorators, generators",
    "machine_learning": "Machine Learning - Algorithms, model evaluation, feature engineering, bias-variance",
    "deep_learning": "Deep Learning - Neural networks, CNNs, RNNs, transformers, training techniques",
    "data_science": "Data Science - Statistics, EDA, visualization, feature selection, A/B testing",
    "system_design": "System Design - Scalability, databases, caching, load balancing, microservices",
    "sql": "SQL & Databases - Queries, joins, indexing, normalization, window functions",
    "nlp": "Natural Language Processing - Tokenization, embeddings, attention, LLMs, RAG",
    "mlops": "MLOps - Model deployment, CI/CD, monitoring, versioning, containerization",
    "generative_ai": "Generative AI - LLMs, prompt engineering, RAG, fine-tuning, agents",
    "dsa": "Data Structures & Algorithms - Arrays, trees, graphs, dynamic programming, sorting",
}


# Free models available on OpenRouter
FREE_MODELS: dict[str, str] = {
    "meta-llama/llama-4-maverick:free": "Llama 4 Maverick (Meta)",
    "meta-llama/llama-4-scout:free": "Llama 4 Scout (Meta)",
    "google/gemma-3-27b-it:free": "Gemma 3 27B (Google)",
    "mistralai/mistral-small-3.1-24b-instruct:free": "Mistral Small 3.1 24B",
    "qwen/qwen3-235b-a22b:free": "Qwen 3 235B (Alibaba)",
    "deepseek/deepseek-chat-v3-0324:free": "DeepSeek Chat V3",
    "google/gemini-2.0-flash-exp:free": "Gemini 2.0 Flash (Google)",
}

# Models available on Groq (fast inference)
GROQ_MODELS: dict[str, str] = {
    "llama-3.3-70b-versatile": "Llama 3.3 70B Versatile",
    "llama-3.1-8b-instant": "Llama 3.1 8B Instant",
    "llama3-70b-8192": "Llama 3 70B",
    "llama3-8b-8192": "Llama 3 8B",
    "gemma2-9b-it": "Gemma 2 9B (Google)",
    "mixtral-8x7b-32768": "Mixtral 8x7B (Mistral)",
    "qwen-qwq-32b": "Qwen QWQ 32B",
}


def get_model_config(
    api_key: str | None = None,
    model_id: str | None = None,
    provider: str = "openrouter",
) -> ModelConfig:
    """Get the model configuration.

    Args:
        api_key: Optional override for the API key.
                 If provided, takes precedence over the env var.
        model_id: Optional override for the model name/ID.
                  If provided, takes precedence over the default.
        provider: LLM provider — 'openrouter' or 'groq'.
    """
    base_url = PROVIDER_BASE_URLS.get(provider, PROVIDER_BASE_URLS["openrouter"])
    default_model = PROVIDER_DEFAULT_MODELS.get(provider, PROVIDER_DEFAULT_MODELS["openrouter"])

    # Choose env-var fallback based on provider
    if provider == "groq":
        env_key = os.getenv("GROQ_API_KEY", "")
    else:
        env_key = os.getenv("OPENROUTER_API_KEY", "")

    return ModelConfig(
        model_name=model_id if model_id else default_model,
        base_url=base_url,
        api_key=api_key if api_key else env_key,
        provider=provider,
    )


def get_interview_config() -> InterviewConfig:
    """Get the interview config."""
    return InterviewConfig()
