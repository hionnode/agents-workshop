# Real-World Agent Projects — Lesson Plans

> Detailed lesson plans for notebooks 01–06. Portfolio-worthy projects demonstrating different agent capabilities across multiple skill areas.
> For the full track overview, see [`../roadmap.md`](../roadmap.md).

---

## 01. Personal Knowledge Assistant

**File:** `01_personal_knowledge_assistant.ipynb`

### Overview
Build an agent that indexes your personal notes and documents, answers questions about them using retrieval-augmented generation, and improves over time through conversation memory and user feedback. This is the quintessential "useful agent" — one that lives alongside your real workflow and provides genuine value. By the end, you will have a working assistant that can ingest markdown files, PDFs, or plain text, retrieve relevant passages, maintain conversation context across sessions, and refine its retrieval based on which answers were helpful.

### Learning Objectives
By the end of this notebook, you will be able to:
- Build a document ingestion pipeline that chunks, embeds, and indexes text from multiple file formats
- Implement a RAG-powered question-answering loop with source attribution
- Add conversation memory that persists across sessions using SQLite
- Create custom tools for file search, semantic retrieval, and note creation
- Implement a feedback mechanism that re-ranks retrieval results based on user signals
- Deploy the assistant as a local CLI tool you can use daily

### Prerequisites
- [`../core/12_conversation_memory.ipynb`](../core/12_conversation_memory.ipynb) — Sliding window and summary memory patterns used for multi-session context
- [`../core/13_rag_from_scratch.ipynb`](../core/13_rag_from_scratch.ipynb) — Embedding, chunking, and vector similarity fundamentals this project builds on
- [`../core/14_rag_with_tools.ipynb`](../core/14_rag_with_tools.ipynb) — Using retrieval as a tool inside an agent loop
- [`../core/05_react_agent.ipynb`](../core/05_react_agent.ipynb) — ReAct loop pattern that drives the agent's reasoning
- [`../appendix/09_file_io_and_text_processing.ipynb`](../appendix/09_file_io_and_text_processing.ipynb) — File reading and text chunking mechanics
- [`../appendix/10_numpy_for_embeddings.ipynb`](../appendix/10_numpy_for_embeddings.ipynb) — Cosine similarity and top-k retrieval

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Project Architecture | Design the full system: ingestion pipeline, vector store, agent loop, memory layer. Diagram the data flow from raw documents to answered questions. |
| 2 | Document Ingestion Pipeline | Build a pipeline that reads markdown, plain text, and PDF files, splits them into overlapping chunks, and computes embeddings using a free OpenRouter embedding model. |
| 3 | Vector Store with Persistence | Store embeddings in a local ChromaDB instance (or a NumPy-based flat index for simplicity). Implement add, search, and delete operations with metadata filtering. |
| 4 | Retrieval Tool | Wrap the vector store in a smolagents `@tool` that accepts a natural language query, retrieves the top-k most relevant chunks, and returns them with source file paths and chunk positions. |
| 5 | Note Creation Tool | Build a tool that lets the agent create new notes — the assistant can save synthesized answers, summaries, or user-provided information back into the knowledge base. |
| 6 | Agent Loop with ReAct | Wire the retrieval and note-creation tools into a ReAct agent. The agent decides when to retrieve, when to answer from memory, and when to ask clarifying questions. |
| 7 | Conversation Memory | Add sliding-window memory for the current session and summary-based long-term memory persisted in SQLite. The agent can reference previous conversations without re-retrieving. |
| 8 | Feedback and Re-ranking | Implement a thumbs-up/thumbs-down mechanism. Track which retrieved chunks led to accepted answers and boost their relevance scores in future retrievals. |
| 9 | CLI Interface | Package the agent as a command-line tool with `argparse`. Support interactive chat mode, single-question mode, and a `--reindex` flag to refresh the knowledge base. |
| 10 | Evaluation | Test the assistant against a set of 10 hand-written question-answer pairs from your own notes. Measure retrieval recall@5 and answer correctness (LLM-as-judge). |

### Putting It Together
The capstone exercise ties every component into a single coherent system. You will point the assistant at a real directory of your own notes (Obsidian vault, a folder of markdown files, or even exported Notion pages), run the full ingestion pipeline, and have a multi-turn conversation where the agent retrieves relevant passages, synthesizes answers with citations, creates new summary notes, and demonstrates that its retrieval improves after feedback. This is a tool you can genuinely continue using after the notebook is complete.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Add PDF Support | Starter | Extend the ingestion pipeline to handle PDF files using `pymupdf` or `pdfplumber`. Parse text, chunk it, and embed it alongside your markdown notes. |
| 2 | Notion Integration | Moderate | Use the Notion API to pull pages from a Notion workspace, convert them to chunks, and index them. Build a `sync_notion` tool the agent can call to refresh its knowledge. |
| 3 | Multi-collection Routing | Moderate | Support multiple knowledge bases (e.g., "work notes" vs "reading notes"). The agent decides which collection to query based on the question. |
| 4 | Obsidian Plugin | Stretch | Package the assistant as a local HTTP server that an Obsidian community plugin can call. The agent answers questions in a sidebar panel inside Obsidian. |

### Key References
- [Obsidian](https://obsidian.md/) — Popular markdown-based knowledge management tool; a natural data source for this project
- [Notion API](https://developers.notion.com/) — REST API for reading and writing Notion pages programmatically
- [Anthropic — Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) — Technique for adding context to chunks before embedding, dramatically improving retrieval quality
- [ChromaDB Documentation](https://docs.trychroma.com/) — Open-source embedding database used for the vector store
- [LangChain Text Splitters](https://python.langchain.com/docs/concepts/text_splitters/) — Reference for chunking strategies (recursive, semantic, markdown-aware)
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — Foundational blog post on agent memory architectures

---

## 02. Code Review Agent

**File:** `02_code_review_agent.ipynb`

### Overview
Build an agent that reviews pull requests by reading diffs, understanding code context across multiple files, checking for common anti-patterns, and suggesting concrete improvements with line-level precision. This project demonstrates how agents can reason about code structure, produce actionable structured output, and interact with real developer tooling through the GitHub API. The result is a working code review bot you can point at any GitHub PR.

### Learning Objectives
By the end of this notebook, you will be able to:
- Parse unified diff format and extract meaningful change context from pull requests
- Build tools that interact with the GitHub API to read PRs, files, and comments
- Implement pattern-matching rules that detect common code issues (unused imports, missing error handling, hardcoded secrets)
- Use a CodeAgent to reason about code structure across multiple files in a repository
- Generate structured review output with file paths, line numbers, severity levels, and suggested fixes
- Post review comments back to GitHub using the Checks or Reviews API

### Prerequisites
- [`../core/08_code_agent_deep_dive.ipynb`](../core/08_code_agent_deep_dive.ipynb) — CodeAgent execution model, sandbox configuration, and code reasoning patterns
- [`../core/04_structured_output.ipynb`](../core/04_structured_output.ipynb) — JSON mode and schema validation for producing structured review comments
- [`../core/07_custom_tools.ipynb`](../core/07_custom_tools.ipynb) — Building custom tools with `@tool` decorator and `Tool` subclass
- [`../appendix/04_strings_and_json.ipynb`](../appendix/04_strings_and_json.ipynb) — String parsing and JSON manipulation for diff processing

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Understanding Diffs | Parse unified diff format. Extract added/removed/modified lines, file paths, and hunks. Build a `DiffParser` class that structures raw diff text into reviewable units. |
| 2 | GitHub API Tools | Build three tools: `get_pr_diff` (fetches the diff for a PR), `get_file_content` (reads any file at a given ref), and `list_pr_files` (lists changed files with stats). Use `httpx` with a GitHub personal access token. |
| 3 | Static Pattern Checks | Implement a rule engine that scans diffs for common issues: TODO comments without tickets, print statements in production code, hardcoded API keys, unused imports, overly broad exception handlers. Each rule returns structured findings. |
| 4 | LLM-Powered Code Reasoning | Build the core review agent using CodeAgent. The agent reads the diff, pulls in surrounding file context when needed, reasons about the changes, and identifies logical bugs, missing edge cases, and style inconsistencies. |
| 5 | Multi-File Context | Teach the agent to follow imports and references across files. When a function signature changes in one file, the agent checks callers in other changed files. Build a `get_symbol_references` tool that searches the repo for usages. |
| 6 | Structured Review Output | Define a JSON schema for review output: list of comments, each with `file`, `line`, `severity` (info/warning/error), `category` (bug/style/security/performance), `message`, and `suggested_fix`. Validate all agent output against this schema. |
| 7 | Review Synthesis | After individual file reviews, the agent produces a summary: overall assessment (approve/request-changes), key concerns, positive observations, and a risk score. This mirrors the structure of a senior engineer's PR review. |
| 8 | Posting Reviews to GitHub | Use the GitHub Pull Request Reviews API to post the agent's findings as a proper PR review with inline comments at specific lines. Handle the mapping from diff line numbers to PR comment positions. |
| 9 | Configuration and Customization | Add support for a `.reviewconfig.yml` file that controls which rules are active, which file patterns to ignore (e.g., generated code, vendored dependencies), and custom review instructions per repository. |
| 10 | End-to-End Demo | Run the full pipeline on a real open-source PR. Compare the agent's review against the actual human review comments. Discuss false positives, missed issues, and calibration strategies. |

### Putting It Together
The capstone exercise runs the complete code review agent against three PRs of increasing complexity: a simple documentation change (expect minimal comments), a feature PR with 5-10 changed files (expect substantive code feedback), and a PR with a known security issue (expect the agent to flag it). You will evaluate the agent's precision (what fraction of its comments are genuinely useful) and recall (what fraction of real issues it catches), then tune the system prompt and rule thresholds to improve both metrics.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Language-Specific Rules | Starter | Add Python-specific review rules: check for missing type hints on public functions, flag `except Exception` without logging, detect mutable default arguments. |
| 2 | Test Coverage Analysis | Moderate | Build a tool that checks whether changed functions have corresponding test changes in the PR. Flag functions that were modified but whose tests were not updated. |
| 3 | GitHub Action Integration | Moderate | Package the review agent as a GitHub Action that runs automatically on every PR to a repository. Configure it to post reviews only when the diff exceeds a size threshold. |
| 4 | Learning from Feedback | Stretch | Track which review comments get "resolved" vs "dismissed" by the PR author. Use this signal to fine-tune the agent's prompts and rule weights over time, reducing false positives. |

### Key References
- [SWE-bench](https://www.swebench.com/) — Benchmark for evaluating code reasoning agents on real GitHub issues
- [GitHub REST API — Pull Requests](https://docs.github.com/en/rest/pulls) — API documentation for reading PRs, diffs, and posting reviews
- [GitHub REST API — Pull Request Reviews](https://docs.github.com/en/rest/pulls/reviews) — Creating and submitting PR reviews programmatically
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — Patterns for agents that produce structured, actionable output
- [Unified Diff Format](https://www.gnu.org/software/diffutils/manual/html_node/Unified-Format.html) — Specification for the diff format used by Git
- [CodeRabbit](https://coderabbit.ai/) — Commercial AI code review tool; useful reference for review structure and UX patterns
- [Aider](https://aider.chat/) — AI pair programming tool with excellent code context management strategies

---

## 03. Customer Support Bot

**File:** `03_customer_support_bot.ipynb`

### Overview
Build a multi-turn customer support agent that can answer questions from a product knowledge base, handle complex support workflows with escalation logic, create and update support tickets, and maintain conversation history across sessions. This project integrates RAG for knowledge retrieval, conversation memory for multi-turn context, human-in-the-loop patterns for escalation, and structured tool use for ticket management. The result is a realistic support bot that mirrors the architecture of production customer service agents.

### Learning Objectives
By the end of this notebook, you will be able to:
- Design a multi-turn conversational agent with distinct dialogue states (greeting, information gathering, resolution, escalation, closing)
- Build a product knowledge base with tiered retrieval: FAQ lookup, documentation search, and policy lookup
- Implement escalation logic that routes to a human agent based on sentiment, topic complexity, and confidence thresholds
- Create ticket management tools that open, update, and close support tickets with structured metadata
- Add conversation memory that persists customer context across sessions so returning customers do not repeat themselves
- Handle edge cases gracefully: off-topic questions, abusive language, requests the agent cannot fulfill

### Prerequisites
- [`../core/12_conversation_memory.ipynb`](../core/12_conversation_memory.ipynb) — Multi-turn memory management for maintaining conversation context
- [`../core/13_rag_from_scratch.ipynb`](../core/13_rag_from_scratch.ipynb) — Retrieval pipeline for the product knowledge base
- [`../core/14_rag_with_tools.ipynb`](../core/14_rag_with_tools.ipynb) — Using retrieval as an agent tool
- [`../patterns/03_human_in_the_loop.ipynb`](../patterns/03_human_in_the_loop.ipynb) — Escalation workflows and confidence-based routing to humans
- [`../core/05_react_agent.ipynb`](../core/05_react_agent.ipynb) — ReAct agent loop for multi-step reasoning
- [`../core/04_structured_output.ipynb`](../core/04_structured_output.ipynb) — Structured output for ticket creation and status reporting

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Support Bot Architecture | Design the full system: knowledge base tiers, conversation flow states, escalation decision tree, and ticket lifecycle. Map out how a real support interaction progresses from greeting to resolution. |
| 2 | Product Knowledge Base | Build a three-tier knowledge base: (1) FAQ pairs with exact-match lookup, (2) product documentation chunked and embedded for semantic search, (3) internal policy documents for edge cases. Populate it with synthetic data for a fictional SaaS product. |
| 3 | Knowledge Retrieval Tools | Create three retrieval tools: `search_faq` (keyword + semantic hybrid), `search_docs` (pure semantic over product docs), and `lookup_policy` (searches internal policies for billing, refund, and escalation rules). Each returns results with confidence scores. |
| 4 | Ticket Management Tools | Build tools for the support ticket lifecycle: `create_ticket` (opens a new ticket with category, priority, and description), `update_ticket` (adds notes or changes status), `get_ticket` (retrieves ticket details), and `list_customer_tickets` (shows a customer's open tickets). Store tickets in SQLite. |
| 5 | Conversation Memory | Implement session memory (sliding window for the current conversation) and customer memory (persistent profile with past interactions, preferences, and ticket history). A returning customer triggers a personalized greeting and context loading. |
| 6 | Escalation Logic | Build the escalation decision engine. The agent escalates when: (1) the customer explicitly asks for a human, (2) sentiment analysis detects frustration above a threshold, (3) the agent's retrieval confidence is below a minimum, or (4) the topic matches a mandatory-escalation list (e.g., legal, security). Escalation pauses the bot and creates a handoff summary for the human agent. |
| 7 | Dialogue State Management | Implement a lightweight state machine for conversation flow: `greeting` -> `information_gathering` -> `retrieval` -> `resolution` -> `confirmation` -> `closing`. The agent tracks which state it is in and transitions based on customer responses. Add fallback handling for unexpected inputs at each state. |
| 8 | Edge Case Handling | Handle the hard cases: off-topic questions (politely redirect), abusive language (acknowledge frustration, offer escalation), questions the knowledge base cannot answer (honest "I don't know" with ticket creation), and repeated questions (detect loops and escalate). |
| 9 | Analytics and Reporting | Track key metrics per conversation: resolution time, number of turns, escalation rate, knowledge base hit rate, and customer satisfaction (post-conversation rating). Store metrics in SQLite and build a simple summary report. |
| 10 | End-to-End Simulation | Run the bot through 5 scripted customer scenarios: a simple FAQ question, a multi-turn troubleshooting session, an angry customer requiring escalation, a returning customer with ticket history, and an off-topic conversation. Evaluate performance across all scenarios. |

### Putting It Together
The capstone exercise simulates a realistic support shift. You will run the bot through a sequence of 5 diverse customer interactions back-to-back, including a returning customer whose previous ticket information should be recalled without prompting. After all conversations complete, generate an analytics report showing resolution rate, average turn count, escalation frequency, and knowledge base coverage gaps. Identify the top 3 questions the bot could not answer and propose knowledge base additions that would address them.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Sentiment-Aware Responses | Starter | Add a sentiment analysis step before each agent response. When negative sentiment is detected, the agent adjusts its tone — more empathetic language, shorter sentences, proactive escalation offers. |
| 2 | Multi-Language Support | Moderate | Detect the customer's language from their first message and respond in that language. The knowledge base remains in English; the agent translates retrieval results before responding. |
| 3 | Slack or Discord Integration | Moderate | Wire the support bot to a Slack or Discord channel using webhooks. Customers message in the channel, the bot responds in a thread, and escalations ping a human support channel. |
| 4 | Proactive Support | Stretch | Build a mode where the agent monitors product error logs and proactively reaches out to affected customers with solutions before they file tickets. Requires event-driven architecture (see `../patterns/02_event_driven_agents.ipynb`). |

### Key References
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — Canonical guide for agent architecture patterns, particularly the workflow and escalation sections
- [Anthropic — Prompt Engineering for Support Bots](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — Best practices for system prompts in customer-facing contexts
- [Intercom](https://www.intercom.com/) — Leading customer support platform; study their Fin AI Agent for design inspiration
- [Zendesk AI Agents](https://www.zendesk.com/service/ai/) — Enterprise support agent patterns and escalation workflows
- [HuggingFace — Sentiment Analysis Models](https://huggingface.co/models?pipeline_tag=text-classification&sort=downloads) — Pre-trained models for detecting customer sentiment
- [Simon Willison — Prompt Injection](https://simonwillison.net/series/prompt-injection/) — Critical reading for any customer-facing agent; understand the attack surface

---

## 04. Data Analysis Agent

**File:** `04_data_analysis_agent.ipynb`

### Overview
Build an agent that takes natural language questions about data and produces answers through a pipeline of SQL generation, pandas transformation, matplotlib/seaborn visualization, and narrative insight generation. This project demonstrates the CodeAgent pattern at its most powerful — the agent writes and executes real Python code to explore, analyze, and visualize data, then summarizes its findings in plain English. The result is an analyst-in-a-box that turns "What were our top 5 products last quarter?" into a chart, a table, and a written summary.

### Learning Objectives
By the end of this notebook, you will be able to:
- Build a CodeAgent that generates and executes SQL queries against a SQLite database from natural language
- Implement a data analysis pipeline: question -> SQL -> pandas DataFrame -> visualization -> narrative summary
- Create tools for database schema inspection, query execution, data profiling, and chart generation
- Handle ambiguous or under-specified questions by having the agent ask clarifying questions or make reasonable assumptions
- Produce structured analysis reports combining tables, charts, and written insights
- Implement safety guardrails that prevent destructive SQL (DROP, DELETE, UPDATE) and limit query execution time

### Prerequisites
- [`../core/08_code_agent_deep_dive.ipynb`](../core/08_code_agent_deep_dive.ipynb) — CodeAgent execution model and sandboxing; the agent writes and runs Python/SQL code
- [`../core/04_structured_output.ipynb`](../core/04_structured_output.ipynb) — Structured output for analysis reports and chart specifications
- [`../appendix/12_databases_and_sql.ipynb`](../appendix/12_databases_and_sql.ipynb) — SQLite fundamentals and SQLAlchemy patterns the agent builds upon
- [`../appendix/03_data_structures.ipynb`](../appendix/03_data_structures.ipynb) — List and dict manipulation for data transformation

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Project Architecture | Design the analysis pipeline: natural language -> intent classification -> SQL generation -> execution -> pandas processing -> visualization -> narrative. Discuss why CodeAgent is the right choice (the agent needs to write and run code). |
| 2 | Sample Database Setup | Create a SQLite database with realistic sample data: a fictional e-commerce dataset with `customers`, `orders`, `products`, `order_items`, and `reviews` tables. Populate with 1000+ rows of synthetic data using Faker or manual generation. |
| 3 | Schema Inspection Tools | Build tools that let the agent explore the database: `list_tables` (shows all tables), `describe_table` (shows columns, types, sample rows), and `get_schema` (returns the full CREATE TABLE DDL). The agent uses these before writing queries. |
| 4 | SQL Generation and Execution | Build the core `run_query` tool. The agent generates SQL from the natural language question, the tool executes it against SQLite, and returns results as a pandas DataFrame. Add safety guards: read-only mode (block INSERT/UPDATE/DELETE/DROP), query timeout (5 seconds), and row limit (10,000 rows). |
| 5 | Data Profiling Tool | Create a `profile_data` tool that takes a DataFrame and returns summary statistics: row count, column types, null percentages, unique value counts, min/max/mean for numeric columns, and most frequent values for categorical columns. The agent uses this to understand data before analysis. |
| 6 | Visualization Generation | Build a `create_chart` tool powered by matplotlib and seaborn. The agent specifies chart type (bar, line, scatter, pie, histogram, heatmap), data columns, and title. The tool renders the chart and saves it as a PNG. Add smart defaults: auto-detect the best chart type based on data characteristics. |
| 7 | Multi-Step Analysis | Handle complex questions that require multiple steps: "Which product category has the highest revenue growth quarter-over-quarter?" requires (1) querying order data, (2) grouping by category and quarter, (3) calculating growth rates, (4) creating a comparison chart. The agent plans and executes these steps sequentially. |
| 8 | Narrative Generation | After producing tables and charts, the agent writes a plain-English summary of findings. Teach it to highlight key numbers, identify trends, note anomalies, and caveat its conclusions. The output is a mini analysis report. |
| 9 | Handling Ambiguity | Build logic for when questions are vague: "How are we doing?" The agent should ask a clarifying question OR make reasonable assumptions and state them explicitly. Add a `suggest_questions` tool that proposes specific analytical questions based on the available data. |
| 10 | End-to-End Analysis Session | Run a full analysis session with 5 progressively complex questions. Start with "How many orders do we have?" and build up to "What is the customer lifetime value segmented by acquisition channel, and which segment has the highest retention rate?" Evaluate the accuracy and usefulness of each answer. |

### Putting It Together
The capstone exercise simulates a real data analysis workflow. You will give the agent a dataset it has never seen before (a CSV file loaded into SQLite), ask it to perform an exploratory data analysis (profile the data, identify interesting patterns, generate 3 visualizations, and write a summary report), and then ask 3 specific business questions. The agent should produce a complete analysis document with charts, tables, and narrative — the kind of deliverable a junior data analyst would produce.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | CSV Upload Support | Starter | Build an `import_csv` tool that loads a CSV file into a new SQLite table, auto-detecting column types. The agent can then analyze any CSV the user provides. |
| 2 | Interactive Dashboard | Moderate | Generate an HTML report with embedded charts (using matplotlib's `savefig` to base64-encoded PNGs) that the user can open in a browser. Include a table of contents and clickable sections. |
| 3 | Anomaly Detection | Moderate | Add an `detect_anomalies` tool that identifies statistical outliers in any numeric column using z-scores or IQR. The agent proactively flags anomalies during exploratory analysis. |
| 4 | Natural Language to Dashboard | Stretch | Accept a high-level request like "Build me a sales dashboard" and have the agent autonomously generate 5-6 relevant charts, a KPI summary table, and a written executive summary — all saved as an HTML file. |

### Key References
- [pandas Documentation](https://pandas.pydata.org/docs/) — Core library for data manipulation; the agent generates pandas code
- [matplotlib Documentation](https://matplotlib.org/stable/) — Plotting library used for chart generation
- [seaborn Documentation](https://seaborn.pydata.org/) — Statistical visualization library built on matplotlib
- [SQLite Documentation](https://www.sqlite.org/docs.html) — Database engine used for query execution
- [Vanna.ai](https://vanna.ai/) — Open-source text-to-SQL tool; useful reference for SQL generation patterns
- [OpenAI Code Interpreter Patterns](https://platform.openai.com/docs/assistants/tools/code-interpreter) — Reference for how code execution agents handle data analysis
- [Anthropic — Tool Use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview) — Patterns for tool design that apply to all the data tools built here

---

## 05. Multi-Agent Research Team

**File:** `05_multi_agent_research_team.ipynb`

### Overview
Build a multi-agent system where three or more specialized agents — a Researcher, an Analyst, a Writer, and an Orchestrator — collaborate to produce a comprehensive research report on any topic. This project is the most architecturally complex in the track, demonstrating hierarchical orchestration, agent communication protocols, planning and task decomposition, and result aggregation. The final system takes a research question and produces a structured report with sourced findings, critical analysis, and clear writing — work that would normally take a human researcher several hours.

### Learning Objectives
By the end of this notebook, you will be able to:
- Design a multi-agent system with clearly defined roles, responsibilities, and communication protocols
- Implement a hierarchical orchestration pattern where a manager agent decomposes tasks and delegates to specialists
- Build specialized agents with distinct system prompts, tool sets, and output formats
- Create inter-agent communication using shared state and structured message passing
- Implement a planning agent that breaks a research question into sub-tasks and monitors execution progress
- Aggregate and synthesize outputs from multiple agents into a coherent final deliverable

### Prerequisites
- [`../core/18_multi_agent_basics.ipynb`](../core/18_multi_agent_basics.ipynb) — Agent communication fundamentals and shared state patterns
- [`../core/19_orchestrator_pattern.ipynb`](../core/19_orchestrator_pattern.ipynb) — Manager agent delegation and result aggregation
- [`../core/20_debate_agents.ipynb`](../core/20_debate_agents.ipynb) — Adversarial collaboration and consensus patterns used in the analysis phase
- [`../core/15_planning_agent.ipynb`](../core/15_planning_agent.ipynb) — Plan-then-execute pattern that drives the orchestrator's task decomposition
- [`../core/10_multi_agent_systems.ipynb`](../core/10_multi_agent_systems.ipynb) — smolagents `managed_agents` and hierarchical orchestration
- [`../core/07_custom_tools.ipynb`](../core/07_custom_tools.ipynb) — Building the custom tools each specialist agent uses

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | System Architecture | Design the multi-agent topology: Orchestrator at the top, Researcher / Analyst / Writer as managed agents. Define each agent's role, tools, input/output contract, and communication protocol. Draw the message flow diagram. |
| 2 | The Researcher Agent | Build a specialist agent with web search tools (`web_search`, `fetch_page`, `extract_content`). The Researcher takes a sub-question, searches for information, reads relevant pages, and returns structured findings with source URLs and relevance scores. |
| 3 | The Analyst Agent | Build a specialist that takes raw findings and performs critical analysis: identifies patterns, contradictions, gaps in evidence, and strength of sources. The Analyst produces a structured assessment with confidence levels and flags areas needing more research. |
| 4 | The Writer Agent | Build a specialist that takes analyzed findings and produces polished prose. The Writer follows a report template (executive summary, sections, conclusion), maintains consistent tone, includes inline citations, and respects a target word count. |
| 5 | The Orchestrator Agent | Build the manager agent that receives the research question, creates a research plan (3-5 sub-questions), delegates sub-questions to the Researcher, passes findings to the Analyst, sends analyzed results to the Writer, and reviews the final output. Uses smolagents `managed_agents`. |
| 6 | Planning and Task Decomposition | Implement the planning phase. The Orchestrator breaks a broad question ("What is the current state of quantum computing?") into specific sub-questions ("What are the leading hardware approaches?", "Which companies are closest to commercial viability?", etc.). Plans are structured as a DAG with dependencies. |
| 7 | Inter-Agent Communication | Build the shared state layer. Agents communicate through a structured workspace: a dictionary of research artifacts (findings, analyses, drafts) keyed by sub-task ID. Each agent reads from and writes to this workspace. Add message logging for debugging. |
| 8 | Iteration and Refinement | Implement a review loop. After the Writer produces a draft, the Orchestrator checks it against the original plan: Are all sub-questions addressed? Are citations present? Is the analysis substantive? If gaps are found, the Orchestrator sends targeted requests back to the Researcher or Analyst. Limit to 2 refinement rounds. |
| 9 | Output Assembly | Combine all artifacts into the final deliverable: a structured markdown report with title, executive summary, numbered sections with inline citations, a sources appendix, and metadata (research question, date, agents involved, total LLM calls). |
| 10 | End-to-End Research Run | Execute the full system on a real research question. Trace the entire execution: which agent was called when, what messages were passed, how the plan evolved, and how the final report compares to what a human researcher would produce. Measure total token usage and cost. |

### Putting It Together
The capstone exercise runs the complete research team on a topic of your choice with a 2-page report target. You will observe the full orchestration: the Orchestrator decomposes the question into 4 sub-tasks, the Researcher gathers information for each, the Analyst critiques and identifies gaps, the Orchestrator requests additional research on one sub-topic, and the Writer produces the final report. After the report is generated, you will evaluate it on 5 dimensions: factual accuracy, source quality, analytical depth, writing clarity, and structural completeness. Compare the total cost and time against what it would take you to write a similar report manually.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Add a Fact-Checker Agent | Starter | Add a fourth specialist that independently verifies key claims from the Researcher's findings by searching for corroborating sources. Flag claims that cannot be independently verified. |
| 2 | Parallel Research | Moderate | Modify the Orchestrator to dispatch independent sub-questions to the Researcher concurrently using `asyncio.gather`. Measure the time savings compared to sequential execution. |
| 3 | Debate Before Consensus | Moderate | Before the Writer begins, have two Analyst agents debate controversial findings. Each presents its interpretation, they exchange rebuttals, and the Orchestrator picks the stronger argument or synthesizes a balanced view. |
| 4 | Recursive Depth | Stretch | Allow the Orchestrator to spawn sub-orchestrators for complex sub-questions. A question like "Compare AI regulation in the US, EU, and China" spawns three sub-orchestrators, each running their own Researcher-Analyst pair for one region. Implement depth limits to prevent runaway recursion. |

### Key References
- [AutoGen Paper (Microsoft)](https://arxiv.org/abs/2308.08155) — Foundational research on multi-agent conversation frameworks and orchestration patterns
- [CrewAI Concepts](https://docs.crewai.com/concepts) — Role-based multi-agent framework; good reference for role definitions and task delegation
- [smolagents — Multi-Agent Systems](https://huggingface.co/docs/smolagents) — smolagents documentation on `managed_agents` and hierarchical orchestration
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — Orchestrator and routing patterns applicable to multi-agent design
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — Planning and task decomposition strategies
- [GPT Researcher](https://github.com/assafelovic/gpt-researcher) — Open-source deep research agent; useful reference for research workflow design
- [STORM (Stanford)](https://storm.genie.stanford.edu/) — Research system that generates Wikipedia-like articles; inspiration for the multi-perspective approach

---

## 06. Browser Automation Project

**File:** `06_browser_automation_project.ipynb`

### Overview
Build an agent that automates a real browser-based workflow: navigating websites, filling out forms, scraping structured data, handling dynamic content, and generating a summary report. This project brings together browser control (via Playwright), LLM reasoning for deciding what to click and where to type, structured output for extracted data, and tool orchestration for multi-step workflows. The result is an agent that can perform tedious browser tasks — like gathering competitor pricing, filling out repetitive forms, or extracting data from web dashboards — autonomously.

### Learning Objectives
By the end of this notebook, you will be able to:
- Control a browser programmatically using Playwright: navigate, click, type, screenshot, and wait for elements
- Build an agent that reasons about webpage structure using accessibility trees or screenshots and decides on next actions
- Implement a multi-step browser workflow with checkpoints and error recovery
- Extract structured data from web pages using LLM-powered parsing (not brittle CSS selectors)
- Handle dynamic web content: SPAs, JavaScript-rendered elements, pagination, and authentication flows
- Generate structured reports from scraped data with tables, summaries, and source attribution

### Prerequisites
- [`../browser-agents/01_computer_use_basics.ipynb`](../browser-agents/01_computer_use_basics.ipynb) — Fundamentals of GUI control through screenshots and coordinate-based actions
- [`../browser-agents/02_browser_agent.ipynb`](../browser-agents/02_browser_agent.ipynb) — Browser agent architecture with Playwright and LLM reasoning
- [`../core/04_structured_output.ipynb`](../core/04_structured_output.ipynb) — Structured output for extracted data and report generation
- [`../core/07_custom_tools.ipynb`](../core/07_custom_tools.ipynb) — Building the custom browser tools the agent uses
- [`../appendix/06_http_and_apis.ipynb`](../appendix/06_http_and_apis.ipynb) — HTTP fundamentals for understanding web requests and responses

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Project Architecture | Design the browser automation system: Playwright for browser control, LLM for decision-making, structured extraction for data, and report generation for output. Discuss when to use browser automation vs. APIs (browser automation is the last resort, but sometimes the only option). |
| 2 | Playwright Fundamentals | Set up Playwright in Python. Launch a browser (headless and headed modes), navigate to URLs, find elements by selector and by role, click buttons, fill input fields, take screenshots, and wait for network idle. Build these as reusable helper functions. |
| 3 | Browser Control Tools | Wrap Playwright operations in agent tools: `navigate_to(url)`, `click_element(selector)`, `fill_field(selector, text)`, `get_page_text()`, `take_screenshot()`, and `get_accessibility_tree()`. Each tool includes error handling and returns confirmation of what happened. |
| 4 | Page Understanding | Build the agent's ability to understand where it is and what it can do. Feed the accessibility tree (or a screenshot) to the LLM and ask it to identify interactive elements, form fields, navigation options, and data tables. This replaces brittle CSS selector chains with adaptive, LLM-driven page comprehension. |
| 5 | Form Filling Workflow | Implement a multi-step form-filling workflow. The agent navigates to a form (use a public test form like httpbin.org/forms/post or a locally hosted one), reads the field labels, fills in values from a provided data dictionary, handles dropdowns and checkboxes, and submits. Add validation by reading the confirmation page. |
| 6 | Data Extraction Pipeline | Build a pipeline that navigates to a page with tabular data (e.g., a public dataset listing, a product catalog, or Wikipedia table), identifies the data structure, extracts rows into a structured format (list of dicts), and handles pagination by detecting "next page" buttons and iterating. |
| 7 | Dynamic Content Handling | Handle the hard parts of modern web: wait for JavaScript-rendered content, deal with infinite scroll, handle modal dialogs and cookie consent banners, and retry on intermittent failures. Build a `wait_for_content(description)` tool where the agent describes what it is waiting for in natural language. |
| 8 | Error Recovery and Checkpointing | Implement resilience: if a step fails (element not found, navigation error, timeout), the agent diagnoses the problem from the current page state, attempts recovery (reload, go back, try alternative selectors), and logs the failure. Add checkpointing so a long workflow can resume from the last successful step. |
| 9 | Report Generation | After data extraction or workflow completion, the agent generates a structured report: what was done, what data was collected (as a formatted table), any errors encountered, and a summary of findings. Output as both JSON (machine-readable) and markdown (human-readable). |
| 10 | End-to-End Automation | Run the complete agent on a real workflow: scrape product listings from a public e-commerce site (e.g., books.toscrape.com), extract titles, prices, ratings, and availability for 50+ products across multiple pages, and generate a summary report with the top 10 highest-rated books, average price by rating, and a price distribution chart. |

### Putting It Together
The capstone exercise runs the agent through a full browser automation scenario end-to-end. You will direct the agent to visit a multi-page website (books.toscrape.com or a similar public scraping sandbox), navigate through category pages, extract structured product data from at least 3 pages, handle pagination automatically, recover from at least one simulated error (e.g., a timeout on one page), and produce a final report with a data table, summary statistics, and one visualization. Evaluate the agent on completeness (did it get all the data?), accuracy (is the extracted data correct?), and resilience (did it recover from errors?).

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Cookie Consent Handler | Starter | Build a universal cookie consent handler. Before any other action on a new page, the agent detects cookie banners (by common patterns like "Accept all", "I agree") and dismisses them. Test on 5 different websites. |
| 2 | Login Flow Automation | Moderate | Extend the agent to handle authenticated workflows. Navigate to a login page, enter credentials (from environment variables, never hardcoded), handle 2FA prompt (pause and ask the user), and maintain the session for subsequent actions. |
| 3 | Competitive Price Monitoring | Moderate | Build a workflow that visits 3 different e-commerce sites, extracts prices for the same product (by searching each site), and generates a comparison table showing the best price, price differences, and direct links. Schedule it to run daily using cron. |
| 4 | Visual Regression Testing | Stretch | Build an agent that takes screenshots of key pages in a web application, compares them against baseline screenshots using pixel-diff or perceptual hashing, and generates a report highlighting visual changes. Useful for QA workflows. |

### Key References
- [Playwright for Python Documentation](https://playwright.dev/python/) — Complete reference for browser automation with Playwright
- [Playwright MCP Server](https://github.com/microsoft/playwright-mcp) — Official MCP server for giving agents browser control
- [Browserbase](https://www.browserbase.com/) — Cloud browser infrastructure for running headless browsers at scale
- [Stagehand](https://github.com/browserbase/stagehand) — AI-native browser automation framework that uses natural language selectors
- [Anthropic — Computer Use](https://docs.anthropic.com/en/docs/agents-and-tools/computer-use) — Anthropic's approach to GUI automation through screenshots and coordinates
- [books.toscrape.com](https://books.toscrape.com/) — Public sandbox for practicing web scraping; no rate limits, designed for learners
- [Web Scraping Best Practices](https://scrapfly.io/blog/web-scraping-best-practices/) — Ethical and technical guidelines for responsible scraping
