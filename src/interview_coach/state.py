"""LangGraph state definitions for the Interview Coach."""

from __future__ import annotations

from typing import Annotated, Literal
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class InterviewState(TypedDict):
    """Main state for the interview workflow graph.

    Attributes:
        messages: Conversation history (auto-appended via add_messages reducer).
        domain: The interview topic domain (e.g. "python", "machine_learning").
        difficulty: Current difficulty level.
        current_question_number: Which question we're on (1-indexed).
        max_questions: Total questions in the session.
        questions_asked: List of questions already asked.
        scores: List of scores for each answer (0-10).
        feedback_history: List of feedback for each answer.
        phase: Current phase of the interview workflow.
        is_complete: Whether the interview session has ended.
    """

    messages: Annotated[list[BaseMessage], add_messages]
    domain: str
    difficulty: str
    current_question_number: int
    max_questions: int
    questions_asked: list[str]
    scores: list[int]
    feedback_history: list[str]
    phase: Literal[
        "greeting",
        "ask_question",
        "evaluate_answer",
        "give_feedback",
        "wrap_up",
    ]
    is_complete: bool
    api_key: str  # API key for the chosen provider (passed at runtime)
    model_id: str  # Model ID / name to use (e.g. "meta-llama/llama-4-maverick:free")
    provider: str  # LLM provider — "openrouter" or "groq"
