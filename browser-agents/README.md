# Computer Use & Browser Agents — Lesson Plans

> Detailed lesson plans for notebooks 01–04. Browser automation is one of the most impactful agent capabilities in 2025-2026.
> For the full track overview, see [`../roadmap.md`](../roadmap.md).

---

## 01. Computer Use Basics

**File:** `01_computer_use_basics.ipynb`

### Overview

This notebook introduces Anthropic's Computer Use API — the ability for an LLM to control a graphical user interface by looking at screenshots, reasoning about what it sees, and issuing coordinate-based actions (click, type, scroll, drag). You will build a minimal computer-use loop that captures a screenshot, sends it to Claude, parses the returned tool call, executes the action, and repeats. This is the foundation for all browser and desktop automation agents: the model literally "sees" the screen and decides what to do next.

### Learning Objectives

By the end of this notebook, you will be able to:
- Explain how the Computer Use API works at the protocol level (screenshot in, tool-use action out)
- Send a screenshot to Claude and receive structured coordinate-based actions (click, type, scroll, key)
- Implement the screenshot-action-screenshot loop that powers all computer-use agents
- Parse and dispatch `computer_20241022` tool calls returned by the model
- Understand the coordinate system (absolute pixel coordinates) and how the model maps visual elements to positions
- Identify the limitations and failure modes of screenshot-based GUI control (resolution sensitivity, dynamic content, timing)

### Prerequisites

- [`../core/05_react_agent.ipynb`](../core/05_react_agent.ipynb) — the computer-use loop is a specialized ReAct loop (Observe screenshot -> Think -> Act -> Observe next screenshot)
- [`../core/04_structured_output.ipynb`](../core/04_structured_output.ipynb) — the API returns structured tool-call JSON that you need to parse and validate

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Why Computer Use? | Motivation: agents that can use ANY software, not just APIs. Survey the landscape — Anthropic Computer Use, OS-level agents, accessibility-tree approaches. |
| 2 | The Computer Use API | How Anthropic's API works: you send a screenshot as a base64 image, the model returns a tool call with action type and coordinates. Walk through the request/response format. |
| 3 | Capturing Screenshots | Use `Pillow` and platform utilities to capture screenshots programmatically. Resize to the resolution the model expects (1280x800 recommended). Encode as base64. |
| 4 | Parsing Tool Calls | The model returns `computer_20241022` tool-use blocks. Parse the action type (`click`, `type`, `key`, `scroll`, `screenshot`), extract coordinates, and build a dispatcher. |
| 5 | Executing Actions | Translate parsed actions into actual OS-level input using `pyautogui` — mouse moves, clicks, keypresses, scrolling. Handle coordinate scaling if screen resolution differs from screenshot resolution. |
| 6 | The Computer Use Loop | Wire it together: capture screenshot -> send to Claude -> parse action -> execute action -> repeat. Implement stop conditions (model says "done", max iterations, error threshold). |
| 7 | Handling Failures | What goes wrong: model clicks wrong coordinates, dynamic content shifts layout, timing issues (page not loaded yet). Implement retry logic and confidence checking. |
| 8 | Running in a Container | Why production computer use runs in sandboxed VMs/containers (Docker + VNC). Brief setup of the Anthropic reference container. Security implications of giving an LLM OS-level control. |

### Putting It Together

Build a complete computer-use agent that opens a calculator application, performs a multi-step calculation (e.g., compound interest: multiply, add, store results), and reads the final answer from the screen. This exercises the full loop — launching an app, clicking buttons by visual recognition, reading displayed output, and deciding when the task is complete.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Screenshot Parser | Starter | Send a screenshot of a web page to Claude and print the structured action it would take. No execution — just parse and display the tool call. |
| 2 | Form Filler | Moderate | Build a computer-use agent that fills out a simple HTML form (name, email, submit) running on localhost. Verify the submission by reading the confirmation page. |
| 3 | Multi-Step Navigation | Moderate | Agent that opens a file manager, navigates to a specific folder, and lists the files it sees by reading the screenshot. Requires multiple sequential actions. |
| 4 | Error Recovery | Stretch | Extend the form filler to handle a form with validation errors — the agent must read the error messages, correct its input, and resubmit. |

### Key References

- [Anthropic Computer Use documentation](https://docs.anthropic.com/en/docs/agents-and-tools/computer-use) — official API reference, supported actions, best practices
- [Anthropic Computer Use blog post](https://www.anthropic.com/news/3-5-models-and-computer-use) — launch announcement explaining the approach and safety considerations
- [Anthropic Computer Use reference implementation](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo) — Docker-based demo with VNC, the reference architecture
- [pyautogui documentation](https://pyautogui.readthedocs.io/) — the library used for programmatic mouse/keyboard control
- [Pillow (PIL) documentation](https://pillow.readthedocs.io/) — screenshot capture and image manipulation
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — broader context on agent architectures (computer use is a specialized tool-use pattern)

---

## 02. Browser Agent

**File:** `02_browser_agent.ipynb`

### Overview

This notebook builds a browser agent from scratch using Playwright for browser control and an LLM for reasoning. Instead of pixel-coordinate clicking (notebook 01), you work with the DOM — Playwright gives you programmatic access to elements, navigation, and page content. You will build an agent that receives a natural-language task, reasons about the current page state, selects Playwright actions (goto, click, fill, extract), executes them, and loops until the task is complete. This is the workhorse pattern behind most practical browser automation agents.

### Learning Objectives

By the end of this notebook, you will be able to:
- Control a browser programmatically with Playwright (navigation, clicking, form filling, content extraction)
- Build an observation function that summarizes the current page state (URL, title, visible elements, text content) for the LLM
- Implement an LLM-driven action loop: the model chooses which Playwright action to take based on page observations
- Handle common browser automation challenges: waiting for elements, dealing with dynamic content, managing navigation
- Extract structured data from web pages using Playwright selectors combined with LLM reasoning
- Compare the DOM-based approach (Playwright) with the screenshot-based approach (Computer Use) and articulate when to use each

### Prerequisites

- [`01_computer_use_basics.ipynb`](./01_computer_use_basics.ipynb) — understanding the screenshot-action loop motivates why DOM-based control is often more reliable and efficient
- [`../appendix/11_async_and_await.ipynb`](../appendix/11_async_and_await.ipynb) — Playwright's Python API is async-first; you need comfortable fluency with `async`/`await` and `asyncio`

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Playwright Fundamentals | Install Playwright, launch a browser, navigate to a page, take a screenshot. Understand the Browser -> Context -> Page hierarchy. Sync vs async API (we use async throughout). |
| 2 | Selectors and Interaction | Click buttons, fill forms, select dropdowns, check boxes. Playwright's selector engine: CSS, text, role-based, and `getByRole`/`getByText` locators. Waiting strategies (`wait_for_selector`, `wait_for_load_state`). |
| 3 | Observing Page State | Build a `get_page_observation()` function: extract URL, title, visible text, interactive elements (links, buttons, inputs) with their selectors. This is what the LLM "sees" instead of a screenshot. Keep it concise to fit in the context window. |
| 4 | The Action Space | Define the actions the agent can take: `goto(url)`, `click(selector)`, `fill(selector, value)`, `extract(selector)`, `scroll(direction)`, `back()`, `wait()`, `done(answer)`. Each action maps to a Playwright method. |
| 5 | LLM-Driven Action Selection | Send the page observation + task description + action space to the LLM. Parse its response into an action call. Handle malformed responses with retry logic. Prompt engineering for reliable action selection. |
| 6 | The Browser Agent Loop | Wire it together: observe -> reason -> act -> observe. Implement the main loop with a conversation history so the LLM remembers what it has already tried. Add stop conditions (max steps, `done` action, repeated failures). |
| 7 | Data Extraction Patterns | Agent that navigates to a page and extracts structured data (e.g., product name, price, rating from an e-commerce listing). Combine Playwright's DOM extraction with LLM parsing for messy or inconsistent pages. |
| 8 | Screenshot vs DOM: When to Use Which | Side-by-side comparison: Computer Use (screenshot-based) vs Playwright (DOM-based). Tradeoffs: universality vs reliability, speed vs flexibility. Hybrid approaches that use both. |

### Putting It Together

Build a browser agent that performs a multi-step web research task: start at a search engine, search for a topic, open the top 3 results, extract key information from each page, and compile a summary. This exercises navigation, search interaction, multi-page data extraction, and synthesis — the core pattern behind research agents.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Single-Page Extractor | Starter | Agent that navigates to a Wikipedia article and extracts the first paragraph, infobox data, and a list of section headings as structured JSON. |
| 2 | Form Automation | Moderate | Agent that fills out a multi-page form (personal info -> preferences -> review -> submit), navigating between pages and verifying each step. Use a practice form site like `httpbin.org` or a local HTML form. |
| 3 | Login and Authenticated Browsing | Moderate | Agent that logs into a site (use a test account on a practice site), navigates to a protected page, and extracts data that is only visible when authenticated. Handle cookies and session state. |
| 4 | Comparison Shopper | Stretch | Agent that searches for a product on two different e-commerce sites, extracts price and ratings from each, and returns a structured comparison. Requires handling different page layouts and selectors. |

### Key References

- [Playwright for Python documentation](https://playwright.dev/python/) — official docs, the primary reference for all Playwright APIs
- [Playwright Python API reference](https://playwright.dev/python/docs/api/class-playwright) — detailed class and method documentation
- [Playwright selectors guide](https://playwright.dev/python/docs/selectors) — CSS, text, role-based, and chained selectors
- [Playwright auto-waiting](https://playwright.dev/python/docs/actionability) — how Playwright waits for elements to be actionable before interacting
- [WebArena benchmark](https://webarena.dev/) — benchmark for evaluating web agents on realistic tasks, good for understanding what browser agents should be able to do
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — general agent design patterns that apply directly to browser agents

---

## 03. Playwright MCP

**File:** `03_playwright_mcp.ipynb`

### Overview

This notebook connects browser automation to the Model Context Protocol (MCP) ecosystem by using the official Playwright MCP server from Microsoft. Instead of writing custom Playwright code, you give any MCP-compatible agent browser control through a standardized tool interface — the MCP server exposes browser actions as tools that any agent can call. You will set up the Playwright MCP server, connect to it from an agent, and build a browser-capable agent that works with any MCP-compatible framework. This is the "batteries-included" approach to browser agents and the pattern that is winning in production.

### Learning Objectives

By the end of this notebook, you will be able to:
- Explain how MCP servers expose capabilities as tools and why this matters for browser automation
- Set up and configure the official Playwright MCP server (`@playwright/mcp`)
- Connect to the Playwright MCP server from a Python client using stdio transport
- Build an agent that uses MCP-provided browser tools without writing any Playwright code directly
- Configure the MCP server's operating modes: snapshot mode (accessibility-tree-based, default) vs vision mode (screenshot-based)
- Compare the three browser-agent approaches: raw Playwright (notebook 02), MCP Playwright (this notebook), and Computer Use (notebook 01)

### Prerequisites

- [`02_browser_agent.ipynb`](./02_browser_agent.ipynb) — you need to understand what Playwright does under the hood before abstracting it behind MCP
- [`../protocols/01_mcp_from_scratch.ipynb`](../protocols/01_mcp_from_scratch.ipynb) — you need to understand MCP's architecture (client/server, tools, transports) to use the Playwright MCP server effectively

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Why MCP for Browser Control? | The problem: every framework reimplements browser tools differently. MCP standardizes it — one server, any agent. Compare bespoke Playwright wrappers vs the MCP approach. |
| 2 | The Playwright MCP Server | Install `@playwright/mcp` (Node.js package). Understand what it exposes: navigation, clicking, filling, screenshots, PDF generation, tab management, console monitoring. Walk through the tool list. |
| 3 | Server Configuration | Configure the server: headless vs headed mode, snapshot mode vs vision mode, browser selection (Chromium, Firefox, WebKit), viewport size, custom user agents. Understand the `--config` options. |
| 4 | Connecting via stdio Transport | Start the MCP server as a subprocess and connect via stdio. Send `initialize`, then `tools/list` to discover available browser tools. Build a minimal MCP client that can call browser tools. |
| 5 | Snapshot Mode Deep Dive | The default mode: the server captures an accessibility snapshot (structured representation of the page) instead of a screenshot. Understand why this is more reliable — the model gets element references (`ref="e42"`) it can use directly in actions. |
| 6 | Vision Mode Deep Dive | The alternative: the server sends screenshots. The model uses visual reasoning and coordinates (like Computer Use). When to use vision mode — visually complex pages, canvas elements, or when the accessibility tree is incomplete. |
| 7 | Building the MCP Browser Agent | Full agent loop: receive task -> list tools -> observe page (snapshot or screenshot) -> LLM picks a tool -> call tool via MCP -> observe result -> repeat. Use the MCP tool interface rather than raw Playwright code. |
| 8 | Integrating with Frameworks | Connect the Playwright MCP server to smolagents (`ToolCollection.from_mcp`) and other MCP-compatible frameworks. Show how the same server works across different agent frameworks with zero code changes. |

### Putting It Together

Build an agent that uses the Playwright MCP server to automate a realistic workflow: navigate to a documentation site, search for a specific topic, read through multiple pages, and compile a structured summary with links. Use snapshot mode for reliable element interaction and demonstrate that the agent code contains zero direct Playwright calls — all browser control flows through the MCP tool interface.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Tool Discovery | Starter | Connect to the Playwright MCP server, list all available tools, and print each tool's name, description, and parameter schema. Categorize the tools by function (navigation, interaction, observation, utility). |
| 2 | Snapshot vs Vision Comparison | Moderate | Perform the same task (navigate to a page, click a button, extract text) using both snapshot mode and vision mode. Compare the observations the model receives, the actions it takes, and the reliability of each approach. |
| 3 | Multi-Framework Agent | Moderate | Connect the same Playwright MCP server to two different agent frameworks (e.g., smolagents and a raw ReAct loop) and run the same browser task with each. Demonstrate that the MCP abstraction makes the browser tools framework-agnostic. |
| 4 | Custom MCP + Playwright Composition | Stretch | Build a custom MCP server that wraps the Playwright MCP server and adds higher-level tools (e.g., `search_and_extract(query, target_data)` that combines navigation + search + extraction into one tool call). Layer MCP servers for composable browser automation. |

### Key References

- [Playwright MCP server (GitHub)](https://github.com/microsoft/playwright-mcp) — the official Microsoft Playwright MCP server, source code and documentation
- [MCP specification](https://modelcontextprotocol.io/) — the Model Context Protocol spec, essential for understanding how tools are discovered and called
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) — Python client library for connecting to MCP servers
- [smolagents MCP integration](https://huggingface.co/docs/smolagents/en/tutorials/mcp) — how smolagents connects to MCP servers via `ToolCollection.from_mcp`
- [Playwright accessibility snapshots](https://playwright.dev/docs/accessibility-testing) — background on the accessibility tree that powers snapshot mode
- [Anthropic MCP documentation](https://docs.anthropic.com/en/docs/agents-and-tools/mcp) — Anthropic's guide to using MCP with Claude, including Claude Desktop configuration

---

## 04. Web Scraping Agent

**File:** `04_web_scraping_agent.ipynb`

### Overview

This notebook builds an agent specialized for web scraping at scale — navigating multi-page sites, extracting structured data from diverse layouts, handling pagination, dealing with authentication, and managing rate limits. While notebook 02 covered general browser control, this notebook focuses on the data extraction mission: the agent must reliably turn messy, variable web pages into clean, structured datasets. You will also explore cloud browser infrastructure (Browserbase) and AI-native scraping frameworks (Stagehand) that handle the hardest parts of browser automation — anti-bot detection, session management, and dynamic content rendering.

### Learning Objectives

By the end of this notebook, you will be able to:
- Build a scraping agent that extracts structured data from multi-page websites with varying layouts
- Implement pagination handling strategies: next-button clicking, infinite scroll detection, URL pattern generation
- Handle authenticated scraping: login flows, cookie persistence, session management across pages
- Use Browserbase for cloud-hosted browser sessions that bypass anti-bot protections and scale horizontally
- Use Stagehand's AI-native selectors (`act`, `extract`, `observe`) for resilient scraping that adapts to layout changes
- Design a data extraction pipeline: define schema -> navigate -> extract -> validate -> store, with retry and error recovery

### Prerequisites

- [`02_browser_agent.ipynb`](./02_browser_agent.ipynb) — you need Playwright fundamentals and the browser agent loop pattern before building a specialized scraping agent
- [`../core/04_structured_output.ipynb`](../core/04_structured_output.ipynb) — extracted data must conform to schemas; you need structured output techniques for reliable data shaping

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Scraping Agent Architecture | How a scraping agent differs from a general browser agent: task is data extraction, success is structured output matching a schema. Design the architecture: schema definition -> navigation strategy -> extraction -> validation -> storage. |
| 2 | Defining Extraction Schemas | Define what data you want using Pydantic models or JSON schemas. The schema drives the agent's extraction behavior. Examples: product listings (name, price, rating, URL), job postings (title, company, salary, location), article metadata (title, author, date, content). |
| 3 | Multi-Page Navigation | Agent that follows links across a site: list pages -> detail pages -> related pages. Implement a crawl strategy: BFS (breadth-first, stay shallow), DFS (depth-first, follow deep), or targeted (follow only links matching a pattern). Track visited URLs to avoid loops. |
| 4 | Pagination Strategies | Handle the three pagination patterns: (1) "Next" button clicking, (2) infinite scroll (detect and trigger scroll, wait for new content, detect end-of-list), (3) URL pattern generation (`?page=1`, `?page=2`, ...). The LLM identifies which pattern a site uses and adapts. |
| 5 | Authenticated Scraping | Login flows: agent fills credentials, submits, verifies login success. Persist cookies across pages and sessions. Handle session expiry and re-authentication. Security: load credentials from environment variables, never hardcode them. |
| 6 | Cloud Browsers with Browserbase | Why local browsers fail at scale: anti-bot detection, CAPTCHAs, IP blocking, resource limits. Browserbase provides cloud-hosted, fingerprint-managed browsers. Connect via the Browserbase API, run scraping sessions remotely, retrieve results. |
| 7 | AI-Native Scraping with Stagehand | Stagehand's paradigm shift: instead of CSS selectors, use natural-language instructions. `act("click the next page button")`, `extract("get the product name and price")`, `observe("what interactive elements are on this page?")`. Build a scraping agent that uses Stagehand's AI-native API for resilient extraction that survives layout changes. |
| 8 | Validation, Storage, and Error Recovery | Validate extracted data against the schema (reject incomplete records, flag anomalies). Store results to JSON, CSV, or SQLite. Handle extraction failures: retry the page, try alternative selectors, skip and log. Build a pipeline that is robust to partial failures. |

### Putting It Together

Build a complete scraping pipeline that extracts structured data from a multi-page listing site (e.g., a public directory, a book catalog, or a job board). The agent should: (1) navigate to the listing page, (2) extract data from each item on the current page, (3) handle pagination to process all pages, (4) validate each extracted record against a Pydantic schema, (5) store valid records to a JSON file, and (6) produce a summary report (total pages scraped, records extracted, records failed validation). Run the same pipeline once with raw Playwright and once with Stagehand to compare reliability and code complexity.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Single-Page Extractor | Starter | Define a Pydantic schema for book data (title, author, price, rating). Build an agent that extracts all books from a single page of [Books to Scrape](http://books.toscrape.com/) and validates them against the schema. |
| 2 | Paginated Scraper | Moderate | Extend Exercise 1 to handle all 50 pages. The agent should detect the "next" button, navigate through every page, and extract all 1000 books. Track progress and handle any failed pages with retries. |
| 3 | Multi-Site Comparison | Moderate | Build a scraping agent that extracts the same type of data (e.g., article titles and dates) from two sites with completely different layouts. Use LLM reasoning to adapt the extraction strategy per site without changing the schema or agent code. |
| 4 | Resilient Production Pipeline | Stretch | Build a scraping pipeline with: (a) cloud browser via Browserbase, (b) Stagehand for AI-native extraction, (c) Pydantic validation, (d) SQLite storage, (e) retry logic with exponential backoff, (f) a summary report. Test it against a site with dynamic content and rate limiting. |

### Key References

- [Browserbase documentation](https://www.browserbase.com/) — cloud browser infrastructure for scraping and automation at scale
- [Stagehand GitHub](https://github.com/browserbase/stagehand) — AI-native browser automation framework: act, extract, observe
- [Stagehand Python SDK](https://github.com/browserbase/stagehand-python) — Python bindings for Stagehand's AI-native browser automation
- [Books to Scrape](http://books.toscrape.com/) — practice site for web scraping exercises (safe, designed for learning)
- [Pydantic documentation](https://docs.pydantic.dev/) — data validation library used for extraction schemas
- [Playwright network interception](https://playwright.dev/python/docs/network) — intercept and modify network requests, useful for handling API-driven pages
- [Browserbase session management](https://docs.browserbase.com/) — managing browser sessions, fingerprinting, and proxy configuration in the cloud
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — agent design patterns applicable to scraping agents (retry, escalation, validation)
