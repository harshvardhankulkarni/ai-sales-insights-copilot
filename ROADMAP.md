# Roadmap — AI Sales Insights Copilot (P5)

**How to use this file.** This is your step by step guide. It tells you what to do next and how your AI agent guides you. Read AI_MEMORY.md first. Then follow these steps one at a time.

Each step ends with a checkpoint. Do not move to the next step until the checkpoint passes.

---

## Level 1 — Basics before you build

**Goal.** Learn the core ideas so code makes sense.

| Step | What you do | How your agent guides you |
|---|---|---|
| 1.1 | Learn what a copilot is | Agent explains NL query to answer flows |
| 1.2 | Learn what grounding means here | Agent explains the LLM writes prose, pandas computes |
| 1.3 | Learn what question classification is | Agent explains limiting question types |
| 1.4 | Learn what synthetic data is | Agent explains demo data, never fake real company numbers |

**Checkpoint.** You explain grounding and why the LLM never computes. If you cannot, repeat.

## Level 2 — Setup and data engine

| Step | What | How your agent guides you |
|---|---|---|
| 2.1 | Create venv and install requirements | Agent runs commands with you, explains each |
| 2.2 | Build generate_sales.py | 180 days of synthetic sales. Agent writes it with you |
| 2.3 | Build data.py + analyze.py | Trend, best day, monthly comparison. Agent writes with you |
| 2.4 | Test analysis outputs | Agent runs and checks numbers |

**Checkpoint.** You run the analysis and see correct numbers per analysis type.

## Level 3 — Charts and NL handling

| Step | What | How your agent guides you |
|---|---|---|
| 3.1 | Build charts.py | Plotly chart per analysis type. Agent explains |
| 3.2 | Confirm chart matches numbers | Agent checks chart against pandas output |
| 3.3 | Build understand.py | Classifies a question into a type. Agent explains |
| 3.4 | Test classification on sample questions | Agent writes tests with you |

**Checkpoint.** A sample question classifies to the right type and the chart matches the numbers.

## Level 4 — Insight writer and pipeline

| Step | What | How your agent guides you |
|---|---|---|
| 4.1 | Build insights.py | LLM writes insight from computed numbers. Agent writes with you |
| 4.2 | Wire pipeline end to end | Agent runs a full question |
| 4.3 | Add weekly auto-insights | Agent explains the reporting pattern |

**Checkpoint.** A question returns chart + numbers + insight.

## Level 5 — UI and finalize (theme chosen by you)

| Step | What | How your agent guides you |
|---|---|---|
| 5.1 | Agent shows you 2-3 theme options | UI agents build each option as a page |
| 5.2 | You pick a theme | Agent builds only what you choose |
| 5.3 | Build the Streamlit chat + charts | Agent wires chat, KPIs, plots |
| 5.4 | Write the 6 GSD docs, push, enable Pages | Agent follows the plan standard |

**Checkpoint.** The repo is on GitHub, Pages works, and a question returns chart + insight in the app.

## How to ask help

Say exactly what blocks you. For example:
- "I'm stuck on 3.3, the classifier picks the wrong type."
- "Explain grounding again in one paragraph."
- "Which step comes next?"

Your agent asks you questions when a step is not clear and keeps the pace to your learning.

## Status tracker

| Step | Status | Notes |
|---|---|---|
| Level 1 basics | Pending | |
| 2.3 data + analyze | Pending | |
| 3.x charts + NL | Pending | |
| 4.x insight + pipeline | Pending | |
| 5.x UI + finalize | Pending | |