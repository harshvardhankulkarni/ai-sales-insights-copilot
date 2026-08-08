# User Guide

**Project:** AI Sales Insights Copilot
**Owner:** Harsh Kulkarni

## 1. Who Uses This

- A sales manager who wants the story behind the number.
- A business team that wants daily sales answers without writing SQL or reading charts.
- Harsh, who built it, to show BI plus GenAI in one screen.

You are the audience. You type a plain question and get a chart, the numbers, and a short written insight.

## 2. Before You Start

You need these:
- Python 3.11 or higher.
- An OpenAI API key.
- Git (only for sharing to GitHub).

## 3. Setup

Open a terminal in the project folder.

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Open `.env` and add your OpenAI key.

```
OPENAI_API_KEY=sk-your-key-here
```

Generate the sales data.

```bash
mkdir -p data
python scripts/generate_sales.py
```

## 4. How to Run

```bash
streamlit run frontend/streamlit_app.py
```

A browser tab opens on `localhost:8501`. The app shows a monitor area and a chat bar.

## 5. Ask a Question

Type a question in the chat bar and press Enter. Start with a seeded example. The app provides 5 examples you click once.

Sample questions:
- "what was our best day of the week for revenue?"
- "is revenue going up over the last 30 days?"
- "how does this month compare to last month?"
- "which product sold the most?"
- "what is the 7 day rolling average trend?"

## 6. What an Answer Looks Like

Ask "what was our best day of the week for revenue?". The app returns three parts:

1. The numbers. For example "Saturday, average revenue 1870.3".
2. One interactive Plotly chart. A bar chart by day of week.
3. A written insight. For example "Revenue peaks on Saturday with an average of 1870.3. The weekend drives most of the week."

The numbers come from pandas. The chart matches those numbers. The insight is written by the LLM from those same numbers.

## 7. Weekly Auto-Insight

The app also writes a weekly narrative. It reads the last week of daily sales, summarizes by day, and asks the LLM for a plain-language summary. You read that summary without asking a question.

## 8. Question Types

Seeded types keep the demo reliable.

| Type | Sample question |
|---|---|
| trend | is revenue going up or down over 30 days? |
| best day | what is the best day of the week? |
| comparison | how does this month compare to last month? |
| top product | which product sold the most? |

A question outside these types returns a friendly fallback message. The limit keeps the demo predictable.

## 9. Notes for Trust

- All numbers come from pandas. The LLM never computes.
- The chart is built from the same numbers, so chart and answer always agree.