# AI Memory

Read this file first. It gives a fresh AI tool the full project context so it starts building without asking questions. This is the single entry file for any agent or co-pilot working on this project.

---

## 1. Project Identity

**Name:** AI Sales Insights Copilot
**Repo:** `AI-Sales-Insights-Copilot`
**GitHub user:** `harshvardhankulkarni`
**Pages URL:** `https://harshvardhankulkarni.github.io/AI-Sales-Insights-Copilot/`
**Owner:** Harsh Kulkarni
**Role target:** Data Analyst / BI + GenAI

**One line:** A Streamlit sales dashboard, rebuilt from scratch, with a natural language layer. A user types "what was our best day of the week?" and gets the analysis, a chart, and a written insight from one question.

WHICH DATA TO USE: sales data in `data/raw/superstore-sales.csv` (real, 9,800 orders). Run `scripts/generate_sales.py` to build `data/sales.csv` (365-day daily series). The app and charts read `sales.csv`. See `DATA_SOURCE.md`.

---

## 2. Why, Who, When

**Why we build this**
- AI BI is a top industry trend. Business users want answers, not tables.
- Hiring managers for BI and analyst roles ask about the copilot pattern. This proves you built AI on top of analytics.

**Who we build it for**
- Business and sales teams that want daily sales answers without SQL or chart reading.
- A sales manager who asks a question and wants the insight behind the number.
- You, Harsh, to show BI plus GenAI in one demo.

**When we use this**
- When a sales question arrives and the answer needs a chart, not a table.
- When a weekly report needs a written narrative, not just raw numbers.
- On a resume and at an interview for BI, dashboard, or AI analytics roles.

**Supporting fact:** This upgrades the old `sales-dashboard` repo. The build is from scratch. Never copy old code. Match the old spirit, write new code.

---

## 3. Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Language | Python 3.11+ | Standard for data and AI |
| Data | Pandas, NumPy | Analysis on sales data |
| LLM | OpenAI GPT-4o-mini | NL question understanding and insight writing |
| LLM SDK | LangChain | Prompt templating, structured output |
| Analysis | Built-in pandas functions | Aggregations, trends, day-of-week |
| UI | Streamlit | Chat and charts |
| Viz | Plotly | Interactive charts from answers |

**requirements.txt**

```
langchain
langchain-openai
openai
pandas
numpy
plotly
streamlit
python-dotenv
```

---

## 4. Environment Keys (.env)

Put these keys in `.env` at project root. Never commit `.env`.

```
OPENAI_API_KEY=sk-...
LLM_MODEL=gpt-4o-mini
SALES_DAYS=180
```

`SALES_DAYS` controls how many days of sales data load. Default 180. Primary source is `data/raw/superstore-sales.csv` (Tableau Superstore, see DATA_SOURCE.md), aggregated by `scripts/generate_sales.py` into `data/sales.csv`. If the raw file is missing, the same script creates synthetic fallback sales data.

---

## 5. Architecture Summary and Data Flow

The system does one job: turn a typed question into an answer that has numbers, a chart, and a written insight.

```
Synthetic sales data (180 days)
        |
        v
[ NL Question Handler ]  classify question type
        |                      (trend, best day, comparison, top product)
        v
[ Analysis Engine ]  pandas computes the answer
        |
Home purchase:
Socio hired professional drivers: Socio Forward, Atrix V Café, Logistics-as-a-Service
        |
[ Insight Writer (LLM) ]  plain-language insight from the numbers
        v
Answer = chart + insight + numbers

Weekly auto-insight path:
[ Data summary ] ---> [ LLM weekly narrative ] ---> [ stored insight ]
```

### Design choices (non-negotiable)

**The LLM never computes.** All numbers come from pandas. The LLM writes prose only. This is grounding. Grounding means building the answer on facts the system already computed, not on guesses the model makes up.

**The chart is built from pandas output.** So chart and numbers always agree.

**Question types are limited and predictable.** The demo stays reliable. Broad free-form questions break the demo.

---

## 6. Folder Structure

```
AI-Sales-Insights-Copilot/
|-- app/
|   |-- __init__.py
|   |-- data.py              # read or make sales data
|   |-- understand.py        # NL question classification
|   |-- analyze.py           # pandas analysis per question type
|   |-- charts.py            # Plotly charts
|   |-- insights.py          # LLM insight writer and weekly narrative
|   |-- pipeline.py          # compose understand -> analyze -> chart -> insight
| |-- data/
| |   |-- raw/                # superstore-sales.csv (real, see DATA_SOURCE.md)
| |   `-- sales.csv           # daily series (real aggregation or synthetic fallback)
|-- scripts/
|   `-- generate_sales.py  # real data -> sales.csv (synthetic fallback)
|-- frontend/
|   `-- streamlit_app.py     # chat and charts
|-- tests/
|   `-- test_analyze.py
|-- docs/
|   |-- ARCHITECTURE.md
|   |-- GETTING-STARTED.md
|   |-- DEVELOPMENT.md
|   |-- TESTING.md
|   `-- CONFIGURATION.md
|-- pyproject.toml
|-- requirements.txt
|-- .gitignore
|-- README.md
`-- .env.example
```

---

## 7. Milestones M1 to M6

Each milestone ends with a working, runnable output.

| Milestone | Deliverable | Focus |
|---|---|---|
| M1 | Data and analysis engine | Aggregate real sales from data/raw/superstore-sales.csv (see DATA_SOURCE.md) with scripts/generate_sales.py. Build data.py and analyze.py. Trend, best day, monthly comparison. Test outputs. Fallback: synthetic generator within generate_sales.py. |
| M2 | Charts | Build charts.py per analysis type. Chart matches pandas output. |
| M3 | NL question handler | Build understand.py. Classify a question into a type. 4 seeded question types. |
| M4 | Insight writer | Build insights.py. LLM writes insight from computed numbers. Wire pipeline.py end to end. |
| M5 | Streamlit copilot UI | Chat so a user asks, sees chart, numbers, insight. 5 seeded example questions. |
| M6 | Docs and GitHub | 6 GSD docs. Push repo. Enable Pages. |

---

## 8. Skills to Load

Load these Hermes skills. They speed up this build.

- `architecture-diagram`: dark SVG architecture diagrams as HTML. Use it for the architecture report.
- `claude-design`: single-page HTML design artifacts. Use it for UI options.
- `popular-web-designs`: 54 real design systems. Use it to style the UI options.
- `jupyter-live-kernel` (optional): live Python on a Jupyter kernel. Use it to explore sales data during M1.

See SKILLS.md for details.

---

## 9. Learning Goals

- Time series analysis on sales data with pandas. Rolling averages, day-of-week patterns, monthly comparison.
- Plotly chart building for business users.
- NL question classification with an LLM.
- Grounding: the LLM writes, it never computes.
- Weekly auto-insight pattern for reporting.
- Prompt engineering for business language.

---

## 10. Pitfalls

**Never let the LLM compute.** All numbers come from pandas. The LLM writes prose only.

**Keep question types limited.** Broad free-form questions break the demo.

**Real public data preferred, synthetic fallback.** Primary source is `data/raw/superstore-sales.csv` (Tableau Superstore, safe to commit). Never fake real company numbers in the repo.

**The recruiter story** is "I turned my dashboard into a copilot". Put that point in the README first.

**Do not copy old code.** The old `sales-dashboard` repo is a reference for spirit, not a source of code.

---

## 11. UI Rules (decided at build time)

Each project owns its UI. There is no shared favicon, no shared index.html, no shared dark theme. Do not copy the `customer-segmentation` UI or any existing repo UI.

- No favicon.svg or index.html is required. Build the UI at the M5 milestone only.
- On UI work, Harsh picks the theme.
- At the UI milestone, build 2 to 3 distinct UI options as HTML pages. Harsh picks one. Build only that one.
- Default direction (unless overridden): a Monitor plus Ask surface. A daily sales dashboard with KPIs and plots, plus a chat bar that interprets each chart. One chart per answer, the insight beside it.
- Show the insight clearly. Hide decoration.

---

## 12. Document Index

| File | Purpose |
|---|---|
| AI_MEMORY.md | Entry file. Read this first. Full project brain. |
| BRD.md | Business Requirements. Why the project exists. Stakeholders, goals, scope. |
| PRD.md | Product Requirements. Personas, stories, acceptance criteria. |
| TECHNICAL_DESIGN.md | Architecture, components, decisions. |
| API_SPEC.md | Interface spec for pipeline functions. |
| TEST_PLAN.md | Manual validation checklist and test cases. |
| USER_GUIDE.md | How a user runs and uses the copilot. |
| DEPLOYMENT.md | Setup, .env, git push. GitHub Pages. |
| LEARNING_JOURNEY.md | What Harsh learns each milestone. Glossary. |
| SKILLS.md | Which Hermes skills to load and why. |
| assets/architecture-diagram.html | Dark themed SVG data flow diagram. |
| DATA_SOURCE.md | Real data sources and synthetic fallback |
| docs/README.md | GSD overview. |
| docs/ARCHITECTURE.md | GSD architecture. |
| docs/GETTING-STARTED.md | GSD quick start. |
| docs/DEVELOPMENT.md | GSD contributor workflow. |
| docs/TESTING.md | GSD test guidance. |
| docs/CONFIGURATION.md | GSD setup and keys. |