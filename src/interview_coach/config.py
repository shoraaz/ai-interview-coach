"""Configuration and settings for the AI Interview Coach."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class ModelConfig:
    """OpenRouter model configuration."""

    # Free models available on OpenRouter (as of 2025)
    # See https://openrouter.ai/models?q=free for latest free models
    model_name: str = "meta-llama/llama-4-maverick:free"
    base_url: str = "https://openrouter.ai/api/v1"
    api_key: str = field(default_factory=lambda: os.getenv("OPENROUTER_API_KEY", ""))
    temperature: float = 0.7
    max_tokens: int = 2048

    # Alternative free models you can try:
    # "meta-llama/llama-4-maverick:free"
    # "meta-llama/llama-4-scout:free"
    # "google/gemma-3-27b-it:free"
    # "mistralai/mistral-small-3.1-24b-instruct:free"
    # "qwen/qwen3-235b-a22b:free"


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


def get_model_config(
    api_key: str | None = None,
    model_id: str | None = None,
) -> ModelConfig:
    """Get the model configuration.

    Args:
        api_key: Optional override for the OpenRouter API key.
                 If provided, takes precedence over the env var.
        model_id: Optional override for the model name/ID.
                  If provided, takes precedence over the default.
    """
    overrides: dict = {}
    if api_key:
        overrides["api_key"] = api_key
    if model_id:
        overrides["model_name"] = model_id
    if overrides:
        return ModelConfig(**overrides)
    return ModelConfig()


def get_interview_config() -> InterviewConfig:
    """Get the interview config."""
    return InterviewConfig()
