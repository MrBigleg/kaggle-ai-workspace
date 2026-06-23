# Capstone Submission Plan

## Capstone thesis

This project demonstrates a grounded multi-agent system for a real operational problem: premium UHP tire promise-to-fit fulfillment in Thailand.

## Why it is not generic

The system is specific to:

- UHP tire fitment constraints
- Thailand branch/DC geography
- Bangkok-to-regional transfer reality
- Rare premium vehicle demand outside Bangkok
- Branch bay scheduling and stock reservation

## Agentic value

A single prompt cannot safely solve this problem because the decision requires several different checks:

- Is the tire technically valid?
- Is the SKU available in the right quantity?
- Can it be reserved?
- Can it physically arrive on time?
- Is a service bay available?
- What should operations do if the answer is no?

The agents divide the work into auditable responsibilities.

## Grounded AI features to highlight

- Tool use over structured data
- Retrieval from fitment and SKU tables
- Thai voice/text intake translated into a structured English backend schema, if bolt-on is implemented
- Route/ETA grounding
- Evidence-backed final answers
- Rejecting unsafe or unsupported promises
- Agent trace inspection
- Scenario-based evaluation

## Demo narrative

1. Show the Lamborghini in Isaan scenario.
2. Optionally start with a Thai spoken or typed request from the Android/frontline intake layer.
3. Show the translated structured request that enters the English backend.
4. Run the request through the agent pipeline.
5. Show the Fitment Agent rejecting unsafe substitutes.
6. Show the Availability Agent finding only DC stock.
7. Show the Logistics Agent proving transfer feasibility or risk.
8. Show the Promise Agent making a clear operational decision.
9. Display the evidence pack and Thai customer-facing explanation.

## Evaluation metrics

Operational correctness:

- Approved fitment used
- Unsafe substitute rejected
- Quantity requirement respected
- Available inventory distinguished from reserved inventory
- ETA before bay slot
- Decision matches evidence

Business usefulness:

- Reduces vague promises
- Reduces lost premium sales
- Improves branch confidence
- Provides fallback plans

AI quality:

- Agents produce structured outputs
- Final answer cites evidence
- Missing data triggers refusal to promise
- No invented branch, stock, or ETA facts

## Suggested project name

Use **Thai UHP Promise Engine** for the capstone. It is short, operational, and clearly states the product value without tying the proof of concept to a specific retailer.

## Submission assets

- Notebook or app demo
- Mock data fixtures
- Agent architecture diagram
- Scenario walkthrough
- Evaluation table
- Short written explanation of grounding controls

## Risk register

### Risk: Looks like a tire recommendation chatbot

Mitigation: Keep the demo focused on fulfillment promise, not product marketing.

### Risk: No real retailer data

Mitigation: Use realistic structured fixtures and clearly label partner-only data.

### Risk: External API setup takes too long

Mitigation: Precompute route fixtures and design the API adapter as a replaceable module.

### Risk: LLM invents operational facts

Mitigation: Final decision must cite evidence references and fail closed on missing data.

### Risk: Translation changes the operational request

Mitigation: Preserve protected terms such as tire sizes, speed ratings, vehicle models, brand names, SKU codes, and location names. Low-confidence translations must require human confirmation.
