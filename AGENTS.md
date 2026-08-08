# AGENTS.md — AI Sales Insights Copilot (P5)

## Project identity
A Streamlit sales dashboard with a natural language layer. You type a question
("what was our best day of the week?") and the app returns the analysis, the
chart, and a written insight. Built for Harsh's resume as proof of BI plus
GenAI.

## Build status (2026-08-08)
- Understanding work: docs complete (19 files). Data staged.
- Implementation: NOT STARTED. Level 1 pending.
- Next step: Level 1 basics (copilot, grounding, classification, synthetic data).

## Data
- `data/sales.csv` (365-day daily series) is the app input.
- Built by `scripts/generate_sales.py` from `data/raw/superstore-sales.csv` (9,800 orders).
- Real source: Tableau Superstore dataset (real numbers, safe for public repo).
- Data is READY. Do not re-run the generator unless the file is missing.

## What is in this folder (file map)
| File | Role |
|---|---|
| AI_MEMORY.md | MUST READ FIRST. Full context for any AI tool. |
| ROADMAP.md | Step ladder. Level 1 to Level 5. Checkpoint per level. |
| LEARNING_JOURNEY.md | Beginner learning path with glossary and progress log. |
| SKILLS.md | Which Hermes skills to load and when. |
| Plan_AI-Sales-Insights-Copilot.md | The original build plan. |
| BRD.md, PRD.md | Business and product requirements. |
| TECHNICAL_DESIGN.md | Architecture and design. |
| API_SPEC.md | Endpoint and interface spec. |
| TEST_PLAN.md | Validation checklist. |
| USER_GUIDE.md | How to use the app. |
| DEPLOYMENT.md | Push and Pages steps. |
| DATA_SOURCE.md | Data origin and why. |
| assets/ | Architecture diagram etc. |
| docs/ | 6 GSD docs for the repo (README, ARCHITECTURE, GETTING-STARTED, DEVELOPMENT, TESTING, CONFIGURATION). |
| scripts/generate_sales.py | Regenerates sales.csv. |
| Skills/ | Project learning notes. |

## Build rules
- Harsh is a beginner. Explain every concept in plain words before code.
- Follow ROADMAP.md order. One level at a time. Confirm the checkpoint with a
  real terminal run before moving on.
- M5 UI: draft 2 or 3 theme options, show Harsh, build only the chosen one.
- Secret handling: `.env` local only, never commit. `.env.example` holds keys.

## Progress maintenance rule (CRITICAL)
After EVERY build session, update exactly 3 places:
1. This file: PROJECT STATUS section at the top (done steps, current step).
2. `ROADMAP.md` Status tracker table (flip Step to Done with a note).
3. `AI_MEMORY.md` (append or refresh the progress note at the top).
Then the next session opens with zero context loss.

## Companion files at the root
- `../Learning-Journey-Overview.md` — the full 5-project ladder map.
- `../PROGRESS.md` — the shared tracker across all 5 projects.
- `../project-start-prompts.md` — copy-paste prompts to start any project.