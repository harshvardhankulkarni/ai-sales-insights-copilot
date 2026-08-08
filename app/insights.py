"""Insight writer. The LLM turns computed numbers into plain prose.

This module never computes. It receives a result dict from analyze.py
and writes sentences about the numbers that are already in it. If the
model call fails, a canned fallback keeps the pipeline alive.
"""

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

OPENROUTER_BASE = "https://openrouter.ai/api/v1"


def _make_llm() -> ChatOpenAI:
    model = os.getenv("LLM_MODEL", "openai/gpt-oss-20b:free")
    return ChatOpenAI(
        model=model,
        temperature=0,
        base_url=OPENROUTER_BASE,
        api_key=os.getenv("OPENROUTER_API_KEY"),
        request_timeout=30,
        max_retries=1,
    )


def _prompt_for(result: dict) -> str:
    """Build a grounded prompt from the numbers pandas already computed.

    The prompt lists the exact numbers. The model may use only these.
    """
    if result["type"] == "trend":
        return (
            "Write 2 plain sentences about sales for a business owner. "
            "Use only these facts. "
            f"Average revenue in the last 7 days: {result['last_window_avg']}. "
            f"Average revenue in the 7 days before that: "
            f"{result['previous_window_avg']}. "
            f"Change: {result['change_pct']}% ({result['direction']}). "
            "State the direction and the percent change. No other numbers."
        )
    if result["type"] == "best_day":
        return (
            "Write 2 plain sentences about sales for a business owner. "
            "Use only these facts. "
            f"Best weekday: {result['best_day']} with average revenue "
            f"{result['avg_revenue']}. "
            "Say which day is best and give its average revenue. "
            "No other numbers."
        )
    if result["type"] == "comparison":
        return (
            "Write 2 plain sentences about sales for a business owner. "
            "Use only these facts. "
            f"Total revenue in {result['current_month']}: "
            f"{result['current_revenue']}. "
            f"Total revenue in {result['previous_month']}: "
            f"{result['previous_revenue']}. "
            f"Change: {result['change_pct']}%. "
            "Say which month was higher and give the percent change. "
            "No other numbers."
        )
    return (
        "Write one plain sentence saying the question cannot be answered "
        "with the available data. No numbers."
    )


def write_insight(result: dict, llm=None) -> str:
    """Return a plain-language insight built from the result numbers.

    Falls back to a canned sentence when the model is unavailable.
    """
    fallback = _fallback_for(result)
    try:
        if llm is None:
            llm = _make_llm()
        reply = llm.invoke(_prompt_for(result))
        text = (reply.content or "").strip()
        return text if text else fallback
    except Exception:
        return fallback


def write_weekly_insight(df, llm=None) -> str:
    """Write a narrative from weekly revenue totals.

    The weekly totals come from pandas. The LLM narrates them.
    """
    weekly = _weekly_summary(df)
    prompt = (
        "Write 3 plain sentences summarizing a sales week for a business "
        "owner. Use only these facts. "
        f"Week totals in order: {weekly} (last week last). "
        "Say how the weeks compare and which was the strongest. "
        "No other numbers."
    )
    fallback = (
        "Weekly revenue trends are available in the dashboard tables."
    )
    try:
        if llm is None:
            llm = _make_llm()
        reply = llm.invoke(prompt)
        text = (reply.content or "").strip()
        return text if text else fallback
    except Exception:
        return fallback


def _weekly_summary(df) -> str:
    """Return the last 4 weeks as a plain text list, oldest first."""
    weekly = (
        df.copy()
        .assign(week=df["date"].dt.to_period("W"))
        .groupby("week")["revenue"]
        .sum()
        .tail(4)
    )
    return ", ".join(f"{idx}: {value:.0f}" for idx, value in weekly.items())


def _fallback_for(result: dict) -> str:
    """Canned sentence with the real numbers, used when the LLM fails.

    The numbers come from pandas, so the fallback stays grounded.
    """
    if result["type"] == "trend":
        return (
            f"Revenue moved {result['direction']} "
            f"{result['change_pct']}% over the last 7 days."
        )
    if result["type"] == "best_day":
        return (
            f"The best weekday was {result['best_day']} with an average "
            f"of {result['avg_revenue']}."
        )
    if result["type"] == "comparison":
        return (
            f"Revenue changed {result['change_pct']}% from "
            f"{result['previous_month']} to {result['current_month']}."
        )
    return "I cannot answer that yet."