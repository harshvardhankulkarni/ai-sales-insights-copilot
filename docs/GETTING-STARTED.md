# Getting Started

**Project:** AI Sales Insights Copilot

## Prerequisites

- Python 3.11 or higher.
- An OpenAI API key.
- Git.

## 1. Clone

```bash
git clone https://github.com/harshvardhankulkarni/AI-Sales-Insights-Copilot.git
cd AI-Sales-Insights-Copilot
```

## 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your key.

```
OPENAI_API_KEY=sk-your-key-here
LLM_MODEL=gpt-4o-mini
SALES_DAYS=180
```

Never commit `.env`.

## 5. Generate Sales Data

```bash
mkdir -p data
python scripts/generate_sales.py
```

This writes `data/sales.csv` with about 180 rows of synthetic daily sales.

## 6. Run the App

```bash
streamlit run frontend/streamlit_app.py
```

Open `http://localhost:8501`.

## 7. Ask a Question

Click a seeded example question or type your own.

- "what was our best day of the week for revenue?"
- "is revenue going up over the last 30 days?"
- "how does this month compare to last month?"
- "which product sold the most?"

You get one chart, the numbers, and a written insight.

## 8. Run the Tests

```bash
python -m pytest
```

## Troubleshooting

**Missing API key.** Streamlit shows a key error. Add `OPENAI_API_KEY` to `.env` and restart.

**No sales.csv.** Run `python scripts/generate_sales.py` first.

**Port in use.** Streamlit picks another port. Read the terminal output.

## Next

Read `docs/ARCHITECTURE.md` for the data flow and `docs/CONFIGURATION.md` for all settings.