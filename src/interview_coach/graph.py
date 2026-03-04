"""LangGraph workflow definition for the AI Interview Coach.

The interview flows through these phases:

    START ──► router
                │
                ├── phase="greeting"          ──► greeting ──► ask_question ──► END
                ├── phase="evaluate_answer"   ──► evaluate_answer ──► END (pause)
                ├── phase="ask_question"      ──► ask_question ──► END
                └── phase="wrap_up"           ──► wrap_up ──► END

After evaluate_answer, the app reads the updated phase and auto-triggers
the next invocation (ask_question or wrap_up) so that feedback and the
next question appear as separate chat messages.
"""

from __future__ import annotations

from typing import Literal

from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import InMemorySaver

from interview_coach.state import InterviewState
from interview_coach.nodes import (
    greeting_node,
    ask_question_node,
    evaluate_answer_node,
    wrap_up_node,
)


# ── Routing functions ───────────────────────────────────────────────────────


def _route_entry(state: InterviewState) -> Literal["greeting", "evaluate_answer", "ask_question", "wrap_up"]:
    """Route from START based on the current phase."""
    phase = state.get("phase", "greeting")
    if phase == "greeting":
        return "greeting"
    if phase == "evaluate_answer":
        return "evaluate_answer"
    if phase == "wrap_up":
        return "wrap_up"
    return "ask_question"


def build_interview_graph() -> StateGraph:
    """Construct and compile the interview coach LangGraph workflow.

    Returns:
        A compiled LangGraph ``StateGraph`` ready for ``.invoke()`` / ``.stream()``.
    """
    builder = StateGraph(InterviewState)

    # ── Register nodes ──────────────────────────────────────────────────
    builder.add_node("greeting", greeting_node)
    builder.add_node("ask_question", ask_question_node)
    builder.add_node("evaluate_answer", evaluate_answer_node)
    builder.add_node("wrap_up", wrap_up_node)

    # ── Define edges ────────────────────────────────────────────────────

    # Entry: router checks `phase` and sends to the right node
    builder.add_conditional_edges(
        START,
        _route_entry,
        {
            "greeting": "greeting",
            "evaluate_answer": "evaluate_answer",
            "ask_question": "ask_question",
            "wrap_up": "wrap_up",
        },
    )

    # greeting → ask first question → pause (END)
    builder.add_edge("greeting", "ask_question")
    builder.add_edge("ask_question", END)

    # evaluate_answer → pause (END) — app will auto-trigger next step
    builder.add_edge("evaluate_answer", END)

    builder.add_edge("wrap_up", END)

    # ── Compile with memory checkpointer ────────────────────────────────
    memory = InMemorySaver()
    graph = builder.compile(checkpointer=memory)

    return graph


def get_initial_state(
    domain: str = "python",
    difficulty: str = "medium",
    max_questions: int = 5,
    api_key: str = "",
    model_id: str = "",
    provider: str = "openrouter",
) -> dict:
    """Return the initial state dict to kick off an interview session.

    Args:
        domain: Interview topic domain.
        difficulty: easy / medium / hard.
        max_questions: Total questions in the session.
        api_key: API key for the chosen provider (overrides .env if provided).
        model_id: Model ID to use (overrides default if provided).
        provider: LLM provider — 'openrouter' or 'groq'.
    """
    return {
        "messages": [],
        "domain": domain,
        "difficulty": difficulty,
        "current_question_number": 1,
        "max_questions": max_questions,
        "questions_asked": [],
        "scores": [],
        "feedback_history": [],
        "phase": "greeting",
        "is_complete": False,
        "api_key": api_key,
        "model_id": model_id,
        "provider": provider,
    }
