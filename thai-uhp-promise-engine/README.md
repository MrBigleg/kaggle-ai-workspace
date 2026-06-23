# Thai UHP Promise Engine

Multi-agent prototype for a Thailand ultra-high-performance tire fulfillment problem.

This is an independent proof of concept for the Kaggle AI Agents Intensive Capstone. It is inspired by real Thailand auto service and tire distribution pain points, not linked to or endorsed by any specific retailer.

## One-line concept

An agentic promise-to-fit system that answers: "Can we fit the exact UHP tires this driver needs, at this branch, by this time, with evidence?"

## Why this niche matters

UHP tire demand is low-volume, high-margin, and operationally unforgiving. A normal tire workflow can tolerate substitutions and loose ETAs. A Lamborghini, Porsche, BMW M, Mercedes-AMG, or modified performance car often cannot.

The hardest cases are not only in Bangkok. A driver in Isaan / Northeast Thailand may need an exact staggered fitment, high speed rating, or uncommon rim size far from the main premium inventory pool. That creates a concrete fulfillment problem:

- The branch may not hold the exact SKU.
- Nearby branches may have partial sets only.
- The DC may have stock but miss the fitting window.
- A vague ETA wastes a bay slot and loses a premium customer.
- An unsafe or unapproved substitute can damage trust.

## Project direction

The strongest capstone direction is the **Thai UHP Promise Engine**, combining:

1. Fitment validation
2. Inventory and reservation checks
3. Branch/DC transfer feasibility
4. Route and ETA confidence
5. Operational recovery when the first plan fails

## Documentation map

- [Project Brief](docs/01-project-brief.md)
- [Operational Scenarios](docs/02-operational-scenarios.md)
- [Agent Architecture](docs/03-agent-architecture.md)
- [Grounding and Data Plan](docs/04-grounding-and-data-plan.md)
- [Prototype Roadmap](docs/05-prototype-roadmap.md)
- [Capstone Submission Plan](docs/06-capstone-submission-plan.md)
- [External API Grounding](docs/07-external-api-grounding.md)
- [Stakeholder Validation Questions](docs/08-stakeholder-validation-questions.md)
- [Thai Android Voice Bolt-on](docs/09-thai-android-voice-bolt-on.md)
- [Data Contracts](data/README.md)

## Prototype output

The prototype should produce a grounded fulfillment decision:

```text
Request: Lamborghini Huracan, rear tire damaged near Udon Thani.
Need: 305/30 ZR20, approved UHP fitment, pair preferred.
Decision: Cannot safely promise same-day fit at local branch.
Best plan: Reserve pair at Bangkok DC, transfer overnight to Khon Kaen branch,
fit tomorrow 14:00-15:00, with fallback equivalent SKU if customer approves.
Evidence: SKU master, branch stock, DC stock, route ETA, branch bay schedule.
```

Optional bolt-on: a Thai-first Android voice app can capture a driver or branch advisor's spoken request in Thai, translate it into the English backend schema, and return a Thai explanation of the grounded promise decision.

## Build principle

No agent should invent availability, fitment, or ETA. Every customer-facing promise must cite a structured data source, API result, or explicit assumption.
