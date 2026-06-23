# Getting Started: Ambient Agent Remixes

## Quick Overview

You now have 5 fully-specified GBP ambient agent prototypes, each with:

- **README.md** — Complete specification, workflow diagram, success metrics
- **workflow.yaml** — ADK 2.0 graph definition (ready to implement)
- **prompts.md** — System prompts, LLM configs, tone guards
- **test-cases.md** — 10+ test scenarios with assertions

## Recommended Start Path

### Phase 1: Prototype (Weeks 1–2)

**Agent #1: GBP Review Triage Agent** ← START HERE
- Simplest workflow (3 nodes: extract → classify → auto_reply/escalate)
- Highest immediate ROI (handles most common GBP pain point)
- Best reference for patterns (fully detailed with examples)

**Steps:**
1. Read `1-gbp-review-triage-agent/README.md` for full context
2. Review `prompts.md` — especially "System Prompts" and "Response Tone Examples"
3. Study `workflow.yaml` — understand the node transitions
4. Run local test cases: `agents workflow test --test-cases test-cases.md`
5. Deploy to ADK runtime: `agents workflow deploy`

### Phase 2: Build (Weeks 2–3)

Once Agent #1 is deployed and logging data:

**Agent #4: Local SEO Report Agent**
- Reusable data-fetch patterns (similar to Agent #1 structure)
- Pairs naturally with Agent #1 (reviews + performance metrics)
- Lower complexity than #2, #3, #5

**Agent #2: GBP Content Calendar Agent**
- More LLM-heavy (post generation, classification)
- Weekly cadence (good for ops scheduling)
- Natural follow-up to Agent #1

### Phase 3: Expand (Weeks 3+)

**Agent #3: GBP Suspension Early Warning Agent**
- Highest operational criticality (15-minute polling)
- Most complex diagnostic logic
- Best deployed after ops are comfortable with #1 and #4

**Agent #5: Client Onboarding Agent**
- Solves your own ops bottleneck (internal workflow)
- Integrates with existing client onboarding process
- Can be built in parallel with #3

---

## File Structure

```
ambient-agent-remixes/
├── README.md                           ← Overview & architecture
├── SETUP.md                            ← Environment setup & CLI commands
├── GETTING_STARTED.md                  ← This file
│
├── 1-gbp-review-triage-agent/
│   ├── README.md                       ← Full specification
│   ├── workflow.yaml                   ← ADK 2.0 definition (COMPLETE)
│   ├── prompts.md                      ← System prompts (COMPLETE)
│   └── test-cases.md                   ← Test scenarios (COMPLETE)
│
├── 2-gbp-content-calendar-agent/
│   ├── README.md
│   ├── workflow.yaml                   ← Template (ready to implement)
│   ├── prompts.md                      ← Template
│   └── test-cases.md                   ← Template
│
├── 3-gbp-suspension-early-warning-agent/
│   ├── README.md
│   ├── workflow.yaml                   ← Template
│   ├── prompts.md                      ← Template
│   └── test-cases.md                   ← Template
│
├── 4-local-seo-report-agent/
│   ├── README.md
│   ├── workflow.yaml                   ← Template
│   ├── prompts.md                      ← Template
│   └── test-cases.md                   ← Template
│
└── 5-client-onboarding-agent/
    ├── README.md
    ├── workflow.yaml                   ← Template
    ├── prompts.md                      ← Template
    └── test-cases.md                   ← Template
```

---

## Next Immediate Steps

### 1. Set Up Environment (15 min)

Follow SETUP.md to install:
- Google Agents CLI
- ADK 2.0
- Google Cloud credentials

```bash
npm install -g @google-cloud/agents-cli
gcloud auth application-default login
```

### 2. Study Agent #1 (1 hour)

```bash
# Read in order:
cat 1-gbp-review-triage-agent/README.md
cat 1-gbp-review-triage-agent/prompts.md
cat 1-gbp-review-triage-agent/workflow.yaml
```

### 3. Test Locally (30 min)

```bash
cd 1-gbp-review-triage-agent

# Run test suite
agents workflow test --definition workflow.yaml --test-cases test-cases.md

# Test specific case
agents workflow test --definition workflow.yaml --test test-cases.md:positive_review_5_stars
```

### 4. Customize for Your GBP Account (1 hour)

**workflow.yaml:**
- Replace `${GBP_API_KEY}`, `${GBP_CLIENT_ID}`, etc. with real creds
- Update location list (fetch from your client DB)
- Set Slack/email channels

**prompts.md:**
- Adjust sensitive keywords per industry (e.g., restaurants vs. healthcare)
- Customize tone/style (casual vs. formal)
- Add client-specific response templates

**config.yaml (create new):**
```yaml
locations:
  - location_id: "10243505254051496320"
    location_name: "Main Street Cafe"
    industry: "restaurant"
    sensitive_keywords:
      - "refund"
      - "poisoning"
      - "dangerous"

response_rules:
  auto_reply_min_rating: 4
  escalation_timeout: 4h
  slack_channel: "C12345"
```

### 5. Deploy to ADK (30 min)

```bash
# Set environment variables
export GBP_API_KEY="YOUR_KEY"
export GBP_CLIENT_ID="YOUR_CLIENT_ID"
export SLACK_BOT_TOKEN="xoxb-YOUR-TOKEN"

# Deploy
agents workflow deploy \
  --definition 1-gbp-review-triage-agent/workflow.yaml \
  --name gbp-review-triage-agent \
  --env-vars .env
```

### 6. Monitor & Iterate (ongoing)

```bash
# Check logs
gcloud logging read "resource.type=cloud_run" --limit 50 --format json

# Review Firestore audit trail
gcloud firestore documents list --collection-id gbp_review_triage_log
```

---

## Success Criteria

### Agent #1 Ready for Production When:

- ✅ Test suite passes 100% (all 10 test cases)
- ✅ Response latency < 2 minutes (average)
- ✅ Auto-reply success rate > 95%
- ✅ Tone validation < 5% failure rate
- ✅ Human escalation rate 15–25% (expected range)
- ✅ Slack notifications working reliably
- ✅ Firestore audit trail complete

### Metrics to Track

| Metric | Target | Alert If |
|--------|--------|----------|
| Auto-reply latency | <2 min | >5 min |
| Success rate | >95% | <90% |
| Escalation rate | 15–25% | <10% or >40% |
| Tone guard fail | <5% | >10% |
| API errors | <1% | >2% |

---

## Common Issues & Troubleshooting

### "API Key Invalid"
- Verify `GBP_API_KEY` env var is set: `echo $GBP_API_KEY`
- Check API is enabled in Google Cloud Console

### "Slack RequestInput Not Firing"
- Verify `SLACK_BOT_TOKEN` and `SLACK_CHANNEL_ID` env vars
- Test bot permissions in Slack workspace

### "Test Case Fails on Assertion"
- Check LLM provider (Claude vs. Gemini vs. GPT)
- Verify temperature/max_tokens in prompts.md match workflow.yaml
- Re-run with `--verbose` flag for debugging

### "Workflow Timeout"
- Increase node timeout in workflow.yaml
- Check GBP API rate limits (batch calls if needed)
- Monitor Cloud Logging for bottlenecks

---

## References

- [ADK 2.0 Quickstart](https://developers.google.com/business/guides/agents-cli)
- [GBP API Documentation](https://developers.google.com/my-business/reference/rest/v4)
- [Enterprise Cloud Scale: Expense Agent](https://codelabs.developers.google.com/enterprise-cloud-scale-deploying-the-expense-agent-to-agent-runtime-on-google-cloud)
- [Agents SDK Docs](https://github.com/google-cloud/agents-sdk)

---

## Questions?

Start with:
1. **agent README.md** — What is this agent supposed to do?
2. **workflow.yaml** — How does it flow?
3. **prompts.md** — How does it decide?
4. **test-cases.md** — Show me examples

Good luck! 🚀
