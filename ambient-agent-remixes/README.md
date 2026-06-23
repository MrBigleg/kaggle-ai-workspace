# Ambient Agent Prompt Remixes for CTB / Rank-in-Maps

Local prototype implementations of ambient agents for Google Business Profile (GBP) management, powered by Google Agents CLI with ADK 2.0 compatibility.

## Overview

Five production-ready agent concepts designed to automate GBP workflows and solve real pain points for multi-location clients:

1. **GBP Review Triage Agent** — Auto-reply to 4–5 star reviews; human-in-the-loop for 1–3 stars + sensitive keywords
2. **GBP Content Calendar Agent** — Weekly post scheduling with auto-publish + human approval gates
3. **GBP Suspension Early Warning Agent** — Real-time profile health monitoring + Slack/email alerts
4. **Local SEO Report Agent** — Weekly KPI summaries + human review for 15%+ drops
5. **Client Onboarding Agent** — Guided setup automation + manual triage for complex cases

## Quick Start

Each agent includes:
- `README.md` — Full specification and workflow diagram
- `workflow.yaml` — Graph definition (ADK 2.0 compatible)
- `prompts.md` — System prompts and node configurations
- `test-cases.md` — Example scenarios and edge cases

## Architecture Pattern

All agents follow this pattern:
- **Input**: Event or scheduled trigger (review received, weekly cadence, etc.)
- **Auto Nodes**: Deterministic paths (auto-reply, auto-publish, auto-alert)
- **Human Nodes**: `RequestInput` gates for complex decisions
- **Output**: Action, notification, or queue for manual review

## Integration

- Google Agents CLI for local development
- ADK 2.0 runtime for deployment
- Slack/Email for notifications
- GBP API for data reads/writes

## Status

Prototype phase — ready for local testing and ADK deployment.

---

Reference: [Enterprise Cloud Scale: Deploying the Expense Agent](https://codelabs.developers.google.com/enterprise-cloud-scale-deploying-the-expense-agent-to-agent-runtime-on-google-cloud)
