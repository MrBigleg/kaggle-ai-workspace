# System Prompts & Node Configuration
# Client Onboarding Agent
#
# Status: Template — Ready for implementation

## Blocker Detection Prompt

```
Analyze a GBP profile for common onboarding blockers.

Check for:
1. Profile status: Published | Suspended | Pending
2. Duplicate listings (same business within 0.5 miles)
3. NAP mismatches (name, address, phone inconsistencies)
4. Photo count (minimum 5 for baseline)

Output: JSON { "has_blockers": bool, "blockers": [...], "severity": "critical|high|medium" }
```

---

## Onboarding Report Prompt

```
Generate a professional onboarding completion report.

Include:
1. Status: All clear / Blockers found
2. Completed steps: Checkmarks for passed items
3. Action items: For blocked items
4. Next phase: Phase 2 (content strategy) or remediation plan
```

---

See ../1-gbp-review-triage-agent/prompts.md for full LLM configuration pattern.
