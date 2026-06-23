# Local SEO Report Agent

## Overview

Generates weekly local SEO performance reports for multi-location portfolios:
- **Auto-generate** KPI summaries for locations meeting targets
- **Human-in-the-loop** review for locations with 15%+ performance drops

## Problem Solved

Multi-location clients need weekly visibility into GBP performance (impressions, calls, direction requests). Manual report assembly is labor-intensive and hard to scale. This agent auto-generates summaries and flags anomalies for investigation.

## Workflow

```
Weekly Trigger (Friday 5pm)
├─ Fetch: GBP Insights API data for all locations (1-week window)
├─ Aggregate: impressions, actions (calls, directions), bookings if available
├─ Calculate: week-over-week change (%)
│  ├─ Loop through locations:
│  │  ├─ Compare current week vs. prior week
│  │  ├─ Detect: <-15% drops across any KPI
│  │  │
│  │  ├─ If no drops → auto_generate node
│  │  │  ├─ Formatted summary (markdown/PDF)
│  │  │  ├─ KPI table: impressions, calls, directions
│  │  │  ├─ Historical trend (4-week chart)
│  │  │  └─ Send to client via email
│  │  │
│  │  └─ If >15% drop → insight_agent node
│  │     ├─ RequestInput (human review)
│  │     ├─ Ops investigates likely causes
│  │     │  ├─ Check review sentiment (recent negative reviews?)
│  │     │  ├─ Check posting activity (went silent?)
│  │     │  ├─ Check photos/Q&A updates (stale content?)
│  │     │  └─ Check competitor activity (seasonal shift?)
│  │     ├─ Compile diagnostic report + recommendations
│  │     └─ Queue for client discussion or remediation
│  │
│  └─ Log: report sent, anomalies detected
│
└─ Email all reports + anomaly alerts
```

## ADK 2.0 Graph Definition

**Nodes:**
- `fetch_insights` — GBP Insights API for all locations (1-week window)
- `aggregate_kpis` — Combine metrics, calculate week-over-week %
- `detect_anomalies` — Flag >15% drops
- `auto_generate` — Format & send summary reports
- `insight_agent` — RequestInput for human investigation + diagnostics
- `log_reports` — Audit trail to Firestore

**Transitions:**
```yaml
fetch_insights → aggregate_kpis → detect_anomalies
detect_anomalies →
  [no_drops] auto_generate → log_reports
  [>15% drop detected] insight_agent → log_reports
```

## Deployment

1. Set up GBP Insights API credentials
2. Configure weekly cron (e.g., Fridays 5pm PT)
3. Link email templates (text + HTML, optional PDF)
4. Define anomaly threshold (default: -15% week-over-week)
5. Deploy workflow via Agents CLI

## Success Metrics

- Report generation latency (target: <30 min)
- Anomaly detection accuracy (target: >85% of flags match root cause)
- Client engagement (target: >60% open rate on weekly reports)
- Time savings (target: 2–4 hours per week per analyst)

## Implementation Notes

- Baseline: Pull 8-week history for trend context
- Anomaly scope: Check impressions, calls, directions separately (not just aggregate)
- Seasonality: Consider weekday/weekend + seasonal patterns if 8+ weeks history
- Missing data: Handle locations with <7 days of data gracefully
- PDF generation: Optional; consider Render.com or Cloud Functions for on-demand rendering
- Client-facing: Vary report detail based on contract tier (basic vs. premium)
