# Test Cases & Scenarios
# GBP Suspension Early Warning Agent
#
# Status: Template — Ready for implementation
# Reference: See ../1-gbp-review-triage-agent/test-cases.md for detailed pattern

## Test Case 1: Status Change Detected (Published → Suspended)

```json
{
  "name": "suspension_detected",
  "input": {
    "location_id": "10243505254051496320",
    "previous_status": "PUBLISHED",
    "current_status": "SUSPENDED",
    "suspended_at": "2026-06-23T14:30:00Z"
  },
  "expected_output": {
    "action": "auto_alert",
    "alert_sent": true,
    "priority": "URGENT",
    "diagnostic_run": true
  },
  "assertions": [
    "output.action == 'auto_alert'",
    "output.alert_sent == true",
    "output.priority == 'URGENT'"
  ]
}
```

---

See ../1-gbp-review-triage-agent/test-cases.md for full testing pattern and CLI commands.
