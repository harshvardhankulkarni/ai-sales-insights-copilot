"""Natural language question classifier.

The only LLM job on this pipeline: pick the right type from a question.
It does not compute. It does not answer. It classifies.
Runs through OpenRouter (https://openrouter.ai) with a free model.
"""

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

VALID_TYPES = {"trend", "best_day", "comparison"}
FALLBACK = "fallback"

OPENROUTER_BASE = "https://openrouter.ai/api/v1"

_SYSTEM_PROMPT = (
    "You classify sales questions into exactly one type. "
    "Types: trend, best_day, comparison, fallback. "
    "trend: revenue going up or down over time. "
    "best_day: which weekday earns the most. "
    "comparison: one month or period against another. "
    "fallback: anything else, including product or category questions. "
    "Reply with a single word: trend, best_day, comparison, or fallback."
)


def _validate(raw: str) -> str:
    """Turn the model reply into a safe type.

    Anything that is not a known type becomes fallback. The app never
    crashes on a bad or empty model reply.
    """
    text = str(raw or "").strip().lower()
    first_word = text.split()[0] if text else ""
    first_word = first_word.strip(".,!?")
    if first_word in VALID_TYPES:
        return first_word
    return FALLBACK


def classify_question(question: str, llm=None) -> dict:
    """Classify a typed question into a seeded type.

    Returns {"type": ..., "question": ...}. The type is one of
    trend, best_day, comparison, fallback.
    """
    try:
        if llm is None:
            model = os.getenv("LLM_MODEL", "openai/gpt-oss-20b:free")
            llm = ChatOpenAI(
                model=model,
                temperature=0,
                base_url=OPENROUTER_BASE,
                api_key=os.getenv("OPENROUTER_API_KEY"),
                request_timeout=30,
                max_retries=1,
            )
        reply = llm.invoke(_SYSTEM_PROMPT + "\n\nQuestion: " + question)
        raw = reply.content
    except Exception:
        return {"type": FALLBACK, "question": question}

    return {"type": _validate(raw), "question": question}