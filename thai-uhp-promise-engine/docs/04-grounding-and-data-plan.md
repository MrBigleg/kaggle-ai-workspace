# Grounding and Data Plan

## Grounding principle

Every final decision must be traceable to an evidence pack. The system should show which facts were retrieved, which assumptions were applied, and where uncertainty remains.

## Data tiers

### Tier 1: Public or mockable data for capstone

Use this for the prototype without internal access.

- Thai speech/translation fixtures for request intake
- Branch coordinates
- DC coordinates
- Candidate route paths and ETAs
- Google Places style branch lookup
- Google Maps style route duration
- Public weather/rain/flood alerts where available
- Mock SKU catalog
- Mock fitment table
- Mock inventory snapshots
- Mock branch bay calendar

### Tier 2: Partner data if a retailer or distributor engages

Use this if access is granted.

- Real branch inventory by SKU
- Real DC inventory by SKU
- Reservation and appointment records
- Internal transfer lead times
- Sales and lost-sales logs
- Inbound PO/ASN data
- Tire aging/DOT records
- Gross margin and cost-to-transfer

## Minimum prototype datasets

### Branches

Fields:

- branch_id
- branch_name
- region
- province
- latitude
- longitude
- service_bay_count
- uhp_capable
- opening_hours

### Distribution centers

Fields:

- dc_id
- dc_name
- latitude
- longitude
- cut_off_time
- overnight_transfer_supported

### SKU catalog

Fields:

- sku
- brand
- pattern
- size
- load_index
- speed_rating
- run_flat
- uhp_category
- approved_vehicle_segments

### Fitment table

Fields:

- vehicle_make
- vehicle_model
- model_year
- trim
- front_size
- rear_size
- minimum_load_index
- minimum_speed_rating
- notes

### Inventory snapshot

Fields:

- location_type
- location_id
- sku
- on_hand_qty
- reserved_qty
- available_qty
- snapshot_time

### Bay schedule

Fields:

- branch_id
- slot_start
- slot_end
- service_type
- available

### Route estimate

Fields:

- origin_id
- destination_id
- departure_time
- distance_km
- duration_minutes
- arrival_time
- confidence
- source

### Thai language request fixture

Fields:

- request_id
- original_language
- original_transcript
- translated_request
- extracted_vehicle
- extracted_location
- extracted_tire_size
- extracted_urgency
- translation_confidence
- requires_confirmation

## External API candidates

These are candidates to verify before implementation:

- Speech-to-text for Thai voice input
- Translation between Thai and English backend schema
- Google Places style lookup for branch/place validation
- Google Maps Routes or Distance Matrix style ETA
- Weather API for heavy rain/flood disruption
- Public holiday/event calendar for demand and transfer constraints

## Hallucination controls

- The Promise Agent must return `do_not_promise` if required fields are missing.
- The Language Bridge Agent must preserve tire sizes, vehicle names, SKUs, and location names.
- The Fitment Agent must never approve a tire below load/speed requirements.
- The Availability Agent must distinguish `on_hand_qty` from `available_qty`.
- The Logistics Agent must include an ETA confidence score.
- The final output must include evidence references.

## Explicit assumptions for capstone

- Inventory data can be mocked as structured CSV/JSON.
- Branch and DC locations can be real or representative.
- Route estimates can come from an API or precomputed fixtures.
- The prototype does not claim real operational access to any specific retailer.
- The system is designed to plug into real data later.
