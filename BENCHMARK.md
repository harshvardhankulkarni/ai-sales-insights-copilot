# Benchmark — AI Sales Insights Copilot

How to test the copilot. Every expected number comes from `app/analyze.py` running on the committed `data/sales.csv`. The app is correct only when its answer matches the rows below.

## Ground truth

Run this any time to regenerate the exact numbers:

```bash
venv/Scripts/python.exe -c "
from app.data import load_sales
from app.analyze import trend, best_day, comparison
df = load_sales()
print(best_day(df))
print(trend(df))
print(comparison(df))
"
```

Current values (data/sales.csv, 365 days):

| Type | Key numbers |
|---|---|
| best_day | Thursday, average 2423.10 |
| trend | Last 7 days 2196.51 vs previous 1626.35, change +35.06%, up |
| comparison | 2018-12: 16647.04 vs 2018-11: 17407.27, change −4.37% |

Full weekday means for chart checks: Friday 2295.95, Monday 1806.99, Saturday 1559.12, Sunday 1829.99, Thursday 2423.10, Tuesday 1905.60, Wednesday 1811.17.

## Question bank

### Best day (expect Thursday, ~2423.10)

1. What was our best day of the week?
2. Which weekday earns the most revenue?
3. On what day do we make the most sales?
4. What is our highest revenue day?
5. Which day of the week performs the best?
6. Where should we focus our best promotions?

### Trend (expect up, 35.06%)

7. Is revenue going up?
8. Are sales increasing or decreasing?
9. What is the sales trend over the last week?
10. How did we do this week compared to last week?
11. Is business growing?

### Comparison (expect 2018-12 vs 2018-11, −4.37%)

1. How does this month compare to last?
2. Is this month better than the last month?
3. What is the month over month change in revenue?
4. Did revenue drop this month?
5. Which month was higher, November or December?

### Fallback. Expect "I cannot answer that yet", no chart

1. Which product sells the most?
2. What is our profit margin?
3. Who is our best customer?
4. Which region has the highest sales?
5. What inventory should I order?
6. How many orders did we get in March?
7. What target should we set for next week?
8. How much money did we make in total?

## Scoring per question

Tick three boxes.

1. Classification. The type falls out right.
2. Numbers match. The insight quotes the exact pandas figure, not an approximation.
3. Chart present. best_day, trend, comparison each render one chart. Fallback has none.

## Phrasings that stress the classifier

These are the interview answers. The app must not crash and must resolve to the listed type.

| Question | Expect | Why it tests something |
|---|---|---|
| What day is strongest? | best_day | "day" without "week" |
| Why is revenue lower now? | trend or comparison | ambiguous, must not crash |
| Are we beating last month? | comparison | "beating" is not "compare" |
| Up or down lately? | trend | slang phrasing |
| Show me this week's performance | trend | "performance" maps to trend |
| Best day? | best_day | minimal input |
| How much money did we make in total? | fallback | total is not a seeded type |

## Acceptance criteria

- A best_day insight contains "Thursday" and "2423.1" or "2423.10".
- A trend insight contains "35.06" and "up".
- A comparison insight contains both month names and a number near 4.37 with a direction or minus sign.
- Every fallback question ends with "I cannot answer that yet."
- Chart bars match the printed weekday means for a best_day question.
- A rate-limited model may return fallback once. Re-run the same question before counting it as a fail.

## Verified

- 2026-08-09: values above produced directly from `analyze.run()` on the committed CSV.
- The live smoke test (`python scripts/smoke_test.py`) runs the full pipeline happy path plus fallback.