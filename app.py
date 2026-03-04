"""Streamlit frontend for the AI Interview Coach."""

from __future__ import annotations

import uuid
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

from interview_coach.config import INTERVIEW_DOMAINS, FREE_MODELS, GROQ_MODELS, get_interview_config
from interview_coach.graph import build_interview_graph, get_initial_state
from interview_coach.utils import format_score_bar, compute_average_score


# ── Page config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎯",
    layout="wide",
)

# ── Session state initialisation ─────────────────────────────────────────────

if "graph" not in st.session_state:
    st.session_state.graph = build_interview_graph()
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "interview_started" not in st.session_state:
    st.session_state.interview_started = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "interview_state" not in st.session_state:
    st.session_state.interview_state = None
if "is_complete" not in st.session_state:
    st.session_state.is_complete = False


# ── Sidebar ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.title("🎯 AI Interview Coach")
    st.markdown("---")

    # Provider selection
    provider = st.radio(
        "🌐 LLM Provider",
        options=["openrouter", "groq"],
        format_func=lambda x: {"openrouter": "OpenRouter (free models)", "groq": "Groq (fast inference)"}[x],
        horizontal=True,
        disabled=st.session_state.interview_started,
    )
    st.session_state.provider = provider

    # API Key input — label & placeholder adapt to provider
    if provider == "groq":
        key_label = "🔑 Groq API Key"
        key_placeholder = "gsk_..."
        key_help = "Get a free key at https://console.groq.com/keys"
    else:
        key_label = "🔑 OpenRouter API Key"
        key_placeholder = "sk-or-v1-..."
        key_help = "Get a free key at https://openrouter.ai/keys. Overrides .env if provided."

    api_key_input = st.text_input(
        key_label,
        type="password",
        value=st.session_state.get("api_key", ""),
        placeholder=key_placeholder,
        help=key_help,
        disabled=st.session_state.interview_started,
    )
    st.session_state.api_key = api_key_input

    # Model selection — show models for the chosen provider
    if provider == "groq":
        model_list = GROQ_MODELS
    else:
        model_list = FREE_MODELS

    model_options = list(model_list.keys()) + ["custom"]
    model_choice = st.selectbox(
        "🧠 Model",
        options=model_options,
        format_func=lambda x: model_list.get(x, "✏️ Enter custom model ID"),
        disabled=st.session_state.interview_started,
    )

    custom_model_id = ""
    if model_choice == "custom":
        custom_model_id = st.text_input(
            "Custom Model ID",
            placeholder="org/model-name" if provider == "groq" else "org/model-name:free",
            help="Enter any model ID supported by the chosen provider.",
            disabled=st.session_state.interview_started,
        )

    selected_model = custom_model_id if model_choice == "custom" else model_choice
    st.session_state.model_id = selected_model

    st.markdown("---")

    # Domain selection
    domain = st.selectbox(
        "📚 Interview Domain",
        options=list(INTERVIEW_DOMAINS.keys()),
        format_func=lambda x: INTERVIEW_DOMAINS[x].split(" - ")[0],
        disabled=st.session_state.interview_started,
    )
    st.caption(INTERVIEW_DOMAINS[domain].split(" - ")[1])

    # Difficulty selection
    cfg = get_interview_config()
    difficulty = st.select_slider(
        "📊 Difficulty Level",
        options=list(cfg.difficulty_levels),
        value=cfg.default_difficulty,
        disabled=st.session_state.interview_started,
    )

    # Number of questions
    max_questions = st.slider(
        "❓ Number of Questions",
        min_value=3,
        max_value=15,
        value=5,
        disabled=st.session_state.interview_started,
    )

    st.markdown("---")

    # Start / Reset buttons
    col1, col2 = st.columns(2)
    with col1:
        start_btn = st.button(
            "▶️ Start",
            disabled=st.session_state.interview_started,
            use_container_width=True,
        )
    with col2:
        reset_btn = st.button("🔄 Reset", use_container_width=True)

    if reset_btn:
        st.session_state.interview_started = False
        st.session_state.chat_history = []
        st.session_state.interview_state = None
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.is_complete = False
        st.rerun()

    # Scoreboard
    if st.session_state.interview_state and st.session_state.interview_state.get("scores"):
        st.markdown("---")
        st.subheader("📊 Scoreboard")
        scores = st.session_state.interview_state["scores"]
        for i, s in enumerate(scores, 1):
            st.text(f"Q{i}: {format_score_bar(s)}")
        avg = compute_average_score(scores)
        st.metric("Average Score", f"{avg:.1f}/10")

    st.markdown("---")
    st.caption("Powered by LangGraph + OpenRouter / Groq")


# ── Helper: run graph ────────────────────────────────────────────────────────


def run_graph(input_state: dict) -> dict:
    """Invoke the LangGraph and return the resulting state snapshot."""
    config = {"configurable": {"thread_id": st.session_state.thread_id}}
    result = st.session_state.graph.invoke(input_state, config)
    return result


# ── Start the interview ──────────────────────────────────────────────────────

if start_btn:
    # Check for API key
    from interview_coach.config import get_model_config
    _cfg = get_model_config(
        api_key=st.session_state.get("api_key", ""),
        provider=st.session_state.get("provider", "openrouter"),
    )
    if not _cfg.api_key:
        provider_name = "Groq" if st.session_state.get("provider") == "groq" else "OpenRouter"
        st.error(f"⚠️ Please enter your {provider_name} API key in the sidebar.")
        st.stop()

    st.session_state.interview_started = True
    initial = get_initial_state(
        domain, difficulty, max_questions,
        api_key=st.session_state.get("api_key", ""),
        model_id=st.session_state.get("model_id", ""),
        provider=st.session_state.get("provider", "openrouter"),
    )

    with st.spinner("Starting interview..."):
        result = run_graph(initial)

    st.session_state.interview_state = result

    # Collect AI messages for display
    for msg in result["messages"]:
        if isinstance(msg, AIMessage):
            st.session_state.chat_history.append(
                {"role": "assistant", "content": msg.content}
            )
    st.rerun()


# ── Chat display ─────────────────────────────────────────────────────────────

st.title("🎤 AI Interview Coach")

if not st.session_state.interview_started:
    st.info(
        "👈 Configure your interview settings in the sidebar and click **Start** to begin!"
    )
else:
    # Render chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ── User input ───────────────────────────────────────────────────────
    if not st.session_state.is_complete:
        user_input = st.chat_input("Type your answer here...")

        if user_input:
            # Display user message
            st.session_state.chat_history.append(
                {"role": "user", "content": user_input}
            )
            with st.chat_message("user"):
                st.markdown(user_input)

            # ── Step 1: Evaluate the answer ──────────────────────────────
            config = {"configurable": {"thread_id": st.session_state.thread_id}}

            with st.spinner("Evaluating your answer..."):
                result = st.session_state.graph.invoke(
                    {
                        "messages": [HumanMessage(content=user_input)],
                        "phase": "evaluate_answer",
                    },
                    config,
                )

            st.session_state.interview_state = result

            # Add feedback message to chat
            for msg in result["messages"]:
                if isinstance(msg, AIMessage):
                    content = msg.content
                    if content not in {
                        m["content"] for m in st.session_state.chat_history if m["role"] == "assistant"
                    }:
                        st.session_state.chat_history.append(
                            {"role": "assistant", "content": content}
                        )

            # ── Step 2: Auto-trigger next question or wrap-up ────────────
            next_phase = result.get("phase", "ask_question")

            if next_phase == "wrap_up":
                with st.spinner("Wrapping up..."):
                    result2 = st.session_state.graph.invoke(
                        {"phase": "wrap_up"}, config
                    )
                st.session_state.interview_state = result2
                st.session_state.is_complete = True
                for msg in result2["messages"]:
                    if isinstance(msg, AIMessage):
                        content = msg.content
                        if content not in {
                            m["content"] for m in st.session_state.chat_history if m["role"] == "assistant"
                        }:
                            st.session_state.chat_history.append(
                                {"role": "assistant", "content": content}
                            )
            elif not result.get("is_complete", False):
                with st.spinner("Next question..."):
                    result2 = st.session_state.graph.invoke(
                        {"phase": "ask_question"}, config
                    )
                st.session_state.interview_state = result2
                for msg in result2["messages"]:
                    if isinstance(msg, AIMessage):
                        content = msg.content
                        if content not in {
                            m["content"] for m in st.session_state.chat_history if m["role"] == "assistant"
                        }:
                            st.session_state.chat_history.append(
                                {"role": "assistant", "content": content}
                            )

            st.rerun()
    else:
        st.success("✅ Interview complete! Check the scoreboard in the sidebar.")
        st.balloons()
