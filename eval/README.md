# Evaluation & Debugging — Lesson Plans

> Detailed lesson plans for notebooks 01–07. "It works on my example" is not enough — agents need systematic evaluation, modern benchmarks, and regression pipelines.
> For the full track overview, see [`../roadmap.md`](../roadmap.md).

---

## 01. Tracing and Logging

**File:** `01_tracing_and_logging.ipynb`

### Overview
Before you can evaluate an agent, you need to see what it is doing. This notebook teaches you to instrument agent runs with structured logging and trace visualization so every decision, tool call, and LLM response is recorded and inspectable. You will build a reusable tracing harness that captures the full Thought/Action/Observation loop of a ReAct agent and renders it as a readable trace — the foundation every subsequent eval notebook depends on.

### Learning Objectives
By the end of this notebook, you will be able to:
- Configure Python's `logging` module with structured formatters (JSON lines) for machine-readable agent logs
- Implement a `Tracer` class that records timestamped spans for each agent step (LLM call, tool execution, parsing)
- Capture token usage, latency, and cost metadata on every LLM call
- Visualize a full agent trace as an indented tree (terminal) and as an HTML timeline
- Distinguish between tracing (structural, per-run) and logging (operational, cross-run) and know when to use each
- Integrate Langfuse's Python SDK for hosted trace collection and exploration

### Prerequisites
- [Core 05 — ReAct Agent](../core/05_react_agent.ipynb) — you need a working ReAct agent to instrument

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Why Trace Agents? | Motivating examples: debugging a wrong tool call, finding where latency hides, comparing two runs side-by-side |
| 2 | Python Logging Refresher | Configure `logging` with `StreamHandler` and `FileHandler`, set levels, use `LoggerAdapter` for run-level context |
| 3 | Structured Log Format (JSON Lines) | Build a custom `Formatter` that emits JSON lines with `run_id`, `step`, `event_type`, `timestamp`, and `payload` |
| 4 | Building a Tracer Class | Implement `Tracer` with `start_span()`, `end_span()`, and `record()` — captures nested spans for LLM calls inside tool calls |
| 5 | Instrumenting the ReAct Agent | Wrap the Core 05 ReAct loop with tracing: log each Thought, Action, Observation, and the final answer |
| 6 | Capturing LLM Metadata | Extract and log `prompt_tokens`, `completion_tokens`, `total_tokens`, `latency_ms`, and estimated cost per call |
| 7 | Trace Visualization | Render traces as indented text trees in the terminal and as a simple HTML timeline using string templates |
| 8 | Langfuse Integration | Send traces to Langfuse (open-source, self-hostable) using their Python decorator API; view traces in the Langfuse UI |

### Putting It Together
Instrument the ReAct agent from Core 05 end-to-end: run it on three different queries, collect structured traces, and render a comparison view showing latency per step, token usage, and which tool was called at each stage. Export traces as JSON lines that the test suite notebook (02) can load and assert against.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Add Error Spans | Starter | Extend the `Tracer` to record exception spans when a tool call fails, including the traceback and retry count |
| 2 | Cost Dashboard | Moderate | Aggregate traces from 10 runs and print a summary table: total tokens, total cost, average latency, slowest step |
| 3 | Trace Diff Tool | Moderate | Write a function that takes two trace JSON files and highlights differences — changed tool calls, new steps, latency regressions |
| 4 | Custom Langfuse Scores | Stretch | After each agent run, send a Langfuse `score` (1-5) based on whether the final answer matches an expected value, and view the score distribution in the Langfuse dashboard |

### Key References
- [Python logging docs](https://docs.python.org/3/library/logging.html) — official reference for the logging module, handlers, and formatters
- [Python logging cookbook](https://docs.python.org/3/howto/logging-cookbook.html) — practical recipes for structured logging, context injection, and performance
- [Langfuse docs](https://langfuse.com/docs) — open-source LLM observability: tracing, scoring, prompt management
- [Langfuse Python decorator guide](https://langfuse.com/docs/sdk/python/decorators) — instrument functions with `@observe()` for automatic span creation
- [OpenTelemetry concepts](https://opentelemetry.io/docs/concepts/) — industry-standard tracing vocabulary (spans, traces, context propagation)
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — why observability matters in agent architectures
- [Hamel Husain — Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/) — practical argument for why tracing and eval are non-negotiable

---

## 02. Building Test Suites

**File:** `02_building_test_suites.ipynb`

### Overview
Agents are software, and software needs tests. This notebook teaches you to build a three-tier testing strategy for agents: unit tests for individual tools, integration tests for the agent loop, and golden-answer tests that assert end-to-end correctness. You will use pytest as the test runner and build a reusable test harness that can run inside a notebook or from the command line, giving you a safety net before every agent change.

### Learning Objectives
By the end of this notebook, you will be able to:
- Write pytest-style unit tests for individual tool functions, including edge cases and error conditions
- Build integration tests that mock the LLM and verify the agent loop executes the correct sequence of tool calls
- Create golden-answer test sets with expected outputs and tolerance-based matching (exact, contains, semantic similarity)
- Use pytest fixtures and parametrize to run the same test logic across multiple input/output pairs
- Measure test coverage for tool code and identify untested paths
- Run tests both inside Jupyter (using `ipytest`) and from the command line with `pytest`

### Prerequisites
- [Core 05 — ReAct Agent](../core/05_react_agent.ipynb) — you need agent code and tools to test
- [Eval 01 — Tracing and Logging](01_tracing_and_logging.ipynb) — traces serve as test oracles and debugging aids when tests fail

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Why Test Agents? | The cost of untested agents: silent regressions, prompt changes that break tools, model upgrades that shift behavior |
| 2 | Unit Testing Tools | Write pytest tests for individual tool functions — test the calculator, search, and file-read tools from Core 05 with normal inputs, edge cases, and expected errors |
| 3 | Mocking the LLM | Build a `MockLLM` class that returns predetermined responses, letting you test agent logic without making API calls |
| 4 | Integration Testing the Agent Loop | Test that the agent calls the right tools in the right order given a mocked LLM conversation, and that it terminates correctly |
| 5 | Golden-Answer Tests | Build a test set of (question, expected_answer) pairs and run the agent against them with real LLM calls, using `pytest.mark.slow` to separate fast and slow tests |
| 6 | Matching Strategies | Implement exact match, substring match, regex match, and semantic similarity match (cosine distance on embeddings) for comparing agent output to expected answers |
| 7 | Running Tests in Notebooks | Use `ipytest` to run pytest inside Jupyter cells; configure `conftest.py` for shared fixtures |
| 8 | Test Organization and CI | Organize tests into `tests/` directory, write a `Makefile` target, and preview what a GitHub Actions workflow would look like |

### Putting It Together
Build a complete test suite for the Core 05 ReAct agent: 5 unit tests for tools, 3 integration tests with mocked LLM, and 5 golden-answer tests with real LLM calls. Run the full suite and generate a pass/fail report with timing information. Save the golden-answer results as a JSON baseline that the regression testing notebook (07) will use.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Edge Case Generator | Starter | Write a function that takes a tool's schema and generates edge-case inputs (empty strings, very long strings, negative numbers, missing required fields) |
| 2 | Flaky Test Detector | Moderate | Run each golden-answer test 5 times and flag any test that passes sometimes and fails others — these are flaky tests caused by non-deterministic LLM output |
| 3 | Coverage Report | Moderate | Use `pytest-cov` to measure line coverage of tool code, and identify at least two untested code paths to write new tests for |
| 4 | Snapshot Testing | Stretch | Implement snapshot testing: on first run, save the full agent trace as a snapshot; on subsequent runs, compare the current trace to the snapshot and flag structural differences (new tool calls, changed order) |

### Key References
- [pytest documentation](https://docs.pytest.org/) — official reference for fixtures, parametrize, markers, and plugins
- [Anthropic — Developing Tests](https://docs.anthropic.com/en/docs/build-with-claude/develop-tests) — Anthropic's guide to evaluating Claude-based applications
- [ipytest](https://github.com/chmp/ipytest) — run pytest inside Jupyter notebooks
- [pytest-cov](https://pytest-cov.readthedocs.io/) — coverage reporting plugin for pytest
- [Hamel Husain — Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/) — practical philosophy on testing LLM applications
- [Braintrust — Intro to Evals](https://www.braintrust.dev/docs/guides/evals) — structured eval framework concepts that inform test suite design

---

## 03. Benchmarking Agents

**File:** `03_benchmarking_agents.ipynb`

### Overview
Unit tests tell you if your agent is correct on known inputs. Benchmarks tell you how it performs on standardized, community-validated tasks. This notebook walks you through running your agent against established benchmarks (GAIA for general-purpose tool use, HotPotQA for multi-hop reasoning) and building your own custom benchmark for a specific domain. You will learn to compute benchmark scores, compare across configurations, and interpret results critically.

### Learning Objectives
By the end of this notebook, you will be able to:
- Download and parse the GAIA benchmark dataset and run an agent against its Level 1 tasks
- Implement a HotPotQA evaluation harness that measures exact match (EM) and F1 on multi-hop questions
- Design a custom benchmark with task categories, difficulty levels, and scoring rubrics
- Compute and interpret standard metrics: accuracy, EM, F1, pass@k, and mean reciprocal rank
- Run benchmark sweeps across different configurations (models, temperatures, system prompts) and tabulate results
- Identify and document benchmark limitations — what a score does and does not tell you about agent quality

### Prerequisites
- [Core 05 — ReAct Agent](../core/05_react_agent.ipynb) — the agent you will benchmark
- [Eval 01 — Tracing and Logging](01_tracing_and_logging.ipynb) — traces are essential for debugging benchmark failures
- [Eval 02 — Building Test Suites](02_building_test_suites.ipynb) — matching strategies and test harness patterns carry over to benchmark evaluation

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | What Benchmarks Measure (and Don't) | The purpose of benchmarks, how to interpret scores, common pitfalls (overfitting to benchmarks, contamination, metric gaming) |
| 2 | GAIA Benchmark Setup | Download GAIA Level 1 validation set from HuggingFace, parse the task format (question, expected answer, tools needed, files) |
| 3 | Running an Agent on GAIA | Build a harness that feeds GAIA tasks to your ReAct agent, captures traces, and scores answers against ground truth |
| 4 | HotPotQA Evaluation | Load HotPotQA distractor setting, implement EM and F1 scoring, run your agent on 50 questions and analyze results |
| 5 | Building a Custom Benchmark | Design a 20-question benchmark for a domain you care about: define task categories, difficulty tiers, expected answers, and scoring criteria |
| 6 | Benchmark Metrics Deep Dive | Implement accuracy, EM, F1, pass@k, and mean reciprocal rank from scratch; understand when each metric is appropriate |
| 7 | Configuration Sweeps | Run the same benchmark with different models, temperatures, and system prompts; tabulate results in a comparison matrix |
| 8 | Interpreting and Reporting Results | Generate a benchmark report: scores by category, failure analysis, confidence intervals, and recommendations for improvement |

### Putting It Together
Run your agent against 20 GAIA Level 1 tasks and 50 HotPotQA questions. Build a custom 20-question benchmark for a domain of your choice. For each benchmark, produce a results table, identify the three most common failure modes, and write a one-paragraph analysis of what the scores mean for your agent's readiness.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Failure Categorization | Starter | For every question your agent gets wrong on GAIA, categorize the failure: wrong tool, right tool wrong input, correct reasoning but wrong final answer, or total hallucination |
| 2 | Difficulty Calibration | Moderate | Add difficulty tags (easy/medium/hard) to your custom benchmark and verify that accuracy decreases with difficulty — if it doesn't, recalibrate the tags |
| 3 | Model Comparison Table | Moderate | Run the same 20 custom benchmark questions on three different models via OpenRouter and produce a comparison table with scores, latency, and cost |
| 4 | Leaderboard Builder | Stretch | Build a simple leaderboard script that reads benchmark results from multiple JSON files and produces a ranked Markdown table with scores, model names, and timestamps |

### Key References
- [GAIA benchmark](https://huggingface.co/gaia-benchmark) — General AI Assistants benchmark: real-world questions requiring tool use, reasoning, and multi-step planning
- [GAIA paper (arXiv)](https://arxiv.org/abs/2311.12983) — the original paper defining GAIA's three difficulty levels and evaluation methodology
- [HotPotQA](https://hotpotqa.github.io/) — multi-hop question answering benchmark requiring reasoning across multiple documents
- [Anthropic — Developing Tests](https://docs.anthropic.com/en/docs/build-with-claude/develop-tests) — guidelines on building evaluation suites for LLM applications
- [Braintrust — Intro to Evals](https://www.braintrust.dev/docs/guides/evals) — framework for thinking about benchmarks as structured evaluation
- [Hugging Face — Open LLM Leaderboard methodology](https://huggingface.co/docs/leaderboards/open_llm_leaderboard/about) — how the biggest public LLM leaderboard works, scoring methods, and known limitations

---

## 04. Failure Modes

**File:** `04_failure_modes.ipynb`

### Overview
Agents fail in predictable ways, and knowing the failure taxonomy saves hours of debugging. This notebook builds a catalog of the most common agent failures — infinite loops, hallucinated tools, wrong tool selection, malformed arguments, context window overflow, and premature termination — and teaches you to detect, reproduce, and fix each one. You will build defensive patterns that prevent failures before they happen and diagnostic tools that help you find them quickly when they do.

### Learning Objectives
By the end of this notebook, you will be able to:
- Identify and name the six most common agent failure modes from traces alone
- Reproduce each failure mode intentionally by crafting adversarial inputs or misconfigured agents
- Implement defensive patterns: loop detection, tool validation, argument schema checking, and graceful degradation
- Build a failure classifier that reads a trace and labels the failure mode automatically
- Design system prompts that reduce specific failure modes (e.g., explicit "do not call tools that are not in your tool list" instructions)
- Create a failure mode test suite that specifically targets each known failure type

### Prerequisites
- [Core 05 — ReAct Agent](../core/05_react_agent.ipynb) — the agent whose failures you will study
- [Eval 01 — Tracing and Logging](01_tracing_and_logging.ipynb) — traces are the raw material for failure diagnosis

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | The Agent Failure Taxonomy | Catalog of six common failure modes with real trace examples: infinite loops, hallucinated tools, wrong tool selection, malformed arguments, context overflow, premature termination |
| 2 | Infinite Loops | Detect the pattern (repeated identical actions), implement a max-iterations guard and a loop-detection heuristic that compares the last N actions |
| 3 | Hallucinated Tools | Agent invents a tool that doesn't exist; implement strict tool name validation and a clear error message that lists available tools |
| 4 | Wrong Tool Selection | Agent picks a real tool but the wrong one; analyze why (ambiguous descriptions, overlapping functionality) and improve tool descriptions and system prompt |
| 5 | Malformed Arguments | Agent generates tool arguments that don't match the schema; implement JSON schema validation on tool inputs and return actionable error messages |
| 6 | Context Window Overflow | Agent conversation grows beyond the model's context window; implement conversation truncation, summarization, and a token budget monitor |
| 7 | Premature Termination | Agent says "DONE" too early without actually completing the task; implement answer-quality checks and a "did you actually answer the question?" self-verification step |
| 8 | Automated Failure Diagnosis | Build a `diagnose_trace()` function that reads a trace JSON file, applies heuristics for each failure mode, and returns a diagnosis with suggested fixes |

### Putting It Together
Run your agent on 15 intentionally adversarial queries designed to trigger each failure mode. Collect traces, run the failure diagnosis tool on each, and verify it correctly identifies the failure. Then apply the defensive patterns and re-run to confirm the fixes work. Produce a before/after comparison showing failure rates.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Loop Breaker | Starter | Implement a `max_iterations` parameter and a "consecutive duplicate action" detector that stops the agent after 3 identical tool calls in a row |
| 2 | Tool Name Fuzzy Matcher | Moderate | When the agent hallucinates a tool name, use string similarity (Levenshtein distance) to suggest the closest valid tool and ask the LLM to retry |
| 3 | Context Budget Monitor | Moderate | Build a token counter that tracks cumulative context size and triggers conversation summarization when usage exceeds 75% of the model's context window |
| 4 | Failure Injection Framework | Stretch | Build a framework that takes a working agent and systematically injects failures (remove a tool, corrupt a tool's response, truncate context) to test resilience |

### Key References
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — agent architecture patterns and common pitfalls
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — failure analysis section covering planning failures and tool use errors
- [Reflexion paper (arXiv)](https://arxiv.org/abs/2303.11366) — agents that learn from failure through verbal self-reflection
- [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) — security-oriented failure modes (tool misuse, goal hijacking) that overlap with reliability failures
- [Simon Willison — Prompt Injection](https://simonwillison.net/series/prompt-injection/) — adversarial input failures that cause agents to misbehave
- [smolagents — Building Good Agents](https://huggingface.co/docs/smolagents/tutorials/building_good_agents) — practical debugging guide from the smolagents documentation

---

## 05. LLM as Judge

**File:** `05_llm_as_judge.ipynb`

### Overview
Many agent outputs — summaries, explanations, multi-step reasoning chains — cannot be evaluated with exact string matching. This notebook teaches you to use a second LLM as an automated judge to score agent outputs against rubrics you design. You will build a reusable evaluation framework, calibrate it against human judgments, measure inter-rater agreement, and learn when LLM-as-judge works well and when it fails. This is one of the most important patterns in modern agent evaluation.

### Learning Objectives
By the end of this notebook, you will be able to:
- Design a scoring rubric with clear criteria, levels (1-5), and anchor examples for each level
- Implement a judge prompt that evaluates an agent's output against a rubric and returns a structured score with reasoning
- Run pairwise comparisons (output A vs output B) and pointwise scoring (rate this output 1-5) and understand the tradeoffs
- Measure inter-rater agreement between the LLM judge and human labels using Cohen's kappa and Pearson correlation
- Detect and mitigate common judge biases: verbosity bias, position bias, self-preference bias
- Build a reusable `LLMJudge` class that can evaluate any agent output against any rubric

### Prerequisites
- [Core 05 — ReAct Agent](../core/05_react_agent.ipynb) — you need agent outputs to evaluate
- [Eval 02 — Building Test Suites](02_building_test_suites.ipynb) — golden-answer test sets provide the evaluation data

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | When Exact Match Fails | Examples where agent output is correct but doesn't match the expected string: paraphrases, different formats, partial answers, multi-step reasoning |
| 2 | Rubric Design | Design rubrics for three evaluation dimensions: correctness, completeness, and reasoning quality. Each dimension has 5 levels with anchor examples |
| 3 | The Judge Prompt | Build a judge system prompt that takes (question, expected_answer, agent_output, rubric) and returns a JSON score with per-dimension ratings and reasoning |
| 4 | Pointwise vs Pairwise Evaluation | Implement both modes: pointwise (rate this output 1-5) and pairwise (which output is better, A or B?); compare when each is more reliable |
| 5 | Building the LLMJudge Class | Implement a reusable `LLMJudge` class with `score()` and `compare()` methods, configurable rubrics, and structured JSON output parsing |
| 6 | Calibration Against Humans | Label 20 agent outputs by hand (human scores), run the LLM judge on the same outputs, compute Cohen's kappa and Pearson correlation, and analyze disagreements |
| 7 | Judge Biases and Mitigation | Demonstrate verbosity bias (judges prefer longer outputs), position bias (in pairwise, judges prefer the first option), and self-preference bias; implement mitigations (randomized order, explicit "length is not quality" instructions) |
| 8 | Multi-Judge Consensus | Run multiple judges (different models or different prompts) on the same outputs, aggregate scores, and measure when consensus improves reliability |

### Putting It Together
Evaluate 20 agent outputs from your golden-answer test set using the `LLMJudge` with a correctness rubric. Calibrate against your own human labels. Produce a calibration report showing agreement rate, kappa score, and the three outputs where human and judge disagree most — with analysis of why.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Custom Rubric | Starter | Design a rubric for a domain you care about (e.g., code quality, helpfulness, safety) with 5 levels and anchor examples, and run the judge on 10 agent outputs |
| 2 | Position Bias Test | Moderate | Run 20 pairwise comparisons in both orders (A vs B, then B vs A) and compute the position bias rate — how often does the judge flip its preference? |
| 3 | Judge Ensemble | Moderate | Run three different judge prompts (strict, moderate, lenient) on the same 20 outputs and implement majority-vote aggregation; compare ensemble accuracy to individual judges |
| 4 | Self-Improving Judge | Stretch | When the judge and human disagree, show the judge the human's reasoning and ask it to update its rubric interpretation; measure whether re-scoring after calibration improves agreement |

### Key References
- [Judging LLM-as-a-Judge (MT-Bench paper)](https://arxiv.org/abs/2306.05685) — foundational paper on using LLMs as evaluators, introducing MT-Bench and systematic bias analysis
- [Anthropic — Developing Tests](https://docs.anthropic.com/en/docs/build-with-claude/develop-tests) — Anthropic's guide including LLM-graded evaluation strategies
- [Braintrust — LLM as Judge](https://www.braintrust.dev/docs/guides/evals#model-graded-evals) — practical guide to implementing model-graded evaluations
- [AlpacaEval](https://github.com/tatsu-lab/alpaca_eval) — automated LLM evaluation framework using LLM judges with length-controlled win rates
- [CritiqueLLM (arXiv)](https://arxiv.org/abs/2311.18702) — scaling human feedback data using LLM critics, with analysis of judge reliability
- [Hamel Husain — Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/) — practical perspective on when LLM-as-judge works and when you need human evaluation

---

## 06. Modern Benchmarks

**File:** `06_modern_benchmarks.ipynb`

### Overview
The agent benchmark landscape evolved rapidly in 2024-2025. Beyond GAIA and HotPotQA, benchmarks like SWE-bench (real GitHub issues), HumanEval (code generation), and domain-specific evals now define the standard for agent capability measurement. This notebook teaches you to run your agents against these modern benchmarks, understand what each measures, build custom domain evals that complement public benchmarks, and critically evaluate what scores mean. You will go from "my agent scores 40% on GAIA" to understanding exactly where it succeeds and fails.

### Learning Objectives
By the end of this notebook, you will be able to:
- Set up and run SWE-bench Lite evaluations for code-editing agents using the official harness
- Run HumanEval code-generation tasks and compute pass@1 and pass@10 scores
- Execute GAIA Level 1-3 tasks and analyze score breakdowns by difficulty and tool category
- Build a custom domain eval with task templates, scoring functions, and category-level reporting
- Compute confidence intervals and statistical significance for benchmark comparisons
- Critically evaluate benchmark scores: what they measure, what they miss, and when to build your own

### Prerequisites
- [Eval 03 — Benchmarking Agents](03_benchmarking_agents.ipynb) — core benchmarking concepts, GAIA setup, and metric computation carry forward

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | The Modern Benchmark Landscape | Survey of major agent benchmarks (2024-2025): what each measures, task format, scoring method, and known limitations |
| 2 | SWE-bench Lite | Set up SWE-bench Lite (300 real GitHub issues), understand the task format (issue description, codebase snapshot, expected patch), and run your agent on 10 tasks |
| 3 | HumanEval for Code Generation | Load HumanEval tasks, run your agent as a code generator, compute pass@1 and pass@10, and analyze failure categories (syntax errors, logic errors, edge cases) |
| 4 | GAIA Level 2-3 | Graduate from Level 1 to harder GAIA tasks that require multi-step reasoning, complex tool orchestration, and handling ambiguity |
| 5 | Custom Domain Evals | Design a 30-question eval for a specific domain: define task templates, scoring functions, difficulty tiers, and category tags; run and analyze results |
| 6 | Statistical Rigor | Compute 95% confidence intervals for benchmark scores, run significance tests (bootstrap) when comparing two agent configurations, and understand sample size requirements |
| 7 | Benchmark Contamination and Gaming | How LLMs can memorize benchmark answers, why you need held-out test sets, and how to detect contamination in your evaluations |
| 8 | Building a Personal Eval Dashboard | Aggregate results from all benchmarks into a single summary dashboard: scores, trends over time, and per-category breakdowns |

### Putting It Together
Run your agent against SWE-bench Lite (10 tasks), HumanEval (20 tasks), GAIA Level 2 (10 tasks), and your custom domain eval (30 tasks). Produce a unified dashboard showing scores by benchmark and category, with confidence intervals. Write a one-page analysis identifying your agent's strongest and weakest capability areas.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Benchmark Quick-Start | Starter | Pick one benchmark you haven't run yet (SWE-bench or HumanEval), set it up, run 5 tasks, and report scores |
| 2 | Category Drill-Down | Moderate | For your worst-performing benchmark category, analyze all failures, identify the common root cause, and propose a specific fix (better tool, better prompt, different model) |
| 3 | Statistical Comparison | Moderate | Run the same 20-task eval with two different models, compute scores and 95% confidence intervals, and determine whether the difference is statistically significant |
| 4 | Contamination Probe | Stretch | Take 10 benchmark questions and rephrase them (same logic, different wording); compare scores on original vs rephrased to estimate how much the model benefits from memorization |

### Key References
- [SWE-bench](https://www.swebench.com/) — benchmark using real GitHub issues to evaluate code-editing agents
- [SWE-bench paper (arXiv)](https://arxiv.org/abs/2310.06770) — the original paper defining SWE-bench's methodology and evaluation harness
- [HumanEval](https://github.com/openai/human-eval) — OpenAI's code generation benchmark with function-level completion tasks
- [GAIA benchmark](https://huggingface.co/gaia-benchmark) — general-purpose assistant benchmark requiring tool use, reasoning, and web browsing
- [BigCodeBench](https://github.com/bigcode-project/bigcodebench) — code generation benchmark with complex, multi-function tasks
- [Anthropic — Developing Tests](https://docs.anthropic.com/en/docs/build-with-claude/develop-tests) — guidance on building evaluations that complement public benchmarks
- [Chatbot Arena (LMSYS)](https://chat.lmsys.org/) — crowdsourced LLM ranking via pairwise comparisons, complementing automated benchmarks

---

## 07. Regression Testing

**File:** `07_regression_testing.ipynb`

### Overview
Every change to an agent — new tool, updated prompt, model upgrade, dependency bump — can silently break something that used to work. This notebook teaches you to build a regression testing pipeline: a golden test set that captures known-good behavior, automated checks that run on every change, version-to-version comparison, and CI integration so regressions are caught before they reach users. This is the capstone of the eval track, pulling together tracing, test suites, benchmarks, failure analysis, and LLM-as-judge into a single automated pipeline.

### Learning Objectives
By the end of this notebook, you will be able to:
- Build and maintain a golden test set: curated inputs with expected outputs, difficulty tags, and category labels
- Implement an automated regression runner that executes the golden set, scores results, and compares to a baseline
- Detect regressions at multiple levels: exact output changes, score drops, new failure modes, latency increases, and cost increases
- Build a version comparison report showing pass/fail diffs, score changes, and newly broken tests
- Set up a GitHub Actions workflow that runs the regression suite on every pull request
- Design an alerting policy: which regressions block a merge, which are warnings, and which are acceptable

### Prerequisites
- [Eval 01 — Tracing and Logging](01_tracing_and_logging.ipynb) — traces are stored with each regression run for debugging
- [Eval 02 — Building Test Suites](02_building_test_suites.ipynb) — golden-answer test sets and matching strategies are the foundation
- [Eval 03 — Benchmarking Agents](03_benchmarking_agents.ipynb) — benchmark scores are tracked across versions
- [Eval 04 — Failure Modes](04_failure_modes.ipynb) — failure diagnosis is run on new regressions to classify the break
- [Eval 05 — LLM as Judge](05_llm_as_judge.ipynb) — the LLM judge scores open-ended outputs in the regression suite
- [Eval 06 — Modern Benchmarks](06_modern_benchmarks.ipynb) — benchmark results from multiple sources feed into the regression dashboard

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Why Regression Testing for Agents? | Real-world examples: a prompt tweak that fixed one task but broke three others, a model upgrade that changed tool-calling format, a dependency update that changed embedding dimensions |
| 2 | Designing the Golden Test Set | Curate 30 test cases: select inputs that cover each tool, each failure mode, easy/medium/hard difficulty, and edge cases; define expected outputs and matching strategies |
| 3 | The Regression Runner | Build a `RegressionRunner` class that executes the golden set, scores each test (exact, contains, LLM-judge), records traces, and saves results as versioned JSON |
| 4 | Baseline Management | Implement baseline storage: save the first passing run as the baseline, compare subsequent runs against it, update the baseline when intentional changes are made |
| 5 | Version Comparison Reports | Build a diff report showing: tests that newly fail, tests that newly pass, score changes per test, aggregate score changes, latency and cost deltas |
| 6 | Alerting and Severity Levels | Define severity levels: P0 (blocks merge — golden test failure), P1 (warning — score drop > 10%), P2 (info — latency increase, cost increase) |
| 7 | GitHub Actions Integration | Write a GitHub Actions workflow that runs the regression suite on every PR, posts a summary comment, and blocks merge on P0 regressions |
| 8 | Regression Dashboard | Build a lightweight dashboard (Markdown report + JSON data) that tracks scores, pass rates, and failure modes across the last 10 versions |

### Putting It Together
Build the complete regression pipeline: a 30-test golden set, a `RegressionRunner` that scores and traces, a baseline, and a version comparison. Run the pipeline twice (simulating a "before" and "after" change), generate the diff report, and verify it correctly identifies the intentional regression. Write the GitHub Actions workflow file and verify it runs locally with `act` or by inspecting the YAML.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Golden Set Curation | Starter | Review your existing test cases from Eval 02-03 and select the 30 most important for the golden set, ensuring coverage across tools, difficulty levels, and failure modes |
| 2 | Automated Baseline Update | Moderate | Add a `--update-baseline` flag to the regression runner that saves the current results as the new baseline, with a confirmation prompt and a git-friendly diff of what changed |
| 3 | Flaky Test Quarantine | Moderate | Identify tests with non-deterministic results (pass rate < 100% over 5 runs), move them to a "quarantine" set that runs separately and doesn't block merges, and track their stability over time |
| 4 | Full CI Pipeline | Stretch | Set up a complete GitHub Actions workflow: install dependencies, load API keys from secrets, run the regression suite, post a PR comment with the diff report, and block merge on P0 failures |

### Key References
- [Braintrust](https://www.braintrust.dev/) — evaluation and regression testing platform for LLM applications, with versioned datasets and scoring
- [GitHub Actions documentation](https://docs.github.com/en/actions) — CI/CD platform for automating test runs on PRs and pushes
- [Anthropic — Developing Tests](https://docs.anthropic.com/en/docs/build-with-claude/develop-tests) — includes guidance on maintaining evaluation suites over time
- [pytest-regressions](https://pytest-regressions.readthedocs.io/) — pytest plugin for regression testing with automatic baseline management
- [Hamel Husain — Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/) — the case for continuous evaluation and regression detection in LLM products
- [Langfuse — Datasets and Experiments](https://langfuse.com/docs/datasets/overview) — managing versioned evaluation datasets and tracking experiment results over time
- [OpenAI — Evals framework](https://github.com/openai/evals) — OpenAI's open-source evaluation framework, useful for understanding eval infrastructure patterns
