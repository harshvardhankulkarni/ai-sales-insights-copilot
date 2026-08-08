"""Generate the P5 daily sales dataset. Real data first, synthetic fallback.

This is the single source of the daily sales file. Behavior:
1. If the real Tableau Superstore file exists at data/raw/superstore-sales.csv,
   it is aggregated into data/sales.csv as a continuous daily series (default
   SALES_DAYS days, real revenue and units).
2. If that file is missing, it synthesizes SALES_DAYS days of fake sales with
   trend, weekly seasonality, and noise. Real data always wins.

Run (from repo root): python scripts/generate_sales.py
Out:  data/sales.csv
"""
import os
import numpy as np
import pandas as pd

RAW = "data/raw/superstore-sales.csv"
OUT = "data/sales.csv"
DAYS = int(os.getenv("SALES_DAYS", 180))

def gen_real():
    """Aggregate the real Superstore orders into a daily series."""
    df = pd.read_csv(RAW, encoding="latin-1")
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%m/%d/%Y",
                                      errors="coerce")
    df["Units"] = 1
    agg = df.groupby("Order Date").agg(
        revenue=("Sales", "sum"),
        units=("Units", "sum"),
    ).reset_index()
    agg["date"] = agg["Order Date"].dt.strftime("%Y-%m-%d")
    return agg.sort_values("date").tail(DAYS)[["date", "revenue", "units"]]

def gen_synthetic(days=DAYS):
    """Fallback: create a synthetic daily sales series."""
    rng = np.random.default_rng(42)
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=days)
    trend = np.linspace(1.0, 1.2, days)
    weekly = 1 + 0.15 * np.sin(np.array(dates.dayofweek) * (2 * np.pi / 7))
    noise = rng.normal(0, 0.05, days)
    base = 5000.0
    revenue = base * trend * weekly * (1 + noise)
    units = (revenue / 25.0).astype(int)
    return pd.DataFrame({
        "date": dates.strftime("%Y-%m-%d"),
        "revenue": np.round(revenue, 2),
        "units": units,
    })

def main():
    if os.path.exists(RAW):
        sales = gen_real()
        print(f"real data used: {DAYS} days from {RAW}")
    else:
        sales = gen_synthetic()
        print("real file missing, synthetic fallback")

    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    sales.to_csv(OUT, index=False)
    print(f"wrote {OUT} ({len(sales)} days)")

if __name__ == "__main__":
    main()