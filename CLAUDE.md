# CLAUDE.md — agents-workshop

## Project Overview

A hands-on, notebook-driven personal learning repo for building AI agents from scratch in Python. The core track starts with raw Python (no frameworks) to build agent primitives, then graduates to smolagents. Appendix notebooks cover Python fundamentals, NumPy, tensors, and other prerequisites separately.

## Tech Stack

- **Python 3.11+**
- **LLM access**: OpenRouter (free-tier models preferred)
- **Agent SDK**: smolagents (HuggingFace) — introduced after raw-Python foundations
- **Notebooks**: Jupyter (.ipynb)
- **No heavyweight frameworks** (no LangChain, no LlamaIndex) unless explicitly exploring them

## Repo Structure

```
agents-workshop/
├── CLAUDE.md              # This file — project conventions
├── README.md              # Setup, overview, quickstart
├── roadmap.md             # Learning path & notebook plan
├── requirements.txt       # Pinned dependencies
├── .env.example           # Template for API keys (OPENROUTER_API_KEY)
│
├── core/                  # Main agents track (numbered notebooks)
│   ├── 01_hello_llm.ipynb
│   ├── 02_basic_agent_loop.ipynb
│   └── ...
│
├── appendix/              # Optional deep-dive notebooks
│   ├── python_basics.ipynb
│   ├── python_intermediate.ipynb
│   ├── numpy_essentials.ipynb
│   ├── tensors.ipynb
│   └── ...
│
└── utils/                 # Shared helper code extracted from notebooks
    └── __init__.py
```

## Conventions

### Notebooks

- **Numbered sequentially** in `core/` — `01_`, `02_`, etc.
- Each notebook starts with a markdown cell: title, what you'll learn, prerequisites (links to appendix if needed), and recommended reading (external high-quality resources).
- Keep notebooks **self-contained** — a reader should be able to run one notebook top-to-bottom without running previous ones (import shared code from `utils/` if needed).
- Prefer **small, runnable cells** over long monolithic blocks.
- Add markdown explanations *between* code cells, not just comments inside code.
- End each notebook with a "Try it yourself" section with exercises.

### Code Style

- Follow PEP 8. Use `snake_case` for functions/variables, `PascalCase` for classes.
- Type hints encouraged but not mandatory in notebooks.
- Use `httpx` for HTTP calls (async-friendly, modern).
- Use `python-dotenv` for loading `.env` — never hardcode API keys.
- When building from scratch, keep implementations minimal — prioritize clarity over robustness.

### External Resources

- Don't try to teach everything. Link to high-quality external material for deep dives.
- Prefer: official docs, Anthropic/OpenAI cookbooks, Andrej Karpathy videos, Lilian Weng blog posts, HuggingFace docs.
- Format: `> **Further reading:** [Title](url) — one-line description`

### Dependencies

- Keep `requirements.txt` updated when a notebook introduces a new dependency.
- Pin major versions (e.g., `smolagents>=1.0,<2.0`).

### Git

- Commit messages: `<type>: <description>` (e.g., `feat: add tool-use notebook`, `fix: correct API call in 03`).
- Clear notebook outputs before committing (use `jupyter nbconvert --clear-output`).
- Don't commit `.env` files.

## Key Design Decisions

1. **Raw Python first** — Build the agent loop (prompt → LLM → parse → tool call → loop) manually before introducing any SDK.
2. **OpenRouter for LLM access** — Free models available, single API key for multiple providers.
3. **smolagents over heavier frameworks** — Minimal, transparent, close to the metal.
4. **Agents-first, appendices second** — The core track is agents. Python/NumPy/tensor notebooks are optional reference material.
5. **Personal learning repo** — Optimize for understanding, not production polish.
