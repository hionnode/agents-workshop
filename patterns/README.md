# Agent Architecture Patterns — Lesson Plans

> Detailed lesson plans for notebooks 01–06. These patterns fill the gaps between basic agent loops and production agent systems.
> For the full track overview, see [`../roadmap.md`](../roadmap.md).

---

## 01. State Machines for Agents

**File:** `01_state_machines_for_agents.ipynb`

### Overview

This notebook teaches you to model agent behavior as explicit finite state machines (FSMs) — where nodes represent states or actions the agent can be in, and edges represent transitions driven by LLM outputs, tool results, or external conditions. You will build a multi-state customer service agent whose behavior is fully defined by a state graph, making it predictable, debuggable, and testable. This is the foundational pattern behind LangGraph and most production agent frameworks in 2025-2026.

### Learning Objectives

By the end of this notebook, you will be able to:

- Define agent behavior as a finite state machine with explicit states, transitions, and terminal conditions
- Implement a `State`, `Transition`, and `StateMachine` class hierarchy in Python
- Route LLM outputs to state transitions using structured parsing
- Add guards (conditional transitions) that inspect tool results or conversation history before transitioning
- Trace agent execution as a sequence of state transitions for debugging
- Recognize how LangGraph's `StateGraph` maps to the FSM primitives you built by hand

### Prerequisites

- [`../core/05_react_agent.ipynb`](../core/05_react_agent.ipynb) — the ReAct loop is the starting point; state machines generalize it beyond the Thought/Action/Observation cycle
- [`../appendix/07_classes_and_oop.ipynb`](../appendix/07_classes_and_oop.ipynb) — you will build class hierarchies for states, transitions, and the state machine engine

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Why State Machines? | Limitations of the flat ReAct loop — what happens when your agent needs branching, retries, or multi-phase workflows. Motivating example: a support agent that triages, researches, drafts, and confirms. |
| 2 | FSM Fundamentals | Define the vocabulary: states, transitions, guards, terminal states, initial state. Draw a state diagram on paper before writing code. |
| 3 | Building the Engine | Implement `AgentState` (enum), `Transition` (dataclass with source, target, guard function), and `StateMachine` (runs the loop, tracks current state, stores history). |
| 4 | Wiring in the LLM | Each state gets a prompt template. The LLM's structured output determines which transition fires. Parse the LLM response into a `TransitionEvent`. |
| 5 | Adding Tool States | States that execute tools instead of calling the LLM — e.g., a `SEARCH` state that calls a search tool, then transitions based on whether results were found. |
| 6 | Guards and Conditional Routing | Implement guard functions on transitions: check confidence scores, result counts, retry budgets. Only transition if the guard returns `True`. |
| 7 | Execution Tracing | Log every state transition with timestamp, input, output, and transition taken. Visualize the trace as a table and as a simple ASCII state diagram. |
| 8 | From FSM to LangGraph | Map your hand-built primitives to LangGraph concepts: `StateGraph`, `add_node`, `add_edge`, `add_conditional_edges`. Show the same agent in both representations. |

### Putting It Together

Build a complete customer service agent with 5 states: `TRIAGE` (classify the request), `LOOKUP` (search knowledge base), `DRAFT_RESPONSE` (generate answer), `CONFIRM` (ask user to confirm), and `ESCALATE` (hand off to human). The agent transitions between states based on LLM classification, tool results, and user feedback. Trace the full execution and compare with a flat ReAct implementation of the same task.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Add a Retry State | Starter | Add a `RETRY` state that the agent enters when a tool call fails, with a max-retries guard that transitions to `ESCALATE` after 3 attempts. |
| 2 | Parallel State Exits | Moderate | Implement a state with multiple conditional exits — e.g., `TRIAGE` can go to `LOOKUP`, `ESCALATE`, or `DRAFT_RESPONSE` depending on the classified category. Test all three paths. |
| 3 | Cycle Detection | Moderate | Add a safety check to the state machine engine that detects if the agent is looping between the same two states more than N times and forces a transition to a terminal state. |
| 4 | Statechart Extensions | Stretch | Implement nested states (a "sub-FSM" inside a state) — e.g., the `LOOKUP` state internally runs a 3-step search-read-summarize sub-machine before returning a result. |

### Key References

- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — the "workflows vs agents" distinction and routing patterns
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/) — the dominant graph-based agent framework that formalizes state machines
- [Wikipedia — Finite-State Machine](https://en.wikipedia.org/wiki/Finite-state_machine) — formal definitions and notation
- [Microsoft AI Agent Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) — state-based patterns in enterprise agent design
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — agent architecture survey covering planning and action loops

---

## 02. Event-Driven Agents

**File:** `02_event_driven_agents.ipynb`

### Overview

This notebook shifts agents from request-response (user asks, agent answers) to event-driven (agent reacts to events from the world). You will build an agent that listens for incoming events — webhooks, message queue messages, file-change notifications — and decides how to respond using an LLM-powered event handler. This pattern is essential for agents that monitor systems, respond to alerts, or participate in multi-agent pipelines where work arrives asynchronously.

### Learning Objectives

By the end of this notebook, you will be able to:

- Distinguish request-response, polling, and event-driven agent architectures and articulate when each is appropriate
- Implement an event bus with publish/subscribe semantics in Python using `asyncio.Queue`
- Build event handler functions that triage incoming events and route them to the LLM or direct-action paths
- Chain agents together via events — one agent's output is another agent's input event
- Implement backpressure and dead-letter queues to handle event bursts and processing failures
- Simulate webhook-driven workflows without deploying a real server

### Prerequisites

- [`../core/05_react_agent.ipynb`](../core/05_react_agent.ipynb) — you need to understand the basic agent loop before making it event-driven
- [`../appendix/11_async_and_await.ipynb`](../appendix/11_async_and_await.ipynb) — event-driven agents are inherently async; you need `asyncio`, `await`, and `async for`

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Request-Response vs Event-Driven | Compare the two paradigms with concrete agent examples. When does an agent need to be event-driven? Real-world triggers: GitHub webhooks, Slack messages, cron schedules, database changes. |
| 2 | The Event Model | Define an `Event` dataclass: `type`, `source`, `payload`, `timestamp`, `correlation_id`. Build a type registry that maps event types to handler functions. |
| 3 | Building an Event Bus | Implement `EventBus` using `asyncio.Queue` — `publish(event)`, `subscribe(event_type, handler)`, and a `run()` loop that dispatches events to registered handlers. |
| 4 | LLM-Powered Event Handlers | Write handlers that pass the event payload to an LLM for triage, classification, or response generation. The LLM decides: act immediately, gather more info, or ignore. |
| 5 | Simulating Webhooks | Create a mock webhook receiver that converts incoming HTTP-like payloads into events. Simulate a GitHub PR webhook triggering a code review agent. |
| 6 | Event Chaining | Connect two agents via events: Agent A processes a "new_document" event, extracts entities, and publishes an "entities_extracted" event that Agent B picks up for knowledge graph updates. |
| 7 | Error Handling and Dead Letters | Implement a dead-letter queue for events that fail processing after N retries. Add backpressure: if the queue exceeds a threshold, drop low-priority events or pause publishing. |
| 8 | Scaling Considerations | Discussion of how this in-process pattern maps to production infrastructure: Redis Streams, Apache Kafka, AWS SQS. What changes, what stays the same. |

### Putting It Together

Build a "repository monitor" agent system: a webhook simulator publishes `push`, `pull_request`, and `issue` events. An event router agent classifies each event and dispatches it to specialized handlers — a code review handler (for PRs), a release notes handler (for pushes to main), and a triage handler (for new issues). Each handler uses the LLM to generate its output and publishes a `notification` event consumed by a summary agent.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Add Priority Queues | Starter | Replace the single `asyncio.Queue` with a `PriorityQueue`. Assign priorities to event types (e.g., `security_alert` > `pull_request` > `comment`) and verify high-priority events are processed first. |
| 2 | Event Filtering | Moderate | Implement subscriber-side filters — a handler can subscribe to `pull_request` events but only receive those where `payload["action"] == "opened"`. Add filter predicates to the subscription API. |
| 3 | Correlation Tracking | Moderate | Use `correlation_id` to group related events into a single "conversation." Build a trace view that shows the full chain of events spawned from a single trigger. |
| 4 | Temporal Triggers | Stretch | Add time-based events: implement a scheduler that publishes `cron_tick` events at specified intervals. Build an agent that aggregates all events from the last hour into a digest every 60 minutes. |

### Key References

- [Confluent — Event-Driven Multi-Agent Systems](https://www.confluent.io/blog/event-driven-multi-agent-systems/) — production event-driven agent architectures using Kafka
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — workflow orchestration patterns relevant to event routing
- [Python asyncio documentation](https://docs.python.org/3/library/asyncio.html) — the concurrency foundation for event-driven Python
- [Martin Fowler — Event-Driven Architecture](https://martinfowler.com/articles/201701-event-driven.html) — canonical overview of event-driven patterns
- [Redis Streams documentation](https://redis.io/docs/latest/develop/data-types/streams/) — production message queue that maps to the in-memory pattern you build here

---

## 03. Human in the Loop

**File:** `03_human_in_the_loop.ipynb`

### Overview

This notebook teaches you to build agents that know when to ask for help. You will implement approval gates, confidence-based escalation, and interactive correction workflows where a human can review, modify, or reject an agent's proposed action before it executes. Human-in-the-loop (HITL) is not a limitation — it is a design pattern that makes agents trustworthy enough to deploy in high-stakes environments like finance, healthcare, and customer service.

### Learning Objectives

By the end of this notebook, you will be able to:

- Identify which agent actions require human approval based on risk, reversibility, and confidence
- Implement an approval gate that pauses agent execution, presents a proposed action to the user, and resumes or aborts based on their response
- Build confidence-based routing: the agent self-assesses its certainty and escalates low-confidence decisions to a human
- Design multi-level escalation chains (agent → senior agent → human reviewer → human approver)
- Handle human corrections by feeding them back into the agent's context for learning within the session
- Measure and tune the approval threshold to balance autonomy and safety

### Prerequisites

- [`../core/05_react_agent.ipynb`](../core/05_react_agent.ipynb) — you need the ReAct loop as the baseline agent behavior that HITL modifies
- [`../core/15_planning_agent.ipynb`](../core/15_planning_agent.ipynb) — planning agents benefit most from HITL because the human can review the plan before execution starts

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Why Human in the Loop? | Case studies of agent failures that HITL would have prevented: wrong email sent, incorrect database update, hallucinated financial advice. The autonomy-safety tradeoff spectrum. |
| 2 | The Approval Gate Pattern | Implement `ApprovalGate` — a class that intercepts a proposed tool call, presents it to the user (via `input()` in the notebook), and either proceeds or aborts. Wrap the ReAct loop with approval gates on specific tools. |
| 3 | Confidence-Based Escalation | Have the LLM output a confidence score (0-1) alongside its action. If confidence < threshold, pause and ask the human. Implement the scoring prompt and the threshold-based router. |
| 4 | Risk Classification | Classify tools and actions by risk level: `low` (read-only), `medium` (reversible writes), `high` (irreversible actions). Auto-approve low, gate medium, require explicit approval for high. |
| 5 | Interactive Correction | When a human rejects an action, collect their correction ("No, search for X instead"). Inject the correction into the agent's context and let it retry. Build the feedback loop. |
| 6 | Escalation Chains | Implement multi-level escalation: Agent tries → if uncertain, asks a "supervisor" LLM → if still uncertain, asks the human. Each level adds context about why the previous level was uncertain. |
| 7 | Timeout and Default Behavior | What happens if the human does not respond? Implement configurable timeouts with default actions: wait, abort, proceed with safest option. |
| 8 | Metrics and Threshold Tuning | Track approval rates, escalation rates, and correction rates. Use these metrics to tune confidence thresholds — too many escalations means the threshold is too low; too many bad actions means it is too high. |

### Putting It Together

Build a "financial assistant" agent that can look up account balances (low risk, auto-approved), draft emails to clients (medium risk, shown to user for review), and initiate transfers (high risk, requires explicit typed confirmation). The agent uses confidence scoring on its draft emails and escalates uncertain ones. Track all approvals, rejections, and corrections in a session log.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Bulk Approval Mode | Starter | Add a "bulk mode" where the human can approve all pending low-and-medium-risk actions at once instead of one at a time. Display them as a numbered list and accept "approve all" or individual numbers. |
| 2 | Adaptive Thresholds | Moderate | Implement a threshold that adjusts dynamically: if the human approves 10 consecutive actions of a certain type, lower the confidence threshold for that action type. If they reject one, raise it. |
| 3 | Audit Trail | Moderate | Generate a complete audit log: every action proposed, whether it was auto-approved/human-approved/rejected/corrected, timestamps, and the human's correction text. Export as JSON. |
| 4 | Async Approval via Callback | Stretch | Replace synchronous `input()` with a callback-based approval system: the agent publishes proposed actions to a queue and continues processing other tasks while waiting for human review. Integrate with the event bus from notebook 02. |

### Key References

- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — the human-in-the-loop section on orchestration patterns
- [Microsoft AI Agent Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) — enterprise HITL patterns including approval workflows and escalation
- [LangGraph Human-in-the-Loop Guide](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/) — how LangGraph implements breakpoints and approval nodes
- [Anthropic — Developing and Testing Agents](https://docs.anthropic.com/en/docs/build-with-claude/develop-tests) — testing agents that include human checkpoints
- [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) — why human oversight is a security requirement, not just a UX choice

---

## 04. Agentic RAG

**File:** `04_agentic_rag.ipynb`

### Overview

This notebook upgrades RAG from a static pipeline (retrieve, then generate) into an agent-controlled process where the LLM decides when to retrieve, what queries to use, whether the retrieved context is sufficient, and when to reformulate and try again. You will build an agentic RAG system that handles multi-hop questions — questions that require chaining multiple retrievals together, where each retrieval depends on information from the previous one. This is how production RAG systems handle complex, real-world queries.

### Learning Objectives

By the end of this notebook, you will be able to:

- Distinguish naive RAG (single retrieval, single generation) from agentic RAG (agent-controlled retrieval loop)
- Implement a retrieval tool that the agent invokes as needed, rather than always retrieving before generating
- Build query reformulation: the agent analyzes retrieved results and rewrites its query when results are insufficient
- Implement multi-hop retrieval: chain retrievals where each step uses information from the previous step to refine the search
- Add retrieval evaluation: the agent scores retrieved passages for relevance before using them in generation
- Compare agentic RAG output quality against naive RAG on the same questions

### Prerequisites

- [`../core/13_rag_from_scratch.ipynb`](../core/13_rag_from_scratch.ipynb) — you need to understand embeddings, vector similarity, chunking, and basic retrieval-augmented generation
- [`../core/14_rag_with_tools.ipynb`](../core/14_rag_with_tools.ipynb) — using retrieval as a tool inside an agent loop
- [`../core/05_react_agent.ipynb`](../core/05_react_agent.ipynb) — the ReAct loop that drives the agentic RAG controller

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Naive RAG vs Agentic RAG | Side-by-side comparison: naive RAG retrieves once and generates. Agentic RAG decides IF, WHEN, and HOW MANY TIMES to retrieve. Demonstrate a question that naive RAG gets wrong but agentic RAG gets right. |
| 2 | Building the Retrieval Tool | Wrap the vector store from Core 13 as a callable tool: `search(query: str, top_k: int) -> list[dict]`. The agent invokes this tool through the standard tool-call mechanism. |
| 3 | The Decide-Retrieve-Evaluate Loop | Implement the core agentic RAG cycle: the agent receives a question, decides whether it needs retrieval, retrieves if needed, evaluates the results, and either generates an answer or retrieves again with a refined query. |
| 4 | Query Reformulation | When retrieved results are insufficient, the agent rewrites the query. Implement three strategies: (a) make the query more specific, (b) make it more general, (c) decompose it into sub-queries. |
| 5 | Multi-Hop Retrieval | Build a multi-hop pipeline: Question "What award did the director of Inception win in 2024?" requires hop 1 (who directed Inception?) then hop 2 (what award did that person win?). The agent chains these automatically. |
| 6 | Relevance Scoring | The agent scores each retrieved passage (0-1) for relevance to the current question. Filter out low-relevance passages before generation. Implement this as an LLM-based scoring step. |
| 7 | Retrieval Budget and Stop Conditions | Set a max retrieval count (e.g., 5 retrievals per question). Track retrieval attempts and force the agent to generate a best-effort answer (or say "I don't know") when the budget is exhausted. |
| 8 | Evaluation: Naive vs Agentic | Run both naive RAG and agentic RAG on 10 test questions. Compare answer quality, number of retrievals, and latency. Discuss when the extra complexity of agentic RAG is worth it. |

### Putting It Together

Build an agentic RAG system over a set of Wikipedia articles about multiple related topics (e.g., a film franchise — directors, actors, awards, box office). Create 5 multi-hop questions that require chaining 2-3 retrievals. Run the agentic RAG system end-to-end, showing the full trace: initial query, each retrieval with scores, reformulations, and the final synthesized answer with citations to specific passages.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Hybrid Retrieval | Starter | Add a keyword search tool alongside vector search. Let the agent choose between them based on query type (factual lookups use keyword, semantic questions use vector). |
| 2 | Self-Correcting Answers | Moderate | After generating an answer, have the agent verify it against the retrieved passages. If the answer contains claims not supported by any passage, flag them and either remove them or retrieve again. |
| 3 | Source Attribution | Moderate | Require the agent to cite specific passages for each claim in its answer. Output format: each sentence followed by `[Source: chunk_id]`. Verify that all cited sources exist and are relevant. |
| 4 | Adaptive Chunking | Stretch | When retrieved chunks seem to cut off mid-thought, have the agent request the surrounding chunks (chunk N-1 and N+1) for more context. Implement a `get_surrounding_context(chunk_id)` tool. |

### Key References

- [Anthropic — Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) — the technique of adding context to chunks before embedding, directly relevant to improving agentic RAG
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — the foundational agent architecture survey, covers retrieval as a tool
- [LangChain — Agentic RAG](https://python.langchain.com/docs/tutorials/qa_chat_history/) — implementation patterns for agent-controlled retrieval
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — routing and orchestration patterns applicable to retrieval decisions
- [HuggingFace — RAG with smolagents](https://huggingface.co/docs/smolagents/examples/rag) — RAG as a tool inside a smolagents agent
- [Jerry Liu — Agentic RAG (talk)](https://www.youtube.com/watch?v=0dRAiMNJlVQ) — LlamaIndex founder on agentic retrieval patterns

---

## 05. Deep Research Agent

**File:** `05_deep_research_agent.ipynb`

### Overview

This notebook builds a multi-step research agent that goes beyond single-query retrieval. The agent takes a research question, searches for sources, reads and extracts information, identifies knowledge gaps, formulates follow-up queries, iterates until it has comprehensive coverage, and synthesizes everything into a structured report with citations. This is the pattern behind OpenAI's Deep Research, Gemini's Deep Research, and Perplexity's multi-step search — arguably the most commercially impactful agent pattern of 2025.

### Learning Objectives

By the end of this notebook, you will be able to:

- Decompose a research question into an initial set of sub-questions using LLM-driven planning
- Implement a search-read-extract loop: search for sources, read/summarize each source, extract structured facts
- Build gap analysis: the agent compares what it has learned against what it still needs to know, and generates follow-up queries
- Implement iterative deepening: the agent repeats the search-read-gap cycle until a coverage threshold is met or a budget is exhausted
- Synthesize extracted facts into a structured report with inline citations and a bibliography
- Control research depth and breadth with configurable parameters (max iterations, max sources, coverage threshold)

### Prerequisites

- [`../core/13_rag_from_scratch.ipynb`](../core/13_rag_from_scratch.ipynb) — retrieval fundamentals: embeddings, chunking, similarity search
- [`../core/15_planning_agent.ipynb`](../core/15_planning_agent.ipynb) — planning and task decomposition, which the research agent uses to break down its question
- [`../core/05_react_agent.ipynb`](../core/05_react_agent.ipynb) — the ReAct loop that drives the research agent's inner reasoning

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | What Is Deep Research? | Anatomy of a deep research session: initial question, sub-question decomposition, iterative search, gap identification, synthesis. Compare with single-shot RAG and agentic RAG. |
| 2 | Question Decomposition | Given a research question, use the LLM to generate 3-5 sub-questions that, if answered, would comprehensively address the original question. Store them in a `ResearchPlan` dataclass. |
| 3 | The Search Tool | Implement a simulated web search tool that returns titles, snippets, and URLs. (Use a curated set of mock results for reproducibility, with notes on swapping in a real search API.) |
| 4 | The Read-and-Extract Step | For each search result, "read" the source (load the text) and extract structured facts: `Fact(claim: str, source: str, confidence: float)`. The LLM does the extraction. |
| 5 | Gap Analysis | After each search-read cycle, the agent reviews its accumulated facts against the original sub-questions. Which sub-questions are well-covered? Which have gaps? Generate follow-up queries for the gaps. |
| 6 | Iterative Deepening | Implement the outer loop: decompose → search → read → extract → analyze gaps → repeat. Add stopping conditions: max iterations (e.g., 3 rounds), max total sources (e.g., 15), or coverage threshold (all sub-questions answered). |
| 7 | Synthesis and Report Generation | Take all extracted facts and generate a structured report: introduction, findings organized by sub-question, conclusion. Each claim includes an inline citation `[1]` linking to the bibliography. |
| 8 | Research Trace and Provenance | Build a complete trace of the research process: which queries were issued, which sources were read, which facts were extracted from which source, how gaps were identified. This trace makes the research auditable. |
| 9 | Quality Controls | Add fact-checking: cross-reference claims across multiple sources. Flag claims supported by only one source. Detect contradictions between sources and note them in the report. |
| 10 | Tuning the Research Agent | Experiment with parameters: deeper iterations vs broader initial search, strict vs lenient coverage thresholds, aggressive vs conservative gap identification. Show how each parameter affects output quality and cost. |

### Putting It Together

Given the research question "What are the leading approaches to AI agent memory in 2025, and how do they compare?", run the full deep research pipeline. The agent should decompose this into sub-questions (e.g., "What memory architectures exist?", "How does Letta/MemGPT handle memory?", "What role do vector databases play?"), search for sources across multiple rounds, extract and cross-reference facts, and produce a 500-word report with at least 8 cited sources. Display the full research trace alongside the final report.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Configurable Depth | Starter | Add a `depth` parameter (shallow=1 iteration, medium=2, deep=3). Run the same question at all three depths and compare the reports — how much does each additional iteration improve coverage? |
| 2 | Source Credibility Scoring | Moderate | Have the agent assign a credibility score to each source based on domain reputation (e.g., arxiv.org > random blog). Weight facts by source credibility in the synthesis step. |
| 3 | Contradiction Detection | Moderate | When two sources make contradictory claims, flag the contradiction in the report with both sources cited. Have the agent attempt to resolve the contradiction by searching for a third source. |
| 4 | Real Search Integration | Stretch | Replace the mock search tool with a real search API (Tavily, Brave Search, or SerpAPI). Run the agent on a question about a recent event and evaluate whether the research process produces an accurate, well-sourced report. |

### Key References

- [OpenAI — Introducing Deep Research](https://openai.com/index/introducing-deep-research/) — OpenAI's production deep research agent and the UX patterns it established
- [Gemini — Deep Research](https://blog.google/products/gemini/google-gemini-deep-research/) — Google's approach: multi-step research plans with user-visible progress
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — orchestration loops relevant to multi-step research
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — planning, tool use, and memory for autonomous agents
- [Tavily AI Search API](https://tavily.com/) — search API purpose-built for AI agents and research applications
- [Perplexity AI](https://www.perplexity.ai/) — production research agent with multi-step search and citation

---

## 06. Workflow Orchestration

**File:** `06_workflow_orchestration.ipynb`

### Overview

This notebook teaches you to build DAG-based (directed acyclic graph) workflow engines for agents — where tasks can execute in parallel, branch conditionally, recover from errors, and checkpoint their progress. You will build a workflow orchestrator that coordinates multiple tools and LLM calls as nodes in a graph, executing them in the correct order with proper dependency management. This is the pattern behind production workflow systems like LangGraph, Prefect, and Temporal, and it is how complex agent tasks (that go beyond a simple linear loop) are actually structured.

### Learning Objectives

By the end of this notebook, you will be able to:

- Model a multi-step agent task as a directed acyclic graph (DAG) of dependent operations
- Implement a `WorkflowNode` and `Workflow` class that support sequential, parallel, and conditional execution
- Execute independent nodes in parallel using `asyncio.gather` and respect dependency edges
- Implement conditional branching: a node's output determines which downstream node runs next
- Add error recovery: retry failed nodes, skip optional nodes, or execute fallback paths
- Checkpoint workflow state to disk so a failed workflow can resume from the last successful node

### Prerequisites

- [`../core/05_react_agent.ipynb`](../core/05_react_agent.ipynb) — the ReAct loop is a linear workflow; this notebook generalizes it to arbitrary graph structures
- [`../appendix/11_async_and_await.ipynb`](../appendix/11_async_and_await.ipynb) — parallel node execution requires async/await and `asyncio.gather`
- [Notebook 01 in this track](./01_state_machines_for_agents.ipynb) — state machines handle state transitions; workflow orchestration handles task dependencies. Understanding both is essential.

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Beyond Linear Loops | Why the ReAct loop is not enough: tasks with independent sub-tasks (run in parallel), conditional paths (only run if X), and failure modes (retry or skip). Motivating example: a report generation workflow. |
| 2 | DAG Fundamentals | Define the vocabulary: nodes (tasks), edges (dependencies), fan-out (one node triggers many), fan-in (many nodes feed one), conditional edges. Draw a workflow DAG before coding it. |
| 3 | Building the Workflow Engine | Implement `WorkflowNode` (name, callable, dependencies, retry policy) and `Workflow` (add nodes, add edges, topological sort, execute). The engine resolves execution order from the DAG structure. |
| 4 | Parallel Execution | When multiple nodes have their dependencies satisfied simultaneously, execute them in parallel with `asyncio.gather`. Implement a dependency tracker that marks nodes as "ready" when all upstream nodes complete. |
| 5 | Conditional Branching | Add `ConditionalEdge`: an edge with a predicate function that checks the upstream node's output. Only traverse the edge if the predicate returns `True`. This enables if/else and switch/case logic in workflows. |
| 6 | Error Recovery Strategies | Implement three strategies per node: (a) retry with exponential backoff, (b) skip and mark as optional, (c) execute a fallback node. Configure these via a `RetryPolicy` dataclass. |
| 7 | Checkpointing and Resume | After each node completes, serialize the workflow state (completed nodes, their outputs, pending nodes) to a JSON file. Implement `Workflow.resume(checkpoint_path)` that loads state and continues from where it left off. |
| 8 | LLM Nodes and Tool Nodes | Make the workflow engine agent-aware: `LLMNode` sends a prompt to the LLM and parses the response; `ToolNode` calls a tool function. Show how these mix with pure-Python computation nodes in the same workflow. |
| 9 | Workflow Composition | Build a workflow that contains a sub-workflow as a single node. This enables hierarchical decomposition: a "research" workflow node internally runs a 5-node sub-workflow. |
| 10 | Comparison with Production Systems | Map your hand-built primitives to LangGraph (StateGraph), Prefect (flows and tasks), and Temporal (workflows and activities). Discuss what production systems add: distributed execution, observability, scheduling. |

### Putting It Together

Build a "weekly digest" workflow that: (1) fetches data from 3 simulated sources in parallel (news API, GitHub activity, calendar), (2) each source goes through an LLM summarization node, (3) a conditional node checks if any source returned critical alerts — if so, branch to an "urgent alert" path; otherwise continue to (4) a synthesis node that combines all summaries into a digest, and (5) a formatting node that produces the final markdown report. Add checkpointing so the workflow can resume if the synthesis node fails. Display the full DAG structure and execution trace.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Add a Timeout Node | Starter | Implement a node-level timeout: if a node does not complete within N seconds, cancel it and trigger its fallback. Test with a deliberately slow node. |
| 2 | Dynamic Fan-Out | Moderate | Build a node that dynamically creates downstream nodes based on its output. E.g., a "list_files" node returns 5 file paths, and the workflow spawns 5 parallel "process_file" nodes — one per file. |
| 3 | Cycle Detection | Moderate | Add validation to `Workflow.add_edge()` that detects cycles. If adding an edge would create a cycle, raise a `WorkflowCycleError` with a description of the cycle path. |
| 4 | Visual DAG Rendering | Stretch | Use `networkx` and `matplotlib` (or ASCII art) to render the workflow DAG as a visual graph. Color-code nodes by status: pending (gray), running (blue), completed (green), failed (red). Update the visualization as the workflow executes. |

### Key References

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/) — graph-based agent framework with built-in parallel execution, conditional edges, and checkpointing
- [Prefect Documentation](https://docs.prefect.io/) — Python-native workflow orchestration with tasks, flows, retries, and observability
- [Temporal Documentation](https://docs.temporal.io/) — durable workflow execution with automatic retries, timeouts, and state persistence
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — orchestration patterns including parallelization and routing
- [NetworkX — DAG Algorithms](https://networkx.org/documentation/stable/reference/algorithms/dag.html) — topological sort and DAG utilities used in the workflow engine
- [Microsoft AI Agent Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) — enterprise workflow patterns for AI agents