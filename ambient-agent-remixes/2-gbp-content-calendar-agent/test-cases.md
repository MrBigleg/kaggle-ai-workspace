# Test Cases & Scenarios
# GBP Content Calendar Agent
#
# Status: Template — Ready for implementation
# Reference: See ../1-gbp-review-triage-agent/test-cases.md for detailed pattern

## Test Case 1: Evergreen Post (Auto-Publish Path)

```json
{
  "name": "evergreen_post_office_hours",
  "input": {
    "location_id": "10243505254051496320",
    "location_name": "Main Street Cafe",
    "industry": "Restaurant"
  },
  "expected_output": {
    "generated_posts": [
      {
        "title": "Summer Hours Update",
        "body": "We're now open until 10pm on weekends!"
      }
    ],
    "classification": "evergreen",
    "action": "auto_publish",
    "posts_scheduled": 1
  },
  "assertions": [
    "output.action == 'auto_publish'",
    "output.posts_scheduled > 0"
  ]
}
```

## Test Case 2: Promotional Post (Human Review Path)

```json
{
  "name": "promotional_post_discount",
  "input": {
    "location_id": "10243505254051496320",
    "location_name": "Main Street Cafe",
    "context": "Summer special: 20% off on weekday lunch"
  },
  "expected_output": {
    "classification": "promotional",
    "action": "human_review",
    "awaiting_approval": true
  },
  "assertions": [
    "output.action == 'human_review'",
    "output.awaiting_approval == true"
  ]
}
```

---

See ../1-gbp-review-triage-agent/test-cases.md for full test structure and running instructions.
