# Data Source — P5 (AI Sales Insights Copilot)

**Status:** Dataset FOUND. Real data preferred, synthetic fallback.

## The dataset (real, verified)

**File:** `data/raw/superstore-sales.csv`
**Name:** Tableau Sample Superstore (global sales)
**Source:** Public Tableau sample dataset mirrored on GitHub
**Verified downloaded:** yes

### What it contains
Real-world order-level sales data.

| Column | Example | Meaning |
|---|---|---|
| Row ID | 1 | Row |
| Order ID | CA-2017-152156 | Order |
| Order Date | 08/11/2017 | Order date |
| Ship Date | 11/11/2017 | Ship date |
| Customer ID | CG-12520 | Customer |
| Segment | Consumer | Segment |
| Country | United States | Country |
| City / State / Region | Henderson / Kentucky / South | Geo |
| Category | Furniture | Product category |
| Sub-Category | Bookcases | Product sub-category |
| Sales | 261.96 | Revenue |

### Scale
- **9,980 order rows** (order-level)
- Date coverage: **2015-2018**, over 1,000 unique order dates
- Aggregates to a **365-day continuous daily series** (via `scripts/generate_sales.py`)
- More than enough for a 180-day sales dashboard

### Why it fits P5
P5 is an AI BI copilot that answers "best day of week", monthly trends, and comparisons. Order Date + Sales + Category are perfect for those analyses. Group by date to get a daily sales series, then compute day-of-week and monthly aggregates.

## How to use it in the project

1. Load `superstore-sales.csv` with pandas.
2. Run `python scripts/generate_sales.py`. It aggregates to a daily series and writes `data/sales.csv` (default 180 days, set `SALES_DAYS=365` for a full year). If the real file is missing, the script synthesizes fallback sales.
3. Filter to the most recent continuous window.
4. The dashboard reads `data/sales.csv`.

## Notes

- Kaggle hosts the same Tableau Superstore dataset. If you prefer Kaggle, use https://www.kaggle.com/datasets/bravehart101/sample-supermarket-dataset. But this GitHub mirror already works with no login, so keep it.
- It mirrors Tableau's official Sample Superstore that ships with Tableau Desktop.

## Synthetic fallback

The plan originally said "generate synthetic sales". That stays as the backup only, inside the same `generate_sales.py`. If the real file is ever missing, the script creates synthetic sales days. Real data wins.

## Redownload command

```
curl -sL -o data/raw/superstore-sales.csv "https://raw.githubusercontent.com/AmiraSayedMohamed/SuperStore-Dataset-Analysis-And-Prediction/master/data/Superstore%20Sales%20Dataset.csv"
```