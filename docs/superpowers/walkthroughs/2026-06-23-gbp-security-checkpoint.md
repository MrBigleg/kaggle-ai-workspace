# Walkthrough: Add security: PII redaction & prompt-injection defense

This document chronicles the design, implementation, and verification of the security controls added to the **Google Business Profile (GBP) Review Triage** agent workflow.

## Overview

To prevent leakage of sensitive personal data (PII) and mitigate prompt injection attacks, we introduced a local, deterministic security checkpoint node `security_checkpoint` at the entry point of the triage graph.

## Implementation Details

### 1. Schema Extensions
- Added `redacted_categories: list[str] | None` to the `TriageResult` schema in [app/models.py](file:///c:/Users/craig/01_Projects/001_Kaggle/gbp-review-triage/app/models.py). This field lists the types of PII detected and redacted (e.g., `"SSN"`, `"Credit Card"`).

### 2. Safety Heuristics
Implemented three core validation functions in [app/agent.py](file:///c:/Users/craig/01_Projects/001_Kaggle/gbp-review-triage/app/agent.py):
- **Luhn Algorithm Validation**: Deterministically validates credit card candidates extracted via regex, reducing false positives.
- **PII Scrubbing**: Detects and redacts US Social Security Numbers (`[REDACTED_SSN]`) and valid Credit Cards (`[REDACTED_CC]`).
- **Prompt Injection Detection**: Scans inputs for phrases commonly associated with prompt injections (e.g., *"ignore all previous instructions"*, *"override rules"*, *"bypass security"*).

### 3. Entry Checkpoint Node
- Implemented `security_checkpoint` as the START node in the `root_agent` workflow graph.
- If a prompt injection is detected:
  - Bypasses the downstream LLM nodes (`classify_review` and any model calls in `flag_for_human`).
  - Sets `ctx.state["is_security_event"] = True` and routes directly to the human flag queue (`flag_for_human`).
- If no prompt injection is detected:
  - Scrubs any PII.
  - Updates the comment in `ctx.state["current_review"]` with the redacted version.
  - Routes to `classify_review` for normal routing based on rating or keyword criteria.

### 4. Downstream Safeguards
- Updated `flag_for_human` to identify when a review is flagged due to a security event:
  - Bypasses all Gemini API calls to prevent running untrusted user input against the LLM.
  - Generates a predefined warning response: `"[Security Event] Review flagged for prompt injection. Auto-generation disabled."`
- Updated both `auto_reply` and `flag_for_human` to populate the `redacted_categories` list in the final `TriageResult` output.

---

## Verification and Security Validation

We implemented comprehensive unit tests in [tests/unit/test_security.py](file:///c:/Users/craig/01_Projects/001_Kaggle/gbp-review-triage/tests/unit/test_security.py) and schema tests in [tests/unit/test_models.py](file:///c:/Users/craig/01_Projects/001_Kaggle/gbp-review-triage/tests/unit/test_models.py).

### Test Suite Execution
Run the unit test suite locally:
```bash
uv run pytest tests/unit/test_security.py tests/unit/test_models.py
```

### Verified Test Cases
1. **Luhn Validation Check**: Verified that correct Luhn checksums are accepted and invalid ones are rejected.
2. **PII Redaction (SSN & Credit Card)**: Verified that valid SSN formats and valid CC numbers are successfully detected and replaced, and corresponding metadata category is recorded.
3. **Prompt Injection Detection**: Verified that injection strings trigger detection.
4. **Clean Input Workflow Routing**: Verified that clean input passes through `security_checkpoint` and routes to `classify` node.
5. **Prompt Injection Workflow Routing**: Verified that injection triggers immediate `flag` routing from `security_checkpoint`.
6. **LLM Bypass on Flag Node**: Verified that if routed to `flag_for_human` as a security event, model calling is skipped and the predefined security warning reply is returned.
7. **TriageResult Schema Compliance**: Verified that `redacted_categories` compiles and is present in the output.
