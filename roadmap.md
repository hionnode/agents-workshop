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
| 06 | `intro_to_smolagents.ipynb` | Rebuild Phase 1 agents with smolagents | smolagents architecture, CodeAgent vs ToolCallingAgent, LiteLLMModel, agent traces, `agent.logs`, `write_memory_to_messages()` |
| 07 | `custom_tools.ipynb` | Custom tools with `@tool` and `Tool` subclass | `@tool` decorator, `Tool` subclass with `forward()`, tool descriptions, debugging tools |
| 08 | `code_agent_deep_dive.ipynb` | CodeAgent that writes and executes Python code | LocalPythonExecutor, `additional_authorized_imports`, state persistence, sandboxing (E2B, Docker), CodeAgent system prompt |
| 09 | `tool_ecosystem.ipynb` | Agent using Hub tools, MCP servers, and Gradio Spaces | `load_tool()`, `Tool.from_hub()`, `Tool.from_space()`, `MCPClient`, LangChain interop, runtime toolbox management |
| 10 | `multi_agent_systems.ipynb` | 3-agent system with manager delegation | Hierarchical orchestration, `managed_agents`, agent type selection, `planning_interval`, multi-agent tracing |
| 11 | `agent_configuration.ipynb` | Polished agent with custom instructions and GradioUI | Custom instructions, `final_answer_checks`, prompt templates, `additional_args`, debugging strategies, sharing agents on Hub, GradioUI |

### Phase 3 — Memory & Knowledge

| # | Notebook | What You Build | Key Concepts |
|---|----------|---------------|--------------|
| 12 | `conversation_memory.ipynb` | Agent with sliding window + summary memory | Context window limits, summarization strategies, token counting |
| 13 | `rag_from_scratch.ipynb` | Retrieval-augmented generation pipeline | Embeddings, vector similarity, chunking strategies, retrieval + generation |
| 14 | `rag_with_tools.ipynb` | Agent that uses RAG as a tool | Retrieval as a tool, when to retrieve vs when to reason, hybrid approaches |

### Phase 4 — Planning & Reasoning

| # | Notebook | What You Build | Key Concepts |
|---|----------|---------------|--------------|
| 15 | `planning_agent.ipynb` | Agent that makes a plan before executing | Plan-then-execute, task decomposition, plan revision |
| 16 | `reflection_agent.ipynb` | Agent that critiques and improves its own output | Self-reflection, critic loop, output refinement |
| 17 | `tree_of_thought.ipynb` | Agent that explores multiple reasoning paths | Branching, evaluation, backtracking, best-path selection |

### Phase 5 — Multi-Agent Systems (Advanced)

| # | Notebook | What You Build | Key Concepts |
|---|----------|---------------|--------------|
| 18 | `multi_agent_basics.ipynb` | Two agents collaborating on a task | Agent communication, message passing, shared state |
| 19 | `orchestrator_pattern.ipynb` | Manager agent that delegates to specialist agents | Orchestration, delegation, result aggregation |
| 20 | `debate_agents.ipynb` | Agents that debate and reach consensus | Adversarial collaboration, voting, consensus mechanisms |

### Phase 6 — Putting It All Together

| # | Notebook | What You Build | Key Concepts |
|---|----------|---------------|--------------|
| 21 | `research_agent.ipynb` | End-to-end research agent (search → read → synthesize → report) | Combining tools + memory + planning + multi-step reasoning |
| 22 | `eval_and_debug.ipynb` | Evaluate and debug agent behavior | Tracing, logging, evaluating agent outputs, common failure modes |

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

### Tier D — ML Foundations (before Karpathy's Zero to Hero)

A separate 6-notebook track in `ml-foundations/` preparing learners for [Karpathy's Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html) course.

| # | Notebook | Key Topics | Unlocks Karpathy Lectures |
|---|----------|-----------|--------------------------|
| 01 | `calculus_for_deep_learning.ipynb` | Derivatives, chain rule, partial derivatives, gradient descent, computational graphs | 1 (micrograd), 4, 5 |
| 02 | `linear_algebra_essentials.ipynb` | Vectors, dot products, matrix multiply, transpose/reshape, softmax | 2, 3, 7 (GPT) |
| 03 | `probability_and_statistics.ipynb` | Distributions, sampling, cross-entropy, NLL, mean/variance, normal distribution | 2, 3, 4 |
| 04 | `pytorch_fundamentals.ipynb` | Tensors, operations, autograd, `nn.Module`, training loop, GPU basics | 2-7 (all PyTorch lectures) |
| 05 | `neural_network_building_blocks.ipynb` | Linear layers, activations, embeddings, BatchNorm, LayerNorm, residual connections, dropout | 3, 4, 6, 7 |
| 06 | `training_deep_networks.ipynb` | SGD, learning rate schedules, train/val/test splits, overfitting, weight initialization | 3, 4, 5, 7 |

See the [cross-reference map](#karpathy-lecture-prerequisites) below for which notebooks to complete before each Karpathy lecture.

### Cross-Reference: Appendix → Core

| Appendix Tier | Unlocks Core Phase | Why |
|---------------|-------------------|-----|
| **Tier A** (01–06) | **Phase 1** — Foundations | Core 01–05 require HTTP calls, JSON parsing, string manipulation, error handling, and basic Python fluency |
| **Tier B** (07–08) | **Phase 2** — smolagents | Core 06–11 use the `@tool` decorator, subclass `Tool`, and rely on type hints throughout |
| **Tier C** (09–10) | **Phase 3** — Memory & Knowledge | Core 12–14 read files, chunk text, compute embeddings, and do vector similarity search |
| **Tier D** (ml-foundations 01–06) | [Karpathy's Zero to Hero](https://karpathy.ai/zero-to-hero.html) | The 8-lecture series requires calculus, linear algebra, probability, and PyTorch fluency |

### Cross-links Between Tracks

- Appendix 10 (NumPy) → ml-foundations/02 (linear algebra uses NumPy extensively)
- Appendix 07 (Classes) → ml-foundations/04 (PyTorch's `nn.Module` is a class)
- Appendix 08 (Type Hints) → ml-foundations/04 (PyTorch type annotations)
- Appendix 04 (Strings) + 09 (File I/O) → Karpathy Lecture 8 (GPT Tokenizer)

### Karpathy Lecture Prerequisites

| Karpathy Lecture | Required ml-foundations Notebooks | Also Helpful |
|-----------------|----------------------------------|-------------|
| 1. micrograd (backprop) | **01** (calculus) | Appendix 07 (classes) |
| 2. makemore/bigrams | **03** (probability), **04** (PyTorch) | 02 (linear algebra) |
| 3. makemore/MLP | **02** (linear algebra), **04** (PyTorch), **05** (building blocks), **06** (training) | — |
| 4. makemore/BatchNorm | **03** (statistics), **05** (building blocks), **06** (training) | — |
| 5. makemore/backprop ninja | **01** (calculus deep), **04** (autograd) | — |
| 6. makemore/WaveNet | **05** (building blocks) | — |
| 7. Let's build GPT | **02** (linear algebra), **05** (building blocks — attention, LayerNorm, residual) | Appendix 10 (NumPy) |
| 8. GPT Tokenizer | Appendix 04 (strings), Appendix 09 (file I/O) | — |

### What was removed (and why)

- **`python_advanced` (metaclasses, descriptors, protocols)** — no core notebook uses these
- **`tensors` (PyTorch, GPU vs CPU)** — moved to ml-foundations/04 (not needed for the agent track)
- **`python_intermediate`** — split into focused notebooks (08 for decorators/type hints, 09 for file I/O/context managers)

---

## Additional Learning Paths

Beyond the core agent track, these paths cover the broader skills an agent builder needs. Each path is self-contained with its own directory.

### Prompt Engineering for Agents (`prompt-engineering/`, 4 notebooks)

**Why:** The system prompt IS the agent's programming language. Bad prompts = bad agents.

| # | Notebook | What You Build |
|---|---------|---------------|
| 01 | `system_prompt_design.ipynb` | Design effective system prompts with role, constraints, format, examples |
| 02 | `few_shot_and_cot.ipynb` | Few-shot prompting, chain-of-thought, self-consistency |
| 03 | `structured_output_prompting.ipynb` | JSON mode, XML tags, constrained generation (Outlines) |
| 04 | `prompt_testing.ipynb` | A/B testing prompts, building a prompt evaluation harness |

> **Key references:** [Anthropic prompt engineering guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview), [OpenAI best practices](https://platform.openai.com/docs/guides/prompt-engineering), [DSPY](https://dspy-docs.vercel.app/)

### Evaluation & Debugging (`eval/`, 4 notebooks)

**Why:** "It works on my example" is not enough. Agents need systematic evaluation.

| # | Notebook | What You Build |
|---|---------|---------------|
| 01 | `tracing_and_logging.ipynb` | Structured logging for agent runs, trace visualization |
| 02 | `building_test_suites.ipynb` | Unit tests for tools, integration tests for agent loops, golden-answer tests |
| 03 | `benchmarking_agents.ipynb` | Run agents against standard benchmarks (GAIA, HotPotQA, simple custom evals) |
| 04 | `failure_modes.ipynb` | Common agent failures (loops, hallucinated tools, wrong tool selection) and fixes |

> **Key references:** [GAIA benchmark](https://huggingface.co/gaia-benchmark), [Braintrust](https://www.braintrust.dev/), [Anthropic eval guide](https://docs.anthropic.com/en/docs/build-with-claude/develop-tests)

### LLM Internals for Agent Builders (`llm-internals/`, 4 notebooks)

**Why:** Understanding how LLMs work makes you a better agent builder — you know WHY prompting tricks work.

| # | Notebook | What You Build |
|---|---------|---------------|
| 01 | `tokenization_deep_dive.ipynb` | Build a BPE tokenizer, understand context windows, token counting |
| 02 | `attention_and_context.ipynb` | How attention works (visual), context window management, long-context strategies |
| 03 | `sampling_and_generation.ipynb` | Temperature, top-p, top-k, repetition penalty — what each does and when to use it |
| 04 | `model_selection.ipynb` | Open vs closed models, cost/quality tradeoffs, when to use which model for agents |

> **Key references:** [Karpathy — Let's build the GPT Tokenizer](https://www.youtube.com/watch?v=zduSFxRajkE), [Jay Alammar — The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/), [Anthropic model card](https://docs.anthropic.com/en/docs/about-claude/models)

### Safety & Guardrails (`safety/`, 3 notebooks)

**Why:** Agents that act in the world need safety rails. Production agents MUST have guardrails.

| # | Notebook | What You Build |
|---|---------|---------------|
| 01 | `input_validation.ipynb` | Sanitizing user input, prompt injection detection, tool argument validation |
| 02 | `output_filtering.ipynb` | Content filtering, PII detection, response validation |
| 03 | `sandboxing_and_permissions.ipynb` | Sandboxed execution (E2B, Docker), permission models, rate limiting |

> **Key references:** [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/), [Anthropic safety docs](https://docs.anthropic.com/en/docs/build-with-claude/guardrails), [Simon Willison — Prompt Injection](https://simonwillison.net/series/prompt-injection/)

### Async & Production Patterns (`production/`, 4 notebooks)

**Why:** Real agent systems need to handle concurrency, streaming, and deployment.

| # | Notebook | What You Build |
|---|---------|---------------|
| 01 | `async_fundamentals.ipynb` | asyncio basics, async HTTP with httpx, parallel tool calls |
| 02 | `streaming_responses.ipynb` | Server-sent events, streaming LLM output, progressive rendering |
| 03 | `api_serving.ipynb` | Wrap an agent in a FastAPI endpoint, request/response patterns |
| 04 | `monitoring_and_cost.ipynb` | Token usage tracking, cost estimation, latency monitoring, alerting |

> **Key references:** [FastAPI docs](https://fastapi.tiangolo.com/), [httpx async docs](https://www.python-httpx.org/async/), [OpenRouter usage API](https://openrouter.ai/docs/api-reference)

### Domain-Specific Agent Patterns (`domain-agents/`, 4 notebooks)

**Why:** Different domains need different agent architectures. One size does not fit all.

| # | Notebook | What You Build |
|---|---------|---------------|
| 01 | `code_agent_patterns.ipynb` | Code review agent, code generation with testing, self-debugging loops |
| 02 | `research_agent_patterns.ipynb` | Web research → synthesis → citation pipeline, source verification |
| 03 | `data_analysis_agent.ipynb` | SQL/pandas agent, visualization generation, data Q&A |
| 04 | `document_agent.ipynb` | Document Q&A with RAG, multi-document summarization, knowledge base agent |

> **Key references:** [SWE-bench](https://www.swebench.com/), [OpenAI code interpreter patterns](https://platform.openai.com/docs/assistants/tools/code-interpreter)

### MCP & Tool Standards (`mcp/`, 3 notebooks)

**Why:** MCP (Model Context Protocol) is becoming the standard for tool interop. Agent builders need to know it.

| # | Notebook | What You Build |
|---|---------|---------------|
| 01 | `mcp_fundamentals.ipynb` | What MCP is, stdio vs HTTP transport, protocol structure |
| 02 | `building_mcp_servers.ipynb` | Build a custom MCP server that exposes tools |
| 03 | `mcp_with_smolagents.ipynb` | Connect smolagents to MCP servers, compose tools from multiple servers |

> **Key references:** [MCP specification](https://modelcontextprotocol.io/), [Anthropic MCP docs](https://docs.anthropic.com/en/docs/agents-and-tools/mcp), [smolagents MCP integration](https://huggingface.co/docs/smolagents/tutorials/mcp)

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

### ML Foundations
- [Karpathy — Neural Networks: Zero to Hero (YouTube)](https://karpathy.ai/zero-to-hero.html)
- [3Blue1Brown — Essence of Linear Algebra (YouTube)](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab)
- [3Blue1Brown — Essence of Calculus (YouTube)](https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr)
- [Fast.ai — Practical Deep Learning](https://course.fast.ai/)

---

## Dependencies

### Current (core + appendix)
- `httpx` — modern HTTP client
- `python-dotenv` — loads API keys from `.env`
- `jupyter` / `ipykernel` — notebook runtime
- `numpy` — used in the embeddings appendix notebook

### Phase 2 (smolagents)
- `smolagents[litellm,toolkit]` — agent framework + LiteLLM integration + default tools
- `gradio` — for GradioUI in notebook 11

### ML Foundations
- `torch` — PyTorch for notebooks 04-06
- `matplotlib` — for plotting loss curves and visualizations

---

## Progression Notes

- **Start with 01-05.** These are the foundation. Don't skip them.
- **06-11 are the smolagents layer.** Graduate from raw Python to a framework.
- **12-14, 15-17, 18-20 are independent phases.** Do them in any order based on interest.
- **21-22 are the capstone.** Do these last.
- **Additional paths are independent.** Pick them based on what you need — prompt engineering, eval, safety, production, etc.
- **ml-foundations is a separate track.** Do it if you want to go deep on ML before or alongside agents.
- **This roadmap is flexible.** Add notebooks, split them, merge them, skip them. It's a personal learning repo, not a curriculum.
