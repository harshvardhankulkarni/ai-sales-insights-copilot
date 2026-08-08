"""Pandas analysis engine. Every number in a copilot answer comes from here.

The LLM never computes. The chart never computes. This module computes.
Each analyzer returns a dict of numbers, plus the series the chart plots.
"""

import pandas as pd

WEEK = 7


def trend(df: pd.DataFrame, window: int = WEEK) -> dict:
    """Return the direction of revenue over recent days.

    Compares the average of the last `window` days with the average of the
    `window` days before that. Also returns the rolling series for the chart.
    """
    last_avg = df["revenue"].tail(window).mean()
    prev_avg = df["revenue"].tail(window * 2).head(window).mean()
    change_pct = (last_avg - prev_avg) / prev_avg * 100
    direction = "up" if change_pct >= 0 else "down"

    series = df.tail(window * 2).copy()
    series["rolling"] = series["revenue"].rolling(window).mean()
    return {
        "type": "trend",
        "last_window_avg": round(float(last_avg), 2),
        "previous_window_avg": round(float(prev_avg), 2),
        "change_pct": round(float(change_pct), 2),
        "direction": direction,
        "chart_dates": series["date"].dt.strftime("%Y-%m-%d").tolist(),
        "chart_revenue": [round(v, 2) for v in series["revenue"]],
        "chart_rolling": [round(v, 2) if pd.notna(v) else None
                          for v in series["rolling"]],
    }


def best_day(df: pd.DataFrame) -> dict:
    """Return the weekday with the highest average revenue.

    Also returns the mean for every weekday so the chart can draw them.
    """
    df = df.copy()
    df["weekday"] = df["date"].dt.day_name()
    grouped = df.groupby("weekday")["revenue"].mean().round(2)
    top = grouped.idxmax()
    return {
        "type": "best_day",
        "best_day": top,
        "avg_revenue": float(grouped.max()),
        "weekday_means": {str(k): float(v) for k, v in grouped.items()},
    }


def comparison(df: pd.DataFrame) -> dict:
    """Compare total revenue of the last month with the month before."""
    df = df.copy()
    df["month"] = df["date"].dt.to_period("M").astype(str)
    totals = df.groupby("month")["revenue"].sum()
    current, previous = totals.iloc[-1], totals.iloc[-2]
    change_pct = (current - previous) / previous * 100
    return {
        "type": "comparison",
        "current_month": str(totals.index[-1]),
        "previous_month": str(totals.index[-2]),
        "current_revenue": round(float(current), 2),
        "previous_revenue": round(float(previous), 2),
        "change_pct": round(float(change_pct), 2),
    }


ANALYZERS = {
    "trend": trend,
    "best_day": best_day,
    "comparison": comparison,
}


def run(df: pd.DataFrame, question_type: str) -> dict:
    """Dispatch a question type to its analyzer.

    Unknown types return a fallback so the app never crashes.
    """
    func = ANALYZERS.get(question_type)
    if func is None:
        return {"type": "fallback", "message": "I cannot answer that yet."}
    return func(df)