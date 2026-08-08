# Learning Journey

> Read `Learning-Journey-Overview.md` at the AI Projects root first. It shows
> what you learn, how you prove it, and how each project lands you a job.

**Project:** AI Sales Insights Copilot
**Owner:** Harsh Kulkarni

This project teaches you, a beginner, the full AI BI copilot pattern. Each milestone ends with a working output and a set of concepts with examples. Read the concept, then ask your AI co-pilot to show you one example in code.

## 1. Before You Start

You will learn two tracks.

- Data and BI: pandas time series, rolling averages, day of week, charts.
- AI: NL question classification, grounding, prompt engineering, auto-insights.

## 2. Glossary (define first)

Define these words before you build so the rest makes sense.

- **Natural language query (NL query).** A question typed in plain words. For example "what was our best day of the week?". The computer reads it like a sentence, not like code.
- **Classification.** The step that decides which seeded question type a typed query matches. The classifier maps "which product sold most?" to the type `top_product`.
- **Grounding.** Building the answer on facts the system already computed, not on guesses the model makes up. Here it means the LLM writes prose and never computes numbers. The numbers come from pandas.
- **Insight.** A short written explanation of what the numbers mean. The LLM turns a table into one readable sentence for a busy manager.
- **Rolling average.** The average of a moving window. For yesterday, the average of the last 7 days. It smooths noise and shows the trend.
- **Seed.** The starting point for a random generator. A seeded generator gives the same data each run, so tests stay repeatable.

## 3. Per-Milestone Learning Goals

### M1 Data and Analysis Engine
**Goals**
- Make a pandas DataFrame from generated rows.
- Use numpy for trend and noise.
- Group sales by day of week.
- Compare two periods.

**Concepts** DataFrame, Series, groupby, mean, rolling mean, synthetic data.

### M2 Charts
**Goals**
- Use Plotly in Python.
- Draw a line chart for trend.
- Draw a bar chart for the best day.

**Concepts** plotly graph_objects, layout, axis title.

### M3 NL Question Handler
**Goals**
- Prompt the LLM to classify a question into a type.
- Constrain the output to trusted types.

**Concepts** classification prompt, structured output, a seeded set.

### M4 Insight Writer
**Goals**
- Send computed numbers to the LLM.
- Get a short plain narrative back.
- Keep the LLM grounded. It never computes.

**Concepts** prompt engineering, grounding, gpt-4o-mini, chunk budget.

### M5 Streamlit Copilot UI
**Goals**
- Render a chat bar.
- Show one chart and one insight per answer.
- Seed 5 examples.

**Concepts** streamlit widgets, rerun, session state basics.

### M6 Docs and GitHub
**Goals**
- Write 6 GSD docs.
- Push to GitHub.
- Enable Pages.

**Concepts** git init, commit, push, Pages source.

## 4. Progress Log

Fill out after each milestone.

| Milestone | Date | Checkpoint | Next step |
|---|---|---|---|
| M1 Data and analysis | | analysis returns correct numbers | charts |
| M2 Charts | | chart matches numbers | NL handler |
| M3 NL handler | | classifies 4 types | insight writer |
| M4 Insight writer | | grounded narrative | Streamlit UI |
| M5 UI | | chat answers with chart | docs |
| M6 Docs and GitHub | | repo and Pages live | done |

## 5. Questions to Ask the AI Co-Pilot

- "Work me a pandas rolling average on this DataFrame, explain each line."
- "Why does the LLM never compute numbers? Show a bad example."
- "How do I build a Plotly bar chart that reads the pandas result only?"
- "Show how to classify a question into one of 4 seed types with LangChain."
- "How load prompt output into a safe, structured value?"
- "Why do I keep question types limited for the demo?"
- "Show a test that checks the insight uses only the passed numbers."
- "Give me a line a streamlit st.selectbox for 5 sample questions."

## 6. Keep This in Mind

- The chart and the answer always agree because both come from pandas.
- The LLM is a writer, not a calculator.
- Synthetic data is fine for the demo. Never put real company numbers in the repo.
- The recruiter story is "I turned my dashboard into a copilot."