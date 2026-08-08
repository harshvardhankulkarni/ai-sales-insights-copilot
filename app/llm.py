"""LLM failover chain. Try several models in order, use the first reply.

The chain exists so one provider outage never kills the app. Each slot
is a different provider or tier built from environment variables.
A slot with no key is skipped. When every slot fails, the caller gets
an empty reply and uses its canned fallback.

Slots:
1. OpenRouter, free tier.  MODEL LLM_MODEL, default openai/gpt-oss-20b:free.
2. OpenRouter, paid tier.  MODEL LLM_MODEL2, default openai/gpt-4o-mini.
3. Gemini, OpenAI-compatible endpoint. Uses GEMINI_API_KEY.

Timeouts shrink per slot so a healthy first model gets the most time.
A slow or capped model fails fast and the chain moves on.
"""

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

OPENROUTER_BASE = "https://openrouter.ai/api/v1"
GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta/openai/"

DEFAULT_MODEL = "openai/gpt-oss-20b:free"
DEFAULT_MODEL2 = "openai/gpt-4o-mini"
DEFAULT_MODEL3 = "gemini-2.0-flash"


def _client(model: str, api_key: str, base_url: str, timeout: int) -> ChatOpenAI:
    return ChatOpenAI(
        model=model,
        temperature=0,
        base_url=base_url,
        api_key=api_key,
        request_timeout=timeout,
        max_retries=0,
    )


def build_chain() -> list:
    """Build the ordered list of ChatOpenAI clients from the environment."""
    chain = []

    or_key = os.getenv("OPENROUTER_API_KEY")
    if or_key:
        chain.append(
            _client(os.getenv("LLM_MODEL", DEFAULT_MODEL), or_key,
                    OPENROUTER_BASE, 30)
        )
        model2 = os.getenv("LLM_MODEL2", DEFAULT_MODEL2)
        if model2 != os.getenv("LLM_MODEL", DEFAULT_MODEL):
            chain.append(_client(model2, or_key, OPENROUTER_BASE, 20))

    gem_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if gem_key:
        chain.append(
            _client(os.getenv("LLM_MODEL3", DEFAULT_MODEL3), gem_key,
                    GEMINI_BASE, 15)
        )

    return chain


def first_reply(prompt: str, chain: list) -> str:
    """Run the prompt through each slot until one answers.

    Returns the first non-empty reply, or "" when every slot failed.
    A slot that returns empty text also counts as a failure.
    """
    for llm in chain:
        try:
            reply = llm.invoke(prompt)
            text = (reply.content or "").strip()
            if text:
                return text
        except Exception:
            continue
    return ""


def latest_reply(prompt: str) -> str:
    """Build the chain from the current environment and run the prompt."""
    return first_reply(prompt, build_chain())