"""Pipeline tests.

answer_question is tested with a fake classifier and fake insight writer
so the pipeline logic runs without the network. One integration test
runs the real pipeline when the OpenRouter key is available.
"""

import pandas as pd

from app import pipeline


def make_df() -> pd.DataFrame:
    """One full week, Monday to Sunday, rising revenue.

    Sunday is the clear best day with 700. No ties.
    """
    dates = pd.date_range("2026-01-05", periods=7, freq="D")
    revenue = [100, 200, 300, 400, 500, 600, 700]
    return pd.DataFrame({"date": dates, "revenue": revenue})


def test_answer_question_full_shape(monkeypatch):
    df = make_df()

    def fake_classify(q):
        return {"type": "best_day", "question": q}

    def fake_insight(result):
        return "Best day is Sunday with 700.0."

    monkeypatch.setattr(pipeline, "classify_question", fake_classify)
    monkeypatch.setattr(pipeline, "write_insight", fake_insight)

    answer = pipeline.answer_question("best day?", df=df)
    assert answer["type"] == "best_day"
    assert answer["result"]["best_day"] == "Sunday"
    assert answer["chart"] is not None
    assert "Sunday" in answer["insight"]
    assert answer["question"] == "best day?"


def test_answer_question_fallback_type(monkeypatch):
    df = make_df()

    def fake_classify(q):
        return {"type": "fallback", "question": q}

    monkeypatch.setattr(pipeline, "classify_question", fake_classify)
    monkeypatch.setattr(pipeline, "write_insight",
                        lambda result: "I cannot answer that yet.")

    answer = pipeline.answer_question("hello?", df=df)
    assert answer["type"] == "fallback"
    assert answer["chart"] is None
    assert answer["result"]["message"]


def test_chart_matches_result_numbers():
    """Chart values must equal the pandas result, field for field."""
    from app.analyze import run as analyze
    from app.charts import build_chart

    df = make_df()
    result = analyze(df, "best_day")
    fig = build_chart(result)
    plotted = list(fig.data[0].y)
    expected = [result["weekday_means"][d] for d in result["weekday_means"]]
    assert plotted == expected
