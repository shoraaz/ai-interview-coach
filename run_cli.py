"""CLI entry point – run the interview in the terminal (no Streamlit)."""

from __future__ import annotations

from langchain_core.messages import HumanMessage, AIMessage

from interview_coach.config import INTERVIEW_DOMAINS
from interview_coach.graph import build_interview_graph, get_initial_state
from interview_coach.utils import format_score_bar, compute_average_score


def main() -> None:
    print("\n🎯  AI Interview Coach (Terminal Mode)")
    print("=" * 50)

    # ── Domain selection ──────────────────────────────────
    print("\nAvailable domains:")
    for i, (key, desc) in enumerate(INTERVIEW_DOMAINS.items(), 1):
        print(f"  {i}. {desc}")

    while True:
        choice = input("\nSelect domain number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(INTERVIEW_DOMAINS):
            domain = list(INTERVIEW_DOMAINS.keys())[int(choice) - 1]
            break
        print("Invalid choice. Try again.")

    # ── Difficulty ────────────────────────────────────────
    diff = input("Difficulty (easy/medium/hard) [medium]: ").strip().lower() or "medium"
    if diff not in ("easy", "medium", "hard"):
        diff = "medium"

    # ── Number of questions ───────────────────────────────
    nq = input("Number of questions (3-15) [5]: ").strip() or "5"
    max_q = max(3, min(15, int(nq))) if nq.isdigit() else 5

    # ── Build and start ───────────────────────────────────
    graph = build_interview_graph()
    initial = get_initial_state(domain, diff, max_q)
    config = {"configurable": {"thread_id": "cli-session"}}

    print("\n" + "=" * 50)
    result = graph.invoke(initial, config)

    # Print greeting + first question
    for msg in result["messages"]:
        if isinstance(msg, AIMessage):
            print(f"\n🤖 Interviewer: {msg.content}")

    # ── Interview loop ────────────────────────────────────
    while not result.get("is_complete", False):
        answer = input("\n✍️  Your answer: ").strip()
        if not answer:
            print("Please provide an answer.")
            continue

        result = graph.invoke(
            {"messages": [HumanMessage(content=answer)], "phase": "evaluate_answer"},
            config,
        )

        for msg in result["messages"]:
            if isinstance(msg, AIMessage):
                # Skip messages already printed
                print(f"\n🤖 Interviewer: {msg.content}")

    # ── Final summary ─────────────────────────────────────
    scores = result.get("scores", [])
    if scores:
        print("\n" + "=" * 50)
        print("📊  Final Scores:")
        for i, s in enumerate(scores, 1):
            print(f"  Q{i}: {format_score_bar(s)}")
        print(f"\n  Average: {compute_average_score(scores):.1f}/10")
    print("\n✅ Interview complete! Good luck! 🍀\n")


if __name__ == "__main__":
    main()
