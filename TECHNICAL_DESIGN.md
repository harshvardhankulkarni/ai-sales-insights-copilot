# Technical Design Document

**Project:** AI Sales Insights Copilot
**Owner:** Harsh Kulkarni
**Version:** 1.0
**Repo:** AI-Sales-Insights-Copilot

---

## 1. Overview

The system is a pipeline. A user types a question. The pipeline classifies the question, computes an answer with pandas, builds a Plotly chart from that answer, and asks the LLM to write a plain-language insight. The answer is the chart, the numbers, and the insight.

The core constraint is grounding. All numbers come from pandas. The LLM only writes prose. The chart is built from the same pandas numbers, so chart and numbers always agree.

## 2. Data Flow

```
Synthetic sales data (180 days)
        |
        v
[NL Question Handler]  classify question type
        |                  (trend, best day, comparison, top product)
        v
[Analysis Engine]  pandas computes the answer
        |
        v
[Chart Builder]  Plotly chart from the analysis numbers
        |
        v
[Insight Writer (LLM)]  plain-language insight from the numbers
        |
        v
Answer = chart + insight + numbers

Weekly auto-insight path:
[Data summary] ---> [LLM weekly narrative] ---> [stored insight]
```

## 3. Architecture Diagram

View the interactive SVG flow in `assets/architecture-diagram.html`.

## 4. Component Table

| Module | File | Role | Tech |
|---|---|---|---|
| Data | app/data.py | Read or generate sales data | pandas, numpy |
| Understand | app/understand.py | Classify a question into a type | LangChain, OpenAI |
| Analyze | app/analyze.py | Compute the answer per type | pandas, numpy |
| Charts | app/charts.py | Build the Plotly chart | plotly |
| Insights | app/insights.py | Write the insight and weekly narrative | LangChain, OpenAI |
| Pipeline | app/pipeline.py | Compose understand, analyze, chart, insight | Python |

Supporting:
- `scripts/generate_sales.py`: create the synthetic CSV.
- `frontend/streamlit_app.py`: the chat and monitor UI.
- `tests/test_analyze.py`: pytest for the analysis engine.

## 5. Module Responsibilities

### data.py
Load `data/sales.csv`. If missing, generate 180 days of synthetic sales with trend, weekly seasonality, and noise. Return a pandas DataFrame with a date index and a daily revenue column.

### understand.py
Take a question string. Ask the LLM to classify it into one of the seeded types: trend, best day, comparison, top product. Return a type label plus the original question. For unknown types, return a fallback label.

### analyze.py
Take the data and a type. Run the matching pandas operation.
- trend: rolling average and revenue over a window.
- best day: mean revenue per day of week.
- comparison: compare two periods or regions.
- top product: rank products by revenue.
Return a dict of computed numbers. No LLM call here.

### charts.py
Take the analysis numbers and type. Return a Plotly figure that matches those numbers. One chart per answer.

### insights.py
Take the computed numbers. Pass them to the LLM with a short prompt that asks for a plain-language insight and forbids new numbers. Return the insight text. Also write a weekly narrative from weekly aggregates.

### pipeline.py
`answer_question(question)` composes:
1. classify via understand.
2. analyze via analyze.
3. chart via charts.
4. insight via insights.
Return a dict with type, numbers, chart, and insight.

## 6. Design Decisions

| Decision | Reason |
|---|---|
| LLM never computes | Grounding keeps the answer honest. Prose only. |
| Chart from pandas output | Chart and numbers always agree. |
| Question types limited | Predictable, reliable demo. |
| Synthetic data | No live connection, no fake real data. |
| Single answer pattern | One chart plus insight, the copilot feel. |
| gpt-4o-mini | Cheap and strong enough for classification and insight. |
| Functional modules | Each file has one job, easy to test and learn. |

## 7. File Organization

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
data/sales.csv
docs/
```

The reporter chain reads clean: understand names a type, analyze math the numbers, charts plot them, insights write the story. Each step passes data to the next with no hidden LLM calls.

## 8. Non-Goals in Code

- No HTTP API server.
- No database layer.
- No auth.
- No free-form question parser.

## 9. Configuration

Settings live in `.env`.
- OPENAI_API_KEY: the secret.
- LLM_MODEL: default gpt-4o-mini.
- SALES_DAYS: default 180.

Load them with python-dotenv at app start.