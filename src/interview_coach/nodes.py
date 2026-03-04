"""LangGraph node functions for the Interview Coach workflow."""

from __future__ import annotations

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage

from interview_coach.config import get_model_config, INTERVIEW_DOMAINS
from interview_coach.state import InterviewState
from interview_coach.prompts import (
    build_greeting_prompt,
    build_question_prompt,
    build_evaluator_prompt,
    build_wrap_up_prompt,
)
from interview_coach.utils import parse_evaluation, compute_average_score


def _get_llm(api_key: str | None = None, model_id: str | None = None, provider: str = "openrouter") -> ChatOpenAI:
    """Instantiate an LLM backed by the chosen provider (OpenRouter or Groq).

    Args:
        api_key: Optional API key override (e.g. from UI input).
        model_id: Optional model ID override (e.g. from UI dropdown).
        provider: LLM provider — 'openrouter' or 'groq'.
    """
    cfg = get_model_config(api_key=api_key, model_id=model_id, provider=provider)
    return ChatOpenAI(
        model=cfg.model_name,
        openai_api_key=cfg.api_key,
        openai_api_base=cfg.base_url,
        temperature=cfg.temperature,
        max_tokens=cfg.max_tokens,
    )


# ── Node: greeting ──────────────────────────────────────────────────────────


def greeting_node(state: InterviewState) -> dict:
    """Welcome the candidate and set up the interview session."""
    llm = _get_llm(api_key=state.get("api_key"), model_id=state.get("model_id"), provider=state.get("provider", "openrouter"))
    domain_label = INTERVIEW_DOMAINS.get(state["domain"], state["domain"])
    prompt = build_greeting_prompt()
    chain = prompt | llm

    response = chain.invoke(
        {
            "domain": domain_label,
            "difficulty": state["difficulty"],
            "max_questions": state["max_questions"],
        }
    )

    return {
        "messages": [AIMessage(content=response.content)],
        "phase": "ask_question",
    }


# ── Node: ask_question ──────────────────────────────────────────────────────


def ask_question_node(state: InterviewState) -> dict:
    """Generate the next interview question."""
    llm = _get_llm(api_key=state.get("api_key"), model_id=state.get("model_id"), provider=state.get("provider", "openrouter"))
    domain_label = INTERVIEW_DOMAINS.get(state["domain"], state["domain"])
    prompt = build_question_prompt()
    chain = prompt | llm

    response = chain.invoke(
        {
            "domain": domain_label,
            "difficulty": state["difficulty"],
            "current_question_number": state["current_question_number"],
            "max_questions": state["max_questions"],
            "questions_asked": "\n".join(state["questions_asked"]) or "None yet",
        }
    )

    question_text = response.content.strip()
    updated_questions = state["questions_asked"] + [question_text]

    return {
        "messages": [AIMessage(content=question_text)],
        "questions_asked": updated_questions,
        "phase": "evaluate_answer",
    }


# ── Node: evaluate_answer ───────────────────────────────────────────────────


def evaluate_answer_node(state: InterviewState) -> dict:
    """Evaluate the candidate's most recent answer."""
    llm = _get_llm(api_key=state.get("api_key"), model_id=state.get("model_id"), provider=state.get("provider", "openrouter"))
    prompt = build_evaluator_prompt()
    chain = prompt | llm

    # The last AI message is the question; the last Human message is the answer
    last_question = ""
    last_answer = ""
    for msg in reversed(state["messages"]):
        if isinstance(msg, HumanMessage) and not last_answer:
            last_answer = msg.content
        if isinstance(msg, AIMessage) and not last_question:
            last_question = msg.content
        if last_question and last_answer:
            break

    response = chain.invoke(
        {
            "question": last_question,
            "answer": last_answer,
        }
    )

    score, feedback, ideal_answer = parse_evaluation(response.content)

    # Build feedback message
    feedback_msg = f"**Score: {score}/10**\n\n"
    feedback_msg += f"**Feedback:** {feedback}\n\n"
    if ideal_answer:
        feedback_msg += f"**Ideal Answer:** {ideal_answer}"

    updated_scores = state["scores"] + [score]
    updated_feedback = state["feedback_history"] + [feedback]
    next_q = state["current_question_number"] + 1

    # Determine next phase
    if next_q > state["max_questions"]:
        next_phase = "wrap_up"
        is_complete = True
    else:
        next_phase = "ask_question"
        is_complete = False

    return {
        "messages": [AIMessage(content=feedback_msg)],
        "scores": updated_scores,
        "feedback_history": updated_feedback,
        "current_question_number": next_q,
        "phase": next_phase,
        "is_complete": is_complete,
    }


# ── Node: wrap_up ───────────────────────────────────────────────────────────


def wrap_up_node(state: InterviewState) -> dict:
    """Summarise the interview and give final feedback."""
    llm = _get_llm(api_key=state.get("api_key"), model_id=state.get("model_id"), provider=state.get("provider", "openrouter"))
    domain_label = INTERVIEW_DOMAINS.get(state["domain"], state["domain"])
    avg = compute_average_score(state["scores"])
    prompt = build_wrap_up_prompt()
    chain = prompt | llm

    response = chain.invoke(
        {
            "domain": domain_label,
            "difficulty": state["difficulty"],
            "current_question_number": state["current_question_number"] - 1,
            "scores": state["scores"],
            "avg_score": avg,
        }
    )

    return {
        "messages": [AIMessage(content=response.content)],
        "phase": "wrap_up",
        "is_complete": True,
    }
