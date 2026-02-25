# Roadmap — agents-workshop

## Philosophy

Don't boil the ocean. Each notebook tackles one concept, builds one thing, and links out to excellent external resources for the theory. The goal is to **scaffold agents from scratch** — understanding every layer before abstracting it away.

---

## Core Track: Building Agents from Scratch

### Phase 1 — Foundations (Raw Python, No SDK)

| # | Notebook | What You Build | Key Concepts |
|---|----------|---------------|--------------|
| 01 | `hello_llm.ipynb` | First API call to OpenRouter | HTTP requests, chat completions API, message format, roles, temperature |
| 02 | `basic_agent_loop.ipynb` | A while-loop agent that keeps calling the LLM until it says "DONE" | Agent loop pattern, stop conditions, conversation history management |
| 03 | `tool_use_from_scratch.ipynb` | Agent that can call Python functions as tools | Function calling, JSON schema for tools, parsing LLM output, tool dispatch |
| 04 | `structured_output.ipynb` | Agent that returns structured data reliably | JSON mode, output parsing, retry logic, schema validation |
| 05 | `react_agent.ipynb` | ReAct (Reason + Act) agent in pure Python | Thought/Action/Observation loop, chain-of-thought prompting, scratchpad |

### Phase 2 — Graduating to smolagents

| # | Notebook | What You Build | Key Concepts |
|---|----------|---------------|--------------|
| 06 | `intro_to_smolagents.ipynb` | Rebuild notebook 03's agent using smolagents | smolagents architecture, Tool class, CodeAgent vs ToolCallingAgent |
| 07 | `custom_tools.ipynb` | Write custom tools (web search, file I/O, calculator) | `@tool` decorator, tool descriptions, input/output types |
| 08 | `code_agent.ipynb` | Agent that writes and executes Python code to solve problems | CodeAgent, sandboxing, code generation vs function calling tradeoffs |

### Phase 3 — Memory & Knowledge

| # | Notebook | What You Build | Key Concepts |
|---|----------|---------------|--------------|
| 09 | `conversation_memory.ipynb` | Agent with sliding window + summary memory | Context window limits, summarization strategies, token counting |
| 10 | `rag_from_scratch.ipynb` | Retrieval-augmented generation pipeline | Embeddings, vector similarity, chunking strategies, retrieval + generation |
| 11 | `rag_with_tools.ipynb` | Agent that uses RAG as a tool | Retrieval as a tool, when to retrieve vs when to reason, hybrid approaches |

### Phase 4 — Planning & Reasoning

| # | Notebook | What You Build | Key Concepts |
|---|----------|---------------|--------------|
| 12 | `planning_agent.ipynb` | Agent that makes a plan before executing | Plan-then-execute, task decomposition, plan revision |
| 13 | `reflection_agent.ipynb` | Agent that critiques and improves its own output | Self-reflection, critic loop, output refinement |
| 14 | `tree_of_thought.ipynb` | Agent that explores multiple reasoning paths | Branching, evaluation, backtracking, best-path selection |

### Phase 5 — Multi-Agent Systems

| # | Notebook | What You Build | Key Concepts |
|---|----------|---------------|--------------|
| 15 | `multi_agent_basics.ipynb` | Two agents collaborating on a task | Agent communication, message passing, shared state |
| 16 | `orchestrator_pattern.ipynb` | Manager agent that delegates to specialist agents | Orchestration, delegation, result aggregation |
| 17 | `debate_agents.ipynb` | Agents that debate and reach consensus | Adversarial collaboration, voting, consensus mechanisms |

### Phase 6 — Putting It All Together

| # | Notebook | What You Build | Key Concepts |
|---|----------|---------------|--------------|
| 18 | `research_agent.ipynb` | End-to-end research agent (search → read → synthesize → report) | Combining tools + memory + planning + multi-step reasoning |
| 19 | `eval_and_debug.ipynb` | Evaluate and debug agent behavior | Tracing, logging, evaluating agent outputs, common failure modes |

---

## Appendix Track: Prerequisite Path

A structured 10-notebook, 3-tier prerequisite path. Each tier maps to a core phase — complete the tier before starting its corresponding phase. Skip any notebook you're already comfortable with.

### Tier A — Absolute Foundations (before Core Phase 1)

| # | Notebook | Key Topics |
|---|----------|-----------|
| 01 | `python_fundamentals.ipynb` | Variables, types, control flow, imports, Jupyter basics |
| 02 | `functions_and_scope.ipynb` | def, params, returns, docstrings, functions-as-values, lambdas |
| 03 | `data_structures.ipynb` | Lists, dicts, nested structures, comprehensions, list-of-dicts pattern |
| 04 | `strings_and_json.ipynb` | String methods, f-strings, regex basics, json module, JSON schemas |
| 05 | `error_handling.ipynb` | try/except, common exceptions, retry patterns, basic logging |
| 06 | `http_and_apis.ipynb` | HTTP fundamentals, httpx, dotenv, API keys, JSON request/response |

### Tier B — Intermediate Python (before Core Phase 2)

| # | Notebook | Key Topics |
|---|----------|-----------|
| 07 | `classes_and_oop.ipynb` | class, \_\_init\_\_, self, inheritance, super(), method override |
| 08 | `decorators_and_type_hints.ipynb` | Type annotations, decorator mechanics, rebuilding a @tool pattern |

### Tier C — Domain-Specific (before Core Phase 3)

| # | Notebook | Key Topics |
|---|----------|-----------|
| 09 | `file_io_and_text_processing.ipynb` | open/with, reading files, text chunking, pathlib |
| 10 | `numpy_for_embeddings.ipynb` | NumPy arrays, dot product, cosine similarity, top-k retrieval |

### Cross-Reference: Appendix → Core

| Appendix Tier | Unlocks Core Phase | Why |
|---------------|-------------------|-----|
| **Tier A** (01–06) | **Phase 1** — Foundations | Core 01–05 require HTTP calls, JSON parsing, string manipulation, error handling, and basic Python fluency |
| **Tier B** (07–08) | **Phase 2** — smolagents | Core 06–08 use the `@tool` decorator, subclass `Tool`, and rely on type hints throughout |
| **Tier C** (09–10) | **Phase 3** — Memory & Knowledge | Core 09–11 read files, chunk text, compute embeddings, and do vector similarity search |

### What was removed (and why)

- **`python_advanced` (metaclasses, descriptors, protocols)** — no core notebook uses these
- **`tensors` (PyTorch, GPU vs CPU)** — no core notebook uses tensors
- **`python_intermediate`** — split into focused notebooks (08 for decorators/type hints, 09 for file I/O/context managers)

---

## Recommended External Resources

These are not notebooks we'll build — these are excellent resources to read alongside the core track.

### LLMs & Foundations
- [Andrej Karpathy — Intro to LLMs (video)](https://www.youtube.com/watch?v=zjkBMFhNj_g)
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/)
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic)

### Tool Use & Function Calling
- [OpenAI — Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [Anthropic — Tool Use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview)

### smolagents
- [smolagents Documentation](https://huggingface.co/docs/smolagents)
- [smolagents GitHub](https://github.com/huggingface/smolagents)

### RAG
- [Anthropic — Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)

### Multi-Agent
- [AutoGen Research Paper](https://arxiv.org/abs/2308.08155)
- [CrewAI Concepts (for pattern inspiration)](https://docs.crewai.com/concepts)

---

## Progression Notes

- **Start with 01-05.** These are the foundation. Don't skip them.
- **06-08 can be done anytime after 05.** They're the "now do it properly" layer.
- **09-11, 12-14, 15-17 are independent phases.** Do them in any order based on interest.
- **18-19 are the capstone.** Do these last.
- **This roadmap is flexible.** Add notebooks, split them, merge them, skip them. It's a personal learning repo, not a curriculum.
