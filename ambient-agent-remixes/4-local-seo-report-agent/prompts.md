# System Prompts & Node Configuration
# Local SEO Report Agent
#
# Status: Template — Ready for implementation

## Report Generation Prompt

```
Generate a professional local SEO performance report for a business location.

Inputs:
- Location name, address
- Current week KPIs: impressions, calls, direction requests
- Prior week KPIs (for comparison)
- 4-week historical trend
- Anomalies detected (if any)

Output: Markdown formatted report with:
1. Executive summary (KPI snapshot)
2. Performance table (current vs. prior week, % change)
3. Trend chart description
4. Anomaly alerts (if >15% drop)
5. Recommended actions
```

---

See ../1-gbp-review-triage-agent/prompts.md for full LLM configuration pattern.
