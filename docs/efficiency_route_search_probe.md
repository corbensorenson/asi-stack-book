# Efficiency Route-Search Probe

The efficiency route-search probe is a synthetic route-ledger check for the
chapter `the-efficient-asi-hypothesis`.

It validates two bounded route traces and six expected-invalid controls. The
valid traces cover minimum verified route selection and compression blocked by
repair/utility burden. The controls reject lower-cost eligible route omission,
missing hidden-cost classes, erased residuals, compression-utility overclaim,
authority bypass, and missing negative controls.

Run:

```bash
python3 scripts/validate_efficiency_route_search_probe.py
```

The local result record is:

```text
experiments/efficiency_route_search/results/2026-07-02-local.json
```

This probe does not prove route-search completeness, cost-estimate accuracy,
measured efficiency, model quality, compression utility, benchmark performance,
or chapter support-state promotion.
