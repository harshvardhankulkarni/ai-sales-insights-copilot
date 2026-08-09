# Walkthrough — AI Sales Insights Copilot

Everything we learned building this project, step by step, with the code
explained. Written for the builder. Read it top to bottom once, then keep
it as the interview revision sheet.

## 1. What we built

A Streamlit sales dashboard with a natural language layer. Type a question
like "what was our best day of the week?" and get three things from one
question: the numbers, a Plotly chart, and a written insight.

Live at https://ai-sales-insights-copilot.streamlit.app/

The stack:

- Python 3.11, pandas, numpy for data
- Plotly for charts
- Streamlit for the UI
- langchain-openai for the LLM calls
- OpenRouter as the model gateway
- pytest for tests
- GitHub for the repo, GitHub Pages for docs, Streamlit Cloud for the app

## 2. The five lessons that carry the whole project

### Grounding

The LLM never computes a number. pandas computes every number. The LLM
writes prose about numbers it was handed. The chart reads the same result
dict. So the insight, the chart, and the printed numbers always agree.

This is the single most important idea. It is why the app is trustworthy.
A model that computes its own math invents numbers. A model that narrates
given numbers cannot.

### Classification, not computation

The question "what was our best day?" is not answered by the model. The
model only picks a type: trend, best_day, comparison, fallback. Then pandas
does the math for that type. The model is a router, not a calculator.

### Synthetic data from real data

We took real Tableau Superstore orders (9,800 rows) and aggregated them
into a 365-day daily series. Real numbers, safe to publish. The generator
script does this once; the output is committed.

### Prompt engineering

Each prompt names the exact types, the exact numbers, and the rule "no
other numbers". Short, explicit prompts beat clever prompts. The model
answers in one word for classification, two sentences for insights.

### Degradation design

Every failure path is planned. Slow model, dead model, wrong answer,
unknown question. Each degrades to a grounded fallback. The app never
crashes and never hangs.

## 3. The file map

```
app/data.py          load the CSV into a DataFrame
app/analyze.py       pandas computes the numbers
app/charts.py        Plotly draws the numbers
app/understand.py    LLM classifies the question type
app/insights.py      LLM writes prose from the numbers
app/llm.py           failover chain: try 3 models, then canned
app/pipeline.py      one question in, one answer dict out
frontend/streamlit_app.py   the UI
scripts/smoke_test.py       live end-to-end check
tests/                      28 unit tests
data/sales.csv              365 days of real sales
BENCHMARK.md                question bank with expected answers
```

The data flow: question -> understand -> analyze -> charts + insights
-> answer dict.

## 4. Level 2: data engine

### app/data.py

```python
DATA_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "sales.csv",
)

def load_sales(path: str = DATA_FILE) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    return df
```

What this does: finds the CSV next to the app package, reads it, and turns
the date column from text into real dates. The path trick matters. It
resolves relative to the file location, not the working folder, so the app
runs from anywhere. Streamlit Cloud needs this.

### app/analyze.py

Three pure functions. Each takes a DataFrame and returns a dict of numbers.
No side effects, no I/O.

```python
def best_day(df: pd.DataFrame) -> dict:
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
```

Line by line:

- `.dt.day_name()` turns each date into "Monday", "Tuesday", ...
- `.groupby("weekday")["revenue"].mean()` averages revenue per weekday.
- `.idxmax()` finds the weekday with the highest average.
- The dict carries the winner AND all the means, so the chart can draw
  every bar and highlight the best one.

The trend function compares the last 7 days against the 7 before:

```python
last_avg = df["revenue"].tail(window).mean()
prev_avg = df["revenue"].tail(window * 2).head(window).mean()
change_pct = (last_avg - prev_avg) / prev_avg * 100
direction = "up" if change_pct >= 0 else "down"
```

The comparison function sums the last two months and computes the percent
change. All three return "type" so the rest of the pipeline knows what to
draw and narrate.

## 5. Level 3: charts and the classifier

### app/charts.py

The chart reads the result dict. It never recomputes. This is grounding
in the UI.

```python
def build_chart(result: dict) -> go.Figure:
    chart_type = result.get("type")
    if chart_type == "trend":
        return _trend_chart(result)
    if chart_type == "best_day":
        return _best_day_chart(result)
    if chart_type == "comparison":
        return _comparison_chart(result)
    return None
```

Fallback returns None. No chart for a question we cannot answer. Each chart
function plots exactly the keys the analyzer produced: rolling averages for
trend, weekday means for best_day, month totals for comparison.

### app/understand.py

The classifier. The model answers with one word.

```python
_SYSTEM_PROMPT = (
    "You classify sales questions into exactly one type. "
    "Types: trend, best_day, comparison, fallback. "
    "trend: revenue going up or down over time. "
    "best_day: which weekday earns the most. "
    "comparison: one month or period against another. "
    "fallback: anything else, including product or category questions. "
    "Reply with a single word: trend, best_day, comparison, or fallback."
)
```

Then a validator turns the reply into a safe type. Anything unexpected
becomes fallback:

```python
def _validate(raw: str) -> str:
    text = str(raw or "").strip().lower()
    first_word = text.split()[0] if text else ""
    first_word = first_word.strip(".,!?")
    if first_word in VALID_TYPES:
        return first_word
    return FALLBACK
```

This is the safety net. A model that replies "comparison." with a period,
or "I think comparison", still lands on comparison. A model that replies
garbage lands on fallback. The app never crashes.

## 6. Level 4: insights and pipeline

### app/insights.py

The insight prompt lists the exact pandas numbers and forbids others:

```python
if result["type"] == "best_day":
    return (
        "Write 2 plain sentences about sales for a business owner. "
        "Use only these facts. "
        f"Best weekday: {result['best_day']} with average revenue "
        f"{result['avg_revenue']}. "
        "Say which day is best and give its average revenue. "
        "No other numbers."
    )
```

The fallback is also grounded. If the model dies, the canned sentence still
carries the pandas numbers:

```python
def _fallback_for(result: dict) -> str:
    if result["type"] == "best_day":
        return (
            f"The best weekday was {result['best_day']} with an average "
            f"of {result['avg_revenue']}."
        )
```

### app/pipeline.py

The thread that joins everything:

```python
def answer_question(question: str, df=None) -> dict:
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
```

One function, one answer. The pieces stay pure. The pipeline only threads
them together. This is the module contract from the API spec.

## 7. Level 5: the UI

### frontend/streamlit_app.py

The Executive Desk theme: warm paper background, gold accent, serif
headings. You picked it from three static sketches.

Three parts:

- KPI cards across the top, every number from pandas
- Left panel: chart of the latest answer, or the default weekday view
- Right panel: example chips, the question thread, the ask form

Key patterns:

```python
@st.cache_data
def get_sales():
    return load_sales()
```

The data loads once, then Streamlit caches it. No re-read on every rerun.

```python
with st.form("ask_form", clear_on_submit=True):
    question = st.text_input(...)
    submitted = st.form_submit_button("Ask", ...)
```

The form submits on Enter or button click. `run_question` calls the
pipeline, stores the answer in `st.session_state`, then reruns. Session
state keeps the thread across reruns.

Grounding holds in the UI. The default view calls `analyze(df, "best_day")`
directly, no LLM. The thread shows a `numbers:` line under every answer,
straight from the result dict. The LLM never touches the page until you
ask a question.

## 8. The failover chain (app/llm.py)

Added after the free tier hit its daily cap. The app no longer depends on
one model.

```python
def build_chain() -> list:
    chain = []
    or_key = os.getenv("OPENROUTER_API_KEY")
    if or_key:
        chain.append(_client(os.getenv("LLM_MODEL", DEFAULT_MODEL),
                             or_key, OPENROUTER_BASE, 30))
        model2 = os.getenv("LLM_MODEL2", DEFAULT_MODEL2)
        if model2 != os.getenv("LLM_MODEL", DEFAULT_MODEL):
            chain.append(_client(model2, or_key, OPENROUTER_BASE, 20))
    gem_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if gem_key:
        chain.append(_client(os.getenv("LLM_MODEL3", DEFAULT_MODEL3),
                             gem_key, GEMINI_BASE, 15))
    return chain
```

Three slots, shrinking timeouts: 30, 20, 15 seconds. A dead slot fails in
about a second and the chain moves on.

```python
def first_reply(prompt: str, chain: list) -> str:
    for llm in chain:
        try:
            reply = llm.invoke(prompt)
            text = (reply.content or "").strip()
            if text:
                return text
        except Exception:
            continue
    return ""
```

understand.py and insights.py both call this through `latest_reply`. When
every slot fails, they fall back to the canned grounded answer.

## 9. Tests

28 tests, all network-free except the smoke test. The trick: every function
accepts an `llm` parameter. Tests pass a fake LLM, so the model is never
called.

```python
class _FakeReply:
    def __init__(self, content):
        self.content = content

class _Raises:
    def invoke(self, prompt):
        raise RuntimeError("provider down")
```

The chain tests prove: first reply wins, a failing slot is skipped, an
empty reply is skipped, all-fail returns empty.

Run them: `python -m pytest`

## 10. Deployment

Two surfaces, both free.

- GitHub Pages hosts the README and docs. Enabled in repo Settings.
- Streamlit Cloud runs the app. Connected to the GitHub repo, main branch,
  entry file frontend/streamlit_app.py. Every push to main redeploys.

Cloud requirements that were hard-won:

- `requirements.txt` pinned to exact tested versions.
- Data path resolved from the file location, not the working folder.
- The API key lives in Settings, Secrets on Streamlit Cloud. Never in the
  repo.

The free tier sleeps on idle. First visit after sleep takes about 30
seconds to wake. That is expected, not a bug.

## 11. The numbers that matter

From the committed 365-day data:

- Best day: Thursday, average 2,423.10
- Trend: last 7 days 2,196.51 vs previous 1,626.35, +35.06%, up
- Comparison: December 16,647.04 vs November 17,407.27, -4.37%

Every answer in the app traces to these pandas outputs.

## 12. Interview talking points

- Grounding: the LLM narrates, pandas computes, charts read the same dict.
- Four seeded question types plus a graceful fallback.
- Failover chain: three model slots, timeouts 30/20/15, never hangs.
- 28 tests, network-free, fake LLM injection.
- Real data, real deployment, public URL, benchmark question bank.
- OpenRouter free model with a paid escape hatch.

## 13. What we did not build

- Top product: the daily series has no product column. The analyzer is
  stubbed as fallback. Adding it needs product-level data.
- Multi-turn conversation: each question is independent. The thread in the
  UI is a history, not context the model uses.
- Authentication: the app is public by design.

These are honest gaps, ready for a "what would you add next?" interview
answer.
