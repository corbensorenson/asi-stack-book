# Substrate Adoption Trace

This note records a deterministic, public-safe fixture for the Mathematical and
Search Substrates chapter. It turns the chapter's adoption protocol into a
checked trace without claiming that any substrate improves search, routing,
compression, representation, runtime, or model quality.

Run:

```bash
python3 scripts/validate_substrate_adoption_trace.py
```

To regenerate the committed result:

```bash
python3 scripts/validate_substrate_adoption_trace.py --write-result
```

Result artifact:

- `experiments/substrate_adoption_trace/results/2026-07-02-local.json`

## What The Trace Checks

The fixture contains four valid synthetic trace states:

- `valid_exploratory_registration`: a substrate is registered for planning
  only, with baseline, negative control, proof boundary, falsification
  condition, fallback, residuals, and non-claims attached.
- `valid_structural_only_receipt`: a structural-only proof boundary may be used
  for diagnostic discussion, not for quality or route promotion.
- `valid_consumer_axis_blocked`: a consumer request for an unmeasured axis is
  blocked rather than routed.
- `valid_negative_control_retirement`: a failed negative-control record retires
  or refutes the adoption route instead of laundering a favorable story.

It also contains eight expected-invalid controls:

- missing ordinary baseline;
- missing falsification condition;
- theorem spillover into a qualified route;
- unmeasured axis allowed into a canary route;
- failed negative control promoted anyway;
- missing fallback substrate;
- support-state promotion overclaim;
- missing non-claim boundary.

## Boundary

This is a record-shape and transition-boundary harness. It does not run a
substrate A/B test, does not prove representation efficiency, search quality,
routing quality, compression quality, model quality, runtime performance, or
downstream task quality, does not validate Circle, CoilMoECOT, Mamba, TreeLLM,
or Theseus substrate adoption, and does not create an evidence transition or
chapter-core support promotion.
