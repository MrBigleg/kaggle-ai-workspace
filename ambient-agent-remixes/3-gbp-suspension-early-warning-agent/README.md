# GBP Suspension Early Warning Agent

## Overview

Monitors Google Business Profile health across a portfolio of locations in real-time:
- **Auto-alert** when status changes (Published → Suspended/Pending)
- **Triage diagnostic** that surface likely suspension causes for human review

## Problem Solved

Profile suspensions are catastrophic for local SEO but often go unnoticed for days. By the time a client realizes, they've lost traffic. This agent detects changes within minutes and surfaces diagnostics so ops can act fast.

## Workflow

```
Health Check Trigger (Every 15 min)
├─ Fetch: GBP profile status for all locations
├─ Compare: against last-known state in DB
├─ Detect: any status change
│  ├─ No change → log & continue
│  │
│  └─ Status changed → auto_alert node
│     ├─ Classify: Published → Suspended (violation)
│     │           → Pending (under review)
│     │           → Other
│     ├─ Run diagnostic:
│     │  ├─ Check recent reviews (policy violations?)
│     │  ├─ Check photos (inappropriate content?)
│     │  ├─ Check NAP consistency (address/phone mismatches?)
│     │  ├─ Check posting history (spam patterns?)
│     │  └─ Compile likely causes
│     │
│     ├─ Slack/Email alert with diagnostics
│     ├─ triage_agent node
│     │  ├─ RequestInput (human escalation)
│     │  ├─ Ops reviews diagnostics
│     │  └─ Queue corrective actions
│     │
│     └─ Update DB state
│
└─ Log: timestamp, status, alert sent
```

## ADK 2.0 Graph Definition

**Nodes:**
- `fetch_profiles` — GBP API list all locations
- `compare_state` — Detect status changes
- `auto_alert` — Classify change type + run diagnostics
- `diagnostic_suite` — Check reviews, photos, NAP, posting history
- `triage_agent` — RequestInput for human review + action queue
- `log_event` — Audit trail to Firestore

**Transitions:**
```yaml
fetch_profiles → compare_state
compare_state →
  [no_change] log_event
  [status_changed] auto_alert → diagnostic_suite → triage_agent → log_event
```

## Deployment

1. Set up GBP API credentials + multi-location access
2. Configure 15-min cron trigger (or on-demand polling)
3. Link Slack workspace for alerts
4. Define escalation contacts (ops lead, client contact)
5. Deploy workflow via Agents CLI

## Success Metrics

- Detection latency (target: <15 min from suspension to alert)
- Diagnostic accuracy (target: >80% of alerts match root cause)
- Resolution time (target: <4 hours from alert to status restored)

## Implementation Notes

- Baseline: On first run, capture current state as baseline
- Diagnostic depth: Run full suite only on status changes (avoid API quota waste)
- Alert tone: Urgent but actionable (include diagnostics + next steps)
- Persistence: Store all state changes for compliance/audit trail
- Rate limiting: Batch checks across locations, respect GBP API quotas
