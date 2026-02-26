# agents-workshop

Hands-on Jupyter notebooks for building AI agents from scratch in Python.

No frameworks, no magic. You start with a raw HTTP call to an LLM and build up — step by step — to a full [ReAct agent](https://arxiv.org/abs/2210.03629) with tool use, structured output, and multi-step reasoning. Later phases graduate to [smolagents](https://huggingface.co/docs/smolagents) and tackle memory, planning, and multi-agent systems.

Uses [OpenRouter](https://openrouter.ai/) for LLM access. Free-tier models work for every notebook — no paid API key required.

## Who this is for

- You want to understand how AI agents actually work, not just import a library
- You know some Python (or are willing to learn it alongside — see the appendix track)
- You learn best by building things and running code

## What you'll build

By the end of the core track's first phase (notebooks 01-05), you'll have built:

1. **A working LLM integration** — raw API calls, message roles, temperature control, multi-turn conversations
2. **An agent loop** — the fundamental while-loop where the LLM decides what happens next
3. **Tool-calling agents** — Python functions the LLM can invoke, with parsing and dispatch
4. **Structured output extraction** — reliable JSON from LLMs, with validation and retry
5. **A ReAct agent** — the full Thought / Action / Observation pattern, built from scratch

All in plain Python. No LangChain, no LlamaIndex, no abstractions hiding the mechanics.

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
   - Clone the repo into Colab: `!git clone <repo-url> && %cd agents-workshop` (then everything works normally), or
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
├── core/                  # Main agents track (numbered notebooks)
│   ├── 01_hello_llm.ipynb             # First LLM API call
│   ├── 02_basic_agent_loop.ipynb      # The agent loop pattern
│   ├── 03_tool_use_from_scratch.ipynb # Tool calling from scratch
│   ├── 04_structured_output.ipynb     # JSON output, validation, retry
│   └── 05_react_agent.ipynb           # Full ReAct agent
│
├── appendix/              # Prerequisite track (10 notebooks, 3 tiers)
│   ├── 01_python_fundamentals.ipynb
│   ├── 02_functions_and_scope.ipynb
│   ├── 03_data_structures.ipynb
│   ├── 04_strings_and_json.ipynb
│   ├── 05_error_handling.ipynb
│   ├── 06_http_and_apis.ipynb
│   ├── 07_classes_and_oop.ipynb
│   ├── 08_decorators_and_type_hints.ipynb
│   ├── 09_file_io_and_text_processing.ipynb
│   └── 10_numpy_for_embeddings.ipynb
│
├── utils/                 # Shared helper code (chat() function, etc.)
├── roadmap.md             # Full learning path and future notebook plan
├── requirements.txt       # Python dependencies
└── .env.example           # Template for your API key
```

## Core track overview

Each notebook is self-contained — you can run it top to bottom without running previous ones. But they build on each other conceptually, so going in order is recommended.

| # | Notebook | What you build | Key concepts |
|---|----------|---------------|--------------|
| 01 | Hello LLM | First API call to OpenRouter | Chat completions API, message roles, temperature, multi-turn |
| 02 | Basic Agent Loop | While-loop agent that decides when to stop | Agent loop, stop conditions, conversation history as memory |
| 03 | Tool Use from Scratch | Agent that calls Python functions as tools | Tool definitions, Action/Input parsing, dispatch, observation |
| 04 | Structured Output | Reliable JSON extraction from LLMs | JSON prompting, schema validation, retry logic |
| 05 | ReAct Agent | Full Reason + Act agent | Thought/Action/Observation, scratchpad, few-shot prompting |

> Phases 2-6 (smolagents, memory, planning, multi-agent, capstone) are planned — see [roadmap.md](roadmap.md) for the full curriculum.

## Appendix track overview

Skip any notebook you're already comfortable with. Each tier unlocks a phase of the core track.

| Tier | Notebooks | Unlocks |
|------|-----------|---------|
| **A: Foundations** | 01-06 (Python basics, functions, data structures, strings/JSON, error handling, HTTP) | Core Phase 1 |
| **B: Intermediate** | 07-08 (classes/OOP, decorators/type hints) | Core Phase 2 |
| **C: Domain-specific** | 09-10 (file I/O, NumPy for embeddings) | Core Phase 3 |

## Notebook conventions

Every notebook follows the same structure:

- **Header** — title, what you'll learn, prerequisites, further reading links
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

Curated external resources are linked throughout each notebook. The best starting points:

- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/)
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic)
- [ReAct Paper (Yao et al., 2022)](https://arxiv.org/abs/2210.03629)
- [OpenRouter Docs](https://openrouter.ai/docs/quickstart)

See [roadmap.md](roadmap.md#recommended-external-resources) for the full reading list.
