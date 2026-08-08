# Product Requirements Document

**Project:** AI Sales Insights Copilot
**Owner:** Harsh Kulkarni
**Version:** 1.0
**Repo:** AI-Sales-Insights-Copilot

---

## 1. Overview

The product is a sales copilot. A business user types a natural language question about sales and gets a Plotly chart, the computed numbers, and a plain-language insight written by an LLM. The product also writes a weekly auto-insight reading the last week of data.

The key story: the user asks, the computer does the math in pandas, and the LLM explains the result in words.

**Terminology**
- Natural language question (NL query): a question typed in plain words, for example "what was our best day of the week?".
- Classification: the step that decides which of the seeded question types a query matches.
- Grounding: building the answer on numbers pandas computed, not on guesses the model makes up.
- Insight: a short written explanation of what the numbers mean.

## 2. Personas

**Sales Manager, Maya.** Wants a daily decision. Asks "which product sold most last week?". Expects a number, a chart, and one sentence about why it matters.

**Business Analyst, Raj.** Wants the trends. Asks "is revenue going up or down over 30 days?". Expects a rolling average and a clear trend line.

**Harsh, the builder.** Wants a demo that shows BI plus GenAI in one screen. Needs the pipeline to never crash on a seeded question.

## 3. User Stories

| # | Story | Priority |
|---|---|---|
| S1 | As a sales manager, I want to ask "what was the best day of the week for revenue?" so I get one number and one chart. | Must |
| S2 | As a sales manager, I want a written insight beside the chart so I understand the story. | Must |
| S3 | As a product manager, I want a 30 day revenue trend so I see direction. | Must |
| S4 | As a user, I want a weekly auto-insight so I get a summary without asking. | Should |
| S5 | As a user, I want 5 seeded example questions so I know what to type. | Should |
| S6 | As a user, I want the chart to match the numbers so I trust the answer. | Must |
| S7 | As a builder, I want the LLM to never compute so answers stay honest. | Must |

## 4. Functional Requirements

### FR1 Data generation
Load 180 days of synthetic sales from a CSV, or generate it. Columns: date, revenue, units, optional product region. A seeded generator adds a trend, weekly seasonality, and noise.

**Acceptance criteria**
- The datasource returns at least 180 rows.
- The numbers are synthetic, never real company data.

### FR2 Natural language question handling
Take a typed query. Classify it into one seeded type: trend, best day, comparison, top product. Unknown questions get a fallback message.

**Acceptance criteria**
- A question that matches a seeded type returns the right type.
- A question outside the types returns a helpful fallback, not a crash.

### FR3 Analysis engine
Use pandas for each type.
- trend: rolling average and slope over a window.
- best day of week: mean revenue per day of week.
- comparison: compare two months or two regions.
- top product: rank products by revenue.

**Acceptance criteria**
- The returned numbers equal the pandas output.
- The engine runs without the LLM. No LLM call in this step.

### FR4 Chart builder
Build a Plotly chart from the analysis numbers for each type. A line chart for trend, a bar for best day, and so on.

**Acceptance criteria**
- Chart values match the analysis numbers exactly.
- The chart is interactive in Streamlit.

### FR5 LLM insight writer
Send the computed numbers to the LLM with a prompt that asks for a short plain-language narrative. The LLM must not write new numbers.

**Acceptance criteria**
- The insight uses only the numbers passed in.
- The insight is readable, short, and business friendly.
- No computed number appears in the insight that pandas did not produce.

### FR6 Pipeline composition
Compose understand, analyze, chart, and insight into one function. Return an answer with numbers, chart, and insight.

**Acceptance criteria**
- One call returns the full answer.
- The pipeline runs end to end on a seeded question.

### FR7 Weekly auto-insight
Summarize daily revenue by week, pass the summary to the LLM, store the narrative.

**Acceptance criteria**
- The weekly narrative uses the weekly computed summary.
- The insight is saved to a local file or view.

### FR8 Streamlit UI
A chat bar plus a monitor area. The user types a question, sees the answer with one chart and the insight beside it. Provide 5 seeded example questions.

**Acceptance criteria**
- A seeded question returns chart plus numbers plus insight.
- The UI shows the insight clearly and hides decoration.

## 5. Non-Functional Requirements

### NFR1 Grounding
The LLM never computes. It receives computed numbers and writes prose.

### NFR2 Reliability
The demo answers all seeded questions without error.

### NFR3 Cost
Use gpt-4o-mini to keep API cost low.

### NFR4 Readability
Insight text is short and plain. No em dashes, no jargon.

### NFR5 Portability
Runs on Python 3.11+ with the listed packages. Local run only.

## 6. Out of Scope

- Live sales database connection.
- Production authentication.
- Free-form questions beyond the 4 seeded types.
- Mobile app.
- Multilingual support.

## 7. Acceptance Criteria Summary

| Criterion | Requirement |
|---|---|
| LLM never computes | FR5, NFR1 |
| Chart matches numbers | FR4, S6 |
| Question types limited | FR2, S1-S3 |
| Weekly insight exists | FR7, S4 |
| UI answers seeded question | FR6, S5 |