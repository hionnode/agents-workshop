# Appendix Track: Prerequisite Path — Tier E Lesson Plans

> Detailed lesson plans for notebooks 11–14 (Tier E — Advanced Foundations). For the full track overview, see [`../roadmap.md`](../roadmap.md).
> Notebooks 01–10 (Tiers A–C) are already written — see them in this directory.

---

## 11. Async and Await

**File:** `11_async_and_await.ipynb`

### Overview

This notebook teaches Python's `asyncio` concurrency model from the ground up — the event loop, coroutines, `async`/`await` syntax, and patterns for running tasks concurrently. You will build an async HTTP client that fires multiple LLM API calls in parallel and an async generator that streams tokens as they arrive. Async is the backbone of production agent systems: without it, an agent that calls three tools sequentially wastes time waiting for each HTTP response. With `asyncio.gather`, those three calls run concurrently, cutting latency from 3x to ~1x.

### Learning Objectives

By the end of this notebook, you will be able to:

- Explain how the asyncio event loop schedules coroutines without threads
- Write `async def` coroutines and use `await` to yield control to the event loop
- Run multiple coroutines concurrently with `asyncio.gather` and `asyncio.create_task`
- Use `async for` to consume async iterators and async generators
- Make concurrent HTTP requests with `httpx.AsyncClient`
- Identify when async helps (I/O-bound work) vs. when it does not (CPU-bound work)

### Prerequisites

- [01_python_fundamentals.ipynb](01_python_fundamentals.ipynb) — variables, control flow, imports
- [02_functions_and_scope.ipynb](02_functions_and_scope.ipynb) — defining functions, closures, `*args`/`**kwargs`
- [05_error_handling.ipynb](05_error_handling.ipynb) — try/except, exception propagation (async errors behave similarly)
- [06_http_and_apis.ipynb](06_http_and_apis.ipynb) — synchronous httpx calls (we convert these to async)
- [07_classes_and_oop.ipynb](07_classes_and_oop.ipynb) — classes and `__init__` (needed for `httpx.AsyncClient` context managers)

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Why Async Matters for Agents | Compare sequential vs concurrent tool calls with a timing diagram. Measure wall-clock time of 3 serial `httpx.get()` calls vs the async equivalent. |
| 2 | Coroutines and the Event Loop | Write your first `async def` function, call it with `await`, and run it with `asyncio.run()`. Inspect the coroutine object before and after awaiting. Use `asyncio.get_event_loop()` to see the scheduler. |
| 3 | Concurrent Execution with `gather` | Use `asyncio.gather()` to run 5 simulated API calls concurrently. Compare wall-clock time with sequential execution. Handle partial failures using `return_exceptions=True`. |
| 4 | Tasks and `create_task` | Create background tasks with `asyncio.create_task()`, cancel tasks with `task.cancel()`, and check results with `task.result()`. Build a task pool that limits concurrency with `asyncio.Semaphore`. |
| 5 | Async HTTP with `httpx.AsyncClient` | Convert the synchronous `call_api()` helper from Appendix 06 into an `async_call_api()` that uses `async with httpx.AsyncClient()`. Fire 5 concurrent requests to JSONPlaceholder and collect results. |
| 6 | Async Generators and Streaming | Write an `async def` generator using `yield` to simulate a token stream. Consume it with `async for`. Build a `stream_tokens()` function that prints characters as they arrive, mimicking streaming LLM output. |
| 7 | Error Handling in Async Code | Catch exceptions inside coroutines, use `asyncio.gather(return_exceptions=True)` to collect errors without crashing, and implement an async retry wrapper with exponential backoff using `asyncio.sleep()`. |
| 8 | Async Context Managers | Write an `async with` block using `__aenter__`/`__aexit__`. Build a reusable `AsyncAPIClient` class that manages an `httpx.AsyncClient` lifecycle and provides a `.call_llm()` method. |

### Putting It Together

Build an `AsyncToolRunner` that accepts a list of tool-call specifications (each a URL + payload), executes all calls concurrently via `asyncio.gather` with a configurable concurrency limit (`asyncio.Semaphore`), collects results and errors into a structured dict, and reports total wall-clock time. This mirrors how production agents dispatch multiple tool calls from a single LLM response.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Concurrent User Fetcher | Starter | Use `httpx.AsyncClient` and `asyncio.gather` to fetch 10 users from JSONPlaceholder concurrently. Print each user's name and email. |
| 2 | Async Retry Wrapper | Starter | Write an `async_retry(coro_fn, max_retries=3)` function that retries a coroutine on exception, using `asyncio.sleep()` for exponential backoff. Test it with a function that fails twice then succeeds. |
| 3 | Streaming Token Printer | Synthesis | Write an async generator `fake_llm_stream(text, delay=0.05)` that yields one character at a time with `asyncio.sleep(delay)` between each. Write a consumer that prints characters without newlines, simulating a streaming LLM response. |
| 4 | Parallel Agent Tool Dispatch | Stretch | Given a dict mapping tool names to async callables, write an `async dispatch(tool_calls: list[dict])` function that runs up to 3 tools concurrently (using `Semaphore`), handles timeouts with `asyncio.wait_for`, and returns `{"results": [...], "errors": [...]}`. |

### Key References

- [Python asyncio documentation](https://docs.python.org/3/library/asyncio.html) — official reference for the event loop, tasks, and synchronization primitives
- [Real Python — Async IO in Python: A Complete Walkthrough](https://realpython.com/async-io-python/) — thorough tutorial with practical examples
- [httpx — Async Support](https://www.python-httpx.org/async/) — async HTTP client patterns used throughout this notebook
- [Brett Cannon — How the heck does async/await work in Python 3.5?](https://snarky.ca/how-the-heck-does-async-await-work-in-python-3-5/) — deep dive into the mechanics behind `async`/`await`
- [David Beazley — Python Concurrency from the Ground Up (PyCon talk)](https://www.youtube.com/watch?v=MCs5OvhV9S4) — builds an event loop from scratch to explain the concepts
- [Python docs — asyncio.gather](https://docs.python.org/3/library/asyncio-task.html#asyncio.gather) — the workhorse for concurrent coroutine execution
- [Python docs — Asynchronous Generators (PEP 525)](https://peps.python.org/pep-0525/) — the spec behind `async def` + `yield`
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — production agent patterns that rely on async

---

## 12. Databases and SQL

**File:** `12_databases_and_sql.ipynb`

### Overview

This notebook teaches relational databases and SQL using Python's built-in `sqlite3` module, then introduces SQLAlchemy's ORM for structured data access. You will build a conversation history database that stores agent sessions, messages, and tool call logs — the same schema a production agent uses for persistent memory. Agents that remember past conversations, track user preferences, or maintain state across sessions need a database. SQLite is the simplest path: it is a single file, requires no server, ships with Python, and is the storage backend for many agent memory systems (Letta, Mem0, local ChromaDB).

### Learning Objectives

By the end of this notebook, you will be able to:

- Create SQLite databases and tables using `sqlite3.connect()` and `CREATE TABLE` statements
- Write SQL queries for `INSERT`, `SELECT`, `UPDATE`, and `DELETE` with `WHERE` clauses, `ORDER BY`, and `LIMIT`
- Use parameterized queries (`?` placeholders) to prevent SQL injection
- Define relationships between tables using foreign keys and `JOIN` queries
- Map Python classes to database tables using SQLAlchemy's ORM (`DeclarativeBase`, `mapped_column`)
- Implement the repository pattern — a clean interface between agent code and database operations

### Prerequisites

- [01_python_fundamentals.ipynb](01_python_fundamentals.ipynb) — variables, control flow, imports
- [03_data_structures.ipynb](03_data_structures.ipynb) — dicts and lists (rows come back as tuples or dicts)
- [05_error_handling.ipynb](05_error_handling.ipynb) — try/except for database errors, context managers
- [07_classes_and_oop.ipynb](07_classes_and_oop.ipynb) — classes and inheritance (SQLAlchemy models are classes)

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Why Databases Matter for Agents | Compare file-based storage vs SQLite for agent memory. Show the limitations of JSON files (no querying, no concurrent access, no schema enforcement) and why agents need structured persistence. |
| 2 | SQLite Basics: Connect, Create, Insert | Create a database with `sqlite3.connect()`, define a `messages` table with `CREATE TABLE`, insert rows with `INSERT INTO`, and read them back with `cursor.fetchall()`. Use `with` for automatic commit/rollback. |
| 3 | Querying Data: SELECT, WHERE, ORDER BY | Write `SELECT` queries with `WHERE` filters, `ORDER BY` for chronological message history, `LIMIT` for pagination, and `COUNT(*)` for aggregation. Build a `get_recent_messages(session_id, n)` function. |
| 4 | Parameterized Queries and SQL Injection | Demonstrate why string formatting in SQL is dangerous (SQL injection). Rewrite all queries to use `?` placeholders. Show the difference between `f"SELECT ... WHERE id = {user_input}"` (vulnerable) and `cursor.execute("SELECT ... WHERE id = ?", (user_input,))` (safe). |
| 5 | Relationships and JOINs | Add a `sessions` table and a `tool_calls` table with foreign keys linking to `messages`. Write `JOIN` queries to retrieve a session with all its messages and tool calls in one query. |
| 6 | Updates, Deletes, and Migrations | Use `UPDATE` to mark messages as summarized, `DELETE` to prune old sessions, and `ALTER TABLE` to add columns to existing tables. Discuss schema migration strategies for evolving agent systems. |
| 7 | SQLAlchemy ORM: Models and Sessions | Define `Session`, `Message`, and `ToolCall` as SQLAlchemy ORM classes using `DeclarativeBase` and `mapped_column`. Create tables with `Base.metadata.create_all()`. Insert and query using the ORM session. |
| 8 | Repository Pattern for Agents | Build a `ConversationRepository` class that wraps all database operations behind clean methods: `create_session()`, `add_message()`, `get_history()`, `log_tool_call()`. This is the interface an agent imports. |

### Putting It Together

Build a complete `AgentMemoryDB` that combines the repository pattern with SQLAlchemy models to provide persistent conversation storage. Write a simulated agent loop that creates a session, records user messages and assistant responses, logs tool calls with arguments and results, and retrieves the full conversation history — all persisted to a SQLite file that survives kernel restarts.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Message CRUD | Starter | Write functions `insert_message()`, `get_messages_by_session()`, and `delete_old_messages(days=30)` using raw `sqlite3`. Test each with assertions. |
| 2 | Session Statistics | Starter | Write a SQL query that returns, per session: message count, first message timestamp, last message timestamp, and number of distinct tool calls. Use `GROUP BY` and aggregate functions. |
| 3 | ORM Search | Synthesis | Using SQLAlchemy, write a `search_messages(keyword)` method on the repository that performs a `LIKE` query across message content, returning results ranked by recency. Handle the case where no results are found. |
| 4 | Memory Pruning Strategy | Stretch | Implement a `prune_memory(max_messages=100)` method that keeps the most recent `max_messages` per session and deletes the rest, but always preserves messages that have associated tool calls (foreign key constraint). Write tests to verify pruning correctness. |

### Key References

- [Python sqlite3 documentation](https://docs.python.org/3/library/sqlite3.html) — official reference for the built-in SQLite module
- [SQLite documentation](https://www.sqlite.org/docs.html) — complete SQL syntax reference and architecture overview
- [SQLAlchemy 2.0 Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/) — the official tutorial for the modern ORM API
- [SQLAlchemy ORM Quickstart](https://docs.sqlalchemy.org/en/20/orm/quickstart.html) — minimal setup for ORM models
- [Real Python — Data Management With Python, SQLite, and SQLAlchemy](https://realpython.com/python-sqlite-sqlalchemy/) — practical walkthrough of both raw SQL and ORM
- [Bobby Tables (bobby-tables.com)](https://bobby-tables.com/python) — SQL injection prevention guide with Python examples
- [Letta (MemGPT) Architecture](https://www.letta.com/) — production agent memory system built on SQLite
- [SQLite — When to Use SQLite](https://www.sqlite.org/whentouse.html) — official guidance on SQLite vs client-server databases

---

## 13. WebSockets and Streaming

**File:** `13_websockets_and_streaming.ipynb`

### Overview

This notebook teaches real-time communication patterns: the WebSocket protocol for bidirectional messaging, Server-Sent Events (SSE) for server-push streaming, and how both are used in agent systems. You will build a WebSocket echo client, an SSE consumer that processes streaming LLM output token-by-token, and a real-time message handler that routes incoming events to callback functions. Agents that operate in real time — voice assistants, live coding copilots, collaborative tools — depend on persistent connections rather than request-response HTTP. Streaming LLM output (the "typing" effect) uses SSE, while bidirectional protocols like OpenAI's Realtime API use WebSockets.

### Learning Objectives

By the end of this notebook, you will be able to:

- Explain the difference between HTTP request-response, SSE (server-push), and WebSockets (bidirectional)
- Connect to a WebSocket server using the `websockets` library and send/receive messages
- Parse Server-Sent Events from a streaming HTTP response using `httpx` streaming
- Implement callback-based event routing for incoming WebSocket messages
- Handle connection lifecycle events: open, close, reconnect, and error recovery
- Build an async generator that yields parsed tokens from a streaming LLM response

### Prerequisites

- [06_http_and_apis.ipynb](06_http_and_apis.ipynb) — HTTP request-response fundamentals (we build on top of this model)
- [11_async_and_await.ipynb](11_async_and_await.ipynb) — async/await, `async for`, `async with` (WebSockets are inherently async)

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | HTTP vs SSE vs WebSockets | Visual comparison of the three communication models. When to use each: HTTP for tool calls, SSE for streaming LLM output, WebSockets for voice agents and real-time collaboration. Diagram the connection lifecycle of each. |
| 2 | WebSocket Basics with `websockets` | Connect to `wss://echo.websocket.org` (or a local echo server) using `async with websockets.connect()`. Send a message with `ws.send()`, receive with `ws.recv()`. Inspect the handshake and frame format. |
| 3 | Continuous Listening Loop | Write an `async for message in ws:` loop that continuously receives messages until the server closes the connection. Handle `ConnectionClosed` exceptions. Build a message logger that timestamps each incoming frame. |
| 4 | Server-Sent Events (SSE) with httpx | Make a streaming GET request with `httpx.AsyncClient.stream()`. Parse the `data:` lines of the SSE protocol. Build a `parse_sse_stream()` async generator that yields parsed event dicts with `event`, `data`, and `id` fields. |
| 5 | Streaming LLM Output | Simulate an OpenRouter-style streaming response where each SSE event contains a `choices[0].delta.content` token. Build a `stream_chat_completion()` async generator that yields content tokens and handles the `[DONE]` sentinel. |
| 6 | Event Routing and Callbacks | Build an `EventRouter` class that maps event types (strings) to async callback functions using a dict. Register handlers with `router.on("message", handler)`. Dispatch incoming WebSocket messages to the correct handler based on a `type` field in the JSON payload. |
| 7 | Connection Management | Implement automatic reconnection with exponential backoff using a `ReconnectingWebSocket` wrapper. Handle network drops, server restarts, and graceful shutdown. Use `asyncio.wait_for()` to add connection timeouts. |
| 8 | Putting It All Together: Real-Time Agent Bus | Build an `AgentEventBus` that combines WebSocket communication with event routing. The bus connects to a server, receives JSON messages, dispatches them to registered handlers, and sends responses back. This is the pattern used by real-time agent frameworks. |

### Putting It Together

Build a simulated real-time agent communication layer. The `AgentEventBus` connects to a WebSocket server, listens for incoming task messages (`{"type": "task", "content": "..."}`), dispatches them to a handler that simulates LLM processing, streams the response back token-by-token as SSE-formatted messages, and handles disconnection with automatic reconnection. This mirrors the architecture of voice agents and real-time copilots.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Echo Client | Starter | Connect to a WebSocket echo server, send 5 messages in a loop, print each echoed response, and close the connection cleanly using `async with`. |
| 2 | SSE Line Parser | Starter | Write a `parse_sse_line(line: str) -> dict | None` function that parses a single SSE line into `{"field": ..., "value": ...}` for `data:`, `event:`, `id:`, and `retry:` prefixes. Return `None` for comments (lines starting with `:`) and empty lines. |
| 3 | Streaming Token Accumulator | Synthesis | Write an async function that consumes a `stream_chat_completion()` generator, accumulates tokens into a complete response string, prints each token as it arrives (no newline), and returns the full response when the stream ends. Add a `timeout` parameter that raises `TimeoutError` if the stream stalls. |
| 4 | Multi-Channel WebSocket Router | Stretch | Build a `ChannelRouter` that maintains multiple WebSocket connections (one per "channel"), routes outgoing messages to the correct channel, merges incoming messages from all channels into a single `async for` stream using `asyncio.Queue`, and handles individual channel disconnections without bringing down the others. |

### Key References

- [WebSocket Protocol (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) — comprehensive guide to the WebSocket API and protocol
- [websockets library documentation](https://websockets.readthedocs.io/) — the Python WebSocket library used in this notebook
- [Server-Sent Events spec (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) — the SSE protocol specification
- [httpx — Streaming Responses](https://www.python-httpx.org/advanced/streaming/) — how to consume streaming HTTP responses in Python
- [OpenAI — Streaming API](https://platform.openai.com/docs/api-reference/streaming) — the SSE format used by OpenAI (and OpenRouter) for streaming completions
- [RFC 6455 — The WebSocket Protocol](https://datatracker.ietf.org/doc/html/rfc6455) — the official WebSocket specification
- [OpenAI Realtime API](https://platform.openai.com/docs/guides/realtime) — production WebSocket-based voice agent API
- [Anthropic — Streaming Messages](https://docs.anthropic.com/en/api/messages-streaming) — Anthropic's SSE streaming format

---

## 14. Graph Data Structures

**File:** `14_graph_data_structures.ipynb`

### Overview

This notebook teaches graph data structures — nodes, edges, adjacency representations, and traversal algorithms — using both raw Python and the NetworkX library. You will build a knowledge graph that models relationships between concepts (entities and edges extracted from text), traverse it with BFS and DFS, and visualize it with NetworkX's drawing utilities. Graphs are everywhere in modern agent architectures: knowledge graphs store entity relationships for RAG, LangGraph models agent workflows as state machines with nodes and edges, and the A2A protocol uses agent discovery graphs. Understanding graphs unlocks the ability to reason about and build all of these systems.

### Learning Objectives

By the end of this notebook, you will be able to:

- Represent graphs using adjacency lists (dicts of lists) and adjacency matrices (2D arrays)
- Implement breadth-first search (BFS) and depth-first search (DFS) from scratch using queues and stacks
- Distinguish directed vs undirected graphs and weighted vs unweighted edges
- Use NetworkX to create, manipulate, query, and visualize graphs programmatically
- Model a knowledge graph with typed nodes (entities) and typed edges (relationships)
- Traverse a graph to answer multi-hop questions ("What tools does the research agent use?")

### Prerequisites

- [03_data_structures.ipynb](03_data_structures.ipynb) — dicts, lists, sets, and nested structures (graphs are built from these)
- [07_classes_and_oop.ipynb](07_classes_and_oop.ipynb) — classes (the `Graph` and `KnowledgeGraph` classes use `__init__`, methods, and `__repr__`)

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | What Is a Graph? | Define nodes, edges, directed vs undirected, weighted vs unweighted. Draw examples: social networks, file dependencies, agent workflows. Explain why trees, linked lists, and state machines are all graphs. |
| 2 | Adjacency List Representation | Build a `Graph` class backed by a `dict[str, list[str]]`. Implement `add_node()`, `add_edge()`, `neighbors()`, and `__repr__()`. Populate it with a small agent-workflow graph: nodes are agent states, edges are transitions. |
| 3 | Breadth-First Search (BFS) | Implement BFS from scratch using a `collections.deque` as a queue and a `set` for visited tracking. Build `bfs(graph, start)` that returns nodes in BFS order. Use it to find the shortest path between two nodes with `bfs_path(graph, start, end)`. |
| 4 | Depth-First Search (DFS) | Implement DFS using both a stack (iterative) and recursion. Build `dfs(graph, start)` and compare the traversal order with BFS. Use DFS to detect cycles in a directed graph — a common bug in agent workflow definitions. |
| 5 | Weighted Graphs and Shortest Paths | Extend the `Graph` class to support edge weights using `dict[str, list[tuple[str, float]]]`. Implement Dijkstra's algorithm to find the lowest-cost path. Apply it to an agent routing scenario: find the cheapest model pipeline for a given task. |
| 6 | NetworkX: Graph Library Basics | Create graphs with `nx.Graph()` and `nx.DiGraph()`. Add nodes with attributes (`node_type="agent"`), add edges with weights, query with `G.neighbors()`, `G.degree()`, `nx.shortest_path()`. Visualize with `nx.draw()` and `matplotlib`. |
| 7 | Building a Knowledge Graph | Model a knowledge graph with entity nodes (agent, tool, concept) and relationship edges (uses, requires, produces). Build a `KnowledgeGraph` class wrapping NetworkX that supports `add_entity()`, `add_relationship()`, and `query_relationships(entity, rel_type)`. Populate it from a list of `(subject, predicate, object)` triples. |
| 8 | Multi-Hop Graph Queries | Write `find_path(kg, start, end)` and `find_all_related(kg, entity, max_hops=2)` functions that traverse the knowledge graph to answer multi-hop questions. Example: "What data sources does the research agent use?" requires traversing agent -> tools -> data sources (2 hops). |

### Putting It Together

Build a `KnowledgeGraph` populated with triples describing an agent system: agents, their tools, the APIs those tools call, and the data they produce. Write a `query_engine(kg, question_triples)` function that takes a list of `(start_entity, relationship_chain)` queries and returns answers by traversing the graph. Demonstrate with multi-hop queries like "Which agents can access the weather API?" (requires finding agents that use tools that call the weather API).

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Build and Traverse | Starter | Create an adjacency-list graph of 8 cities with edges representing direct flights. Run BFS from your home city and print the order in which cities are discovered. Verify that BFS finds the path with the fewest flights. |
| 2 | Cycle Detector | Starter | Write a `has_cycle(graph)` function using DFS that returns `True` if a directed graph contains a cycle. Test it with an acyclic agent workflow graph (should return `False`) and a graph with a feedback loop (should return `True`). |
| 3 | Agent Workflow Visualizer | Synthesis | Use NetworkX to model a ReAct agent's state machine: nodes = `[Start, Think, Act, Observe, Finish]`, edges = transitions with labels. Color nodes by type (decision vs action), set edge widths by frequency, and render with `nx.draw()`. Export as a PNG. |
| 4 | Knowledge Graph from Text | Stretch | Write a function `extract_triples(text: str) -> list[tuple[str, str, str]]` that takes a paragraph about an agent system and extracts `(subject, predicate, object)` triples using simple regex patterns (e.g., "X uses Y", "X requires Y", "X produces Y"). Feed the triples into your `KnowledgeGraph` and run multi-hop queries on the result. |

### Key References

- [NetworkX documentation](https://networkx.org/documentation/stable/) — the standard Python library for graph creation, manipulation, and analysis
- [NetworkX Tutorial](https://networkx.org/documentation/stable/tutorial.html) — official getting-started guide with examples
- [Wikipedia — Graph theory](https://en.wikipedia.org/wiki/Graph_theory) — foundational concepts: vertices, edges, paths, cycles, connectivity
- [Visualizing Algorithms (Mike Bostock)](https://bost.ocks.org/mike/algorithms/) — stunning interactive visualizations of BFS, DFS, and shortest-path algorithms
- [LangGraph documentation](https://langchain-ai.github.io/langgraph/) — production agent framework that models agents as graph state machines
- [Google A2A Protocol](https://google.github.io/A2A/) — agent-to-agent discovery and communication protocol using agent graphs
- [Real Python — Graphs in Python](https://realpython.com/python-graph-theory/) — practical introduction to graph implementation in Python
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — knowledge graph retrieval in the context of agent memory
