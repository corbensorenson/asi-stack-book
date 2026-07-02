# Substrate Adoption Trace

This directory contains the deterministic result artifact for
`scripts/validate_substrate_adoption_trace.py`.

The trace is intentionally synthetic. It checks whether a substrate-adoption
record can preserve baselines, negative controls, consumer-axis limits,
fallbacks, retirement/refutation paths, residuals, and non-claim boundaries.
It is not a benchmark, model-quality result, Circle/Theseus replay,
CoilMoECOT run, or substrate adoption decision.

Regenerate:

```bash
python3 scripts/validate_substrate_adoption_trace.py --write-result
```
