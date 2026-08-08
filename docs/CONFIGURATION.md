# Configuration

**Project:** AI Sales Insights Copilot

## Environment Variables

The app reads settings from `.env` at the project root with python-dotenv.

| Variable | Required | Default | Purpose |
|---|---|---|---|
| OPENROUTER_API_KEY | Yes | none | Key for the LLM backend |
| LLM_MODEL | No | openai/gpt-oss-20b:free | Model for classification and insight |

The generator has one more setting, `SALES_DAYS`. It lives in `.env.example` for reference. The committed CSV already holds 365 days, so the generator is only used if the file goes missing.

## Setup

```bash
cp .env.example .env
```

Edit `.env`.

```
OPENROUTER_API_KEY=your-key-here
LLM_MODEL=openai/gpt-oss-20b:free
```

## LLM Backend

The app calls OpenRouter at `https://openrouter.ai/api/v1` through `langchain-openai`'s `ChatOpenAI` with a custom base URL. The default model `openai/gpt-oss-20b:free` costs nothing.

Free models are rate limited. Every call sends `request_timeout=30` and `max_retries=1`. When the model is slow or unavailable, the pipeline returns a grounded fallback written from the pandas numbers. The app never hangs.

## Security

- Never commit `.env`. The `.gitignore` excludes it.
- A key pasted into chat or a screenshot is a leaked key. Rotate it at https://openrouter.ai/keys.
- No secret goes into code or the docs.
- `.env.example` holds placeholder values only.

## Data Files

`data/sales.csv` is committed. It is the app input: 365 daily rows derived from the real Tableau Superstore dataset.

`data/raw/superstore-sales.csv` is the large source file. It is git-ignored and stays out of the public repo.

## Local Only

This project runs locally. GitHub Pages hosts the static docs and the architecture diagram. The Streamlit app runs from your terminal only.