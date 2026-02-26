# Agent Memory & Knowledge Infrastructure — Lesson Plans

> Detailed lesson plans for notebooks 01–05. Production memory is far more complex than basic RAG — hybrid storage, knowledge graphs, temporal memory, and personalization.
> For the full track overview, see [`../roadmap.md`](../roadmap.md).

---

## 01. Memory Architectures

**File:** `01_memory_architectures.ipynb`

### Overview

This notebook surveys the major memory architecture patterns used by production agent systems — Letta's OS-inspired hierarchy (core/recall/archival memory), Mem0's hybrid datastore, and Zep's episodic memory engine. You will implement simplified versions of each pattern in raw Python, compare their tradeoffs, and understand when each design fits. This is the conceptual foundation for everything else in the memory track: before you build production memory, you need a mental model of how the design space is structured.

### Learning Objectives

By the end of this notebook, you will be able to:
- Explain the difference between working memory, episodic memory, semantic memory, and procedural memory in the context of AI agents
- Diagram Letta's three-tier memory hierarchy (core/recall/archival) and describe the role of each tier
- Implement a minimal core-memory system with in-context read/write operations driven by agent tool calls
- Compare the Mem0 hybrid-store approach (vector + key-value + graph) against Letta's tiered model on the same retrieval tasks
- Describe how Zep models episodic memory as a temporal knowledge graph and why this matters for multi-session agents
- Evaluate which memory architecture fits a given agent use case (single-session assistant vs. long-running personal agent vs. multi-user system)

### Prerequisites

- [`../core/12_conversation_memory.ipynb`](../core/12_conversation_memory.ipynb) — understanding of basic conversation buffers, sliding windows, and summary memory
- [`../core/13_rag_from_scratch.ipynb`](../core/13_rag_from_scratch.ipynb) — familiarity with embedding, retrieval, and augmented generation

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Why RAG Is Not Memory | Distinguish retrieval (stateless, query-time) from memory (stateful, evolving). Show failure cases where naive RAG breaks down: contradictory facts over time, user preference drift, relationship tracking. |
| 2 | Human Memory as a Design Blueprint | Map cognitive science categories (working, episodic, semantic, procedural) to agent design. Build a simple `MemoryStore` base class with `read`, `write`, `search`, and `forget` interfaces. |
| 3 | Letta (MemGPT) — OS-Inspired Memory | Implement Letta's three-tier model: core memory (in-context, editable blocks), recall memory (conversation log database), archival memory (vector-indexed long-term store). Build a `LettaMemory` class that pages data between tiers. |
| 4 | The Self-Editing Memory Pattern | Implement the key MemGPT insight: the agent itself decides what to write to and evict from core memory using tool calls (`core_memory_append`, `core_memory_replace`, `archival_memory_insert`, `archival_memory_search`). Wire these as tools in a simple agent loop. |
| 5 | Mem0 — Hybrid Datastore | Implement Mem0's approach: extract "memory items" from conversations using an LLM, store them in a flat hybrid store (vector similarity + key-value metadata + optional graph edges). Compare retrieval quality against the Letta model on the same test conversations. |
| 6 | Zep — Episodic Memory and Temporal Knowledge | Implement Zep's episode-centric model: conversations become episodes, facts are extracted into a temporal knowledge graph, entity summaries are maintained. Show how this handles "what did the user say last week about X?" queries. |
| 7 | Architecture Comparison Matrix | Build a comparison table across dimensions: latency, storage cost, query expressiveness, temporal reasoning, multi-user support, implementation complexity. Run the same 10 test queries across all three implementations and compare results. |
| 8 | Choosing an Architecture | Decision framework: map use cases (chatbot, personal assistant, customer support, research agent) to architecture choices. Discuss hybrid approaches that combine elements from multiple systems. |

### Putting It Together

Build a `MemoryBenchmark` harness that takes a synthetic conversation log (20+ turns with preference changes, factual updates, and temporal references) and evaluates each of the three architectures on retrieval accuracy, factual consistency, and temporal awareness. Present results in a comparison table and write up which architecture you would choose for a personal learning assistant and why.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Add `forget` to Letta Memory | Starter | Implement a `core_memory_delete` tool that removes a specific block from core memory and observe how the agent's behavior changes when key context is evicted. |
| 2 | Memory Conflict Resolution | Moderate | Given two contradictory facts stored at different timestamps ("User is vegetarian" vs. "User ordered a steak"), implement a resolution strategy that surfaces the conflict and asks the agent to reconcile. |
| 3 | Cross-Architecture Query | Moderate | Implement a `UnifiedMemoryInterface` that routes queries to the best-fit backend (vector for semantic similarity, graph for relationships, key-value for exact lookups) based on query classification. |
| 4 | Scalability Stress Test | Stretch | Load 1,000 synthetic conversation turns into each architecture and measure query latency, memory footprint, and retrieval precision at scale. Identify the breaking point for each system. |

### Key References

- [Letta (MemGPT)](https://www.letta.com/) — OS-inspired memory management for LLM agents; production platform built on the MemGPT research
- [MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560) — foundational paper on virtual context management and self-editing memory
- [Mem0](https://mem0.ai/) — hybrid memory layer for personalized AI with vector + graph + key-value storage
- [Zep](https://www.getzep.com/) — long-term memory and knowledge infrastructure for assistants with automatic fact extraction
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — survey post covering memory in the broader agent architecture
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — architectural patterns including memory management
- [Mem0 GitHub](https://github.com/mem0ai/mem0) — open-source implementation of the Mem0 memory layer

---

## 02. Vector Databases

**File:** `02_vector_databases.ipynb`

### Overview

This notebook is a hands-on deep dive into vector databases — the storage backbone for semantic memory in agent systems. You will work directly with ChromaDB (embedded, Python-native), Qdrant (client-server, filtering-focused), and pgvector (SQL-native), building indexes, running queries, and implementing hybrid search that combines dense vector similarity with sparse keyword matching and metadata filters. By the end, you will have a practical understanding of how to choose and operate a vector database for agent memory at scale.

### Learning Objectives

By the end of this notebook, you will be able to:
- Explain how approximate nearest neighbor (ANN) search works at a conceptual level (HNSW, IVF) and why exact brute-force search does not scale
- Set up ChromaDB, Qdrant, and pgvector and perform full CRUD operations on vector collections
- Implement hybrid search combining dense embeddings with BM25 sparse vectors and metadata filters using Reciprocal Rank Fusion
- Tune chunking strategies (fixed-size, recursive, semantic) and measure their impact on retrieval quality with precision@k and MRR
- Choose appropriate distance metrics (cosine, dot product, Euclidean) for different embedding models and use cases
- Design a vector storage schema for a multi-session agent with user-scoped collections, TTL-based expiration, and metadata indexing

### Prerequisites

- [`../core/13_rag_from_scratch.ipynb`](../core/13_rag_from_scratch.ipynb) — basic embedding and retrieval pipeline
- [`../appendix/10_numpy_for_embeddings.ipynb`](../appendix/10_numpy_for_embeddings.ipynb) — vector operations, cosine similarity, and distance metrics

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | From Cosine Similarity to ANN | Review exact nearest-neighbor search from Core 13, then show why it fails at 100k+ vectors. Introduce HNSW and IVF index structures at a conceptual level with visual diagrams. Benchmark brute-force vs. ANN on a 10k vector dataset. |
| 2 | ChromaDB — Embedded Vector Store | Install ChromaDB, create a collection, embed and insert 200 text chunks, query with metadata filters. Build a helper class `ChromaMemory` that wraps the ChromaDB client with `add`, `search`, `update`, and `delete` methods. Highlight its zero-config, in-process design ideal for notebooks and prototypes. |
| 3 | Qdrant — Client-Server Vector DB | Run Qdrant in in-memory mode, create a collection with payload indexes, insert the same 200 chunks, query with payload filters and score thresholds. Use Qdrant's nested filtering and range queries. Compare query latency and expressiveness against ChromaDB. |
| 4 | pgvector — SQL-Native Vectors | Set up SQLite with sqlite-vss (or Postgres with pgvector if available). Write SQL queries that combine vector similarity with WHERE clauses on structured columns. Show the power of having vectors live alongside relational data — join vectors with user tables, session tables, etc. |
| 5 | Chunking Strategies | Implement three chunking approaches: fixed-size with overlap, recursive character splitting, and semantic chunking using embedding similarity breakpoints. Chunk the same 10-page document with each strategy. Measure retrieval quality on 20 test queries and show which strategy wins for which query types. |
| 6 | Hybrid Search — Dense + Sparse + Metadata | Implement Reciprocal Rank Fusion (RRF) to combine dense vector results with BM25 keyword results. Add metadata filters (timestamp ranges, source document, user_id). Show concrete cases where hybrid search beats pure vector search — especially for proper nouns and exact phrases. |
| 7 | Retrieval Evaluation | Build an evaluation harness: create a test set of 30 question-answer pairs with ground-truth source passages. Compute precision@k, recall@k, and Mean Reciprocal Rank (MRR) for each database and chunking strategy combination. Visualize results in a comparison matrix. |
| 8 | Schema Design for Agent Memory | Design a collection schema for a multi-session agent: separate collections for conversation history, extracted facts, and user preferences. Implement user-scoped namespacing so User A's memories never leak into User B's queries. Add TTL-based expiration for ephemeral memories and importance-weighted retention for critical ones. |

### Putting It Together

Build a `VectorMemoryBackend` class that provides a unified interface over ChromaDB, Qdrant, and pgvector with a pluggable backend configuration. The class should support hybrid search (dense + sparse + metadata), automatic chunking of long documents on ingestion, and user-scoped namespacing. Test it by indexing a small corpus of 50 documents and running the same 20 queries against all three backends, comparing results side by side in a pandas DataFrame.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Metadata-Filtered Retrieval | Starter | Add timestamp and source metadata to your ChromaDB collection, then write queries that retrieve only chunks from the last 7 days or from a specific document source. Verify that filters correctly narrow results without degrading semantic relevance. |
| 2 | Chunking Quality Comparison | Moderate | Take a 10-page technical document, chunk it with all three strategies, and create a 10-question test set. Measure which chunking approach gives the best retrieval accuracy and write up why — consider how chunk boundaries interact with the information needed for each question. |
| 3 | Multi-Tenant Vector Store | Moderate | Implement user-scoped collections in Qdrant where each user's memories are isolated by payload filter. Add an admin query path that searches across all users (for analytics) while respecting tenant boundaries for user-facing queries. Test with 3 synthetic users. |
| 4 | Build a Reranker Pipeline | Stretch | Add a cross-encoder reranker (using a small model like `cross-encoder/ms-marco-MiniLM-L-6-v2`) on top of your vector search results. Measure the improvement in precision@5 on your test set. Analyze which queries benefit most from reranking and why. |

### Key References

- [ChromaDB Documentation](https://docs.trychroma.com/) — getting started, collections, querying, filtering, and embedding functions
- [Qdrant Documentation](https://qdrant.tech/documentation/) — concepts, indexing, payload filtering, and hybrid search
- [pgvector GitHub](https://github.com/pgvector/pgvector) — Postgres extension for vector similarity search with HNSW and IVFFlat indexes
- [HNSW Algorithm Explained (Pinecone)](https://www.pinecone.io/learn/series/faiss/hnsw/) — visual walkthrough of hierarchical navigable small world graphs
- [Anthropic — Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) — prepending chunk-specific context to improve retrieval quality
- [Chunking Strategies for LLM Applications (Pinecone)](https://www.pinecone.io/learn/chunking-strategies/) — practical guide to text chunking approaches and tradeoffs
- [Reciprocal Rank Fusion (Cormack et al.)](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) — the algorithm behind hybrid search result fusion
- [MTEB Leaderboard (HuggingFace)](https://huggingface.co/spaces/mteb/leaderboard) — Massive Text Embedding Benchmark for comparing embedding models

---

## 03. Knowledge Graphs for Agents

**File:** `03_knowledge_graphs_for_agents.ipynb`

### Overview

This notebook teaches you to build graph-based memory for agents — where entities are nodes, relationships are edges, and the graph evolves over time as the agent learns from conversations. You will use NetworkX to construct knowledge graphs from unstructured text via LLM-powered extraction, implement graph-based retrieval (subgraph expansion, path finding, community detection), and handle temporal changes where facts update or become invalid. Graph memory complements vector memory by capturing *structure* — who is connected to whom, what caused what, and how relationships change over time.

### Learning Objectives

By the end of this notebook, you will be able to:
- Represent agent knowledge as a property graph with typed entities, labeled relationships, and temporal metadata
- Extract entities and relationships from unstructured text using LLM-based structured extraction with confidence scores and coreference resolution
- Build and query knowledge graphs using NetworkX: subgraph retrieval, shortest path, multi-hop traversal, and community detection
- Implement temporal versioning so the graph tracks when facts were added, updated, or invalidated without deleting history
- Combine graph traversal with vector search for hybrid retrieval that handles both structural and semantic queries
- Design a knowledge graph schema for a conversational agent that maintains an evolving model of its user and their world

### Prerequisites

- [`../appendix/14_graph_data_structures.ipynb`](../appendix/14_graph_data_structures.ipynb) — graph fundamentals, adjacency representations, BFS/DFS traversal, and NetworkX basics
- [`../core/13_rag_from_scratch.ipynb`](../core/13_rag_from_scratch.ipynb) — embedding and retrieval patterns; understanding of why chunked-document retrieval has limits

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Why Graphs for Agent Memory | Show retrieval failures that vector search cannot solve: multi-hop reasoning ("Who manages the person who filed that bug?"), relationship queries ("What projects is Alice connected to through her team?"), and temporal reasoning ("Who was my manager before the reorg?"). Introduce property graphs as the solution. |
| 2 | Knowledge Graph Fundamentals | Build a `KnowledgeGraph` class wrapping NetworkX's `MultiDiGraph`. Define entity types (Person, Organization, Concept, Event, Location), relationship types (works_at, knows, caused_by, located_in), and property schemas. Implement `add_entity`, `add_relationship`, `get_neighbors`, and `get_subgraph`. |
| 3 | LLM-Based Entity and Relationship Extraction | Build an extraction pipeline: given a text passage, prompt the LLM to return structured JSON of entities and relationships with confidence scores. Implement validation (schema conformance), deduplication (fuzzy entity matching via embedding similarity), and coreference resolution (mapping "he", "the company", "my boss" to known entities). |
| 4 | Building a Graph from Conversations | Process a 30-turn synthetic conversation through the extraction pipeline, building a knowledge graph incrementally turn by turn. Visualize the graph at 5 stages using matplotlib. Handle entity merging when the LLM extracts the same entity with different surface forms ("Anthropic", "anthropic", "the company"). |
| 5 | Graph Querying for Retrieval | Implement four retrieval strategies: (a) direct neighbor lookup — all facts about an entity, (b) subgraph expansion within k hops — local context, (c) shortest path between two entities — how things connect, and (d) community detection to find topic clusters. Compare each strategy's results on 10 test queries. |
| 6 | Temporal Knowledge — Facts That Change | Add `valid_from` and `valid_until` timestamps to edges. Implement a `TemporalKnowledgeGraph` that supports point-in-time queries ("What was true about X on date Y?") and change tracking ("How has X's role changed over time?"). Show how to invalidate stale facts by closing their validity window without deleting them. |
| 7 | Graph + Vector Hybrid Retrieval | Implement a retrieval pipeline that first does a vector search to find relevant text chunks, then expands context by traversing the knowledge graph from entities mentioned in the retrieved chunks. Measure improvement over pure vector search on 15 relationship-heavy queries. This is the GraphRAG pattern. |
| 8 | Visualization and Debugging | Build graph visualization utilities using matplotlib and optionally pyvis (interactive HTML): entity clusters color-coded by type, relationship labels on edges, temporal layers showing the graph at different points in time. Add a `graph_summary()` method that uses an LLM to narrate the current graph state in natural language for debugging. |

### Putting It Together

Build a `ConversationKnowledgeGraph` that processes a 50-turn multi-session conversation, extracts entities and relationships with an LLM, maintains temporal versioning, and answers 10 test queries using graph + vector hybrid retrieval. The system should correctly handle entity updates ("I moved to Seattle" overriding "I live in Portland"), relationship changes ("I left Google and joined Anthropic"), and multi-hop queries ("What city does my former colleague at Google work in now?"). Evaluate each query's answer against a ground-truth expected result.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Entity Deduplication | Starter | Implement fuzzy matching (Levenshtein distance or embedding similarity) to merge entities like "Anthropic", "anthropic", and "Anthropic Inc." into a single canonical node. Test on a graph with 20 intentionally noisy entities. |
| 2 | Temporal Query Engine | Moderate | Build a query interface that accepts natural language temporal queries ("Who did I work with before 2024?", "What changed about my team in the last month?") and translates them into graph traversals with timestamp filters. |
| 3 | Contradiction Detection | Moderate | When a new edge contradicts an existing one (e.g., two different `lives_in` edges for the same person at the same time), detect the conflict automatically, log it, and prompt the LLM to resolve it by choosing the more recent or more confident fact. |
| 4 | Graph-Guided Question Answering | Stretch | Given a complex multi-hop question, use the knowledge graph to decompose it into sub-questions, resolve each sub-question via graph traversal, and synthesize a final answer with an LLM. Compare answer quality against a pure RAG approach on 5 multi-hop questions. |

### Key References

- [NetworkX Documentation](https://networkx.org/documentation/stable/) — Python library for graph creation, manipulation, and analysis
- [Anthropic — Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) — combining retrieval methods for better context; the vector baseline you are extending
- [Microsoft GraphRAG](https://microsoft.github.io/graphrag/) — knowledge graph-enhanced RAG architecture combining graph structure with LLM summarization
- [Zep — Temporal Knowledge Graphs](https://help.getzep.com/) — production implementation of temporal graph memory for AI assistants
- [Mem0 — Graph Memory](https://docs.mem0.ai/features/graph-memory) — graph-based memory extraction and querying in the Mem0 platform
- [Knowledge Graphs and LLMs (survey)](https://arxiv.org/abs/2306.08302) — academic survey of KG + LLM integration patterns and architectures
- [Neo4j — Knowledge Graphs Explained](https://neo4j.com/blog/knowledge-graph-explained/) — comprehensive overview of knowledge graph concepts for those wanting to go deeper

---

## 04. Long-Term Memory

**File:** `04_long_term_memory.ipynb`

### Overview

This notebook integrates the three storage systems from the previous notebooks — vector database (semantic similarity), knowledge graph (relationships and structure), and relational database (state and metadata) — into a unified long-term memory system. This is the "memory trifecta" pattern used by production agent systems like Letta and Mem0. You will build a `LongTermMemory` class that routes writes to the appropriate store, fuses retrieval results across stores, manages memory lifecycle (consolidation, decay, garbage collection), and persists state across independent conversation sessions.

### Learning Objectives

By the end of this notebook, you will be able to:
- Design a multi-store memory architecture that combines vector, graph, and relational storage with clear write and read routing responsibilities
- Implement a memory ingestion pipeline that extracts facts, entities, relationships, and metadata from conversations and routes them to the correct stores
- Build a retrieval fusion layer that queries all three stores in parallel, deduplicates results, and ranks them by combined relevance
- Implement memory consolidation — periodically summarizing and compressing old memories to manage storage growth while preserving retrieval quality
- Add memory decay and importance scoring so the agent naturally deprioritizes low-value information over time
- Handle multi-session memory persistence where the agent saves full state to disk and restores it when a new session begins

### Prerequisites

- [`01_memory_architectures.ipynb`](01_memory_architectures.ipynb) — understanding of architectural patterns and tradeoffs across Letta, Mem0, and Zep
- [`02_vector_databases.ipynb`](02_vector_databases.ipynb) — vector storage, hybrid search, schema design, and the `VectorMemoryBackend` class
- [`03_knowledge_graphs_for_agents.ipynb`](03_knowledge_graphs_for_agents.ipynb) — knowledge graph construction, temporal versioning, and graph-based retrieval
- [`../appendix/12_databases_and_sql.ipynb`](../appendix/12_databases_and_sql.ipynb) — SQLite, schema design, and query patterns for the relational storage layer

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | The Memory Trifecta Pattern | Explain why no single store is sufficient: vectors lack structure, graphs lack semantic fuzzy matching, SQL lacks similarity. Diagram the three-store architecture with clear data flow for writes (ingestion routing) and reads (retrieval fusion). Show a concrete example where each store contributes a different piece to the same answer. |
| 2 | Schema Design Across Stores | Design coordinated schemas: SQLite tables for session metadata, user profiles, and memory metadata with foreign keys; ChromaDB collections for semantic chunks with metadata linking back to SQLite records; NetworkX graph for entity-relationship-temporal data with node IDs matching SQLite entity records. Define the shared identifier scheme that links records across stores. |
| 3 | Memory Ingestion Pipeline | Build a `MemoryWriter` class that takes a conversation turn and: (a) stores the raw message in SQLite with session and timestamp metadata, (b) extracts and embeds semantic chunks into ChromaDB, (c) extracts entities and relationships into the knowledge graph, (d) updates user profile metadata in SQLite. Each step is independent, so they can run in parallel. |
| 4 | Multi-Store Retrieval Fusion | Build a `MemoryReader` class that, given a query: (a) runs vector search for semantically similar memories, (b) runs graph traversal for structurally connected knowledge starting from entities in the query, (c) runs SQL queries for session context and metadata. Implement Reciprocal Rank Fusion to merge and deduplicate results into a single ranked list. |
| 5 | Memory Consolidation | Implement periodic consolidation: summarize old conversation chunks into higher-level summaries (reducing 50 chunks to 5 summary chunks), merge redundant graph nodes that refer to the same entity, and archive low-access memories to a cold store. Build a `consolidate()` method that reduces storage by 40-60% while maintaining >95% retrieval quality on a test query set. |
| 6 | Importance Scoring and Decay | Assign importance scores to memories based on: recency (when was it stored?), access frequency (how often retrieved?), emotional valence (did the user express strong feelings?), and user-flagged significance ("remember this!"). Implement exponential decay so old, unaccessed memories gradually lose ranking weight. Build a `garbage_collect()` method that prunes memories below a configurable threshold. |
| 7 | Multi-Session Persistence | Implement full session management: `persist(path)` saves SQLite database, serialized NetworkX graph (pickle), and ChromaDB persist directory to a single folder. `restore(path)` reloads everything. Maintain a session log that tracks what memories changed between sessions. Test with a three-session conversation where information from Session 1 is correctly recalled in Session 3. |
| 8 | End-to-End Integration | Wire the `MemoryWriter` and `MemoryReader` into a full agent loop. The agent processes user messages, writes memories via the ingestion pipeline, retrieves relevant context for each response via fusion retrieval, and runs consolidation between sessions. Run a 30-turn conversation and inspect the memory state at each stage using a debug view that shows what was stored, what was retrieved, and what was used. |

### Putting It Together

Build a `LongTermMemory` class that integrates all three stores behind a unified interface with `remember(conversation_turn)`, `recall(query, top_k)`, `consolidate()`, and `persist(path)` / `restore(path)` methods. Test it in a three-session scenario: Session 1 introduces user preferences and project context (10 turns). Session 2 updates some preferences and adds new information (10 turns). Session 3 tests recall of information from both prior sessions including correctly handling updates — the agent should return the *updated* preference, not the original (10 turns). Measure retrieval precision against a ground-truth set of 15 expected memories.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Write Router | Starter | Implement a classifier that examines an extracted memory and routes it to the correct store(s): factual statements to the graph, descriptive passages to the vector store, structured metadata to SQLite. Ensure some memories (like "Alice works at Anthropic in Seattle") are written to multiple stores. Test on 20 diverse inputs. |
| 2 | Retrieval Ablation Study | Moderate | Measure retrieval quality (precision@5, MRR) when using all three stores vs. just vector, just graph, just SQL, and each pair combination. Run on a 15-query test set. Quantify the contribution of each store to overall recall and identify which query types benefit most from which store. |
| 3 | Memory Compression Ratio | Moderate | Run consolidation at different aggressiveness thresholds (compress top 25%, 50%, 75% of old memories) and measure the tradeoff between storage reduction and retrieval quality degradation. Find the sweet spot where you achieve >50% compression with <5% quality loss on your test queries. |
| 4 | Streaming Memory Ingestion | Stretch | Modify the ingestion pipeline to process memories asynchronously using Python's `asyncio`, so the agent does not block on memory writes during conversation. Implement a write queue, background workers, and confirmation callbacks. Measure the latency improvement and verify no memories are dropped under concurrent load. |

### Key References

- [Letta Documentation](https://docs.letta.com/) — production implementation of hierarchical long-term memory with self-editing capabilities
- [Mem0 Documentation](https://docs.mem0.ai/) — hybrid memory layer with vector + graph + key-value stores and automatic extraction
- [MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560) — the foundational paper on virtual context management and unbounded agent memory
- [Zep — Memory Enrichment](https://help.getzep.com/) — automated memory extraction, enrichment, and temporal indexing pipeline
- [SQLite Documentation](https://www.sqlite.org/docs.html) — lightweight relational database used for metadata, state, and session management
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — patterns for stateful agent systems including memory considerations
- [Chip Huyen — AI Engineering (Memory chapter)](https://huyenchip.com/2025/01/07/agents.html) — practical overview of memory patterns in production agents

---

## 05. Personalization and User Modeling

**File:** `05_personalization_and_user_modeling.ipynb`

### Overview

This notebook brings memory to its ultimate purpose: building an agent that genuinely learns about its user and adapts its behavior over time. You will implement preference extraction from conversations, build structured user profiles that update incrementally with confidence tracking, and create adaptive behavior strategies where the agent adjusts its tone, detail level, format, and proactive suggestions based on what it has learned. This is where memory becomes personalization — the difference between a stateless tool and an assistant that knows you.

### Learning Objectives

By the end of this notebook, you will be able to:
- Extract user preferences, habits, expertise levels, and goals from conversational text using structured LLM extraction with confidence scores
- Build and maintain a user profile schema that represents preferences, expertise, communication style, recurring topics, and interaction patterns — all evolving over time
- Implement incremental profile updates that handle new information, reinforcing evidence, preference changes, and contradictions with confidence-weighted resolution
- Design adaptive agent behavior that modifies response style (verbosity, formality, technical depth, format) based on the current user profile
- Build proactive suggestion systems that anticipate user needs based on historical interaction patterns and stated goals
- Evaluate personalization quality using both automated metrics (profile accuracy, retrieval of known preferences) and rubric-based LLM evaluation of response adaptation

### Prerequisites

- [`01_memory_architectures.ipynb`](01_memory_architectures.ipynb) — architectural patterns for agent memory, especially how Mem0 and Zep approach user-level memory
- [`02_vector_databases.ipynb`](02_vector_databases.ipynb) — semantic storage and retrieval for preference and context lookup
- [`03_knowledge_graphs_for_agents.ipynb`](03_knowledge_graphs_for_agents.ipynb) — entity extraction and relationship tracking for modeling user connections and context
- [`04_long_term_memory.ipynb`](04_long_term_memory.ipynb) — the unified multi-store memory system you will extend with personalization capabilities

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | From Memory to Personalization | Define the personalization stack: raw memories (what happened) -> extracted preferences (what matters) -> user model (who they are) -> adaptive behavior (how the agent responds). Show before/after examples: the same question answered generically vs. adapted to a known user profile. Explain why this is the highest-value application of agent memory. |
| 2 | Preference Extraction Pipeline | Build an LLM-powered extraction pipeline that processes conversation turns and outputs structured preference objects: `{ category: "communication", preference: "prefers concise answers", confidence: 0.85, evidence: "turn 12: 'can you keep it brief?'" }`. Handle both explicit preferences ("I prefer bullet points") and implicit ones (user consistently asks for shorter explanations, always asks about implementation details). |
| 3 | User Profile Schema | Design a `UserProfile` dataclass with sections: identity (name, timezone, language), expertise (topic-skill level mappings), communication preferences (verbosity, formality, format, tone), interests (topics weighted by recency and frequency), goals (short-term tasks, long-term objectives), and interaction patterns (session frequency, typical duration, common task types). Each attribute has a confidence score and evidence trail. |
| 4 | Incremental Profile Updates | Implement `update_profile()` that merges new preference signals into the existing profile. Handle three cases: (a) new information — add to profile with initial confidence, (b) reinforcing evidence — increase confidence on existing preference, (c) contradicting information — use recency weighting and confidence comparison to resolve, flagging genuine preference changes vs. one-off requests. Track full version history so you can see how the profile evolved. |
| 5 | Adaptive Response Generation | Build a `PersonalizedResponder` that dynamically constructs the system prompt based on the user profile. Implement concrete adaptations: adjust technical depth (beginner gets analogies, expert gets implementation details), response format (prose vs. bullets vs. code-first), verbosity (concise vs. comprehensive), and tone (casual vs. professional). Show side-by-side comparisons of the same query answered with 3 different user profiles. |
| 6 | Proactive Suggestions | Implement pattern detection over interaction history: recurring topics the user keeps returning to, time-based habits (always asks about deployment on Fridays), incomplete tasks mentioned but not followed up on, and knowledge gaps (topics where the user frequently asks basic questions). Build a `suggest()` method that generates contextually relevant proactive suggestions at the start of each session. |
| 7 | Privacy and User Control | Implement user-facing memory controls: `show_profile()` displays everything the agent knows in a readable format, `correct_preference(key, value)` lets the user override an extracted preference, `forget_topic(topic)` removes all memories and preferences related to a topic across all stores, and `export_data()` creates a portable JSON profile export. Discuss the ethics of passive preference learning and the importance of transparency. |
| 8 | Evaluation Framework | Build a personalization evaluation suite with three components: (a) profile accuracy — compare extracted profiles against ground-truth labels for 3 synthetic user personas, (b) adaptation quality — use an LLM judge with a rubric to rate whether responses are well-adapted to the user profile on a 1-5 scale, (c) A/B preference test — for the same query, generate personalized vs. default responses and have the LLM judge which the synthetic user would prefer. Aggregate results into a personalization quality score. |

### Putting It Together

Build a `PersonalizedAgent` that integrates the full long-term memory stack (from notebook 04) with the preference extraction and adaptive behavior systems from this notebook. Run a five-session simulation with a synthetic user persona who is a backend engineer, prefers concise technical answers, and is learning about AI agents. Session 1: introductory conversation where the agent gives generic responses and begins building a profile. Sessions 2-3: domain-specific questions where the agent progressively adapts its detail level and format. Session 4: the user starts asking more advanced questions, and the agent detects the expertise shift. Session 5: the user explicitly changes a preference ("Actually, give me more detailed explanations from now on"), and the agent updates its profile and adapts immediately. Evaluate all sessions using the rubric from Section 8 and present a personalization quality report showing improvement over time.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Implicit Preference Detection | Starter | Analyze a 20-turn conversation and extract at least 5 implicit preferences that the user never explicitly stated but are evident from their behavior patterns — e.g., always asks follow-up questions about implementation details (suggesting they prefer depth), consistently ignores theoretical explanations (suggesting they prefer practical examples). |
| 2 | Multi-User Profiles | Moderate | Extend the system to support 3 simultaneous users, each with their own profile and memory scope. Implement profile switching and verify no memory leakage between users. Create two synthetic personas with opposing preferences (one concise/technical, one verbose/conceptual) and show the agent adapts differently to each. |
| 3 | Preference Drift Detection | Moderate | Implement a system that detects when a user's preferences are gradually shifting — not a single contradictory statement, but a trend over 5+ interactions. For example, a user who was asking beginner questions is now consistently asking intermediate ones. Alert the agent to update its model and log the detected drift with evidence. |
| 4 | Cold Start Optimization | Stretch | Build an onboarding flow that efficiently bootstraps a new user's profile in the first 5 conversation turns by asking strategically chosen high-information-gain questions. Use an information-theoretic approach: each question should maximize the expected reduction in uncertainty about the user's profile. Compare profile quality after 5 targeted onboarding turns vs. 20 turns of organic conversation. |

### Key References

- [Zep Documentation](https://help.getzep.com/) — user-scoped memory, automatic fact extraction, and session-based personalization features
- [Anthropic — Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agentic) — patterns for adaptive agent behavior and user-aware design
- [Mem0 — User Memory](https://docs.mem0.ai/) — per-user memory management, preference storage, and cross-session personalization
- [Letta — Agent State and Core Memory](https://docs.letta.com/) — how Letta manages per-user core memory blocks that the agent reads and writes
- [Chip Huyen — AI Engineering](https://huyenchip.com/2025/01/07/agents.html) — practical patterns for production agents including personalization and user modeling
- [The Ethics of AI Personalization](https://arxiv.org/abs/2305.15700) — considerations for responsible preference learning, consent, and data minimization
- [GDPR — Right to Erasure](https://gdpr.eu/right-to-be-forgotten/) — privacy framework relevant to any system that stores user data and preferences
