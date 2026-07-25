# Source Note: AI Simulation by Digital Twins

| Field | Value |
|---|---|
| Source ID | `ext_ai_simulation_digital_twins_2025` |
| Source title | AI Simulation by Digital Twins: Systematic Survey and Reference Framework |
| Source version / URL | <https://arxiv.org/abs/2506.06580> |
| Ingestion date | 2026-07-24 |

## Thesis

The survey positions a digital twin as a virtual representation linked to a
physical system for simulation, training, monitoring, and decision support.
The live linkage matters: a static simulator or dashboard does not become a
twin merely by adopting the label.

## Mechanisms

- physical-to-virtual sensing and state synchronization;
- virtual-to-physical decision or control paths;
- model calibration, fidelity envelopes, latency, and uncertainty;
- scenario generation, counterfactual simulation, and lifecycle updating;
- explicit sim-to-real transfer and residual tracking.

## Evidence

This is a systematic survey and reference framework, not a local digital-twin
deployment or proof of transfer. The reviewed systems and reported outcomes
retain their domain, hardware, model, data, and evaluation limits.

## Failure Modes

- stale or partial physical state presented as current reality;
- unmeasured fidelity gaps and latency;
- simulator exploitation or policy overfitting;
- feedback changing the physical process being modeled;
- transfer beyond the calibrated operating envelope;
- a monitoring replica being mislabeled as a decision-valid twin.

## Book Chapters Supported

- `embodied-agency-real-time-control-and-physical-safety`
- `governed-world-models-and-reality-grounding`

## Claims To Add Or Update

- A governed twin should expose synchronization, fidelity, latency, coverage,
  intervention scope, uncertainty, and sim-to-real residuals.
- Twin identity alone establishes neither physical faithfulness nor safe
  policy transfer.

## Open Questions

- How should fidelity renew after hardware, environment, or controller change?
- Which discrepancies must block control rather than merely lower confidence?
- How can independent tests detect simulator-policy co-adaptation?
