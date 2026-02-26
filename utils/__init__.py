"""Shared helper code for agents-workshop notebooks.

Utilities extracted from notebooks live here so individual notebooks
remain self-contained while avoiding duplication.
"""

import json
import os
import re
import time

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

    Retries up to 3 times with exponential backoff on transient errors
    (429 rate-limit and 5xx server errors).

    Args:
        messages: List of message dicts with 'role' and 'content' keys.
        model: OpenRouter model identifier.
        temperature: Sampling temperature (0 = deterministic, higher = more random).
        max_tokens: Optional max tokens in the response.

    Returns:
        The assistant's response text as a string.

    Raises:
        RuntimeError: If the API call fails after all retries or the response
            is malformed.
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

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = httpx.post(
                OPENROUTER_BASE_URL,
                headers=headers,
                json=payload,
                timeout=60,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            status = e.response.status_code
            if status in (429, 500, 502, 503, 504) and attempt < max_retries - 1:
                delay = 2 ** attempt  # 1s, 2s, 4s
                time.sleep(delay)
                continue
            raise RuntimeError(
                f"OpenRouter API error {status}: {e.response.text}"
            ) from e
        except httpx.RequestError as e:
            if attempt < max_retries - 1:
                delay = 2 ** attempt
                time.sleep(delay)
                continue
            raise RuntimeError(f"Request failed: {e}") from e

        data = response.json()

        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            raise RuntimeError(f"Unexpected response shape: {data}") from e

    raise RuntimeError("chat() exited retry loop unexpectedly")


# ---------------------------------------------------------------------------
# JSON parsing and validation helpers — extracted from core/04
# ---------------------------------------------------------------------------


def safe_parse_json(text):
    """Try to parse JSON from LLM output, handling common issues.

    Handles clean JSON, markdown code fences, and JSON embedded in
    surrounding text. Returns the parsed dict/list on success, or None.
    """
    text = text.strip()

    # Remove markdown code fences
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

    # Try direct parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try to find a JSON object in the text (greedy — works for nested objects)
    json_match = re.search(r"\{.*\}", text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass

    return None


def validate_schema(data, schema):
    """Validate parsed JSON against an expected schema.

    Args:
        data: The parsed dict to validate.
        schema: Dict of ``{key: type}`` where *type* is ``str``, ``int``,
            ``float``, ``list``, etc.

    Returns:
        List of error strings (empty means valid).
    """
    errors = []
    for key, expected_type in schema.items():
        if key not in data:
            errors.append(f"Missing required key: '{key}'")
        elif not isinstance(data[key], expected_type):
            errors.append(
                f"Key '{key}' should be {expected_type.__name__}, "
                f"got {type(data[key]).__name__}"
            )
    return errors
