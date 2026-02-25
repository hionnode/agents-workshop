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

## Appendix Track: Prerequisites & Deep Dives

These are **optional** — use them to fill gaps or as reference. Not required for the core track.

| Notebook | Covers | When to Use |
|----------|--------|------------|
| `python_basics.ipynb` | Variables, control flow, functions, data structures | If rusty on Python fundamentals |
| `python_intermediate.ipynb` | Decorators, generators, context managers, type hints | Before Phase 2 (smolagents uses decorators heavily) |
| `python_advanced.ipynb` | Metaclasses, descriptors, async/await, protocols | When you want to understand SDK internals |
| `numpy_essentials.ipynb` | Arrays, broadcasting, vectorized operations | Before the RAG notebooks (embeddings are arrays) |
| `tensors.ipynb` | Tensor basics, PyTorch tensor ops, GPU vs CPU | For understanding model internals later |
| `http_and_apis.ipynb` | REST, HTTP methods, headers, auth, httpx | If unfamiliar with calling APIs from Python |

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
