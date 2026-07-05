# Circle Sparse-Attention Receipt Slice

This directory records one public-safe local external-project import from
Circle Calculus for the Coil Attention, Cyclic Memory, and Recurrence Contracts
chapter.

The tracked result is:

- `results/2026-07-05-local.json`
- strict receipt fingerprint
  `c23809cef9b821b1e4f9cabf53fcac724a0757bf3f86594e1d12710fe0cd9ec1`

Validator:

- `python3 scripts/validate_circle_sparse_attention_receipt_slice.py`

Scope:

- external Circle commit `63b0f511`
- contract `CC-AI-CONTRACT-SPARSE-001`
- kind `sparse_attention_coverage`
- theorem IDs `AIT-T0104` and `AIT-T0172`
- theorem_count=141
- recommendations `SPARSE-LOCAL-FIRST-INTERVAL-REPAIR` and
  `SPARSE-DENSE-LOCAL-COMPLETE-FALLBACK`
- local-window plus stride-family fixture: sequence length `120`, strides
  `[7, 13]`, path length `3`, local window `4`
- accepted strict receipt for first missed interval and dense-local complete
  fallback fields
- `first_uncovered_lag=5`
- `uncovered_lag_count=109`
- `covered_lag_count=10`
- `complete_repair_window=119`
- `complete_repair_window_additional_local_slots=115`
- `complete_repair_window_minimal_for_declared_stride_family=true`
- `complete_repair_window_minimal_witness_lag=119`
- `interval_repair_plan_step_count=6`
- `lag_collision_pair_count=0`
- `query_collision_pair_count=0`
- Circle CLI output: `10 passed in 1.87s`
- no-promotion decision:
  `evidence_transitions/v1_x_measured/circle_sparse_attention_receipt_no_change.json`

Boundary:

- this is structural sparse-coverage and repair/fallback evidence only
- the fixture records `coverage_complete=false`
- does not promote any chapter core claim
- does not create a support-state transition
- does not prove sparse-attention coverage success
- does not prove deployed sparse-attention behavior
- does not prove retrieval quality, model quality, memory savings, or
  deployment safety
- no retrieval-quality, long-context, model-quality, speed, memory-savings,
  deployed attention, transfer, deployment-safety, or ASI claim is promoted
- no chapter core claim or support state moves
