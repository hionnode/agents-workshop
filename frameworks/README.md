# Agent Framework Landscape — Lesson Plans

> Detailed lesson plans for notebooks 01–05. Understanding framework tradeoffs is more valuable than framework lock-in.
> For the full track overview, see [`../roadmap.md`](../roadmap.md).

---

## 01. Framework Landscape

**File:** `01_framework_landscape.ipynb`

### Overview

Build the same tool-calling agent — a weather lookup assistant — in four frameworks (smolagents, OpenAI Agents SDK, LangGraph, Pydantic AI) and compare them side by side. This notebook establishes the mental model for the entire track: every framework solves the same core problems (tool registration, agent loop, output parsing, error handling) but makes radically different design choices. By the end, you will have a concrete, code-level understanding of what each framework gives you for free and what it forces you to do yourself.

### Learning Objectives

By the end of this notebook, you will be able to:

- Implement the same tool-calling agent in smolagents, OpenAI Agents SDK, LangGraph, and Pydantic AI
- Identify the core abstractions each framework provides (tool registration, agent loop, state management, output parsing)
- Compare how each framework handles tool definitions, error recovery, and conversation history
- Articulate the architectural philosophy behind each framework (code-first vs graph-first vs type-first vs SDK-first)
- Evaluate framework tradeoffs along dimensions that matter: learning curve, flexibility, vendor lock-in, and observability
- Choose an appropriate framework for a given project based on concrete criteria rather than hype

### Prerequisites

- [`../core/06_intro_to_smolagents.ipynb`](../core/06_intro_to_smolagents.ipynb) — you need hands-on experience with at least one agent framework before comparing four
- [`../core/07_custom_tools.ipynb`](../core/07_custom_tools.ipynb) — tool registration patterns are the primary comparison axis in this notebook

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | The comparison agent | Define a shared task spec: a weather lookup agent with `get_weather` and `get_forecast` tools, a shared system prompt, and a fixed test conversation. This is the control for the experiment. |
| 2 | smolagents implementation | Build the agent using `@tool`, `ToolCallingAgent`, and `LiteLLMModel`. Observe how smolagents handles the tool loop, JSON parsing, and `agent.logs` for tracing. |
| 3 | OpenAI Agents SDK implementation | Build the agent using `@function_tool`, `Agent`, and `Runner.run()`. Observe the declarative agent definition, built-in guardrails hooks, and OpenAI-native tracing. |
| 4 | LangGraph implementation | Build the agent as a `StateGraph` with `MessagesState`, a `tools` node, and `tools_condition` routing. Observe the explicit graph structure, state immutability, and checkpoint-based persistence. |
| 5 | Pydantic AI implementation | Build the agent using `Agent`, `@agent.tool`, and `RunContext`. Observe type-safe dependency injection, result validators, and structured output via Pydantic models. |
| 6 | Side-by-side comparison | Compare all four implementations across 8 dimensions: lines of code, tool registration API, agent loop control, error handling, tracing/observability, model flexibility, state management, and extensibility. |
| 7 | Framework philosophy map | Map each framework to an architectural philosophy — smolagents (minimal, code-first), OpenAI Agents SDK (SDK-first, opinionated), LangGraph (graph-first, explicit state), Pydantic AI (type-first, validation-native). |
| 8 | When to use what (first pass) | Decision tree sketch: match project requirements (vendor lock-in tolerance, team size, type safety needs, graph complexity) to frameworks. This gets refined in notebook 05. |

### Putting It Together

Extend all four implementations to support a third tool — `get_air_quality(city: str)` — and add a multi-turn conversation where the user asks about weather, then air quality, then a forecast. Compare how each framework handles tool addition and conversation continuity. This exercise reveals which frameworks make iteration cheap and which impose ceremony.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Add a tool to all four | Starter | Add `get_air_quality` to each implementation and verify it works end-to-end. Note the number of lines changed per framework. |
| 2 | Error handling comparison | Moderate | Make `get_weather` raise an exception for a specific city. Compare how each framework surfaces the error to the LLM and whether it retries or fails gracefully. |
| 3 | Swap the model | Moderate | Switch all four implementations from the default model to a different OpenRouter model (e.g., `mistralai/mistral-7b-instruct`). Note which frameworks make this a one-line change and which require plumbing. |
| 4 | Framework benchmark | Stretch | Time each implementation over 10 identical runs. Measure latency, token usage, and success rate. Build a comparison table and identify which framework adds the most overhead. |

### Key References

- [smolagents Documentation](https://huggingface.co/docs/smolagents) — official docs covering ToolCallingAgent, CodeAgent, tools, multi-agent, and model integrations
- [OpenAI Agents SDK Documentation](https://openai.github.io/openai-agents-python/) — official guide covering agents, tools, handoffs, guardrails, and tracing
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/) — official docs covering StateGraph, nodes, edges, persistence, and human-in-the-loop
- [Pydantic AI Documentation](https://ai.pydantic.dev/) — official docs covering agents, tools, dependency injection, result validation, and structured outputs
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — framework-agnostic guide to agent architecture patterns and when to use workflows vs agents
- [Chip Huyen — Building A Generative AI Platform (2024)](https://huyenchip.com/2024/07/25/genai-platform.html) — industry perspective on AI infrastructure including framework selection tradeoffs

---

## 02. LangGraph Deep Dive

**File:** `02_langgraph_deep_dive.ipynb`

### Overview

LangGraph models agents as state machines: nodes are functions, edges are transitions, and state flows through the graph immutably. This notebook goes deep on the graph-based paradigm — you build agents with cycles, conditional branching, parallel fan-out, and persistent checkpoints. LangGraph's explicit state management makes it the dominant choice for complex, multi-step agent workflows where you need full control over execution flow, and understanding its patterns is essential even if you choose a different framework.

### Learning Objectives

By the end of this notebook, you will be able to:

- Build a `StateGraph` with typed state, nodes, conditional edges, and cycles
- Implement conditional branching using `add_conditional_edges` and custom routing functions
- Execute parallel tool calls using fan-out/fan-in patterns with `Send`
- Add persistent checkpointing with `MemorySaver` and `SqliteSaver` to enable resumable agents
- Implement human-in-the-loop workflows using `interrupt_before` and `Command(resume=...)`
- Debug LangGraph agents using `get_state`, `get_state_history`, and stream modes (`values`, `updates`, `messages`)

### Prerequisites

- [`01_framework_landscape.ipynb`](01_framework_landscape.ipynb) — you need the LangGraph basics from the comparison notebook before going deep
- [`../appendix/14_graph_data_structures.ipynb`](../appendix/14_graph_data_structures.ipynb) — graph terminology (nodes, edges, cycles, DAGs) is used throughout without re-explanation

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | StateGraph fundamentals | Build a minimal graph with `StateGraph`, `MessagesState`, `add_node`, `add_edge`, and `START`/`END`. Trace state flow through the graph manually. |
| 2 | Tool-calling agent graph | Build the standard ReAct pattern as a graph: `call_model` node, `tools` node, `tools_condition` routing. Compare to the raw Python ReAct loop from Core 05. |
| 3 | Custom state and reducers | Define custom `TypedDict` state with `Annotated` reducer functions (`add`, `replace`). Build an agent that tracks metadata (step count, tool call history, confidence scores) alongside messages. |
| 4 | Conditional branching | Build an agent that routes to different subgraphs based on LLM classification — e.g., "research" path vs "calculation" path vs "direct answer" path using `add_conditional_edges`. |
| 5 | Parallel execution with Send | Implement fan-out/fan-in: an agent that generates multiple search queries in parallel, executes them concurrently, then aggregates results in a synthesis node. |
| 6 | Persistence and checkpointing | Add `MemorySaver` checkpointing to the agent. Demonstrate state recovery after interruption, conversation continuation across sessions, and `get_state_history` for debugging. |
| 7 | Human-in-the-loop | Build an approval workflow: the agent proposes an action, execution pauses with `interrupt_before`, a human approves or rejects, and execution resumes with `Command(resume=...)`. |
| 8 | Subgraphs and composition | Compose a multi-agent system from subgraphs — a research agent subgraph and a writing agent subgraph orchestrated by a parent graph. Demonstrate state namespacing and cross-graph communication. |

### Putting It Together

Build a research assistant that: (1) takes a question, (2) generates 3 search queries in parallel using `Send`, (3) executes searches concurrently, (4) routes to either a "sufficient information" synthesis path or a "need more research" cycle based on a quality check, (5) pauses for human approval before delivering the final answer. This exercises conditional edges, parallel execution, cycles, human-in-the-loop, and checkpointing in a single coherent agent.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Add a retry cycle | Starter | Modify the tool-calling agent to retry failed tool calls up to 3 times before giving up. Track retry count in custom state. |
| 2 | Build a classification router | Moderate | Create a graph that classifies user input into 4 categories and routes to specialized subgraphs (math, code, research, chitchat), each with different tool sets. |
| 3 | Parallel tool execution | Moderate | Build an agent that calls 3 different APIs in parallel (weather, news, stocks), then synthesizes results. Use `Send` for fan-out and a collector node for fan-in. |
| 4 | Persistent conversation agent | Stretch | Build a multi-session agent using `SqliteSaver` that remembers previous conversations. Demonstrate resuming a conversation after "restarting" the agent. Include `get_state_history` to inspect past states. |

### Key References

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/) — official docs: concepts, how-to guides, API reference
- [LangGraph Tutorials](https://langchain-ai.github.io/langgraph/tutorials/) — official step-by-step tutorials covering quick start through advanced patterns
- [LangGraph Conceptual Guides](https://langchain-ai.github.io/langgraph/concepts/) — deep explanations of StateGraph, persistence, human-in-the-loop, streaming, and memory
- [LangGraph GitHub](https://github.com/langchain-ai/langgraph) — source code, examples, and issue discussions
- [LangGraph Platform](https://langchain-ai.github.io/langgraph/concepts/langgraph_platform/) — managed deployment option (LangGraph Cloud) for production agents
- [LangChain Blog — LangGraph Announcement](https://blog.langchain.dev/langgraph/) — original design rationale and motivation for the graph-based approach

---

## 03. OpenAI Agents SDK

**File:** `03_openai_agents_sdk.ipynb`

### Overview

OpenAI's Agents SDK is a production-grade framework that ships with opinionated defaults: declarative agent definitions, built-in guardrails, handoffs between specialized agents, structured tracing, and native MCP integration. This notebook builds a multi-agent system using the SDK's core primitives — you create specialized agents that hand off to each other, add input/output guardrails, instrument everything with traces, and connect to MCP servers for tool access. The SDK represents the "batteries-included" philosophy: maximum productivity at the cost of vendor alignment.

### Learning Objectives

By the end of this notebook, you will be able to:

- Define agents with `Agent` using instructions, tools, handoffs, and output types
- Implement tool functions using `@function_tool` with type-annotated parameters and docstrings
- Build multi-agent systems with handoffs using `Handoff` and transfer-of-control patterns
- Add input and output guardrails using `@input_guardrail` and `@output_guardrail` decorators
- Instrument agent runs with the built-in tracing system and inspect traces programmatically
- Connect agents to external tools via MCP servers using `MCPServerStdio` and `MCPServerStreamableHTTP`

### Prerequisites

- [`01_framework_landscape.ipynb`](01_framework_landscape.ipynb) — you need the OpenAI Agents SDK basics from the comparison notebook before going deep

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Agent definition and Runner | Define an `Agent` with instructions and tools, run it with `Runner.run()` and `Runner.run_streamed()`. Inspect the `RunResult` object: final output, new messages, raw responses, and last agent. |
| 2 | Function tools deep dive | Build tools with `@function_tool`, explore automatic schema generation from type hints, add `FunctionTool` with custom error handling, and use `tool_use_behavior` to control how tool results are processed. |
| 3 | Structured output with output types | Set `output_type` on an agent to a Pydantic model. Build an agent that always returns structured JSON — travel itineraries, analysis reports, or classification results. Compare to freeform text output. |
| 4 | Handoffs and multi-agent routing | Build a triage agent that hands off to specialist agents (billing, technical support, general). Implement `Handoff` with custom `on_handoff` callbacks, input filters, and transfer messages. |
| 5 | Guardrails | Add `@input_guardrail` to block prompt injection attempts and `@output_guardrail` to validate response quality. Build guardrails that use a secondary LLM call for classification. Handle `GuardrailFunctionOutput` with tripwire behavior. |
| 6 | Tracing and observability | Enable the built-in tracing system. Create custom `@trace` spans, inspect traces via the `traces` module, and understand the span hierarchy: agent spans, tool spans, LLM spans, guardrail spans. Export traces for external analysis. |
| 7 | MCP integration | Connect an agent to MCP servers using `MCPServerStdio` (local process) and `MCPServerStreamableHTTP` (remote). Give the agent access to filesystem tools, database tools, or custom MCP servers. |
| 8 | Using with non-OpenAI models | Configure the SDK to use non-OpenAI models via `set_default_openai_client` or custom `Model` implementations. Test with OpenRouter models. Understand what works and what breaks outside the OpenAI ecosystem. |

### Putting It Together

Build a customer support system with three agents: a triage agent, a billing agent, and a technical support agent. The triage agent classifies incoming requests and hands off to the appropriate specialist. Each specialist has domain-specific tools (billing: `lookup_invoice`, `process_refund`; technical: `search_docs`, `create_ticket`). Add input guardrails to block abusive messages, output guardrails to ensure PII is not leaked, and tracing to capture the full execution flow. Connect the technical agent to a documentation MCP server for knowledge retrieval.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Add a specialist agent | Starter | Add a "shipping" specialist to the customer support system with `track_package` and `update_address` tools. Update the triage agent's handoff logic. |
| 2 | Build a guardrail chain | Moderate | Create three guardrails (prompt injection detection, topic classification, PII detection) and chain them on a single agent. Test with adversarial inputs that should trigger each guardrail. |
| 3 | Trace analysis | Moderate | Run the multi-agent system 10 times with varied inputs. Export all traces and build a summary: average latency per agent, handoff frequency, guardrail trigger rate, tool call distribution. |
| 4 | MCP-powered research agent | Stretch | Build a research agent that connects to a web search MCP server and a filesystem MCP server. The agent searches the web, saves relevant content to local files, and produces a summary report with citations. |

### Key References

- [OpenAI Agents SDK Documentation](https://openai.github.io/openai-agents-python/) — official guide: quickstart, agents, tools, handoffs, guardrails, tracing, MCP, models, voice
- [OpenAI Agents SDK GitHub](https://github.com/openai/openai-agents-python) — source code, examples, and issue tracker
- [OpenAI Agents SDK — Models](https://openai.github.io/openai-agents-python/models/) — how to use non-OpenAI models, custom providers, and model configuration
- [OpenAI Agents SDK — Tracing](https://openai.github.io/openai-agents-python/tracing/) — built-in tracing system, custom spans, and external trace processors
- [OpenAI Agents SDK — MCP](https://openai.github.io/openai-agents-python/mcp/) — connecting to MCP servers for tool discovery and execution
- [MCP Specification](https://modelcontextprotocol.io/) — the Model Context Protocol spec for understanding what MCP servers provide

---

## 04. Pydantic AI Agents

**File:** `04_pydantic_ai_agents.ipynb`

### Overview

Pydantic AI brings the "if it compiles, it works" philosophy to agents: tools have typed parameters, agents return validated Pydantic models, dependencies are injected at runtime, and result validators catch semantic errors before they reach the user. This notebook builds type-safe agents that leverage Pydantic's validation ecosystem — you will use dependency injection for database connections and API clients, define structured output schemas, build result validators that check business logic, and see how type safety eliminates entire categories of agent bugs at development time rather than in production.

### Learning Objectives

By the end of this notebook, you will be able to:

- Define agents with `Agent` using typed `result_type`, `deps_type`, and system prompts
- Build tools with `@agent.tool` that receive `RunContext[DepsType]` for dependency injection
- Use Pydantic models as `result_type` to enforce structured, validated agent outputs
- Implement result validators with `@agent.result_validator` to enforce business logic constraints
- Manage agent dependencies using `deps_type` for database connections, API clients, and configuration
- Stream structured responses using `agent.run_stream()` with typed partial results

### Prerequisites

- [`01_framework_landscape.ipynb`](01_framework_landscape.ipynb) — you need the Pydantic AI basics from the comparison notebook before going deep
- [`../appendix/08_decorators_and_type_hints.ipynb`](../appendix/08_decorators_and_type_hints.ipynb) — type annotations and decorator mechanics are foundational to every Pydantic AI pattern

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Agent basics and system prompts | Define an `Agent` with a model, system prompt, and `result_type=str`. Run it with `agent.run()` and `agent.run_sync()`. Inspect `RunResult`: data, usage, all messages, and new messages. |
| 2 | Structured output with result types | Set `result_type` to a Pydantic model (e.g., `TravelItinerary`, `AnalysisReport`). Build agents that always return validated, structured data. Compare to JSON-mode prompting and see how Pydantic validation catches malformed outputs automatically. |
| 3 | Tools with RunContext | Build tools using `@agent.tool` that receive `RunContext` for accessing dependencies. Implement `get_weather(ctx: RunContext[WeatherDeps], city: str)` where `WeatherDeps` carries the API client. Compare to smolagents `@tool` and OpenAI `@function_tool`. |
| 4 | Dependency injection | Define `deps_type` as a dataclass carrying a database connection, API client, and config. Pass deps at `agent.run(deps=...)`. Build an agent where tools query a SQLite database and call external APIs through injected dependencies — no global state. |
| 5 | Result validators | Add `@agent.result_validator` to enforce business rules the LLM cannot guarantee — e.g., "all recommended items must exist in the database", "total cost must be under budget", "no PII in the response". When validation fails, the agent automatically retries with the error message. |
| 6 | Dynamic system prompts | Use `@agent.system_prompt` as a decorator to build system prompts dynamically based on `RunContext` — e.g., include the current user's name, role, and preferences from the database. Compare to static string prompts. |
| 7 | Streaming structured responses | Use `agent.run_stream()` to stream partial structured responses. Build a UI-friendly pattern where fields of a Pydantic model appear incrementally as the LLM generates them. Handle `StreamedRunResult` and typed partial results. |
| 8 | Multi-agent patterns | Build a two-agent system: a classifier agent that returns an `enum` result type, and specialist agents that receive the classification as a dependency. Demonstrate agent composition without a framework-level orchestration primitive. |

### Putting It Together

Build a travel planning agent that: takes a user's travel preferences as input, queries a database of destinations and hotels via injected dependencies, returns a validated `TravelPlan` Pydantic model (destinations, hotels, daily itinerary, estimated budget), runs a result validator that checks all hotels exist in the database and the total budget is within the user's limit, and streams the itinerary to the console as it generates. This exercises every major Pydantic AI feature: typed deps, structured output, result validation, dynamic system prompts, and streaming.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Structured output agent | Starter | Build an agent that takes a news article URL and returns a `NewsAnalysis` Pydantic model with `title`, `summary`, `sentiment`, `key_entities`, and `topics`. Validate that `sentiment` is one of `positive`, `negative`, `neutral`. |
| 2 | Dependency injection practice | Moderate | Build an agent with a `deps_type` carrying a dictionary of user preferences. The agent recommends books based on preferences, and tools access the preferences through `RunContext`. Add a result validator that checks all recommended books exist in a mock catalog. |
| 3 | Multi-model comparison | Moderate | Create the same agent with `result_type=AnalysisReport` but configure it to use 3 different models (via OpenRouter). Compare structured output quality, validation pass rate, and latency across models. |
| 4 | Full-stack Pydantic AI app | Stretch | Build a FastAPI endpoint that wraps a Pydantic AI agent. The endpoint accepts a request body (Pydantic model), injects database deps, runs the agent, and returns the validated result. Add streaming support via SSE. |

### Key References

- [Pydantic AI Documentation](https://ai.pydantic.dev/) — official docs: agents, tools, dependencies, results, testing, debugging
- [Pydantic AI — Agents](https://ai.pydantic.dev/agents/) — agent definition, system prompts, result types, and model configuration
- [Pydantic AI — Tools](https://ai.pydantic.dev/tools/) — tool definition, RunContext, dependency injection, and tool retries
- [Pydantic AI — Results](https://ai.pydantic.dev/results/) — result types, result validators, streaming, and usage tracking
- [Pydantic AI — Dependencies](https://ai.pydantic.dev/dependencies/) — dependency injection patterns, testing with mock deps, and override patterns
- [Pydantic Documentation](https://docs.pydantic.dev/) — the Pydantic validation library that underpins Pydantic AI's type safety
- [Pydantic AI GitHub](https://github.com/pydantic/pydantic-ai) — source code, examples, and issue discussions
- [Samuel Colvin — Pydantic AI Announcement](https://blog.pydantic.dev/blog/2024/12/05/pydantic-ai/) — design rationale and philosophy from the Pydantic creator

---

## 05. Choosing a Framework

**File:** `05_choosing_a_framework.ipynb`

### Overview

After building with all four frameworks, this notebook synthesizes everything into a practical decision framework. You build a scoring rubric, evaluate each framework against real project requirements, explore migration patterns between frameworks, and develop strategies for minimizing vendor lock-in. This is the notebook you revisit when starting a new agent project — it gives you a systematic way to choose rather than defaulting to whatever you used last. It also surveys the broader landscape (DSPy, CrewAI, AutoGen, Strands Agents) so you know what else is out there.

### Learning Objectives

By the end of this notebook, you will be able to:

- Apply a structured decision framework to select an agent SDK for a new project
- Evaluate frameworks across 10+ dimensions (learning curve, type safety, observability, vendor lock-in, community, multi-agent support, deployment, cost)
- Design a tool abstraction layer that allows migrating between frameworks without rewriting tool logic
- Identify the minimal portable core (tools, prompts, evaluation data) that should remain framework-agnostic
- Assess emerging frameworks (DSPy, CrewAI, AutoGen, Strands Agents) and determine when they are a better fit than the big four
- Build a migration checklist for moving an agent from one framework to another

### Prerequisites

- [`01_framework_landscape.ipynb`](01_framework_landscape.ipynb) — the comparison foundation
- [`02_langgraph_deep_dive.ipynb`](02_langgraph_deep_dive.ipynb) — deep understanding of the graph-based approach
- [`03_openai_agents_sdk.ipynb`](03_openai_agents_sdk.ipynb) — deep understanding of the SDK-first approach
- [`04_pydantic_ai_agents.ipynb`](04_pydantic_ai_agents.ipynb) — deep understanding of the type-safe approach

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | The decision dimensions | Define 12 evaluation dimensions: learning curve, type safety, model flexibility, multi-agent support, state management, observability, deployment story, community/ecosystem, MCP support, streaming support, cost overhead, and vendor lock-in risk. Weight each dimension by project type (prototype, production, research). |
| 2 | Framework scorecards | Build a quantitative scorecard for each framework across all dimensions. Ground scores in specific evidence from notebooks 01-04 (code examples, API surface area, documentation quality, GitHub activity). |
| 3 | Project archetypes | Define 5 project archetypes (quick prototype, production SaaS, research experiment, enterprise integration, personal tool) and map each to a recommended framework with justification. Show that the "best" framework changes with the use case. |
| 4 | The portability layer | Build a thin abstraction: a `PortableTool` base class and adapter functions that convert tools between frameworks. Demonstrate the same tool definition working in smolagents, OpenAI Agents SDK, LangGraph, and Pydantic AI without rewriting business logic. |
| 5 | Migration patterns | Walk through three concrete migrations: smolagents to LangGraph (adding state management), OpenAI Agents SDK to Pydantic AI (removing vendor lock-in), and LangGraph to smolagents (reducing complexity). Identify what migrates easily (tools, prompts) and what does not (state graphs, handoff logic). |
| 6 | The broader landscape | Survey frameworks not covered in depth: DSPy (prompt optimization), CrewAI (role-based multi-agent), AutoGen (conversation-driven), Strands Agents (AWS, model-driven), LlamaIndex Workflows (data-focused). For each: 2-sentence philosophy, when it shines, when to avoid. |
| 7 | Vendor lock-in strategies | Identify the three layers of lock-in (model, framework, platform) and strategies for each: portable tool definitions, model abstraction via LiteLLM/OpenRouter, prompt templates as data, evaluation suites as framework-agnostic test harnesses. |
| 8 | Your decision checklist | Build a reusable one-page checklist: given a new project, answer 8 questions, score frameworks, and arrive at a recommendation. Run the checklist against 3 hypothetical projects to validate it. |

### Putting It Together

Apply the full decision framework to a real project: a customer-facing support agent that needs multi-turn conversation, tool calling (CRM lookup, ticket creation, knowledge base search), human-in-the-loop escalation, structured output (ticket objects), and production deployment. Score all four frameworks, select one with justification, identify the portable core that should remain framework-agnostic, and outline a migration plan in case the choice proves wrong. This is the exercise that makes the decision framework practical rather than theoretical.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Score a new framework | Starter | Pick a framework not covered in depth (DSPy, CrewAI, AutoGen, or Strands) and score it on all 12 dimensions using the scorecard template. Compare to the big four. |
| 2 | Build a portable tool library | Moderate | Take 3 tools from the core track (weather lookup, web search, file reader) and implement them as `PortableTool` instances with adapters for all four frameworks. Verify each adapter produces a working agent. |
| 3 | Migration dry run | Moderate | Take the LangGraph research assistant from notebook 02 and migrate it to Pydantic AI. Document every change, measure the effort, and identify what was lost in translation (e.g., parallel execution, checkpointing). |
| 4 | Decision framework for your project | Stretch | Apply the full decision checklist to a real project you want to build. Score all frameworks, select one, write a 1-page justification, identify your portable core, and outline your lock-in mitigation strategy. Present your analysis as a markdown document. |

### Key References

- [DSPy Documentation](https://dspy.ai/) — programming (not prompting) language models: automatic prompt optimization, few-shot compilation, and modular LM programs
- [Strands Agents SDK (AWS)](https://github.com/strands-agents/sdk-python) — AWS's open-source agent framework: model-driven execution, built-in tools, and natural Python development
- [CrewAI Documentation](https://docs.crewai.com/) — role-based multi-agent framework: agents with roles, goals, and backstories collaborating on tasks
- [AutoGen Documentation](https://microsoft.github.io/autogen/) — Microsoft's conversation-driven multi-agent framework with human-in-the-loop patterns
- [LlamaIndex Workflows](https://docs.llamaindex.ai/en/stable/understanding/workflows/) — data-focused agent framework: document indexing, retrieval, and query pipelines
- [Chip Huyen — Building A Generative AI Platform (2024)](https://huyenchip.com/2024/07/25/genai-platform.html) — industry perspective on the AI infrastructure stack and framework selection
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — when you need an agent vs a workflow, and the patterns that work regardless of framework
- [LiteLLM Documentation](https://docs.litellm.ai/) — model abstraction layer that enables framework-agnostic model access across 100+ providers
