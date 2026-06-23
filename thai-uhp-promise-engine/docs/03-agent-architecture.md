# Agent Architecture

## System pattern

Use a small orchestrated multi-agent workflow. Each agent has one operational responsibility and passes structured outputs to the next agent.

```text
Customer request
  -> optional Thai Voice / Language Bridge Agent
  -> Fitment Agent
  -> Availability Agent
  -> Logistics Agent
  -> Promise Agent
  -> Evidence Pack
```

## Optional Agent 0: Thai Voice / Language Bridge Agent

### Role

Allow Thai drivers or branch advisors to speak naturally in Thai while the backend continues to use a structured English operational schema.

This is a bolt-on, not the core MVP. It becomes valuable because frontline tire requests often include mixed Thai, English brand names, vehicle nicknames, tire sizes, and location descriptions.

### Inputs

- Thai speech or typed Thai
- Optional branch/advisor ID
- Optional customer location
- Optional photo/OCR of sidewall or invoice in a later version

### Tools/data

- Android app voice capture
- Speech-to-text
- Translation to English
- Intent extraction
- Protected term dictionary for tire sizes, SKU codes, brand names, vehicle models, and province names

### Output

```json
{
  "original_language": "th",
  "original_transcript": "Thai customer request transcript",
  "translated_request": "Customer has a Lamborghini Huracan near Udon Thani and needs rear tires urgently.",
  "structured_request": {
    "vehicle_make": "Lamborghini",
    "vehicle_model": "Huracan",
    "location_text": "Udon Thani",
    "requested_service": "rear tire replacement",
    "urgency": "urgent"
  },
  "translation_confidence": 0.86,
  "needs_human_confirmation": false
}
```

### Guardrails

- Do not translate tire sizes into approximations.
- Preserve brand names, SKU codes, vehicle models, and locations as protected terms.
- Ask for confirmation when confidence is low.
- Return the final Promise Agent explanation in Thai, but keep evidence references tied to the English backend records.

## Agent 1: Fitment Agent

### Role

Convert a vehicle/customer request into valid tire requirements and approved SKU candidates.

### Inputs

- Vehicle make/model/year/trim
- Current tire size, if available
- Plate/VIN-derived vehicle profile, if available
- Customer location
- Tire damage context

### Tools/data

- Vehicle fitment table
- SKU catalog
- Brand/category rules
- Safety constraints: size, load index, speed rating, run-flat requirement

### Output

```json
{
  "vehicle_profile": "Lamborghini Huracan",
  "required_positions": ["rear_left", "rear_right"],
  "fitment_requirements": {
    "size": "305/30 ZR20",
    "minimum_speed_rating": "Y",
    "minimum_load_index": 103,
    "uhp_required": true
  },
  "approved_sku_candidates": ["SKU-PZERO-3053020Y", "SKU-PS4S-3053020Y"],
  "non_negotiable_constraints": ["size", "speed_rating", "load_index"]
}
```

## Agent 2: Availability Agent

### Role

Determine whether approved SKUs exist in usable quantity and can be reserved.

### Inputs

- Approved SKU candidates from Fitment Agent
- Target branch
- Desired fit date/time
- Required quantity

### Tools/data

- Branch inventory
- DC inventory
- Reservations
- Purchase order/inbound stock status
- Branch bay schedule

### Output

```json
{
  "stock_options": [
    {
      "sku": "SKU-PZERO-3053020Y",
      "source_type": "dc",
      "source_id": "BKK-DC-01",
      "available_qty": 2,
      "reservable": true
    }
  ],
  "bay_options": [
    {
      "branch_id": "KKN-01",
      "slot_start": "2026-06-16T14:00:00+07:00",
      "slot_end": "2026-06-16T15:00:00+07:00"
    }
  ]
}
```

## Agent 3: Logistics Agent

### Role

Estimate whether the tire can move from source to fitting branch before the service slot.

### Inputs

- Source branch/DC
- Destination branch
- Candidate fitting slot
- Transfer cut-off rules
- Current or predicted route conditions

### Tools/data

- Branch/DC coordinates
- Google Maps Platform style route/ETA data
- Historical transfer time
- Weather and flooding alerts, if available
- Courier cut-off rules

### Output

```json
{
  "route_plan": {
    "source_id": "BKK-DC-01",
    "destination_id": "KKN-01",
    "estimated_arrival": "2026-06-16T11:30:00+07:00",
    "confidence": 0.78,
    "risks": ["overnight_linehaul_variability"]
  },
  "feasible_before_slot": true
}
```

## Agent 4: Promise Agent

### Role

Make the final operational decision and produce a concise evidence pack.

### Inputs

- Fitment requirements
- Stock/reservation options
- Bay options
- Route feasibility

### Decision logic

1. Reject unsafe or unapproved fitments.
2. Prefer exact SKU and full required quantity.
3. Prefer available branch stock over transfers.
4. Only promise transfer if ETA clears slot with buffer.
5. If confidence is low, propose a recovery plan instead of a hard promise.

### Output

```json
{
  "decision": "promise_by_transfer",
  "customer_message": "We can fit the approved rear tire pair tomorrow at Khon Kaen branch between 14:00 and 15:00.",
  "operations_plan": [
    "Reserve 2 units SKU-PZERO-3053020Y at BKK-DC-01",
    "Dispatch overnight transfer to KKN-01",
    "Hold bay slot 14:00-15:00"
  ],
  "evidence_refs": [
    "fitment_table:HURACAN-2020",
    "inventory_snapshot:2026-06-15T13:00+07:00",
    "route_eta:BKK-DC-01_TO_KKN-01",
    "bay_calendar:KKN-01"
  ]
}
```

## Orchestration rule

The LLM can reason over options, but it cannot create facts. Availability, distance, ETA, branch identity, and fitment constraints must come from structured tools or explicit mock datasets.
