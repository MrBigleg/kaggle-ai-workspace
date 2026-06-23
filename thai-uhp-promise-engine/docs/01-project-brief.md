# Project Brief

## Working title

Thai UHP Promise Engine: grounded multi-agent fulfillment for premium tire customers in Thailand.

This is an independent proof of concept. A large Thailand auto service chain such as B-Quik can be used as market inspiration, but the project is not presented as a B-Quik engagement.

## Core problem

National auto service chains in Thailand are strong at broad coverage and standard replacement tires. UHP tires are different:

- Exact fitment matters.
- SKUs are expensive to hold everywhere.
- Demand is sparse and geographically uneven.
- Customers are high-value and time-sensitive.
- Service promises depend on inventory, logistics, and bay capacity all being true at once.

The operational failure is not "AI cannot recommend tires." The failure is that a branch cannot confidently promise the right tire, at the right place, by the right time, with reliable fallback options.

## Sharp edge case

A Lamborghini driver in Isaan / Northeast Thailand needs an uncommon UHP fitment after tire damage. They may be far from Bangkok premium-stock density. The system must decide whether a same-day or next-day fit is actually possible.

This is a good capstone scenario because it is:

- Specific
- High value
- Logistically hard
- Groundable with branch locations, route data, inventory records, and fitment tables
- Easy to demo with maps, stock tables, and agent traces

## Users

Primary operational users:

- Branch service advisor
- Regional inventory planner
- DC/transfer coordinator

Secondary users:

- Premium customer
- Country operations leader
- Category manager for UHP tires

## Main decision

The system must return one of four decisions:

1. **Promise now**: exact approved SKU is available and fitment slot is feasible.
2. **Promise by transfer**: exact approved SKU can arrive before the slot.
3. **Offer grounded alternatives**: equivalent approved SKUs are available, with tradeoffs.
4. **Do not promise**: no safe, verifiable path exists.

## Out of scope for prototype

- Dynamic pricing optimization
- Full ERP integration
- Payment capture
- Warranty adjudication
- Fully automated customer messaging
- Real-time proprietary retailer inventory unless access is granted

## Success criteria

The prototype wins if it can show:

- A non-hallucinated tire fulfillment decision
- Agent handoffs with inspectable state
- Verifiable evidence behind every promise
- Realistic fallback paths
- A Thailand-specific logistics constraint, not a generic ecommerce demo
