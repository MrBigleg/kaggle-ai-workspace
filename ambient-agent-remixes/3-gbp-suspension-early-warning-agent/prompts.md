# System Prompts & Node Configuration
# GBP Suspension Early Warning Agent
#
# Status: Template — Ready for implementation

## Diagnostic Analysis Prompt

```
Analyze a GBP profile status change and identify likely root causes.

Inputs:
- Previous status: Published | Suspended | Pending
- Current status: Published | Suspended | Pending
- Recent reviews (sentiment + keywords)
- Recent photos (count, metadata)
- NAP data (name, address, phone consistency)
- Posting activity (frequency, recency)

Output: JSON { "likely_causes": [...], "severity": "critical|high|medium", "next_steps": [...] }
```

---

See ../1-gbp-review-triage-agent/prompts.md for full LLM configuration pattern.
