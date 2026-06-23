# Prototype Roadmap

## Goal

Build a working demo that accepts a premium tire request and returns a grounded promise decision with agent traces and evidence.

## MVP workflow

1. User enters vehicle, location, requested branch, and urgency.
2. Fitment Agent identifies valid tire requirements and candidate SKUs.
3. Availability Agent checks mock branch/DC inventory and bay schedule.
4. Logistics Agent checks route feasibility from the stock source to the branch.
5. Promise Agent returns decision, operations plan, and evidence pack.

## Week-style build plan

### Phase 1: Data fixtures

Create small but realistic CSV/JSON fixtures:

- 8-12 branches across Bangkok, Khon Kaen, Udon Thani, Nakhon Ratchasima, and Chiang Mai
- 1-2 DCs
- 20-40 UHP tire SKUs
- 5-8 premium vehicle fitment profiles
- Inventory snapshots with intentional gaps
- Bay schedule examples
- Route ETA fixtures

### Phase 2: Deterministic tools

Build non-LLM functions first:

- `lookup_fitment(vehicle)`
- `find_approved_skus(fitment)`
- `check_inventory(skus, quantity)`
- `check_bay_slots(branch, requested_time)`
- `estimate_route(source, destination, time)`
- `reserve_plan(option)`

### Phase 3: Agents

Wrap tools with agents:

- Fitment Agent
- Availability Agent
- Logistics Agent
- Promise Agent

Each agent should emit structured JSON and a short human explanation.

### Phase 4: Demo interface

Build a lightweight interface:

- Scenario selector
- Request form
- Agent trace panel
- Evidence pack panel
- Map or route summary
- Final promise decision

### Phase 5: Evaluation

Create 10 test scenarios:

- Same-branch exact stock
- Nearby transfer feasible
- DC transfer feasible
- Partial stock only
- Unsafe substitute rejected
- Route arrives too late
- Bay unavailable
- Missing fitment data
- Isaan Lamborghini edge case
- Bangkok traffic constraint
- Thai voice request translated into backend schema

## Technical architecture options

### Option A: Python notebook

Best for Kaggle-native presentation and fast iteration.

Pros:

- Easy to show dataframes, traces, and evaluation
- Good for a capstone notebook
- Lower frontend burden

Cons:

- Less polished operational UI

### Option B: Streamlit app

Best for an interactive operational demo.

Pros:

- Simple UI
- Good for scenario switching
- Easy map/table display

Cons:

- Slightly more deployment work

### Option C: Next.js app

Best if the goal is a polished product prototype.

Pros:

- Strong product feel
- Better stakeholder demo

Cons:

- Higher implementation overhead for capstone timeline

## Recommended path

Start with a Python notebook plus structured data. If time allows, wrap the same logic in Streamlit.

The Android Thai voice app should stay as a bolt-on unless the core promise engine is already working. For the capstone, it can be demonstrated with recorded Thai transcripts or text fixtures before building a full mobile client.

## First implementation milestone

Produce this end-to-end result:

```text
Input:
Vehicle: Lamborghini Huracan
Location: Udon Thani
Requested branch: Khon Kaen
Need: rear tire pair
Urgency: tomorrow afternoon

Output:
Decision: promise_by_transfer
Evidence:
- approved rear size from fitment table
- 2 units available at Bangkok DC
- no branch stock in Isaan sample branches
- route ETA arrives before bay slot with buffer
- bay slot available at Khon Kaen
```

## Optional Android milestone

Produce this bolt-on result:

```text
Input:
Thai spoken request from driver or branch advisor.

Output:
Structured English backend request plus Thai confirmation message.

Critical behavior:
Tire sizes, brand names, vehicle models, and locations are preserved exactly.
Low-confidence translations require confirmation before the system checks fitment or inventory.
```
