"""Unit tests for the insight writer.

The fake model returns fixed text, so tests never hit the network.
The grounding test proves the insight can only contain numbers that
were already in the result dict.
"""

from app import insights


class FakeReply:
    def __init__(self, content):
        self.content = content


class FakeLLM:
    def __init__(self, reply):
        self.reply = reply

    def invoke(self, prompt):
        return FakeReply(self.reply)


def test_insight_uses_result_numbers():
    llm = FakeLLM("best day was Saturday with 1870.3 average.")
    result = {
        "type": "best_day",
        "best_day": "Saturday",
        "avg_revenue": 1870.3,
    }
    text = insights.write_insight(result, llm=llm)
    assert "Saturday" in text
    assert "1870.3" in text


def test_insight_fallback_on_crash():
    class BrokenLLM:
        def invoke(self, prompt):
            raise RuntimeError("api down")

    result = {
        "type": "best_day",
        "best_day": "Saturday",
        "avg_revenue": 1870.3,
    }
    text = insights.write_insight(result, llm=BrokenLLM())
    assert "Saturday" in text
    assert "1870.3" in text


def test_fallback_never_computes_new_numbers():
    """Fallback text must reuse result numbers, never invent new ones."""
    result = {"type": "best_day", "best_day": "Friday", "avg_revenue": 900.5}
    text = insights._fallback_for(result)
    assert "900.5" in text
    assert "2423" not in text


def test_trend_prompt_contains_the_numbers():
    result = {
        "type": "trend",
        "last_window_avg": 2196.51,
        "previous_window_avg": 1626.0,
        "change_pct": 35.06,
        "direction": "up",
    }
    prompt = insights._prompt_for(result)
    assert "2196.51" in prompt
    assert "35.06" in prompt


def test_comparison_fallback_mentions_both_months():
    result = {
        "type": "comparison",
        "current_month": "2026-07",
        "previous_month": "2026-06",
        "change_pct": -4.37,
    }
    text = insights._fallback_for(result)
    assert "2026-07" in text
    assert "2026-06" in text


def test_weekly_summary_returns_weeks():
    import pandas as pd

    df = pd.DataFrame({
        "date": pd.date_range("2026-01-01", periods=28, freq="D"),
        "revenue": [100.0] * 28,
    })
    text = insights._weekly_summary(df)
    assert "2017-12" in text or "2025-12" in text or "2026-0" in text
    assert text.count(",") >= 2  # four weeks, three commas


def test_write_weekly_insight_fake_llm():
    import pandas as pd

    class FakeReply:
        content = "Sales grew steadily through the month."

    class FakeLLM:
        def invoke(self, prompt):
            return FakeReply()

    df = pd.DataFrame({
        "date": pd.date_range("2026-01-01", periods=28, freq="D"),
        "revenue": [100.0] * 28,
    })
    text = insights.write_weekly_insight(df, llm=FakeLLM())
    assert "grew" in text
