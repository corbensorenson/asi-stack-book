# Circle MultiCoil Phase Receipt Slice

This directory records one public-safe local external-project import from
Circle Calculus for the CoilRA, MultiCoil RoPE, and Cyclic Mixers chapter.

The tracked result is:

- `results/2026-07-05-local.json`
- strict receipt fingerprint
  `4b562beab64ec863903e4267f50c90049f0d3fa612f6c1bb2f06ad07e821ffd7`

Validator:

- `python3 scripts/validate_circle_multicoil_phase_receipt_slice.py`

Scope:

- external Circle commit `63b0f511`
- contract `CC-AI-CONTRACT-PHASE-FEATURE-001`
- kind `multicoil_phase_feature`
- theorem IDs `AIA-T0001`, `AIA-T0002`, `AIA-T0004`, `AIT-T0004`, and
  `AIT-T0005`
- theorem_count=5
- recommendations `PHASE-USE-JOINT-REPEAT-HORIZON` and
  `PHASE-AUDIT-RELATIVE-SHIFT-INVARIANT`
- deterministic phase fixture: `periods=[5, 7]`, position `37`,
  `phase_tuple=[2, 2]`, shifted position `72`,
  `shifted_phase_tuple=[2, 2]`, and `joint_repeat_horizon=35`
- relative phase fixture: query position `41`, key position `18`,
  relative period `5`, `relative_phase=3`, and
  `shifted_relative_phase=3`; `relative_phase_invariant=true`
- targeted Circle CLI output: `3 passed in 2.99s` and `1 passed in 1.76s`
- no-promotion decision:
  `evidence_transitions/v1_x_measured/circle_multicoil_phase_receipt_no_change.json`

Boundary:

- this is structural phase-feature and relative-phase evidence only
- does not promote any chapter core claim
- does not create a support-state transition
- does not prove MultiCoil, RoPE, attention, retrieval, or model quality
- does not prove context length, runtime speed, memory scaling, hardware
  efficiency, training stability, deployment readiness, transfer, benchmark
  performance, or ASI
- no chapter core claim or support state moves
