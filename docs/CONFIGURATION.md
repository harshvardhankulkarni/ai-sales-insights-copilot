# Configuration

**Project:** AI Sales Insights Copilot

## Environment Variables

The app reads settings from `.env` at the project root. Load it with python-dotenv.

| Variable | Required | Default | Purpose |
|---|---|---|---|
| OPENAI_API_KEY | Yes | none | Your OpenAI secret key |
| LLM_MODEL | No | gpt-4o-mini | Model for classification and insight |
| SALES_DAYS | No | 180 | Days of synthetic sales to generate |

## Setup

```bash
cp .env.example .env
```

Edit `.env`.

```
OPENAI_API_KEY=sk-your-key-here
LLM_MODEL=gpt-4o-mini
SALES_DAYS=180
```

## Security

- Never commit `.env`. The `.gitignore` excludes it.
- The API key stays in `.env` only.
- No secret goes into code or the docs.
- Use `.env.example` for the committed template with placeholder values.

## Data Files

`data/sales.csv` holds the generated sales. It is a build artifact. Add it to `.gitignore` or keep it, your choice. The loader regenerates it when missing.

## Model Selection

`LLM_MODEL` defaults to `gpt-4o-mini`. Swap it for another OpenAI model if you want. Keep the change local. The cost stays low with the default.

## Settings Reference

| Setting | Where used |
|---|---|
| OPENAI_API_KEY | `app/understand.py`, `app/insights.py` |
| LLM_MODEL | LangChain client setup |
| SALES_DAYS | `scripts/generate_sales.py`, `app/data.py` |

## Changing SALES_DAYS

Set a new number in `.env`, delete `data/sales.csv` if present, and rerun:

```bash
python scripts/generate_sales.py
```

The loader reads the new value on startup.

## Local Only

This project runs locally. No production hosting. The GitHub Pages page hosts the static docs and architecture diagram, not the Streamlit app.