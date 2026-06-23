# GBP Review Triage Agent

## Overview

Monitors incoming Google Business Profile reviews across multiple locations and intelligently routes them:
- **Auto-reply** to positive reviews (4–5 stars)
- **Human-in-the-loop** for negative reviews (1–3 stars) or sensitive keywords

## Problem Solved

Multi-location clients (e.g., David Timm's 26+ restaurants) drown in review notifications. Manual triage wastes hours daily. This agent handles routine positivity and escalates friction.

## Workflow

```
Review Received (Webhook)
├─ Extract: rating, text, location_id, reviewer_name
├─ Classify: sentiment + keyword detection
│  ├─ Rating 4–5 → auto_reply node
│  │  ├─ Generate response via LLM
│  │  └─ Post to GBP
│  │
│  └─ Rating 1–3 OR keywords ["refund", "dangerous", "fake"] → flag_for_human node
│     ├─ RequestInput (human in the loop)
│     ├─ Human reviews + approves response
│     └─ Post approved response
│
└─ Log: audit trail, response latency
```

## ADK 2.0 Graph Definition

**Nodes:**
- `extract_review` — Parse GBP API payload
- `classify_sentiment` — LLM-based rating + keyword detection
- `auto_reply` — Generate & post positive-review response
- `flag_for_human` — RequestInput pause for manual triage
- `log_action` — Audit trail to Firestore

**Transitions:**
```yaml
extract_review → classify_sentiment
classify_sentiment →
  [rating ≥ 4] auto_reply → log_action
  [rating < 4 OR has_sensitive_keywords] flag_for_human → log_action
```

## Deployment

1. Set up GBP API credentials
2. Configure webhook for review events
3. Point to Slack or email for RequestInput notifications
4. Deploy workflow via Agents CLI

## Success Metrics

- Response latency (target: <5 min for auto-replies)
- Human escalation rate (target: <20% of reviews)
- Client satisfaction with tone/accuracy

## Implementation Notes

- Tone guard: LLM validation before posting auto-replies
- Rate limiting: Batch reviews per location to avoid GBP API throttling
- Sensitive keywords: Configurable per client/industry
