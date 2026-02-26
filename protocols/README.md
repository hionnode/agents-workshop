# Agent Protocols & Interoperability — Lesson Plans

> Detailed lesson plans for notebooks 01–04. MCP (agent-to-tool) and A2A (agent-to-agent) are the emerging interoperability standards for AI agents.
> For the full track overview, see [`../roadmap.md`](../roadmap.md).

---

## 01. MCP from Scratch

**File:** `01_mcp_from_scratch.ipynb`

### Overview

MCP (Model Context Protocol) is the open standard that lets any agent talk to any tool server using a shared protocol — the same way HTTP lets any browser talk to any web server. This notebook tears the protocol apart layer by layer: JSON-RPC message format, capability negotiation, stdio and Streamable HTTP transports, and the resource/tool/prompt primitives. You will build a minimal MCP client and server from first principles, without using any SDK, so you understand exactly what the official libraries abstract away.

### Learning Objectives

By the end of this notebook, you will be able to:
- Explain the MCP architecture (host, client, server) and why it exists as an alternative to per-provider function-calling formats
- Read and construct JSON-RPC 2.0 messages (request, response, notification, error) by hand
- Describe the MCP capability negotiation handshake (`initialize` / `initialized`) and what each capability flag means
- Compare stdio transport vs Streamable HTTP transport and articulate when to use each
- Implement a minimal MCP server (stdio) that exposes a tool and a resource
- Implement a minimal MCP client that discovers and calls tools on that server
- Trace a full tool-call lifecycle: `tools/list` -> user confirms -> `tools/call` -> result

### Prerequisites

- [`../core/03_tool_use_from_scratch.ipynb`](../core/03_tool_use_from_scratch.ipynb) — You need to understand function calling and tool dispatch before layering a protocol on top
- [`../core/05_react_agent.ipynb`](../core/05_react_agent.ipynb) — The ReAct loop is the agent pattern that MCP plugs into
- [`../appendix/04_strings_and_json.ipynb`](../appendix/04_strings_and_json.ipynb) — MCP is built entirely on JSON; you need fluency with `json` module, JSON schemas, and nested structures

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Why protocols matter | The problem MCP solves: N agents x M tools = N*M integrations without a standard. How MCP reduces this to N+M. Comparison to USB, HTTP, LSP. |
| 2 | MCP architecture overview | Hosts, clients, servers. The three primitives: resources (read data), tools (perform actions), prompts (templated interactions). Capability negotiation. |
| 3 | JSON-RPC 2.0 deep dive | Build JSON-RPC requests, responses, notifications, and error objects by hand. Understand `id`, `method`, `params`, `result`, `error` fields. Batch requests. |
| 4 | The MCP lifecycle | Walk through the full protocol flow: `initialize` -> `initialized` -> `tools/list` -> `tools/call` -> `shutdown`. Build a state machine diagram. |
| 5 | Stdio transport from scratch | Build a server that reads JSON-RPC from stdin and writes to stdout. Build a client that spawns it as a subprocess and communicates via pipes. |
| 6 | Streamable HTTP transport | Implement the same server over HTTP using SSE (server-sent events) for server-to-client streaming. Compare latency, complexity, and deployment tradeoffs. |
| 7 | Resources and prompts | Extend the server with `resources/list`, `resources/read` (expose a file or database row) and `prompts/list`, `prompts/get` (expose a prompt template). |
| 8 | Plugging MCP into a ReAct loop | Connect your from-scratch MCP client to the ReAct agent from Core 05. The agent discovers tools dynamically via `tools/list` instead of having them hardcoded. |

### Putting It Together

The capstone exercise connects all the pieces: you run your hand-built MCP server (exposing a calculator tool and a notes resource) and wire it into your Core 05 ReAct agent via the from-scratch MCP client. The agent discovers available tools at startup, uses them during its reasoning loop, and reads resources when it needs context — all through the protocol, with no hardcoded tool definitions in the agent code. You will add logging to trace every JSON-RPC message so you can see the full conversation between agent and server.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Add a new tool to your server | Starter | Add a `get_weather` tool to your stdio server and verify the client discovers and calls it without any client-side code changes. |
| 2 | Error handling | Moderate | Make your server return proper JSON-RPC error codes (-32600, -32601, -32602) for invalid requests, unknown methods, and bad parameters. Test each case from the client. |
| 3 | Pagination support | Moderate | Implement cursor-based pagination for `tools/list` (the MCP spec supports this). Return 2 tools per page and have the client follow the cursor to get all tools. |
| 4 | Streamable HTTP with session management | Stretch | Extend your HTTP transport to support the `Mcp-Session-Id` header for stateful sessions. Track initialization state per session and reject requests on uninitialized sessions. |

### Key References

- [MCP Specification](https://modelcontextprotocol.io/) — The official specification site; start with the Architecture and Transports pages
- [MCP GitHub Organization](https://github.com/modelcontextprotocol) — Reference implementations, SDKs, and spec source
- [Anthropic — Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) — The original announcement blog post explaining the motivation
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification) — The wire format MCP is built on; short and worth reading end-to-end
- [MCP Specification — Transports](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports) — Detailed spec for stdio and Streamable HTTP transports
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — Foundational blog post on agent architecture; MCP implements the "tool use" layer she describes
- [Microsoft LSP Specification](https://microsoft.github.io/language-server-protocol/) — MCP's spiritual ancestor; understanding LSP makes MCP's design choices obvious
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — The broader agent design guide; MCP is one piece of this architecture

---

## 02. Building MCP Servers

**File:** `02_building_mcp_servers.ipynb`

### Overview

Notebook 01 built MCP from the wire protocol up. This notebook shifts to the builder's perspective: using the official Python SDK (`mcp`) to create production-quality MCP servers that expose your own tools, resources, and prompts. You will build, test, and package a real MCP server — then connect it to Claude Desktop and other MCP hosts. This is the practical skill: most agent builders will consume the protocol through SDKs, and the ability to ship a solid MCP server is immediately valuable.

### Learning Objectives

By the end of this notebook, you will be able to:
- Use the `mcp` Python SDK to create a server with tools, resources, and prompts using the `@mcp.tool()`, `@mcp.resource()`, and `@mcp.prompt()` decorators
- Write tool functions with proper type annotations, descriptions, and error handling that produce good auto-generated JSON schemas
- Implement dynamic resources with URI templates (e.g., `notes://{note_id}`) and resource subscriptions
- Test MCP servers locally using the MCP Inspector and by writing automated integration tests
- Package an MCP server for distribution (pip-installable package, Docker container)
- Configure Claude Desktop, VS Code, and Cursor to use your custom MCP server
- Implement logging, progress reporting, and cancellation support in your server

### Prerequisites

- [`../core/03_tool_use_from_scratch.ipynb`](../core/03_tool_use_from_scratch.ipynb) — Understanding tool definitions and JSON schema for tool parameters
- [`01_mcp_from_scratch.ipynb`](01_mcp_from_scratch.ipynb) — You need to understand the protocol your server implements: JSON-RPC messages, the lifecycle, capability negotiation

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | The `mcp` Python SDK | Install and explore the SDK. Understand `FastMCP` (high-level) vs `Server` (low-level) APIs. When to use which. |
| 2 | Your first SDK server | Build a server with `FastMCP` that exposes two tools (`add`, `get_weather`). Run it with `mcp dev` and test in the MCP Inspector. |
| 3 | Tools — best practices | Type-annotated parameters, docstring-driven descriptions, `Context` parameter for logging and progress, returning `TextContent` vs `ImageContent` vs `EmbeddedResource`. Error handling patterns. |
| 4 | Resources and resource templates | Expose static resources (`config://app`) and dynamic resources with URI templates (`users://{user_id}`). Implement `list_changed` notifications for live-updating resource lists. |
| 5 | Prompts as first-class primitives | Define prompt templates with `@mcp.prompt()`. Multi-turn prompts with argument interpolation. Use case: standardized tool-use prompts your agents can discover at runtime. |
| 6 | Testing your server | Unit-test tool functions directly. Integration-test the server using `mcp` client in-process. Test with MCP Inspector. Automated test patterns with pytest. |
| 7 | Connecting to real hosts | Configure Claude Desktop (`claude_desktop_config.json`), VS Code (Copilot MCP settings), and Cursor to use your server. Verify tool discovery and execution in each host. |
| 8 | Packaging and deployment | Package as a pip-installable tool (`pyproject.toml`, entry points). Build a Docker image. Publish to PyPI or a private registry. Remote server deployment with Streamable HTTP. |

### Putting It Together

The capstone has you build and ship a complete "Personal Notes" MCP server that exposes: (1) tools for creating, searching, and tagging notes, (2) resources for reading individual notes by ID and listing all notes, and (3) a prompt template for summarizing notes on a topic. You test it end-to-end with the MCP Inspector, write a pytest integration test suite, configure it in Claude Desktop, and package it as a pip-installable command-line tool that anyone can install and run.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Add image support | Starter | Add a tool that returns an `ImageContent` result (e.g., a dynamically generated chart using matplotlib). Verify it renders correctly in Claude Desktop. |
| 2 | Progress reporting | Moderate | Implement a long-running tool (e.g., batch file processing) that reports progress via `ctx.report_progress()`. Watch the progress updates in the MCP Inspector. |
| 3 | Resource subscriptions | Moderate | Implement resource subscriptions so that when a note is updated via a tool, the server sends a `notifications/resources/updated` message. Write a client-side test that verifies the notification arrives. |
| 4 | Build a database MCP server | Stretch | Build an MCP server that connects to a SQLite database and exposes: a `query` tool (read-only SQL), a `schema://` resource listing all tables and columns, and a prompt template for generating SQL from natural language. Package it and test in Claude Desktop. |

### Key References

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) — The official Python SDK; the README is the best quickstart guide
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk) — The TypeScript equivalent; useful if you want to compare approaches or build Node.js servers
- [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector) — Interactive debugging tool for MCP servers; essential during development
- [MCP Specification — Tools](https://modelcontextprotocol.io/specification/2025-03-26/server/tools) — The spec section on tool definition, discovery, and invocation
- [MCP Specification — Resources](https://modelcontextprotocol.io/specification/2025-03-26/server/resources) — Resource URIs, templates, subscriptions, and list-changed notifications
- [MCP Specification — Prompts](https://modelcontextprotocol.io/specification/2025-03-26/server/prompts) — Prompt primitives and argument interpolation
- [Claude Desktop MCP Setup](https://modelcontextprotocol.io/quickstart/user) — How to configure Claude Desktop to use MCP servers
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers) — Community-maintained list of MCP servers for inspiration and reference
- [FastMCP Documentation](https://gofastmcp.com/) — Extended documentation for the FastMCP high-level API

---

## 03. A2A Protocol

**File:** `03_a2a_protocol.ipynb`

### Overview

A2A (Agent-to-Agent) is Google's open protocol for agent-to-agent communication — the complement to MCP's agent-to-tool story. While MCP standardizes how agents access tools (vertical integration), A2A standardizes how agents discover each other, negotiate capabilities, and collaborate on tasks (horizontal integration). This notebook covers the full A2A specification: agent cards for discovery, the task lifecycle (submitted -> working -> completed), multipart message streaming, and push notifications. You will build an A2A client and server that let two agents collaborate on a task neither could complete alone.

### Learning Objectives

By the end of this notebook, you will be able to:
- Explain the A2A architecture and how it differs from MCP (agent-to-agent vs agent-to-tool)
- Read and construct Agent Cards (the `/.well-known/agent.json` discovery mechanism) with skills, authentication requirements, and supported capabilities
- Trace the full A2A task lifecycle: `tasks/send` -> status updates (submitted, working, input-required, completed, failed, canceled) -> final artifacts
- Implement multipart messages with `TextPart`, `FilePart`, and `DataPart` for rich agent-to-agent communication
- Build an A2A server that advertises capabilities via an Agent Card and processes tasks
- Build an A2A client that discovers agents, sends tasks, and handles streaming status updates
- Implement push notifications so a server can proactively notify clients of task progress via webhooks

### Prerequisites

- [`../core/18_multi_agent_basics.ipynb`](../core/18_multi_agent_basics.ipynb) — You need to understand multi-agent collaboration patterns (message passing, shared state, delegation) before standardizing them with a protocol
- [`../appendix/14_graph_data_structures.ipynb`](../appendix/14_graph_data_structures.ipynb) — Agent networks form graphs; understanding graph traversal helps with discovery and routing in multi-agent systems

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Why agent-to-agent protocols | The problem: agents from different vendors/frameworks cannot collaborate today. N agents need N*(N-1) custom integrations. A2A reduces this to a shared contract. Real-world scenarios: travel booking, research pipelines, enterprise workflows. |
| 2 | A2A architecture overview | The key abstractions: Agent Cards, Tasks, Messages, Parts, Artifacts. The HTTP+JSON wire format. How A2A compares to MCP (complementary, not competing). |
| 3 | Agent Cards and discovery | Build an Agent Card with `name`, `description`, `url`, `skills`, `authentication`, and `capabilities`. Serve it at `/.well-known/agent.json`. Implement a client that discovers agents by fetching their cards. |
| 4 | The Task lifecycle | Walk through task states: submitted -> working -> input-required -> completed/failed/canceled. Build a state machine diagram. Understand `tasks/send`, `tasks/get`, `tasks/cancel`. Idempotency via task IDs. |
| 5 | Messages and Parts | Construct multipart messages with `TextPart` (plain text or markdown), `FilePart` (binary data with MIME types), and `DataPart` (structured JSON). Role semantics: user messages vs agent messages. |
| 6 | Building an A2A server | Implement a FastAPI-based A2A server: serve the Agent Card, handle `tasks/send`, process tasks asynchronously, return streaming status updates via SSE, produce final artifacts. |
| 7 | Streaming and push notifications | Implement `tasks/sendSubscribe` for SSE-based streaming updates. Add webhook-based push notifications (`tasks/pushNotification/set`) for long-running tasks where the client cannot hold a connection open. |
| 8 | Two-agent collaboration | Build two A2A agents — a "Researcher" that finds information and an "Writer" that produces reports. The client sends a task to the Writer, which discovers and delegates sub-tasks to the Researcher via A2A, then synthesizes the final output. |

### Putting It Together

The capstone builds a two-agent system where agents from different "organizations" collaborate through A2A. Agent A is a research specialist: it can search the web and summarize articles. Agent B is a report writer: it can structure findings into a formatted report. A client sends a research topic to Agent B. Agent B discovers Agent A via its Agent Card, delegates research sub-tasks via `tasks/send`, streams progress updates back to the original client, and produces a final report artifact. Neither agent knows the other's implementation — they communicate purely through the A2A protocol.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Add a skill to your Agent Card | Starter | Add a second skill to your A2A server's Agent Card (e.g., "summarization" alongside "research"). Write a client that filters agents by skill before sending tasks. |
| 2 | Handle `input-required` state | Moderate | Modify your server to pause a task with `input-required` status when it needs clarification. Write a client that detects this state, prompts the user, and sends a follow-up message to continue the task. |
| 3 | File artifacts | Moderate | Have your server produce a `FilePart` artifact (e.g., a CSV file or PDF report). Implement the client-side code to receive and save the file. |
| 4 | Three-agent pipeline | Stretch | Add a third agent (e.g., "Fact Checker") to the system. The Writer discovers both the Researcher and the Fact Checker, delegates to each, and only produces the final report after the Fact Checker validates the Researcher's findings. Implement the full discovery and delegation flow. |

### Key References

- [A2A Specification (Google)](https://google.github.io/A2A/) — The official spec; start with the overview, then read the protocol detail page
- [A2A GitHub Repository](https://github.com/google/A2A) — Reference implementations, samples, and the spec source
- [Google — Announcing A2A](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/) — The launch blog post with motivation and partner list
- [A2A Specification — Agent Card](https://google.github.io/A2A/#/documentation?id=agent-card) — The discovery mechanism specification
- [A2A Specification — Task Lifecycle](https://google.github.io/A2A/#/documentation?id=agent-task-lifecycle) — States, transitions, and message semantics
- [MCP vs A2A — Clearly Explained (Clarifai)](https://www.clarifai.com/blog/mcp-vs-a2a-clearly-explained) — Clear comparison of the two protocols and how they complement each other
- [A2A Python SDK](https://github.com/google/A2A/tree/main/sdk/python) — Google's official Python SDK for building A2A clients and servers
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — Multi-agent patterns that A2A standardizes

---

## 04. MCP plus A2A

**File:** `04_mcp_plus_a2a.ipynb`

### Overview

MCP and A2A are not competing protocols — they are complementary layers of an agent interoperability stack. MCP handles the vertical axis: an agent connecting to tools and data sources. A2A handles the horizontal axis: agents collaborating with other agents. This notebook builds a system that uses both protocols together: agents discover and delegate to each other via A2A, while each agent accesses its own tools through MCP servers. This is the architecture that the industry is converging on, and building it end-to-end is the best way to understand where each protocol fits.

### Learning Objectives

By the end of this notebook, you will be able to:
- Articulate the MCP + A2A layered architecture: MCP for agent-to-tool (vertical), A2A for agent-to-agent (horizontal)
- Design a system where agents advertise MCP-powered capabilities through A2A Agent Cards
- Build an agent that uses MCP clients internally to access tools and exposes its capabilities externally via A2A
- Implement cross-protocol task delegation: an A2A task triggers MCP tool calls, and MCP results flow back as A2A artifacts
- Handle failure modes that span both protocols: MCP tool failures surfaced as A2A task errors, timeout propagation, partial results
- Evaluate when to use MCP alone, A2A alone, or both together based on system requirements
- Design agent network topologies: star (single orchestrator), mesh (peer-to-peer), and hierarchical (delegated orchestration)

### Prerequisites

- [`01_mcp_from_scratch.ipynb`](01_mcp_from_scratch.ipynb) — Deep understanding of MCP protocol, transports, and the tool/resource/prompt primitives
- [`02_building_mcp_servers.ipynb`](02_building_mcp_servers.ipynb) — Practical experience building and testing MCP servers with the SDK
- [`03_a2a_protocol.ipynb`](03_a2a_protocol.ipynb) — Full understanding of A2A: Agent Cards, task lifecycle, multipart messages, streaming

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | The two-protocol architecture | Why one protocol is not enough. MCP's scope (tools, resources, prompts) vs A2A's scope (discovery, delegation, collaboration). The "USB + TCP/IP" analogy: MCP is the peripheral protocol, A2A is the network protocol. |
| 2 | Designing the system | Architecture diagram for the capstone: an Orchestrator agent, a Data agent (with MCP access to a database), and a Chart agent (with MCP access to a plotting library). Agent Cards advertise skills powered by MCP tools. |
| 3 | MCP-powered agents | Build two specialist agents, each backed by MCP servers. The Data agent connects to an MCP server exposing SQL query tools. The Chart agent connects to an MCP server exposing matplotlib plotting tools. Each agent wraps MCP tool results into its reasoning. |
| 4 | A2A discovery and delegation | Build the Orchestrator agent. It discovers the Data and Chart agents via their Agent Cards, decomposes a user request ("show me sales trends") into sub-tasks, and delegates via A2A `tasks/send`. |
| 5 | Cross-protocol data flow | Trace a request end-to-end: user -> Orchestrator (A2A) -> Data Agent (A2A) -> SQL MCP Server (MCP) -> query result -> Data Agent -> Orchestrator (A2A) -> Chart Agent (A2A) -> Matplotlib MCP Server (MCP) -> chart image -> Chart Agent -> Orchestrator -> user. Implement this full flow. |
| 6 | Error handling across protocol boundaries | What happens when an MCP tool call fails mid-task? Implement: MCP error -> agent catches and retries or reports -> A2A task status set to `failed` with error details in the message. Timeout propagation. Partial result handling. |
| 7 | Agent network topologies | Implement three patterns: (1) Star — single orchestrator delegates to specialists. (2) Mesh — agents discover and call each other peer-to-peer. (3) Hierarchical — orchestrator delegates to sub-orchestrators. Compare tradeoffs: latency, failure isolation, complexity. |
| 8 | When to use what | Decision framework: MCP alone (single agent + tools), A2A alone (homogeneous agents sharing work), both together (heterogeneous specialists with their own tool ecosystems). Real-world case studies. |

### Putting It Together

The capstone is a "Data Analysis Pipeline" that demonstrates the full MCP + A2A stack. The user asks a natural language question about a dataset (e.g., "What were the top 5 products by revenue last quarter, and show me the trend?"). The Orchestrator agent decomposes this into sub-tasks. It delegates the data query to the Data agent (which uses MCP to run SQL queries against a SQLite database). It then sends the query results to the Chart agent (which uses MCP to generate a matplotlib chart). Both agents stream progress via A2A. The Orchestrator collects the artifacts — a text summary from the Data agent and a chart image from the Chart agent — and assembles a final response. You add structured logging at every protocol boundary to trace the full MCP and A2A message flow.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Add a third specialist | Starter | Add a "Summary" agent that takes data results and produces a written analysis. Wire it into the Orchestrator's delegation flow. It does not need MCP tools — it just uses its LLM directly. |
| 2 | Graceful degradation | Moderate | Simulate the Chart agent being unavailable (shut down its server). Modify the Orchestrator to detect the A2A failure, skip the charting step, and return a text-only result with a note that visualization was unavailable. |
| 3 | Caching layer | Moderate | Add a caching MCP server that the Orchestrator uses to store and retrieve previous query results. Before delegating to the Data agent, check the cache. Implement cache invalidation based on TTL. |
| 4 | Multi-hop research pipeline | Stretch | Build a 4-agent research system: (1) Search agent (MCP: web search tool), (2) Reader agent (MCP: URL fetch + extraction tool), (3) Fact-checker agent (MCP: knowledge base tool), (4) Writer agent (no MCP, LLM-only). The Orchestrator sends a research question, and agents collaborate via A2A, each using their MCP tools. Implement the full discovery, delegation, and artifact assembly flow. |

### Key References

- [MCP vs A2A — Clearly Explained (Clarifai)](https://www.clarifai.com/blog/mcp-vs-a2a-clearly-explained) — The clearest comparison of the two protocols and how they complement each other
- [MCP Specification](https://modelcontextprotocol.io/) — Full spec reference for the tool/resource/prompt layer
- [A2A Specification (Google)](https://google.github.io/A2A/) — Full spec reference for the discovery/delegation/collaboration layer
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) — For building the MCP server components
- [A2A Python SDK](https://github.com/google/A2A/tree/main/sdk/python) — For building the A2A client and server components
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — Multi-agent design patterns that this notebook implements with real protocols
- [Google — A2A and MCP: Better Together](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/) — Google's perspective on protocol complementarity
- [MCP GitHub Organization](https://github.com/modelcontextprotocol) — Reference implementations and community servers
- [A2A GitHub Repository](https://github.com/google/A2A) — Reference implementations and samples
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — The foundational mental model: tool use + planning + memory — MCP and A2A standardize the tool use and multi-agent layers
