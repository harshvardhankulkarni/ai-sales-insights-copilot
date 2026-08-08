"""Unit tests for the pandas analysis engine.

Each test feeds a small known DataFrame and checks the returned numbers.
No LLM call happens here. Grounding test: analyze runs without any API.
"""

import pandas as pd

from app import analyze


def make_df() -> pd.DataFrame:
    """Tiny deterministic daily series: 14 days starting Thursday 2026-01-01.

    Pattern: every day divisible by 8 in the list is 400, others alternate.
    Friday, Sunday, Tuesday mean 300. All other days mean 150.
    """
    dates = pd.date_range("2026-01-01", periods=14, freq="D")
    revenue = [100, 200, 100, 200, 100, 200, 100,
               200, 400, 200, 400, 200, 400, 200]
    return pd.DataFrame({"date": dates, "revenue": revenue, "units": [1] * 14})


def make_two_month_df() -> pd.DataFrame:
    """75 days covers three calendar months, so comparison has a previous one."""
    dates = pd.date_range("2026-01-01", periods=75, freq="D")
    revenue = [500.0] * 75
    return pd.DataFrame({"date": dates, "revenue": revenue, "units": [1] * 75})


def test_trend_returns_direction_and_average():
    df = make_df()
    result = analyze.run(df, "trend")
    assert result["type"] == "trend"
    assert result["direction"] in ("up", "down")
    assert result["last_window_avg"] > 0
    assert len(result["chart_dates"]) == len(result["chart_rolling"])


def test_best_day_returns_highest_mean():
    df = make_df()
    result = analyze.run(df, "best_day")
    # Friday, Sunday, Tuesday all mean 300. pandas picks the first in order.
    assert result["best_day"] in ("Friday", "Sunday", "Tuesday")
    assert result["avg_revenue"] == 300.0
    assert result["weekday_means"]["Monday"] == 150.0


def test_comparison_returns_two_periods_and_change():
    df = make_two_month_df()
    result = analyze.run(df, "comparison")
    assert result["current_month"] != result["previous_month"]
    assert result["current_revenue"] > 0
    assert result["previous_revenue"] > 0
    assert isinstance(result["change_pct"], float)


def test_fallback_returns_message_only():
    df = make_df()
    result = analyze.run(df, "alien_invasion")
    assert result["type"] == "fallback"
    assert "message" in result


def test_grounding_no_llm_import():
    """analyze must compute without importing any LLM library."""
    import sys

    assert "langchain" not in sys.modules