# Test Cases & Scenarios
# Client Onboarding Agent
#
# Status: Template — Ready for implementation
# Reference: See ../1-gbp-review-triage-agent/test-cases.md for detailed pattern

## Test Case 1: Clean Onboarding (Auto-Complete Path)

```json
{
  "name": "clean_onboarding_no_blockers",
  "input": {
    "client_name": "Main Street Cafe",
    "location_id": "10243505254051496320",
    "existing_gbp_access": true
  },
  "expected_output": {
    "action": "generate_report",
    "blockers_found": false,
    "steps_completed": 7,
    "phase_transition": "ready_for_phase_2",
    "onboarding_complete": true
  },
  "assertions": [
    "output.blockers_found == false",
    "output.steps_completed == 7",
    "output.onboarding_complete == true"
  ]
}
```

## Test Case 2: Blocker Detected (Human Review Path)

```json
{
  "name": "onboarding_blocker_suspended_profile",
  "input": {
    "client_name": "Downtown Pizza",
    "location_id": "10243505254051496321",
    "profile_status": "SUSPENDED"
  },
  "expected_output": {
    "action": "human_review",
    "blockers_found": true,
    "blocker_types": ["suspended_profile"],
    "awaiting_escalation": true
  },
  "assertions": [
    "output.blockers_found == true",
    "output.action == 'human_review'"
  ]
}
```

---

See ../1-gbp-review-triage-agent/test-cases.md for full testing pattern and CLI commands.
