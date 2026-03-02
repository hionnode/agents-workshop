# agents-workshop

Hands-on Jupyter notebooks for building AI agents from scratch in Python.

No frameworks, no magic. You start with a raw HTTP call to an LLM and build up — step by step — to a full [ReAct agent](https://arxiv.org/abs/2210.03629) with tool use, structured output, and multi-step reasoning. Phase 2 graduates to [smolagents](https://huggingface.co/docs/smolagents) (HuggingFace's lightweight agent framework) and goes deep on custom tools, CodeAgent, multi-agent systems, and more. Later phases tackle memory, planning, and advanced multi-agent patterns.

Uses [OpenRouter](https://openrouter.ai/) for LLM access. Free-tier models work for every notebook — no paid API key required.

## Who this is for

- You want to understand how AI agents actually work, not just import a library
- You know some Python (or are willing to learn it alongside — see the appendix track)
- You learn best by building things and running code

## What you'll build

By the end of the core track, you'll have built:

1. **A working LLM integration** — raw API calls, message roles, temperature control, multi-turn conversations
2. **An agent loop** — the fundamental while-loop where the LLM decides what happens next
3. **Tool-calling agents** — Python functions the LLM can invoke, with parsing and dispatch
4. **Structured output extraction** — reliable JSON from LLMs, with validation and retry
5. **A ReAct agent** — the full Thought / Action / Observation pattern, built from scratch
6. **smolagents mastery** — custom tools, CodeAgent, multi-agent systems, MCP integration, GradioUI
7. **Memory & RAG** — conversation memory, retrieval-augmented generation, knowledge tools
8. **Planning agents** — plan-then-execute, self-reflection, tree-of-thought reasoning
9. **Multi-agent systems** — collaboration, orchestration, debate patterns
10. **A research agent** — end-to-end agent combining everything

All starting from plain Python. No LangChain, no LlamaIndex, no abstractions hiding the mechanics.

## Setup

You need two things: the notebooks and an OpenRouter API key. Get a free key at [openrouter.ai/keys](https://openrouter.ai/keys) — the free tier is all you need.

### Option A: Local setup (recommended)

Best for: working offline, full control, using your own editor alongside Jupyter.

```bash
# Clone the repo
git clone <repo-url>
cd agents-workshop

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up your API key
cp .env.example .env
# Edit .env and paste your OpenRouter API key
```

Then start Jupyter:

```bash
jupyter notebook
```

Open `core/01_hello_llm.ipynb` and you're ready to go.

### Option B: Google Colab (no local install)

Best for: getting started fast, Chromebook/tablet users, avoiding local Python setup.

1. Open any notebook directly in Colab — go to [colab.research.google.com](https://colab.research.google.com), click **File > Open notebook > GitHub**, and paste the repo URL
2. Install dependencies in the first cell of each notebook:
   ```python
   !pip install httpx python-dotenv
   ```
3. Set your API key using Colab's Secrets feature (recommended) or inline:
   ```python
   # Option 1: Colab Secrets (recommended — click the key icon in the left sidebar)
   from google.colab import userdata
   import os
   os.environ["OPENROUTER_API_KEY"] = userdata.get("OPENROUTER_API_KEY")

   # Option 2: Set directly (less secure — don't share the notebook with your key in it)
   import os
   os.environ["OPENROUTER_API_KEY"] = "sk-or-v1-your-key-here"
   ```
4. The `utils/` imports won't work out of the box in Colab since it doesn't clone the full repo. For notebooks 02-05, either:
   - Clone the repo into Colab (git is pre-installed): `!git clone <repo-url> && %cd agents-workshop` — this is the easiest approach and makes everything work normally, or
   - Copy the `chat()` function from notebook 01 into a cell at the top

> **Colab notes:** The appendix notebooks (01-06) work in Colab with no special setup — they don't make API calls. Appendix 06 (HTTP & APIs) and all core notebooks need the API key setup above.

## Where to start

### Path A: Jump straight into agents

If you're comfortable with Python (functions, dicts, loops, `try`/`except`, f-strings), start here:

> **`core/01_hello_llm.ipynb`** &rarr; follow the "Next up" links at the bottom of each notebook

### Path B: Build up the prerequisites first

If you're newer to Python or want a structured refresher, start with the appendix:

> **`appendix/01_python_fundamentals.ipynb`** &rarr; work through all 10 appendix notebooks, then start the core track

Each appendix notebook tells you exactly which core notebooks it unlocks.

## Project structure

```
agents-workshop/
├── core/                  # Main agents track (22 notebooks, Phases 1-6)
│   ├── 01_hello_llm.ipynb             # Phase 1: First LLM API call
│   ├── 02_basic_agent_loop.ipynb      # Phase 1: The agent loop pattern
│   ├── 03_tool_use_from_scratch.ipynb # Phase 1: Tool calling from scratch
│   ├── 04_structured_output.ipynb     # Phase 1: JSON output, validation, retry
│   ├── 05_react_agent.ipynb           # Phase 1: Full ReAct agent
│   └── 06-22 (planned)               # Phases 2-6: smolagents → capstone
│
├── appendix/              # Prerequisite track (14 notebooks, 5 tiers)
│   ├── 01-06                          # Tier A: Python foundations
│   ├── 07-08                          # Tier B: OOP, decorators, type hints
│   ├── 09-10                          # Tier C: File I/O, NumPy
│   └── 11-14 (planned)               # Tier E: Async, SQL, WebSockets, graphs
│
├── ml-foundations/         # ML prerequisite track (6 notebooks, Tier D)
│   └── 01-06                          # Calculus → PyTorch → training
│
├── frameworks/            # Agent framework comparison (5 notebooks)
├── protocols/             # MCP & A2A interoperability (4 notebooks)
├── browser-agents/        # Computer use & browser automation (4 notebooks)
├── multimodal/            # Voice & vision agents (4 notebooks)
├── patterns/              # Agent architecture patterns (6 notebooks)
├── memory/                # Memory & knowledge infrastructure (5 notebooks)
├── observability/         # Tracing, cost optimization (4 notebooks)
├── projects/              # Portfolio projects (6 notebooks)
├── prompt-engineering/    # Prompt design & testing (4 notebooks)
├── eval/                  # Evaluation & debugging (7 notebooks)
├── llm-internals/         # LLM internals for agent builders (4 notebooks)
├── safety/                # Safety & guardrails (6 notebooks)
├── production/            # Async & production patterns (8 notebooks)
├── domain-agents/         # Domain-specific agent patterns (4 notebooks)
│
├── utils/                 # Shared helper code (chat() function, etc.)
├── roadmap.md             # Full learning path and future notebook plan
├── requirements.txt       # Python dependencies
└── .env.example           # Template for your API key
```

## Learning paths

This repo offers multiple tracks. Pick the one(s) that match your goals:

| Track | Directory | Notebooks | What it covers |
|-------|-----------|-----------|---------------|
| **Core: Agents** | `core/` | 22 (planned) | The main track — raw Python agents → smolagents → memory → planning → multi-agent → capstone |
| **Appendix: Python** | `appendix/` | 14 (10 + 4 planned) | Prerequisite Python skills — fundamentals, OOP, decorators, file I/O, NumPy, async, SQL, WebSockets, graphs |
| **ML Foundations** | `ml-foundations/` | 6 (planned) | Calculus, linear algebra, probability, PyTorch — prerequisites for [Karpathy's Zero to Hero](https://karpathy.ai/zero-to-hero.html) |
| **Prompt Engineering** | `prompt-engineering/` | 4 (planned) | System prompts, few-shot/CoT, structured output, prompt testing |
| **Evaluation** | `eval/` | 7 (planned) | Tracing, test suites, benchmarks, failure modes, LLM-as-judge, regression testing |
| **LLM Internals** | `llm-internals/` | 4 (planned) | Tokenization, attention, sampling, model selection |
| **Safety** | `safety/` | 6 (planned) | Input validation, output filtering, sandboxing, OWASP agentic top 10, auth, governance |
| **Production** | `production/` | 8 (planned) | Async, streaming, API serving, monitoring, databases, containers, agent-as-a-service, managed platforms |
| **Domain Agents** | `domain-agents/` | 4 (planned) | Code agents, research agents, data analysis, document Q&A |
| **Frameworks** | `frameworks/` | 5 (planned) | Framework comparison (smolagents, LangGraph, OpenAI Agents SDK, Pydantic AI), choosing a framework |
| **Protocols** | `protocols/` | 4 (planned) | MCP deep dive, building MCP servers, A2A protocol, MCP + A2A integration |
| **Browser Agents** | `browser-agents/` | 4 (planned) | Computer Use API, Playwright browser agent, Playwright MCP, web scraping agent |
| **Multimodal** | `multimodal/` | 4 (planned) | Vision agents, voice pipeline, realtime voice, multimodal tool use |
| **Architecture Patterns** | `patterns/` | 6 (planned) | State machines, event-driven, human-in-the-loop, agentic RAG, deep research, workflow orchestration |
| **Memory Infrastructure** | `memory/` | 5 (planned) | Memory architectures, vector databases, knowledge graphs, long-term memory, personalization |
| **Observability** | `observability/` | 4 (planned) | Langfuse tracing, OpenTelemetry, cost optimization, production dashboards |
| **Projects** | `projects/` | 6 (planned) | Portfolio projects — knowledge assistant, code review, support bot, data analysis, research team, browser automation |

See [roadmap.md](roadmap.md) for full details on every track.

## Core track overview

Each notebook is self-contained — you can run it top to bottom without running previous ones. But they build on each other conceptually, so going in order is recommended.

### Phase 1 — Foundations (Raw Python, No SDK)

| # | Notebook | What you build | Key concepts |
|---|----------|---------------|--------------|
| 01 | Hello LLM | First API call to OpenRouter | Chat completions API, message roles, temperature, multi-turn |
| 02 | Basic Agent Loop | While-loop agent that decides when to stop | Agent loop, stop conditions, conversation history as memory |
| 03 | Tool Use from Scratch | Agent that calls Python functions as tools | Tool definitions, Action/Input parsing, dispatch, observation |
| 04 | Structured Output | Reliable JSON extraction from LLMs | JSON prompting, schema validation, retry logic |
| 05 | ReAct Agent | Full Reason + Act agent | Thought/Action/Observation, scratchpad, few-shot prompting |

### Phase 2 — smolagents (6 notebooks)

| # | Notebook | What you build | Key concepts |
|---|----------|---------------|--------------|
| 06 | Intro to smolagents | Rebuild Phase 1 agents with smolagents | CodeAgent vs ToolCallingAgent, LiteLLMModel, agent traces |
| 07 | Custom Tools | Tools with `@tool` and `Tool` subclass | Decorator vs subclass, tool descriptions, debugging |
| 08 | CodeAgent Deep Dive | Agent that writes and executes Python | LocalPythonExecutor, sandboxing, state persistence |
| 09 | Tool Ecosystem | Hub tools, MCP servers, Gradio Spaces | `load_tool()`, `MCPClient`, `Tool.from_space()`, interop |
| 10 | Multi-Agent Systems | 3-agent system with manager delegation | Hierarchical orchestration, `managed_agents`, planning |
| 11 | Agent Configuration | Polished agent with GradioUI | Custom instructions, output validation, sharing, GradioUI |

> Phases 3-6 (memory, planning, advanced multi-agent, capstone) are planned — see [roadmap.md](roadmap.md) for the full curriculum.

## Appendix track overview

Skip any notebook you're already comfortable with. Each tier unlocks a phase of the core track or additional learning paths.

| Tier | Notebooks | Unlocks |
|------|-----------|---------|
| **A: Foundations** | 01-06 (Python basics, functions, data structures, strings/JSON, error handling, HTTP) | Core Phase 1 |
| **B: Intermediate** | 07-08 (classes/OOP, decorators/type hints) | Core Phase 2 |
| **C: Domain-specific** | 09-10 (file I/O, NumPy for embeddings) | Core Phase 3 |
| **D: ML Foundations** | ml-foundations/01-06 (calculus, linear algebra, probability, PyTorch, NN building blocks, training) | [Karpathy's Zero to Hero](https://karpathy.ai/zero-to-hero.html) |
| **E: Advanced Foundations** | 11-14 (async/await, databases/SQL, WebSockets/streaming, graph data structures) | Production, multimodal, memory, protocols paths |

## Notebook conventions

Every notebook follows the same structure:

- **Header** — title, what you'll learn, prerequisites, further reading links (8-12 curated external references per notebook)
- **Numbered sections** — small runnable cells with markdown explanations between them
- **Putting It Together** — a capstone exercise combining all concepts from the notebook
- **Try It Yourself** — 3-4 exercises with scaffold code cells
- **Navigation** — link to the next notebook at the bottom

## Dependencies

- **Python 3.11+**
- **httpx** — modern HTTP client (async-friendly)
- **python-dotenv** — loads API keys from `.env`
- **jupyter** / **ipykernel** — notebook runtime
- **numpy** — used in the embeddings appendix notebook

All pinned in `requirements.txt`. No heavyweight frameworks.

## Resources

Curated external resources are linked throughout each notebook (8-12 per notebook). The best starting points:

- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/)
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic)
- [ReAct Paper (Yao et al., 2022)](https://arxiv.org/abs/2210.03629)
- [OpenRouter Docs](https://openrouter.ai/docs/quickstart)
- [smolagents Documentation](https://huggingface.co/docs/smolagents)
- [Karpathy — Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html)

See [roadmap.md](roadmap.md#recommended-external-resources) for the full reading list.
