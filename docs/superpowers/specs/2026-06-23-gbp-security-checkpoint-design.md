# Design Spec: GBP Review Triage Security Checkpoint

Add security controls to the GBP Review Triage Agent graph before any review comment reaches LLM nodes, ensuring PII scrubbing (SSNs and credit card numbers) and prompt injection defense.

## Goals

1. **PII Redaction**: Identify and scrub SSNs and Credit Card numbers from review comments before they reach any LLM reviewer, agent logs, or human approval payloads. Keep track of which categories were redacted.
2. **Prompt Injection Defense**: Detect attempts to bypass rules or force auto-approval in comments. Route these malicious requests directly to a human reviewer, flag them as a security event, and disable LLM auto-generation for them entirely.

## Proposed Design

### 1. Data Models (`app/models.py`)

Update `TriageResult` to return a list of redacted PII categories:

```python
class TriageResult(BaseModel):
    review_id: str
    status: str = Field(description="Triage status: 'replied' or 'flagged'")
    reply_text: str | None = Field(
        default=None, description="Generated response if status is 'replied'"
    )
    flag_reason: str | None = Field(
        default=None, description="Reason for flagging if status is 'flagged'"
    )
    redacted_categories: list[str] | None = Field(
        default=None, description="Categories of PII redacted from the review comment"
    )
```

### 2. Security Checkpoint Node (`app/agent.py`)

#### Local Scrubbing & Luhn Validation
We implement local, deterministic helpers in `app/agent.py`:
*   `is_luhn_valid(number_str: str) -> bool`: Verifies a digit sequence represents a valid credit card pattern using the Luhn checksum.
*   `scrub_pii(comment: str) -> tuple[str, list[str]]`: Matches SSN and CC patterns. Replaces matches with `[REDACTED_SSN]` and `[REDACTED_CC]` respectively, returning the scrubbed text and the list of redacted categories.

#### Prompt Injection Detection
*   `detect_prompt_injection(comment: str) -> bool`: Checks the comment text (case-insensitive) for injection indicators, such as `"ignore all previous"`, `"force auto-approval"`, `"bypass rules"`, `"forget instructions"`, etc.

#### Node Definition
```python
@node
async def security_checkpoint(ctx: Context, node_input: Any):
    """Scrubs PII and detects prompt injection before any LLM processing."""
    # 1. Parse review input
    if "current_review" in ctx.state:
        review = ReviewInput(**ctx.state["current_review"])
    elif isinstance(node_input, dict):
        review = ReviewInput(**node_input)
    else:
        review = node_input

    # 2. Scrub PII
    scrubbed_comment, redacted = scrub_pii(review.comment)
    review.comment = scrubbed_comment
    
    # Store redacted categories and updated review in state
    ctx.state["redacted_categories"] = redacted
    ctx.state["current_review"] = review.model_dump()

    # 3. Check for Prompt Injection
    if detect_prompt_injection(scrubbed_comment):
        ctx.state["is_security_event"] = True
        return Event(
            output={
                "review": review.model_dump(),
                "reason": "Security Event: Prompt Injection Detected"
            },
            actions=EventActions(route="flag"),
        )
    
    # Continue to normal classification if clean
    return Event(
        output=review.model_dump(),
        actions=EventActions(route="classify"),
    )
```

### 3. Graph Edge Configuration

Update the `Workflow` edges to place `security_checkpoint` as the root node:

```python
root_agent = Workflow(
    name="gbp_triage_agent",
    output_schema=TriageResult,
    edges=[
        Edge(from_node=START, to_node=security_checkpoint),
        Edge(from_node=security_checkpoint, to_node=flag_for_human, route="flag"),
        Edge(from_node=security_checkpoint, to_node=classify_review, route="classify"),
        Edge(from_node=classify_review, to_node=auto_reply, route="auto_reply"),
        Edge(from_node=classify_review, to_node=flag_for_human, route="flag"),
    ],
    description="Ambient GBP review triage agent with security controls, auto-reply and human-in-the-loop flags.",
)
```

### 4. Downstream Node Safeguards

*   **`auto_reply`**: Incorporates `ctx.state.get("redacted_categories")` into the final `TriageResult`.
*   **`flag_for_human`**:
    *   Saves `ctx.state.get("redacted_categories")` to the final `TriageResult`.
    *   If `ctx.state.get("is_security_event")` is `True` or the reason starts with `"Security Event"`, the node blocks any model call (even if the human inputs `"APPROVE"` or the offline eval runner auto-approves) and immediately sets `reply_text = "[Security Event] Review flagged for prompt injection. Auto-generation disabled."`

## Verification Plan

### Automated Tests
1. **Unit Tests**:
   Create `tests/unit/test_security.py` to test:
   *   `is_luhn_valid` helper function.
   *   `scrub_pii` correctly redacts valid CCs/SSNs and ignores invalid ones.
   *   `detect_prompt_injection` flags malicious phrases.
2. **Integration Tests**:
   Run the offline evaluation suite using `uv run agents-cli eval generate` and `agents-cli eval grade` to verify that the security checkpoint routes correctly and does not fail when processing flagged injections or redacted reviews.
