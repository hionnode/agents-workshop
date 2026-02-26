"""Shared helper code for agents-workshop notebooks.

Utilities extracted from notebooks live here so individual notebooks
remain self-contained while avoiding duplication.
"""

import os

import httpx
from dotenv import load_dotenv

# Load .env from the repo root (works from any notebook location)
load_dotenv()

# ---------------------------------------------------------------------------
# LLM chat helper — thin wrapper around the OpenRouter Chat Completions API
# ---------------------------------------------------------------------------

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "meta-llama/llama-3.1-8b-instruct:free"


def chat(
    messages: list[dict],
    model: str = DEFAULT_MODEL,
    temperature: float = 0.7,
    max_tokens: int | None = None,
) -> str:
    """Send messages to OpenRouter and return the assistant's response text.

    Args:
        messages: List of message dicts with 'role' and 'content' keys.
        model: OpenRouter model identifier.
        temperature: Sampling temperature (0 = deterministic, higher = more random).
        max_tokens: Optional max tokens in the response.

    Returns:
        The assistant's response text as a string.

    Raises:
        RuntimeError: If the API call fails or the response is malformed.
    """
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY not found. "
            "Copy .env.example to .env and add your key."
        )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }
    if max_tokens is not None:
        payload["max_tokens"] = max_tokens

    try:
        response = httpx.post(
            OPENROUTER_BASE_URL,
            headers=headers,
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"OpenRouter API error {e.response.status_code}: {e.response.text}") from e
    except httpx.RequestError as e:
        raise RuntimeError(f"Request failed: {e}") from e

    data = response.json()

    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Unexpected response shape: {data}") from e
