# Test Cases & Scenarios
# Local SEO Report Agent
#
# Status: Template — Ready for implementation
# Reference: See ../1-gbp-review-triage-agent/test-cases.md for detailed pattern

## Test Case 1: Healthy Location (Auto-Generate Path)

```json
{
  "name": "healthy_location_week_over_week_growth",
  "input": {
    "location_id": "10243505254051496320",
    "location_name": "Main Street Cafe",
    "current_week": {
      "impressions": 2500,
      "calls": 45,
      "directions": 120
    },
    "prior_week": {
      "impressions": 2400,
      "calls": 42,
      "directions": 110
    }
  },
  "expected_output": {
    "action": "auto_generate",
    "report_generated": true,
    "anomalies_detected": false,
    "pct_change_impressions": 4.2,
    "pct_change_calls": 7.1
  },
  "assertions": [
    "output.action == 'auto_generate'",
    "output.anomalies_detected == false",
    "output.report_generated == true"
  ]
}
```

## Test Case 2: Location with 15%+ Drop (Human Review Path)

```json
{
  "name": "location_15_percent_drop",
  "input": {
    "location_id": "10243505254051496321",
    "location_name": "Downtown Pizza",
    "current_week": {
      "impressions": 1700,
      "calls": 22,
      "directions": 60
    },
    "prior_week": {
      "impressions": 2000,
      "calls": 26,
      "directions": 70
    }
  },
  "expected_output": {
    "action": "insight_agent",
    "anomalies_detected": true,
    "affected_metrics": ["impressions", "calls", "directions"],
    "awaiting_investigation": true
  },
  "assertions": [
    "output.action == 'insight_agent'",
    "output.anomalies_detected == true"
  ]
}
```

---

See ../1-gbp-review-triage-agent/test-cases.md for full testing pattern and CLI commands.
