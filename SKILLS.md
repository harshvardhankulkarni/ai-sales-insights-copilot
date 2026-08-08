# Skills

**Project:** AI Sales Insights Copilot
**Owner:** Harsh Kulkarni
**Purpose:** Which Hermes skills to load and why.

Load these Hermes skills during this build. Each one speeds up a specific part of the work.

## Required Skills

### architecture-diagram
**What it gives:** A worked way to build dark themed SVG architecture and data flow diagrams as HTML pages.
**Load when:** M2 and M6. Use it to draw the data flow from sales data to chart to insight.
**Why:** The diagram in `assets/architecture-diagram.html` follows this skill so it stays readable, consistent, and dependency-free.

### claude-design
**What it gives:** A method to design single-page HTML artifacts, from landing pages to demo pages.
**Load when:** M5, the Streamlit UI milestone.
**Why:** Use it to draft 2 to 3 distinct UI option pages. Harsh picks one theme, then the build renders it in Streamlit.

### popular-web-designs
**What it gives:** 54 real design systems, for example Stripe and Linear, with HTML and CSS.
**Load when:** M5 UI milestone.
**Why:** Source a modern look for the UI options drawn from real products, not from guesswork.

## Optional Skill

### jupyter-live-kernel
**What it gives:** A live Python kernel to run code step by step in a notebook style.
**Load when:** M1 data exploration.
**Why:** Explore the synthetic sales data interactively while you learn pandas, before you write the analysis modules.

## Order of Use

1. M1: `jupyter-live-kernel` to explore the data.
2. M5: `claude-design` and `popular-web-designs` to draft UI options.
3. M6: `architecture-diagram` for the final architecture report.

## Why This Skill List

| Skill | Job in this project |
|---|---|
| architecture-diagram | Data flow diagram for the report |
| claude-design | UI option drafts to let Harsh choose |
| popular-web-designs | Real design references for the UI |
| jupyter-live-kernel | Explore sales data in M1 |

No other Hermes skill is needed. The rest of the work is plain Python, pandas, and Streamlit.