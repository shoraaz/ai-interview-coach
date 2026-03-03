"""Utility helpers for the Interview Coach."""

from __future__ import annotations

import re


def parse_evaluation(text: str) -> tuple[int, str, str]:
    """Parse the evaluator LLM response into (score, feedback, ideal_answer).

    Expected format::

        SCORE: 7
        FEEDBACK: Good answer but missed edge cases …
        IDEAL_ANSWER: The ideal answer would be …

    Returns:
        Tuple of (score: int, feedback: str, ideal_answer: str).
        Falls back to (5, raw_text, "") if parsing fails.
    """
    score = 5  # default
    feedback = text
    ideal_answer = ""

    # Extract score
    score_match = re.search(r"SCORE:\s*(\d+)", text, re.IGNORECASE)
    if score_match:
        score = min(10, max(0, int(score_match.group(1))))

    # Extract feedback
    feedback_match = re.search(
        r"FEEDBACK:\s*(.+?)(?=IDEAL_ANSWER:|$)", text, re.IGNORECASE | re.DOTALL
    )
    if feedback_match:
        feedback = feedback_match.group(1).strip()

    # Extract ideal answer
    ideal_match = re.search(r"IDEAL_ANSWER:\s*(.+)", text, re.IGNORECASE | re.DOTALL)
    if ideal_match:
        ideal_answer = ideal_match.group(1).strip()

    return score, feedback, ideal_answer


def format_score_bar(score: int, max_score: int = 10) -> str:
    """Return a text-based progress bar for a score."""
    filled = "█" * score
    empty = "░" * (max_score - score)
    return f"{filled}{empty} {score}/{max_score}"


def compute_average_score(scores: list[int]) -> float:
    """Compute the average of a list of scores."""
    if not scores:
        return 0.0
    return sum(scores) / len(scores)
