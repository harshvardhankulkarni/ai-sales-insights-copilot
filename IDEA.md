# IDEA.md: AI Sales Insights Copilot (P5)

Profile: forge (project development co-pilot). Build order: 1st.

## The idea in one line
Talk to your sales data like a colleague. Type a question, get the number, the chart, and the story.

## Why this project exists
Sales reports sit in dashboards that no one reads. People want answers, not screens. This project turns sales data into a conversation: ask in plain words, get a plain-word answer with a chart that agrees.

For Harsh, this is the first rung of the learning ladder. It teaches the core loop: LLM turns your question into a plan, pandas computes the real number, and the LLM writes the story from that number. The LLM never guesses. The math and the words always match.

## Who it serves
- A small sales manager with a CSV of daily sales.
- Someone who wants "what was our best day of the week" answered in ten seconds, not ten clicks.
- Any non-technical reader of a sales report.

## What problem it solves
- People avoid dashboards because they need practice to read them.
- Numbers without context are meaningless.
- Charts without a story do not drive decisions.
The copilot removes the barrier: the question is the interface.

## How it works (plain version)
1. You ask a question about sales data.
2. A classifier names the question type: trend, best day, comparison, top product.
3. A pandas engine computes the answer from real data. No LLM math.
4. Plotly draws a chart from the same numbers.
5. The LLM writes a short story about what the numbers say.
6. You see the answer, the chart, and the story together.

## Why this one matters for interviews
- It proves you understand what an LLM does well (language) and what it does poorly (math).
- It shows you keep the LLM on a leash: compute in pandas, narrate in words.
- It is a natural demo for Data Analyst and BI roles.
- It starts with data and ends with business insight.

## Success looks like
- A Streamlit app where a manager asks "what is our best day?" then gets a chart.
- Weekly auto-insight: the app writes a plain-word update without a prompt.
- The chart and the answer never disagree.
- You can explain every line of the pipeline to an interviewer.

## Honest scope
- Demo scope only. One CSV, seeded question types.
- No live CRM connection, no user accounts.
- The real metric: how clearly you explain grounding in an interview. Clarify your understanding.

---
Profile: forge. Built by Harsh Kulkarni, beginning-to-expert learner, with the teaching co-pilot.