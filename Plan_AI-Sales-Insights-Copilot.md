# Project Plan 5 — AI Sales Insights Copilot (upgraded Sales Dashboard)

**Owner:** Harsh Kulkarni
**Role target:** Data Analyst / BI + GenAI
**Repo name:** `ai-sales-insights-copilot`
**One line:** Your Streamlit sales dashboard, rebuilt from scratch, with a natural language layer. Ask "what was our best day of the week?" and get the analysis, a chart, and a written insight, all from one question.

---

## 1. Project Overview

You already built a sales dashboard (`sales-dashboard` repo). This project rebuilds it from zero and adds the trending "AI BI" pattern: a copilot a business user talks to. The user types a question about sales data, the system runs the analysis, returns a chart, and writes a plain-language insight.

This is a rebuild from scratch, not an edit of the old repo. You learn as you build, working with an AI agent as your co-pilot for fast learning and quick output. Each build step teaches you a new skill.

This upgrade matches the strongest BI trend in 2026: dashboards you can ask questions of, instead of dashboards you read.

### Why we build this
"AI BI" is a top trend. Business users want answers, not tables. A copilot that turns a question into analysis plus insight is the exact pattern hiring managers ask about for BI and analyst roles. It proves you can build AI on top of your existing analytics strength.

### Who we build
- Business and sales teams who want daily sales answers without SQL or chart reading
- A sales manager who asks questions and wants the insight behind the number
- You (Harsh), to show BI + GenAI in one demo

### When we use this
- When a sales question arrives and the answer needs a chart, not a table
- When a weekly report needs a written insight, not just numbers
- On resume and at interview when a role asks for BI, dashboards, or AI analytics

### Project Goals
- Rebuild the sales data + dashboard from scratch
- Add natural language question handling that returns analysis + chart + insight
- Add weekly auto-insights: the LLM reads the data and writes the summary
- Ship a clean Streamlit UI and 6 GSD docs
- Push to GitHub, enable Pages

### Non-Goals
- No live sales connection. Synthetic data only, generated on load
- No production auth. Keep it a demo-scope internal copilot

---

## 2. Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Language | Python 3.11+ | Standard for data + AI |
| Data | Pandas, NumPy | Analysis on sales data |
| LLM | OpenAI GPT-4o-mini | NL query understanding + insight writing |
| LLM SDK | LangChain | Prompt templating, structured output |
| Analysis | Built-in pandas functions | Aggregations, trends, day-of-week |
| UI | Streamlit | Chat + charts |
| Viz | Plotly | Interactive charts from answers |

### requirements.txt
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

## 3. Architecture / Data Flow

```
Synthetic sales data (180 days)
        │
        ▼
[ NL Question Handler ]  classify question type
        │                      (trend, best day, comparison, top product)
        ▼
[ Analysis Engine ]  pandas computes the answer
        │
        ▼
[ Chart Builder ]  Plotly chart for the answer
        │
        ▼
[ Insight Writer (LLM) ]  plain-language insight from the numbers
        │
        ▼
Answer = chart + insight + numbers

Weekly auto-insight path:
[ Data summary ] ──► [ LLM weekly narrative ] ──► [ Stored insight ]

Design choices:
- The chart is built from pandas output, so chart and numbers always agree
- The LLM writes the insight from the computed numbers. It never computes
- Question types are limited and predictable so the demo is reliable
```

---

## 4. Configurations

`.env` at project root. Never commit `.env`.
```
OPENAI_API_KEY=sk-...
LLM_MODEL=gpt-4o-mini
SALES_DAYS=180
```

### Sample data
Generate 180 days of synthetic daily sales in `scripts/generate_sales.py` with trend, seasonality, and noise. Same spirit as the old project, written new.

---

## 5. Prerequisites

- Python 3.11+
- OpenAI API key
- Basic git + GitHub (harshvardhankulkarni)
- AI agent / coding tool as your implementation partner

Local setup:
```
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
mkdir -p data
python scripts/generate_sales.py
```

---

## 6. Project Structure

```
AI-Sales-Insights-Copilot/
├── app/
│   ├── __init__.py
│   ├── data.py              # load or generate sales data
│   ├── understand.py        # NL question classification
│   ├── analyze.py           # pandas analysis per question type
│   ├── charts.py            # Plotly charts
│   ├── insights.py          # LLM insight writer + weekly narrative
│   └── pipeline.py          # compose understand -> analyze -> chart -> insight
├── data/
│   └── sales.csv            # generated, can be .gitignore'd
├── scripts/
│   └── generate_sales.py
├── frontend/
│   └── streamlit_app.py     # chat + charts
├── tests/
│   └── test_analyze.py
├── docs/
│   ├── ARCHITECTURE.md
│   ├── GETTING-STARTED.md
│   ├── DEVELOPMENT.md
│   ├── TESTING.md
│   └── CONFIGURATION.md
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── README.md
└── .env.example
```

## 12. UI & Theme (per project, decided at build time)

Each project ships its own unique UI with its own design rules. No shared favicon, no shared index.html, no shared dark theme. Do not copy `customer-segmentation` or any existing repo's UI.

Rules:
- No favicon.svg or index.html is required. Build the UI at the UI milestone only.
- On UI work, the user tells you the theme to use.
- Use UI/design expert agents to research the latest 3D animation and web design trends matching the theme.
- Present 2-3 distinct UI options as HTML pages. User picks one; build only that.
- Show the insight clearly, hide decoration.

Default UI direction (unless overridden): a Monitor + Ask surface. A daily sales dashboard with KPIs and plots, plus a chat bar that interprets each chart. One chart per answer, the insight beside it.

---

## 7. Build Milestones

Each ends with a working, runnable output. Use the AI agent to explain each concept as you build.

**M1: Data + analysis engine**
Generate synthetic sales. Build `data.py` + `analyze.py`: trend, best day, monthly comparison. Test outputs.

**M2: Charts**
Build `charts.py` per analysis type. Confirm chart matches the pandas output.

**M3: NL question handler**
Build `understand.py`: classify a question into a type. Add 4 seeded question types.

**M4: Insight writer**
Build `insights.py`: LLM writes insight from computed numbers. Wire `pipeline.py` end to end.

**M5: Streamlit copilot UI**
Build the chat: user asks, sees chart + numbers + insight. Add 5 seeded example questions.

**M6: Docs + GitHub + Pages**
Write 6 GSD docs. Push repo, enable Pages.

---

## 8. What You'll Learn

**Data + BI skills (your primary track).**
- Time series analysis on sales data with pandas
- Rolling averages, day-of-week patterns, monthly comparison
- Plotly chart building for business users

**AI skills (the upgrade).**
- NL question classification with an LLM
- How to keep the LLM grounded: it writes, it never computes
- Weekly auto-insight pattern for reporting
- Prompt engineering for business language

---

## 9. GitHub Push

Repo: **AI-Sales-Insights-Copilot** (github.com/harshvardhankulkarni)

```
git init
git add .
git commit -m "feat: AI Sales Insights Copilot"
git branch -M main
git remote add origin https://github.com/harshvardhankulkarni/AI-Sales-Insights-Copilot.git
git push -u origin main
```

Pages: `https://harshvardhankulkarni.github.io/AI-Sales-Insights-Copilot/`. Enable on `main` root.

---

## 10. Validation / Testing

Include the 6 GSD docs. Manual checklist:
- [ ] sales data generates
- [ ] analyze.py returns correct numbers per question type
- [ ] chart matches the numbers
- [ ] LLM insight uses the computed numbers only
- [ ] Streamlit chat answers a seeded question with chart + insight

---

## 11. Pitfalls / Notes for the Next AI

- Never let the LLM compute. All numbers come from pandas. The LLM writes prose only.
- Match the spirit of the old `sales-dashboard` repo, but write it new. Do not copy old code.
- Keep question types limited so the demo is reliable. Broad free-form questions break the demo.
- Synthetic data is fine. Never fake real company numbers in the repo.
- The story for recruiters is "I turned my dashboard into a copilot". Make that the README point.