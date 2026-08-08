"""Streamlit frontend. Theme: Executive Desk (user chosen).

Layout mirrors sketches/001-executive-desk:
- warm paper background, gold accent, serif headings
- KPI cards across the top (pandas numbers only)
- chart panel left, ask panel right
- one chart per answer, insight beside it

Grounding rules hold here too: every number in the UI comes from
pandas (analyze.run). The pipeline calls the LLM only to narrate
those numbers. Chart and insight always match the same result dict.
"""

import html
import sys
from pathlib import Path

# Streamlit puts frontend/ on sys.path. The app package lives one level up.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st  # noqa: E402

from app.analyze import run as analyze  # noqa: E402
from app import charts  # noqa: E402
from app.data import load_sales  # noqa: E402
from app.insights import _fallback_for  # noqa: E402
from app.insights import write_weekly_insight  # noqa: E402
from app.pipeline import answer_question  # noqa: E402

st.set_page_config(
    page_title="Sales Insights Copilot",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

EXAMPLES = [
    "What was our best day of the week?",
    "Is revenue going up?",
    "How does this month compare to last?",
]

_CSS = """
<style>
  :root {
    --paper: #f6f5f1;
    --panel: #ffffff;
    --line: #e5e1d8;
    --ink: #1a1f2e;
    --muted: #8a8a85;
    --gold: #8a6d3b;
    --up: #1e7a4d;
    --down: #b03a2e;
  }
  [data-testid="stAppViewContainer"] { background: var(--paper); }
  [data-testid="stHeader"] { background: transparent; }
  .block-container { padding-top: 24px; }
  h1, h2, h3 { font-family: Georgia, serif; }
  .kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr);
              gap: 14px; margin-bottom: 22px; }
  .kpi { background: var(--panel); border: 1px solid var(--line);
         border-radius: 10px; padding: 14px 16px; }
  .kpi .k { font-size: 12px; color: var(--muted);
            text-transform: uppercase; letter-spacing: .06em; }
  .kpi .v { font-size: 24px; font-weight: 700; color: var(--ink);
            margin-top: 4px; font-variant-numeric: tabular-nums; }
  .kpi .d { font-size: 13px; margin-top: 2px; }
  .up { color: var(--up); } .down { color: var(--down); }
  .panel { background: var(--panel); border: 1px solid var(--line);
           border-radius: 10px; padding: 18px 20px; }
  .panel h2 { font-family: Georgia, serif; font-size: 20px;
              font-weight: 400; color: var(--ink); margin-bottom: 12px; }
  .insight { margin-top: 14px; border-left: 3px solid var(--gold);
             padding: 10px 14px; background: #faf8f2;
             border-radius: 0 8px 8px 0; font-size: 14px; color: #3a3f4c; }
  .ex-label { font-size: 12px; color: var(--muted); margin: 12px 0 8px; }
  .q-bubble, .a-bubble { border-radius: 10px; padding: 10px 12px;
                         font-size: 14px; margin-bottom: 10px; }
  .q-bubble { background: #fafafa; border: 1px solid var(--line);
              text-align: right; color: var(--ink); }
  .a-bubble { background: #f6f5f1; border: 1px solid var(--line);
              color: #22242b; }
  .chips { color: var(--muted); font-size: 12px; margin-top: 4px; }
  .meta { font-size: 12px; color: var(--muted); }
  .stButton > button { background: var(--panel); border: 1px solid var(--line);
                       color: #4a4f5c; border-radius: 8px; }
  .stButton > button:hover { border-color: var(--gold); color: var(--ink); }
  .stFormSubmitButton > button { background: var(--ink); color: #fff;
                       border: 0; border-radius: 8px; }
  .stFormSubmitButton > button:hover { background: #2c3350; color: #fff; }
  [data-testid="stForm"] [data-testid="stTextInput"] input {
      border: 1px solid var(--line); border-radius: 8px; }
</style>
"""
st.markdown(_CSS, unsafe_allow_html=True)


def fmt(n: float) -> str:
    return f"{n:,.0f}"


@st.cache_data
def get_sales():
    return load_sales()


def kpi_html(df) -> str:
    """KPI numbers, all from pandas."""
    thirty = df["revenue"].tail(30).sum()
    prior = df["revenue"].tail(60).head(30).sum()
    delta30 = (thirty - prior) / prior * 100
    best = analyze(df, "best_day")
    trend_r = analyze(df, "trend")
    total = df["revenue"].sum()
    days = len(df)
    up_down = "up" if delta30 >= 0 else "down"
    trend_class = "up" if trend_r["direction"] == "up" else "down"
    return f"""
    <div class="kpi-grid">
      <div class="kpi"><div class="k">Last 30 days</div>
        <div class="v">{fmt(thirty)}</div>
        <div class="d {up_down}">{delta30:+.1f}% vs prior 30</div></div>
      <div class="kpi"><div class="k">Best weekday</div>
        <div class="v">{best["best_day"]}</div>
        <div class="d">avg {fmt(best["avg_revenue"])}</div></div>
      <div class="kpi"><div class="k">Trend, 7d</div>
        <div class="v">{trend_r["change_pct"]:+.1f}%</div>
        <div class="d {trend_class}">{trend_r["direction"]}</div></div>
      <div class="kpi"><div class="k">Data period</div>
        <div class="v">{days} days</div>
        <div class="d">total {fmt(total)}</div></div>
    </div>
    """


def theme_chart(fig, result):
    """Apply the Executive Desk palette to a pipeline chart.

    The figure already plots the pandas numbers. Recoloring only.
    No number is recomputed here.
    """
    t = result["type"]
    if t == "best_day":
        days = list(result["weekday_means"].keys())
        colors = [("#d9c8a8" if d == result["best_day"] else "#e0dacd")
                  for d in days]
        fig.update_traces(marker_color=colors)
    elif t == "comparison":
        fig.update_traces(marker_color=["#e0dacd", "#8a6d3b"])
    elif t == "trend":
        fig.update_traces(line_color="#8a6d3b", marker_color="#8a6d3b")
        for shape in fig.layout.shapes or ():
            shape.line.color = "#8a6d3b"
    return fig


def render_chart_panel(df):
    """Left column: the chart of the latest answer, or the default view."""
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    last_result = st.session_state.get("last_result")
    if last_result is None:
        # default view: best weekday, computed by pandas, no LLM call
        result = analyze(df, "best_day")
        fig = charts.build_chart(result)
        st.markdown("<h2>Average revenue by weekday</h2>", unsafe_allow_html=True)
        st.plotly_chart(theme_chart(fig, result), use_container_width=True)
        st.markdown(
            f'<div class="insight">{html.escape(_fallback_for(result))}'
            f'<br><span class="meta">Default view. Ask a question to run the copilot.</span></div>',
            unsafe_allow_html=True)
    else:
        q = st.session_state.get("last_question", "")
        st.markdown(f"<h2>{html.escape(q)}</h2>", unsafe_allow_html=True)
        if last_result["type"] == "fallback":
            st.markdown(
                f'<div class="insight">{html.escape(last_result["message"])}</div>',
                unsafe_allow_html=True)
        else:
            fig = charts.build_chart(last_result)
            st.plotly_chart(theme_chart(fig, last_result), use_container_width=True)
            if st.session_state.get("last_insight"):
                st.markdown(
                    f'<div class="insight">{html.escape(st.session_state["last_insight"])}</div>',
                    unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def render_ask_panel():
    """Right column: example chips, answer thread, ask form."""
    st.markdown('<div class="panel"><h2>Ask</h2>', unsafe_allow_html=True)
    st.markdown('<div class="ex-label">Try a question</div>', unsafe_allow_html=True)
    for ex in EXAMPLES:
        if st.button(ex, key=f"chip:{ex}", use_container_width=True):
            run_question(ex)
    st.markdown('<div class="ex-label">Thread</div>', unsafe_allow_html=True)
    answers = st.session_state.get("answers", [])
    if not answers:
        st.markdown('<div class="meta">No questions asked yet.</div>',
                    unsafe_allow_html=True)
    for a in answers:
        st.markdown(
            f'<div class="q-bubble">{html.escape(a["question"])}</div>'
            f'<div class="a-bubble">{html.escape(a["insight"])}</div>'
            f'<div class="chips">numbers: {html.escape(a["meta"])}</div>',
            unsafe_allow_html=True)
    with st.form("ask_form", clear_on_submit=True):
        question = st.text_input("Ask a sales question", label_visibility="collapsed",
                                 placeholder="Ask a sales question…")
        submitted = st.form_submit_button("Ask", use_container_width=True)
    if submitted and question.strip():
        run_question(question.strip())
    st.markdown("</div>", unsafe_allow_html=True)


def run_question(question: str):
    """Run the pipeline and store the result in session state."""
    with st.spinner("Analyzing with the model… this can take up to a minute."):
        answer = answer_question(question)
    meta = summarize_meta(answer["result"])
    st.session_state.setdefault("answers", []).append(
        {"question": question,
         "insight": answer["insight"],
         "meta": meta})
    st.session_state["last_question"] = question
    st.session_state["last_result"] = answer["result"]
    st.session_state["last_insight"] = answer["insight"]
    st.rerun()


def summarize_meta(result: dict) -> str:
    """Grounded mini-number line for the thread, straight from pandas."""
    t = result["type"]
    if t == "best_day":
        return f'Best {result["best_day"]}: {fmt(result["avg_revenue"])}'
    if t == "trend":
        return (f'Last 7d {fmt(result["last_window_avg"])} vs '
                f'{fmt(result["previous_window_avg"])} '
                f'({result["change_pct"]:+.2f}%)')
    if t == "comparison":
        return (f'{result["current_month"]} {fmt(result["current_revenue"])} '
                f'vs {result["previous_month"]} '
                f'{fmt(result["previous_revenue"])} '
                f'({result["change_pct"]:+.2f}%)')
    return result.get("message", "")


def main():
    df = get_sales()
    st.markdown(
        '<div style="display:flex;justify-content:space-between;'
        'align-items:baseline;margin-bottom:6px"><span style="'
        'font-size:15px;letter-spacing:.14em;text-transform:uppercase;'
        f'color:#7a6a4d;font-weight:600">Sales Insights</span>'
        f'<span class="meta">{df["date"].max().strftime("%d %b %Y")}</span></div>',
        unsafe_allow_html=True)
    st.markdown(kpi_html(df), unsafe_allow_html=True)
    left, right = st.columns([2.2, 1.0], gap="large")
    with left:
        render_chart_panel(df)
        st.divider()
        with st.expander("Weekly auto-insight"):
            st.caption("A short narrative of the last 4 weeks, "
                       "written from the pandas weekly totals.")
            if st.button("Write the week's story", key="weekly_btn"):
                with st.spinner("Writing from the weekly totals…"):
                    st.session_state["weekly"] = write_weekly_insight(df)
            if st.session_state.get("weekly"):
                st.write(st.session_state["weekly"])
    with right:
        render_ask_panel()


if __name__ == "__main__":
    main()