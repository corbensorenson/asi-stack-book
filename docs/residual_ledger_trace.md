# Residual Ledger Trace

Command:

```bash
python3 scripts/validate_residual_ledger_trace.py
```

Result:

```text
experiments/residual_ledger_trace/results/2026-07-03-local.json
```

This is a cross-artifact residual trace over already committed repository
evidence. It is not a new synthetic record fixture. The validator reads the
Resource flagship lane, Resource workflow trace, Compact GVR slice,
Readiness/residual gate result, and the prior residual-honesty conservation
fixture, then records whether residual burdens and no-promotion decisions stay
visible across those artifacts.

Validated surfaces:

| Artifact lane | Residual surface checked | Boundary |
|---|---|---|
| Resource flagship | Seven deferred task-ticks are residualized, the hidden-deferral negative control remains visible, and five sublane no-promotion decisions remain review-accepted. | No production scheduler, economic outcome, workload-quality, or chapter-core support claim. |
| Resource workflow | Displaced costs remain residualized and the erased-displaced-cost control remains rejected. | No runtime budget enforcement, physical-feasibility, or model-quality claim. |
| Compact GVR | The selected compact receipt keeps an explicit repair residual and fallback path, while lossy exactness, negative-rate/no-fallback, and bounded-search-overrun controls remain rejected. | No deployed codec, generator, verifier, compression-utility, or benchmark claim. |
| Readiness/residual gate | Canary residual escrow and quarantine surfaces remain visible, while lost residual escrow is rejected. | No deployed readiness engine, residual-ledger storage, rollback execution, or AI safety claim. |

Lean bridge:

- `residual_ledger_trace_surface_bridge` in
  `lean/AsiStackProofs/CompactGenerativeSystems.lean` mirrors the finite trace
  summary: Resource artifact read, sublane decisions recorded, residualized
  deferrals visible, displaced costs residualized, Compact GVR residuals and
  controls visible, readiness escrow visible, lost-residual control rejected,
  no support-state effect, non-claim boundary, and no deployed-ledger claim.

Non-claims:

- This does not prove deployed residual-ledger behavior.
- This does not prove safety.
- This does not promote any chapter core claim.
- This does not prove model quality or benchmark performance.
- This improves drift detection and residual-surface accountability for the
  book's current local artifacts only.
