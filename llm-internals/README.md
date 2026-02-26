# LLM Internals for Agent Builders — Lesson Plans

> Detailed lesson plans for notebooks 01–04. Understanding how LLMs work makes you a better agent builder — you know WHY prompting tricks work.
> For the full track overview, see [`../roadmap.md`](../roadmap.md).

---

## 01. Tokenization Deep Dive

**File:** `01_tokenization_deep_dive.ipynb`

### Overview

Tokens are the atoms of every LLM interaction. This notebook teaches you how text becomes numbers through Byte Pair Encoding (BPE), then has you build a minimal BPE tokenizer from scratch. You will learn how to count tokens accurately, understand why context window limits exist, and discover why seemingly simple prompts can blow your token budget. For agent builders, every API call costs tokens — knowing how tokenization works lets you write tighter prompts, estimate costs before runtime, and debug mysterious truncation bugs.

### Learning Objectives

By the end of this notebook, you will be able to:
- Explain how BPE tokenization converts raw text into integer token IDs step by step
- Implement a minimal BPE tokenizer from scratch in Python (training + encoding + decoding)
- Use `tiktoken` and the OpenRouter tokenization endpoint to count tokens for real models
- Predict how different content types (code, JSON, multilingual text, whitespace-heavy prompts) affect token counts
- Calculate the token budget for an agent's system prompt, conversation history, tool definitions, and expected output
- Identify tokenization pitfalls that cause agent failures (mid-word splits, special tokens, encoding mismatches)

### Prerequisites

- [`../appendix/04_strings_and_json.ipynb`](../appendix/04_strings_and_json.ipynb) — string manipulation, encoding basics, and JSON structure (tokens are built from bytes and characters)
- [`../core/01_hello_llm.ipynb`](../core/01_hello_llm.ipynb) — making API calls to OpenRouter (you will tokenize the same messages you send to the API)

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | From Text to Numbers | Why LLMs can't read text directly. Walk through character-level, word-level, and subword tokenization with examples showing the tradeoffs of each approach. |
| 2 | Byte Pair Encoding (BPE) — The Algorithm | Step-by-step BPE: start with bytes, count pairs, merge the most frequent pair, repeat. Trace through a worked example by hand before writing any code. |
| 3 | Build a BPE Tokenizer from Scratch | Implement `train()`, `encode()`, and `decode()` for a minimal BPE tokenizer. Train it on a small corpus and inspect the learned merges. |
| 4 | Real Tokenizers: tiktoken and SentencePiece | Use OpenAI's `tiktoken` to tokenize text for GPT-4o and Claude-compatible tokenizers. Compare your BPE output with production tokenizers — where do they differ and why? |
| 5 | Token Counting for Agent Builders | Count tokens in a realistic agent prompt: system message + conversation history + tool definitions + user query. Build a `count_tokens()` utility function for the `utils/` module. |
| 6 | Context Windows and Token Budgets | Map out the token budget for popular models (Claude, GPT-4o, Llama 3, Mistral). Calculate how many conversation turns fit before truncation. Build a budget planner function. |
| 7 | Tokenization Gotchas | Explore edge cases that break agents: multilingual text inflating token counts, JSON and code being surprisingly expensive, whitespace tokens, special/control tokens, and prompt injection via token boundaries. |
| 8 | Visualizing Tokenization | Build a color-coded token visualizer that highlights token boundaries in any text string. Use it to inspect how your agent prompts get split. |

### Putting It Together

Build a `TokenBudgetPlanner` class that takes a model name and its context window size, then accepts a system prompt, tool definitions, and conversation history. It calculates the remaining tokens available for the LLM's response, warns when you are approaching the limit, and suggests truncation strategies (drop oldest messages, summarize, or trim tool definitions). Wire it into the `chat()` helper from `utils/` so every API call reports its token usage.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Tokenize and Compare | Starter | Tokenize the same paragraph with your BPE tokenizer and with `tiktoken`. Count the tokens, list the differences, and explain why production tokenizers produce fewer tokens. |
| 2 | Multilingual Token Tax | Moderate | Pick 5 languages (English, Spanish, Chinese, Arabic, Hindi). Tokenize the same 100-word passage in each. Graph the token counts and explain the disparity. What does this mean for multilingual agents? |
| 3 | Agent Budget Estimator | Moderate | Given a ReAct agent with 5 tools (each with a JSON schema description), a system prompt, and a 10-turn conversation, calculate the total token cost per loop iteration. Identify which component consumes the most tokens. |
| 4 | Build a Tokenization-Aware Truncator | Stretch | Write a function that truncates conversation history to fit within a token budget while preserving the system prompt, the most recent N messages, and a summary of dropped messages. Test it against your `TokenBudgetPlanner`. |

### Key References

- [Andrej Karpathy — Let's build the GPT Tokenizer (video)](https://www.youtube.com/watch?v=zduSFxRajkE) — 2-hour deep dive building a BPE tokenizer from scratch, the single best resource on this topic
- [tiktoken (GitHub)](https://github.com/openai/tiktoken) — OpenAI's fast BPE tokenizer library; the standard for token counting
- [Anthropic — Token Counting](https://docs.anthropic.com/en/docs/build-with-claude/token-counting) — Official docs on counting tokens for Claude models
- [HuggingFace Tokenizer Summary](https://huggingface.co/docs/transformers/tokenizer_summary) — Excellent overview of BPE, WordPiece, and SentencePiece with diagrams
- [OpenRouter API — Models](https://openrouter.ai/models) — Context window sizes and pricing per token for every model you can access
- [Sennrich et al. — Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909) — The original BPE-for-NLP paper (short, readable)
- [Karpathy — minbpe (GitHub)](https://github.com/karpathy/minbpe) — Minimal, clean BPE implementations in Python for educational use

---

## 02. Attention and Context

**File:** `02_attention_and_context.ipynb`

### Overview

Attention is the mechanism that lets LLMs decide which parts of the input matter for each output token. This notebook demystifies the attention mechanism with visual, step-by-step NumPy implementations — you will compute query, key, and value matrices, visualize attention patterns, and understand why models with 128K context windows can still "lose" information in the middle. For agent builders, understanding attention explains why tool definitions at the start of a long prompt get ignored, why retrieval placement matters, and how to structure prompts so the model attends to what matters.

### Learning Objectives

By the end of this notebook, you will be able to:
- Implement single-head scaled dot-product attention from scratch using NumPy
- Explain the roles of queries, keys, and values using an intuitive analogy and concrete matrix operations
- Visualize attention weight heatmaps and interpret which tokens attend to which
- Describe multi-head attention and why it outperforms single-head attention
- Apply the "lost in the middle" research to structure agent prompts for maximum information retention
- Compare context window strategies (sliding window, sparse attention, retrieval-augmented) and choose the right one for an agent task

### Prerequisites

- [`01_tokenization_deep_dive.ipynb`](01_tokenization_deep_dive.ipynb) — tokens are the units that attention operates over; you need to understand tokenization before attention makes sense
- [`../appendix/10_numpy_for_embeddings.ipynb`](../appendix/10_numpy_for_embeddings.ipynb) — dot products, matrix multiplication, and softmax (the mathematical building blocks of attention)

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | The Intuition: Why Attention? | Before attention, models processed sequences left-to-right with fixed-size hidden states (RNNs). Learn why this bottleneck killed long-range dependencies, and how attention solved it by letting every token "look at" every other token. |
| 2 | Scaled Dot-Product Attention in NumPy | Implement the core attention formula: `softmax(QK^T / sqrt(d_k)) V`. Start with tiny matrices (4 tokens, dimension 3) so you can trace every number. Visualize the attention weights as a heatmap. |
| 3 | Queries, Keys, and Values — Demystified | Build intuition for Q, K, V using the "library search" analogy: query = what you are looking for, keys = book titles on the shelf, values = book contents. Show how learned weight matrices (W_Q, W_K, W_V) project embeddings into these roles. |
| 4 | Causal Masking and Autoregressive Generation | Apply a causal mask so tokens can only attend to previous tokens (not future ones). Implement masked attention and show why this is essential for text generation. Visualize the triangular attention pattern. |
| 5 | Multi-Head Attention | Split the attention computation into multiple heads, each attending to different aspects of the input. Implement multi-head attention, concatenate the heads, and compare its attention patterns against single-head. |
| 6 | The Full Transformer Block | Assemble a complete transformer block: multi-head attention + residual connection + layer normalization + feed-forward network + another residual connection. Run a forward pass through your block. |
| 7 | Context Windows in Practice | Map context windows across models (4K to 200K+). Explore the "lost in the middle" phenomenon with experiments: place key information at the beginning, middle, and end of long prompts and measure retrieval accuracy. Derive practical placement rules for agent builders. |
| 8 | Long-Context Strategies for Agents | Survey strategies for when your agent's context overflows: sliding window, RAG (retrieve instead of stuff), summarization, hierarchical context, and hybrid approaches. Build a decision tree for choosing the right strategy. |

### Putting It Together

Build an `AttentionExplorer` tool that takes a short text, tokenizes it (using your tokenizer from notebook 01), runs it through your NumPy attention implementation, and produces an interactive-style heatmap showing which tokens attend to which. Then use it to analyze a real agent prompt — a ReAct system prompt with tool definitions and a user query — to visualize where the model's "attention budget" is being spent. Use the findings to refactor the prompt for better information retention.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Trace Attention by Hand | Starter | Given a 4-token input and pre-computed Q, K, V matrices, compute the attention weights and output by hand (on paper or in a cell). Verify your answer against the NumPy implementation. |
| 2 | Attention Pattern Zoo | Moderate | Generate attention heatmaps for 5 different input types: a simple sentence, a code snippet, a JSON object, a list of instructions, and a question about a paragraph. Compare the patterns and write up what you observe. |
| 3 | Lost in the Middle Experiment | Moderate | Place a unique "needle" fact at 5 different positions in a 2000-token prompt. Send each version to an LLM via OpenRouter and measure whether the model retrieves the needle correctly. Plot retrieval accuracy vs. position. |
| 4 | Context Window Strategy Advisor | Stretch | Build a function that takes an agent's current context (system prompt + history + tools) and recommends a context management strategy based on the token count, the model's context window, and the task type. Implement at least two strategies (truncation and summarization) and benchmark them. |

### Key References

- [Jay Alammar — The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) — The definitive visual walkthrough of the transformer architecture; read this first
- [Vaswani et al. — Attention Is All You Need (2017)](https://arxiv.org/abs/1706.03762) — The original transformer paper; Section 3 on scaled dot-product and multi-head attention is essential
- [3Blue1Brown — Visualizing Attention (video)](https://www.youtube.com/watch?v=eMlx5fFNoYc) — Beautiful visual explanation of attention mechanics with animations
- [Liu et al. — Lost in the Middle (2023)](https://arxiv.org/abs/2307.03172) — Research showing LLMs struggle with information placed in the middle of long contexts
- [Anthropic — Long Context Tips](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips) — Practical advice for structuring long prompts for Claude
- [Karpathy — Let's build GPT from scratch (video)](https://www.youtube.com/watch?v=kCc8FmEb1nY) — Builds a full transformer including attention from scratch in PyTorch
- [Jay Alammar — The Illustrated GPT-2](https://jalammar.github.io/illustrated-gpt2/) — Visual walkthrough of GPT-2 architecture with attention patterns
- [Lilian Weng — Attention? Attention!](https://lilianweng.github.io/posts/2018-06-24-attention/) — Comprehensive survey of attention mechanisms from soft attention through transformers

---

## 03. Sampling and Generation

**File:** `03_sampling_and_generation.ipynb`

### Overview

When an LLM generates text, it produces a probability distribution over the entire vocabulary for each next token. How you *sample* from that distribution — temperature, top-p, top-k, repetition penalty — determines whether your agent's output is creative or deterministic, diverse or repetitive, safe or risky. This notebook makes these parameters concrete: you will implement each sampling strategy from scratch, visualize how they reshape the probability distribution, and develop intuition for which settings to use for different agent tasks (tool calls demand low temperature; brainstorming wants high temperature). Mastering sampling is the difference between an agent that reliably calls tools and one that hallucinates function names.

### Learning Objectives

By the end of this notebook, you will be able to:
- Implement greedy decoding, temperature scaling, top-k filtering, top-p (nucleus) sampling, and repetition penalty from scratch
- Visualize how each sampling parameter reshapes the token probability distribution
- Explain why `temperature=0` is not truly deterministic and what that means for reproducibility
- Select optimal sampling parameters for different agent tasks (tool calling, creative writing, code generation, structured output)
- Diagnose agent failures caused by incorrect sampling settings (hallucinated tool names, repetitive loops, truncated JSON)
- Combine multiple sampling strategies (e.g., temperature + top-p) and understand their interaction effects

### Prerequisites

- [`01_tokenization_deep_dive.ipynb`](01_tokenization_deep_dive.ipynb) — you need to understand token vocabularies and token IDs since sampling selects from a distribution over the vocabulary
- [`../core/01_hello_llm.ipynb`](../core/01_hello_llm.ipynb) — you have already used `temperature` as an API parameter; now you will learn what it actually does under the hood

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | From Logits to Probabilities | Start with raw model outputs (logits), apply softmax to get probabilities, and visualize the resulting distribution. Understand why the distribution is almost always "spiky" — a few tokens have high probability, most have near-zero. |
| 2 | Greedy Decoding | Always pick the highest-probability token. Implement it, generate text, and observe the result: coherent but boring, repetitive, and prone to loops. Understand when greedy decoding is actually what you want (structured output, tool calls). |
| 3 | Temperature Scaling | Implement temperature: divide logits by T before softmax. Visualize how T < 1 sharpens the distribution (more deterministic), T > 1 flattens it (more random), and T = 1 leaves it unchanged. Generate text at temperatures 0.1, 0.5, 1.0, and 1.5 and compare. |
| 4 | Top-k Sampling | Keep only the k highest-probability tokens, zero out the rest, re-normalize. Implement it, experiment with k values (1, 5, 40, 100), and observe how it prevents low-probability garbage tokens while preserving diversity. |
| 5 | Top-p (Nucleus) Sampling | Keep the smallest set of tokens whose cumulative probability exceeds p. Implement it, compare with top-k (top-p adapts to the distribution shape — tight distributions need fewer tokens, flat distributions keep more). Show why top-p is generally preferred over top-k. |
| 6 | Repetition Penalty and Frequency Penalty | Implement penalties that reduce the probability of tokens that have already appeared. Understand the difference between presence penalty (did it appear?) and frequency penalty (how often?). Show how they break repetition loops in agent output. |
| 7 | Combining Strategies | Apply temperature + top-p + repetition penalty together. Implement the full sampling pipeline in the correct order: logits -> repetition penalty -> temperature -> top-k -> top-p -> sample. Experiment with combinations. |
| 8 | Sampling Recipes for Agent Tasks | Build a lookup table of recommended sampling configurations for common agent tasks: tool calling, ReAct reasoning, creative writing, code generation, JSON output, summarization. Test each recipe against real API calls via OpenRouter. |

### Putting It Together

Build a `SamplingPlayground` that takes a prompt, calls the LLM multiple times with different sampling configurations, and displays the outputs side by side. Then run it on three agent-critical prompts: (1) a tool-calling prompt where the agent must output a valid JSON function call, (2) a ReAct reasoning prompt where the agent must produce Thought/Action/Observation, and (3) an open-ended research prompt where the agent must brainstorm approaches. For each, identify which sampling configuration produces the most reliable agent behavior, and document your findings as a reusable reference.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Temperature Visualizer | Starter | For a fixed set of logits (provided), plot the probability distribution at temperatures 0.1, 0.5, 1.0, and 2.0 as bar charts. Annotate the top-5 tokens and their probabilities on each chart. |
| 2 | Top-k vs Top-p Showdown | Moderate | Generate 20 completions each using top-k=40 and top-p=0.9 for the same prompt. Measure the diversity (unique completions) and quality (does the output make sense?) of each. Which strategy wins for your test case? |
| 3 | Agent Reliability Benchmark | Moderate | Pick a tool-calling prompt and generate 50 completions at 5 different temperature settings (0.0, 0.3, 0.5, 0.7, 1.0). Parse each completion and count how many produce valid JSON tool calls. Plot the reliability curve. |
| 4 | Build a Sampling Strategy Recommender | Stretch | Write a function that takes a task description (e.g., "generate a JSON tool call", "brainstorm research questions", "summarize a document") and returns recommended sampling parameters with explanations. Test it against the recipes from Section 8. |

### Key References

- [HuggingFace — How to Generate Text](https://huggingface.co/blog/how-to-generate) — Excellent walkthrough of greedy, beam search, top-k, and top-p with interactive visualizations
- [Anthropic — Model Card (Claude)](https://docs.anthropic.com/en/docs/about-claude/models) — Supported parameters, context windows, and recommended settings for Claude models
- [Holtzman et al. — The Curious Case of Neural Text Degeneration (2020)](https://arxiv.org/abs/1904.09751) — The paper that introduced nucleus (top-p) sampling and demonstrated why pure top-k fails
- [OpenRouter API Docs — Parameters](https://openrouter.ai/docs/api-reference/parameters) — Which sampling parameters each provider supports through OpenRouter
- [Cohere — LLM University: Text Generation](https://docs.cohere.com/docs/text-generation) — Clear explanations of temperature, top-k, and top-p with examples
- [Anthropic — Prompt Engineering: Be Direct](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/be-direct) — How prompt structure interacts with sampling to produce reliable agent output

---

## 04. Model Selection

**File:** `04_model_selection.ipynb`

### Overview

Not every agent task needs the same model. A simple classifier agent can use a free 7B model; a multi-step research agent needs a frontier model. This notebook teaches you how to evaluate and select models for different agent use cases, covering the open vs. closed model spectrum, cost/quality/latency tradeoffs, benchmark interpretation, and practical routing strategies. You will build a model selection framework that recommends the right model for a given task and budget, then validate it by running the same agent across multiple models and comparing results. For agent builders, model selection is one of the highest-leverage decisions you make — picking the right model can cut costs 100x while maintaining quality.

### Learning Objectives

By the end of this notebook, you will be able to:
- Compare open-weight and closed-source models across capability, cost, latency, and privacy dimensions
- Read and critically interpret LLM benchmarks (MMLU, HumanEval, MATH, Chatbot Arena ELO) without being misled by cherry-picked numbers
- Calculate the full cost of an agent run (input tokens + output tokens + tool calls + retries) for different model choices
- Implement a model routing strategy that uses cheap models for easy tasks and expensive models for hard tasks
- Select the right model for specific agent patterns: tool calling, code generation, long-context RAG, multi-turn conversation, structured output
- Set up A/B testing to compare models on your specific agent workload

### Prerequisites

- [`01_tokenization_deep_dive.ipynb`](01_tokenization_deep_dive.ipynb) — token counting and context window concepts (you need these to calculate costs and understand model limits)
- [`02_attention_and_context.ipynb`](02_attention_and_context.ipynb) — context window strategies and attention mechanics (you need these to evaluate long-context models)
- [`03_sampling_and_generation.ipynb`](03_sampling_and_generation.ipynb) — sampling parameters and their effect on output quality (different models respond differently to the same sampling settings)
- [`../core/05_react_agent.ipynb`](../core/05_react_agent.ipynb) — you need a working agent to test across models (the ReAct agent is the benchmark agent for this notebook)

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | The Model Landscape (2025-2026) | Survey the current model ecosystem: frontier closed models (Claude, GPT-4o, Gemini), open-weight models (Llama 3, Mistral, Qwen), and specialized models (code, math, vision). Understand the open vs. closed tradeoffs: capability, cost, privacy, customizability, and rate limits. |
| 2 | Reading Benchmarks Without Getting Fooled | Interpret major benchmarks: MMLU (general knowledge), HumanEval (code), MATH/GSM8K (reasoning), Chatbot Arena ELO (human preference). Learn why benchmarks lie — contamination, task mismatch, cherry-picking — and how to read them critically. |
| 3 | Cost Anatomy of an Agent Run | Break down the full cost of an agent run: input tokens (system prompt + history), output tokens (reasoning + tool calls + final answer), and hidden costs (retries on failures, multi-turn overhead). Calculate costs for the same agent task across 5 models. |
| 4 | Latency, Throughput, and Time-to-First-Token | Measure latency (time to first token), throughput (tokens per second), and total generation time for different models via OpenRouter. Understand why latency matters for agent loops (10 LLM calls at 2s each = 20s total). Build a latency benchmarking script. |
| 5 | Model Capabilities Matrix | Build a capabilities matrix: which models support tool calling, JSON mode, vision, long context (100K+), streaming, and system prompts? Test each capability with a concrete example. Identify the gaps that will break your agent. |
| 6 | Model Routing: Cheap for Easy, Expensive for Hard | Implement a model router that classifies task difficulty (simple lookup, moderate reasoning, complex multi-step) and routes to the appropriate model. Start with a rule-based router, then build an LLM-based difficulty classifier. |
| 7 | Same Agent, Different Models | Run your ReAct agent (from Core 05) against the same set of 10 test queries using 4 different models. Score each on: correctness, cost, latency, and tool-calling reliability. Build a comparison scorecard. |
| 8 | Building Your Model Selection Framework | Synthesize everything into a reusable `ModelSelector` that takes task requirements (capabilities needed, budget, latency target, quality threshold) and returns ranked model recommendations. Save your decision criteria as a reference card. |

### Putting It Together

Run the ReAct agent from Core 05 against a standardized test suite of 10 tasks (ranging from simple factual lookups to multi-step reasoning) using at least 4 models: one frontier closed model (Claude Sonnet or GPT-4o), one mid-tier model (Claude Haiku, GPT-4o-mini), one open-weight model (Llama 3 70B via OpenRouter), and one free-tier model. For each model-task combination, record correctness, total cost, latency, and number of tool calls. Produce a summary scorecard and use it to configure your `ModelSelector` with empirically-validated routing rules. The goal is a concrete, data-driven answer to: "Which model should my agent use, and when?"

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Cost Calculator | Starter | Build a function that takes a model name and a conversation (list of messages) and returns the estimated cost in USD. Support at least 5 models with their current pricing from OpenRouter. |
| 2 | Benchmark Critic | Moderate | Pick a model provider's blog post announcing a new model. Find 3 benchmark claims, look up the methodology for each benchmark, and write a critical assessment: are the claims meaningful for agent use cases? |
| 3 | Build a Latency Profiler | Moderate | Write a script that sends the same prompt to 5 models via OpenRouter and records time-to-first-token, tokens-per-second, and total time. Run it 10 times each and report the median and p95 latencies. Visualize the results. |
| 4 | Production Model Router | Stretch | Implement a model router that uses a cheap, fast model to classify incoming queries by difficulty, then routes to the appropriate model. Test it on 20 diverse queries and measure whether routing decisions match what you would choose manually. Calculate the cost savings compared to always using the most expensive model. |

### Key References

- [OpenRouter — Models](https://openrouter.ai/models) — Live pricing, context windows, and capabilities for every model accessible through OpenRouter
- [Chatbot Arena / LMSYS Leaderboard](https://chat.lmsys.org/) — Human-preference ELO rankings; the most trusted model comparison benchmark
- [Anthropic — Model Card (Claude)](https://docs.anthropic.com/en/docs/about-claude/models) — Capabilities, context windows, pricing, and recommended use cases for Claude models
- [Artificial Analysis](https://artificialanalysis.ai/) — Independent benchmarks for LLM speed, quality, and cost across providers
- [OpenAI — Model Overview](https://platform.openai.com/docs/models) — GPT model capabilities, pricing, and rate limits
- [Vellum LLM Leaderboard](https://www.vellum.ai/llm-leaderboard) — Aggregated benchmark scores with filtering by task type
- [HuggingFace Open LLM Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard) — Rankings for open-weight models across standard benchmarks
- [Simon Willison — Understanding LLM Pricing](https://simonwillison.net/tags/llm-pricing/) — Practical analysis of LLM costs and how they affect real applications
