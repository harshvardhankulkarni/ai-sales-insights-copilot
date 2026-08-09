# AI Sales Insights Copilot

Ask your sales data a question. Get the numbers, the chart, and the story in plain words.

Built with pandas, Plotly, Streamlit, and an LLM. The LLM never computes. Pandas computes every number. The chart plots those exact numbers. The insight describes those numbers. All three always agree.

## How it works

Type a question like "what was our best day of the week?". The pipeline runs five steps:

1. `classify_question` names the question type: trend, best_day, comparison, or fallback.
2. `analyze` computes the answer with pandas.
3. `build_chart` plots the pandas numbers with Plotly.
4. `write_insight` asks the LLM to narrate the numbers in plain words.
5. Streamlit renders the chart, the numbers, and the insight together.

A weekly auto-insight path summarizes the last 4 weeks from pandas totals.

## Highlights

- Grounded answers. Every number comes from pandas, never from the model.
- One chart per answer, always matching the pandas result.
- 3 seeded question types plus a graceful fallback.
- Free LLM backend through OpenRouter: `openai/gpt-oss-20b:free`.
- Hard safety net: a slow or missing model degrades to a grounded fallback, never a crash.
- Failover chain: OpenRouter free, then paid tier, then Gemini, then canned. One dead model never kills the app.
- 28 automated tests plus a full end-to-end smoke test.

## Tech stack

Python 3.11, pandas, numpy, Plotly, Streamlit, LangChain, OpenRouter (gpt-oss-20b:free).

## Repo layout

```
app/            core pipeline: data, understand, analyze, charts, insights, pipeline
frontend/       streamlit_app.py (Executive Desk theme)
scripts/        generate_sales.py, smoke_test.py, verify_app.py
tests/          28 pytest tests
data/sales.csv  365 days of revenue, real Superstore-derived numbers
sketches/       3 UI themes; Executive Desk was chosen and built
docs/           GSD documentation set
assets/         architecture diagram
```

## Quick start

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # add your OPENROUTER_API_KEY
streamlit run frontend/streamlit_app.py
```

Open http://localhost:8501. Data is committed, no generation needed.

## The app

Live demo: https://ai-sales-insights-copilot.streamlit.app/

![Executive Desk theme](assets/screenshot.png)

## Verify

```bash
python -m pytest                              # 22 unit tests, fast, offline
python scripts/smoke_test.py                  # full live pipeline test, minutes
```

## Documentation

- `docs/GETTING-STARTED.md`: setup step by step.
- `docs/ARCHITECTURE.md`: data flow and design rules.
- `docs/DEVELOPMENT.md`: build workflow and milestones.
- `docs/TESTING.md`: tests and manual checklist.
- `docs/CONFIGURATION.md`: environment keys and defaults.
- `docs/WALKTHROUGH.md`: what we learned, step-by-step build, code explained.
- `BENCHMARK.md`: the question bank with expected answers.

## Project state

Levels 1 to 5 complete. See ROADMAP.md for the full ladder.

## Notes from Harsh

I built this with an AI coding partner. The structure, the fixes, and the
decisions are mine. The AI drafted code, I reviewed and shipped every line.
I can walk through any part of this in an interview.

What I actually learned while building:

**Grounding is not a rule, it is the whole app.** My first idea was to let
the LLM answer questions directly. That would have invented numbers. So I
made pandas the only calculator. The model gets a result dict, not the raw
data. It writes sentences about numbers that already exist. The chart reads
the same dict. Nothing can disagree. This was the first concept I had to
really rewire my head around.

**Models lie about reliability.** OpenAI gave me a 401. Gemini gave me 429
with no quota. OpenRouter free tier gave me 50 requests a day and then
stopped. My app had to survive all of that. It does. A dead model becomes
a grounded fallback with real pandas numbers. No hang, no crash, no invented
math. The user still gets a correct answer.

**Slow models are worse than dead ones.** The free model once hung for over
a minute. A hung call looks exactly like a broken app. I added a hard
timeout on every call. Now the app answers in seconds or falls back
without waiting forever.

**Free tiers are a demo story.** My live URL is on the free tier. It sleeps
when idle and wakes in about 30 seconds. First visit after sleep always
logs. That is expected. Everyone on the free tier hits it.

**Real data makes a demo honest.** The CSV is 365 days made from real
Tableau Superstore orders. I did not invent numbers. A recruiter can verify
any value in the app against the data file.

**The hard part is not the model. It is the data.** Writing the prompt was
easy. Making pandas, Plotly, and the LLM agree on every number took most of
the effort. That is the real BI skill.

I would redo nothing except start faster. Next project: an agent that reads
documents, not a single CSV.