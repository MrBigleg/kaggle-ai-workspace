# kaggle-ai-workspace

> **Building in public.** Nothing here is finished. This is an active workspace — experiments, capstone work, remixes, and scaffolding evolve in real time.

My working repo for the [5-Day AI Agents Intensive: Vibe-coding Course with Google](https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google/overview) on Kaggle. Built with Google ADK, Vertex AI, and Gemini — exploring ambient agents, OKF knowledge bundles, and real-world agent architectures.

---

## What's in here

| Folder | Status | What it is |
|--------|--------|------------|
| [`thai-uhp-promise-engine/`](thai-uhp-promise-engine/) | 🔧 WIP | **Capstone project.** An AI agent that helps Thai UHP health insurance holders understand and act on their benefits. |
| [`gbp-review-triage/`](gbp-review-triage/) | 🔧 WIP | Google Business Profile review triage agent — classifies, prioritises, and drafts responses to GBP reviews using ADK. |
| [`ambient-expense-agent/`](ambient-expense-agent/) | 🔧 WIP | Ambient agent pattern experiment: passive expense monitoring and summarisation via Agent Runtime. |
| [`weather-assistant/`](weather-assistant/) | 🔧 WIP | Starter agent from the course scaffold — extended to explore ADK tool use and FastAPI deployment patterns. |
| [`ambient-agent-remixes/`](ambient-agent-remixes/) | 📐 Design | Five ambient agent designs (GBP content calendar, suspension early warning, local SEO report, client onboarding) — specs and workflow YAML, not yet built. |
| [`GBP-TO-OKF AUTO-SCAFFOLDER/`](https://github.com/MrBigleg/GBP-TO-OKF-AUTO-SCAFFOLDER) | 🔧 WIP | Git submodule. Auto-scaffolder that exports Google Business Profile data into OKF knowledge bundles. |
| [`_okf-reference/`](_okf-reference/) | ✅ Reference | Local OKF v0.1 spec summary, validator, producer (`export_okf.py`), and visualiser (`viz_okf.py`). |
| [`okf/`](okf/) | 🔧 WIP | OKF bundle experiments and scratch work. |
| [`docs/`](docs/) | 🔧 WIP | Agent design specs and architecture notes. |
| [`white-papers/`](white-papers/) | 📄 Notes | Course white papers and reference PDFs. |

---

## Tech stack

- **[Google ADK](https://google.github.io/adk-docs/)** — Agent Development Kit
- **Vertex AI / Agent Runtime** — cloud execution and deployment
- **Gemini** (via Vertex AI or AI Studio) — model layer
- **FastAPI** — agent API endpoints
- **OKF v0.1** — Open Knowledge Format for structured knowledge bundles
- **Python / uv** — dependency management

---

## Getting started

Each subfolder is its own project with its own `README.md`, `pyproject.toml`, and `.env.example`. Copy `.env.example` to `.env` and fill in your GCP project details.

```bash
# authenticate with GCP (required for Vertex AI)
gcloud auth application-default login
```

This repo uses a git submodule for `GBP-TO-OKF AUTO-SCAFFOLDER`. Clone with:

```bash
git clone --recurse-submodules https://github.com/MrBigleg/kaggle-ai-workspace.git
```

---

## Why public?

I learn better when I build in the open. Expect rough edges, incomplete implementations, and the occasional pivot. If something here is useful to you, use it.
