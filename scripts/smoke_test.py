"""End-to-end smoke test. Run it yourself to check everything built so far.

Usage (from the project root, venv active):
    venv/Scripts/python.exe scripts/smoke_test.py

It asks all four question types, checks the answer shape, verifies the
chart plots the exact numbers pandas computed, proves the insight quotes
those numbers, and runs the weekly auto-insight.

Every check prints PASS or FAIL. The script exits 0 only if all pass.
The live model is slow (free tier). Allow a few minutes.
"""

import sys
import time
from pathlib import Path

# Make the project root importable when run as scripts/smoke_test.py
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.data import load_sales
from app.pipeline import answer_question
from app.insights import write_weekly_insight, _weekly_summary

PAUSE = 1.0
passed = 0
failed = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global passed, failed
    mark = "PASS" if ok else "FAIL"
    if ok:
        passed += 1
    else:
        failed += 1
    print(f"[{mark}] {name}" + (f"  ({detail})" if detail else ""))


def bar_values(fig) -> list[float]:
    """Read the plotted bar values back out of a plotly figure."""
    for trace in fig.data:
        if trace.type == "bar":
            return [float(v) for v in trace.y]
    return []


def last_line_point(fig) -> float | None:
    """Read the last non-empty point of the first line trace."""
    for trace in fig.data:
        if trace.type == "scatter":
            ys = [float(v) for v in trace.y if v is not None]
            return ys[-1] if ys else None
    return None


def main() -> int:
    print("Loading data...")
    df = load_sales()
    print(f"  {len(df)} days, {df['date'].min().date()} to {df['date'].max().date()}")
    print()

    # 1. Best day
    print("Q1  what was our best day of the week?")
    a = answer_question("what was our best day of the week?", df=df)
    r = a["result"]
    check("classified best_day", a["type"] == "best_day")
    check("answer has chart", a["chart"] is not None)
    check("answer has insight", bool(a["insight"].strip()))
    best = r["best_day"]
    avg = r["avg_revenue"]
    bars = bar_values(a["chart"])
    check("best day matches pandas",
          bars and max(bars) == avg,
          f"max bar {max(bars) if bars else 'n/a':.2f} vs pandas {avg:.2f}")
    check("insight quotes the best day", best in a["insight"], best)
    print(f"    insight: {a['insight']}")
    print()
    time.sleep(PAUSE)

    # 2. Trend
    print("=" * 24 + "  is revenue going up over the last 10 days?")
    a = answer_question("is revenue going up over the last 10 days?", df=df)
    r = a["result"]
    check("classified trend", a["type"] == "trend")
    check("answer has chart", a["chart"] is not None)
    last = last_line_point(a["chart"])
    check("trend chart ends at pandas last avg",
          last is not None and abs(last - r["last_window_avg"]) < 0.01,
          f"last {last if last is not None else 'n/a'} vs {r['last_window_avg']}")
    check("insight quotes direction", r["direction"] in a["insight"].lower(),
          f"{r['direction']} {r['change_pct']}%")
    print(f"    insight: {a['insight']}")
    print()
    time.sleep(PAUSE)

    # 3. Comparison
    print("Q)  how does this month compare to last month?")
    a = answer_question("how does this month compare to last month?", df=df)
    r = a["result"]
    check("classified comparison", a["type"] == "comparison")
    check("answer has chart", a["chart"] is not None)
    bars = bar_values(a["chart"])
    check("comparison bars match pandas",
          len(bars) == 2
          and abs(bars[0] - r["previous_revenue"]) < 0.01
          and abs(bars[1] - r["current_revenue"]) < 0.01,
          f"bars {bars} vs prev {r['previous_revenue']}, curr {r['current_revenue']}")
    pct = abs(r["change_pct"])
    insight_lower = a["insight"].lower()
    if r["change_pct"] < 0:
        ok_dir = any(w in insight_lower
                     for w in ("decreas", "decline", "down", "lower", "fell", "drop",
                               "-", "\u2212", "\u2013", "minus"))
    else:
        ok_dir = any(w in insight_lower
                     for w in ("increas", "rise", "up", "higher", "grew", "grow",
                               "climb", "+"))
    check("insight quotes change percent",
          str(pct) in a["insight"] and ok_dir,
          f"{r['change_pct']}%")
    print(f"    insight: {a['insight']}")
    print()
    time.sleep(PAUSE)

    # 4. Fallback
    print("Q)  what is the weather in pune today?")
    a = answer_question("what is the weather in pune today?", df=df)
    check("classified fallback", a["type"] == "fallback")
    check("fallback has no chart", a["chart"] is None)
    check("fallback message present", "cannot answer" in a["result"]["message"])
    print(f"    message: {a['result']['message']}")
    print()

    # 5. Weekly auto-insight
    print("Weekly auto-insight")
    weekly = _weekly_summary(df)
    text = write_weekly_insight(df)
    check("weekly insight written", bool(text.strip()))
    check("weekly numbers computable", len(weekly) > 0, weekly[:60])
    print(f"    numbers: {weekly}")
    print(f"    insight: {text}")
    print()

    print(f"RESULT: {passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())