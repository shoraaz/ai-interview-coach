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

## ☁️ Deploy to Streamlit Cloud

### Step 1 — Push to GitHub (see section below)

### Step 2 — Go to Streamlit Cloud

1. Visit **[https://share.streamlit.io](https://share.streamlit.io)**
2. Sign in with your GitHub account

### Step 3 — Deploy

1. Click **"New app"**
2. Select your **repository** → `ai-interview-coach`
3. Set **Branch** → `main`
4. Set **Main file path** → `app.py`
5. Click **"Advanced settings"** → under **Secrets**, add:
   ```toml
   OPENROUTER_API_KEY = "sk-or-v1-your-key-here"
   ```
   *(Optional — users can also paste their own key in the sidebar)*
6. Click **"Deploy!"**

Your app will be live at `https://<your-app>.streamlit.app` in ~2 minutes.

> **Tip:** The `requirements.txt` file is what Streamlit Cloud uses to install dependencies. It's already included in the repo.

---

## 🔧 Push to GitHub — Step by Step

### First Time Setup

```bash
# 1. Navigate to the project folder
cd "c:\Users\shour\OneDrive\Desktop\eval_mech"

# 2. Initialize git
git init

# 3. Add all files
git add .

# 4. Make the first commit
git commit -m "feat: AI Interview Coach with LangGraph + OpenRouter"

# 5. Create a new repo on GitHub:
#    Go to https://github.com/new
#    - Repository name: ai-interview-coach
#    - Description: AI-powered Interview Coach built with LangGraph and free OpenRouter models
#    - Set to Public
#    - Do NOT add README/gitignore (we already have them)
#    - Click "Create repository"

# 6. Connect your local repo to GitHub (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/ai-interview-coach.git

# 7. Push
git branch -M main
git push -u origin main
```

### Subsequent Changes

```bash
git add .
git commit -m "your commit message"
git push
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

## 📝 Probable Interview Questions (By Domain)

### 🐍 Python Programming

| # | Question | Difficulty |
|---|---|---|
| 1 | What is the difference between a list and a tuple in Python? | Easy |
| 2 | Explain the GIL (Global Interpreter Lock) and its impact on multi-threading. | Medium |
| 3 | What are Python decorators? Write a decorator that logs function execution time. | Medium |
| 4 | Explain the difference between `__new__` and `__init__` methods. | Hard |
| 5 | How does Python's garbage collection work? Explain reference counting and generational GC. | Hard |
| 6 | What are generators and how do they differ from iterators? When would you use `yield from`? | Medium |
| 7 | Explain Python's MRO (Method Resolution Order) with diamond inheritance. | Hard |
| 8 | What is the difference between `deepcopy` and `copy`? When does it matter? | Easy |
| 9 | How do context managers work? Implement one using `__enter__` and `__exit__`. | Medium |
| 10 | What are metaclasses in Python and when would you use them? | Hard |
| 11 | Explain `*args` and `**kwargs` with practical examples. | Easy |
| 12 | What is monkey patching? What are its pros and cons? | Medium |
| 13 | How does Python handle memory management for small integers and string interning? | Hard |
| 14 | What is the difference between `@staticmethod`, `@classmethod`, and instance methods? | Easy |
| 15 | Explain async/await in Python. How does `asyncio` event loop work? | Hard |

### 🤖 Machine Learning

| # | Question | Difficulty |
|---|---|---|
| 1 | What is the bias-variance tradeoff? Give an example. | Easy |
| 2 | Explain the difference between L1 and L2 regularization. | Medium |
| 3 | How does a Random Forest work? What makes it better than a single decision tree? | Easy |
| 4 | What is cross-validation and why is it important? | Easy |
| 5 | Explain the curse of dimensionality and how PCA addresses it. | Medium |
| 6 | How does gradient boosting work? Compare XGBoost, LightGBM, and CatBoost. | Medium |
| 7 | What is the difference between generative and discriminative models? | Medium |
| 8 | How would you handle class imbalance in a dataset? List at least 5 techniques. | Medium |
| 9 | Explain the ROC curve and AUC. When is accuracy not a good metric? | Easy |
| 10 | What is feature importance and how do different algorithms compute it? | Medium |
| 11 | Explain the EM algorithm and how it's used in Gaussian Mixture Models. | Hard |
| 12 | What is the kernel trick in SVMs and why is it useful? | Hard |
| 13 | How does Bayesian optimization work for hyperparameter tuning? | Hard |
| 14 | Explain the difference between bagging and boosting with examples. | Medium |
| 15 | What is data leakage and how do you prevent it? | Easy |

### 🧠 Deep Learning

| # | Question | Difficulty |
|---|---|---|
| 1 | What is the vanishing gradient problem and how do you solve it? | Easy |
| 2 | Explain the architecture of a Transformer. What is self-attention? | Medium |
| 3 | What is batch normalization and why does it help training? | Easy |
| 4 | Compare RNN, LSTM, and GRU. When would you use each? | Medium |
| 5 | What is transfer learning? How do you fine-tune a pre-trained model? | Easy |
| 6 | Explain the difference between encoder-only, decoder-only, and encoder-decoder transformers. | Medium |
| 7 | How does dropout work during training vs inference? | Easy |
| 8 | What is the difference between SGD, Adam, and AdamW optimizers? | Medium |
| 9 | Explain skip connections in ResNet. Why do they help? | Medium |
| 10 | What are positional encodings in transformers and why are they needed? | Medium |
| 11 | Explain the attention mechanism mathematically (Q, K, V). | Hard |
| 12 | What is knowledge distillation? How does it compress models? | Hard |
| 13 | How do GANs work? Explain the min-max game between generator and discriminator. | Hard |
| 14 | What is mixed-precision training and how does it speed up training? | Hard |
| 15 | Explain LoRA and QLoRA. How do they enable efficient fine-tuning? | Hard |

### 📊 Data Science

| # | Question | Difficulty |
|---|---|---|
| 1 | What is the Central Limit Theorem and why is it important? | Easy |
| 2 | Explain the difference between Type I and Type II errors. | Easy |
| 3 | What is A/B testing? How do you determine the required sample size? | Medium |
| 4 | How do you handle missing data? List at least 5 strategies. | Medium |
| 5 | What is the difference between correlation and causation? | Easy |
| 6 | Explain p-value and statistical significance in hypothesis testing. | Easy |
| 7 | What is Simpson's Paradox? Give a real-world example. | Hard |
| 8 | How would you detect and handle outliers in a dataset? | Medium |
| 9 | Explain the difference between parametric and non-parametric tests. | Medium |
| 10 | What is survivorship bias and how can it affect your analysis? | Medium |
| 11 | Explain Bayesian vs Frequentist approaches to statistics. | Hard |
| 12 | What is multicollinearity and how does it affect regression? | Medium |
| 13 | How do you evaluate the results of a clustering algorithm? | Medium |
| 14 | What is the bootstrap method and when would you use it? | Hard |
| 15 | Explain the difference between ETL and ELT. | Easy |

### 🏗️ System Design

| # | Question | Difficulty |
|---|---|---|
| 1 | What is the CAP theorem? Explain with examples. | Easy |
| 2 | How would you design a URL shortener like bit.ly? | Medium |
| 3 | Explain horizontal vs vertical scaling. | Easy |
| 4 | How does a load balancer work? Compare different strategies. | Medium |
| 5 | Design a real-time chat application (like WhatsApp). | Hard |
| 6 | What is database sharding? What are the tradeoffs? | Medium |
| 7 | Explain microservices vs monolithic architecture. | Easy |
| 8 | How would you design a rate limiter? | Medium |
| 9 | What is a CDN and how does it improve performance? | Easy |
| 10 | Design a notification system that handles millions of users. | Hard |
| 11 | Explain event-driven architecture and message queues. | Medium |
| 12 | How would you design a recommendation system? | Hard |
| 13 | What is CQRS and Event Sourcing? | Hard |
| 14 | How does consistent hashing work? | Hard |
| 15 | Design a distributed cache system. | Hard |

### 🗃️ SQL & Databases

| # | Question | Difficulty |
|---|---|---|
| 1 | What is the difference between INNER JOIN, LEFT JOIN, RIGHT JOIN, and FULL OUTER JOIN? | Easy |
| 2 | Explain database normalization (1NF, 2NF, 3NF, BCNF). | Medium |
| 3 | What are window functions? Write a query using ROW_NUMBER(), RANK(). | Medium |
| 4 | What is an index? When should you use (and not use) indexes? | Easy |
| 5 | Explain ACID properties with examples. | Easy |
| 6 | What is a CTE? How does it differ from a subquery? | Medium |
| 7 | Explain the difference between DELETE, TRUNCATE, and DROP. | Easy |
| 8 | What are stored procedures and triggers? | Medium |
| 9 | How do you optimize a slow SQL query? | Hard |
| 10 | What is a deadlock in databases? How do you prevent it? | Hard |
| 11 | Explain transaction isolation levels. | Hard |
| 12 | What is the difference between SQL and NoSQL databases? | Medium |
| 13 | Write a query to find the Nth highest salary from an employee table. | Medium |
| 14 | What is a composite index? How does column order matter? | Hard |
| 15 | Explain eventual consistency vs strong consistency. | Medium |

### 📝 Natural Language Processing

| # | Question | Difficulty |
|---|---|---|
| 1 | What is tokenization? Compare word-level, character-level, and subword tokenization. | Easy |
| 2 | Explain word embeddings (Word2Vec, GloVe). | Easy |
| 3 | What is the attention mechanism and why was it a breakthrough? | Medium |
| 4 | Explain the difference between BERT and GPT architectures. | Medium |
| 5 | What is named entity recognition (NER)? | Easy |
| 6 | What is RAG (Retrieval-Augmented Generation)? | Medium |
| 7 | Explain BPE (Byte-Pair Encoding) tokenization. | Medium |
| 8 | What is the difference between semantic search and keyword search? | Easy |
| 9 | How do you evaluate an NLP model? Explain BLEU, ROUGE, and perplexity. | Medium |
| 10 | What are hallucinations in LLMs and how can you mitigate them? | Medium |
| 11 | Explain multi-head attention mathematically. | Hard |
| 12 | What is RLHF (Reinforcement Learning from Human Feedback)? | Hard |
| 13 | How does beam search differ from greedy decoding and top-k sampling? | Hard |
| 14 | What are vision-language models (VLMs)? | Hard |
| 15 | Explain prompt engineering. What makes a good prompt? | Easy |

### ⚙️ MLOps

| # | Question | Difficulty |
|---|---|---|
| 1 | What is MLOps and why is it important? | Easy |
| 2 | Explain the ML lifecycle from data collection to model monitoring. | Easy |
| 3 | What is model versioning? Compare DVC, MLflow, and W&B. | Medium |
| 4 | How do you containerize an ML model with Docker? | Medium |
| 5 | What is model drift? How do you detect and handle it? | Medium |
| 6 | Explain CI/CD for machine learning pipelines. | Medium |
| 7 | What is A/B testing for ML models in production? | Medium |
| 8 | How do you serve an ML model as a REST API? | Medium |
| 9 | What is a feature store? Why is it important in production ML? | Hard |
| 10 | Explain canary and blue-green deployment for ML models. | Hard |
| 11 | What is model observability? What metrics should you monitor? | Medium |
| 12 | How do you handle model retraining pipelines? | Hard |
| 13 | What is GPU optimization for model inference? | Hard |
| 14 | Explain the difference between online and batch inference. | Easy |
| 15 | How do you implement data validation in ML pipelines? | Medium |

### 🤖 Generative AI

| # | Question | Difficulty |
|---|---|---|
| 1 | What is a Large Language Model (LLM)? How does it generate text? | Easy |
| 2 | Explain the difference between fine-tuning and prompt engineering. | Easy |
| 3 | What is RAG? Design a simple RAG pipeline. | Medium |
| 4 | Explain temperature, top-k, and top-p sampling in LLMs. | Easy |
| 5 | What are AI agents? How do they differ from simple chatbots? | Medium |
| 6 | Explain chain-of-thought prompting. Why does it improve reasoning? | Medium |
| 7 | What is function calling / tool use in LLMs? | Medium |
| 8 | Compare LangChain vs LangGraph for building AI applications. | Medium |
| 9 | What is vector embedding and how are vector databases used in GenAI? | Medium |
| 10 | Explain the concept of context window and its limitations. | Easy |
| 11 | What is Constitutional AI and how does it improve safety? | Hard |
| 12 | Explain LoRA and parameter-efficient fine-tuning (PEFT). | Hard |
| 13 | What are mixture-of-experts (MoE) models? How do they scale? | Hard |
| 14 | How do multi-modal models (GPT-4V, Gemini) process images + text? | Hard |
| 15 | What is model distillation? | Hard |

### 🧮 Data Structures & Algorithms

| # | Question | Difficulty |
|---|---|---|
| 1 | What is the time complexity of common operations on arrays, linked lists, and hash maps? | Easy |
| 2 | Explain BFS vs DFS. When would you use each? | Easy |
| 3 | What is dynamic programming? Solve the Fibonacci problem using DP. | Medium |
| 4 | Explain how a hash table works internally. How are collisions handled? | Medium |
| 5 | What is a balanced BST? Compare AVL trees and Red-Black trees. | Hard |
| 6 | Explain Dijkstra's algorithm. What is its time complexity? | Medium |
| 7 | What is the difference between a stack and a queue? | Easy |
| 8 | How does merge sort work? What is its space and time complexity? | Easy |
| 9 | Explain the two-pointer technique with an example. | Medium |
| 10 | What is a trie? When is it more efficient than a hash map? | Medium |
| 11 | Explain topological sorting and its applications. | Hard |
| 12 | What is the sliding window technique? | Medium |
| 13 | How does quicksort's partition scheme work? | Medium |
| 14 | Explain Union-Find (Disjoint Set Union) with path compression. | Hard |
| 15 | What is A* search algorithm? How does it compare to Dijkstra's? | Hard |

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