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

Live deployment: streamlit run on GitHub pushes to Streamlit Cloud. Free URL:

```
https://ai-sales-insights-copilot.streamlit.app/
```

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

Pages serves the README and the docs. It is the static project story.

## 9. Streamlit Cloud

The live app runs on Streamlit Community Cloud:

```
https://ai-sales-insights-copilot.streamlit.app/
```

Deploy steps:

1. Sign in at share.streamlit.io with your GitHub account.
2. New app, from existing repo: `harshvardhankulkarni/ai-sales-insights-copilot`.
3. Branch `main`, main file `frontend/streamlit_app.py`.
4. Deploy. The build pulls requirements.txt exactly.
5. Settings, Secrets: add `OPENROUTER_API_KEY`.

Every git push to main redeploys the app automatically.

## 10. Notes

- The live app runs on Streamlit Cloud. The local run is for development.
- Locally the API key lives in `.env`, never committed. On the cloud it lives in Settings, Secrets.
- The app talks to OpenRouter, not directly to OpenAI.
- Free models are rate limited. Slow answers are expected, and the app turns a slow model into a grounded fallback instead of a hang.
- The free Cloud tier sleeps after inactivity. First visit after sleep takes about 30 seconds to wake.