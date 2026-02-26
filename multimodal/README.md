# Voice & Multimodal Agents — Lesson Plans

> Detailed lesson plans for notebooks 01–04. Voice and vision capabilities unlock entirely new categories of agent applications.
> For the full track overview, see [`../roadmap.md`](../roadmap.md).

---

## 01. Vision Agents

**File:** `01_vision_agents.ipynb`

### Overview

This notebook teaches you how to build agents that can see — processing images as first-class inputs alongside text. You will construct an agent that accepts screenshots, diagrams, and charts, reasons about their visual content, and calls tools based on what it observes. Vision is a critical modality for agents that need to interact with GUIs, interpret data visualizations, or parse documents containing non-textual information.

### Learning Objectives

By the end of this notebook, you will be able to:

- Send images (base64-encoded and URL-referenced) to multimodal LLMs via the chat completions API
- Build an agent that interprets screenshots and describes UI elements, layout, and interactive components
- Extract structured data from charts and diagrams using vision combined with structured output parsing
- Combine vision understanding with tool calling so the agent can act on what it sees
- Handle multiple images in a single conversation turn and reason across them
- Evaluate vision agent accuracy by comparing extracted data against known ground truth

### Prerequisites

- [`../core/05_react_agent.ipynb`](../core/05_react_agent.ipynb) — You need a working ReAct agent loop to extend with vision capabilities
- [`../core/04_structured_output.ipynb`](../core/04_structured_output.ipynb) — Extracting structured data from charts requires reliable JSON output from the LLM

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | How Vision Models Work | Understand how multimodal LLMs process image tokens alongside text tokens — the cost/resolution tradeoffs, detail levels, and token budget implications. |
| 2 | Sending Your First Image | Encode a local image as base64 and send it to Claude and OpenAI vision endpoints via OpenRouter. Compare the two API formats side by side. |
| 3 | URL-Based Image Input | Pass images by URL instead of base64. Learn when each approach is appropriate, the security considerations, and how image caching affects behavior. |
| 4 | Screenshot Understanding | Feed the agent a screenshot of a web page and ask it to identify UI elements, read text, and describe layout — the foundation of GUI agents. |
| 5 | Chart and Diagram Analysis | Give the agent a bar chart and a flowchart diagram. Extract numerical data from the chart into a structured JSON object using your structured output skills from Core 04. |
| 6 | Multi-Image Reasoning | Send multiple images in one turn (e.g., "compare these two screenshots") and have the agent reason across them to identify differences, trends, or relationships. |
| 7 | Vision + Tool Calling | Wire vision into your ReAct agent loop: the agent sees an image, decides it needs to call a tool (e.g., a calculator for chart values), executes the tool, and returns a final answer. |
| 8 | Evaluation and Failure Modes | Test your vision agent against edge cases — low-resolution images, ambiguous charts, text-heavy screenshots — and measure extraction accuracy against ground truth data. |

### Putting It Together

Build a "Chart Analyst" agent that accepts a chart image and a natural-language question (e.g., "Which quarter had the highest revenue?"), extracts the relevant data using vision, calls a calculator tool to verify arithmetic, and returns a structured answer with confidence scores. This exercise combines every skill from the notebook: image encoding, structured extraction, tool use, and multi-step reasoning.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Screenshot Describer | Starter | Send three different screenshots to the vision API and compare the descriptions. Experiment with different system prompts to control verbosity and focus. |
| 2 | Invoice Data Extractor | Moderate | Build a pipeline that takes a photo of an invoice, extracts vendor name, line items, and total into a JSON object, and validates that line items sum to the total. |
| 3 | Visual Diff Agent | Moderate | Given two screenshots of the same page (before/after a change), have the agent identify and describe all visual differences, returning them as a structured list. |
| 4 | GUI Navigator | Stretch | Build an agent that receives a screenshot, identifies clickable elements with bounding-box coordinates, and outputs a step-by-step action plan to accomplish a user task (e.g., "click the search bar and type 'agents'"). |

### Key References

- [Anthropic Vision Documentation](https://docs.anthropic.com/en/docs/build-with-claude/vision) — Official guide to sending images to Claude, including supported formats, resolution limits, and best practices
- [OpenAI Vision Guide](https://platform.openai.com/docs/guides/vision) — GPT-4o vision capabilities, detail levels (`low` vs `high`), and token cost calculations
- [OpenRouter Multi-Modal Models](https://openrouter.ai/docs/requests#multi-modal-models) — How to send images through OpenRouter's unified API to various vision-capable models
- [Anthropic Cookbook: Vision](https://github.com/anthropics/anthropic-cookbook/tree/main/misc/vision) — Practical code examples for chart reading, document extraction, and image analysis with Claude
- [Claude Computer Use Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/computer-use) — Reference architecture for agents that interact with GUIs via screenshots — the production version of what you prototype here
- [Google Gemini Vision Docs](https://ai.google.dev/gemini-api/docs/vision) — Gemini's multimodal approach for comparison with Claude and OpenAI

---

## 02. Voice Pipeline

**File:** `02_voice_pipeline.ipynb`

### Overview

This notebook builds a complete voice agent pipeline from discrete components: speech-to-text (STT) transcription with Whisper, reasoning with your existing LLM agent, and text-to-speech (TTS) synthesis for spoken output. You will wire these three stages together into a pipeline that accepts audio input and produces audio output. Understanding the sequential STT-LLM-TTS architecture is essential before moving to the streaming realtime approach in notebook 03, and this modular design lets you swap in different STT or TTS providers without changing the agent logic.

### Learning Objectives

By the end of this notebook, you will be able to:

- Transcribe audio files to text using the OpenAI Whisper API, including language detection and timestamps
- Integrate STT output into your existing agent loop as the user message
- Generate spoken audio from agent text responses using a TTS API with configurable voice and speed
- Build an end-to-end voice pipeline: audio in, agent reasoning, audio out
- Measure and optimize end-to-end latency across the three pipeline stages
- Handle audio formats, sample rates, and chunking for robust real-world input processing

### Prerequisites

- [`../core/05_react_agent.ipynb`](../core/05_react_agent.ipynb) — The voice pipeline wraps your existing ReAct agent; you need a working agent loop to integrate with
- [`../appendix/11_async_and_await.ipynb`](../appendix/11_async_and_await.ipynb) — STT and TTS calls benefit from async execution; understanding `asyncio` is needed for the concurrent pipeline variant in Section 7

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | The STT-LLM-TTS Architecture | Map out the three-stage voice pipeline, understand where latency accumulates at each stage, and see why this sequential approach is the simplest starting point before streaming. |
| 2 | Audio Fundamentals | Learn the minimum about audio formats (WAV, MP3, OGG), sample rates, channels, and duration that you need to work with speech APIs. Load and play audio in a notebook with IPython.display. |
| 3 | Speech-to-Text with Whisper | Send an audio file to the OpenAI Whisper API and get back a transcript. Explore language detection, timestamps, word-level output, and the `prompt` parameter for domain vocabulary. |
| 4 | Wiring STT to Your Agent | Take the Whisper transcript and feed it as the user message into your ReAct agent loop. Run the full reasoning cycle and capture the text response, including any tool calls the agent makes. |
| 5 | Text-to-Speech Synthesis | Send the agent's text response to a TTS API (OpenAI TTS) and receive audio bytes. Explore voice selection, speed control, and output format options (mp3, opus, aac, flac). |
| 6 | End-to-End Pipeline | Connect all three stages into a single `voice_agent(audio_bytes) -> audio_bytes` function. Measure the total round-trip latency and identify the bottleneck stage. |
| 7 | Async Pipeline Optimization | Run STT and agent-setup concurrently where possible, stream TTS output as audio chunks arrive, and reduce perceived latency using async patterns from Appendix 11. |
| 8 | Recording Live Audio | Capture microphone input in the notebook (using `ipywidgets` or `sounddevice`), send it through the pipeline, and play back the agent's spoken response — the complete interactive loop. |

### Putting It Together

Build a "Voice Assistant" that records your spoken question from the microphone, transcribes it, runs it through your ReAct agent (with at least one tool — such as a weather lookup or calculator), and speaks the answer back to you. Log the latency of each stage (STT ms, LLM reasoning ms, TTS ms) so you can see where the time goes and have a quantitative baseline to compare against the Realtime API in notebook 03.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Transcript Comparison | Starter | Transcribe the same audio clip with different Whisper parameters (language hints, temperature, prompt) and compare accuracy, speed, and behavior across settings. |
| 2 | Voice Changer | Moderate | Build a pipeline where the user speaks, the agent paraphrases the input in a different style (e.g., pirate, formal English, ELI5), and the TTS speaks the paraphrase in a different voice. |
| 3 | Multi-Turn Voice Chat | Moderate | Extend the pipeline to support multi-turn conversation: maintain chat history across voice exchanges so the agent remembers prior questions and can refer back to earlier context. |
| 4 | Latency Profiler | Stretch | Instrument every stage of the pipeline with precise timing. Generate a waterfall chart (using matplotlib) showing STT, LLM, and TTS durations across 10 different queries. Identify which stage dominates and write up optimization strategies. |

### Key References

- [OpenAI Speech-to-Text API](https://platform.openai.com/docs/guides/speech-to-text) — API reference for Whisper transcription, including supported audio formats, parameters, and pricing
- [OpenAI Text-to-Speech Guide](https://platform.openai.com/docs/guides/text-to-speech) — API reference for TTS synthesis, voice options (alloy, echo, fable, onyx, nova, shimmer), and streaming output
- [Whisper GitHub Repository](https://github.com/openai/whisper) — Source code and local-run instructions for Whisper, useful for understanding model internals and running offline
- [Deepgram STT Documentation](https://developers.deepgram.com/docs/stt-pre-recorded) — Alternative STT provider with streaming and real-time capabilities for comparison with Whisper
- [ElevenLabs TTS API](https://elevenlabs.io/docs/api-reference/text-to-speech) — High-quality alternative TTS with voice cloning and ultra-low latency, useful as a comparison point
- [Python sounddevice Library](https://python-sounddevice.readthedocs.io/) — Library for recording and playing audio in Python, used in Section 8 for microphone capture

---

## 03. Realtime Voice Agent

**File:** `03_realtime_voice_agent.ipynb`

### Overview

This notebook moves beyond the sequential STT-LLM-TTS pipeline to the OpenAI Realtime API, which provides bidirectional audio streaming over a single WebSocket connection. You will build a low-latency conversational agent that listens and speaks in real time, with the ability to call tools mid-conversation. The Realtime API fundamentally changes the agent interaction model — from request-response to continuous, interruptible dialogue — and understanding it prepares you for production-grade voice agent architectures used by companies like LiveKit, Retell, and Vapi.

### Learning Objectives

By the end of this notebook, you will be able to:

- Establish a WebSocket connection to the OpenAI Realtime API and manage session lifecycle events
- Stream audio input to the API and receive audio output in real time over the same connection
- Configure server-side voice activity detection (VAD) for automatic turn-taking with tunable sensitivity
- Register tools (function definitions) with the Realtime API and handle tool-call events mid-conversation
- Implement interruption handling so the user can cut in while the agent is speaking
- Compare latency, cost, and architectural complexity tradeoffs between the pipeline approach (notebook 02) and the Realtime API

### Prerequisites

- [`02_voice_pipeline.ipynb`](02_voice_pipeline.ipynb) — Understanding the STT-LLM-TTS pipeline gives you the conceptual baseline and makes you appreciate what the Realtime API abstracts away
- [`../appendix/13_websockets_and_streaming.ipynb`](../appendix/13_websockets_and_streaming.ipynb) — The Realtime API runs over WebSockets; you need to be comfortable with async connection handling, message framing, and event-driven programming patterns

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Pipeline vs. Realtime Architecture | Compare the STT-LLM-TTS pipeline with the Realtime API side by side. Understand why bidirectional streaming reduces latency, eliminates transcription as a separate step, and enables natural interruptions. |
| 2 | WebSocket Connection Setup | Establish a WebSocket connection to the Realtime API endpoint, authenticate with your API key, and configure the session — voice selection, modality (text+audio or audio-only), and turn detection mode. |
| 3 | Sending and Receiving Audio | Stream raw PCM16 audio chunks to the API using `input_audio_buffer.append` events and receive audio response chunks back via `response.audio.delta` events. Play the received audio in real time. |
| 4 | Voice Activity Detection | Configure server-side VAD so the API automatically detects when the user stops speaking and triggers a response. Tune `silence_duration_ms`, `threshold`, and `prefix_padding_ms` for your use case. |
| 5 | Conversation Management | Handle multi-turn conversation state managed server-side. Explore conversation item creation, the response lifecycle (`response.created` through `response.done`), and how context accumulates across turns. |
| 6 | Tool Use in Realtime | Register function tools in the session configuration. Handle `response.function_call_arguments.done` events, execute the tool locally, send results back via `conversation.item.create`, and trigger a follow-up response. |
| 7 | Interruption Handling | Implement user-initiated interruptions: when the user speaks while the agent is mid-response, send `response.cancel`, handle the `response.cancelled` event, and truncate the conversation item so context stays clean. |
| 8 | Latency Benchmarking | Measure time-to-first-audio-byte, end-to-end response time, and tool-call round-trip latency. Compare quantitatively with notebook 02's pipeline results and analyze the cost per minute of audio. |

### Putting It Together

Build a "Realtime Assistant" that maintains a persistent WebSocket connection, listens for spoken questions via VAD, responds with natural speech, and can call at least two tools (e.g., a weather API and a unit converter) mid-conversation without breaking the audio stream. The user should be able to interrupt the agent while it is speaking. Produce a latency comparison table (time-to-first-audio-byte, total response time) against the pipeline approach from notebook 02 on the same set of queries.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Hello Realtime | Starter | Establish a Realtime API session, send a single audio clip via `input_audio_buffer.append`, commit the buffer, and play back the agent's audio response. Log every WebSocket event type to map out the protocol flow. |
| 2 | Multi-Tool Realtime Agent | Moderate | Register three tools with the Realtime API and hold a multi-turn conversation where the agent calls different tools depending on the question. Verify that tool results are incorporated into the spoken response. |
| 3 | Interruption Stress Test | Moderate | Write an automated script that sends audio input while the agent is still generating a response, triggering an interruption. Verify the agent stops its current response, truncates the item, and addresses the new input cleanly. |
| 4 | Realtime vs. Pipeline Shootout | Stretch | Run the same 10 queries through both the pipeline (notebook 02) and the Realtime API. Produce a comparison table with time-to-first-byte, total latency, token/cost estimates, and transcript accuracy. Write a 500-word analysis of which approach fits which use case. |

### Key References

- [OpenAI Realtime API Guide](https://platform.openai.com/docs/guides/realtime) — Official documentation covering WebSocket and WebRTC connection setup, session configuration, events, and audio format requirements
- [OpenAI Voice Agents Guide](https://platform.openai.com/docs/guides/voice-agents) — Higher-level guide on building production voice agents with tool use, guardrails, multi-turn patterns, and deployment considerations
- [OpenAI Realtime API Reference](https://platform.openai.com/docs/api-reference/realtime) — Full client/server event reference, session object schema, and error codes
- [OpenAI Realtime Console](https://github.com/openai/openai-realtime-console) — Open-source reference implementation of a Realtime API client with a web UI — study the event handling code
- [WebSocket Protocol (RFC 6455)](https://datatracker.ietf.org/doc/html/rfc6455) — The underlying protocol specification, useful for understanding framing, ping/pong, and connection lifecycle
- [websockets Python Library](https://websockets.readthedocs.io/) — Documentation for the `websockets` library you will use to connect to the Realtime API from Python
- [LiveKit OpenAI Realtime Integration](https://docs.livekit.io/agents/integrations/openai/overview/) — Production framework for deploying Realtime API agents at scale, useful as a reference architecture for what comes after this notebook

---

## 04. Multimodal Tool Use

**File:** `04_multimodal_tool_use.ipynb`

### Overview

This notebook is the capstone of the multimodal track. You will build an agent that accepts text, images, and audio in any combination, reasons across all modalities simultaneously, and calls tools based on its multimodal understanding. Where notebooks 01-03 each focused on a single modality, this notebook teaches you to compose them — building an agent that can look at a photo, listen to a voice instruction, read accompanying text, and take coordinated action by calling the right tools. This is the architecture pattern behind modern general-purpose AI assistants.

### Learning Objectives

By the end of this notebook, you will be able to:

- Design a unified message format that carries text, image, and audio content blocks in a single conversation turn
- Route different input modalities through appropriate preprocessing (base64 encoding for images, STT transcription for audio) before feeding them to the LLM
- Build an agent loop that reasons over mixed-modality inputs and decides which tools to call based on combined understanding
- Chain multimodal observations: use the output of a vision tool as input to a text-reasoning step, or transcribe audio and cross-reference it with an image
- Handle modality-specific errors gracefully (corrupt images, inaudible audio, unsupported formats) without crashing the agent loop
- Evaluate multimodal agent performance across a test suite that includes text-only, image-only, audio-only, and combined inputs

### Prerequisites

- [`01_vision_agents.ipynb`](01_vision_agents.ipynb) — You need to know how to send images to multimodal LLMs and extract structured data from visual input
- [`02_voice_pipeline.ipynb`](02_voice_pipeline.ipynb) — You need the STT transcription skills to convert audio inputs to text for models that do not natively accept audio
- [`../core/03_tool_use_from_scratch.ipynb`](../core/03_tool_use_from_scratch.ipynb) — The agent calls tools based on multimodal reasoning; solid understanding of tool definition, invocation, and result handling is essential

### Section Breakdown

| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | The Multimodal Agent Architecture | Design the high-level architecture for an agent that accepts any combination of text, image, and audio. Map out where preprocessing, modality detection, LLM reasoning, and tool calling fit in the extended agent loop. |
| 2 | Unified Input Handling | Build an input normalizer that detects modality type (text string, image file, audio file, URL) and converts each into the correct API content block format. Handle mixed-modality user turns with multiple content blocks. |
| 3 | Vision + Text Reasoning | Give the agent an image and a text question that requires both visual understanding and factual knowledge. The agent reasons across both modalities — e.g., "What city is shown in this photo, and what is its population?" |
| 4 | Audio + Text Reasoning | Feed the agent a voice memo alongside a text document. The agent transcribes the audio, cross-references it with the document, and answers questions that require synthesizing both sources of information. |
| 5 | Multimodal Tool Definitions | Define tools that accept or return non-text data: an image-analysis tool that returns structured descriptions, an audio-transcription tool, and a chart-generation tool that produces images. Register them with the agent. |
| 6 | Cross-Modal Tool Chaining | Build a multi-step workflow where the agent calls a vision tool to extract data from a chart image, passes that data to a calculator tool for analysis, and formats the result as a spoken response via TTS. Each tool's output feeds the next step. |
| 7 | Error Handling Across Modalities | Handle failures gracefully: corrupt image files, inaudible audio, unsupported formats, oversized inputs. The agent should detect the failure, explain what went wrong to the user, and ask for alternative input rather than crashing. |
| 8 | Evaluation Suite | Run the multimodal agent against a diverse test suite: text-only queries, image-only queries, audio-only queries, and multi-modal combination queries. Score accuracy per modality combination and identify where the agent struggles. |

### Putting It Together

Build a "Universal Research Assistant" that accepts a research question in any modality combination. For example: the user sends a photo of a whiteboard diagram, a voice memo providing context, and a text query asking for a specific analysis. The agent processes all three inputs through the unified handler, calls relevant tools (image analyzer, web search, calculator), chains the results across modalities, and returns a comprehensive written answer. Test it with at least three different modality combinations (text+image, audio+text, image+audio+text) to verify robustness across input types.

### Exercises

| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Modality Detector | Starter | Build the input normalizer function that accepts a file path or raw text, detects the modality (text, image, audio) based on file extension and content inspection, and returns the appropriate API-formatted message content block. Write tests for at least five input types. |
| 2 | Photo + Voice Note Agent | Moderate | Build an agent that accepts a photo and a voice note together. The agent describes the photo, transcribes the voice note, and answers a question that requires understanding both inputs (e.g., a photo of a restaurant menu + a voice note asking "what's the cheapest vegetarian option?"). |
| 3 | Cross-Modal Pipeline | Moderate | Construct a three-step tool chain: (1) extract text from a document photo using vision, (2) summarize the extracted text using the LLM, (3) convert the summary to speech using TTS. Each step's output becomes the next step's input. Log the data transformations at each stage. |
| 4 | Multimodal Benchmark | Stretch | Create a benchmark suite of 15+ test cases spanning all modality combinations (text-only, image-only, audio-only, text+image, text+audio, image+audio, all three). Run your agent against it, score accuracy per combination, and write a 500-word analysis of which combinations the agent handles best and worst with proposed improvements. |

### Key References

- [Anthropic Vision Documentation](https://docs.anthropic.com/en/docs/build-with-claude/vision) — Official guide for sending images to Claude, including multi-image turns and mixed content blocks with text
- [Anthropic Tool Use Documentation](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview) — Claude-specific tool use patterns, including how tool results can contain image content blocks
- [OpenAI Vision Guide](https://platform.openai.com/docs/guides/vision) — GPT-4o vision capabilities and how image inputs combine with text and tool calling
- [OpenAI Realtime API Guide](https://platform.openai.com/docs/guides/realtime) — Reference for native audio input/output alongside tool calling in a streaming context
- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling) — Defines how to register and invoke tools, the foundation layer for multimodal tool orchestration
- [Google Gemini Multimodal Docs](https://ai.google.dev/gemini-api/docs/vision) — Gemini's approach to mixed-modality input (text, image, audio, video) for comparison with Claude and OpenAI
- [HuggingFace smolagents Documentation](https://huggingface.co/docs/smolagents/) — How smolagents handles multimodal inputs and tool outputs in its agent framework
- [Lilian Weng: LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — Foundational blog post on agent architectures, relevant to understanding how multimodal inputs extend the standard agent loop
