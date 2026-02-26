# Safety & Guardrails — Lesson Plans

> Detailed lesson plans for notebooks 01–06. Production agents MUST have safety rails. The OWASP Agentic Top 10 defines the threat landscape.
> For the full track overview, see [`../roadmap.md`](../roadmap.md).

---

## 01. Input Validation

**File:** `01_input_validation.ipynb`

### Overview
This notebook teaches you to treat every user input as untrusted. You will build a layered input validation pipeline — from basic sanitization and length checks through regex-based pattern detection to an LLM-powered prompt injection classifier. Input validation is the first and most critical line of defense for any agent that accepts natural language input, because a compromised prompt means a compromised agent.

### Learning Objectives
By the end of this notebook, you will be able to:
- Sanitize raw user input (strip control characters, enforce length limits, normalize Unicode)
- Detect common prompt injection patterns using heuristic rules and regex
- Build an LLM-based prompt injection classifier that scores inputs for manipulation attempts
- Validate tool arguments against JSON schemas before execution
- Implement a layered validation pipeline that combines fast heuristic checks with slower LLM-based analysis
- Explain the difference between direct and indirect prompt injection and why each matters for agents

### Prerequisites
- [`../core/05_react_agent.ipynb`](../core/05_react_agent.ipynb) — Understanding the full agent loop that input validation protects
- [`../core/03_tool_use_from_scratch.ipynb`](../core/03_tool_use_from_scratch.ipynb) — Tool calling and argument parsing (which we validate here)
- [`../appendix/04_strings_and_json.ipynb`](../appendix/04_strings_and_json.ipynb) — String methods, regex, and JSON schema validation

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Why Input Validation Matters for Agents | Survey of real prompt injection attacks against agents — goal hijacking, data exfiltration through tool calls, indirect injection via retrieved documents |
| 2 | Basic Sanitization | Strip control characters, normalize whitespace, enforce max length, reject null/empty input. Build a `sanitize_input()` function |
| 3 | Heuristic Injection Detection | Regex patterns for common injection phrases ("ignore previous instructions", "system prompt:", role-switching attempts). Build a `HeuristicInjectionDetector` class |
| 4 | LLM-Based Injection Classification | Use a secondary LLM call to classify whether an input is attempting manipulation. Design the classification prompt, parse confidence scores, set thresholds |
| 5 | Tool Argument Validation | Validate tool arguments against JSON schemas before execution — type checking, range constraints, allowlisted values. Reject malformed or suspicious arguments |
| 6 | Layered Validation Pipeline | Combine sanitization, heuristic checks, and LLM classification into a single `InputValidator` pipeline with configurable strictness levels (permissive, standard, strict) |
| 7 | Indirect Prompt Injection | Demonstrate how injected instructions in retrieved documents or tool outputs can hijack agents. Build defenses: content tagging, instruction hierarchy, delimiter enforcement |
| 8 | Integrating with the Agent Loop | Wire the `InputValidator` into the ReAct agent from Core 05. Show how validation happens before and during the loop (user input + tool outputs) |

### Putting It Together
Build a complete `InputValidator` class that accepts raw user input, runs it through sanitization, heuristic detection, and LLM classification, then returns a validated input or a rejection with explanation. Integrate it into the ReAct agent loop so that both user messages and tool return values pass through validation before the LLM processes them.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Add Unicode Normalization | Starter | Extend `sanitize_input()` to handle Unicode homoglyph attacks (e.g., Cyrillic "а" vs Latin "a") |
| 2 | Custom Injection Patterns | Moderate | Add 5 new regex patterns for injection techniques not covered in the notebook (e.g., base64-encoded instructions, markdown link injection) |
| 3 | Threshold Tuning | Moderate | Build a small test set of 20 benign and 20 malicious inputs. Tune the LLM classifier threshold to minimize false positives while catching all injections |
| 4 | Adversarial Red-Teaming | Stretch | Try to bypass your own validation pipeline. Document 3 successful bypass techniques and then patch each one |

### Key References
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — The canonical list of LLM vulnerabilities; prompt injection is #1
- [Simon Willison — Prompt Injection](https://simonwillison.net/series/prompt-injection/) — The best ongoing coverage of prompt injection research and real-world exploits
- [Anthropic — Guardrails](https://docs.anthropic.com/en/docs/build-with-claude/guardrails) — Official guidance on input screening, harmlessness screens, and known-attack detection
- [Lakera — Prompt Injection Guide](https://www.lakera.ai/blog/guide-to-prompt-injection) — Practical taxonomy of injection types with examples
- [Rebuff — Prompt Injection Detection](https://github.com/protectai/rebuff) — Open-source multi-layered prompt injection detection framework
- [NIST AI 100-2e2023 — Adversarial ML](https://csrc.nist.gov/pubs/ai/100/2/e2023/final) — Formal taxonomy of adversarial attacks on ML systems including LLMs

---

## 02. Output Filtering

**File:** `02_output_filtering.ipynb`

### Overview
This notebook teaches you to validate and filter everything an agent says before it reaches the user. You will build a content filtering pipeline that catches harmful content, detects and redacts PII (personally identifiable information), and validates that responses conform to expected schemas and policies. Output filtering is the complement to input validation — even with perfect input handling, a compromised or hallucinating LLM can produce dangerous, leaky, or off-policy responses.

### Learning Objectives
By the end of this notebook, you will be able to:
- Build regex-based content filters that detect and block harmful or off-topic output
- Implement PII detection and redaction for common entity types (emails, phone numbers, SSNs, credit card numbers, names)
- Use Microsoft Presidio for production-grade PII detection with configurable confidence thresholds
- Validate agent responses against structural schemas (JSON shape, required fields, value constraints)
- Build policy-based output filters (topic guardrails, tone enforcement, factual grounding checks)
- Chain multiple filters into an `OutputFilter` pipeline with fail-open vs fail-closed modes

### Prerequisites
- [`01_input_validation.ipynb`](01_input_validation.ipynb) — Understanding the layered validation pattern we extend here to outputs
- [`../appendix/04_strings_and_json.ipynb`](../appendix/04_strings_and_json.ipynb) — Regex, string manipulation, and JSON parsing

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Why Output Filtering Matters | Examples of agent output failures: leaking system prompts, exposing PII from retrieval context, generating harmful instructions, hallucinating tool outputs |
| 2 | Content Safety Filters | Keyword and regex-based toxicity detection. Build a `ContentFilter` that flags or blocks outputs containing harmful content categories |
| 3 | PII Detection from Scratch | Regex patterns for emails, phone numbers, SSNs, credit cards, IP addresses. Build a `PIIDetector` class that returns entity spans and types |
| 4 | PII Detection with Presidio | Install and configure Microsoft Presidio. Use its `AnalyzerEngine` and `AnonymizerEngine` for production-grade PII detection and redaction with confidence scores |
| 5 | Response Schema Validation | Validate that agent responses match expected schemas — required fields present, types correct, values within allowed ranges. Build a `ResponseValidator` |
| 6 | Policy-Based Filtering | Define output policies (allowed topics, required disclaimers, tone constraints). Use an LLM-as-judge call to check policy compliance |
| 7 | Building the Output Pipeline | Chain `ContentFilter`, `PIIDetector`, `ResponseValidator`, and policy checks into an `OutputFilter` pipeline. Configure fail-open (warn but pass) vs fail-closed (block and retry) behavior |
| 8 | Retry and Fallback Strategies | When output is rejected: retry with a modified prompt, return a safe fallback response, or escalate. Build a retry loop with backoff |

### Putting It Together
Build a complete `OutputFilter` class that receives raw LLM output and runs it through content safety, PII redaction, schema validation, and policy compliance checks. Integrate it with the agent loop so that every response — including intermediate tool-calling steps — is filtered before the user sees it. Demonstrate both fail-open (log and warn) and fail-closed (block and regenerate) modes.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Add Custom PII Entity Types | Starter | Extend the regex-based PII detector to catch passport numbers and IBAN bank account numbers |
| 2 | Presidio Custom Recognizer | Moderate | Build a custom Presidio recognizer for a domain-specific entity (e.g., internal project codes matching a pattern like `PROJ-\d{4}`) |
| 3 | LLM-as-Judge Output Filter | Moderate | Replace the keyword-based content filter with an LLM-based classifier that evaluates outputs against a rubric of safety criteria |
| 4 | Adversarial Output Testing | Stretch | Craft 10 prompts designed to make the agent leak its system prompt, produce PII, or violate output policies. Verify your filters catch all 10 |

### Key References
- [Anthropic — Guardrails](https://docs.anthropic.com/en/docs/build-with-claude/guardrails) — Official guidance on output validation, content filtering, and LLM-as-judge screening
- [Microsoft Presidio](https://microsoft.github.io/presidio/) — Open-source PII detection and anonymization framework with support for 50+ entity types
- [OWASP LLM Top 10 — Sensitive Information Disclosure](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — LLM06 covers unintended information leakage
- [Guardrails AI](https://www.guardrailsai.com/) — Open-source framework for adding structural and semantic validation to LLM outputs
- [NeMo Guardrails (NVIDIA)](https://github.com/NVIDIA/NeMo-Guardrails) — Programmable guardrails for LLM-based applications with dialog management

---

## 03. Sandboxing and Permissions

**File:** `03_sandboxing_and_permissions.ipynb`

### Overview
This notebook teaches you to contain the blast radius when agents execute code or call external tools. You will build sandboxed execution environments using Docker and E2B, implement a permission model that gates tool access based on user roles and request context, and add rate limiting to prevent runaway agents. Any agent that can execute code or make HTTP requests is one bad prompt away from disaster without proper sandboxing.

### Learning Objectives
By the end of this notebook, you will be able to:
- Explain the security risks of unsandboxed code execution in agents (file system access, network exfiltration, resource exhaustion)
- Run agent-generated code inside a Docker container with restricted capabilities
- Use E2B sandboxes for secure remote code execution with built-in isolation
- Design a permission model with role-based access control (RBAC) for tool access
- Implement per-user and per-tool rate limiting to prevent abuse and runaway loops
- Build a `PermissionManager` that enforces least-privilege tool access at runtime

### Prerequisites
- [`../core/08_code_agent_deep_dive.ipynb`](../core/08_code_agent_deep_dive.ipynb) — CodeAgent execution model and why sandboxing matters
- [`01_input_validation.ipynb`](01_input_validation.ipynb) — Input validation as the first layer; sandboxing is the second

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | The Case for Sandboxing | Demonstrate what an unsandboxed CodeAgent can do: read `/etc/passwd`, write arbitrary files, make network requests, fork-bomb. Motivate containment |
| 2 | Docker-Based Sandboxing | Use the Docker SDK for Python to spin up ephemeral containers for code execution. Configure resource limits (CPU, memory, network), mount read-only volumes, set timeouts |
| 3 | E2B Cloud Sandboxes | Use E2B's `Sandbox` class for zero-config remote code execution. Compare cold start times, supported languages, and persistence vs Docker |
| 4 | smolagents Sandboxing Options | Configure smolagents' built-in sandboxing: `LocalPythonExecutor` vs `E2BSandbox` vs `DockerSandbox`. Understand `additional_authorized_imports` as an allowlist |
| 5 | Permission Models | Design a permission model: define tool categories (read-only, write, network, code-execution), user roles (viewer, operator, admin), and map roles to allowed tool categories |
| 6 | Building a PermissionManager | Implement `PermissionManager` with `check_permission(user, tool, args)` that enforces RBAC. Add argument-level restrictions (e.g., file tools can only access `/data/`) |
| 7 | Rate Limiting | Implement token-bucket rate limiting per user and per tool. Prevent runaway agent loops from burning API credits or making unlimited external requests |
| 8 | Wiring It All Together | Integrate `PermissionManager` and rate limiting into the agent loop. Every tool call checks permissions and rate limits before execution; code runs in a sandbox |

### Putting It Together
Build a secured agent runtime that wraps every tool invocation in three checks: (1) does this user have permission to call this tool with these arguments, (2) has this user/tool exceeded its rate limit, and (3) if the tool involves code execution, run it inside a Docker or E2B sandbox. Demonstrate the complete flow with a CodeAgent that attempts both allowed and forbidden operations.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Docker Resource Limits | Starter | Configure a Docker sandbox with a 50MB memory limit and 5-second timeout. Verify it kills a memory-hogging script |
| 2 | Custom Permission Policy | Moderate | Define a `researcher` role that can use search and read tools but not code execution or file write tools. Test enforcement with 5 tool calls |
| 3 | Dynamic Permission Escalation | Moderate | Implement a flow where an agent requests elevated permissions, a human approves or denies, and the permission is granted for a single tool call |
| 4 | Escape the Sandbox | Stretch | Research 3 known Docker escape techniques. Verify that your container configuration mitigates each one. Document your findings |

### Key References
- [E2B Documentation](https://e2b.dev/docs) — Cloud sandboxes purpose-built for AI code execution with Python SDK
- [Docker SDK for Python](https://docker-py.readthedocs.io/) — Programmatic Docker container management for building custom sandboxes
- [smolagents — Sandboxed Execution](https://huggingface.co/docs/smolagents/tutorials/secure_code_execution) — smolagents' built-in sandboxing options and configuration
- [gVisor](https://gvisor.dev/) — Google's container sandbox runtime for defense-in-depth (used by E2B under the hood)
- [OWASP — Improper Output Handling](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — LLM05 covers risks when LLM output is passed to downstream systems without validation
- [Principle of Least Privilege (NIST)](https://csrc.nist.gov/glossary/term/least_privilege) — The foundational security principle behind permission models

---

## 04. OWASP Agentic Top 10

**File:** `04_owasp_agentic_top_10.ipynb`

### Overview
This notebook walks through all 10 attack vectors from the OWASP Top 10 for Agentic Applications. For each vector, you will understand the threat model, see a concrete exploit demonstration against a sample agent, and build a targeted mitigation. This is the conceptual backbone of the safety track — it maps the full threat landscape that the other notebooks address piecemeal.

### Learning Objectives
By the end of this notebook, you will be able to:
- Name and explain all 10 OWASP Agentic Top 10 attack categories with concrete examples
- Demonstrate at least 5 of the 10 attack vectors against a sample multi-tool agent
- Map each attack vector to the appropriate mitigation strategy (input validation, output filtering, sandboxing, auth, governance)
- Assess an existing agent system for agentic security vulnerabilities using a threat-modeling checklist
- Explain the difference between the OWASP LLM Top 10 (model-level) and the OWASP Agentic Top 10 (system-level)
- Design a defense-in-depth strategy that layers multiple mitigations

### Prerequisites
- [`01_input_validation.ipynb`](01_input_validation.ipynb) — Input validation mitigations referenced throughout
- [`02_output_filtering.ipynb`](02_output_filtering.ipynb) — Output filtering mitigations referenced throughout
- [`03_sandboxing_and_permissions.ipynb`](03_sandboxing_and_permissions.ipynb) — Sandboxing and permission mitigations referenced throughout

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | LLM Top 10 vs Agentic Top 10 | Understand the difference: LLM Top 10 covers model vulnerabilities (prompt injection, training data poisoning); Agentic Top 10 covers system-level risks when LLMs have tools, memory, and autonomy |
| 2 | Excessive Agency | When agents have more permissions than needed. Demo: agent with unrestricted file-system tool deletes critical files. Mitigation: least-privilege tool design, argument constraints |
| 3 | Unrestricted Resource Access | When agents access data or APIs without proper authorization. Demo: agent reads environment variables and exfiltrates API keys. Mitigation: sandboxing, credential isolation |
| 4 | Insecure Tool/Function Design | When tools are built without security considerations. Demo: SQL injection through a poorly designed database tool. Mitigation: parameterized queries, input validation on tool arguments |
| 5 | Inadequate Multi-Agent Trust | When agents trust each other's outputs without verification. Demo: a compromised sub-agent returns manipulated data to the orchestrator. Mitigation: output validation between agents, signed messages |
| 6 | Identity and Access Mismanagement | When agent identity and user identity are conflated. Demo: agent uses its own elevated credentials for user-scoped requests. Mitigation: brokered auth, per-user credential scoping |
| 7 | Insufficient Agent Autonomy Controls | When agents can act without human oversight on high-impact operations. Demo: agent autonomously sends emails and makes purchases. Mitigation: mandatory human approval for high-impact actions |
| 8 | Knowledge Poisoning & Memory Manipulation | When agent memory or knowledge base is compromised. Demo: injecting false "memories" that alter future behavior. Mitigation: memory integrity checks, source attribution |
| 9 | Goal Hijacking & Rogue Agents | When an agent's objective is manipulated mid-task. Demo: indirect prompt injection in a web page redirects the research agent to a different goal. Mitigation: goal anchoring, progress validation |
| 10 | Unmonitored Agent Activity & Logging Gaps | When agent actions are not logged or auditable. Demo: agent makes 100+ tool calls with no trace. Mitigation: structured logging, audit trails, anomaly detection |
| 11 | Threat Modeling Checklist | Build a reusable checklist that maps each attack vector to questions, detection methods, and mitigations for assessing any agent system |

### Putting It Together
Build a threat model for a realistic multi-tool research agent (web search, file read/write, code execution, email sending). Walk through the checklist, identify the 5 highest-risk vectors for that specific agent, and implement targeted mitigations for each. Produce a one-page security assessment document.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Classify Existing Defenses | Starter | Take the `InputValidator` from notebook 01 and the `OutputFilter` from notebook 02. Map each component to the OWASP Agentic Top 10 categories it mitigates |
| 2 | Red Team a Multi-Tool Agent | Moderate | Given a sample agent with 4 tools (search, calculator, file reader, code runner), attempt to exploit 3 different OWASP categories. Document attack and result |
| 3 | Defense-in-Depth Design | Moderate | Design a layered mitigation strategy for a customer-support agent. For each OWASP category, specify which layer (input, tool, output, governance) handles it |
| 4 | Multi-Agent Trust Protocol | Stretch | Design and implement a simple message-signing protocol between two agents so the orchestrator can verify a sub-agent's response has not been tampered with |

### Key References
- [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) — The definitive reference: all 10 categories with examples, risk ratings, and mitigations
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — The model-level companion; covers prompt injection, training data poisoning, insecure output handling
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — Anthropic's agent design principles, including safety-by-design patterns
- [Simon Willison — Prompt Injection](https://simonwillison.net/series/prompt-injection/) — Ongoing real-world prompt injection coverage relevant to attack vectors 2 and 9
- [MITRE ATLAS](https://atlas.mitre.org/) — Adversarial threat landscape for AI systems — formal attack taxonomy
- [NIST AI Risk Management Framework](https://www.nist.gov/artificial-intelligence/executive-order-safe-secure-and-trustworthy-artificial-intelligence) — Federal guidance on AI risk assessment applicable to agent systems

---

## 05. Agent Authentication

**File:** `05_agent_authentication.ipynb`

### Overview
This notebook teaches you how agents should handle credentials and authenticate with external services. You will implement the brokered credential pattern (where the LLM never sees API keys), build OAuth 2.1 flows with PKCE for agent-initiated authentication, manage ephemeral scoped tokens, and integrate with MCP's authorization specification. Credential management is one of the most dangerous aspects of agent systems — a single leaked API key in a prompt can compromise an entire organization.

### Learning Objectives
By the end of this notebook, you will be able to:
- Explain why agents must never have direct access to long-lived credentials
- Implement the brokered credential pattern where a middleware layer injects credentials into tool calls
- Build an OAuth 2.1 authorization code flow with PKCE for agent-to-service authentication
- Generate and manage ephemeral, scoped tokens that expire after a single use or short TTL
- Integrate MCP's authorization specification for tool-server authentication
- Design a credential vault architecture that separates agent logic from secret storage

### Prerequisites
- [`01_input_validation.ipynb`](01_input_validation.ipynb) — Input validation fundamentals that apply to auth token handling
- [`../appendix/06_http_and_apis.ipynb`](../appendix/06_http_and_apis.ipynb) — HTTP fundamentals, headers, and API authentication patterns
- [`../protocols/01_mcp_from_scratch.ipynb`](../protocols/01_mcp_from_scratch.ipynb) — MCP protocol structure (for MCP auth integration)

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | The Credential Problem | Why agents + credentials = danger. Demonstrate: LLM leaks an API key through prompt, tool call exposes bearer token in logs, agent stores credentials in conversation memory |
| 2 | Brokered Credentials Pattern | Build a `CredentialBroker` middleware that intercepts tool calls, injects the required credentials from a secure vault, and strips them from the response before the LLM sees it |
| 3 | OAuth 2.1 Primer for Agents | OAuth 2.1 fundamentals: authorization code grant, PKCE (Proof Key for Code Exchange), scopes, token exchange. Why OAuth 2.1 replaces implicit grant and why PKCE is mandatory |
| 4 | Implementing PKCE Flow | Build a complete PKCE flow: generate code verifier and challenge, redirect user to authorization endpoint, handle callback, exchange code for tokens. Use httpx for all HTTP calls |
| 5 | Ephemeral Token Management | Generate scoped tokens with short TTLs (5 minutes), single-use constraints, and minimum necessary scopes. Build a `TokenManager` that mints, validates, and revokes tokens |
| 6 | MCP Authorization Integration | Implement MCP's auth spec: client registration, token exchange, scope negotiation between agent and MCP server. Show how MCP servers can require per-tool authorization |
| 7 | Credential Vault Architecture | Design a vault-backed credential system: secrets stored in environment variables or a vault service (HashiCorp Vault, AWS Secrets Manager), never in code, prompts, or agent memory |
| 8 | Audit and Rotation | Log every credential use (who, when, which tool, which scope). Implement automatic credential rotation and revocation on suspected compromise |

### Putting It Together
Build a complete credential management system for a multi-tool agent. The agent calls three external APIs (a search API, a database API, and an email API), each requiring different credentials. The `CredentialBroker` injects credentials at call time, the `TokenManager` handles ephemeral tokens for the database API's OAuth flow, and an audit log records every credential use. At no point does the LLM see any credential.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Credential Leak Detection | Starter | Build a regex-based scanner that checks LLM prompts and responses for accidentally-included API keys, bearer tokens, and passwords |
| 2 | Scoped Token Generator | Moderate | Implement a `TokenManager` that generates JWT tokens with custom claims (tool name, allowed operations, expiry). Validate tokens before each tool call |
| 3 | MCP Auth Server | Moderate | Build a minimal MCP server that requires OAuth token exchange before exposing its tools. Test with an MCP client that negotiates auth |
| 4 | Full Vault Integration | Stretch | Integrate with a local HashiCorp Vault dev server. Store 3 API keys in Vault, build a `VaultBroker` that fetches them at runtime, and verify zero credentials in agent memory |

### Key References
- [OAuth 2.1 for Agents (Descope)](https://www.descope.com/blog/post/oauth-vs-api-keys) — Practical guide to why agents need OAuth 2.1 and how brokered credentials work
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization) — The official MCP auth spec: client registration, token exchange, scope negotiation
- [OAuth 2.1 Draft (IETF)](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-12) — The IETF specification for OAuth 2.1, consolidating best practices from OAuth 2.0 extensions
- [OWASP — Identity and Access Mismanagement](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) — OWASP Agentic category covering credential mismanagement in agent systems
- [HashiCorp Vault](https://www.vaultproject.io/) — Industry-standard secrets management for production credential storage
- [Anthropic — Tool Use Security](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview) — Anthropic's guidance on secure tool integration patterns

---

## 06. Governance and Least Agency

**File:** `06_governance_and_least_agency.ipynb`

### Overview
This notebook teaches you to design agents that do the minimum necessary and always have a human in the loop for high-stakes decisions. You will build bounded autonomy controls, mandatory escalation paths, structured audit trails, and compliance patterns that ensure agents remain accountable and governable. This is the capstone of the safety track — it ties together everything from input validation to authentication into a coherent governance framework.

### Learning Objectives
By the end of this notebook, you will be able to:
- Apply the principle of least agency: agents should request only the permissions they need and prefer asking for confirmation over acting autonomously
- Implement mandatory human-in-the-loop escalation for high-risk tool calls based on configurable risk thresholds
- Build structured audit trails that log every agent decision, tool call, and outcome for post-hoc review
- Design bounded autonomy policies that limit agent actions per session (max tool calls, max cost, allowed tool set)
- Create compliance patterns for regulated domains (financial, healthcare, legal) where agent actions have legal implications
- Evaluate agent governance maturity using a rubric and recommend improvements

### Prerequisites
- [`01_input_validation.ipynb`](01_input_validation.ipynb) — Input validation as part of the governance stack
- [`02_output_filtering.ipynb`](02_output_filtering.ipynb) — Output filtering as part of the governance stack
- [`03_sandboxing_and_permissions.ipynb`](03_sandboxing_and_permissions.ipynb) — Permission models that governance policies build on
- [`04_owasp_agentic_top_10.ipynb`](04_owasp_agentic_top_10.ipynb) — The threat landscape that governance addresses holistically
- [`05_agent_authentication.ipynb`](05_agent_authentication.ipynb) — Credential management and audit trails

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | The Principle of Least Agency | Anthropic's formulation: "give agents the minimum footprint for the task." Compare maximally-autonomous vs minimally-autonomous agent designs for the same task. Show how less agency often produces better outcomes |
| 2 | Bounded Autonomy Policies | Define `AgentPolicy` objects: max tool calls per turn, max total cost, allowed tool set, forbidden actions. Build a `PolicyEnforcer` that wraps the agent loop and enforces limits |
| 3 | Risk Classification for Tool Calls | Classify tools and actions by risk tier (low: read-only lookups; medium: data writes; high: external communications, financial transactions). Build a `RiskClassifier` that evaluates each tool call |
| 4 | Human-in-the-Loop Escalation | Build an `EscalationManager` that pauses agent execution when a high-risk action is detected, presents the proposed action to a human, and proceeds only with approval. Support approve, deny, and modify responses |
| 5 | Structured Audit Trails | Design an audit log schema: timestamp, session ID, user ID, agent action, tool name, arguments, result, risk level, approval status. Build an `AuditLogger` that writes structured JSON logs for every agent step |
| 6 | Compliance Patterns | Templates for regulated domains: (a) financial — pre-trade compliance checks and transaction limits, (b) healthcare — PHI access logging and minimum necessary standard, (c) legal — privilege preservation and disclosure controls |
| 7 | Governance Dashboard | Build a simple analysis tool that reads audit logs and produces governance metrics: actions per session, escalation rate, denial rate, policy violations, cost per session |
| 8 | The Complete Governance Stack | Wire together `InputValidator`, `OutputFilter`, `PermissionManager`, `CredentialBroker`, `PolicyEnforcer`, `EscalationManager`, and `AuditLogger` into a single governed agent runtime. Show the full lifecycle of a request |

### Putting It Together
Build a fully governed agent that handles a realistic scenario: a customer-support agent with access to user account data, a knowledge base, and an email-sending tool. The agent operates under a policy that allows autonomous read-only lookups, requires human approval for account modifications, and blocks direct access to financial data. Every action is logged. The governance dashboard shows the session's risk profile, escalation events, and total actions.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Define a Least-Agency Policy | Starter | Write an `AgentPolicy` for a research agent that can search the web and read files but cannot write files, execute code, or send emails. Test that the enforcer blocks forbidden actions |
| 2 | Build an Escalation Flow | Moderate | Implement a complete escalation flow: agent proposes a high-risk action, `EscalationManager` pauses execution, a simulated human reviews and approves/denies, agent proceeds or falls back |
| 3 | Audit Log Analysis | Moderate | Given a sample audit log with 50 entries, write analysis code that identifies: (a) the most frequently used tools, (b) the highest-risk actions taken, (c) any policy violations |
| 4 | Governance Maturity Assessment | Stretch | Design a 5-level governance maturity rubric (ad-hoc, basic, managed, measured, optimized). Assess the governed agent you built in this notebook against the rubric. Identify 3 improvements to reach the next level |

### Key References
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — The canonical source on least agency: "maintain the smallest footprint of agency needed to complete the task"
- [Microsoft AI Agent Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) — Enterprise governance patterns including human-in-the-loop, monitoring, and bounded autonomy
- [OWASP — Insufficient Agent Autonomy Controls](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) — OWASP Agentic category covering governance gaps
- [NIST AI Risk Management Framework](https://www.nist.gov/artificial-intelligence/executive-order-safe-secure-and-trustworthy-artificial-intelligence) — Federal framework for managing AI risk, applicable to agent governance
- [EU AI Act — High-Risk AI Systems](https://artificialintelligenceact.eu/) — Regulatory requirements for AI systems in the EU, including transparency and human oversight mandates
- [ISO/IEC 42001 — AI Management System](https://www.iso.org/standard/81230.html) — International standard for establishing and maintaining AI governance
- [Anthropic — Responsible Scaling Policy](https://www.anthropic.com/research/responsible-scaling-policy) — How Anthropic thinks about AI safety governance at the organizational level
