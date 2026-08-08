# Testing

**Project:** AI Sales Insights Copilot

## Test Layers

Three layers.

1. Automated unit tests with pytest. Fast, offline, fake model.
2. A live smoke test. Runs the real pipeline against OpenRouter.
3. A manual checklist in the Streamlit app.

## 1. Unit Tests

```bash
python -m pytest
```

22 tests in 4 files:

| File | Covers |
|---|---|
| test_analyze.py | pandas numbers per type, fallback shape |
| test_understand.py | classifier maps to known types, bad input to fallback |
| test_insights.py | insight grounded in result numbers, weekly insight grounded in weekly totals, fallback on model failure |
| test_pipeline.py | full answer dict, chart matches result, fake LLM keeps tests offline |

The tests use a fake LLM. No network, no key. One integration test runs the real pipeline and is skipped when no answer arrives.

## 2. Live Smoke Test

```bash
python scripts/smoke_test.py
```

Runs all four question types live, then the weekly insight. Each check prints PASS or FAIL. It verifies:

- The classifier returns the right type.
- The insight quotes the pandas numbers exactly.
- The chart plots the same numbers as the result dict.
- An unrelated question returns the fallback, not a crash.

Needs the OpenRouter key and a few minutes. The free model is slow.

## 3. Manual Checklist

Run the app. Tick each item.

- [ ] KPI cards show pandas numbers.
- [ ] A seeded example question returns an answer.
- [ ] The chart renders and matches the insight numbers.
- [ ] The insight appears beside the chart.
- [ ] The weekly auto-insight shows a narrative.
- [ ] An unknown question returns a friendly fallback.

## Acceptance Mapping

| Criterion | How to test |
|---|---|
| LLM never computes | Read `insights.py`. Only prose prompts, no math |
| Chart matches numbers | Extract plotted values from the figure, compare to the result |
| Insight uses computed numbers | Every number in the insight exists in the result |
| Question types work | Test each type in the smoke test |
| UI answers a question | Ask one in Streamlit |

## Chart Agreement Check

Ask "what was our best day of the week?". The chart bars equal `weekday_means`. The best bar equals `avg_revenue`. Chart, numbers, and insight always agree because all three come from one pandas result.

## Timeout Guarantee

Every LLM call uses `request_timeout=30, max_retries=1`. A rate-limited free model cannot hang the pipeline. It degrades to the grounded fallback with the real pandas numbers.

## When to Test

- After any change to `app/analyze.py`: `python -m pytest tests/test_analyze.py`.
- After changes to `understand.py` or `insights.py`: full pytest.
- Before pushing: full pytest plus `python scripts/smoke_test.py`.
- After changing the UI: run the app and click the example chips.