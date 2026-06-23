# Test Cases & Scenarios
# GBP Review Triage Agent

## Test Case Format

```json
{
  "name": "Test Case Name",
  "input": { /* webhook payload */ },
  "expected_output": { /* expected workflow result */ },
  "assertions": [ /* conditions to verify */ ]
}
```

---

## Test Case 1: Positive Review (Auto-Reply Path)

**Scenario:** 5-star review, no sensitive keywords → should auto-reply

```json
{
  "name": "positive_review_5_stars",
  "input": {
    "location_id": "10243505254051496320",
    "review_id": "AixDSyk2VRmGlZE1gZmqTARjbOVQsqaZ8gzYWMv6IfJtBe-hRp0bFUL8RM7BJoH9Wd-ZJIl3w0_G-7LN9LMA8kHvQ",
    "rating": 5,
    "reviewer_name": "Jane Smith",
    "review_text": "Best Italian restaurant in the city! The pasta was incredible and the staff was so friendly. Will definitely come back!",
    "review_timestamp": "2026-06-23T14:30:00Z"
  },
  "expected_output": {
    "action": "auto_reply",
    "human_involved": false,
    "response_posted": true,
    "generated_response": "Thank you Jane! We're thrilled you loved our pasta. Our team can't wait to welcome you back!"
  },
  "assertions": [
    "output.action == 'auto_reply'",
    "output.human_involved == false",
    "output.response_posted == true",
    "length(output.generated_response) <= 140",
    "output.response_posted_timestamp > input.review_timestamp"
  ]
}
```

---

## Test Case 2: Positive Review with Minor Complaint (Auto-Reply Path)

**Scenario:** 4-star review with constructive feedback → should auto-reply

```json
{
  "name": "positive_review_4_stars_constructive",
  "input": {
    "location_id": "10243505254051496320",
    "review_id": "BixDSyk2VRmGlZE1gZmqTARjbOVQsqaZ8gzYWMv6IfJtBe-hRp0bFUL8RM7BJoH9Wd-ZJIl3w0_G-7LN9LMA8kHvR",
    "rating": 4,
    "reviewer_name": "Michael Chen",
    "review_text": "Great food and atmosphere, but service was a bit slow. Still would recommend!",
    "review_timestamp": "2026-06-23T15:45:00Z"
  },
  "expected_output": {
    "action": "auto_reply",
    "human_involved": false,
    "response_posted": true
  },
  "assertions": [
    "output.action == 'auto_reply'",
    "output.human_involved == false",
    "contains(output.generated_response, 'Michael')",
    "contains(output.generated_response, 'patience') OR contains(output.generated_response, 'appreciate')"
  ]
}
```

---

## Test Case 3: Negative Review (Escalation Path)

**Scenario:** 2-star review → should escalate to human

```json
{
  "name": "negative_review_escalation",
  "input": {
    "location_id": "10243505254051496320",
    "review_id": "CixDSyk2VRmGlZE1gZmqTARjbOVQsqaZ8gzYWMv6IfJtBe-hRp0bFUL8RM7BJoH9Wd-ZJIl3w0_G-7LN9LMA8kHvS",
    "rating": 2,
    "reviewer_name": "Sarah Johnson",
    "review_text": "Waited 45 minutes for appetizers. Food was cold when it arrived. Very disappointed.",
    "review_timestamp": "2026-06-23T16:20:00Z"
  },
  "expected_output": {
    "action": "human_escalated",
    "human_involved": true,
    "escalation_reason": "Low rating (< 4 stars)",
    "slack_message_sent": true,
    "awaiting_human_decision": true
  },
  "assertions": [
    "output.action == 'human_escalated'",
    "output.human_involved == true",
    "output.slack_message_sent == true",
    "output.awaiting_human_decision == true"
  ]
}
```

---

## Test Case 4: Review with Sensitive Keywords (Escalation Path)

**Scenario:** 5-star review BUT contains "refund" → escalate despite high rating

```json
{
  "name": "positive_rating_sensitive_keyword",
  "input": {
    "location_id": "10243505254051496320",
    "review_id": "DixDSyk2VRmGlZE1gZmqTARjbOVQsqaZ8gzYWMv6IfJtBe-hRp0bFUL8RM7BJoH9Wd-ZJIl3w0_G-7LN9LMA8kHvT",
    "rating": 5,
    "reviewer_name": "Tom Williams",
    "review_text": "Fantastic restaurant! Had to ask for a refund on one item but staff handled it perfectly. Great experience overall!",
    "review_timestamp": "2026-06-23T17:00:00Z"
  },
  "expected_output": {
    "action": "human_escalated",
    "human_involved": true,
    "detected_keywords": ["refund"],
    "escalation_reason": "Sensitive keywords detected despite positive rating"
  },
  "assertions": [
    "output.action == 'human_escalated'",
    "contains(output.detected_keywords, 'refund')",
    "output.human_involved == true",
    "output.escalation_reason contains 'Sensitive keywords'"
  ]
}
```

---

## Test Case 5: Highly Negative Review with Multiple Keywords (Escalation Path)

**Scenario:** 1-star review with multiple sensitive keywords → urgent escalation

```json
{
  "name": "urgent_escalation_dangerous_claim",
  "input": {
    "location_id": "10243505254051496320",
    "review_id": "EixDSyk2VRmGlZE1gZmqTARjbOVQsqaZ8gzYWMv6IfJtBe-hRp0bFUL8RM7BJoH9Wd-ZJIl3w0_G-7LN9LMA8kHvU",
    "rating": 1,
    "reviewer_name": "Anonymous",
    "review_text": "I got food poisoning from eating here. This is dangerous! Never coming back and I'm calling the health department.",
    "review_timestamp": "2026-06-23T18:15:00Z"
  },
  "expected_output": {
    "action": "human_escalated",
    "human_involved": true,
    "detected_keywords": ["food_poisoning", "dangerous", "never_coming_back"],
    "priority": "URGENT",
    "slack_mention": "@gbp-ops-oncall"
  },
  "assertions": [
    "output.action == 'human_escalated'",
    "output.priority == 'URGENT'",
    "length(output.detected_keywords) >= 2",
    "contains(output.detected_keywords, 'food_poisoning')",
    "contains(output.slack_mention, 'oncall') OR output.timeout_hours < 2"
  ]
}
```

---

## Test Case 6: Human Decision - Approved

**Scenario:** Review escalated, human approves custom response

```json
{
  "name": "human_escalation_approved",
  "input": {
    "location_id": "10243505254051496320",
    "review_id": "FixDSyk2VRmGlZE1gZmqTARjbOVQsqaZ8gzYWMv6IfJtBe-hRp0bFUL8RM7BJoH9Wd-ZJIl3w0_G-7LN9LMA8kHvV",
    "rating": 3,
    "reviewer_name": "David Lee",
    "review_text": "Good food but pricing is quite high for portion sizes.",
    "review_timestamp": "2026-06-23T19:30:00Z"
  },
  "human_response": {
    "decision": "approve",
    "comment": "We appreciate your feedback on value. Our portions reflect our commitment to quality ingredients.",
    "approved_at": "2026-06-23T19:45:00Z"
  },
  "expected_output": {
    "action": "human_approved",
    "human_involved": true,
    "response_posted": true,
    "posted_response": "We appreciate your feedback on value. Our portions reflect our commitment to quality ingredients.",
    "approval_latency_minutes": 15
  },
  "assertions": [
    "output.action == 'human_approved'",
    "output.response_posted == true",
    "output.approval_latency_minutes > 0 AND output.approval_latency_minutes < 240",
    "length(output.posted_response) <= 140"
  ]
}
```

---

## Test Case 7: Human Decision - Rejected

**Scenario:** Review escalated, human chooses not to respond

```json
{
  "name": "human_escalation_rejected",
  "input": {
    "location_id": "10243505254051496320",
    "review_id": "GixDSyk2VRmGlZE1gZmqTARjbOVQsqaZ8gzYWMv6IfJtBe-hRp0bFUL8RM7BJoH9Wd-ZJIl3w0_G-7LN9LMA8kHvW",
    "rating": 1,
    "reviewer_name": "Angry Customer",
    "review_text": "Worst experience ever. Rude staff, cold food, will never return!!!",
    "review_timestamp": "2026-06-23T20:00:00Z"
  },
  "human_response": {
    "decision": "reject",
    "approved_at": "2026-06-23T20:20:00Z"
  },
  "expected_output": {
    "action": "human_rejected",
    "human_involved": true,
    "response_posted": false,
    "reason": "No response posted (human decision)"
  },
  "assertions": [
    "output.action == 'human_rejected'",
    "output.response_posted == false",
    "output.human_involved == true"
  ]
}
```

---

## Test Case 8: Human Escalation Timeout

**Scenario:** Review escalated, human doesn't respond within 4 hours → auto-expire

```json
{
  "name": "human_escalation_timeout",
  "input": {
    "location_id": "10243505254051496320",
    "review_id": "HixDSyk2VRmGlZE1gZmqTARjbOVQsqaZ8gzYWMv6IfJtBe-hRp0bFUL8RM7BJoH9Wd-ZJIl3w0_G-7LN9LMA8kHvX",
    "rating": 2,
    "reviewer_name": "Impatient Customer",
    "review_text": "Service was terrible.",
    "review_timestamp": "2026-06-23T12:00:00Z"
  },
  "escalation_timeout": {
    "timeout_seconds": 14400,  // 4 hours
    "expired": true,
    "expired_at": "2026-06-23T16:00:00Z"
  },
  "expected_output": {
    "action": "human_timeout_expired",
    "human_involved": true,
    "response_posted": false,
    "reason": "No human response within 4-hour timeout window"
  },
  "assertions": [
    "output.action == 'human_timeout_expired'",
    "output.response_posted == false",
    "output.timeout_reason contains '4 hour' OR output.timeout_reason contains '4h'"
  ]
}
```

---

## Edge Cases to Test

### Test Case 9: Empty/Null Fields

```json
{
  "name": "edge_case_missing_reviewer_name",
  "input": {
    "location_id": "10243505254051496320",
    "review_id": "test-123",
    "rating": 5,
    "reviewer_name": null,
    "review_text": "Great restaurant!",
    "review_timestamp": "2026-06-23T21:00:00Z"
  },
  "expected_output": {
    "action": "auto_reply",
    "generated_response": "Thank you! We're thrilled you loved your experience. We look forward to your next visit!"
  },
  "assertions": [
    "output.action == 'auto_reply'",
    "NOT contains(output.generated_response, 'null')",
    "length(output.generated_response) > 0"
  ]
}
```

### Test Case 10: Very Long Review Text

```json
{
  "name": "edge_case_very_long_review",
  "input": {
    "location_id": "10243505254051496320",
    "review_id": "test-124",
    "rating": 5,
    "reviewer_name": "Verbose Customer",
    "review_text": "[1000+ word detailed review describing entire dining experience]",
    "review_timestamp": "2026-06-23T22:00:00Z"
  },
  "expected_output": {
    "action": "human_escalated",  // May escalate due to complexity
    "human_involved": true
  },
  "assertions": [
    "output.human_involved == true OR (output.action == 'auto_reply' AND length(output.generated_response) <= 140)"
  ]
}
```

---

## Running Tests

### Local Test Execution

```bash
# Run all tests
agents workflow test --definition workflow.yaml --test-cases test-cases.md

# Run specific test
agents workflow test --definition workflow.yaml --test test-cases.md:positive_review_5_stars

# Run with verbose output
agents workflow test --definition workflow.yaml --test-cases test-cases.md --verbose

# Run with assertions
agents workflow test --definition workflow.yaml --test-cases test-cases.md --assert-all
```

### Expected Output

```
✅ positive_review_5_stars
   └─ action: auto_reply
   └─ response_posted: true
   └─ latency: 1.2s

✅ negative_review_escalation
   └─ action: human_escalated
   └─ slack_message_sent: true
   └─ latency: 0.8s

❌ edge_case_very_long_review
   └─ assertion failed: length(output.generated_response) > 140
   └─ got: 156 characters
```

---

## Integration Tests (Post-Deployment)

Once deployed to ADK, test with real GBP webhooks:

```bash
# Trigger test webhook
curl -X POST https://your-agent.cloudfunctions.net/gbp-review-webhook \
  -H "Content-Type: application/json" \
  -d @test-cases.md:positive_review_5_stars

# Check Slack for response (human escalation cases)
# Check Firestore audit trail for action log
```

---

## Monitoring & Logging

Track these metrics post-deployment:

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Auto-reply latency | <2 min | >5 min |
| Human escalation rate | <20% | >40% |
| Auto-reply success rate | >95% | <90% |
| Human decision latency | <2 hours | >4 hours |
| Response tone validation fail | <5% | >10% |
