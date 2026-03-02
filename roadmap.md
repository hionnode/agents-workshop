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

A structured 14-notebook prerequisite path in 4 tiers (A, B, C, E). Each tier maps to a core phase or additional track — complete the tier before starting its corresponding phase. Tier D (ML Foundations) is housed separately in `ml-foundations/`. Skip any notebook you're already comfortable with.

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

### Tier E — Advanced Foundations (before new learning paths)

Foundational topics that are prerequisites for the expanded learning paths (production, multimodal, memory infrastructure, protocols).

| # | Notebook | Key Topics | Unlocks |
|---|----------|-----------|---------|
| 11 | `async_and_await.ipynb` | asyncio event loop, async/await, async generators, asyncio.gather | Production path, voice agents |
| 12 | `databases_and_sql.ipynb` | SQLite, basic SQL, SQLAlchemy ORM, connection patterns | Memory infrastructure, production |
| 13 | `websockets_and_streaming.ipynb` | WebSocket protocol, `websockets` library, SSE, streaming patterns | Voice agents, real-time agents |
| 14 | `graph_data_structures.ipynb` | Graphs, adjacency lists, traversal (BFS/DFS), NetworkX basics | Knowledge graphs, LangGraph, A2A |

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

| Appendix Tier | Unlocks | Why |
|---------------|---------|-----|
| **Tier A** (01–06) | **Core Phase 1** — Foundations | Core 01–05 require HTTP calls, JSON parsing, string manipulation, error handling, and basic Python fluency |
| **Tier B** (07–08) | **Core Phase 2** — smolagents | Core 06–11 use the `@tool` decorator, subclass `Tool`, and rely on type hints throughout |
| **Tier C** (09–10) | **Core Phase 3** — Memory & Knowledge | Core 12–14 read files, chunk text, compute embeddings, and do vector similarity search |
| **Tier D** (ml-foundations 01–06) | [Karpathy's Zero to Hero](https://karpathy.ai/zero-to-hero.html) | The 8-lecture series requires calculus, linear algebra, probability, and PyTorch fluency |
| **Tier E** (11–14) | Production, multimodal, memory, protocols paths | Async/await for concurrency, SQL for state persistence, WebSockets for streaming, graphs for knowledge graphs and LangGraph |

### Cross-links Between Tracks

- Appendix 10 (NumPy) → ml-foundations/02 (linear algebra uses NumPy extensively)
- Appendix 07 (Classes) → ml-foundations/04 (PyTorch's `nn.Module` is a class)
- Appendix 08 (Type Hints) → ml-foundations/04 (PyTorch type annotations)
- Appendix 04 (Strings) + 09 (File I/O) → Karpathy Lecture 8 (GPT Tokenizer)
- Appendix 11 (Async) → production/01 (async fundamentals), multimodal/03 (realtime voice)
- Appendix 12 (Databases) → memory/04 (long-term memory), production/05 (database for agents)
- Appendix 13 (WebSockets) → multimodal/03 (realtime voice), production/02 (streaming)
- Appendix 14 (Graphs) → memory/03 (knowledge graphs), frameworks/02 (LangGraph), protocols/03 (A2A)

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

### Evaluation & Debugging (`eval/`, 7 notebooks)

**Why:** "It works on my example" is not enough. Agents need systematic evaluation, modern benchmarks, and regression pipelines.

| # | Notebook | What You Build |
|---|---------|---------------|
| 01 | `tracing_and_logging.ipynb` | Structured logging for agent runs, trace visualization |
| 02 | `building_test_suites.ipynb` | Unit tests for tools, integration tests for agent loops, golden-answer tests |
| 03 | `benchmarking_agents.ipynb` | Run agents against standard benchmarks (GAIA, HotPotQA, simple custom evals) |
| 04 | `failure_modes.ipynb` | Common agent failures (loops, hallucinated tools, wrong tool selection) and fixes |
| 05 | `llm_as_judge.ipynb` | Use an LLM to evaluate agent outputs — rubric design, calibration, agreement metrics |
| 06 | `modern_benchmarks.ipynb` | Run agents against SWE-bench Lite, HumanEval, GAIA, and custom domain evals |
| 07 | `regression_testing.ipynb` | CI pipeline for agents — golden test sets, automated regression detection, version comparison |

> **Key references:** [GAIA benchmark](https://huggingface.co/gaia-benchmark), [SWE-bench](https://www.swebench.com/), [Braintrust](https://www.braintrust.dev/), [Anthropic eval guide](https://docs.anthropic.com/en/docs/build-with-claude/develop-tests)

### LLM Internals for Agent Builders (`llm-internals/`, 4 notebooks)

**Why:** Understanding how LLMs work makes you a better agent builder — you know WHY prompting tricks work.

| # | Notebook | What You Build |
|---|---------|---------------|
| 01 | `tokenization_deep_dive.ipynb` | Build a BPE tokenizer, understand context windows, token counting |
| 02 | `attention_and_context.ipynb` | How attention works (visual), context window management, long-context strategies |
| 03 | `sampling_and_generation.ipynb` | Temperature, top-p, top-k, repetition penalty — what each does and when to use it |
| 04 | `model_selection.ipynb` | Open vs closed models, cost/quality tradeoffs, when to use which model for agents |

> **Key references:** [Karpathy — Let's build the GPT Tokenizer](https://www.youtube.com/watch?v=zduSFxRajkE), [Jay Alammar — The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/), [Anthropic model card](https://docs.anthropic.com/en/docs/about-claude/models)

### Safety & Guardrails (`safety/`, 6 notebooks)

**Why:** Agents that act in the world need safety rails. Production agents MUST have guardrails. The OWASP Agentic Top 10 defines the threat landscape.

| # | Notebook | What You Build |
|---|---------|---------------|
| 01 | `input_validation.ipynb` | Sanitizing user input, prompt injection detection, tool argument validation |
| 02 | `output_filtering.ipynb` | Content filtering, PII detection, response validation |
| 03 | `sandboxing_and_permissions.ipynb` | Sandboxed execution (E2B, Docker), permission models, rate limiting |
| 04 | `owasp_agentic_top_10.ipynb` | Walk through all 10 agentic attack vectors: goal hijacking, tool misuse, identity abuse, rogue agents, etc. |
| 05 | `agent_authentication.ipynb` | OAuth 2.1 for agents — brokered credentials (LLM never sees API keys), PKCE, ephemeral tokens, MCP auth |
| 06 | `governance_and_least_agency.ipynb` | Bounded autonomy, mandatory escalation paths, audit trails, compliance patterns |

> **Key references:** [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/), [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/), [Anthropic safety docs](https://docs.anthropic.com/en/docs/build-with-claude/guardrails), [Simon Willison — Prompt Injection](https://simonwillison.net/series/prompt-injection/), [OAuth 2.1 for Agents (Descope)](https://www.descope.com/blog/post/oauth-vs-api-keys)

### Async & Production Patterns (`production/`, 8 notebooks)

**Why:** Real agent systems need to handle concurrency, streaming, deployment, and state management.

| # | Notebook | What You Build |
|---|---------|---------------|
| 01 | `async_fundamentals.ipynb` | asyncio basics, async HTTP with httpx, parallel tool calls |
| 02 | `streaming_responses.ipynb` | Server-sent events, streaming LLM output, progressive rendering |
| 03 | `api_serving.ipynb` | Wrap an agent in a FastAPI endpoint, request/response patterns |
| 04 | `monitoring_and_cost.ipynb` | Token usage tracking, cost estimation, latency monitoring, alerting |
| 05 | `database_for_agents.ipynb` | SQLite + SQLAlchemy for agent state persistence — sessions, memory, conversation history |
| 06 | `containerized_agents.ipynb` | Package an agent in Docker, deploy to a cloud platform (Modal, Fly.io, or Railway) |
| 07 | `agent_as_a_service.ipynb` | Full agent API: auth, rate limiting, session management, webhook callbacks |
| 08 | `managed_platforms.ipynb` | Survey of managed agent platforms: Amazon Bedrock AgentCore, Azure AI Foundry, Vertex AI Agent Builder |

> **Key references:** [FastAPI docs](https://fastapi.tiangolo.com/), [httpx async docs](https://www.python-httpx.org/async/), [OpenRouter usage API](https://openrouter.ai/docs/api-reference), [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/), [Modal](https://modal.com/), [Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/)

### Domain-Specific Agent Patterns (`domain-agents/`, 4 notebooks)

**Why:** Different domains need different agent architectures. One size does not fit all.

| # | Notebook | What You Build |
|---|---------|---------------|
| 01 | `code_agent_patterns.ipynb` | Code review agent, code generation with testing, self-debugging loops |
| 02 | `research_agent_patterns.ipynb` | Web research → synthesis → citation pipeline, source verification |
| 03 | `data_analysis_agent.ipynb` | SQL/pandas agent, visualization generation, data Q&A |
| 04 | `document_agent.ipynb` | Document Q&A with RAG, multi-document summarization, knowledge base agent |

> **Key references:** [SWE-bench](https://www.swebench.com/), [OpenAI code interpreter patterns](https://platform.openai.com/docs/assistants/tools/code-interpreter)

### Agent Framework Landscape (`frameworks/`, 5 notebooks)

**Why:** smolagents is great for learning, but agent builders encounter OpenAI Agents SDK, LangGraph, Pydantic AI, Strands, and others on the job. Understanding tradeoffs > framework lock-in.

| # | Notebook | What You Build |
|---|---------|---------------|
| 01 | `framework_landscape.ipynb` | Same agent in 4 frameworks (smolagents, OpenAI Agents SDK, LangGraph, Pydantic AI) — side-by-side comparison |
| 02 | `langgraph_deep_dive.ipynb` | Graph-based agent with cycles, conditionals, and parallel execution — the dominant architecture pattern |
| 03 | `openai_agents_sdk.ipynb` | Agent using OpenAI's Agents SDK — handoffs, guardrails, tracing, MCP integration |
| 04 | `pydantic_ai_agents.ipynb` | Type-safe agent with Pydantic AI — structured outputs, dependency injection, result validation |
| 05 | `choosing_a_framework.ipynb` | Decision framework: when to use which SDK, migration patterns, vendor lock-in strategies |

> **Key references:** [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/), [LangGraph docs](https://langchain-ai.github.io/langgraph/), [Pydantic AI docs](https://ai.pydantic.dev/), [Strands Agents (AWS)](https://github.com/strands-agents/sdk-python), [DSPy](https://dspy.ai/)

### Agent Protocols & Interoperability (`protocols/`, 4 notebooks)

**Why:** MCP (agent-to-tool) and A2A (agent-to-agent) are being called the "TCP/IP moment" for AI. MCP was donated to the Linux Foundation; OpenAI, Google, Microsoft all adopted it. A2A launched April 2025 with 50+ tech partners.

| # | Notebook | What You Build |
|---|---------|---------------|
| 01 | `mcp_from_scratch.ipynb` | Deep dive: MCP protocol structure, stdio vs HTTP transport, build a client and server from the spec |
| 02 | `building_mcp_servers.ipynb` | Production MCP server exposing custom tools — packaging, testing, deployment |
| 03 | `a2a_protocol.ipynb` | Google's Agent-to-Agent protocol — agent cards, capability discovery, task lifecycles, multipart messages |
| 04 | `mcp_plus_a2a.ipynb` | System using both: MCP for tool access (vertical) + A2A for agent collaboration (horizontal) |

> **Key references:** [MCP spec](https://modelcontextprotocol.io/), [A2A spec (Google)](https://google.github.io/A2A/), [MCP vs A2A comparison](https://www.clarifai.com/blog/mcp-vs-a2a-clearly-explained)

### Computer Use & Browser Agents (`browser-agents/`, 4 notebooks)

**Why:** One of the hottest areas in 2025-2026. Anthropic Computer Use API, Playwright MCP server, and purpose-built browser agents (Browserbase, Stagehand) are making browser automation a core agent capability.

| # | Notebook | What You Build |
|---|---------|---------------|
| 01 | `computer_use_basics.ipynb` | Anthropic's Computer Use API — controlling GUIs through screenshots + coordinate-based actions |
| 02 | `browser_agent.ipynb` | Browser agent using Playwright + LLM reasoning — navigate, click, fill forms, extract data |
| 03 | `playwright_mcp.ipynb` | Give any MCP-compatible agent browser control via the official Playwright MCP server |
| 04 | `web_scraping_agent.ipynb` | Agent that navigates multi-page sites, extracts structured data, handles pagination and auth |

> **Key references:** [Anthropic Computer Use docs](https://docs.anthropic.com/en/docs/agents-and-tools/computer-use), [Playwright MCP](https://github.com/microsoft/playwright-mcp), [Browserbase](https://www.browserbase.com/), [Stagehand](https://github.com/browserbase/stagehand)

### Voice & Multimodal Agents (`multimodal/`, 4 notebooks)

**Why:** Voice agents had a "Cambrian explosion" in 2025-2026. OpenAI's Realtime API went GA with WebRTC, native tool use, and MCP support. Vision-enabled agents unlock new tool categories (screenshot analysis, document understanding, chart reading).

| # | Notebook | What You Build |
|---|---------|---------------|
| 01 | `vision_agents.ipynb` | Agent that processes images — screenshot understanding, diagram analysis, chart reading + tool calling |
| 02 | `voice_pipeline.ipynb` | Voice agent pipeline: STT → LLM → TTS — using Whisper + your agent + a TTS API |
| 03 | `realtime_voice_agent.ipynb` | OpenAI Realtime API — bidirectional audio streaming, low-latency conversational agent with tool use |
| 04 | `multimodal_tool_use.ipynb` | Agent that combines text, image, and audio inputs to reason and call tools |

> **Key references:** [OpenAI Realtime API](https://platform.openai.com/docs/guides/realtime), [OpenAI Voice Agents guide](https://platform.openai.com/docs/guides/voice-agents), [Anthropic vision docs](https://docs.anthropic.com/en/docs/build-with-claude/vision)

### Agent Architecture Patterns (`patterns/`, 6 notebooks)

**Why:** The core track covers ReAct, planning, reflection, tree-of-thought, and multi-agent. But several patterns that became standard in 2025-2026 are missing — particularly event-driven, state-machine-based, and human-in-the-loop architectures.

| # | Notebook | What You Build |
|---|---------|---------------|
| 01 | `state_machines_for_agents.ipynb` | Model agent behavior as explicit FSMs — nodes = states/actions, edges = transitions. Foundation for LangGraph. |
| 02 | `event_driven_agents.ipynb` | Agent reacting to real-time events (webhooks, message queues) instead of request-response |
| 03 | `human_in_the_loop.ipynb` | Approval workflows, escalation thresholds, confidence-based routing to humans |
| 04 | `agentic_rag.ipynb` | Agent-controlled retrieval: decides when/what to retrieve, reformulates queries, does multi-hop retrieval |
| 05 | `deep_research_agent.ipynb` | Multi-step research: search → read → identify gaps → iterate → synthesize with citations |
| 06 | `workflow_orchestration.ipynb` | DAG-based workflows: parallel tool execution, conditional branching, error recovery, checkpointing |

> **Key references:** [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic), [Microsoft AI Agent Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns), [Confluent — Event-Driven Multi-Agent Systems](https://www.confluent.io/blog/event-driven-multi-agent-systems/)

### Agent Memory & Knowledge Infrastructure (`memory/`, 5 notebooks)

**Why:** Phase 3 covers basic conversation memory and RAG. Production memory is far more complex — hybrid storage, knowledge graphs, temporal memory, long-term personalization. Letta (MemGPT), Mem0, and Zep have defined the production patterns.

| # | Notebook | What You Build |
|---|---------|---------------|
| 01 | `memory_architectures.ipynb` | Survey: Letta's OS-inspired hierarchy (core/recall/archival), Mem0's hybrid datastore, Zep's episodic memory |
| 02 | `vector_databases.ipynb` | Hands-on with vector DBs: ChromaDB, Qdrant, pgvector — indexing, querying, hybrid search |
| 03 | `knowledge_graphs_for_agents.ipynb` | Graph-based memory: entities, relationships, temporal changes — using NetworkX + LLM extraction |
| 04 | `long_term_memory.ipynb` | Production pattern: vector DB (semantic) + graph DB (relationships) + SQLite (state) — the memory trifecta |
| 05 | `personalization_and_user_modeling.ipynb` | Agent that learns user preferences over time — preference extraction, profile building, adaptive behavior |

> **Key references:** [Letta (MemGPT)](https://www.letta.com/), [Mem0](https://mem0.ai/), [Zep](https://www.getzep.com/), [Anthropic — Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)

### Observability & Cost Optimization (`observability/`, 4 notebooks)

**Why:** 89% of organizations now implement agent observability. The tooling (Langfuse, Arize Phoenix, Braintrust) has matured. Without observability, you can't debug, improve, or manage costs for production agents.

| # | Notebook | What You Build |
|---|---------|---------------|
| 01 | `tracing_with_langfuse.ipynb` | Instrument an agent with Langfuse (open-source) — traces, spans, generations, scores |
| 02 | `opentelemetry_for_agents.ipynb` | OpenTelemetry/OpenInference standard — vendor-neutral agent tracing (the emerging standard) |
| 03 | `cost_optimization.ipynb` | Token tracking, cost estimation per run, model routing (cheap model for easy tasks, expensive for hard), caching strategies |
| 04 | `production_dashboards.ipynb` | Build monitoring dashboards: latency p50/p95, error rates, cost per session, tool success rates |

> **Key references:** [Langfuse docs](https://langfuse.com/docs), [Arize Phoenix](https://phoenix.arize.com/), [Braintrust](https://www.braintrust.dev/), [OpenInference spec](https://github.com/Arize-ai/openinference)

### Real-World Agent Projects (`projects/`, 6 notebooks)

**Why:** Learners need portfolio-worthy projects demonstrating different agent capabilities. Each project integrates multiple skills from the core track.

| # | Notebook | What You Build | Skills Demonstrated |
|---|---------|---------------|-------------------|
| 01 | `personal_knowledge_assistant.ipynb` | Agent that indexes your notes/docs, answers questions, and learns over time | RAG + memory + tools + conversation |
| 02 | `code_review_agent.ipynb` | Agent that reviews PRs: reads diffs, checks patterns, suggests improvements | Code understanding + structured output + multi-file |
| 03 | `customer_support_bot.ipynb` | Multi-turn support agent with knowledge base, escalation, and ticket creation | Memory + RAG + human-in-the-loop + tools |
| 04 | `data_analysis_agent.ipynb` | Agent that takes natural language → SQL → pandas → visualization → insights | CodeAgent + structured output + data tools |
| 05 | `multi_agent_research_team.ipynb` | 3+ agent system: researcher + analyst + writer + orchestrator | Multi-agent + planning + tool use |
| 06 | `browser_automation_project.ipynb` | Agent that automates a real workflow: fill forms, scrape data, generate report | Browser agent + tools + structured output |

> **Key references:** [SWE-bench](https://www.swebench.com/), [GAIA benchmark](https://huggingface.co/gaia-benchmark)

---

## Complete Track Inventory

| Track | Directory | Notebooks | Status |
|-------|-----------|-----------|--------|
| **Core: Agents** | `core/` | 22 | Planned (5 written) |
| **Appendix: Python** | `appendix/` | 14 (was 10) | 10 written + 4 new |
| **ML Foundations** | `ml-foundations/` | 6 | Planned |
| **Prompt Engineering** | `prompt-engineering/` | 4 | Planned |
| **Eval & Debugging** | `eval/` | 7 (was 4) | Expanded |
| **LLM Internals** | `llm-internals/` | 4 | Planned |
| **Safety & Guardrails** | `safety/` | 6 (was 3) | Expanded |
| **Async & Production** | `production/` | 8 (was 4) | Expanded |
| **Domain Agents** | `domain-agents/` | 4 | Planned |
| **Frameworks** | `frameworks/` | 5 | New |
| **Protocols** | `protocols/` | 4 | New (replaces `mcp/`) |
| **Browser Agents** | `browser-agents/` | 4 | New |
| **Multimodal** | `multimodal/` | 4 | New |
| **Architecture Patterns** | `patterns/` | 6 | New |
| **Memory Infrastructure** | `memory/` | 5 | New |
| **Observability** | `observability/` | 4 | New |
| **Projects** | `projects/` | 6 | New |
| **TOTAL** | | **113** | |

---

## Implementation Priority

Grouped by impact and interdependence:

### Wave 1 — Core gaps (implement first)
1. **Protocols** (`protocols/`) — replaces `mcp/`, the interoperability foundation
2. **Frameworks** (`frameworks/`) — learners will encounter these immediately
3. **Architecture Patterns** (`patterns/`) — fills real conceptual gaps

### Wave 2 — Hot areas
4. **Browser Agents** (`browser-agents/`) — high learner engagement
5. **Observability** (`observability/`) — practical debugging
6. **Safety expansion** (+3 notebooks) — OWASP, auth, governance

### Wave 3 — Depth
7. **Memory Infrastructure** (`memory/`) — beyond basic RAG
8. **Production expansion** (+4 notebooks) — deployment, databases
9. **Eval expansion** (+3 notebooks) — modern benchmarks

### Wave 4 — Specialized
10. **Multimodal** (`multimodal/`) — voice + vision
11. **Appendix Tier E** (+4 notebooks) — async, SQL, websockets, graphs
12. **Projects** (`projects/`) — portfolio pieces (do last, builds on everything)

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

### Expanded Paths (added as notebooks are implemented)
- `langgraph` — frameworks path (LangGraph deep dive)
- `openai-agents` — frameworks path (OpenAI Agents SDK)
- `pydantic-ai` — frameworks path (Pydantic AI)
- `playwright` — browser agents path
- `chromadb` — memory infrastructure path (vector databases)
- `networkx` — memory infrastructure path (knowledge graphs), appendix 14
- `sqlalchemy` — production path (database for agents), appendix 12
- `websockets` — appendix 13 (WebSocket protocol)
- `langfuse` — observability path (tracing)
- `opentelemetry-api` — observability path (vendor-neutral tracing)
- `fastapi` — production path (API serving)

---

## Progression Notes

- **Start with core 01-05.** These are the foundation. Don't skip them.
- **06-11 are the smolagents layer.** Graduate from raw Python to a framework.
- **12-14, 15-17, 18-20 are independent phases.** Do them in any order based on interest.
- **21-22 are the capstone.** Do these last.
- **Additional paths are independent.** Pick them based on what you need. The [implementation priority](#implementation-priority) section suggests a wave-based order, but follow your interests.
- **Protocols and Frameworks are the highest-impact additions.** If you're only going to do a few extra paths, start there.
- **Appendix Tier E is optional.** Only needed if the advanced paths expose gaps in your async, SQL, WebSocket, or graph knowledge.
- **Projects path should come last.** It integrates skills from multiple tracks — do it after completing the core track and at least one additional path.
- **ml-foundations is a separate track.** Do it if you want to go deep on ML before or alongside agents.
- **This roadmap is flexible.** Add notebooks, split them, merge them, skip them. It's a personal learning repo, not a curriculum.
