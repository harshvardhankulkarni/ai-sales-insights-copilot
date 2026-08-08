# Development

**Project:** AI Sales Insights Copilot

## Build Milestones

Each milestone ends with a working, runnable output.

### M1 Data and Analysis Engine
- Write `scripts/generate_sales.py`. Generate 180 days with trend, weekly seasonality, and noise.
- Write `app/data.py`. Load or generate the DataFrame.
- Write `app/analyze.py`. One pandas function per type: trend, best day, comparison, top product.
- Verify the numbers with quick prints.

### M2 Charts
- Write `app/charts.py`. One Plotly chart per type.
- Confirm the chart values equal the pandas output.

### M3 NL Question Handler
- Write `app/understand.py`. Classify a question into a seeded type with the LLM.
- Return a fallback for unknown questions.

### M4 Insight Writer
- Write `app/insights.py`. Pass computed numbers to the LLM and get prose back.
- Write `app/pipeline.py`. Compose understand, analyze, chart, and insight.
- Test one full answer.

### M5 Streamlit Copilot UI
- Write `frontend/streamlit_app.py`. Chat input, chart output, insight beside it.
- Add 5 seeded example questions.

### M6 Docs and GitHub
- Finish the 6 GSD docs.
- Push the repo. Enable Pages.

## Coding Rules

- All numbers come from pandas. The LLM never computes.
- The chart reads the pandas result only.
- Keep question types limited to the 4 seeded types.
- Synthetic data only in the repo.
- Match the old `sales-dashboard` spirit. Do not copy old code.

## Module Contract

| Module | Input | Output |
|---|---|---|
| data.py | path, days | DataFrame with date and revenue |
| understand.py | question string | type label |
| analyze.py | DataFrame, type | dict of numbers |
| charts.py | dict of numbers | Plotly Figure |
| insights.py | dict of numbers | insight string |
| pipeline.py | question string | answer dict with type, result, chart, insight |

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
scripts/generate_sales.py
frontend/streamlit_app.py
tests/test_analyze.py
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

- [ ] `.env` is not committed.
- [ ] `generate_sales.py` produces repeatable data.
- [ ] `analyze.py` answers all 4 types.
- [ ] Charts match the numbers.
- [ ] The LLM writes prose only.
- [ ] A seeded question works in Streamlit.
- [ ] Tests pass with `python -m pytest`.