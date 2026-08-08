# AI Sales Insights Copilot

Ask your sales data a question. Get the numbers, the chart, and the story in plain words.

I turned my dashboard into a copilot. You type "what was our best day of the week?" and the system classifies the question, computes the answer with pandas, builds a Plotly chart, and writes a plain-language insight with the LLM. It also writes a weekly auto-insight.

## Highlights

- Natural language questions about sales data.
- 4 seeded question types: trend, best day, comparison, top product.
- pandas analysis engine. The LLM never computes.
- Plotly charts that match the pandas numbers.
- Weekly auto-insight narrative.
- Streamlit chat UI.

## Tech Stack

Python 3.11, Pandas, NumPy, OpenAI GPT-4o-mini, LangChain, Streamlit, Plotly.

## Repo Layout

```
app/            core pipeline: data, understand, analyze, charts, insights, pipeline
scripts/        generate_sales.py
frontend/       streamlit_app.py
tests/          test_analyze.py
docs/           GSD documentation set
assets/         architecture diagram
```

## Quick Start

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # add your OPENAI_API_KEY
mkdir -p data
python scripts/generate_sales.py
streamlit run frontend/streamlit_app.py
```

## Documentation

- `docs/GETTING-STARTED.md` for setup.
- `docs/ARCHITECTURE.md` for the data flow.
- `docs/DEVELOPMENT.md` for the build workflow.
- `docs/TESTING.md` for test guidance.
- `docs/CONFIGURATION.md` for env keys and settings.
- `docs/README.md` for this index.

## Roadmap

- M1 Data and analysis engine
- M2 Charts
- M3 NL question handler
- M4 Insight writer
- M5 Streamlit copilot UI
- M6 Docs, GitHub, Pages

## License

Private demo project.