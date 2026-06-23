# External API Grounding

## Purpose

External APIs should ground geography, route timing, place identity, and disruption signals. They should not be used to invent stock, fitment, reservations, or service capacity.

## Google Places style grounding

Use for:

- Validating branch names and addresses
- Finding candidate nearby branches or service locations
- Normalizing place IDs
- Getting latitude/longitude when branch coordinates are missing

Do not use for:

- Tire availability
- Service bay availability
- Internal branch capabilities for any specific retailer unless verified elsewhere

## Google Maps route/ETA style grounding

Use for:

- Branch-to-branch transfer estimates
- DC-to-branch delivery estimates
- Customer-to-branch travel comparison
- Checking whether route time clears the fitting slot with buffer

Required output:

```json
{
  "origin_id": "BKK-DC-01",
  "destination_id": "KKN-01",
  "departure_time": "2026-06-15T20:00:00+07:00",
  "duration_minutes": 810,
  "arrival_time": "2026-06-16T09:30:00+07:00",
  "source": "external_route_api_or_fixture",
  "retrieved_at": "2026-06-15T13:10:00+07:00"
}
```

## Weather and disruption grounding

Use for:

- Heavy rain risk
- Flood disruption risk
- Regional travel delay warnings
- Low-confidence transfer flags

The Logistics Agent should never simply say "bad weather." It should cite the retrieved alert or mark the risk as an assumption.

## API adapter pattern

Build adapters behind stable internal functions:

```text
resolve_place(query) -> place
estimate_route(origin, destination, departure_time) -> route_estimate
get_weather_risk(location, time_window) -> disruption_signal
```

This allows the capstone to run on fixtures first, then swap in live APIs later.

## Fixture-first rule

For the Kaggle prototype, start with precomputed fixtures:

- Known branch coordinates
- Known DC coordinates
- Route durations for scenario pairs
- A few disruption examples

Then clearly label which results are mocked and which would come from external APIs in production.

## Decision impact

External API data can change a decision from:

- `promise_by_transfer` to `do_not_promise`
- `same_day_fit` to `next_day_fit`
- `target_branch` to `alternate_branch`

It should not change:

- Approved tire fitment
- SKU availability
- Reservation status
- Bay capacity
