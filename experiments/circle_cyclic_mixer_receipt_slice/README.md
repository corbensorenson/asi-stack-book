# Circle Cyclic-Mixer Receipt Slice

This directory records one public-safe local external-project import from
Circle Calculus for the CoilRA, MultiCoil RoPE, and Cyclic Mixers chapter.

The tracked result is:

- `results/2026-07-05-local.json`
- strict receipt fingerprint
  `b3e3e0cf420d9e8e79a28a55ef8322f9a214c8d5a957dd8b06e5e5373c684ea5`

Validator:

- `python3 scripts/validate_circle_cyclic_mixer_receipt_slice.py`

Scope:

- external Circle commit `63b0f511`
- contract `CC-AI-CONTRACT-MIXER-001`
- kind `circulant_block_cyclic_mixer`
- theorem IDs `AIT-T0006`, `AIT-T0007`, `AIT-T0008`, `AIT-T0009`,
  `AIRA-T0001`, `AIRA-T0002`, and `AIRA-T0004`
- theorem_count=7
- recommendations `MIXER-AUDIT-CIRCULANT-DENSE-PARITY` and
  `MIXER-AUDIT-BLOCK-CYCLIC-PARAMETER-BUDGET`
- deterministic circulant fixture: period `8`, dense output equals
  circulant output, and `max_abs_dense_delta=0`
- parameter accounting fixture: `dense_parameters=64`,
  `circulant_parameters=8`, `circulant_parameter_ratio=0.125`,
  `dense_adapter_parameters=2048`, `lora_parameters=576`,
  `block_cyclic_parameters=128`, and `block_to_dense_ratio=0.0625`
- targeted Circle CLI output: `3 passed in 2.49s` and `1 passed in 1.47s`
- no-promotion decision:
  `evidence_transitions/v1_x_measured/circle_cyclic_mixer_receipt_no_change.json`

Boundary:

- this is structural parity and parameter-accounting evidence only
- does not promote any chapter core claim
- does not create a support-state transition
- does not prove cyclic-mixer model quality
- does not prove runtime speed, memory scaling, hardware efficiency, training
  stability, deployment readiness, transfer, benchmark performance, or ASI
- no chapter core claim or support state moves
