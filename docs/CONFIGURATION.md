# Configuration

**Project:** AI Sales Insights Copilot

## Environment Variables

The app reads settings from `.env` at the project root with python-dotenv.

| Variable | Required | Default | Purpose |
|---|---|---|---|
| OPENROUTER_API_KEY | Yes | none | Key for the LLM backend, slot 1 and 2 |
| LLM_MODEL | No | openai/gpt-oss-20b:free | Slot 1 model, OpenRouter free tier |
| LLM_MODEL2 | No | openai/gpt-4o-mini | Slot 2 model, OpenRouter paid tier |
| GEMINI_API_KEY | No | none | Slot 3, Gemini. Get one at aistudio.google.com |
| LLM_MODEL3 | No | gemini-2.0-flash | Slot 3 model, Gemini |

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

## Failover chain

The app never depends on a single model. `app/llm.py` builds an ordered chain from the environment and tries each slot until one answers:

1. OpenRouter free tier. Default `openai/gpt-oss-20b:free`. Costs nothing, capped at 50 requests per day.
2. OpenRouter paid tier. Default `openai/gpt-4o-mini`. Same key, bypasses the free cap, costs a fraction of a cent per question. Needs credits on the OpenRouter account.
3. Gemini, OpenAI-compatible endpoint. Default `gemini-2.0-flash`. Free key from aistudio.google.com.

Timeouts shrink per slot: 30, 20, 15 seconds. A failing slot is skipped in around a second. When every slot fails, the pipeline returns a grounded fallback written from the pandas numbers. The app never hangs and never shows a stale number.

On the cloud, add the same keys to Settings, Secrets in Streamlit Cloud. `.env` never ships.

## Security

- Never commit `.env`. The `.gitignore` excludes it.
- A key pasted into chat or a screenshot is a leaked key. Rotate it at https://openrouter.ai/keys.
- No secret goes into code or the docs.
- `.env.example` holds placeholder values only.

## Data Files

`data/sales.csv` is committed. It is the app input: 365 daily rows derived from the real Tableau Superstore dataset.

`data/raw/superstore-sales.csv` is the large source file. It is git-ignored and stays out of the public repo.

## Deployment

The app runs on Streamlit Cloud at https://ai-sales-insights-copilot.streamlit.app/. GitHub Pages hosts the static docs. Secrets for the LLM chain live in Settings, Secrets alongside `.env` locally.