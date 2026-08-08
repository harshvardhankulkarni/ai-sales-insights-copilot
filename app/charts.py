"""Plotly charts. The chart reads the pandas result and plots it.

It never computes its own numbers. If the number is not in the result
dict, the chart does not show it.
"""

import plotly.graph_objects as go


def build_chart(result: dict) -> go.Figure:
    """Return a Plotly figure for the analysis result.

    Fallback results have no numbers and return no chart.
    """
    chart_type = result.get("type")
    if chart_type == "trend":
        return _trend_chart(result)
    if chart_type == "best_day":
        return _best_day_chart(result)
    if chart_type == "comparison":
        return _comparison_chart(result)
    return None


def _trend_chart(result: dict) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=result["chart_dates"],
        y=result["chart_rolling"],
        mode="lines+markers",
        name="7 day rolling avg",
    ))
    fig.add_hline(y=result["last_window_avg"], line_dash="dash",
                  annotation_text="last 7 day avg")
    fig.update_layout(
        title=f"Revenue trend: {result['direction']} "
              f"({result['change_pct']}%)",
        xaxis_title="date",
        yaxis_title="revenue",
        height=420,
    )
    return fig


def _best_day_chart(result: dict) -> go.Figure:
    means = result["weekday_means"]
    days = list(means.keys())
    values = list(means.values())
    colors = ["#94a3b8"] * len(days)
    colors[days.index(result["best_day"])] = "#2563eb"
    fig = go.Figure(go.Bar(
        x=days,
        y=values,
        marker_color=colors,
        text=values,
        textposition="outside",
    ))
    fig.update_layout(
        title=f"Average revenue by weekday. Best: {result['best_day']}",
        xaxis_title="weekday",
        yaxis_title="average revenue",
        height=420,
    )
    return fig


def _comparison_chart(result: dict) -> go.Figure:
    fig = go.Figure(go.Bar(
        x=[result["previous_month"], result["current_month"]],
        y=[result["previous_revenue"], result["current_revenue"]],
        text=[result["previous_revenue"], result["current_revenue"]],
        textposition="outside",
        marker_color=["#94a3b8", "#2563eb"],
    ))
    fig.update_layout(
        title=f"Month over month: {result['change_pct']}%",
        xaxis_title="month",
        yaxis_title="total revenue",
        height=420,
    )
    return fig