# Data Contracts

This folder will hold CSV or JSON fixtures for the prototype.

The first build should use small, inspectable datasets. Keep them realistic enough to support the demo, but simple enough that every decision can be audited.

## Suggested files

```text
branches.csv
distribution_centers.csv
sku_catalog.csv
vehicle_fitments.csv
inventory_snapshots.csv
bay_schedule.csv
route_estimates.csv
test_scenarios.csv
```

## Key rule

The agents should only make promises from these datasets or from explicitly configured external tools. If the data is missing, stale, or contradictory, the correct answer is not a guess. The correct answer is a grounded refusal or escalation.

