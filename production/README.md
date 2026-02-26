# Async & Production Patterns — Lesson Plans

> Detailed lesson plans for notebooks 01–08. Real agent systems need concurrency, streaming, deployment, and state management.
> For the full track overview, see [`../roadmap.md`](../roadmap.md).

---

## 01. Async Fundamentals

**File:** `01_async_fundamentals.ipynb`

### Overview
This notebook teaches the concurrency model that production agents depend on: Python's `asyncio`. You build async HTTP pipelines with `httpx.AsyncClient` that dispatch multiple tool calls in parallel rather than sequentially, cutting agent latency by the number of independent calls. Every subsequent production notebook builds on async patterns introduced here, making this the single most important unlock for agent performance — real agents spend most of their wall-clock time waiting on I/O (LLM APIs, web requests, database queries), and concurrency lets you overlap that waiting.

### Learning Objectives
By the end of this notebook, you will be able to:
- Explain the difference between concurrency and parallelism, and why asyncio uses cooperative multitasking for I/O-bound agent workloads
- Write coroutines with `async def` and `await`, and run them with `asyncio.run()` and in Jupyter notebooks
- Use `asyncio.gather()` and `asyncio.TaskGroup` to execute multiple coroutines concurrently with structured error handling
- Make non-blocking HTTP requests with `httpx.AsyncClient`, including timeouts, retries, and connection pooling
- Refactor a sequential multi-tool agent into an async agent that dispatches independent tool calls in parallel
- Measure and compare wall-clock time for sequential vs. concurrent execution with timing instrumentation

### Prerequisites
- [`../core/05_react_agent.ipynb`](../core/05_react_agent.ipynb) — you need a working ReAct agent loop to make async
- [`../appendix/11_async_and_await.ipynb`](../appendix/11_async_and_await.ipynb) — covers the asyncio event loop, `async`/`await` syntax, and `asyncio.gather` from first principles

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Why Async Matters for Agents | Visualize where time is spent in a typical agent run — nearly all of it is I/O wait. Measure 5 sequential LLM calls and establish the baseline latency to beat. |
| 2 | Coroutines and the Event Loop | Write basic coroutines, understand `await` suspension points, visualize the event loop's task switching with a logging example. Run a minimal example in a Jupyter cell. |
| 3 | Gathering Concurrent Tasks | Use `asyncio.gather()` to run multiple coroutines concurrently. Compare `gather(return_exceptions=True)` with Python 3.11's `TaskGroup` for structured concurrency. |
| 4 | Async HTTP with httpx | Replace synchronous `httpx.post()` calls with `httpx.AsyncClient`. Configure timeouts, connection limits, and retry logic. Make concurrent API calls to OpenRouter. |
| 5 | Async Tool Dispatch | Build an async tool registry where each tool is an `async def`. Wire it into the agent loop so independent tool calls execute concurrently via `asyncio.gather`. |
| 6 | Error Handling and Cancellation | Handle timeouts with `asyncio.wait_for()`, protect critical tasks with `asyncio.shield()`, and implement structured error handling for partial failures in gathered tasks. |
| 7 | Semaphores and Rate Limiting | Use `asyncio.Semaphore` to limit concurrent API calls (respect rate limits). Build a simple async rate limiter that prevents 429 errors from the LLM provider. |
| 8 | Async Agent: Full Integration | Combine everything into a complete async ReAct agent with parallel tool calls, proper error handling, rate limiting, and timing instrumentation. Benchmark the speedup. |

### Putting It Together
The capstone exercise wires together an async ReAct agent that receives a complex question requiring three different tools (web search, calculator, and knowledge lookup). The agent identifies that all three tool calls are independent, dispatches them concurrently via `asyncio.gather` with a semaphore limiting concurrency to 3, collects the results, and synthesizes a final answer. You measure the wall-clock improvement over the sequential baseline and handle partial failures gracefully — if one tool times out, the agent still uses results from the tools that succeeded.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Async Weather Dashboard | Starter | Fetch weather data from 5 cities concurrently using `httpx.AsyncClient` and display results as they arrive using `asyncio.as_completed()`. |
| 2 | Retry with Exponential Backoff | Moderate | Implement an async retry decorator that retries failed HTTP calls with exponential backoff and jitter, configurable max retries, and proper timeout handling. |
| 3 | Rate-Limited Parallel Calls | Moderate | Build an async scraper that fetches 10 URLs concurrently with an `asyncio.Semaphore` limiting to 3 simultaneous requests, collecting all results without triggering rate limits. |
| 4 | Fully Async Multi-Tool Agent | Stretch | Extend the ReAct agent to detect which tool calls are independent (no data dependencies) and execute them in parallel, falling back to sequential for dependent calls. Measure the speedup on 5 different queries. |

### Key References
- [Python asyncio documentation](https://docs.python.org/3/library/asyncio.html) — official reference for the event loop, tasks, and synchronization primitives
- [httpx async documentation](https://www.python-httpx.org/async/) — async HTTP client API, connection pooling, streaming
- [Real Python — Async IO in Python](https://realpython.com/async-io-python/) — comprehensive tutorial from basics to advanced patterns
- [Python 3.11 TaskGroup](https://docs.python.org/3/library/asyncio-task.html#asyncio.TaskGroup) — structured concurrency for cleaner error handling
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — architecture patterns including parallel tool execution
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — foundational agent architecture reference

---

## 02. Streaming Responses

**File:** `02_streaming_responses.ipynb`

### Overview
This notebook teaches you to stream LLM output token-by-token instead of waiting for complete responses. You build a streaming pipeline using Server-Sent Events (SSE) that progressively renders agent reasoning and tool calls in real time. This is critical for production agents because users expect immediate feedback — a 10-second wait with no output feels broken, while streaming the first token in 200ms feels responsive. You wire up OpenRouter's streaming API, parse incremental deltas, and build a streaming agent loop that interleaves streamed reasoning with tool execution.

### Learning Objectives
By the end of this notebook, you will be able to:
- Explain the SSE protocol and how it differs from WebSockets and long-polling
- Consume streaming responses from the OpenRouter chat completions API using `httpx` async streaming
- Parse incremental SSE chunks (`data:` frames) and reconstruct complete messages from deltas
- Build a progressive renderer that displays agent reasoning as tokens arrive
- Detect and handle tool-call deltas within a streaming response
- Implement a streaming agent loop that interleaves streamed LLM output with tool execution

### Prerequisites
- [`01_async_fundamentals.ipynb`](01_async_fundamentals.ipynb) — async HTTP and coroutines are required for non-blocking stream consumption
- [`../appendix/13_websockets_and_streaming.ipynb`](../appendix/13_websockets_and_streaming.ipynb) — covers the SSE and WebSocket protocols, streaming patterns, and `async for` iteration

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Why Streaming Matters | Compare user experience of blocking vs. streaming responses. Measure time-to-first-token vs. time-to-complete for a typical agent response. Discuss TTFT as a UX metric. |
| 2 | Server-Sent Events Protocol | Understand the SSE format (`data:`, `event:`, `id:`, `retry:` fields). Parse raw SSE frames by hand. Compare with WebSockets and when to use each. |
| 3 | Streaming from OpenRouter | Make a streaming chat completion request with `stream=True`, iterate over SSE chunks with `httpx.AsyncClient.stream()` and `aiter_lines()`, and handle the `[DONE]` sentinel. |
| 4 | Reconstructing Messages from Deltas | Accumulate `delta.content` chunks into a complete message. Handle partial JSON, empty deltas, and multi-choice responses. Build a helper that yields complete tokens as they arrive. |
| 5 | Streaming Tool Calls | Parse streamed tool-call deltas (`delta.tool_calls`), accumulate function name and arguments across chunks, detect when a tool call is complete and ready for dispatch. |
| 6 | Progressive Rendering in Notebooks | Display streaming text in a Jupyter notebook using `IPython.display` — clear-and-rewrite approach for smooth UX. Handle markdown formatting mid-stream without breaking rendering. |
| 7 | Streaming Agent Loop | Build a complete agent loop that streams LLM reasoning, detects tool calls mid-stream, pauses streaming to execute tools, and resumes streaming — all visible in real time. |
| 8 | Backpressure and Buffering | Handle slow consumers: word-level and sentence-level buffering strategies, dropping frames for display, ensuring tool-call parsing never misses chunks even when display is throttled. |

### Putting It Together
The capstone builds a streaming ReAct agent that displays its thought process in real time. As the LLM generates text, reasoning appears token-by-token. When the agent decides to call a tool, the tool name and arguments stream in, the tool executes (with a progress indicator), and the observation is displayed. The user sees the complete Thought/Action/Observation cycle unfold live, rather than waiting for the entire loop to finish. The entire interaction uses SSE and handles mid-stream tool interruptions cleanly.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Basic Streaming Display | Starter | Stream a simple chat completion from OpenRouter and print each token as it arrives, measuring time-to-first-token and total duration. |
| 2 | Markdown-Safe Buffering | Moderate | Build a buffer that accumulates tokens and only flushes complete markdown elements (e.g., don't flush half a `**bold**` tag or an incomplete code fence). |
| 3 | Multi-Model Stream Race | Moderate | Send the same prompt to two models simultaneously, stream both responses side-by-side, and let the user pick the better one after both finish. |
| 4 | Full Streaming Agent with Progress | Stretch | Build a streaming agent that shows a progress indicator for tool execution, streams reasoning text, and renders the final answer with syntax-highlighted code blocks — all in a Jupyter notebook. |

### Key References
- [OpenRouter streaming documentation](https://openrouter.ai/docs/api-reference/streaming) — streaming parameters, SSE format, delta structure
- [MDN — Server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) — canonical reference for the SSE protocol
- [OpenAI streaming guide](https://platform.openai.com/docs/api-reference/streaming) — delta format for chat completions (OpenRouter follows the same format)
- [httpx streaming responses](https://www.python-httpx.org/async/#streaming-responses) — `aiter_bytes`, `aiter_lines`, and `aiter_text` for async stream consumption
- [Anthropic streaming messages](https://docs.anthropic.com/en/api/messages-streaming) — event types and delta patterns for Claude's streaming API

---

## 03. API Serving

**File:** `03_api_serving.ipynb`

### Overview
This notebook wraps an agent in a FastAPI web service, turning a notebook prototype into something other applications can call over HTTP. You build REST endpoints for synchronous agent invocation, a streaming endpoint using Server-Sent Events, and a WebSocket endpoint for bidirectional multi-turn conversation. This is the bridge between "I built an agent" and "other people and systems can use my agent" — every subsequent production notebook (monitoring, containers, auth) builds on this API layer.

### Learning Objectives
By the end of this notebook, you will be able to:
- Create a FastAPI application with typed request/response models using Pydantic
- Expose an agent as a POST endpoint that accepts a user message and returns the agent's final answer
- Implement a streaming endpoint that sends agent reasoning and tool calls as SSE events via `StreamingResponse`
- Build a WebSocket endpoint for multi-turn conversational agents with connection lifecycle management
- Add structured error handling, request validation, and CORS middleware
- Run and test the API locally with `uvicorn` and write integration tests with `httpx.AsyncClient`

### Prerequisites
- [`01_async_fundamentals.ipynb`](01_async_fundamentals.ipynb) — FastAPI is async-native; you need coroutine fluency
- [`../core/05_react_agent.ipynb`](../core/05_react_agent.ipynb) — the agent you will wrap in an API

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | From Notebook to Service | Why agents need APIs. The gap between a working notebook and a callable service. Architecture overview of the sync, streaming, and WebSocket endpoints you will build. |
| 2 | FastAPI Crash Course | Install FastAPI + uvicorn, create a minimal app, define Pydantic request/response models, understand routing and automatic OpenAPI docs. Run the server from a notebook cell. |
| 3 | Synchronous Agent Endpoint | `POST /agent/invoke` — accepts a user message, runs the ReAct agent, returns the final answer with tool call details and token usage. Add request validation and structured error responses. |
| 4 | Streaming Agent Endpoint | `POST /agent/stream` — returns a `StreamingResponse` with SSE-formatted events (reasoning, tool calls, observations, final answer). Wire up the streaming pipeline from notebook 02. |
| 5 | WebSocket Conversation Endpoint | `WS /agent/chat` — bidirectional WebSocket for multi-turn conversation. Maintain conversation history per connection. Handle disconnects and reconnection gracefully. |
| 6 | Middleware and CORS | Add CORS middleware for browser clients, request logging middleware with timing, and a request-ID middleware for distributed traceability. |
| 7 | Testing the Agent API | Use `httpx.AsyncClient` with FastAPI's `ASGITransport` to write in-process integration tests. Test each endpoint (sync, streaming, WebSocket) without starting a real server. |
| 8 | Running in Production Mode | Configure uvicorn workers, discuss ASGI deployment (gunicorn + uvicorn workers), and preview what containerization (notebook 06) and auth (notebook 07) will add. |

### Putting It Together
The capstone assembles a complete agent API server with all three endpoint groups (invoke, stream, chat), conversation management, health checks, and OpenAPI documentation. You run it locally with uvicorn and write a client script that demonstrates each endpoint: a single synchronous call, a streaming call that prints tokens as they arrive, and a multi-turn WebSocket conversation. The client script serves as both a test and a usage example for anyone consuming the agent API.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Health and Metadata Endpoints | Starter | Add `GET /health` (returns status + uptime) and `GET /agent/info` (returns agent name, available tools, model name) endpoints. |
| 2 | Conversation History Endpoint | Moderate | Add `GET /conversations/{session_id}` that returns the full message history for a WebSocket session, stored in an in-memory dict with proper cleanup. |
| 3 | Background Agent Tasks | Moderate | Add a `POST /agent/tasks` endpoint that starts an agent run in the background, returns a task ID immediately, and provides `GET /agent/tasks/{id}` for polling results. |
| 4 | Multi-Agent Router | Stretch | Create a FastAPI app that routes requests to different agents (research, code, general) based on a `type` field in the request body. Each agent runs as a separate async task with its own system prompt and tool set. |

### Key References
- [FastAPI documentation](https://fastapi.tiangolo.com/) — official tutorial, from basics through advanced features
- [FastAPI WebSockets](https://fastapi.tiangolo.com/advanced/websockets/) — WebSocket endpoint patterns and connection management
- [FastAPI StreamingResponse](https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse) — SSE and streaming response patterns
- [Pydantic V2 documentation](https://docs.pydantic.dev/latest/) — model definitions for request/response validation
- [uvicorn documentation](https://www.uvicorn.org/) — ASGI server configuration and deployment
- [httpx documentation](https://www.python-httpx.org/) — the HTTP client you will use to test your API

---

## 04. Monitoring and Cost

**File:** `04_monitoring_and_cost.ipynb`

### Overview
This notebook builds the instrumentation layer that every production agent needs: token counting, cost estimation, latency tracking, and threshold-based alerting. You build a monitoring wrapper that captures every LLM call's metrics and a cost calculator that estimates spend in real time. Without this, you are flying blind — you cannot optimize what you cannot measure, and LLM API costs can spiral quickly when agents loop excessively or use expensive models for simple tasks.

### Learning Objectives
By the end of this notebook, you will be able to:
- Count prompt and completion tokens for each LLM call using the API response metadata
- Calculate per-call and per-session cost using model-specific pricing tables from OpenRouter
- Measure and record latency metrics (time-to-first-token, total duration, tokens-per-second)
- Build a metrics collector that stores usage data across an agent's lifetime and supports querying
- Implement threshold-based alerts for cost overruns, latency spikes, and excessive tool-call loops
- Generate a session summary report with cost breakdown by model, tool, and reasoning step

### Prerequisites
- [`../core/05_react_agent.ipynb`](../core/05_react_agent.ipynb) — the agent you will instrument
- [`01_async_fundamentals.ipynb`](01_async_fundamentals.ipynb) — async context managers and wrapper patterns for non-blocking metric collection

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | The Cost of Ignorance | Show a real agent session's hidden costs: 15 LLM calls, 12K tokens, tool retries, $0.35 spent on one question. Motivate why monitoring is not optional. |
| 2 | Token Counting | Extract `usage.prompt_tokens` and `usage.completion_tokens` from OpenRouter API responses. Build a `TokenTracker` that accumulates counts per session with per-call breakdowns. |
| 3 | Cost Estimation | Build a pricing table mapping OpenRouter model IDs to per-token costs (input vs. output). Calculate cost per call and running total. Handle models with different prompt vs. completion pricing. |
| 4 | Latency Instrumentation | Wrap LLM calls with timing decorators. Record time-to-first-token (for streaming), total call duration, and tokens-per-second throughput. Store as structured timing data. |
| 5 | The Metrics Collector | Build a `MetricsCollector` class that intercepts every LLM call, records token usage, cost, latency, and tool invocations, and stores them in a structured log with timestamps. |
| 6 | Alerting and Guardrails | Implement threshold-based alerts: abort if session cost exceeds $0.50, warn if a single call takes >30s, detect infinite tool-call loops (same tool called >5 times with similar arguments). |
| 7 | Session Summary Reports | Generate an end-of-session report: total cost, cost breakdown by step and tool, slowest calls, most expensive calls, tool success rates. Display as formatted tables. |
| 8 | Visualizing Agent Performance | Plot latency distributions, cost-per-step bar charts, and token usage over time using matplotlib. Identify bottlenecks visually from a batch of agent runs. |

### Putting It Together
The capstone wraps the ReAct agent with the full monitoring stack: every LLM call is instrumented with token counting, cost estimation, and latency tracking. Run the agent on 3 different queries of varying complexity (a simple factual question, a multi-step reasoning problem, and a tool-heavy research task) and generate a comparative report. The report reveals which queries are expensive, which tools are slow, and where optimization would have the highest impact. At least one alert fires during the test run when the complex query triggers excessive tool calls.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Per-Model Cost Comparison | Starter | Run the same prompt through 3 different OpenRouter models, compare token usage and cost, and display a comparison table showing cost-per-quality tradeoffs. |
| 2 | Budget-Aware Agent | Moderate | Modify the agent loop to check remaining budget before each LLM call. If the budget is exhausted, return the best answer so far instead of making another call. |
| 3 | Latency Budget Enforcer | Moderate | Build a wrapper that enforces a total latency budget: if the agent has used 80% of its 30-second budget, force it to return its best answer so far instead of starting another tool call. |
| 4 | Cost Anomaly Detection | Stretch | Implement a sliding-window anomaly detector that alerts when the last 10 minutes of spend deviates more than 2 standard deviations from the rolling hourly average. |

### Key References
- [OpenRouter API reference](https://openrouter.ai/docs/api-reference) — token usage fields in API responses and account-level usage endpoints
- [Anthropic — Token counting](https://docs.anthropic.com/en/docs/build-with-claude/token-counting) — how to count tokens before sending requests, model-specific tokenizers
- [tiktoken](https://github.com/openai/tiktoken) — OpenAI's fast tokenizer library for client-side token estimation
- [Langfuse — LLM observability](https://langfuse.com/docs) — open-source observability platform that automates what this notebook builds manually
- [Helicone](https://www.helicone.ai/) — LLM proxy that captures metrics transparently without code changes
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — includes patterns for monitoring agent loops and preventing runaway costs

---

## 05. Database for Agents

**File:** `05_database_for_agents.ipynb`

### Overview
This notebook adds persistent state to your agents using SQLite and SQLAlchemy. You design a database schema for storing conversation sessions, agent memory, tool execution history, and metadata, then build a persistence layer that lets agents resume conversations, recall past interactions, and maintain state across server restarts. In-memory state is fine for demos, but production agents need durable storage — without it, every server restart wipes all context and every user session starts from zero.

### Learning Objectives
By the end of this notebook, you will be able to:
- Design a relational schema for agent state: sessions, messages, tool calls, and metadata
- Use SQLAlchemy ORM to define models, create tables, and perform CRUD operations
- Build a `SessionManager` that creates, loads, resumes, and archives agent conversations
- Store and retrieve full conversation histories with message roles, timestamps, and token counts
- Persist tool execution results for auditability, replay, and analytics
- Query historical data for insights: most-used tools, average session length, failure rates, cost trends

### Prerequisites
- [`../appendix/12_databases_and_sql.ipynb`](../appendix/12_databases_and_sql.ipynb) — covers SQLite basics, raw SQL, and SQLAlchemy ORM fundamentals from scratch
- [`../core/12_conversation_memory.ipynb`](../core/12_conversation_memory.ipynb) — covers in-memory conversation management and context window strategies that this notebook makes persistent

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Why Agents Need Databases | Walk through failure modes of in-memory state: server restarts lose everything, no cross-session memory, no audit trail. Compare with what persistence enables. |
| 2 | Schema Design for Agents | Design four tables: `sessions` (id, user_id, created_at, status), `messages` (role, content, tokens, session_id), `tool_calls` (name, args, result, latency, success), `metadata` (key-value per session). Discuss relationships, indexes, and why timestamps matter. |
| 3 | SQLAlchemy Models | Define ORM models for each table. Set up `relationship()` for session-to-messages and message-to-tool-calls. Configure SQLite with WAL mode for concurrent reads. Run `create_all()`. |
| 4 | Session Management | Build a `SessionManager` class: `create_session()`, `load_session()`, `list_sessions()`, `archive_session()`. Each session has a UUID, creation time, and status lifecycle (active, paused, archived). |
| 5 | Conversation Persistence | Store each message with its full content, role, timestamp, and token count. Implement `get_recent_messages(n)`, `search_messages(query)`, and `get_conversation_context(token_budget)` for context-aware retrieval. |
| 6 | Tool Call Logging | Record every tool invocation: tool name, arguments, result, duration, and success/failure. Build queries for tool usage analytics: most-used tools, average latency per tool, failure rates. |
| 7 | Wiring It Into the Agent | Integrate the database layer with the async ReAct agent from notebook 01. Every message and tool call is persisted automatically. Restart the agent and resume a conversation seamlessly. |
| 8 | Migrations and Maintenance | Handle schema changes with lightweight migration patterns (add column, create index, backfill data). Discuss when to graduate to Alembic. Implement a cleanup job for old sessions. |

### Putting It Together
The capstone replaces the in-memory conversation store from notebook 03's FastAPI app with the fully persistent database layer. Start a multi-turn conversation, send several messages with tool calls, shut down the server (simulate a restart), resume the conversation from the database, and verify continuity. Then query the database to generate an analytics report: total sessions, average conversation length, most-used tools, and failure rates. The agent's state survives restarts, and its history is queryable.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Conversation Search | Starter | Add full-text search to the messages table using SQLite FTS5. Build a `search_conversations(query)` function that finds relevant past conversations with context. |
| 2 | User Preferences Store | Moderate | Add a `user_preferences` table that stores key-value pairs per user. The agent reads preferences at session start and updates them based on conversation signals. |
| 3 | Token-Budgeted History | Moderate | Implement `get_context(max_tokens=4000)` that returns as many recent messages as fit within the token budget, dropping oldest messages first when the budget is exceeded. |
| 4 | Async Database Layer | Stretch | Replace synchronous SQLAlchemy with `aiosqlite` + SQLAlchemy's async engine. All database operations become non-blocking, suitable for the async agent from notebook 01. |

### Key References
- [SQLAlchemy 2.0 Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/) — the official unified tutorial covering ORM and Core
- [SQLite documentation](https://www.sqlite.org/docs.html) — SQLite-specific features, limits, and best practices
- [SQLite WAL mode](https://www.sqlite.org/wal.html) — Write-Ahead Logging for concurrent read access
- [SQLAlchemy async session](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html) — async ORM usage with aiosqlite
- [Alembic documentation](https://alembic.sqlalchemy.org/en/latest/) — database migration tool for SQLAlchemy
- [Letta (MemGPT)](https://www.letta.com/) — production agent memory architecture using tiered database storage (core/recall/archival)

---

## 06. Containerized Agents

**File:** `06_containerized_agents.ipynb`

### Overview
This notebook packages an agent into a Docker container and deploys it to a cloud platform. You go from "it works on my machine" to "it runs anywhere" — writing a Dockerfile, building optimized images with multi-stage builds, handling environment variables and secrets securely, and deploying to Modal, Fly.io, or Railway. Containerization is the standard way to ship software, and agents are no exception. This is the step that makes your agent deployable, reproducible, and scalable.

### Learning Objectives
By the end of this notebook, you will be able to:
- Write a Dockerfile that packages a FastAPI agent application with all dependencies
- Build and run Docker containers locally, passing API keys via environment variables securely
- Configure multi-stage builds to minimize container image size (from ~1GB to ~200MB)
- Deploy a containerized agent to at least one cloud platform (Modal, Fly.io, or Railway)
- Set up health checks, restart policies, and graceful shutdown for containerized agents
- Manage persistent storage (database volumes) across container restarts and redeploys

### Prerequisites
- [`03_api_serving.ipynb`](03_api_serving.ipynb) — the FastAPI agent application you will containerize
- [`05_database_for_agents.ipynb`](05_database_for_agents.ipynb) — persistent state that must survive container restarts

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Why Containers for Agents | The "works on my machine" problem. Why Docker is the standard for deployment. Overview of the container lifecycle for an agent application. Compare with bare-metal and virtual machine deployment. |
| 2 | Writing a Dockerfile | Build a Dockerfile for the FastAPI agent: base image selection (`python:3.11-slim`), `COPY`, `RUN pip install`, `CMD`. Understand layer caching, build context, and `.dockerignore`. |
| 3 | Multi-Stage Builds | Optimize the image: builder stage installs dependencies with build tools, runtime stage copies only the installed packages. Reduce image size from ~1GB to ~200MB. Compare sizes. |
| 4 | Secrets and Environment Variables | Pass `OPENROUTER_API_KEY` securely via `docker run -e` or `--env-file`. Never bake secrets into images. Verify with `docker history`. Discuss secrets management patterns for production. |
| 5 | Local Docker Development | Build and run the container locally. Test all endpoints (invoke, stream, WebSocket). Mount volumes for the SQLite database so data persists across `docker stop`/`docker start` cycles. |
| 6 | Deploying to a Cloud Platform | Step-by-step deployment to one platform: Modal (serverless, Python-native), Fly.io (container-based, global edge), or Railway (git-push deploys). Walk through each platform's deployment flow and compare tradeoffs. |
| 7 | Health Checks and Resilience | Add a Docker `HEALTHCHECK` instruction. Configure the cloud platform's health monitoring. Set up restart policies so the container auto-recovers from crashes. Test with a simulated failure. |
| 8 | Persistent Storage in the Cloud | Configure cloud volumes or managed databases so the SQLite data survives redeploys. Discuss when to upgrade from SQLite to PostgreSQL. Demonstrate a zero-downtime redeploy that preserves all data. |

### Putting It Together
The capstone deploys the complete agent stack (FastAPI + async agent + SQLite database + monitoring) to a cloud platform. You verify that the deployed agent responds to HTTP requests, streams correctly, maintains conversation state across calls, and survives a redeploy without losing data. You also set up a health check endpoint that the platform monitors, trigger a simulated crash to verify auto-recovery, and demonstrate a zero-downtime redeploy by pushing a configuration change.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Minimal Container | Starter | Write a Dockerfile for a simple "echo" FastAPI app. Build it, run it, and verify it responds on port 8000 with `curl`. |
| 2 | Docker Compose Multi-Service | Moderate | Create a `docker-compose.yml` that runs the agent API and a separate metrics dashboard service, connected via a shared Docker network with a shared database volume. |
| 3 | CI/CD Pipeline | Moderate | Write a GitHub Actions workflow that builds the Docker image, runs the test suite inside the container, and pushes to a container registry on success. |
| 4 | Blue-Green Deployment | Stretch | Deploy two versions of the agent simultaneously. Route 10% of traffic to the new version, verify it works via health checks, then shift 100%. Implement using your chosen cloud platform's traffic splitting. |

### Key References
- [Docker — Python language guide](https://docs.docker.com/language/python/) — official guide for containerizing Python applications
- [Docker multi-stage builds](https://docs.docker.com/build/building/multi-stage/) — reduce image size with build stages
- [Modal documentation](https://modal.com/docs) — serverless Python deployment, GPU support, scheduled tasks
- [Fly.io documentation](https://fly.io/docs/) — container deployment with global edge distribution
- [Railway documentation](https://docs.railway.app/) — git-push deployment with automatic builds
- [12-Factor App](https://12factor.net/) — methodology for building portable, deployable applications (especially factor III: Config, and factor VI: Processes)

---

## 07. Agent as a Service

**File:** `07_agent_as_a_service.ipynb`

### Overview
This notebook transforms the basic FastAPI agent into a production-grade service with authentication, rate limiting, session management, and webhook callbacks. You build the features that real SaaS products need: API keys for access control, per-user rate limits to prevent abuse, persistent sessions so users can resume conversations, and webhooks so the agent can notify external systems when long-running tasks complete. This is where "demo" becomes "product" — the difference between an endpoint your team calls internally and a service you could open to external users.

### Learning Objectives
By the end of this notebook, you will be able to:
- Implement API key authentication with key generation, hashing, validation, and revocation
- Build a token-bucket rate limiter that enforces per-user and per-tier request limits
- Manage user sessions with unique IDs, TTL-based expiration, and database-backed persistence
- Implement webhook callbacks for asynchronous agent task completion with retry logic
- Add request queuing for long-running agent tasks with status polling and cancellation
- Design idempotent endpoints that handle client retries safely without duplicate processing

### Prerequisites
- [`03_api_serving.ipynb`](03_api_serving.ipynb) — the base FastAPI agent application to extend
- [`05_database_for_agents.ipynb`](05_database_for_agents.ipynb) — database layer for session, API key, and usage record persistence
- [`06_containerized_agents.ipynb`](06_containerized_agents.ipynb) — deployment infrastructure context for understanding production constraints

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | From API to Service | What separates an API endpoint from a production service. Survey real-world agent APIs (OpenAI, Anthropic) for patterns: auth, rate limits, usage tracking, async tasks, webhooks. |
| 2 | API Key Authentication | Generate random API keys, hash with SHA-256, store in the database. Use FastAPI's `Depends()` with a custom `verify_api_key` dependency. Return 401 for invalid keys, 403 for revoked keys. |
| 3 | Rate Limiting | Implement a sliding-window rate limiter. Track usage per API key with timestamps. Return 429 with `Retry-After` header when limits are exceeded. Configure tiers (free: 10 req/min, paid: 100 req/min). |
| 4 | Session Management | Extend database-backed sessions from notebook 05 with TTL-based expiration, automatic cleanup of stale sessions, and session-scoped conversation limits. Add session resume and archive endpoints. |
| 5 | Async Tasks and Webhooks | For long-running agent tasks: `POST /tasks` returns `202 Accepted` with a task ID. `GET /tasks/{id}` polls for status. When the agent finishes, POST the result to the client's registered webhook URL. Implement retry with exponential backoff for failed deliveries. |
| 6 | Usage Tracking | Record every request with timestamp, API key, tokens used, estimated cost, and latency. Build per-key usage summaries. Add `GET /usage` endpoint for clients to check their consumption. |
| 7 | Idempotency and Error Handling | Add idempotency keys to prevent duplicate processing on client retries. Implement consistent structured error responses with error codes, messages, and retry guidance. |
| 8 | Integration Test Suite | Write a comprehensive test suite covering: valid auth, invalid auth, rate limit enforcement, webhook delivery, session expiration, idempotency, and concurrent request handling. |

### Putting It Together
The capstone assembles the complete agent-as-a-service. A client script generates an API key, authenticates requests, creates a session, sends a complex multi-step query as an async task, registers a webhook callback URL, and receives the result via webhook when the agent finishes. The client also demonstrates rate limiting by sending a burst of requests, session resumption by continuing a conversation after a pause, and usage tracking by querying token consumption and cost. The entire flow is tested end-to-end.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | API Key Management CLI | Starter | Build notebook cells (or a small CLI) that creates, lists, and revokes API keys, storing them hashed in the database with creation timestamps. |
| 2 | Tiered Rate Limits | Moderate | Implement three tiers (free: 10 req/min, basic: 60 req/min, pro: 300 req/min). Associate each API key with a tier at creation and enforce the corresponding limit dynamically. |
| 3 | Webhook with Dead-Letter Queue | Moderate | Build the webhook delivery system with exponential backoff (retry at 1s, 4s, 16s, 64s) and a dead-letter queue table for permanently failed deliveries that can be retried manually. |
| 4 | Full Multi-Tenant Service | Stretch | Combine everything: multi-tenant isolation (users cannot see each other's sessions or data), per-tenant rate limits, usage dashboards, and admin endpoints for key management and system metrics. |

### Key References
- [FastAPI Security tutorial](https://fastapi.tiangolo.com/tutorial/security/) — OAuth2, API keys, and dependency-based auth patterns
- [Stripe webhook best practices](https://stripe.com/docs/webhooks/best-practices) — production webhook patterns: signatures, retries, idempotency
- [OpenAI API reference](https://platform.openai.com/docs/api-reference) — well-designed production agent API (auth, rate limits, usage tracking)
- [Anthropic API reference](https://docs.anthropic.com/en/api) — production API design with rate limiting, usage, and error handling
- [OWASP API Security Top 10](https://owasp.org/API-Security/) — common API security risks and mitigations
- [webhooks.fyi](https://webhooks.fyi/) — patterns for reliable webhook delivery, retry logic, and security

---

## 08. Managed Platforms

**File:** `08_managed_platforms.ipynb`

### Overview
This notebook surveys the major managed agent platforms — Amazon Bedrock AgentCore, Azure AI Foundry, and Google Vertex AI Agent Builder — plus developer-focused platforms like Modal. Instead of building everything yourself (as in notebooks 01-07), you evaluate when to use a managed platform that handles orchestration, tool integration, memory, and scaling for you. You deploy the same agent concept to multiple platforms and compare the developer experience, capabilities, pricing, and vendor lock-in tradeoffs. This is the "build vs. buy" decision every agent builder faces.

### Learning Objectives
By the end of this notebook, you will be able to:
- Describe the architecture and key features of Amazon Bedrock AgentCore, Azure AI Foundry, and Vertex AI Agent Builder
- Deploy a simple tool-calling agent on at least one managed platform using its SDK
- Map your self-built agent stack (LLM calls, tool dispatch, memory, API serving) to each platform's managed equivalents
- Evaluate managed platforms against self-hosted solutions on dimensions: cost, flexibility, vendor lock-in, and time-to-production
- Identify which workloads are best suited for managed platforms versus custom infrastructure
- Articulate portability patterns (MCP, LiteLLM, standard schemas) that reduce vendor lock-in

### Prerequisites
- [`../core/06_intro_to_smolagents.ipynb`](../core/06_intro_to_smolagents.ipynb) — familiarity with an agent framework helps you compare it to managed alternatives
- [`03_api_serving.ipynb`](03_api_serving.ipynb) — understanding the self-built stack makes the comparison meaningful

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | The Build vs. Buy Spectrum | Map the full spectrum: raw Python (Core 05) to frameworks (smolagents) to self-hosted APIs (production 03-07) to fully managed platforms. Discuss when each level is appropriate based on team size, compliance, customization, budget, and time-to-market. |
| 2 | Amazon Bedrock AgentCore | Architecture overview: agent definitions, action groups (tools), knowledge bases (RAG), guardrails, session management. Walk through creating an agent with the Bedrock SDK. Discuss AgentCore runtime and AWS-native integrations. |
| 3 | Azure AI Foundry | Architecture overview: AI Foundry hub, agent service, built-in tools (Bing search, code interpreter, Azure AI Search), prompt flow. Walk through deploying an agent. Discuss Azure OpenAI models and enterprise governance features. |
| 4 | Vertex AI Agent Builder | Architecture overview: agent engines, data stores, playbooks, tools, grounding with Google Search. Walk through creating an agent with the Vertex SDK. Discuss Google Cloud integration and multimodal capabilities. |
| 5 | Modal for Agent Workloads | Deploy the FastAPI agent from notebook 03 to Modal with minimal changes. Show how Modal handles scaling, secrets, GPU access, and scheduled functions — ideal for ML-heavy agent workloads and rapid iteration. |
| 6 | Platform Comparison Matrix | Side-by-side table: supported models, tool/function calling ecosystem, memory and state management, MCP support, pricing model, cold start latency, observability, and vendor lock-in risk score. |
| 7 | Portability Patterns | Strategies to reduce lock-in: MCP for portable tool definitions, LiteLLM for model abstraction, standard conversation schemas, infrastructure-as-code. Show how to wrap platform-specific code behind portable interfaces. |
| 8 | Decision Framework | A practical rubric for choosing: startup vs. enterprise, prototype vs. production, single-cloud vs. multi-cloud. Build a decision tree. Provide a migration guide between self-hosted and managed (in both directions). |

### Putting It Together
The capstone defines a standard agent specification (a tool-calling agent with web search and calculator tools) and deploys it to two environments: your self-built FastAPI stack and one managed platform of your choice. You compare the deployment experience (lines of code, time to deploy, configuration complexity), runtime behavior (latency, streaming support, error handling), and operational characteristics (monitoring, cost visibility, scaling). The comparison is documented in a structured decision matrix that serves as a personal reference for future projects.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Platform Feature Matrix | Starter | Build a detailed comparison table of the 3 managed platforms covering: supported models, tool types, memory options, pricing tiers, and SDK languages. Research using official documentation. |
| 2 | Managed Agent Deployment | Moderate | Deploy the calculator + web search agent to one managed platform's free tier. Document every step, noting friction points, pleasant surprises, and deviations from the documentation. |
| 3 | Cost Projection at Scale | Moderate | Estimate the monthly cost of running 1,000 agent sessions/day on your self-built stack (Fly.io) vs. Modal vs. one managed platform. Include compute, LLM API calls, storage, and bandwidth. Present as a comparison chart. |
| 4 | Portable Agent Interface | Stretch | Write an `AgentBackend` abstract class with `run(message)` and `stream(message)` methods. Implement it for both your self-hosted agent and one managed platform. Client code works with either backend by changing a config variable. |

### Key References
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/) — AWS managed agent runtime with action groups, knowledge bases, and guardrails
- [Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/) — Microsoft's platform for building and deploying AI agents with enterprise governance
- [Vertex AI Agent Builder](https://cloud.google.com/products/agent-builder) — Google Cloud's agent development platform with grounding and multimodal support
- [Modal documentation](https://modal.com/docs) — Python-native serverless platform, excellent for ML workloads and rapid deployment
- [LiteLLM documentation](https://docs.litellm.ai/) — unified API for 100+ LLM providers, key portability layer across platforms
- [MCP specification](https://modelcontextprotocol.io/) — Model Context Protocol for portable tool definitions across platforms and frameworks
