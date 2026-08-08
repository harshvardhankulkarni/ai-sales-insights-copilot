"""Pipeline. One question in, one complete answer out.

answer_question runs the full flow:
classify the question, compute with pandas, build the chart,
write the insight. The pieces stay pure. This module only threads them.
"""

from app.analyze import run as analyze
from app.charts import build_chart
from app.data import load_sales
from app.insights import write_insight
from app.understand import classify_question


def answer_question(question: str, df=None) -> dict:
    """Run the full copilot flow for one typed question.

    Returns a dict with question, type, result, chart, insight.
    """
    if df is None:
        df = load_sales()

    classification = classify_question(question)
    question_type = classification["type"]
    result = analyze(df, question_type)
    chart = build_chart(result)
    insight = write_insight(result)

    return {
        "question": question,
        "type": result["type"],
        "result": result,
        "chart": chart,
        "insight": insight,
    }