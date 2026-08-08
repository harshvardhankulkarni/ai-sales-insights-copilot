# AGENTS.md — AI Sales Insights Copilot (P5)

## Overview
A Streamlit sales dashboard with a natural language layer. A user types a
question ("what was our best day of the week?") and gets the analysis numbers,
a Plotly chart, and a written insight from one question. Built for Harsh's
resume as proof of BI plus GenAI. Harsh is a beginner: teach every concept in
plain words before writing code. Read `AI_MEMORY.md` first — it is the single
source of project context.

## Build status (2026-08-09)
- Planning: 19 docs complete. Data staged. Branch main, origin main.
- Level 1 (basics): DONE. Grounding explained in own words.
- Level 2 (setup + data engine): DONE. Checkpoint verified in terminal.
- Level 3 (charts + NL): DONE. Checkpoint passed 2026-08-08. charts.py
  verified against analyze numbers. understand.py classifies through
  OpenRouter (openai/gpt-oss-20b:free). Live run: best_day, trend,
  comparison, fallback all classified correctly. 12 unit tests pass.
- Level 4 (insight + pipeline): DONE. Checkpoint passed 2026-08-08.
  insights.py (write_insight, write_weekly_insight) + pipeline.py
  (answer_question) built. Live runs: best_day and comparison questions
  returned numbers + chart + insight; weekly insight narrates pandas
  weekly totals. 22 unit tests pass.
- Level 5 (UI + finalize): DONE 2026-08-09. User picked Executive Desk
  theme from 3 sketches. frontend/streamlit_app.py built and verified:
  boots headless, 4 KPI cards + chart + ask panel render, no traceback,
  app screenshot in assets/. All 6 GSD docs + README rewritten to match
  the real build (OpenRouter free model, committed data). Committed and
  pushed. Pages documented in DEPLOYMENT.md. Live on Streamlit Cloud:
  https://ai-sales-insights-copilot.streamlit.app/ (free tier, sleeps
  on idle). Every push to main redeploys.
- Next step: none. Project complete.
- App files: app/data.py, app/analyze.py, app/charts.py, app/understand.py,
  app/insights.py, app/llm.py, app/pipeline.py, app/__init__.py,
  frontend/streamlit_app.py. tests/ has 5 files, 28 tests, all pass.
- LLM failover chain: app/llm.py tries OpenRouter free (LLM_MODEL), then
  OpenRouter paid (LLM_MODEL2), then Gemini (GEMINI_API_KEY), then canned.
  Timeouts 30/20/15s. 2026-08-09 it survived the free tier 429 cap cleanly.

## Data
- `data/sales.csv` (365-day daily series) is the app input. It is committed.
- Built by `scripts/generate_sales.py` from `data/raw/superstore-sales.csv`
  (Tableau Superstore, 9,800 orders, real numbers, safe for a public repo).
- Data is READY. Do not re-run the generator unless the file is missing:
  `python scripts/generate_sales.py`  (run from repo root)
- If the raw file is missing, the script synthesizes fake data. Real data wins.

## Dev environment
- Python 3.11+ required. On this machine `python` is 3.11; `python3` is 3.14.
  Always use `python`.
- venv: `python -m venv venv`, then `source venv/bin/activate` (git-bash) or
  `venv\Scripts\activate` (cmd).
- Install: `pip install -r requirements.txt`. The file exists and contains:
  langchain, langchain-openai, pandas, numpy, plotly, streamlit,
  python-dotenv, pytest.
- Secrets: copy `.env.example` to `.env`, fill `OPENROUTER_API_KEY` (key from
  https://openrouter.ai/keys). Other keys: `LLM_MODEL` (a `:free` model from
  OpenRouter, default `openai/gpt-oss-20b:free`), `SALES_DAYS` (generator
  window, default 180, `.env.example` ships 365). Never commit `.env`.

## Build & test (after the modules exist)
- Run app: `streamlit run frontend/streamlit_app.py` (opens
  http://localhost:8501; keep the shell running)
- Tests: `python -m pytest` (all), `python -m pytest tests/test_analyze.py` (one file)
- Full live check: `python scripts/smoke_test.py` (runs the real model,
  takes a few minutes, must end with `0 failed`)

## Conventions
- Follow ROADMAP.md strictly. One level at a time. Confirm every checkpoint
  with a real terminal run before moving on.
- Teach, then code: explain grounding, classification, synthetic data, pandas,
  and prompt engineering in plain words first. Ask clarifying questions.
- Grounding rule: pandas computes every number. The LLM writes prose only and
  never calculates. Charts read the pandas result, so chart and numbers agree.
- Question types are limited to 4 seeded types: trend, best day, comparison,
  top product. Unknown questions get a friendly fallback, never a crash.
- Module contract from TECHNICAL_DESIGN.md / API_SPEC.md:
  data.py -> DataFrame; understand.py -> type; analyze.py -> dict of numbers;
  charts.py -> Plotly Figure; insights.py -> prose;
  pipeline.py -> answer dict with type, result, chart, insight.
- Code style: one module one job, short functions, type hints and docstrings
  on public functions, no secrets in code.
- Commit messages use `feat:`, `fix:`, `docs:`, `test:` prefixes.
- M5 UI: draft 2-3 theme options, show Harsh, build only the one he picks.
- Old `sales-dashboard` repo is spirit only. Never copy its code.

## Key files
| File | Role |
|---|---|
| AI_MEMORY.md | Read first. Full brain: stack, env keys, architecture, pitfalls. |
| ROADMAP.md | Step ladder Level 1-5 with checkpoints and status tracker. |
| IDEA.md / BRD.md / PRD.md | Idea, business, product requirements. |
| TECHNICAL_DESIGN.md / API_SPEC.md | Architecture and module contract. |
| DATA_SOURCE.md | Where the sales data comes from and why. |
| docs/ | 6 GSD docs: README, ARCHITECTURE, GETTING-STARTED, DEVELOPMENT, TESTING, CONFIGURATION. |
| scripts/generate_sales.py | Regenerates sales.csv (run only if missing). |
| scripts/smoke_test.py | End-to-end live check of all functionality. Run before Level 5 signoff; must end with 0 failed. |
| Skills/ | Project learning notes. |

## Pitfalls (this repo's own)
- `data/raw/superstore-sales.csv` is gitignored; `data/sales.csv` is committed.
  Do not gitignore sales.csv and do not hand-edit it — regenerate instead.
- Docs reference `pip install -r requirements.txt`. The file now exists
  (created at Level 2, extended with pytest at Level 3).
- Missing `OPENROUTER_API_KEY` makes the classifier fall back to fallback
  type at runtime. The code degrades to fallback instead of crashing.
- OpenRouter `:free` models can be rate-limited upstream (429). The safety
  handler returns fallback in that case. Retry later or switch to a paid
  model in `LLM_MODEL`.
- Port 8501 busy: Streamlit picks another port; read the terminal output.
- Never re-run generate_sales.py "just to refresh" — data is committed and
  stale re-runs would rewrite the canonical 365-day file.

## Session end ritual (CRITICAL, no skipping)
After every build session, update exactly 3 places:
1. This file: the Build status block above.
2. ROADMAP.md: Status tracker table.
3. AI_MEMORY.md: progress note at the top.
Then write one line in `../PROGRESS.md` (master tracker) build log.

## Companion files
- `../Learning-Journey-Overview.md`, `../PROGRESS.md`, `../project-start-prompts.md`