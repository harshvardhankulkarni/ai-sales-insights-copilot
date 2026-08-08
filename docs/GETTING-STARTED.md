# Getting Started

**Project:** AI Sales Insights Copilot

## Prerequisites

- Python 3.11 or higher.
- An OpenRouter API key. Get one at https://openrouter.ai/keys.
- Git.

## 1. Clone or open the folder

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

Edit `.env` and add your key. The file needs two lines:

```
OPENROUTER_API_KEY=your-key-here
LLM_MODEL=openai/gpt-oss-20b:free
```

Never commit `.env`. The `.gitignore` blocks it.

No OpenAI key needed. The app talks to OpenRouter, which hosts free models.

## 5. Data

`data/sales.csv` is committed. It holds 365 days of daily revenue, derived from the real Tableau Superstore dataset. Nothing to generate.

The generator `scripts/generate_sales.py` exists only to rebuild the file if it is ever missing.

## 6. Run the App

```bash
streamlit run frontend/streamlit_app.py
```

Open `http://localhost:8501`.

## 7. Ask a Question

Click an example chip or type your own.

- "what was our best day of the week?"
- "is revenue going up?"
- "how does this month compare to last?"

You get one chart, the numbers, and a written insight. The free model can take 30 to 90 seconds to answer. The spinner shows progress.

## 8. Run the Tests

Fast, offline:

```bash
python -m pytest
```

Full live pipeline test (a few minutes, needs the key):

```bash
python scripts/smoke_test.py
```

## Troubleshooting

**No insight, just a canned line.** The model call failed or timed out. The app degrades to a grounded fallback with the real pandas numbers. Check your key and your connection.

**Answers are slow.** The free model is rate limited. The app caps every call at 30 seconds with one retry. A slow model degrades to the fallback instead of hanging.

**Port in use.** Streamlit picks another port. Read the terminal output.

**Missing sales.csv.** Run `python scripts/generate_sales.py`.

## Next

Read `docs/ARCHITECTURE.md` for the data flow and `docs/CONFIGURATION.md` for all settings.