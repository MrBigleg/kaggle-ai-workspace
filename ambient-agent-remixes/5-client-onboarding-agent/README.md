# Client Onboarding Agent

## Overview

Guides new GBP management clients through structured onboarding:
- **Auto-complete** standard setup steps (access requests, NAP audit, photo checklist)
- **Human-in-the-loop** review for complex cases (suspensions, duplicate listings, mismatched data)

## Problem Solved

CTB's 90-day onboarding package is critical revenue, but manual ops overhead is a scaling bottleneck. This agent automates routine checklist tasks and flags exceptions so humans can focus on strategy and complex triage.

## Workflow

```
New Client Added (Manual trigger or API)
├─ Onboarding initiated with location_id, client_name, existing_gbp_access
├─ auto_complete node:
│  ├─ Step 1: Send GBP access request email (template-driven)
│  ├─ Step 2: Validate existing NAP (name, address, phone) vs. GBP
│  ├─ Step 3: Audit existing photos (count, quality, optimization)
│  ├─ Step 4: Generate photo checklist (high-priority gaps)
│  ├─ Step 5: Flag duplicate listings (reverse geocoding check)
│  ├─ Step 6: Review Q&A section for gaps
│  ├─ Step 7: Check attributes/services completeness
│  │
│  └─ Auto-complete success path:
│     ├─ All steps validated
│     ├─ No blockers found
│     └─ Generate "Ready for Content Phase" report
│
├─ human_review node triggered if:
│  ├─ GBP profile is Suspended or Pending
│  │  → RequestInput: "Profile under review - escalate to legal?"
│  │
│  ├─ Duplicate listings detected (3+ results within 0.5mi)
│  │  → RequestInput: "Multiple profiles found - consolidate?"
│  │
│  ├─ Critical NAP mismatches (address/phone mismatch > 1 field)
│  │  → RequestInput: "NAP audit failed - resolve mismatches first?"
│  │
│  └─ Photo count <5 (missing baseline content)
│     → RequestInput: "Insufficient photos - client needs to upload 5+?"
│
├─ Resolution paths:
│  ├─ Auto-complete all steps → report generated → move to Phase 2
│  ├─ Human escalation → triage/correction → retry auto-complete
│  └─ Blocker unresolved → pause onboarding + schedule follow-up
│
└─ Log: onboarding progress, blockers, resolution time
```

## ADK 2.0 Graph Definition

**Nodes:**
- `init_onboarding` — Accept client details, initialize workflow state
- `validate_access` — Confirm GBP access, set up API calls
- `auto_complete` — Run standard checklist steps in sequence
- `detect_blockers` — Check for suspensions, duplicates, NAP mismatches
- `human_review` — RequestInput for exception cases
- `generate_report` — Onboarding summary + next steps
- `log_progress` — Audit trail to Firestore

**Transitions:**
```yaml
init_onboarding → validate_access → auto_complete
auto_complete → detect_blockers
detect_blockers →
  [no_blockers] generate_report → log_progress
  [has_blockers] human_review → [remediation] auto_complete (retry)
                               → [unresolved] pause_workflow
```

## Deployment

1. Set up GBP API credentials + service account
2. Create email templates (access request, checklist, phase reports)
3. Define blocker rules (suspension, duplicate threshold, NAP mismatch tolerance)
4. Link Slack/email for RequestInput escalations
5. Set up Firestore collection for onboarding state + progress
6. Deploy workflow via Agents CLI

## Success Metrics

- Auto-complete rate (target: >70% of onboardings with no blockers)
- Blocker detection latency (target: <30 min)
- Time to Phase 2 (target: <5 business days)
- Human escalation resolution time (target: <2 business days)

## Implementation Notes

- State persistence: Store onboarding state in Firestore to survive workflow retries
- Duplicate detection: Use reverse geocoding (Google Maps API) + business name similarity
- NAP validation: Check against authoritative sources (Google, Yelp, Apple Maps if available)
- Photo checklist: Prioritize by category (storefront, interior, team, product, service)
- Email tone: Professional but encouraging; acknowledge complexity of edge cases
- Retry logic: Allow manual re-trigger of failed steps (e.g., after NAP correction)
- Reporting: Generate PDF summary for client onboarding kickoff meeting
