# Prompt Engineering for Agents — Lesson Plans

> Detailed lesson plans for notebooks 01–04. The system prompt IS the agent's programming language — bad prompts = bad agents.
> For the full track overview, see [`../roadmap.md`](../roadmap.md).

---

## 01. System Prompt Design

**File:** `01_system_prompt_design.ipynb`

### Overview

System prompts are the foundational programming layer for every LLM-based agent. This notebook teaches you to design effective system prompts by decomposing them into structural components — role, constraints, output format, and embedded examples — and measuring how each component changes agent behavior. By the end you will have built a reusable system prompt template and tested it against multiple tasks, giving you a framework you will use in every subsequent notebook.

### Learning Objectives

By the end of this notebook, you will be able to:
- Identify the four structural components of a system prompt (role/persona, constraints, output format, embedded examples) and explain what each controls.
- Write a role/persona block that steers an LLM's tone, domain expertise, and behavioral boundaries.
- Add hard constraints (things the model must/must not do) and verify compliance with adversarial test inputs.
- Specify an output format contract (markdown, bullet list, JSON skeleton) and measure format adherence across multiple runs.
- Embed 1-2 in-prompt examples that anchor the model's behavior without relying on few-shot message arrays.
- Compare a naive prompt vs. a structured system prompt on the same task and articulate the performance difference.

### Prerequisites

- [`../core/01_hello_llm.ipynb`](../core/01_hello_llm.ipynb) — You need to be comfortable making chat completion API calls and understand the roles (system, user, assistant).
- [`../core/05_react_agent.ipynb`](../core/05_react_agent.ipynb) — Seeing a ReAct system prompt in action gives you concrete motivation for why system prompt design matters.

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Why System Prompts Matter | Compare the same user query with no system prompt, a one-liner, and a detailed system prompt. Observe how output quality, format, and reliability change. |
| 2 | Anatomy of a System Prompt | Dissect three real-world system prompts (a coding assistant, a customer support bot, and a ReAct agent) into their structural components: role, constraints, format, examples. |
| 3 | Writing Role and Persona Blocks | Build role blocks for different personas (cautious analyst, creative brainstormer, strict validator). Measure how persona affects response style, length, and risk tolerance. |
| 4 | Hard Constraints and Behavioral Boundaries | Add must-do and must-not-do rules. Test them with adversarial inputs designed to break the constraints (e.g., asking the model to ignore instructions). |
| 5 | Output Format Contracts | Define explicit format specifications (markdown headers, numbered lists, JSON skeletons). Run 10 trials per format and measure adherence rate. |
| 6 | Embedded Examples vs. Few-Shot Messages | Compare placing examples inside the system prompt vs. as separate user/assistant message pairs. Discuss when each approach is appropriate and the token-cost tradeoffs. |
| 7 | Building a Reusable Prompt Template | Create a Python function `build_system_prompt(role, constraints, format, examples)` that assembles a structured system prompt from components. Use string templates with clear section delimiters. |
| 8 | System Prompts for Agents | Apply the template to build system prompts for a ReAct agent and a tool-calling agent. Compare agent behavior with a generic vs. tailored system prompt. |

### Putting It Together

Take a ReAct agent from Core 05 and replace its system prompt with one you design using the template from Section 7. The prompt should define the agent's role (research assistant), its constraints (cite sources, never fabricate data), its output format (Thought/Action/Observation), and embed one worked example. Run the agent on three different tasks and evaluate whether the structured prompt improves output quality and format compliance compared to the original.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Constraint Stress Test | Starter | Write a system prompt with 3 hard constraints, then craft 5 adversarial user messages that try to break each one. Record which constraints hold and which fail. |
| 2 | Persona A/B Test | Moderate | Build two system prompts for the same task with different personas (e.g., "concise analyst" vs. "thorough researcher"). Run both on 5 queries and compare output length, detail, and usefulness. |
| 3 | Format Adherence Benchmark | Moderate | Define 3 different output formats (JSON, markdown table, numbered list). Run 20 trials each and compute the format adherence rate. Identify which formats LLMs follow most reliably. |
| 4 | Agent System Prompt from Scratch | Stretch | Design a complete system prompt for a new agent type not covered in the notebook (e.g., a code review agent or a debate moderator). Include all four components and test it on at least 5 diverse inputs. |

### Key References

- [Anthropic — Prompt Engineering Overview](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — Anthropic's official guide covering system prompts, role assignment, and best practices.
- [OpenAI — Prompt Engineering Best Practices](https://platform.openai.com/docs/guides/prompt-engineering) — OpenAI's guide with concrete examples of system prompt structuring.
- [Anthropic — System Prompts](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts) — Deep dive on how Claude processes system prompts and how to use them effectively.
- [Lilian Weng — Prompt Engineering](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/) — Comprehensive survey of prompting techniques with academic references.
- [Brex's Prompt Engineering Guide](https://github.com/brexhq/prompt-engineering) — Practical guide from a production engineering team with real system prompt patterns.
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — How system prompt design affects agent reliability and behavior.

---

## 02. Few-Shot and Chain-of-Thought

**File:** `02_few_shot_and_cot.ipynb`

### Overview

Few-shot prompting and chain-of-thought (CoT) reasoning are the two most impactful techniques for getting LLMs to perform complex, multi-step tasks — which is exactly what agents do every turn. This notebook teaches you to construct effective few-shot examples, elicit step-by-step reasoning with CoT prompts, combine both techniques, and use self-consistency (multiple reasoning paths) to boost reliability. You will build a prompting toolkit that makes your agents dramatically more capable on tasks requiring logic, math, or multi-step planning.

### Learning Objectives

By the end of this notebook, you will be able to:
- Construct few-shot example sets that improve LLM accuracy on classification, extraction, and formatting tasks.
- Explain the difference between zero-shot, few-shot, and zero-shot-CoT prompting and select the right approach for a given task.
- Write chain-of-thought prompts that elicit explicit step-by-step reasoning before the final answer.
- Implement self-consistency: sample multiple CoT reasoning paths and select the most common answer via majority vote.
- Measure the accuracy gain from each technique (zero-shot vs. few-shot vs. CoT vs. few-shot-CoT vs. self-consistency) on a consistent test set.
- Apply few-shot and CoT techniques to agent system prompts, specifically for tool selection and action planning.

### Prerequisites

- [`01_system_prompt_design.ipynb`](01_system_prompt_design.ipynb) — You need to know how to structure system prompts before layering few-shot examples and CoT reasoning into them.
- [`../core/05_react_agent.ipynb`](../core/05_react_agent.ipynb) — The ReAct loop is a form of chain-of-thought. Seeing it in action helps you understand why CoT matters for agents.

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Zero-Shot Baseline | Establish a baseline by running a set of 10 test problems (math word problems, classification, entity extraction) with zero-shot prompting. Record accuracy. |
| 2 | Few-Shot Prompting Fundamentals | Add 2-4 examples to the prompt and re-run the same test set. Learn how example selection, ordering, and formatting affect results. |
| 3 | Few-Shot Example Engineering | Explore strategies for choosing examples: diverse coverage, boundary cases, adversarial examples. Build a helper function that selects examples from a pool based on similarity to the input. |
| 4 | Chain-of-Thought Prompting | Add "Let's think step by step" and structured reasoning templates. Re-run the test set with zero-shot-CoT and measure the accuracy improvement on reasoning-heavy tasks. |
| 5 | Few-Shot + CoT Combined | Provide examples that include explicit reasoning chains (not just input/output pairs). This is the most powerful combination — measure the accuracy gain over each technique alone. |
| 6 | Self-Consistency | Sample N=5 reasoning paths at temperature > 0, extract the final answer from each, and take the majority vote. Build a `self_consistent_answer()` function and measure its accuracy improvement. |
| 7 | CoT for Agent Tool Selection | Apply CoT to an agent's tool-selection step: instead of directly choosing a tool, the agent first reasons about which tool fits the task and why. Compare tool selection accuracy with and without CoT. |
| 8 | Cost and Latency Tradeoffs | Measure token usage and latency for each technique. Build a table showing accuracy vs. cost vs. latency for all five approaches. Discuss when each technique is worth the extra tokens. |

### Putting It Together

Build an enhanced agent tool-selection module that uses few-shot-CoT prompting. Given a user query and a list of available tools (with descriptions), the module should: (1) present few-shot examples of correct tool selection with reasoning, (2) elicit CoT reasoning about the current query, (3) optionally use self-consistency with 3 samples to pick the tool. Evaluate it on 10 diverse queries where at least 3 have ambiguous tool choices, and compare accuracy against a zero-shot tool selector.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Example Set Construction | Starter | Given a classification task (sentiment analysis on 5 categories), build a few-shot example set of 5 examples. Test with and without examples on 10 inputs and compute accuracy. |
| 2 | CoT Prompt Engineering | Moderate | Take a set of 5 math word problems that a zero-shot prompt gets wrong. Write CoT prompts that get at least 4 of 5 correct. Document which reasoning patterns you had to elicit. |
| 3 | Self-Consistency Implementation | Moderate | Implement self-consistency with configurable N (number of samples) and temperature. Run it on 10 logic puzzles with N=1, 3, 5, 7 and plot accuracy vs. N. Find the sweet spot for cost vs. accuracy. |
| 4 | Automatic CoT Generation | Stretch | Build a system that automatically generates CoT examples by prompting an LLM to solve problems step-by-step, then uses those generated chains as few-shot examples for new problems (Auto-CoT pattern). Test whether generated examples perform as well as hand-crafted ones. |

### Key References

- [Chain-of-Thought Prompting Elicits Reasoning (Wei et al., 2022)](https://arxiv.org/abs/2201.11903) — The foundational CoT paper demonstrating that adding "let's think step by step" dramatically improves reasoning.
- [Self-Consistency Improves Chain of Thought Reasoning (Wang et al., 2022)](https://arxiv.org/abs/2203.11171) — Introduces majority-vote self-consistency over multiple reasoning paths.
- [Automatic Chain of Thought Prompting (Zhang et al., 2022)](https://arxiv.org/abs/2210.03493) — Automates the construction of CoT demonstrations instead of hand-crafting them.
- [Anthropic — Give Claude Examples](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting) — Anthropic's guide on multishot prompting with practical formatting advice.
- [OpenAI — Strategy: Provide Reference Text](https://platform.openai.com/docs/guides/prompt-engineering#strategy-provide-reference-text) — OpenAI's few-shot and reference text patterns.
- [Lilian Weng — Prompt Engineering](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/) — Section on CoT, self-consistency, and related prompting strategies.
- [Tree of Thoughts (Yao et al., 2023)](https://arxiv.org/abs/2305.10601) — Extension of CoT that explores multiple reasoning branches; useful context for understanding where CoT fits in the broader landscape.

---

## 03. Structured Output Prompting

**File:** `03_structured_output_prompting.ipynb`

### Overview

Agents must produce structured, parseable output — tool calls need valid JSON arguments, multi-step plans need consistent formatting, and downstream systems need data they can process programmatically. This notebook covers three levels of structured output control: prompt-level techniques (XML tags, JSON instruction), API-level features (JSON mode, response format), and library-level constrained generation (Outlines). You will build increasingly reliable structured output pipelines and learn when each approach is appropriate, from quick-and-dirty prompting to guaranteed-valid output.

### Learning Objectives

By the end of this notebook, you will be able to:
- Use XML tags and delimiters in prompts to create parseable output sections that can be extracted with simple string operations.
- Write JSON-producing prompts with schema descriptions and extract valid JSON from LLM responses, including handling common failure modes (markdown fencing, trailing commas, partial output).
- Use API-level JSON mode (where available) and compare its reliability against prompt-only approaches.
- Define a Pydantic model for your expected output and validate LLM responses against it, including retry logic for validation failures.
- Use the Outlines library for constrained generation that guarantees output conforming to a JSON schema or regex pattern.
- Select the appropriate structured output technique for a given use case based on the tradeoffs between flexibility, reliability, latency, and model compatibility.

### Prerequisites

- [`../core/04_structured_output.ipynb`](../core/04_structured_output.ipynb) — Core 04 covers JSON mode and basic output parsing. This notebook goes deeper into prompt-level techniques and constrained generation.
- [`01_system_prompt_design.ipynb`](01_system_prompt_design.ipynb) — Structured output prompting builds on system prompt design skills, especially format contracts.

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | The Structured Output Spectrum | Survey three levels of structured output control: prompt-level (soft), API-level (medium), library-level (hard). Understand when each is appropriate and the reliability vs. flexibility tradeoff. |
| 2 | XML Tags and Delimiters | Use XML-style tags (`<thinking>`, `<answer>`, `<tool_call>`) to create parseable output regions. Build a `parse_xml_tags()` helper. This is Anthropic's recommended approach for Claude and works well across models. |
| 3 | JSON via Prompting | Write prompts that produce JSON output: include the target schema in the system prompt, add "respond only with valid JSON" constraints, and handle common failures (markdown code fences, extra text before/after JSON). Build a robust `extract_json()` parser. |
| 4 | API-Level JSON Mode | Use OpenRouter's JSON mode / response_format parameter. Compare reliability: prompt-only JSON vs. API JSON mode on 20 test cases. Measure parse success rate for each. |
| 5 | Schema Validation with Pydantic | Define Pydantic models for expected outputs (e.g., `ToolCall(name: str, arguments: dict)`, `PlanStep(step: int, action: str, reason: str)`). Validate LLM output against the model and build a retry loop for validation failures. |
| 6 | Constrained Generation with Outlines | Use the Outlines library to guarantee output matches a JSON schema or regex. Understand how constrained decoding works (token masking at generation time). Compare latency and output quality vs. unconstrained generation. |
| 7 | Nested and Complex Schemas | Handle real-world complexity: nested objects, arrays of objects, optional fields, enums. Build a structured output pipeline for a multi-step agent plan with nested tool call arguments. |
| 8 | Choosing the Right Approach | Decision framework: when to use XML tags (human-readable intermediate reasoning), when to use JSON mode (API integrations), when to use constrained generation (safety-critical outputs). Build a comparison table from your experiments. |

### Putting It Together

Build a structured output pipeline for an agent that produces multi-step plans. The pipeline should: (1) prompt the LLM to output a plan in a defined JSON schema (array of steps, each with action, tool, arguments, and expected_result fields), (2) validate the response against a Pydantic model, (3) retry up to 3 times on validation failure with the error message fed back to the LLM, and (4) fall back to XML-tag parsing if JSON mode is unavailable. Test on 5 different planning tasks and report the first-attempt success rate and the retry-corrected success rate.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | XML Tag Parser | Starter | Build a `parse_tags(text, tag_name)` function that extracts content from XML-style tags, handling nested tags and multiple occurrences. Test on 5 different LLM outputs. |
| 2 | Robust JSON Extractor | Moderate | Build an `extract_json(text)` function that handles: markdown fencing, leading/trailing text, single quotes instead of double quotes, trailing commas, and truncated JSON. Test against 10 malformed LLM outputs. |
| 3 | Pydantic Retry Loop | Moderate | Define a complex Pydantic model (at least 3 levels of nesting) and build a retry loop that feeds validation errors back to the LLM. Measure how many retries are needed on average across 10 runs. |
| 4 | Constrained Generation Benchmark | Stretch | Compare three approaches (prompt-only, API JSON mode, Outlines constrained generation) on the same 20 test cases across 3 different schemas. Measure: parse success rate, schema compliance rate, latency, and output quality. Write up which approach wins under what conditions. |

### Key References

- [Outlines — Structured Generation Library](https://github.com/outlines-dev/outlines) — Python library for constrained LLM generation using JSON schemas, regex patterns, and grammars.
- [Anthropic — Structured Output with Claude](https://docs.anthropic.com/en/docs/build-with-claude/structured-output) — Anthropic's guide on getting structured output from Claude, including XML tags and tool use.
- [Anthropic — Use XML Tags](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags) — Best practices for XML tag-based output structuring.
- [OpenAI — Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) — OpenAI's JSON mode and structured output features.
- [Pydantic Documentation](https://docs.pydantic.dev/latest/) — Pydantic's validation library, essential for schema validation of LLM outputs.
- [Instructor Library](https://github.com/jxnl/instructor) — Library that patches LLM clients to return Pydantic models directly, with built-in retry logic.
- [Lilian Weng — Prompt Engineering](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/) — Section on output formatting techniques.
- [Guidance Library](https://github.com/guidance-ai/guidance) — Microsoft's library for structured output using interleaved generation and constraints.

---

## 04. Prompt Testing

**File:** `04_prompt_testing.ipynb`

### Overview

Prompt engineering without testing is guessing. This notebook teaches you to build a lightweight prompt evaluation harness that lets you systematically compare prompts, detect regressions, and make data-driven decisions about prompt changes. You will construct test suites with input/expected-output pairs, build automated scoring functions (exact match, fuzzy match, LLM-as-judge), run A/B tests between prompt variants, and produce evaluation reports. This is the prompt engineer's equivalent of a test suite — and it is just as essential.

### Learning Objectives

By the end of this notebook, you will be able to:
- Build a prompt test suite: a structured collection of (input, expected_output, metadata) triples stored as JSON.
- Implement three scoring strategies: exact match, fuzzy/semantic similarity, and LLM-as-judge with a scoring rubric.
- Run an A/B test between two prompt variants on the same test suite and compute pass rates, average scores, and per-case comparisons.
- Build a `PromptEvalHarness` class that runs a prompt against a test suite, collects results, and produces a summary report.
- Detect prompt regressions: given a baseline and a candidate prompt, identify cases where the candidate is worse.
- Articulate the limitations of prompt evaluation (non-determinism, evaluator bias, metric gaming) and mitigations for each.

### Prerequisites

- [`01_system_prompt_design.ipynb`](01_system_prompt_design.ipynb) — You need to be able to write structured prompts before you can test them systematically.
- [`02_few_shot_and_cot.ipynb`](02_few_shot_and_cot.ipynb) — Few-shot and CoT prompts are key candidates for A/B testing; you should understand the techniques being evaluated.
- [`03_structured_output_prompting.ipynb`](03_structured_output_prompting.ipynb) — Structured output is essential for automated evaluation (you need parseable outputs to score them).
- [`../core/05_react_agent.ipynb`](../core/05_react_agent.ipynb) — Agent prompts are the highest-stakes prompts to test; the ReAct agent gives you a concrete prompt to evaluate.

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Why Test Prompts? | See how a "minor" prompt tweak can break 30% of previously-passing cases. Motivate systematic testing with a concrete before/after example on an agent system prompt. |
| 2 | Building a Test Suite | Define a test case schema: `{input, expected_output, tags, difficulty}`. Build a JSON test suite for a specific prompt task (e.g., tool selection, entity extraction). Include edge cases and adversarial inputs. |
| 3 | Scoring Functions: Exact and Fuzzy | Implement exact match, contains-match, and fuzzy string similarity (using `difflib.SequenceMatcher`). Discuss when each metric is appropriate and their failure modes. |
| 4 | LLM-as-Judge Scoring | Build an LLM-based evaluator: give a judge LLM the input, expected output, and actual output, and ask it to score on a 1-5 rubric. Calibrate the judge by checking its agreement with your own manual scores on 10 cases. |
| 5 | The PromptEvalHarness | Build a `PromptEvalHarness` class with methods: `run(prompt, test_suite) -> results`, `score(results, scorer) -> scored_results`, `report(scored_results) -> summary`. The summary includes pass rate, average score, worst cases, and score distribution. |
| 6 | A/B Testing Prompt Variants | Run two prompt variants through the harness on the same test suite. Produce a side-by-side comparison: overall scores, per-case deltas, cases where variant B regressed vs. baseline A. Build a `compare(results_a, results_b)` function. |
| 7 | Regression Detection | Given a baseline result set and a candidate, flag any cases where the candidate scores lower. Build a `detect_regressions(baseline, candidate, threshold)` function. Discuss how to set the threshold and handle non-determinism (run N trials per case). |
| 8 | Practical Workflow | Put it all together into a prompt development workflow: (1) write test suite, (2) establish baseline scores, (3) make prompt changes, (4) run candidate through harness, (5) compare, (6) accept or reject. Apply this workflow to improve an agent system prompt through 3 iterations. |

### Putting It Together

Take the agent system prompt you built in Notebook 01 and run it through the full evaluation workflow. Build a 15-case test suite covering normal queries, edge cases, and adversarial inputs. Establish baseline scores with the original prompt. Then make two deliberate improvements (e.g., adding CoT from Notebook 02, tightening the output format from Notebook 03) and run each variant through the harness. Produce a final report showing which changes helped, which hurt, and what the optimal prompt is. Use LLM-as-judge scoring for qualitative aspects and exact match for format compliance.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Build a Test Suite | Starter | Create a 10-case test suite for a classification prompt (e.g., intent detection for a customer support agent). Include 2 edge cases and 2 adversarial inputs. Store as JSON. |
| 2 | LLM-as-Judge Calibration | Moderate | Build an LLM judge with a 5-point rubric. Score 10 cases manually and with the judge. Compute agreement (percentage of cases within 1 point). Iterate on the rubric until agreement exceeds 80%. |
| 3 | Three-Variant A/B/C Test | Moderate | Write three prompt variants for the same task (zero-shot, few-shot, few-shot-CoT). Run all three through the harness on a 15-case test suite. Produce a comparison report with statistical summary and per-case breakdown. |
| 4 | Continuous Prompt Regression Pipeline | Stretch | Build a Python script that loads a prompt and test suite from files, runs the evaluation, compares against a saved baseline, and prints a pass/fail verdict with a regression report. This is the foundation for CI/CD for prompts — connect it to the eval track (`../eval/`) for the full pipeline. |

### Key References

- [DSPY — Programming (Not Prompting) Language Models](https://dspy-docs.vercel.app/) — Framework that compiles declarative specifications into optimized prompts. Represents the frontier of automated prompt optimization.
- [Braintrust — AI Evaluation Platform](https://www.braintrust.dev/) — Production-grade prompt evaluation and testing platform. Good reference for what a mature eval workflow looks like.
- [Anthropic — Develop Tests](https://docs.anthropic.com/en/docs/build-with-claude/develop-tests) — Anthropic's guide on building evaluations for LLM applications.
- [OpenAI — Evals Framework](https://github.com/openai/evals) — OpenAI's open-source framework for evaluating LLM outputs.
- [Hamel Husain — Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/) — Practical guide on building evals for LLM products, with emphasis on starting simple.
- [Eugene Yan — LLM Evaluation Patterns](https://eugeneyan.com/writing/llm-patterns/) — Survey of evaluation patterns for LLM systems.
- [Promptfoo](https://www.promptfoo.dev/) — Open-source tool for testing and evaluating LLM prompts.
- [Langfuse — Prompt Management](https://langfuse.com/docs/prompts) — Open-source prompt versioning and evaluation integrated with tracing.
