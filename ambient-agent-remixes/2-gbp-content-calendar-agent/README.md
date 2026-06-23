# GBP Content Calendar Agent

## Overview

Generates and schedules weekly Google Business Profile posts across multiple locations:
- **Auto-publish** evergreen content (offers, updates, events)
- **Human-in-the-loop** for promotional claims, pricing, or seasonal campaigns

## Problem Solved

Multi-location clients need consistent GBP engagement. Manual post creation is tedious and error-prone. This agent auto-generates topical posts and gates brand-sensitive content for approval.

## Workflow

```
Weekly Trigger (Monday 8am)
├─ Fetch: location list, past posts, current events/offers
├─ Generate: 1–3 post drafts per location via LLM
├─ Classify: evergreen vs. promotional
│  ├─ Evergreen (office hours, menu updates, event info) → auto_publish node
│  │  ├─ Format & schedule
│  │  └─ Post to GBP
│  │
│  └─ Promotional (discounts, pricing, seasonal) → review_agent node
│     ├─ RequestInput (human approval)
│     ├─ Marketing/ops team reviews for brand alignment
│     └─ Post approved content
│
└─ Log: scheduled posts, approval times
```

## ADK 2.0 Graph Definition

**Nodes:**
- `fetch_context` — Pull locations, events, prior posts from DB
- `generate_posts` — LLM drafting (1–3 posts per location)
- `classify_content` — Evergreen vs. promotional routing
- `auto_publish` — Format, schedule, post to GBP
- `review_agent` — RequestInput for human approval gates
- `log_schedule` — Audit trail to Firestore

**Transitions:**
```yaml
fetch_context → generate_posts → classify_content
classify_content →
  [evergreen_confidence > 0.85] auto_publish → log_schedule
  [promotional OR promotional_confidence > 0.7] review_agent → log_schedule
```

## Deployment

1. Set up GBP API credentials + multi-location access
2. Configure weekly cron trigger (e.g., Mondays 8am PT)
3. Link Slack/email for RequestInput notifications
4. Define location + brand context (industry, tone, prior posts)
5. Deploy workflow via Agents CLI

## Success Metrics

- Posts published per week per location (target: 1–3)
- Time-to-publish (target: <24 hours for auto-posts, <4 hours for reviewed)
- Engagement lift (impressions, clicks, direction requests)

## Implementation Notes

- Context window: Pull 4–8 prior posts for tone consistency
- Promotional keywords: Configurable per industry (e.g., "% off", "limited time")
- Scheduling: Respect location timezone + business hours
- Brand safety: Never post without approval if keywords detected
