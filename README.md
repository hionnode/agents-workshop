# agents-workshop

Hands-on Jupyter notebooks for building AI agents from scratch in Python.

Starts with raw Python — no frameworks, no magic. Builds the core agent patterns (loops, tool use, ReAct, memory, planning, multi-agent) from first principles, then graduates to [smolagents](https://huggingface.co/docs/smolagents). Uses [OpenRouter](https://openrouter.ai/) for LLM access (free models available).

## Setup

```bash
# Clone
git clone <repo-url>
cd agents-workshop

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your OpenRouter API key
```

Get a free OpenRouter API key at [openrouter.ai/keys](https://openrouter.ai/keys).

## Structure

```
core/          # Main track — numbered notebooks (01-19)
appendix/      # Prerequisite path — 3 tiers (Foundations, Intermediate, Domain-Specific)
utils/         # Shared helper code
```

See [roadmap.md](roadmap.md) for the full learning path and notebook plan.

## Quick Start

1. Set up your environment (above)
2. Open `core/01_hello_llm.ipynb`
3. Follow the roadmap from there

**New to Python?** Start with the appendix track instead — `appendix/01_python_fundamentals.ipynb` covers variables, types, and control flow, and the 10 appendix notebooks build up to the prerequisites you'll need for the core agent track.

## Dependencies

- Python 3.11+
- `httpx` — HTTP client
- `python-dotenv` — env variable loading
- `smolagents` — agent SDK (from Phase 2 onward)
- `jupyter` — notebook runtime

## Resources

Curated reading list in [roadmap.md](roadmap.md#recommended-external-resources).
