# API Specification

**Project:** AI Sales Insights Copilot
**Owner:** Harsh Kulkarni
**Version:** 1.0

This spec covers the internal functions of the pipeline. The product runs locally. It exposes no HTTP API. The functions pass Python objects between modules. This spec gives every current and future caller a clear contract.

## 1. Data Module (app/data.py)

### load_or_generate_sales()
Return a pandas DataFrame with a daily revenue series.

**Signature** `load_or_generate_sales(path="data/sales.csv", days=180) -> pd.DataFrame`

**Returns** a DataFrame with `date` and `revenue`.

**Behavior** Reads the CSV if present. Otherwise generates 180 rows with trend, weekly seasonality, and noise, and saves to `path`.

**Example**

```python
df = load_or_generate_sales()
print(df.head())
```

## 2. Understand Module (app/understand.py)

### `classify_question(question) -> dict`
Classify a typed question into one seeded type. This is the natural language understanding step. It calls the LLM.

**Parameters**
- `question`: the user text, for example "what was our best day of the week?".

**Returns** a dict
```python
{"type": "best_day", "question": "what was our best day of the week?"}
```

**Types** `trend`, `best_day`, `comparison`, `top_product`, `fallback`.

**Acceptance** the `type` is one of those five strings.

## 3. Analyze Module (app/analyze.py)

### `analyze(df, type, question="") -> dict`
Compute the answer with pandas only. No LLM call.

**Parameters**
- `df`: the sales DataFrame.
- `type`: the type label from `classify_question`.
- `question`: kept for context, not used in math.

**Returns** a dict of computed numbers. The shape varies by type.

**Example**

```python
result = analyze(df, "best_day")
# {"best_day": "Saturday", "mean_revenue": 1870.3}
```

**Type mapping**
- `trend` returns rolling average and direction.
- `best_day` returns the day with the highest mean revenue and that mean.
- `comparison` returns two periods and the change percent.
- `top_product` returns the top product and its revenue.
- `fallback` returns a message and no chart numbers.

## 4. Charts Module (app/charts.py)

### `build_chart(result) -> plotly.graph_objects.Figure`
Build a Plotly chart from the analysis numbers.

**Parameters** `result`: the dict from `analyze`.

**Returns** a Plotly `Figure`. The chart matches the numbers in `result`.

**Rule** The chart reads from the pandas result only. It never computes its own numbers.

## 5. Insights Module (app/insights.py)

### `write_insight(result) -> str`
Have the LLM write a plain-language insight from the computed numbers.

**Parameters** `result`: the dict from `analyze`.

**Returns** an insight string that uses only numbers in `result`.

### `write_weekly_insight(df) -> str`
Pass a weekly revenue summary to the LLM and return a narrative.

**Parameters** `df`: the sales DataFrame.

**Returns** a string weekly narrative built from the weekly aggregates.

## 6. Pipeline Module (app/pipeline.py)

### `answer_question(question) -> dict`
Run the full flow: classify, analyze, chart, insight.

**Example**

```python
answer = answer_question("what was our best day of the week?")
# answer = {
#   "question": "what was our best day of the week?",
#   "type": "best_day",
#   "result": {"best_day": "Saturday", "mean_revenue": 1870.3},
#   "chart": figure_object,
#   "insight": "Revenue is highest on Saturday with an average of 1870.3."
# }
```

**Acceptance** a seeded question returns a complete answer. The chart matches `result`. The insight uses only numbers from `result`.

## 7. Contract Rules

- `analyze` never calls the LLM.
- `write_insight` never computes. It reads numbers only from the result.
- `build_chart` never computes. It plots the given numbers.
- Every `type` resolves a value, including `fallback`.
- All functions are pure relative to their inputs. No global state.

## 8. Types

| Type | Question example | Chart |
|---|---|---|
| trend | "is revenue going up over 30 days?" | line with rolling mean |
| best_day | "what was our best day of the week?" | bar by day |
| comparison | "how does June compare to May?" | grouped bar |
| top_product | "which product sold most?" | horizontal bar |
| fallback | any other question | message only |