# Thai Android Voice Bolt-on

## Purpose

The core system can run in English because most backend data, schemas, APIs, and technical operations are easier to normalize in English. The frontline experience in Thailand should not require that.

This bolt-on lets Thai drivers or branch advisors speak naturally in Thai, then converts the request into the English operational schema used by the Thai UHP Promise Engine.

## Why it matters

This is a real adoption pain point:

- Branch advisors may speak Thai but backend systems often use English fields.
- Customers describe vehicles and locations informally.
- Tire requests mix Thai sentences with English brand names and numeric tire sizes.
- A bad translation can create a wrong fitment, wrong branch, or unsafe promise.

## Product shape

Android app for:

- Branch advisor intake
- Customer hotline intake
- Field/courier escalation
- Optional premium customer self-service later

The app should be a thin capture and confirmation layer, not a separate decision engine.

## Workflow

```text
Thai speech or typed request
  -> speech-to-text
  -> translation and protected-term preservation
  -> structured English request
  -> Thai UHP Promise Engine
  -> Thai explanation of decision and next action
```

## Language Bridge Agent

### Responsibilities

- Transcribe Thai voice
- Translate Thai request into English
- Extract vehicle, location, tire position, tire size, urgency, and branch preference
- Preserve protected terms exactly
- Ask for confirmation when uncertain
- Translate the final promise decision back into Thai

### Protected terms

Never paraphrase these:

- Tire sizes: `305/30 ZR20`, `275/35 R21`
- Load/speed ratings: `103Y`, `ZR`, `XL`
- Brand and pattern names: Michelin Pilot Sport 4S, Pirelli P Zero
- Vehicle names: Lamborghini Huracan, Porsche 911, BMW M4
- Branch, district, province, and region names
- SKU and order IDs

## Structured handoff

```json
{
  "source": "android_thai_voice",
  "original_language": "th",
  "original_transcript": "Thai transcript captured by the app",
  "translated_request": "English translation for backend processing",
  "structured_request": {
    "vehicle_make": "Lamborghini",
    "vehicle_model": "Huracan",
    "current_location": "Udon Thani",
    "preferred_branch": "Khon Kaen",
    "requested_position": "rear",
    "known_tire_size": null,
    "urgency": "tomorrow_afternoon"
  },
  "protected_terms_detected": ["Lamborghini", "Huracan", "Udon Thani", "Khon Kaen"],
  "translation_confidence": 0.86,
  "requires_confirmation": false
}
```

## Confirmation behavior

Ask the advisor/customer to confirm when:

- Vehicle model is ambiguous
- Tire position is unclear
- Location could refer to multiple places
- Tire size is detected with low confidence
- Urgency conflicts with route or bay feasibility

## Output back to Thai user

The final Thai-facing response should include:

- Can promise / cannot promise
- Branch
- Time window
- Tire or approved alternative
- What happens next
- Any required confirmation

It should not expose raw internal routing, inventory, or margin details unless the user is an authorized operator.

## MVP approach

Do not build the Android app first. First create:

- Thai request fixtures
- English structured outputs
- Translation confidence examples
- Protected-term tests

Then add the Android app as a thin UI once the core promise engine works.

## Capstone framing

Present this as an adoption and localization layer:

"The agent system reasons in a grounded English backend schema, while Thai users interact naturally in Thai. The translation layer is controlled, auditable, and designed around operational safety."
