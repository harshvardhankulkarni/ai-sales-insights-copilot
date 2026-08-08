# Business Requirements Document

**Project:** AI Sales Insights Copilot
**Owner:** Harsh Kulkarni
**Version:** 1.0
**Repo:** AI-Sales-Insights-Copilot

---

## 1. Executive Summary

Business users want answers, not tables. This project rebuilds the old sales dashboard from scratch and adds an AI layer. A user types a question, for example "what was our best day of the week?". The system runs the analysis, builds a chart, and writes a plain-language insight. A weekly auto-insight also reads the week and writes a summary.

The result is a demo of the AI BI copilot pattern, the trend hiring managers ask about for analyst and BI roles.

## 2. Business Problem

The current sales dashboard shows numbers and charts. A manager must read the chart and build the story herself. That step takes time and skill.

The copilot removes that step. The user asks a question. The system does the math in pandas, shows the chart, and writes the story. The manager gets a decision-ready answer.

## 3. Stakeholders

| Stakeholder | Interest | Use |
|---|---|---|
| Sales managers | Answer "why" behind the number | Ask questions, read insights |
| Business teams | Daily sales answers without SQL | Ask questions, read weekly notes |
| Harsh | Show BI + GenAI skills | Demo, resume, interview |

## 4. Goals

**Business goals**
- Turn the sales dashboard into a copilot you ask questions to.
- Deliver analysis plus a written insight for each question.
- Produce a weekly written auto-insight.

**Learning goals**
- Build time series analysis with pandas.
- Add a natural language layer with an LLM.
- Keep the LLM grounded: it writes, never computes.
- Deliver Streamlit chat plus Plotly charts.

## 5. Success Metrics

| Metric | Target | How measured |
|---|---|---|
| Answer correctness | Numbers match pandas output | Review test cases |
| Grounding | Insight uses computed numbers only | Manual test |
| Chart agreement | Chart values equal the pandas numbers | Manual test |
| Coverage | 4 seeded question types always answer | Manual test |
| Shop reliability | No crash on a seeded question | Manual run |

## 6. Scope

**In scope**
- Synthetic sales data from 180 days.
- Natural language question handling with 4 question types.
- pandas analysis engine.
- Plotly chart builder.
- LLM insight writer.
- Weekly auto-insight.
- Streamlit chat UI.
- 6 GSD docs and README.
- GitHub push and Pages.

**Out of scope**
- Live sales connection to a real database.
- Production authentication.
- Broad free-form natural language questions.
- Mobile native app.
- LLM that computes numbers.

## 7. Business Rules

- All numbers come from pandas. The LLM writes prose only.
- The chart is built from the same pandas numbers.
- Question types stay limited to keep the demo reliable.
- Data is synthetic. Never put fake real company numbers in the repo.
- The repo UI is unique to this project. No shared theme.

## 8. Constraints

- Python 3.11 or higher.
- OpenAI API key required for insight writing.
- Local run only. No production hosting.

## 9. Risks

| Risk | Mitigation |
|---|---|
| LLM guesses numbers | Ground it: pass computed numbers only |
| LLM API cost | Use gpt-4o-mini, the cheap model |
| Broad question breaks the demo | Keep question types seeded and limited |
| Chart disagrees with analysis | Build the chart from pandas output only |
| Synthetic data goes stale | Regenerate on load with a seeded generator |