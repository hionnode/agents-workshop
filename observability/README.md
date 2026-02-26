# Observability & Cost Optimization — Lesson Plans

> Detailed lesson plans for notebooks 01–04. Without observability, you can't debug, improve, or manage costs for production agents.
> For the full track overview, see [`../roadmap.md`](../roadmap.md).

---

## 01. Tracing with Langfuse

**File:** `01_tracing_with_langfuse.ipynb`

### Overview

This notebook introduces structured observability for LLM agents using Langfuse, a popular open-source tracing platform. You will instrument an existing ReAct agent with traces, spans, and generation events — giving you a full timeline view of every LLM call, tool invocation, and reasoning step. Tracing is the single most important observability primitive: without it, debugging a multi-step agent is like debugging a program without stack traces.

### Learning Objectives

By the end of this notebook, you will be able to:
- Set up Langfuse (self-hosted or cloud) and connect it to a Python agent via the Langfuse SDK
- Instrument an agent loop with traces, spans, and generation events using the `@observe` decorator and manual context managers
- Record token usage, latency, and model metadata on each generation span
- Attach user-defined scores (correctness, helpfulness, tool success) to traces for later analysis
- Navigate the Langfuse dashboard to inspect a single agent run end-to-end — identifying where time and tokens are spent
- Compare trace structures across different agent architectures (simple loop vs. ReAct vs. multi-agent)

### Prerequisites

- [Core 05 — ReAct Agent](../core/05_react_agent.ipynb) — you will instrument the ReAct agent built in this notebook
- [Core 06 — Intro to smolagents](../core/06_intro_to_smolagents.ipynb) — optional but useful; Langfuse has a smolagents integration you can explore in the exercises

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Why Tracing Matters | Motivating example: a 7-step agent run that fails silently. Without tracing you see only the final error. With tracing you see exactly which step went wrong and why. |
| 2 | Langfuse Setup | Install `langfuse`, create a project, configure API keys via `.env`. Verify the connection with a smoke-test trace. |
| 3 | Core Concepts — Traces, Spans, Generations | Understand the data model: a trace is one agent invocation, spans are nested sub-operations, generations are LLM calls with prompt/completion/token counts. |
| 4 | Instrumenting the Agent Loop | Add `@observe` decorators and manual `langfuse.trace()` / `langfuse.span()` calls to the ReAct agent from Core 05. See traces appear in the dashboard. |
| 5 | Recording Token Usage and Costs | Extract token counts from the OpenRouter response and attach them to generation spans. Configure model-level cost tables so Langfuse computes dollar costs automatically. |
| 6 | Scoring Traces | Attach scores to completed traces — both programmatic scores (did the agent reach the right answer?) and manual annotation scores from the dashboard UI. |
| 7 | Navigating the Dashboard | Guided walkthrough: filter traces by user, model, score, latency. Drill into a trace to see the span waterfall. Identify the slowest and most expensive steps. |
| 8 | Tracing smolagents (Optional) | Use the `LangfuseInstrumentor` or callback handler to automatically trace smolagents runs — zero-code instrumentation. Compare auto-generated traces with your hand-instrumented ones. |

### Putting It Together

Take the ReAct agent from Core 05, add full Langfuse instrumentation, run it against 5 different queries, and use the Langfuse dashboard to answer: (1) which query was the most expensive, (2) which tool was called most often, and (3) which run had the highest latency. Write a short summary of your findings as a markdown cell at the end of the notebook.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Trace a Simple Chat | Starter | Instrument a basic chat completion (no agent loop) with a single trace and generation. Verify it appears in Langfuse. |
| 2 | Add Error Tracking | Moderate | Modify the agent loop so that tool execution errors are recorded as span events with `level="ERROR"`. Filter for error traces in the dashboard. |
| 3 | Session Grouping | Moderate | Add `session_id` to traces so that multi-turn conversations are grouped. Run a 3-turn conversation and inspect the session view. |
| 4 | Custom Evaluation Pipeline | Stretch | Write a Python function that fetches traces from the Langfuse API, runs an LLM-as-judge evaluation on each, and posts scores back. Automate the feedback loop. |

### Key References

- [Langfuse Documentation](https://langfuse.com/docs) — official docs covering setup, SDK reference, and integrations
- [Langfuse GitHub](https://github.com/langfuse/langfuse) — open-source repo; self-hosting instructions in the README
- [Langfuse Python SDK](https://langfuse.com/docs/sdk/python) — decorator-based and low-level API for Python instrumentation
- [Langfuse Tracing Concepts](https://langfuse.com/docs/tracing) — detailed explanation of traces, spans, generations, and scores
- [Langfuse smolagents Integration](https://langfuse.com/docs/integrations/smolagents) — zero-code tracing for smolagents
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — context on agent architectures you will trace
- [Hamel Husain — Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/) — why tracing and evaluation are essential, not optional

---

## 02. OpenTelemetry for Agents

**File:** `02_opentelemetry_for_agents.ipynb`

### Overview

This notebook covers vendor-neutral agent tracing using OpenTelemetry (OTel) and the OpenInference semantic conventions. While Langfuse is an excellent all-in-one tool, production systems increasingly need vendor-neutral telemetry that can route to any backend — Jaeger, Grafana Tempo, Arize Phoenix, Datadog, or Langfuse itself (which accepts OTel). You will instrument an agent with standard OTel spans and learn how OpenInference extends OTel with LLM-specific semantics (prompt templates, token counts, tool calls).

### Learning Objectives

By the end of this notebook, you will be able to:
- Explain the OpenTelemetry data model (traces, spans, attributes, resources) and why vendor-neutral telemetry matters
- Set up the OTel Python SDK with an exporter (console, OTLP to Jaeger/Phoenix, or Langfuse's OTel endpoint)
- Instrument an agent using OpenInference semantic conventions — recording LLM calls, tool invocations, retrieval steps, and embeddings with standardized attribute names
- Use Arize Phoenix as a local trace viewer for development and debugging
- Compare the tracing ergonomics of Langfuse-native vs. OTel-based instrumentation and identify when each approach is appropriate
- Configure context propagation so traces flow correctly across async operations and multi-agent handoffs

### Prerequisites

- [Observability 01 — Tracing with Langfuse](01_tracing_with_langfuse.ipynb) — provides foundational tracing concepts; this notebook builds on that understanding with a vendor-neutral alternative

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | The Case for Vendor-Neutral Telemetry | Why OTel is becoming the standard: avoid lock-in, route data to multiple backends, use the same instrumentation in dev (Phoenix) and prod (Datadog). |
| 2 | OTel Fundamentals | Install `opentelemetry-api`, `opentelemetry-sdk`, and an exporter. Create a `TracerProvider`, configure a `SpanProcessor`, and emit your first span. |
| 3 | OpenInference Semantic Conventions | Learn the LLM-specific attribute names defined by OpenInference: `llm.input_messages`, `llm.output_messages`, `llm.token_count.*`, `tool.name`, `tool.parameters`, `retrieval.documents`. |
| 4 | Instrumenting an Agent with OTel | Wrap the ReAct agent from Core 05 in OTel spans using OpenInference conventions. Each LLM call becomes a span of kind `LLM`, each tool call a span of kind `TOOL`. |
| 5 | Local Trace Viewing with Arize Phoenix | Install and launch `arize-phoenix`. Export OTel traces to Phoenix and explore the trace waterfall, LLM call details, and token usage breakdowns in the browser UI. |
| 6 | Exporting to Multiple Backends | Configure a `BatchSpanProcessor` with an OTLP exporter pointing to a remote backend (Jaeger, Grafana Tempo, or Langfuse's OTel endpoint). Show the same trace appearing in two different UIs. |
| 7 | Context Propagation in Async Agents | Ensure trace context flows correctly through `asyncio.gather()` calls and across agent-to-agent boundaries. Use `context.attach()` and `context.detach()` to manage propagation manually when needed. |
| 8 | OTel vs. Langfuse-Native: When to Use Which | Side-by-side comparison. Langfuse-native is simpler for small projects. OTel is the right choice when you need multi-backend export, when your org already uses OTel for other services, or when you want to avoid SDK lock-in. |

### Putting It Together

Instrument the same ReAct agent with both Langfuse-native tracing (from notebook 01) and OTel/OpenInference tracing. Export the OTel traces to Arize Phoenix. Run the agent on 3 queries and compare the trace views side-by-side. Summarize the tradeoffs: what information is easier to find in each tool, what was harder to set up, and which you would choose for a new project.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Console Exporter | Starter | Configure the OTel `ConsoleSpanExporter` and run an agent. Read the raw JSON spans printed to stdout. Identify the parent-child relationships manually. |
| 2 | Custom Span Attributes | Moderate | Add custom attributes to your agent spans: `agent.iteration_count`, `agent.final_answer_length`, `agent.tools_called` (comma-separated list). Query these in Phoenix. |
| 3 | Auto-Instrumentation | Moderate | Use `openinference-instrumentation-openai` or `openinference-instrumentation-httpx` to automatically trace LLM calls without modifying agent code. Compare with manual instrumentation. |
| 4 | Multi-Agent Trace Propagation | Stretch | Build a 2-agent system where Agent A delegates sub-tasks to Agent B. Ensure the OTel trace correctly shows Agent B's spans nested under Agent A's delegation span, even across async boundaries. |

### Key References

- [OpenTelemetry Documentation](https://opentelemetry.io/docs/) — official docs for the OTel standard, SDKs, and collector
- [OpenTelemetry Python SDK](https://opentelemetry.io/docs/languages/python/) — Python-specific setup, instrumentation, and configuration
- [OpenInference Specification](https://github.com/Arize-ai/openinference) — semantic conventions for LLM observability built on OTel
- [Arize Phoenix](https://phoenix.arize.com/) — open-source LLM trace viewer that natively supports OpenInference
- [Langfuse OTel Integration](https://langfuse.com/docs/integrations/opentelemetry) — send OTel traces to Langfuse as a backend
- [OpenLLMetry by Traceloop](https://github.com/traceloop/openllmetry) — another OTel-based LLM instrumentation library, good for comparison
- [Jaeger](https://www.jaegertracing.io/) — popular open-source distributed tracing backend compatible with OTel

---

## 03. Cost Optimization

**File:** `03_cost_optimization.ipynb`

### Overview

LLM API costs can spiral out of control when agents make multiple calls per request, retry on failure, and use expensive models by default. This notebook teaches you to track token usage and dollar costs per agent run, then implement three cost reduction strategies: prompt caching, semantic caching, and model routing (cheap model for easy tasks, expensive model for hard ones). You will build a cost-aware agent wrapper that logs every dollar spent and can enforce per-session budgets.

### Learning Objectives

By the end of this notebook, you will be able to:
- Track input tokens, output tokens, and total cost for every LLM call in an agent run, aggregated into a per-run cost report
- Implement prompt caching to avoid re-sending identical system prompts and tool definitions on every call
- Build a semantic cache that stores LLM responses keyed by embedding similarity, skipping the API entirely for near-duplicate queries
- Implement a model router that classifies query difficulty and routes to an appropriate model (e.g., a small model for simple lookups, a large model for complex reasoning)
- Set per-session and per-user cost budgets that halt the agent gracefully when exceeded
- Use Langfuse cost tracking and the OpenRouter usage API to validate your local cost estimates against actual billing

### Prerequisites

- [Core 05 — ReAct Agent](../core/05_react_agent.ipynb) — the agent you will wrap with cost tracking
- [Observability 01 — Tracing with Langfuse](01_tracing_with_langfuse.ipynb) — you will use Langfuse traces to validate cost data and compare pre/post-optimization runs

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | The Cost Problem | Real-world example: an agent that costs $0.02 per run seems cheap until it handles 10,000 sessions/day. Break down where tokens go: system prompt, conversation history, tool definitions, reasoning chains, retries. |
| 2 | Token Counting and Cost Estimation | Build a `CostTracker` class that hooks into every LLM call, extracts token counts from response headers/body, and calculates dollar cost using a model pricing table. Support OpenRouter's pricing metadata. |
| 3 | Per-Run Cost Reports | Aggregate token usage across all LLM calls in a single agent run. Generate a report: total input/output tokens, cost per step, cost per tool call, total run cost. Display as a formatted table. |
| 4 | Prompt Caching | Implement Anthropic-style prompt caching: mark the system prompt and tool definitions as cacheable so the API can reuse KV-cache across calls. Measure the token savings on multi-turn conversations. |
| 5 | Semantic Caching | Build a simple semantic cache: embed each user query, check cosine similarity against cached queries. If similarity exceeds a threshold, return the cached response without calling the LLM. Track cache hit rate and estimated savings. |
| 6 | Model Routing | Build a lightweight classifier (an LLM call to a cheap model, or a keyword heuristic) that routes queries to different models: a small, fast model for factual lookups and a capable model for multi-step reasoning. Measure cost reduction vs. quality degradation. |
| 7 | Budget Enforcement | Add a `BudgetGuard` that tracks cumulative spend per session. When the budget is 80% consumed, warn the user. At 100%, the agent returns a graceful "budget exceeded" message instead of making another LLM call. |
| 8 | Validating Against Actual Billing | Compare your local cost estimates against Langfuse's cost tracking and the OpenRouter usage API. Identify discrepancies (e.g., cached tokens billed differently, retry tokens not counted). Calibrate your pricing table. |

### Putting It Together

Wrap the ReAct agent in a `CostOptimizedAgent` that combines the `CostTracker`, semantic cache, model router, and `BudgetGuard`. Run it on a set of 10 diverse queries — some simple, some complex, some repeated. Generate a cost report showing: total cost, cost savings from caching, cost savings from model routing, and budget remaining. Compare this against a baseline run with no optimizations.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Token Counter | Starter | Build a standalone function that takes an OpenRouter API response and returns `(input_tokens, output_tokens, cost_usd)`. Test it against 3 different models with known pricing. |
| 2 | Cache Hit Rate Analysis | Moderate | Run the semantic cache against a dataset of 50 queries (with ~30% near-duplicates). Plot cache hit rate over time and total cost savings. Experiment with different similarity thresholds (0.90, 0.95, 0.99). |
| 3 | Router Quality Evaluation | Moderate | Build an evaluation harness: run the same 20 queries through both the routed agent (cheap + expensive model) and a baseline (always expensive model). Score answer quality using an LLM-as-judge. Calculate the cost-quality Pareto curve. |
| 4 | Multi-Tenant Budget System | Stretch | Extend the budget system to support multiple users with different budget tiers (free, basic, premium). Persist budget state to SQLite so it survives restarts. Add an admin endpoint that shows spend by user. |

### Key References

- [OpenRouter API Reference — Usage](https://openrouter.ai/docs/api-reference) — response format including token counts and cost metadata
- [Anthropic — Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) — how prompt caching works and how to enable it
- [Anthropic — Token Counting](https://docs.anthropic.com/en/docs/build-with-claude/token-counting) — client-side token counting for cost estimation
- [Langfuse — Cost Tracking](https://langfuse.com/docs/model-usage-and-cost) — automatic cost computation from traced generations
- [OpenRouter Model Pricing](https://openrouter.ai/models) — current pricing for all available models
- [GPTCache](https://github.com/zilliztech/GPTCache) — open-source semantic caching library for LLM calls (reference implementation)
- [Martian — Model Router](https://withmartian.com/) — commercial model routing service; useful for understanding the routing concept
- [Not Diamond](https://www.notdiamond.ai/) — another model routing approach; their blog has good writeups on routing strategies

---

## 04. Production Dashboards

**File:** `04_production_dashboards.ipynb`

### Overview

Individual traces are useful for debugging single runs, but production agents need aggregate monitoring: latency percentiles, error rates, cost trends, tool success rates, and quality scores over time. This notebook teaches you to build monitoring dashboards that answer operational questions — is the agent getting slower? Are costs trending up? Is a particular tool failing more than usual? You will build dashboards using both Langfuse's built-in analytics and a custom Python dashboard using collected metrics.

### Learning Objectives

By the end of this notebook, you will be able to:
- Define and compute the key operational metrics for a production agent: latency (p50, p95, p99), error rate, cost per session, tokens per session, tool call frequency, and tool success rate
- Query the Langfuse API to extract aggregated metrics across hundreds or thousands of traces
- Build a custom Python monitoring dashboard using `matplotlib` (or `plotly`) that visualizes metric trends over time
- Set up alerting rules that detect anomalies: latency spikes, error rate increases, cost overruns, and quality score drops
- Design a runbook for investigating common agent failures using dashboard data as the entry point
- Evaluate managed observability platforms (Braintrust, Arize Phoenix, Langfuse Analytics) and understand when to build custom vs. adopt a platform

### Prerequisites

- [Observability 01 — Tracing with Langfuse](01_tracing_with_langfuse.ipynb) — you need instrumented traces to aggregate into dashboards
- [Observability 02 — OpenTelemetry for Agents](02_opentelemetry_for_agents.ipynb) — understanding OTel data model helps when building metric pipelines
- [Observability 03 — Cost Optimization](03_cost_optimization.ipynb) — cost metrics feed directly into dashboard panels

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | From Traces to Metrics | The mental model shift: traces are for debugging individual runs, metrics are for monitoring the fleet. Define the key metrics every production agent needs: latency percentiles, error rate, cost, throughput, tool success rate, and quality scores. |
| 2 | Generating Synthetic Trace Data | Since you likely don't have thousands of real agent runs yet, generate realistic synthetic trace data: varied latencies, occasional errors, different models, multiple tools. Store in a format compatible with Langfuse's data model. |
| 3 | Querying Langfuse Analytics | Use the Langfuse API (`GET /api/public/metrics`) and Python SDK to fetch aggregated data: trace counts, average latency, cost sums, score distributions. Build helper functions that return DataFrames ready for plotting. |
| 4 | Building the Latency Dashboard | Plot latency percentiles (p50, p95, p99) over time using `matplotlib`. Add a horizontal threshold line. Annotate points where latency exceeds the SLA. Discuss what causes latency spikes in agent systems (long tool calls, model cold starts, retries). |
| 5 | Cost and Token Usage Panels | Build panels showing: daily cost trend, cost per session distribution (histogram), token usage breakdown (input vs. output vs. cached), and cost by model. Identify the most expensive queries and models. |
| 6 | Tool Performance Monitoring | Track per-tool metrics: call frequency, success rate, average latency, and error types. Build a tool health table and a time-series chart. Identify tools that are degrading (success rate dropping or latency increasing). |
| 7 | Alerting and Anomaly Detection | Implement simple alerting rules: (1) latency p95 exceeds threshold for N minutes, (2) error rate exceeds X%, (3) daily cost exceeds budget, (4) quality score drops below baseline. Send alerts as console logs (or optionally email/Slack webhook). |
| 8 | Managed Platforms Comparison | Survey Braintrust, Arize Phoenix, Langfuse Analytics, and Datadog LLM Observability. Compare: what metrics they provide out of the box, pricing, setup complexity, and integration with OTel. Provide a decision matrix for choosing a platform. |

### Putting It Together

Build a complete agent monitoring dashboard with 4 panels: (1) latency percentiles over time, (2) daily cost with budget line, (3) tool success rates as a stacked bar chart, and (4) quality score trend with alerting threshold. Feed it with either real Langfuse trace data or the synthetic data generator from Section 2. Add at least one alerting rule that fires on the synthetic data. Present the dashboard as a set of `matplotlib` figures in the notebook with written interpretations of what each panel shows.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Metric Aggregation Functions | Starter | Write functions to compute p50, p95, and p99 latency from a list of trace durations. Verify against `numpy.percentile`. Handle edge cases (empty list, single trace). |
| 2 | Interactive Dashboard | Moderate | Replace `matplotlib` static plots with `plotly` interactive charts. Add hover tooltips showing individual trace IDs. Add a date range selector to zoom into specific time periods. |
| 3 | Live Monitoring Simulation | Moderate | Write a loop that generates a new synthetic trace every 2 seconds, appends it to the dataset, and re-renders the dashboard. Simulate a latency spike at minute 5 and verify the alert fires. |
| 4 | Full Observability Stack | Stretch | Combine all 4 notebooks: instrument a real agent (01), export traces via OTel (02), add cost tracking (03), and feed everything into the dashboard (04). Run 50 queries and present a production-ready monitoring view of your agent's performance. |

### Key References

- [Langfuse Analytics Documentation](https://langfuse.com/docs/analytics) — built-in analytics features including dashboards and metric queries
- [Langfuse API Reference](https://langfuse.com/docs/api) — REST API for programmatically fetching traces, scores, and metrics
- [Braintrust](https://www.braintrust.dev/) — managed LLM evaluation and monitoring platform with built-in dashboards
- [Arize Phoenix — Tracing](https://docs.arize.com/phoenix/tracing/llm-traces) — open-source trace viewer with built-in metric panels
- [Datadog LLM Observability](https://www.datadoghq.com/product/llm-observability/) — enterprise-grade LLM monitoring (commercial, but good for understanding what production dashboards look like)
- [Google SRE Book — Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/) — foundational reading on the four golden signals (latency, traffic, errors, saturation) — directly applicable to agent monitoring
- [matplotlib Documentation](https://matplotlib.org/stable/contents.html) — reference for building the static dashboard panels
- [plotly Python Documentation](https://plotly.com/python/) — for the interactive dashboard exercise
