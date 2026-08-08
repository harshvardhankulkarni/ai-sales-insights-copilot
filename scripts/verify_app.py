"""Probe the Streamlit app in headless Chrome.

Loads http://localhost:8501, waits for the websocket round-trip, then
checks the rendered DOM for real content markers.
"""

import re
import subprocess
import sys

from pathlib import Path

CHROME = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]


def find_chrome() -> str:
    for candidate in CHROME:
        if Path(candidate).exists():
            return candidate
    raise SystemExit("Chrome not found")


def main() -> int:
    chrome = find_chrome()
    result = subprocess.run(
        [chrome, "--headless=new", "--disable-gpu",
         "--virtual-time-budget=15000", "--dump-dom",
         "http://localhost:8501"],
        capture_output=True, text=True, timeout=90,
    )
    dom = result.stdout
    print(f"DOM length: {len(dom)}")
    for marker in ("kpi-grid", "Best weekday", "Trend, 7d",
                   "Default view", "class=\"kpi\"", "Ask a sales question",
                   "canvas", "plotly", "Traceback"):
        print(f"marker {marker!r}: {dom.count(marker)}")
    # Streamlit renders custom HTML inside stMarkdown blocks.
    print("stMarkdown blocks:", dom.count("stMarkdown"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())