# Architecture

**Project:** AI Sales Insights Copilot

## Overview

The system runs a pipeline. A user types a question. The pipeline classifies the question, computes the answer with pandas, builds a Plotly chart, and writes a plain-language insight with the LLM.

The rule that holds everything together is grounding. All numbers come from pandas. The LLM writes prose only and never computes. The chart reads the pandas result, so chart and numbers always agree.

## Data Flow

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

Interactive version: `assets/architecture-diagram.html`.

## Components

| Module | File | Responsibility |
|---|---|---|
| Data | app/data.py | Read or generate sales data |
| Understand | app/understand.py | Classify a question into a type |
| Analyze | app/analyze.py | Compute the answer per type |
| Charts | app/charts.py | Build the Plotly chart |
| Insights | app/insights.py | Write the insight and weekly narrative |
| Pipeline | app/pipeline.py | Compose all steps end to end |

## Design Decisions

| Decision | Reason |
|---|---|
| LLM never computes | Grounding keeps the answer honest |
| Chart from pandas output | Chart and numbers always agree |
| Question types limited | Predictable, reliable demo |
| Synthetic data | No live connection, no fake real data |
| gpt-4o-mini | Cheap and strong for this job |

## Sequence

1. Streamlit receives the typed question.
2. `understand.py` classifies it into a seeded type.
3. `analyze.py` computes the numbers with pandas.
4. `charts.py` plots those numbers with Plotly.
5. `insights.py` asks the LLM to write the insight from those numbers.
6. Streamlit renders the chart, the numbers, and the insight.

## Configuration

Settings come from `.env`. See `docs/CONFIGURATION.md`.