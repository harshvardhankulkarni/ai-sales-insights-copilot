# Testing

**Project:** AI Sales Insights Copilot

## Test Levels

The project uses two layers.

1. Automated unit tests with pytest, focused on the analysis engine.
2. A manual checklist you run in the Streamlit app.

## Automated Tests

`tests/test_analyze.py` holds pytest tests for `analyze.py`.

Run all:

```bash
python -m pytest
```

Run one file:

```bash
python -m pytest tests/test_analyze.py
```

## What the Unit Tests Cover

For each question type, the test feeds a small DataFrame and checks the returned numbers.

- `trend`: returns the rolling average and a direction.
- `best_day`: returns the day with the highest mean revenue.
- `comparison`: returns both totals and a percent change.
- `top_product`: returns the top product and its revenue.
- `fallback`: returns a message and no chart numbers.

Grounding tests confirm `analyze.py` runs without the LLM. No API call happens in this module.

## Manual Validation Checklist

Run the app. Tick each item.

- [ ] Sales data generates with about 180 rows.
- [ ] `.env` loads the API key and model.
- [ ] A seeded example question returns an answer.
- [ ] The chart renders.
- [ ] The insight appears beside the chart.
- [ ] The weekly auto-insight shows a narrative.
- [ ] An unknown question returns a friendly fallback, not a crash.

## Acceptance Mapping

| Criterion | How to test |
|---|---|
| LLM never computes | Read `insights.py`. Only prose prompts, no math |
| chart matches numbers | Read the chart values against the pandas result |
| Insight uses computed numbers | Every number in the insight exists in the result |
| Question types work | Test each of the 4 types |
| UI answers a seeded question | Ask one in Streamlit |

## Manual Chart Check

Ask "what is the weekday?" Read the bar values. Read the `best_day` numbers returned by `analyze`. The values must match exactly.

## Manual Insight Check

Ask any seeded question. Read the insight. Every number in the text must appear in the pandas result. If a number appears that pandas did not output, the test fails and the insight is ungrounded.

## When to Test

- After M1, test the analysis engine.
- After M2, test chart agreement.
- After M4, test grounding.
- After M5, test the UI end to end.
- After M6, re-run everything before push.