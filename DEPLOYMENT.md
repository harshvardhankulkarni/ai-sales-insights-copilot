# Deployment

**Project:** AI Sales Insights Copilot
**Owner:** Harsh Kulkarni
**Repo:** AI-Sales-Insights-Copilot
**GitHub user:** harshvardhankulkarni

## 1. Prerequisites

- Python 3.11 or higher.
- An OpenRouter API key.
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
OPENROUTER_API_KEY=your-key-here
LLM_MODEL=openai/gpt-oss-20b:free
```

Never commit `.env`. `.gitignore` keeps it out.

## 4. Data

`data/sales.csv` is committed: 365 daily rows from the Superstore source. No generation step. If the file is ever missing, run `python scripts/generate_sales.py`.

## 5. Run the Copilot

```bash
streamlit run frontend/streamlit_app.py
```

Open `localhost:8501`.

## 6. Tests

```bash
python -m pytest
```

22 tests. Then run the live check:

```bash
python scripts/smoke_test.py
```

## 7. Git Push

The remote already points to the repo. To publish changes:

```bash
git add .
git commit -m "feat: describe the change"
git push origin main
```

## 8. GitHub Pages

1. Open the repo on GitHub.
2. Go to Settings, then Pages.
3. Set source to `main` branch, root folder.
4. Save.

Pages URL after a few minutes:

```
https://harshvardhankulkarni.github.io/ai-sales-insights-copilot/
```

Pages serves the README and the docs. The Streamlit app runs locally only. The public page is the project story and architecture report.

## 9. Notes

- This is a local demo. No cloud hosting for the Streamlit app.
- The API key stays in `.env` locally.
- The app talks to OpenRouter, not directly to OpenAI.
- Free models are rate limited. Slow answers are expected, and the app turns a slow model into a grounded fallback instead of a hang.