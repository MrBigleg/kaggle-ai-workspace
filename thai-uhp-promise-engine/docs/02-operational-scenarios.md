# Operational Scenarios

## Scenario A: Lamborghini in Isaan

### Situation

A Lamborghini Huracan driver damages a rear tire near Udon Thani or Khon Kaen. The required tire is an uncommon UHP size, likely with a high speed rating and possibly staggered front/rear setup.

### Why it fails today

- Local branch may not stock rare rear sizes.
- Inventory may show one unit, but the customer needs a pair.
- Bangkok DC may have the SKU, but transfer timing is uncertain.
- A service advisor may suggest a non-equivalent tire under pressure.
- Customer expects premium handling and exact communication.

### Prototype decision

The system checks fitment, inventory, branch bay availability, and route timing. It either promises a fit or refuses to promise with a clear reason.

### Evidence needed

- Vehicle fitment profile
- SKU master with size, load index, speed rating, brand, and UHP category
- Branch/DC stock by SKU
- Branch service bay schedule
- Branch and DC coordinates
- Route ETA from stock source to target branch
- Transfer cut-off rules

## Scenario B: Bangkok premium branch stockout

### Situation

A Porsche 911 customer requests same-day tire replacement at a central Bangkok branch. The branch has no stock, but another branch across Bangkok has two units.

### Why it fails today

- Cross-branch visibility may be stale.
- Traffic makes "nearby" unreliable.
- A branch transfer can arrive after the customer's slot.
- The customer may leave for a competitor if ETA is vague.

### Prototype decision

The system compares transfer routes and bay times, then recommends either a branch transfer, customer relocation, or next-slot promise.

### Evidence needed

- Live or mock branch stock
- Reservation status
- Branch-to-branch route ETA
- Bay calendar
- Customer appointment time

## Scenario C: Resort / track weekend demand spike

### Situation

A performance-car group travels to a regional destination or track-adjacent area. Demand for UHP replacement spikes for a short window.

### Why it fails today

- Historical average demand hides event-driven spikes.
- Local branches do not hold premium SKUs.
- Late repositioning is costly.
- The system needs to know whether pre-positioning is worth it.

### Prototype decision

The system flags temporary stockout risk and recommends pre-positioning selected UHP SKUs before the event window.

### Evidence needed

- Historical UHP sales
- Quote/request logs
- Current inventory
- Event or location signal
- Transfer lead time and cost
- SKU margin

## Recommended demo scenario

Use Scenario A for the main capstone story. It is sharper, easier to explain, and makes the multi-agent system necessary.

