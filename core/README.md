# Core Track: Building Agents from Scratch — Lesson Plans

> Detailed lesson plans for notebooks 06–22. For the full track overview, see [`../roadmap.md`](../roadmap.md).
> Notebooks 01–05 are already written — see them in this directory.

---

## 06. Intro to smolagents

**File:** `06_intro_to_smolagents.ipynb`

### Overview

This notebook bridges the gap between raw Python agents and a real framework. You'll rebuild the agents from Phase 1 using smolagents — HuggingFace's minimal agent SDK — and see how the framework handles the plumbing you wrote by hand (tool dispatch, output parsing, agent loops). Understanding what smolagents automates (and what it doesn't) is key to using any agent framework effectively.

### Learning Objectives

By the end of this notebook, you will be able to:
- Install and configure smolagents with LiteLLM for OpenRouter model access
- Explain the difference between `CodeAgent` and `ToolCallingAgent` and when to use each
- Build a working agent with `ToolCallingAgent` that uses built-in tools
- Read and interpret `agent.logs` and trace output to debug agent behavior
- Compare raw-Python agent code (from Phase 1) with the equivalent smolagents code
- Use `write_memory_to_messages()` to inspect and understand the agent's internal message history

### Prerequisites

- [05. ReAct Agent](05_react_agent.ipynb) — the raw-Python agent you'll now rebuild with a framework
- [Appendix 07. Classes and OOP](../appendix/07_classes_and_oop.ipynb) — smolagents uses class inheritance heavily
- [Appendix 08. Decorators and Type Hints](../appendix/08_decorators_and_type_hints.ipynb) — the `@tool` decorator and type annotations

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Why a Framework? | Compare the ~100 lines of raw ReAct code from NB 05 to the equivalent ~10 lines with smolagents. Understand what the framework handles. |
| 2 | Installation and LiteLLM Setup | Install `smolagents[litellm]`, configure `LiteLLMModel` to route through OpenRouter, verify with a test call. |
| 3 | Your First smolagents Agent | Build a `ToolCallingAgent` with a calculator tool. Run a query and inspect the result. |
| 4 | CodeAgent vs ToolCallingAgent | Build the same agent as a `CodeAgent`. Compare how each formats tool calls (JSON vs Python code). Discuss tradeoffs. |
| 5 | Reading Agent Traces | Dive into `agent.logs` — understand the trace format: `TaskStep`, `ActionStep`, `tool_calls`, `observations`. |
| 6 | Rebuilding Phase 1 Agents | Recreate the weather + calculator + search agent from NB 05 in smolagents. Side-by-side comparison with the raw version. |
| 7 | Memory and Message History | Use `write_memory_to_messages()` to inspect how smolagents constructs the LLM prompt internally. Compare to your manual scratchpad. |
| 8 | When to Use Raw Python vs Framework | Decision framework: prototype speed vs control, debugging ease vs abstraction cost. |

### Putting It Together

Rebuild the multi-step conditional agent from NB 05's capstone ("If it's above 20C in Paris...") using smolagents. Compare the trace output side-by-side with the raw Python scratchpad to see exactly what the framework adds and removes.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Swap Models | Starter | Run the same agent with 3 different OpenRouter models via LiteLLM. Compare response quality and latency. |
| 2 | Trace Inspector | Starter | Write a function that takes `agent.logs` and prints a clean summary: step count, tools called, tokens used per step. |
| 3 | CodeAgent Challenge | Synthesis | Solve a multi-step math word problem using `CodeAgent`. Inspect the generated Python code and explain each step. |
| 4 | Framework Overhead Benchmark | Stretch | Time the same 5 queries on both your raw ReAct agent and the smolagents version. Measure latency difference and identify where the overhead comes from. |

### Key References

- [smolagents Documentation](https://huggingface.co/docs/smolagents) — official docs, start here
- [smolagents GitHub](https://github.com/huggingface/smolagents) — source code and examples
- [smolagents Guided Tour](https://huggingface.co/docs/smolagents/guided_tour) — step-by-step walkthrough
- [LiteLLM Documentation](https://docs.litellm.ai/) — the model routing layer smolagents uses
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — framework-agnostic agent design principles

---

## 07. Custom Tools

**File:** `07_custom_tools.ipynb`

### Overview

Tools are how agents interact with the world — APIs, databases, file systems, calculators, search engines. This notebook teaches you to build custom tools for smolagents using both the `@tool` decorator (quick and simple) and the `Tool` subclass (full control). You'll learn what makes a good tool description, how to debug tool failures, and how to test tools in isolation before wiring them into an agent.

### Learning Objectives

By the end of this notebook, you will be able to:
- Create tools using the `@tool` decorator with proper type hints and docstrings
- Build tools using the `Tool` subclass with `forward()`, custom `inputs`, and `output_type`
- Write tool descriptions that help the LLM choose and use tools correctly
- Debug common tool failures: wrong arguments, missing returns, type mismatches
- Test tools independently before integrating them into an agent

### Prerequisites

- [06. Intro to smolagents](06_intro_to_smolagents.ipynb) — agent basics with the framework
- [Appendix 08. Decorators and Type Hints](../appendix/08_decorators_and_type_hints.ipynb) — how `@tool` works under the hood

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | The `@tool` Decorator | Build a calculator tool with `@tool`. Understand how smolagents extracts the name, description, and schema from the function signature and docstring. |
| 2 | Type Hints Drive the Schema | See how `str`, `int`, `float`, `list[str]`, and `Optional` type hints map to the tool's JSON schema. What happens when types are wrong or missing. |
| 3 | Tool Descriptions That Work | Compare good and bad tool descriptions. Guidelines: be specific, include examples, describe edge cases, state what the tool does NOT do. |
| 4 | The `Tool` Subclass | Build the same calculator as a `Tool` subclass with `forward()`, `inputs`, `output_type`, and `description`. When to use this over `@tool`. |
| 5 | Tools That Call APIs | Build a tool that calls a real API (e.g., a weather API or dictionary API). Handle errors, timeouts, and rate limits inside the tool. |
| 6 | Debugging Tools | Common failure modes: tool returns `None`, wrong argument types, description confuses the LLM. Debugging workflow using `agent.logs`. |
| 7 | Testing Tools in Isolation | Write test calls for each tool before wiring them into an agent. Verify input/output contracts. |
| 8 | Composing a Multi-Tool Agent | Wire 3-4 custom tools into a `ToolCallingAgent`, run multi-step queries, and trace which tools get selected. |

### Putting It Together

Build a "personal assistant" agent with 4 custom tools: a calculator, a dictionary lookup, a unit converter, and a note-taker. Run a complex query that requires chaining multiple tools and trace the agent's tool selection decisions.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | `@tool` vs `Tool` Subclass | Starter | Implement the same tool both ways. Compare the resulting schemas by inspecting `tool.inputs` and `tool.description`. |
| 2 | Bad Descriptions | Starter | Deliberately write a vague tool description and observe how the agent misuses the tool. Fix the description and compare. |
| 3 | API-Backed Tool | Synthesis | Build a tool that calls a public API (e.g., Open Trivia DB, REST Countries) and returns formatted results. Handle API errors gracefully. |
| 4 | Tool Auto-Generator | Stretch | Write a function that takes any Python function with type hints and generates a `Tool` subclass automatically. Compare to what `@tool` does internally. |

### Key References

- [smolagents — Tools Guide](https://huggingface.co/docs/smolagents/tools) — official tool documentation
- [smolagents — Tool Subclass API](https://huggingface.co/docs/smolagents/reference/tools) — API reference for `Tool`
- [Anthropic — Tool Use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview) — general tool-use design patterns
- [OpenAI — Function Calling Guide](https://platform.openai.com/docs/guides/function-calling) — JSON schema patterns for tool definitions
- [JSON Schema Reference](https://json-schema.org/understanding-json-schema/) — the standard smolagents uses for tool inputs

---

## 08. Code Agent Deep Dive

**File:** `08_code_agent_deep_dive.ipynb`

### Overview

`CodeAgent` is smolagents' most powerful agent type — instead of emitting JSON tool calls, it writes and executes Python code to solve problems. This notebook explores how `CodeAgent` works internally: the `LocalPythonExecutor`, authorized imports, state persistence across steps, the system prompt that teaches the LLM to write code, and sandboxing options (E2B, Docker) for safe execution.

### Learning Objectives

By the end of this notebook, you will be able to:
- Explain how `CodeAgent` generates and executes Python code instead of JSON tool calls
- Configure `additional_authorized_imports` to give the agent access to libraries like `math`, `re`, `json`
- Understand how the `LocalPythonExecutor` maintains state across execution steps
- Compare local execution vs sandboxed execution (E2B, Docker) and explain the security tradeoffs
- Read and modify the `CodeAgent` system prompt to customize agent behavior
- Debug code execution failures by inspecting the generated code and error messages

### Prerequisites

- [06. Intro to smolagents](06_intro_to_smolagents.ipynb) — `CodeAgent` basics
- [07. Custom Tools](07_custom_tools.ipynb) — tools that `CodeAgent` can call from generated code

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | How CodeAgent Works | Trace through a `CodeAgent` run: prompt → LLM generates Python → executor runs it → result feeds back. Compare to `ToolCallingAgent`. |
| 2 | The LocalPythonExecutor | How the executor parses and runs code safely. What's allowed and forbidden by default. How `state` persists variables across steps. |
| 3 | Authorized Imports | Configure `additional_authorized_imports` to let the agent use `math`, `re`, `json`, `datetime`, etc. Security implications. |
| 4 | State Persistence | Demonstrate how variables created in step 1 are available in step 2. The agent can build up complex data structures across steps. |
| 5 | The CodeAgent System Prompt | Read and analyze the system prompt. Understand how it teaches the LLM to write executable Python with `print()` for observations. |
| 6 | Customizing the System Prompt | Modify the system prompt to add constraints (e.g., "always use list comprehensions", "add type hints"). Observe behavior changes. |
| 7 | Sandboxing: E2B and Docker | Run the same agent in E2B's cloud sandbox and a local Docker container. Compare setup, latency, and security guarantees. |
| 8 | When CodeAgent Shines | Patterns where `CodeAgent` excels: data manipulation, multi-step computation, string processing, generating visualizations. |

### Putting It Together

Build a `CodeAgent` that solves a data analysis task: given a CSV-like data string, the agent writes code to parse it, compute statistics, sort the results, and format a summary. Trace the generated code at each step.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Import Explorer | Starter | Try different `additional_authorized_imports` lists. What happens when the agent tries to use an unauthorized import? |
| 2 | State Debugger | Starter | Write a helper that prints the executor's `state` dict after each step, showing all variables the agent has created. |
| 3 | Prompt Surgery | Synthesis | Modify the `CodeAgent` system prompt to make the agent always include error handling (`try/except`) in generated code. Test with edge cases. |
| 4 | Sandbox Benchmark | Stretch | Run the same 5 tasks on `LocalPythonExecutor`, E2B, and Docker. Compare latency, failure rates, and output quality. |

### Key References

- [smolagents — Code Agents](https://huggingface.co/docs/smolagents/guided_tour#code-agents) — how CodeAgent works
- [smolagents — Secure Code Execution](https://huggingface.co/docs/smolagents/secure_code_execution) — E2B and Docker sandboxing
- [E2B Documentation](https://e2b.dev/docs) — cloud code sandboxing
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — code generation patterns
- [OpenAI Code Interpreter](https://platform.openai.com/docs/assistants/tools/code-interpreter) — a similar concept in OpenAI's ecosystem

---

## 09. Tool Ecosystem

**File:** `09_tool_ecosystem.ipynb`

### Overview

Agents become powerful when they access a rich ecosystem of tools beyond what you build yourself. This notebook covers smolagents' tool ecosystem: loading community tools from the Hub, connecting to Gradio Spaces as tools, integrating MCP servers, interoperating with LangChain tools, and managing an agent's toolbox at runtime. By the end, your agent can tap into hundreds of pre-built capabilities.

### Learning Objectives

By the end of this notebook, you will be able to:
- Load and use community tools from the HuggingFace Hub with `Tool.from_hub()`
- Connect Gradio Spaces as agent tools with `Tool.from_space()`
- Integrate MCP servers into smolagents using `MCPClient`
- Convert LangChain tools for use in smolagents
- Add and remove tools from an agent's toolbox at runtime
- Evaluate third-party tools for quality, security, and reliability before using them

### Prerequisites

- [06. Intro to smolagents](06_intro_to_smolagents.ipynb) — framework basics
- [07. Custom Tools](07_custom_tools.ipynb) — understanding tool schemas and descriptions

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | The Tool Ecosystem Landscape | Overview: Hub tools, Gradio Spaces, MCP servers, LangChain tools. When to build vs borrow. |
| 2 | Hub Tools with `load_tool()` | Load default tools (web search, python interpreter). Inspect schemas and test. |
| 3 | Community Tools with `Tool.from_hub()` | Browse and load community-contributed tools from HuggingFace Hub. Evaluate quality. |
| 4 | Gradio Spaces as Tools | Use `Tool.from_space()` to turn any Gradio Space into an agent tool. Handle async Spaces and GPU queues. |
| 5 | MCP Integration | Connect an MCP server using `MCPClient`. Use MCP tools alongside native smolagents tools. |
| 6 | LangChain Tool Interop | Convert LangChain tools (via `from_langchain()`) for use in smolagents. Handle schema differences. |
| 7 | Runtime Toolbox Management | Add/remove tools mid-session with `agent.tools`. Dynamic tool loading based on task type. |
| 8 | Evaluating Third-Party Tools | Checklist: description quality, input validation, error handling, security risks, rate limits. |

### Putting It Together

Build an agent with a mixed toolbox: 2 custom tools, 1 Hub tool, 1 Gradio Space tool, and 1 MCP tool. Run a complex query that exercises at least 3 different tool sources and trace which tools from which ecosystems get called.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Hub Explorer | Starter | Browse the HuggingFace Hub for agent tools. Load 3 different tools and test each with sample inputs. |
| 2 | Gradio Space Tool | Starter | Find a Gradio Space (e.g., image captioning, translation) and wire it into an agent as a tool. |
| 3 | MCP Server Setup | Synthesis | Start a local MCP server (e.g., filesystem or SQLite) and connect it to a smolagents agent via `MCPClient`. |
| 4 | Tool Router | Stretch | Build a system that dynamically selects which tools to load based on the user's query category (math, research, code, etc.). |

### Key References

- [smolagents — Tools Guide](https://huggingface.co/docs/smolagents/tools) — full tools documentation
- [smolagents — MCP Integration](https://huggingface.co/docs/smolagents/reference/tools#smolagents.MCPClient) — MCP client docs
- [HuggingFace Hub — Tools](https://huggingface.co/tools) — community tool repository
- [MCP Specification](https://modelcontextprotocol.io/) — the protocol your MCP tools speak
- [Gradio Documentation](https://www.gradio.app/docs) — understanding how Spaces work

---

## 10. Multi-Agent Systems

**File:** `10_multi_agent_systems.ipynb`

### Overview

Complex tasks often exceed what a single agent can handle well. This notebook introduces smolagents' multi-agent system: a manager agent that delegates subtasks to specialist agents. You'll build a 3-agent system with hierarchical orchestration, learn how `managed_agents` works, configure `planning_interval` for periodic replanning, and trace cross-agent communication.

### Learning Objectives

By the end of this notebook, you will be able to:
- Build a multi-agent system with a manager and 2+ managed agents using smolagents
- Configure `managed_agents` and explain how the manager delegates work
- Choose appropriate agent types (`CodeAgent` vs `ToolCallingAgent`) for different roles
- Use `planning_interval` to control how often the manager replans
- Trace and debug multi-agent runs by reading cross-agent logs
- Design agent team compositions for different task types

### Prerequisites

- [06. Intro to smolagents](06_intro_to_smolagents.ipynb) — agent fundamentals
- [07. Custom Tools](07_custom_tools.ipynb) — building tools for specialist agents
- [08. Code Agent Deep Dive](08_code_agent_deep_dive.ipynb) — understanding `CodeAgent` for the manager role

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Why Multi-Agent? | When a single agent breaks down: context limits, tool overload, specialization benefits. |
| 2 | Manager-Worker Architecture | How `managed_agents` works: the manager calls specialist agents as if they were tools. |
| 3 | Building Specialist Agents | Create 2 specialist agents: a researcher (with search tools) and an analyst (with calculation tools). |
| 4 | The Manager Agent | Wire specialists into a `CodeAgent` manager. Run a query that requires delegation. |
| 5 | Agent Type Selection | When to use `CodeAgent` vs `ToolCallingAgent` for manager and worker roles. Performance comparison. |
| 6 | Planning Interval | Configure `planning_interval` to add periodic replanning. Compare traces with and without it. |
| 7 | Tracing Multi-Agent Runs | Read cross-agent logs. Understand which agent executed what and how results flowed. |
| 8 | Designing Agent Teams | Patterns: researcher + writer, planner + executor, critic + creator. When to add more agents vs more tools. |

### Putting It Together

Build a 3-agent research system: a Manager (`CodeAgent`) that delegates to a Researcher (web search + extraction tools) and an Analyst (calculator + data tools). Answer a complex question like "Compare the populations of the 3 largest EU countries and calculate the percentage each represents of the total EU population."

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Two-Agent Basics | Starter | Build a minimal 2-agent system: manager + one specialist. Verify delegation works by checking logs. |
| 2 | Agent Role Swap | Starter | Swap the manager from `CodeAgent` to `ToolCallingAgent`. Compare how delegation is expressed (code vs tool calls). |
| 3 | Three-Agent Pipeline | Synthesis | Add a Writer agent that takes the Researcher's findings and Analyst's numbers and produces a formatted report. |
| 4 | Agent Team Optimizer | Stretch | Run the same complex query with 1-agent, 2-agent, and 3-agent configurations. Compare accuracy, token usage, and latency. |

### Key References

- [smolagents — Multi-Agent Systems](https://huggingface.co/docs/smolagents/multi_agents) — official multi-agent docs
- [AutoGen Research Paper](https://arxiv.org/abs/2308.08155) — foundational multi-agent research
- [CrewAI Concepts](https://docs.crewai.com/concepts) — alternative multi-agent patterns for comparison
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — when multi-agent is and isn't the right choice
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — theoretical foundations

---

## 11. Agent Configuration

**File:** `11_agent_configuration.ipynb`

### Overview

This notebook covers the polish layer: everything you need to configure a smolagents agent for real use. Custom system instructions, output validation with `final_answer_checks`, prompt template customization, `additional_args`, debugging strategies, sharing agents on the Hub, and building a chat interface with `GradioUI`. This is the capstone of Phase 2 — after this, you can build, configure, debug, and share complete agents.

### Learning Objectives

By the end of this notebook, you will be able to:
- Write custom system instructions that shape agent behavior without modifying the base prompt
- Implement `final_answer_checks` to validate agent outputs before they reach the user
- Customize prompt templates and pass `additional_args` for dynamic prompt content
- Apply systematic debugging strategies when agents misbehave
- Share a configured agent on the HuggingFace Hub
- Build and launch a `GradioUI` chat interface for your agent

### Prerequisites

- [06. Intro to smolagents](06_intro_to_smolagents.ipynb) — agent fundamentals
- [07. Custom Tools](07_custom_tools.ipynb) — tools you'll configure the agent with
- [08. Code Agent Deep Dive](08_code_agent_deep_dive.ipynb) — understanding prompts
- [10. Multi-Agent Systems](10_multi_agent_systems.ipynb) — optional but helpful for sharing multi-agent setups

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Custom Instructions | Add `system_prompt` and `additional_instructions` to shape agent behavior. Compare default vs customized. |
| 2 | Output Validation | Implement `final_answer_checks` — functions that validate the agent's answer before returning it. Handle validation failures with retries. |
| 3 | Prompt Templates | Inspect and modify the default prompt template. Understand `{{tool_descriptions}}`, `{{managed_agents_descriptions}}`, and other template variables. |
| 4 | Additional Args | Pass dynamic context with `additional_args` (e.g., user preferences, session metadata) that the agent can reference. |
| 5 | Debugging Strategies | Systematic debugging: verbose mode, log inspection, step-by-step execution, common failure patterns and fixes. |
| 6 | Sharing on Hub | Push a configured agent (with tools and settings) to the HuggingFace Hub. Load it back. |
| 7 | GradioUI | Build a chat interface with `GradioUI`. Configure the UI: title, description, examples, tool display. |
| 8 | Configuration Checklist | A reusable checklist for configuring agents: instructions, tools, validation, monitoring, UI. |

### Putting It Together

Configure a "Customer FAQ Agent" with custom instructions (polite, concise, always cite sources), 3 tools (knowledge base search, ticket creator, escalation trigger), `final_answer_checks` (verify answer contains a source citation), and a `GradioUI` interface. Deploy it and test with 5 different customer queries.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Instruction Tuning | Starter | Write 3 different custom instruction sets (formal, casual, technical) for the same agent. Compare output styles. |
| 2 | Validation Pipeline | Starter | Implement `final_answer_checks` that rejects answers containing "I don't know" and forces the agent to try harder. |
| 3 | Hub Round-Trip | Synthesis | Push a fully configured agent to the Hub, then load it in a fresh notebook and verify all settings survived. |
| 4 | Full Agent Product | Stretch | Build a complete agent "product": custom tools, instructions, validation, GradioUI, and Hub deployment. Share the link. |

### Key References

- [smolagents — Agent Configuration](https://huggingface.co/docs/smolagents/guided_tour) — configuration options
- [smolagents — GradioUI](https://huggingface.co/docs/smolagents/reference/agents#smolagents.GradioUI) — UI reference
- [Gradio Documentation](https://www.gradio.app/docs) — customizing the chat interface
- [HuggingFace Hub — Spaces](https://huggingface.co/spaces) — where shared agents live
- [smolagents — Prompt Templates](https://huggingface.co/docs/smolagents/reference/prompts) — template reference

---

## 12. Conversation Memory

**File:** `12_conversation_memory.ipynb`

### Overview

LLMs are stateless — they forget everything between calls. For agents that have multi-turn conversations, you need memory management: deciding what to keep, what to summarize, and what to drop as the context window fills up. This notebook builds conversation memory from scratch: a naive "keep everything" approach, a sliding window, a summarization strategy, and token counting to stay within limits.

### Learning Objectives

By the end of this notebook, you will be able to:
- Explain why LLM context windows create a memory bottleneck for agents
- Implement a sliding window memory that keeps the N most recent messages
- Build a summarization memory that compresses old messages into a running summary
- Count tokens using tiktoken to estimate context window usage
- Compare memory strategies on the same long conversation and measure quality tradeoffs
- Integrate memory management into a ReAct agent loop

### Prerequisites

- [05. ReAct Agent](05_react_agent.ipynb) — the agent loop you'll add memory to
- [Appendix 09. File I/O and Text Processing](../appendix/09_file_io_and_text_processing.ipynb) — text chunking concepts

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | The Memory Problem | Demonstrate context window overflow: a 20-turn conversation that breaks when the context fills up. |
| 2 | Naive Memory: Keep Everything | The simplest approach — append every message. Show where and why it fails. |
| 3 | Token Counting | Use tiktoken to count tokens in messages. Build a `count_tokens()` utility. Estimate how many turns fit in different context windows. |
| 4 | Sliding Window Memory | Keep only the last N messages (or last T tokens). Implement `SlidingWindowMemory`. Demonstrate what gets lost. |
| 5 | Summarization Memory | When old messages are evicted, summarize them using the LLM. Implement `SummaryMemory` with a running summary prepended to the conversation. |
| 6 | Hybrid Strategy | Combine: system prompt + running summary + last N messages. Implement `HybridMemory`. |
| 7 | Memory in the Agent Loop | Wire `HybridMemory` into the ReAct agent from NB 05. Run a 15-turn conversation and trace memory transitions. |
| 8 | Comparing Strategies | Run the same 20-question conversation with each strategy. Compare: answer quality, token usage, information retention. |

### Putting It Together

Build a "study buddy" agent that maintains a long conversation about a topic. The agent uses hybrid memory: a summary of earlier discussion + the last 5 exchanges. Test it with a 15-turn conversation where later questions reference earlier answers.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Token Counter | Starter | Build a `count_tokens()` function and use it to measure the token cost of 10 sample messages. |
| 2 | Window Size Sweep | Starter | Run the same conversation with window sizes 3, 5, 10, and 20. Plot answer quality vs token usage. |
| 3 | Smart Summarization | Synthesis | Improve the summarizer to preserve key facts (names, numbers, decisions) while compressing narrative. Test retention. |
| 4 | Importance-Based Eviction | Stretch | Instead of evicting the oldest messages, score each message by importance and evict the least important ones first. |

### Key References

- [Anthropic — Long Context Tips](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) — managing long contexts
- [tiktoken Library](https://github.com/openai/tiktoken) — fast token counting
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — memory architectures overview
- [MemGPT Paper (Packer et al., 2023)](https://arxiv.org/abs/2310.08560) — OS-inspired memory management for LLMs
- [Anthropic — Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) — retrieval as a memory strategy

---

## 13. RAG from Scratch

**File:** `13_rag_from_scratch.ipynb`

### Overview

When an agent needs to answer questions about documents it hasn't been trained on, it needs Retrieval-Augmented Generation (RAG). This notebook builds a complete RAG pipeline from scratch: chunk documents, generate embeddings via an API, store them, retrieve the most relevant chunks for a query, and inject them into the LLM prompt. You'll go from the synthetic embeddings of Appendix 10 to real embeddings from an actual model.

### Learning Objectives

By the end of this notebook, you will be able to:
- Chunk documents using fixed-size, sentence-based, and recursive strategies
- Generate real embeddings using an embedding API (via OpenRouter or a local model)
- Store and retrieve embeddings using a simple vector store
- Implement a complete RAG pipeline: chunk → embed → store → retrieve → generate
- Evaluate retrieval quality using precision@k and MRR
- Explain the tradeoffs between chunk size, overlap, and retrieval quality

### Prerequisites

- [05. ReAct Agent](05_react_agent.ipynb) — the agent loop RAG plugs into
- [Appendix 09. File I/O and Text Processing](../appendix/09_file_io_and_text_processing.ipynb) — reading and processing text files
- [Appendix 10. NumPy for Embeddings](../appendix/10_numpy_for_embeddings.ipynb) — cosine similarity and vector math

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | What is RAG? | The problem RAG solves: LLMs can't read your documents. The pipeline: chunk → embed → retrieve → generate. |
| 2 | Chunking Strategies | Implement 3 strategies: fixed-size with overlap, sentence-based, recursive (split by headings → paragraphs → sentences). Compare results. |
| 3 | Real Embeddings | Call an embedding API to convert text chunks into vectors. Compare to the synthetic embeddings from Appendix 10. |
| 4 | Building a Vector Store | Store embeddings in a simple dict-based vector store. Implement `add()`, `search()`, `save()`, and `load()`. |
| 5 | The Retrieval Step | Given a user query, embed it, search the store, return top-k chunks. Implement `retrieve()`. |
| 6 | The Generation Step | Inject retrieved chunks into the system prompt. Build `rag_answer()` that retrieves then generates. |
| 7 | End-to-End Pipeline | Wire everything together: load a document → chunk → embed → store → query → answer. |
| 8 | Evaluating Retrieval | Measure precision@k and MRR on a test set of question-chunk pairs. Identify retrieval failures. |

### Putting It Together

Build a complete RAG system over a set of text documents (e.g., the README files from this repo). Index the documents, then ask 5 questions that require information from specific chunks. Evaluate whether the right chunks were retrieved and whether the generated answers are correct.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Chunk Size Experiment | Starter | Chunk the same document at 3 different sizes (100, 300, 500 tokens). Compare retrieval quality for the same questions. |
| 2 | Embedding Model Comparison | Starter | Use 2 different embedding models and compare their retrieval results on the same queries. |
| 3 | Persistent Vector Store | Synthesis | Add `save()` and `load()` methods to persist the vector store to disk (JSON or pickle). Verify round-trip works. |
| 4 | Contextual Chunking | Stretch | Implement Anthropic's contextual retrieval approach: prepend a context sentence to each chunk before embedding. Measure improvement. |

### Key References

- [Anthropic — Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) — state-of-the-art RAG techniques
- [OpenAI — Embeddings Guide](https://platform.openai.com/docs/guides/embeddings) — embedding API patterns
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — RAG in the agent architecture
- [Sentence Transformers](https://www.sbert.net/) — open-source embedding models
- [ChromaDB](https://docs.trychroma.com/) — a simple vector database you might graduate to

---

## 14. RAG with Tools

**File:** `14_rag_with_tools.ipynb`

### Overview

In NB 13 you built a static RAG pipeline. Now you'll make it agentic: the agent decides *when* to retrieve, *what query* to use, and whether the retrieved results are good enough — or whether to reformulate and try again. This transforms retrieval from a fixed pipeline step into an intelligent tool the agent uses as needed.

### Learning Objectives

By the end of this notebook, you will be able to:
- Wrap a RAG pipeline as a smolagents `@tool` that the agent can call on demand
- Build an agent that decides when to retrieve vs when to answer from its own knowledge
- Implement query reformulation — the agent rewrites bad queries and retries
- Combine RAG retrieval with other tools (calculator, search) in a single agent
- Compare static RAG (always retrieve) vs agentic RAG (retrieve when needed) on the same questions

### Prerequisites

- [13. RAG from Scratch](13_rag_from_scratch.ipynb) — the pipeline you'll wrap as a tool
- [06. Intro to smolagents](06_intro_to_smolagents.ipynb) — building agents with the framework

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Static vs Agentic RAG | The problem with "always retrieve": irrelevant context, wasted tokens, wrong answers. Why the agent should decide. |
| 2 | RAG as a Tool | Wrap `retrieve()` + `generate()` into a `@tool` function. The agent calls it like any other tool. |
| 3 | When to Retrieve | The agent learns to distinguish: questions about the knowledge base (retrieve) vs general knowledge (answer directly). |
| 4 | Query Reformulation | When retrieval returns low-quality results, the agent rewrites the query and retries. Implement a reformulation loop. |
| 5 | Multi-Source RAG | The agent has access to multiple knowledge bases (e.g., docs + FAQ + code). It decides which source to query. |
| 6 | RAG + Other Tools | Combine retrieval with a calculator and a web search tool. The agent chains them for complex queries. |
| 7 | Evaluating Agentic RAG | Compare static vs agentic RAG on 10 questions: answer quality, retrieval precision, token usage. |
| 8 | Hybrid Approaches | When to use static RAG, agentic RAG, or a hybrid. Decision framework. |

### Putting It Together

Build a "documentation assistant" agent with 3 tools: a knowledge base retriever (your RAG pipeline), a web search tool (for questions not in the docs), and a calculator. Test with 10 questions that require different tool combinations.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Basic RAG Tool | Starter | Wrap your NB 13 RAG pipeline as a `@tool` and use it in a `ToolCallingAgent`. Verify it works. |
| 2 | Retrieve-or-Not Decision | Starter | Test the agent with 5 questions that need retrieval and 5 that don't. Check if it makes the right call. |
| 3 | Query Reformulation | Synthesis | Add a reformulation step: if retrieval returns low-similarity results, rewrite the query and retry. |
| 4 | Multi-Hop RAG | Stretch | Build a tool that can do multi-hop retrieval: retrieve, extract an entity, retrieve again using that entity. |

### Key References

- [Anthropic — Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) — advanced retrieval patterns
- [smolagents — Tools Guide](https://huggingface.co/docs/smolagents/tools) — wrapping anything as a tool
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — agentic RAG patterns
- [Self-RAG Paper (Asai et al., 2023)](https://arxiv.org/abs/2310.11511) — the agent decides when and what to retrieve
- [CRAG Paper (Yan et al., 2024)](https://arxiv.org/abs/2401.15884) — corrective RAG with quality evaluation

---

## 15. Planning Agent

**File:** `15_planning_agent.ipynb`

### Overview

ReAct agents decide their next action one step at a time. A planning agent thinks ahead: it decomposes a complex task into subtasks, creates an execution plan, then works through it step by step — revising the plan when things go wrong. This notebook builds the plan-then-execute pattern from scratch, a fundamental architecture for agents that tackle multi-step problems.

### Learning Objectives

By the end of this notebook, you will be able to:
- Explain the difference between reactive (one-step-at-a-time) and planning-based agents
- Build a planning agent that decomposes tasks into numbered subtask lists
- Implement plan execution with progress tracking and status updates
- Add plan revision: when a step fails or produces unexpected results, the agent updates its plan
- Compare planning vs reactive agents on multi-step tasks (accuracy, efficiency, debuggability)

### Prerequisites

- [05. ReAct Agent](05_react_agent.ipynb) — the reactive agent you'll contrast with

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Reactive vs Planning | Side-by-side comparison: ReAct tackles one step at a time, planning agent maps out the full path first. |
| 2 | Task Decomposition | Build a `decompose()` function that uses the LLM to break a complex task into numbered subtasks. |
| 3 | Plan Representation | Define a `Plan` data structure: list of steps with status (pending, in_progress, completed, failed). |
| 4 | Plan Execution | Build the execution loop: pick next pending step, execute it (may involve tool calls), update status. |
| 5 | Progress Tracking | Track which steps are done, which are in progress. Feed this context back to the LLM for each step. |
| 6 | Plan Revision | When a step fails or returns unexpected results, the agent revises the remaining plan. Implement `revise_plan()`. |
| 7 | Planning with smolagents | Use smolagents' `planning_interval` to add periodic replanning to a framework agent. |
| 8 | Planning vs Reactive Comparison | Run both agent types on 5 multi-step tasks. Compare step counts, accuracy, and trace readability. |

### Putting It Together

Build a planning agent that tackles a complex research question requiring 4-5 steps (e.g., "Find the 3 most populated countries in Europe, get their capitals, and calculate the total population"). The agent plans all steps upfront, executes them, and revises if any step fails.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Basic Planner | Starter | Build a `decompose()` function that breaks "Plan a weekend trip to Paris" into 5 subtasks. |
| 2 | Plan Execution | Starter | Execute a 3-step plan using simulated tools. Track status transitions for each step. |
| 3 | Adaptive Replanning | Synthesis | Make the agent detect when a step produces insufficient results and automatically add clarifying steps. |
| 4 | Hierarchical Planning | Stretch | Build a two-level planner: high-level plan → each step gets decomposed into sub-steps. |

### Key References

- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — planning architectures
- [HuggingPlan Paper (Yao et al., 2022)](https://arxiv.org/abs/2305.04091) — plan-and-solve prompting
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — when planning helps
- [smolagents — Planning](https://huggingface.co/docs/smolagents/guided_tour#planning) — framework support for planning
- [ReWOO Paper (Xu et al., 2023)](https://arxiv.org/abs/2305.18323) — reasoning without observation (plan first)

---

## 16. Reflection Agent

**File:** `16_reflection_agent.ipynb`

### Overview

Agents make mistakes: they call the wrong tool, generate incomplete answers, or miss important details. A reflection agent adds a self-critique step: after generating an output, it evaluates its own work, identifies problems, and iterates to improve. This pattern — generate → critique → revise — is one of the most effective ways to improve agent output quality.

### Learning Objectives

By the end of this notebook, you will be able to:
- Explain the reflection pattern: generate → critique → revise → repeat
- Build a critic prompt that evaluates agent outputs against specific criteria
- Implement a reflection loop with configurable iteration limits
- Distinguish between self-reflection (same model critiques itself) and cross-reflection (different model critiques)
- Measure output quality improvement across reflection iterations

### Prerequisites

- [05. ReAct Agent](05_react_agent.ipynb) — the base agent loop you'll add reflection to

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Why Reflection? | Demo: a ReAct agent gives an incomplete answer. Add one reflection step → the answer improves dramatically. |
| 2 | The Critic Prompt | Design a prompt that evaluates outputs on specific criteria: completeness, accuracy, clarity, source quality. |
| 3 | The Reflection Loop | Build `reflect_and_improve()`: generate → critique → revise. Implement iteration limits and convergence detection. |
| 4 | Self-Reflection vs Cross-Reflection | Compare: same LLM critiques itself vs a different LLM critiques. Tradeoffs in cost, quality, and bias. |
| 5 | Reflection in Tool Use | Add reflection after tool calls: "Did I call the right tool? Is this result sufficient? Should I try a different approach?" |
| 6 | Scoring Criteria | Build a rubric-based evaluation: the critic scores each criterion 1-5 and provides specific improvement suggestions. |
| 7 | When to Stop Reflecting | Convergence detection: stop when the critique says "no issues found" or when quality score plateaus. |
| 8 | Reflection in Practice | When reflection helps (writing, analysis, complex reasoning) and when it hurts (simple lookups, factual queries). |

### Putting It Together

Build a "writing assistant" agent that generates an article outline, critiques it (is it well-structured? are key points covered?), and revises it through 3 iterations. Track the quality score at each iteration to show improvement.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Basic Critic | Starter | Write a critic prompt that evaluates whether a summary covers all key points from a source text. |
| 2 | Reflection Loop | Starter | Build a loop that generates → critiques → revises an answer 3 times. Print the quality score at each step. |
| 3 | Cross-Model Reflection | Synthesis | Use one model to generate and a different model to critique. Compare to self-reflection on the same tasks. |
| 4 | Reflexion Agent | Stretch | Implement the Reflexion pattern: the agent maintains a memory of past failures and uses them to avoid repeating mistakes. |

### Key References

- [Reflexion Paper (Shinn et al., 2023)](https://arxiv.org/abs/2303.11366) — self-reflection with episodic memory
- [Self-Refine Paper (Madaan et al., 2023)](https://arxiv.org/abs/2303.17651) — iterative self-refinement
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — reflection patterns
- [Constitutional AI (Bai et al., 2022)](https://arxiv.org/abs/2212.08073) — AI critiquing AI outputs
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — reflection in agent architectures

---

## 17. Tree of Thought

**File:** `17_tree_of_thought.ipynb`

### Overview

ReAct agents follow a single reasoning path. Tree of Thought (ToT) agents explore multiple paths simultaneously: at each step, they generate several candidate thoughts, evaluate them, and pursue the most promising ones — potentially backtracking when a path turns out to be a dead end. This is the most powerful reasoning pattern for problems with branching solution spaces.

### Learning Objectives

By the end of this notebook, you will be able to:
- Explain the Tree of Thought pattern: branching, evaluation, selection, and backtracking
- Implement thought generation: produce multiple candidate next-steps at each node
- Build an evaluation function that scores candidate thoughts
- Implement BFS and DFS search strategies for exploring the thought tree
- Visualize the thought tree to understand the agent's exploration pattern
- Compare ToT vs CoT vs ReAct on problems that require exploration

### Prerequisites

- [05. ReAct Agent](05_react_agent.ipynb) — the single-path agent you'll extend
- [15. Planning Agent](15_planning_agent.ipynb) — decomposition skills useful for generating candidate thoughts

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Why Explore Multiple Paths? | Demo: a ReAct agent gets stuck on a problem that requires backtracking. ToT finds the solution by exploring alternatives. |
| 2 | The Thought Tree | Define the tree structure: nodes are partial solutions, edges are reasoning steps, leaves are candidate answers. |
| 3 | Thought Generation | At each node, generate K candidate next-steps using the LLM. Implement `generate_thoughts()`. |
| 4 | Thought Evaluation | Score each candidate thought using the LLM as a judge. Implement `evaluate_thought()`. |
| 5 | BFS Strategy | Explore the tree breadth-first: expand all nodes at depth D before moving to D+1. Best for wide, shallow problems. |
| 6 | DFS Strategy | Explore depth-first with backtracking: go deep, backtrack when stuck. Best for deep, narrow problems. |
| 7 | Putting It Together | Full ToT agent: generate → evaluate → select → expand → repeat until solution found or budget exhausted. |
| 8 | ToT vs CoT vs ReAct | Run all three on the same set of puzzles. Compare solution rates, step counts, and token costs. |

### Putting It Together

Build a ToT agent that solves a multi-step logic puzzle (e.g., "24 game": make 24 from four numbers using +, -, *, /). The agent generates multiple candidate operations at each step, evaluates which are most promising, and backtracks from dead ends.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Basic Tree | Starter | Build a thought tree with branching factor 3 and depth 2. Visualize all 9 leaf nodes. |
| 2 | BFS vs DFS | Starter | Run both strategies on the same puzzle. Compare which finds the answer first and how many nodes each explores. |
| 3 | Adaptive Branching | Synthesis | Instead of fixed branching factor K, let the evaluator decide how many candidates to keep at each level (1-5 based on difficulty). |
| 4 | Monte Carlo ToT | Stretch | Implement a Monte Carlo Tree Search (MCTS) variant: use random rollouts to estimate the value of each thought node. |

### Key References

- [Tree of Thoughts Paper (Yao et al., 2023)](https://arxiv.org/abs/2305.10601) — the original paper
- [Tree of Thoughts GitHub](https://github.com/princeton-nlp/tree-of-thought-llm) — reference implementation
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — ToT in context
- [Graph of Thoughts (Besta et al., 2023)](https://arxiv.org/abs/2308.09687) — extending trees to graphs
- [Algorithm of Thoughts (Sel et al., 2023)](https://arxiv.org/abs/2308.10379) — LLM as an algorithm

---

## 18. Multi-Agent Basics

**File:** `18_multi_agent_basics.ipynb`

### Overview

NB 10 introduced multi-agent systems via smolagents' `managed_agents`. This notebook goes deeper: you'll build multi-agent collaboration from scratch in raw Python — two agents that communicate through message passing, share state, and collaborate on tasks. Understanding the raw mechanics makes you a better multi-agent system designer regardless of framework.

### Learning Objectives

By the end of this notebook, you will be able to:
- Build two agents that communicate through a shared message queue
- Implement message passing protocols: request/response, broadcast, publish/subscribe
- Design shared state that multiple agents can read and write safely
- Coordinate agents to work on different parts of a task in parallel
- Debug multi-agent interactions by tracing message flow

### Prerequisites

- [05. ReAct Agent](05_react_agent.ipynb) — the single agents you'll combine

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Why Multi-Agent? | When one agent isn't enough: specialization, parallel work, perspective diversity. |
| 2 | Agent Communication | Build a `MessageBus` class. Agents send and receive typed messages: `Request`, `Response`, `Broadcast`. |
| 3 | Two Agents, One Task | A researcher agent gathers information, passes it to a writer agent via the message bus. |
| 4 | Shared State | Implement a `SharedState` dict that both agents can read/write. Handle concurrent access. |
| 5 | Message Passing Patterns | Request/response, publish/subscribe, and broadcast. When to use each pattern. |
| 6 | Parallel Execution | Two agents work on different subtasks simultaneously. Merge results when both finish. |
| 7 | Error Handling | What happens when one agent fails? Timeout, retry, and fallback strategies. |
| 8 | Multi-Agent Tracing | Build a trace visualizer that shows message flow between agents as a timeline. |

### Putting It Together

Build a 2-agent system: a Researcher that answers factual questions using tools, and a Writer that takes the Researcher's findings and produces a well-formatted summary. They communicate via the message bus. Test with a question that requires 3 research steps before the Writer can produce the final output.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Message Bus | Starter | Build a `MessageBus` and test it with two agents exchanging 3 messages each. |
| 2 | Shared State | Starter | Create a `SharedState` and have two agents contribute to a shared "findings" list. |
| 3 | Parallel Research | Synthesis | Two researcher agents each investigate a different aspect of a question. Merge their findings. |
| 4 | Agent Network | Stretch | Build a 4-agent network where any agent can message any other agent. Implement routing logic. |

### Key References

- [AutoGen Research Paper](https://arxiv.org/abs/2308.08155) — multi-agent conversation framework
- [CrewAI Concepts](https://docs.crewai.com/concepts) — role-based multi-agent patterns
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — multi-agent architectures
- [Microsoft — Multi-Agent Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) — enterprise patterns
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — when to use multi-agent

---

## 19. Orchestrator Pattern

**File:** `19_orchestrator_pattern.ipynb`

### Overview

The orchestrator pattern is the most common multi-agent architecture in production: a manager agent receives a complex task, decomposes it, delegates subtasks to specialist agents, aggregates their results, and produces a final output. This notebook builds the pattern from scratch with a focus on delegation strategies, result aggregation, and handling specialist failures.

### Learning Objectives

By the end of this notebook, you will be able to:
- Build an orchestrator agent that delegates work to 2+ specialist agents
- Implement delegation strategies: round-robin, skill-based routing, load-aware
- Aggregate results from multiple specialists into a coherent final answer
- Handle specialist failures: retries, fallback to different specialists, graceful degradation
- Compare flat (all specialists equal) vs hierarchical (sub-orchestrators) architectures

### Prerequisites

- [18. Multi-Agent Basics](18_multi_agent_basics.ipynb) — agent communication and shared state

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | The Orchestrator Pattern | Architecture overview: orchestrator receives task, decomposes, delegates, aggregates, returns. |
| 2 | Specialist Agent Design | Build 3 specialist agents with distinct capabilities: researcher, calculator, writer. Each has focused tools. |
| 3 | The Orchestrator Agent | Build the orchestrator: it reads the task, decides which specialists to invoke, and in what order. |
| 4 | Delegation Strategies | Skill-based routing (match task to specialist capabilities). Implement a routing function. |
| 5 | Result Aggregation | The orchestrator combines results from multiple specialists. Strategies: concatenate, summarize, synthesize. |
| 6 | Handling Failures | When a specialist fails: retry, delegate to a different specialist, or return a partial answer. |
| 7 | Hierarchical Orchestration | Nest orchestrators: a top-level orchestrator delegates to sub-orchestrators who have their own specialists. |
| 8 | Orchestrator Tracing | Build a visualization that shows the delegation tree: which orchestrator → which specialist → which result. |

### Putting It Together

Build a 4-agent system: an Orchestrator that delegates to a Researcher (search tools), a Calculator (math tools), and a Writer (no tools, just good prompts). Answer: "What is the GDP per capita of the 3 largest EU economies, and how do they compare to the US?" The Orchestrator decomposes this into research, calculation, and writing subtasks.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Basic Orchestrator | Starter | Build an orchestrator with 2 specialists. Have it delegate a simple task and aggregate results. |
| 2 | Skill-Based Routing | Starter | Implement routing logic that picks the right specialist based on task keywords. Test with 5 tasks. |
| 3 | Failure Recovery | Synthesis | Simulate a specialist failure and implement retry + fallback. Verify the orchestrator still produces a result. |
| 4 | Dynamic Team Assembly | Stretch | The orchestrator decides how many and which specialists to create based on the task. It assembles the team dynamically. |

### Key References

- [AutoGen Research Paper](https://arxiv.org/abs/2308.08155) — orchestration patterns
- [CrewAI Documentation](https://docs.crewai.com/) — role-based orchestration
- [Microsoft — Multi-Agent Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) — enterprise orchestration
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — orchestration vs single-agent
- [smolagents — Multi-Agent Systems](https://huggingface.co/docs/smolagents/multi_agents) — framework-level orchestration

---

## 20. Debate Agents

**File:** `20_debate_agents.ipynb`

### Overview

When agents debate, they challenge each other's reasoning, catch errors, and converge on better answers. This notebook builds adversarial collaboration: two or more agents argue different positions, critique each other's arguments, and reach consensus through structured debate. This pattern is especially valuable for tasks where the "right" answer isn't obvious and benefits from multiple perspectives.

### Learning Objectives

By the end of this notebook, you will be able to:
- Build a debate framework where 2+ agents argue and critique each other's positions
- Implement turn-taking protocols: alternating, round-robin, free-form
- Design a consensus mechanism: voting, judge agent, convergence detection
- Use adversarial collaboration to improve answer quality on ambiguous questions
- Compare debate-based answers to single-agent answers on the same questions

### Prerequisites

- [18. Multi-Agent Basics](18_multi_agent_basics.ipynb) — agent communication
- [19. Orchestrator Pattern](19_orchestrator_pattern.ipynb) — managing multiple agents

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Why Debate? | Demo: a single agent gives a mediocre answer to an ambiguous question. Two debating agents produce a much better one. |
| 2 | The Debate Framework | Build `DebateArena`: manages debaters, turn-taking, and transcripts. Each debater is a ReAct agent with a position. |
| 3 | Argument and Critique | Each agent generates an argument, then critiques the opponent's argument. Structured format: claim, evidence, rebuttal. |
| 4 | Turn-Taking Protocols | Implement alternating turns and round-robin (3+ agents). Compare debate dynamics. |
| 5 | Consensus Mechanisms | Three approaches: majority voting, a neutral judge agent evaluates arguments, convergence detection (agents agree). |
| 6 | The Judge Agent | Build a judge that reads the full debate transcript and renders a verdict. Design the evaluation rubric. |
| 7 | Multi-Agent Debate (3+) | Extend to 3 debaters with different perspectives. Observe how more perspectives affect answer quality. |
| 8 | Debate vs Single Agent | Run both on 5 ambiguous questions. Compare answer quality, nuance, and coverage of edge cases. |

### Putting It Together

Build a 3-agent debate on a complex question (e.g., "Should AI agents be given internet access in production?"). Agent A argues for, Agent B argues against, Agent C takes a nuanced middle position. A Judge agent evaluates all arguments and produces a balanced summary with the strongest points from each side.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Basic Debate | Starter | Build a 2-agent debate with 3 rounds of alternating arguments on a simple topic. |
| 2 | Judge Agent | Starter | Add a judge that reads the debate transcript and picks the winner with justification. |
| 3 | Consensus Detection | Synthesis | Implement convergence detection: stop the debate when agents start agreeing. Measure how many rounds that takes. |
| 4 | Debate Tournament | Stretch | Run a tournament: 4 agents in pairs, winners debate each other. Does the "best" argument consistently win? |

### Key References

- [Society of Mind Paper (Zhuge et al., 2023)](https://arxiv.org/abs/2305.17066) — multi-agent collaboration through debate
- [LLM Debate Paper (Du et al., 2023)](https://arxiv.org/abs/2305.14325) — improving factuality through debate
- [AutoGen Research Paper](https://arxiv.org/abs/2308.08155) — conversational multi-agent patterns
- [Constitutional AI (Bai et al., 2022)](https://arxiv.org/abs/2212.08073) — AI evaluating AI arguments
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — adversarial collaboration patterns

---

## 21. Research Agent

**File:** `21_research_agent.ipynb`

### Overview

This is the capstone project of the core track: a complete, end-to-end research agent that searches the web, reads documents, takes notes, synthesizes findings, and produces a structured research report with citations. It combines tools (search, read, calculate), memory (conversation + notes), planning (decompose the research question), and multi-step reasoning (the ReAct loop) — everything from Phase 1 through Phase 5.

### Learning Objectives

By the end of this notebook, you will be able to:
- Design a research agent that orchestrates search, reading, note-taking, and synthesis
- Build a research pipeline: decompose question → search → read → extract → synthesize → report
- Implement a citation system that tracks which facts came from which sources
- Handle research dead-ends: the agent detects insufficient results and tries alternative queries
- Produce a structured research report with sections, key findings, and a bibliography

### Prerequisites

- [05. ReAct Agent](05_react_agent.ipynb) — the core agent loop
- [13. RAG from Scratch](13_rag_from_scratch.ipynb) — retrieval for the knowledge base
- [15. Planning Agent](15_planning_agent.ipynb) — task decomposition for research planning

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Research Agent Architecture | The full pipeline: question → plan → search → read → extract → synthesize → report. |
| 2 | Research Tools | Build 4 tools: web search (simulated), page reader, note-taker, citation tracker. |
| 3 | Research Planning | The agent decomposes a research question into sub-questions and creates a research plan. |
| 4 | Search and Read Loop | The agent searches for each sub-question, reads results, extracts key facts, and stores them. |
| 5 | Note-Taking and Citations | The agent maintains structured notes with source attribution. Implement a citation system. |
| 6 | Gap Detection | The agent reviews its notes, identifies gaps (unanswered sub-questions), and does additional research. |
| 7 | Synthesis and Report Generation | The agent synthesizes all notes into a structured report: intro, findings, analysis, conclusion, bibliography. |
| 8 | End-to-End Demo | Run the full research agent on a real question. Trace the complete pipeline from question to report. |

### Putting It Together

The entire notebook IS the capstone. Run the research agent on a complex question like "How are the major cloud providers (AWS, Azure, GCP) approaching AI agent deployment, and what are the key differences in their approaches?" The agent should produce a multi-section report with 5+ cited sources.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Custom Research Question | Starter | Run the research agent on a topic you're genuinely curious about. Evaluate the report quality. |
| 2 | Source Verification | Starter | Add a verification step: the agent double-checks key claims by searching for confirming or contradicting sources. |
| 3 | Multi-Agent Research | Synthesis | Split the research agent into 3 specialist agents (searcher, reader, writer) coordinated by an orchestrator. |
| 4 | Research Quality Eval | Stretch | Build an evaluation rubric and use an LLM-as-judge to score research reports on completeness, accuracy, and citation quality. |

### Key References

- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — agent design principles
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — the full architecture
- [STORM Paper (Shao et al., 2024)](https://arxiv.org/abs/2402.14207) — LLM-powered research synthesis
- [OpenAI Deep Research](https://openai.com/index/introducing-deep-research/) — production research agent
- [GAIA Benchmark](https://huggingface.co/gaia-benchmark) — evaluating research-style agent tasks

---

## 22. Eval and Debug

**File:** `22_eval_and_debug.ipynb`

### Overview

The final core notebook focuses on a critical skill: systematically evaluating and debugging agent behavior. You'll build a tracing system, create test suites for agents, identify common failure modes, and learn debugging strategies that work across all agent architectures. This notebook gives you the tools to answer: "Is my agent working correctly, and if not, why?"

### Learning Objectives

By the end of this notebook, you will be able to:
- Build a structured tracing system that records every agent step (thought, action, observation, timing)
- Create test suites: unit tests for tools, integration tests for agent loops, golden-answer regression tests
- Identify and diagnose the 5 most common agent failure modes
- Use trace analysis to pinpoint where an agent's reasoning went wrong
- Build a simple evaluation harness that scores agent outputs against expected answers

### Prerequisites

- All core notebooks (01-21) — this is the capstone evaluation notebook

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Why Eval Matters | The "it works on my example" trap. Why systematic evaluation is essential for agent development. |
| 2 | Structured Tracing | Build a `Tracer` class that records every step: thought, action, action_input, observation, timestamp, token count. |
| 3 | Trace Analysis | Functions that analyze traces: total tokens, step count, tool usage frequency, error rate, bottleneck identification. |
| 4 | Unit Testing Tools | Write pytest tests for individual tools. Mock external APIs. Test edge cases. |
| 5 | Integration Testing Agents | Test the full agent loop with scripted inputs and expected outputs. Handle non-determinism with fuzzy matching. |
| 6 | Golden-Answer Tests | Build a test suite of question-answer pairs. Run the agent on all questions and score accuracy. |
| 7 | Common Failure Modes | The top 5: infinite loops, hallucinated tools, wrong tool selection, format drift, premature termination. How to detect and fix each. |
| 8 | Debugging Workflow | A systematic debugging process: reproduce → trace → isolate → hypothesize → fix → verify. |

### Putting It Together

Build an evaluation harness for the ReAct agent from NB 05. Create a 10-question test suite spanning different difficulty levels. Run the agent, score each answer (exact match + LLM-as-judge), generate a report showing pass rate, average tokens, and failure categories.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Trace Builder | Starter | Instrument the ReAct agent from NB 05 with the `Tracer`. Run 3 queries and print trace summaries. |
| 2 | Tool Unit Tests | Starter | Write 5 pytest tests for the `calculate`, `get_weather`, and `search` tools from NB 05. |
| 3 | Failure Mode Detector | Synthesis | Build a function that analyzes a trace and classifies the failure mode (if any): loop, hallucinated tool, format drift, etc. |
| 4 | Continuous Eval Pipeline | Stretch | Build a script that runs the full test suite, compares to previous results, and flags regressions. Store results in a JSON file. |

### Key References

- [Anthropic — Developing Tests](https://docs.anthropic.com/en/docs/build-with-claude/develop-tests) — evaluation best practices
- [GAIA Benchmark](https://huggingface.co/gaia-benchmark) — standard agent benchmark
- [Braintrust](https://www.braintrust.dev/) — agent evaluation platform
- [pytest Documentation](https://docs.pytest.org/) — Python testing framework
- [Langfuse](https://langfuse.com/) — open-source LLM tracing and evaluation
