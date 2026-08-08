# Architecture

**Project:** AI Sales Insights Copilot

## Overview

The system is a pipeline. A user types a question. The pipeline classifies it, computes the answer with pandas, builds a Plotly chart, and asks the LLM to narrate the numbers.

The core rule is grounding. All numbers come from pandas. The LLM writes prose only and never computes. The chart reads the pandas result, so chart and numbers always agree.

## Data

`data/sales.csv`: 365 rows of daily revenue, derived from the real Tableau Superstore dataset. Loaded by `app/data.py`.

## Data Flow

```
data/sales.csv (365 days, committed)
        |
        v
[NL Question Handler]  classify question type
        |                  (trend, best_day, comparison, fallback)
        v
[Analysis Engine]  pandas computes the answer
        |
        v
[Chart Builder]  Plotly chart from the analysis numbers
        |
        v
[Insight Writer (LLM)]  plain-language insight from those numbers
        |
        v
Answer = chart + numbers + insight

Weekly auto-insight path:
[pandas weekly totals] ---> [LLM narrative] ---> [shown in UI]
```

Interactive version: `assets/architecture-diagram.html`.

## Components

| Module | File | Responsibility |
|---|---|---|
| Data | app/data.py | Load the sales DataFrame |
| Understand | app/understand.py | Classify a question into a type |
| Analyze | app/analyze.py | Compute the answer with pandas |
| Charts | app/charts.py | Build the Plotly chart from the result |
| Insights | app/insights.py | Write the insight and weekly narrative |
| Pipeline | app/pipeline.py | Compose all steps end to end |
| Frontend | frontend/streamlit_app.py | Streamlit UI, Executive Desk theme |

## Design Decisions

| Decision | Reason |
|---|---|
| LLM never computes | Grounding keeps the answer honest |
| Chart from pandas output | Chart and numbers always agree |
| Question types limited | Predictable, reliable demo |
| Every LLM call capped at 30s | A slow free model degrades, never hangs |
| Model construction in try blocks | Missing key yields fallback, not crash |
| OpenRouter free model | Zero cost, still a real LLM call |

## Sequence

1. Streamlit receives the typed question.
2. `understand.py` classifies it into a seeded type.
3. `analyze.py` computes the numbers with pandas.
4. `charts.py` plots those numbers with Plotly.
5. `insights.py` asks the LLM to write the insight from those numbers.
6. Streamlit renders the chart, the numbers, and the insight.

## Configuration

Settings come from `.env`. See `docs/CONFIGURATION.md`.