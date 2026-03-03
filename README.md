# 🎯 AI Interview Coach

> An AI-powered technical interview practice coach built with **LangGraph 1.0+** and **free OpenRouter models**. Practice interviews across 10+ domains, get scored 0-10 per answer with detailed feedback, and track your progress — all for free.

---

## 📸 Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Streamlit UI                       │
│  (Chat • Sidebar config • API key • Model picker)    │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│              LangGraph StateGraph                    │
│                                                      │
│  START ──► greeting ──► ask_question ──► END (pause) │
│                              ▲                       │
│                              │                       │
│                       evaluate_answer ◄── user msg   │
│                              │                       │
│                     ┌────────┴────────┐              │
│                     ▼                 ▼              │
│               ask_question         wrap_up ──► END   │
│               (next Q)            (summary)          │
└─────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│            OpenRouter API (Free Models)               │
│  Llama 4 Maverick • Gemma 3 • Qwen 3 • DeepSeek     │
│  Mistral Small • Gemini Flash • or any custom model   │
└─────────────────────────────────────────────────────┘
```

---

## ✨ Features

| Feature | Description |
|---|---|
| **10+ Interview Domains** | Python, ML, Deep Learning, Data Science, System Design, SQL, NLP, MLOps, GenAI, DSA |
| **3 Difficulty Levels** | Easy (conceptual), Medium (applied), Hard (edge-case/tricky) |
| **7 Free Models** | Pre-configured free OpenRouter models + custom model ID support |
| **API Key from UI** | Paste your OpenRouter key directly in the sidebar — no `.env` needed |
| **Instant Scoring** | Each answer scored 0-10 with feedback + ideal answer |
| **Live Scoreboard** | Track progress in the sidebar |
| **Session Summary** | Strengths & improvement areas at the end |
| **Stateful Memory** | Full conversation context via LangGraph checkpointer |
| **Two UIs** | Streamlit web app + terminal CLI mode |

---

## 🛠️ Tech Stack

| Layer | Technology | Version |
|---|---|---|
| Agent Framework | LangGraph | ≥ 1.0.0 |
| LLM Integration | LangChain + langchain-openai | ≥ 0.3.0 |
| LLM Provider | OpenRouter (free tier) | — |
| Frontend | Streamlit | ≥ 1.40.0 |
| Python | Python | ≥ 3.11 |

---

## 🚀 Quick Start (Local)

### 1. Clone the Repo

```bash
git clone https://github.com/<YOUR_USERNAME>/ai-interview-coach.git
cd ai-interview-coach
```

### 2. Get a Free OpenRouter API Key

1. Go to **[https://openrouter.ai/keys](https://openrouter.ai/keys)**
2. Sign up (free) → Create an API key
3. You can either paste it in the sidebar UI **or** create a `.env` file:

```bash
cp .env.example .env
# Edit .env → OPENROUTER_API_KEY=sk-or-v1-your-key
```

### 3. Install Dependencies

**With uv (recommended):**
```bash
uv sync
```

**With pip:**
```bash
pip install -r requirements.txt
pip install -e .
```

### 4. Run

**Streamlit Web App:**
```bash
streamlit run app.py
```

**Terminal CLI Mode:**
```bash
python run_cli.py
```

---

## 📁 Project Structure

```
ai-interview-coach/
├── .env.example                 # API key template
├── .gitignore                   # Git ignore rules
├── app.py                       # Streamlit web UI
├── run_cli.py                   # Terminal CLI mode
├── pyproject.toml               # Project config & dependencies
├── requirements.txt             # pip requirements (for Streamlit Cloud)
├── README.md                    # This file
└── src/
    └── interview_coach/
        ├── __init__.py          # Package init
        ├── config.py            # Model config, free models list, domains
        ├── state.py             # LangGraph InterviewState (TypedDict)
        ├── prompts.py           # All prompt templates
        ├── nodes.py             # LangGraph node functions
        ├── graph.py             # LangGraph workflow definition
        └── utils.py             # Parsing & formatting utilities
```

---

## ⚙️ Configuration

### Choosing a Model

Pick from 7 free models in the sidebar dropdown, or select **"Custom"** and type any OpenRouter model ID:

| Model | ID |
|---|---|
| Llama 4 Maverick (Meta) | `meta-llama/llama-4-maverick:free` |
| Llama 4 Scout (Meta) | `meta-llama/llama-4-scout:free` |
| Gemma 3 27B (Google) | `google/gemma-3-27b-it:free` |
| Mistral Small 3.1 24B | `mistralai/mistral-small-3.1-24b-instruct:free` |
| Qwen 3 235B (Alibaba) | `qwen/qwen3-235b-a22b:free` |
| DeepSeek Chat V3 | `deepseek/deepseek-chat-v3-0324:free` |
| Gemini 2.0 Flash (Google) | `google/gemini-2.0-flash-exp:free` |

Browse all models at [openrouter.ai/models](https://openrouter.ai/models).

### Adding a New Domain

Add an entry to `INTERVIEW_DOMAINS` in `src/interview_coach/config.py`:

```python
INTERVIEW_DOMAINS["cloud"] = "Cloud Computing - AWS, Azure, GCP, serverless, IaC"
```

---

## 🔍 How It Works (LangGraph Concepts)

| Concept | Where Used |
|---|---|
| `StateGraph` | `graph.py` — the core workflow |
| `TypedDict` state | `state.py` — `InterviewState` with 12 fields |
| `add_messages` reducer | State accumulates full conversation history |
| Conditional edges | After evaluation → next question OR wrap-up |
| `InMemorySaver` checkpointer | Persistence between graph invocations |
| Node functions | `nodes.py` — greeting, ask, evaluate, wrap_up |
| `ChatPromptTemplate` | `prompts.py` — structured prompts per phase |
| `ChatOpenAI` with custom base_url | Connects LangChain to OpenRouter |

---

## 🐛 Troubleshooting

| Issue | Solution |
|---|---|
| `OPENROUTER_API_KEY` not found | Paste key in sidebar UI or add to `.env` |
| Model returns empty response | Try a different model from the dropdown |
| Rate limit exceeded | Free tier has limits — wait a few minutes |
| Import errors | Run `uv sync` or `pip install -e .` |
| Streamlit port in use | `streamlit run app.py --server.port 8502` |

---

## 📄 License

MIT License — free for personal and educational use.

---

## 🙏 Acknowledgements

- [LangGraph](https://github.com/langchain-ai/langgraph) — stateful agent framework
- [OpenRouter](https://openrouter.ai/) — free model access
- [Streamlit](https://streamlit.io/) — rapid UI prototyping
