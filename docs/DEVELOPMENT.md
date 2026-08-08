# Development

**Project:** AI Sales Insights Copilot

## Build Milestones

The project follows ROADMAP.md, five levels, one at a time. This page records how each piece is built and how to keep it healthy.

### Level 1: Basics
- Learn grounding: pandas computes, the LLM writes prose only.
- Learn question classification: exactly 4 types plus fallback.

### Level 2: Setup and Data Engine
- `venv/` with Python 3.11.15, requirements.txt.
- `scripts/generate_sales.py`: builds 365 days from the raw Superstore CSV.
- `app/data.py`: `load_sales()` reads `data/sales.csv`.
- `app/analyze.py`: one pandas function per type. Trend, best_day, comparison.

### Level 3: Charts and NL handling
- `app/charts.py`: `build_chart(result)` plots the pandas numbers. It never computes.
- `app/understand.py`: `classify_question(question)` returns one type via the LLM.

### Level 4: Insights and pipeline
- `app/insights.py`: `write_insight(result)` and `write_weekly_insight(df)`. The model narrates numbers that pandas already computed.
- `app/pipeline.py`: `answer_question(question)` runs classify, analyze, chart, insight.

### Level 5: UI and finalize
- `sketches/`: 3 theme options. Executive Desk chosen by the user.
- `frontend/streamlit_app.py`: the chosen theme. KPIs, charts, ask panel, weekly expander.
- Docs, push, Pages.

## Coding Rules

- All numbers come from pandas. The LLM never computes.
- The chart reads the pandas result only. No math in charts.
- Every LLM call has `request_timeout=30` and `max_retries=1`. A slow model must degrade to the fallback, never hang.
- Constructor calls happen inside try blocks. A missing key yields a fallback, not a crash.
- Question types stay: trend, best_day, comparison, fallback.
- `.env` holds keys. Never commit it.

## Module Contract

| Module | Input | Output |
|---|---|---|
| data.py | path | DataFrame with date, revenue, units |
| understand.py | question string | {"type": ..., "question": ...} |
| analyze.py | DataFrame, type | dict of numbers with plot series |
| charts.py | dict of numbers | Plotly Figure, or None for fallback |
| insights.py | dict of numbers | insight string |
| pipeline.py | question string | dict: type, result, chart, insight |

## Project Layout

```
app/
  __init__.py
  data.py
  understand.py
  analyze.py
  charts.py
  insights.py
  pipeline.py
frontend/streamlit_app.py
scripts/generate_sales.py
scripts/smoke_test.py
scripts/verify_app.py
tests/test_analyze.py, test_understand.py, test_insights.py, test_pipeline.py
data/sales.csv
data/raw/superstore-sales.csv (gitignored)
sketches/
docs/
```

## Code Style

- Short functions with one job.
- Type hints on public functions.
- Docstrings on public functions.
- No secrets in code. Read them from `.env`.

## Commit Workflow

```bash
git add .
git commit -m "feat: describe the change"
git push origin main
```

Use messages like `feat:`, `fix:`, `docs:`, `test:`.

## Review Checklist Before Push

- [ ] `.env` is git-ignored: `git check-ignore .env` prints `.env`.
- [ ] `data/sales.csv` exists and loads.
- [ ] `analyze.py` answers trend, best_day, comparison.
- [ ] Charts match the numbers: extract plotted values, compare to the result dict.
- [ ] The LLM writes prose only.
- [ ] `python -m pytest` passes (22 tests).
- [ ] `python scripts/smoke_test.py` ends with 0 failed.