# Domain-Specific Agent Patterns — Lesson Plans

> Detailed lesson plans for notebooks 01–04. Different domains need different agent architectures — one size does not fit all.
> For the full track overview, see [`../roadmap.md`](../roadmap.md).

---

## 01. Code Agent Patterns

**File:** `01_code_agent_patterns.ipynb`

### Overview

This notebook explores agent architectures purpose-built for software engineering tasks: reviewing code, generating code with tests, and self-debugging when tests fail. You build three progressively sophisticated code agents, culminating in a self-healing loop where the agent writes code, runs tests, reads failures, and patches its own output until the tests pass. Code agents are the most commercially impactful agent pattern today — understanding their architecture is essential for anyone building developer tools or coding assistants.

### Learning Objectives

By the end of this notebook, you will be able to:
- Build a code review agent that reads diffs, identifies issues, and produces structured feedback
- Implement a code generation pipeline that writes both implementation and tests from a natural-language spec
- Design a self-debugging loop where the agent iterates on its own code using test output as feedback
- Use sandboxed execution (subprocess or E2B) to safely run agent-generated code
- Apply static analysis tools (AST parsing, linting) as agent-accessible verification steps
- Evaluate code agent output against reference solutions using automated metrics

### Prerequisites

- [Core 08 — CodeAgent Deep Dive](../core/08_code_agent_deep_dive.ipynb) — understanding of smolagents' CodeAgent, LocalPythonExecutor, and sandboxing fundamentals
- [Core 16 — Reflection Agent](../core/16_reflection_agent.ipynb) — the self-critique and iterative refinement loop that powers self-debugging

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Why Code Agents Are Different | How code domains differ from general Q&A: deterministic verification (tests), structured input (AST), and composability (functions/modules). Survey of production code agents (Aider, Cursor, Copilot, Devin). |
| 2 | Code Review Agent | Agent that takes a unified diff as input, parses it into hunks, and produces structured review comments (file, line, severity, suggestion). Uses few-shot prompting with real review examples. |
| 3 | Code Generation with Specs | Agent that receives a natural-language specification, generates Python code, and simultaneously produces a pytest test suite. Explores prompt strategies for encouraging testable, modular output. |
| 4 | Sandboxed Execution | Run agent-generated code safely using subprocess isolation. Capture stdout, stderr, and return codes. Discuss E2B and Docker sandboxes for production use cases. |
| 5 | The Self-Debugging Loop | Core pattern: generate code, run tests, parse failures, feed errors back to the agent, re-generate. Implement a max-retries loop with exponential backoff on LLM calls. Track iteration count and success rate. |
| 6 | Static Analysis as a Tool | Give the agent access to AST parsing (`ast` module) and linting (`ruff`) as callable tools. Agent uses these for pre-flight checks before running tests, catching syntax and style issues early. |
| 7 | Multi-File Code Generation | Extend the agent to generate multiple files (module + tests + `__init__.py`). Manage file system state, imports between generated files, and test discovery across directories. |
| 8 | Evaluation and Metrics | Measure code agent performance: pass@k, test pass rate, iteration count, and qualitative review of generated code. Compare against hand-written solutions on a small benchmark. |

### Putting It Together

Build a mini "SWE-agent" that takes a GitHub issue description as input, generates a Python module implementing the requested feature, writes tests, and iterates through a self-debugging loop until all tests pass or the retry budget is exhausted. The final output includes the implementation, passing tests, and a summary of the debugging iterations with what was fixed at each step.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Add Docstring Enforcement | Starter | Extend the code review agent to flag functions missing docstrings, using AST inspection as a tool. |
| 2 | Multi-Language Review | Moderate | Adapt the review agent to handle JavaScript diffs in addition to Python by switching the static analysis toolset based on file extension. |
| 3 | Benchmark on HumanEval | Moderate | Run your self-debugging agent on 10 problems from the HumanEval dataset and report pass@1 and average iteration count. |
| 4 | Aider-Style Edit Format | Stretch | Implement Aider's "search/replace block" edit format so the agent produces minimal diffs instead of rewriting entire files, reducing token usage and improving accuracy on large files. |

### Key References

- [SWE-bench](https://www.swebench.com/) — the standard benchmark for evaluating code agents on real GitHub issues
- [Aider](https://aider.chat/) — open-source AI pair programming tool with excellent edit format design
- [OpenAI Code Interpreter Patterns](https://platform.openai.com/docs/assistants/tools/code-interpreter) — OpenAI's approach to sandboxed code execution
- [HumanEval Benchmark](https://github.com/openai/human-eval) — function-level code generation benchmark from OpenAI
- [Anthropic — Tool Use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview) — patterns for giving agents access to external tools like linters and test runners
- [Reflexion Paper (Shinn et al.)](https://arxiv.org/abs/2303.11366) — the foundational paper on self-reflective agents that iterate using verbal feedback
- [E2B — Sandboxed Code Execution](https://e2b.dev/) — cloud sandboxes purpose-built for AI-generated code

---

## 02. Research Agent Patterns

**File:** `02_research_agent_patterns.ipynb`

### Overview

This notebook builds a research agent that searches the web, reads sources, verifies claims, synthesizes findings, and produces a cited report. Unlike code agents that have deterministic verification (tests pass or fail), research agents must handle ambiguous, contradictory, and unreliable information — requiring fundamentally different architectural choices around source evaluation, claim verification, and citation tracking. You build a full search-to-synthesis pipeline with source provenance at every step.

### Learning Objectives

By the end of this notebook, you will be able to:
- Architect a multi-phase research pipeline: query formulation, search, retrieval, verification, synthesis, and citation
- Implement iterative query refinement where the agent identifies knowledge gaps and searches again
- Build a source credibility evaluation system that scores and filters retrieved documents
- Design a claim verification step that cross-references facts across multiple sources
- Generate a structured research report with inline citations and a bibliography
- Handle conflicting information by surfacing disagreements rather than silently picking one source

### Prerequisites

- [Core 21 — Research Agent](../core/21_research_agent.ipynb) — the end-to-end research agent capstone that introduces the search-read-synthesize pattern
- [Core 13 — RAG from Scratch](../core/13_rag_from_scratch.ipynb) — embedding-based retrieval, chunking, and similarity search fundamentals

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Research vs. Other Agent Domains | Why research agents face unique challenges: no ground truth, source reliability varies, information conflicts, and synthesis requires judgment. Compare to code agents (deterministic) and data agents (structured). |
| 2 | Query Formulation and Decomposition | Agent that takes a broad research question, decomposes it into sub-questions, and generates targeted search queries for each. Uses chain-of-thought to identify what it needs to know before it can answer the main question. |
| 3 | Search Integration (Tavily + Fallbacks) | Connect the agent to Tavily for web search. Implement fallback strategies: Tavily for depth, DuckDuckGo as a free alternative, direct URL fetching for known sources. Parse and normalize results from each provider. |
| 4 | Source Evaluation and Filtering | Build a source credibility scoring system. The agent evaluates each retrieved source on recency, domain authority, content relevance, and internal consistency. Filter low-quality sources before synthesis. |
| 5 | Claim Extraction and Verification | Agent extracts discrete factual claims from retrieved content, then cross-references each claim against other sources. Flag claims that appear in only one source, contradict other sources, or lack supporting evidence. |
| 6 | Synthesis with Citations | Generate a coherent narrative that weaves findings from multiple sources. Every factual statement gets an inline citation. Handle conflicting information explicitly: "Source A claims X, while Source B reports Y." |
| 7 | Iterative Deepening | After an initial synthesis pass, the agent identifies gaps and unanswered sub-questions. It formulates new queries, retrieves additional sources, and incorporates them. Implement a depth budget to prevent unbounded research loops. |
| 8 | Output Formatting and Bibliography | Produce a final report in structured markdown with sections, inline citations (numbered or author-date), and a bibliography. Include a confidence assessment for each major finding. |

### Putting It Together

Build a research agent that takes a question like "What are the current best practices for deploying LLM agents in production?" and produces a 1000-word report with at least 5 cited sources. The agent should decompose the question into sub-topics, search for each, verify key claims across sources, handle any contradictions, and produce a final report with inline citations and a bibliography. Track the full provenance chain: which search query led to which source, which source supports which claim.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Add Recency Filtering | Starter | Modify the search step to prioritize sources from the last 12 months and flag outdated information in the final report. |
| 2 | Fact-Check Mode | Moderate | Build a mode where the agent takes a claim as input (instead of a question) and produces a verification report: confirmed, refuted, or unverifiable, with supporting evidence. |
| 3 | Multi-Perspective Research | Moderate | Extend the agent to explicitly search for opposing viewpoints on a topic and present a balanced analysis with a "perspectives" section in the final report. |
| 4 | Research Memory | Stretch | Add persistent memory so the agent can build on previous research sessions. When asked a follow-up question, it retrieves relevant findings from past sessions before searching the web. |

### Key References

- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — canonical guide to agentic architectures including research patterns
- [Tavily](https://tavily.com/) — search API purpose-built for AI agents with relevance scoring and content extraction
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — comprehensive survey including planning and tool use for research
- [STORM (Stanford)](https://arxiv.org/abs/2402.14207) — research paper on generating Wikipedia-style articles through multi-perspective question asking
- [Anthropic — Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) — techniques for improving retrieval quality with contextual embeddings
- [GAIA Benchmark](https://huggingface.co/gaia-benchmark) — benchmark requiring multi-step research and reasoning, relevant for evaluating research agents
- [Perplexity AI](https://www.perplexity.ai/) — production research agent to study for UX and citation patterns

---

## 03. Data Analysis Agent

**File:** `03_data_analysis_agent.ipynb`

### Overview

This notebook builds an agent that performs data analysis through natural language: it translates user questions into SQL queries or pandas code, executes them against real datasets, generates visualizations, and explains the results. Data analysis agents operate on structured data with known schemas, which enables a tight feedback loop — the agent can inspect table schemas, run queries, check output shapes, and iterate. You build a conversational data analyst that handles the full cycle from question to insight to chart.

### Learning Objectives

By the end of this notebook, you will be able to:
- Build an agent that translates natural-language questions into SQL queries against a SQLite database
- Implement schema-aware prompting so the agent understands table structures before writing queries
- Create a pandas-based analysis tool that the agent invokes for complex transformations and aggregations
- Generate matplotlib/seaborn visualizations from agent-produced code and embed them in responses
- Design error recovery for failed queries: parse SQL errors, fix the query, and re-execute
- Build a multi-turn data conversation where the agent maintains context about previous queries and results

### Prerequisites

- [Core 08 — CodeAgent Deep Dive](../core/08_code_agent_deep_dive.ipynb) — CodeAgent's ability to write and execute Python code is the foundation for data analysis agents
- [Appendix 12 — Databases and SQL](../appendix/12_databases_and_sql.ipynb) — SQL fundamentals, SQLite, and SQLAlchemy patterns needed for the SQL agent

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Data Agents vs. General Agents | Why structured data changes the architecture: known schemas enable validation, query results are inspectable, and visualizations provide a natural "answer format." Survey of data analysis tools (ChatGPT Code Interpreter, Julius, Hex). |
| 2 | Setting Up the Data Environment | Load sample datasets (CSV files) into SQLite. Build a schema introspection tool that the agent calls to discover tables, columns, types, and sample rows before writing queries. |
| 3 | Text-to-SQL Agent | Agent that receives a natural-language question, calls the schema tool, writes a SQL query, executes it, and returns the results as a formatted table. Handle common SQL errors (missing columns, type mismatches) with retry logic. |
| 4 | Schema-Aware Prompting | Techniques for injecting schema context into the agent's prompt. Compare strategies: full schema dump, relevant-tables-only (selected by a pre-filter), and few-shot examples of question-to-SQL pairs for the specific dataset. |
| 5 | Pandas Analysis Tool | Build a tool that lets the agent write and execute pandas code for operations awkward in SQL: pivot tables, rolling averages, percentage changes, and custom transformations. Agent chooses SQL vs. pandas based on the question. |
| 6 | Visualization Generation | Agent generates matplotlib or seaborn code to produce charts. Implement a visualization tool that executes plotting code, saves the figure, and returns the image path. Cover bar charts, line charts, scatter plots, and histograms. |
| 7 | Multi-Turn Data Conversations | Maintain conversation state so the agent can refer to previous queries and results. "Now filter that to just Q4" should work without restating the original query. Implement a query history and result cache. |
| 8 | Validation and Guardrails | Prevent destructive operations (DROP, DELETE, UPDATE) with query parsing. Validate output shapes and types. Add row-count limits to prevent the agent from dumping 100,000 rows into the context window. |

### Putting It Together

Build a conversational data analyst that takes a CSV file upload (simulated as a file path), loads it into SQLite, and then answers a series of natural-language questions about the data. The agent should: (1) inspect the schema and summarize the dataset, (2) answer at least three analytical questions using SQL or pandas, (3) produce at least one visualization, and (4) handle a multi-turn follow-up question that refines a previous query. Use a sample e-commerce dataset with orders, products, and customers tables.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Add Summary Statistics | Starter | When the agent first loads a dataset, have it automatically compute and present summary statistics (row count, column types, null counts, value distributions for categorical columns). |
| 2 | SQL Explainer Mode | Moderate | After generating a SQL query, have the agent explain the query in plain English before executing it, so the user can confirm or correct the approach. |
| 3 | Multi-Dataset Joins | Moderate | Give the agent access to multiple related tables and have it perform JOIN operations to answer cross-table questions. Test with at least 3 tables. |
| 4 | Automated EDA Report | Stretch | Build a mode where the agent conducts a full exploratory data analysis autonomously: profiles every column, identifies correlations, detects outliers, and produces a multi-section report with visualizations — all without manual prompting. |

### Key References

- [OpenAI Code Interpreter](https://platform.openai.com/docs/assistants/tools/code-interpreter) — the paradigm-defining tool for data analysis agents
- [pandas Documentation](https://pandas.pydata.org/docs/) — essential reference for DataFrame operations the agent will generate
- [matplotlib Documentation](https://matplotlib.org/stable/contents.html) — plotting library the agent uses for visualization
- [DuckDB](https://duckdb.org/) — high-performance analytical SQL engine, alternative to SQLite for larger datasets
- [Vanna.ai](https://vanna.ai/) — open-source text-to-SQL framework worth studying for prompt engineering techniques
- [Spider Benchmark](https://yale-lily.github.io/spider) — the standard benchmark for text-to-SQL evaluation
- [Anthropic — Tool Use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview) — patterns for structuring the SQL and pandas tools the agent calls

---

## 04. Document Agent

**File:** `04_document_agent.ipynb`

### Overview

This notebook builds an agent that ingests documents (PDFs, markdown, plain text), indexes them into a searchable knowledge base, and answers questions with precise citations back to the source material. Unlike web research agents that search the open internet, document agents work over a closed corpus — the user's own files — which changes the retrieval architecture, the grounding strategy, and the failure modes. You build a full document Q&A system with multi-document summarization and a knowledge base that grows over time.

### Learning Objectives

By the end of this notebook, you will be able to:
- Build a document ingestion pipeline that handles PDFs, markdown, and plain text with format-specific chunking
- Implement a retrieval-augmented generation system over a private document corpus with source attribution
- Design multi-document summarization where the agent synthesizes information across several documents
- Create a knowledge base agent that accumulates documents over time and answers questions across the full corpus
- Apply contextual retrieval techniques to improve chunk relevance by adding document-level context to each chunk
- Handle common document agent failure modes: unanswerable questions, hallucinated citations, and retrieval misses

### Prerequisites

- [Core 13 — RAG from Scratch](../core/13_rag_from_scratch.ipynb) — embedding-based retrieval, chunking strategies, and the retrieval-then-generate pattern
- [Core 14 — RAG with Tools](../core/14_rag_with_tools.ipynb) — using retrieval as an agent tool, deciding when to retrieve vs. reason from context
- [Core 12 — Conversation Memory](../core/12_conversation_memory.ipynb) — context window management and summarization strategies needed for long documents

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Document Agents vs. Web Research Agents | Key architectural differences: closed corpus (all sources are known), higher citation precision expected, no source credibility issues but format diversity challenges. Survey of production document agents (NotebookLM, ChatPDF, custom enterprise systems). |
| 2 | Document Ingestion Pipeline | Build loaders for three formats: plain text (split on paragraphs), markdown (split on headers), and PDF (extract text with `pymupdf` or `pdfplumber`). Normalize all formats into a common `Document` dataclass with metadata (source file, page number, section title). |
| 3 | Chunking Strategies for Documents | Compare chunking approaches: fixed-size with overlap, recursive text splitting, semantic chunking (split on topic boundaries), and section-aware chunking (respect document structure). Measure retrieval quality with each strategy on a test set. |
| 4 | Contextual Retrieval | Implement Anthropic's contextual retrieval technique: prepend each chunk with a short summary of its position and role within the full document. This dramatically improves retrieval accuracy for chunks that are meaningless in isolation. |
| 5 | Document Q&A with Citations | Build the core Q&A loop: user asks a question, agent retrieves relevant chunks, generates an answer, and cites the specific document and chunk (file name, page number, or section) for each claim. Implement a "no answer" response when the corpus doesn't contain relevant information. |
| 6 | Multi-Document Summarization | Agent that reads across multiple documents and produces a unified summary. Handle the challenge of documents that overlap (say the same thing differently), contradict each other, or cover complementary aspects of a topic. Use map-reduce: summarize each document individually, then synthesize the summaries. |
| 7 | Growing Knowledge Base | Build a persistent knowledge base that accumulates documents over multiple sessions. New documents are ingested and indexed incrementally. The agent answers questions across the full corpus, not just the most recently added document. Use ChromaDB or a simple JSON-based vector store for persistence. |
| 8 | Failure Modes and Guardrails | Address common document agent failures: hallucinated citations (agent cites a document that doesn't contain the claimed information), retrieval misses (relevant chunk exists but wasn't retrieved), and over-reliance on a single chunk. Implement citation verification: after generating an answer, check that each citation actually supports its claim. |

### Putting It Together

Build a "personal research library" agent. Ingest 3-5 documents on a related topic (e.g., a few research papers or blog posts about agent architectures). The agent should: (1) index all documents with contextual retrieval, (2) answer specific questions with precise citations (document name + section or page), (3) produce a cross-document summary highlighting agreements, disagreements, and unique contributions of each document, and (4) gracefully handle a question whose answer is not in any of the documents.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Add Metadata Filtering | Starter | Extend the retrieval step to support metadata filters: "only search documents from 2024" or "only search the API docs, not the blog posts." |
| 2 | Citation Verification | Moderate | After the agent generates an answer, automatically verify each citation by re-reading the cited chunk and checking whether it actually supports the claim. Flag unsupported citations. |
| 3 | Conversational Document Q&A | Moderate | Add multi-turn conversation support so the agent can handle follow-up questions like "What does Document B say about that same topic?" without the user restating the full context. |
| 4 | Hybrid Search | Stretch | Implement hybrid retrieval combining dense embeddings (semantic similarity) with sparse keyword matching (BM25). Compare retrieval quality against pure dense search on a set of test questions, especially for queries containing specific technical terms or proper nouns. |

### Key References

- [Anthropic — Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) — the technique for prepending document-level context to chunks, dramatically improving retrieval
- [Unstructured.io](https://unstructured.io/) — open-source library for document parsing across formats (PDF, DOCX, HTML, etc.)
- [ChromaDB](https://www.trychroma.com/) — lightweight vector database well-suited for document knowledge bases
- [LlamaIndex Document Agents](https://docs.llamaindex.ai/en/stable/) — reference architecture for document Q&A (study the patterns, not the framework)
- [Google NotebookLM](https://notebooklm.google.com/) — production document agent to study for UX and citation patterns
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) — fast PDF text extraction library
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — agentic RAG patterns relevant to document agents
- [BM25 (rank-bm25)](https://github.com/dorianbrown/rank_bm25) — sparse keyword retrieval for hybrid search
