# Deployment

**Project:** AI Sales Insights Copilot
**Owner:** Harsh Kulkarni
**Repo:** AI-Sales-Insights-Copilot
**GitHub user:** harshvardhankulkarni

## 1. Prerequisites

- Python 3.11 or higher.
- OpenAI API key.
- Git.
- A GitHub account for `harshvardhankulkarni`.

## 2. Local Run

From the project folder:

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 3. .env Setup

Create `.env` from the example.

```bash
cp .env.example .env
```

Add your key.

```
OPENAI_API_KEY=sk-your-key-here
LLM_MODEL=gpt-4o-mini
SALES_DAYS=180
```

Never commit `.env`. `.gitignore` keeps it out.

## 4. Generate Sales Data

```bash
mkdir -p data
python scripts/generate_sales.py
```

This writes `data/sales.csv` with about 180 rows of synthetic sales.

## 5. Run the Copilot

```bash
streamlit run frontend/streamlit_app.py
```

Open `localhost:8501`.

## 6. Tests

```bash
python -m pytest
```

Run the analysis engine checks in `tests/test_analyze.py`.

## 7. Git Push

```bash
git init
git add .
git commit -m "feat: AI Sales Insights Copilot"
git branch -M main
git remote add origin https://github.com/harshvardhankulkarni/AI-Sales-Insights-Copilot.git
git push -u origin main
```

## 8. GitHub Pages

1. Open the repo on GitHub.
2. Go to Settings, then Pages.
3. Set source to `main` branch, root folder.
4. Save.

Pages URL after a few minutes:

```
https://harshvardhankulkarni.github.io/AI-Sales-Insights-Copilot/
```

Pages serves the static docs and architecture diagram. The Streamlit app runs locally only. The documented page is the project story and the architecture report.

## 9. Notes

- This is a local demo. No cloud hosting for the Streamlit app.
- The API key stays in `.env` locally.
- Keep question types limited so the hosted story stays reliable.