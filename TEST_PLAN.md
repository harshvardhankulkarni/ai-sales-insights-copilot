# Test Plan

**Project:** AI Sales Insights Copilot
**Owner:** Harsh Kulkarni
**Version:** 1.0

## 1. Purpose

This manual proves the system answers seeded questions correctly, the chart matches the numbers, the LLM stays grounded, and the UI works. You run the app and check each item.

## 2. Test Environment

- Python 3.11 or higher.
- All packages installed from `requirements.txt`.
- An OpenAI API key in `.env`.

## 3. Manual Validation Checklist

Run the app and confirm each item.

- [ ] Sales data generates with at least 180 rows.
- [ ] `.env` loads the API key and model.
- [ ] A seeded example question returns an answer.
- [ ] The chart renders in the app.
- [ ] The insight appears beside the chart.
- [ ] The weekly auto-insight shows a narrative.
- [ ] An unknown question returns a fallback, not a crash.
- [ ] The app closes cleanly with no errors in the log.

## 4. Test Cases

### TC-1 Data generation
**Steps** Run the data loader.
**Expected** A DataFrame with about 180 rows, a date column and a revenue column.

### TC-2 Analyze correctness per type

| Type | Input | Expected |
|---|---|---|
| trend | 30 day history | Rolling mean returned, direction is up or down |
| best_day | ask the best day | The day with the highest mean revenue |
| comparison | compare two months | Both totals and the difference percent |
| top_product | which product sold most | The top ranked product and its revenue |
| fallback | random text | A helpful message, no numbers |

**Acceptance** The returned number equals the pandas value computed in `analyze`.

### TC-3 Chart matches numbers
  **Steps** Ask a seeded question. Read the chart titles and values. Compare them to the numbers returned by `analyze`.
  **Expected** Every chart label equals the corresponding number in the result.
  **Result pass** if no mismatch and source note points to pandas output only.

### TC-4 Insight uses computed numbers only
  **Steps** Run `write_insight` with a known result.
  **Expected** The insight text contains only numbers from the result.
  **Failed if** the text names a number not in the result.

### TC-5 Insight is grounded, never computes
  **Steps** Read the code path that calls the LLM.
  **Expected** The prompt passes numbers in, not a request to calculate.

### TC-6 Pipeline end to end
**Steps** Call `answer_question("what was our best day of the week?")`.
**Expected** Returns a dict with `type`, `result`, `chart`, and `insight`. The chart JSON matches `result`.

### TC-7 UI chat
**Steps** Open the Streamlit app. Click a seeded example question.
**Expected** The app shows one chart, one insight, and the numbers.

### TC-8 Weekly auto-insight
**Steps** Trigger the weekly writer.
**Expected** A narrative reads the weekly summary. The weekly numbers are in the text.

### TC-9 Config loading
**Steps** Start the app with a valid `.env`.
**Expected** `LLM_MODEL` and `SALES_DAYS` load. Sales rows match `SALES_DAYS`.

## 4. Acceptance Criteria to Test Mapping

| Acceptance criterion | Test cases |
|---|---|
| Sales data generates | TC-1 |
| analyze returns correct numbers per type | TC-2 |
| Chart matches numbers | TC-3, TC-6 |
| Insight uses computed numbers only | TC-4, TC-5 |
| LLM never computes | TC-5 |
| Streamlit answers a seeded question with chart and insight | TC-7, TC-8 |

## 5. Automated Tests

`tests/test_analyze.py` holds pytest cases for the analysis engine. Run with:

```bash
python -m pytest tests/
```

Add a case per type. Cover the fallback path.

## 6. Results Log

Fill this table as you test each build.

| Test | Date | Result | Notes |
|---|---|---|---|
| TC-1 | | Pass / Fail | |
| TC-2 trend | | Pass / Fail | |
| TC-2 best_day | | Pass / Fail | |
| TC-2 comparison | | Pass / Fail | |
| TC-2 top_product | | Pass / Fail | |
| TC-3 | | Pass / Fail | |
| TC-4 | | Pass / Fail | |
| TC-5 | | Pass / Fail | |
| TC-6 | | Pass / Fail | |
| TC-7 | | Pass / Fail | |
| TC-8 | | Pass / Fail | |
| TC-9 | | Pass / Fail | |