# Circle Sparse-Attention Receipt Slice

Date: 2026-07-05

This record imports one public-safe Circle Calculus sparse-attention coverage
receipt slice for the Coil Attention, Cyclic Memory, and Recurrence Contracts
chapter. It is structural contract evidence only: a finite local-window plus
stride-family fixture, gap witnesses, first-interval repair fields,
dense-local complete-fallback fields, theorem IDs, receipt fingerprints,
command-output digests, planner recommendations, and non-claim boundaries.

Tracked result:
`experiments/circle_sparse_attention_receipt_slice/results/2026-07-05-local.json`

Validator:
`python3 scripts/validate_circle_sparse_attention_receipt_slice.py`

No-promotion decision:
`evidence_transitions/v1_x_measured/circle_sparse_attention_receipt_no_change.json`

## Scope

External project: Circle Calculus at commit `63b0f511`.

Accepted contract ID: `CC-AI-CONTRACT-SPARSE-001`

Contract kind: `sparse_attention_coverage`

Receipt schema: `circle_calculus.ai_contract_acceptance_receipt.v0`

Pack fingerprint:
`df673f8a661fc89a26372685986c92f2221aaa617d6738fce5c2a76bd5d0eeae`

Contract fingerprint:
`c23809cef9b821b1e4f9cabf53fcac724a0757bf3f86594e1d12710fe0cd9ec1`

Required theorem IDs:

- `AIT-T0104`
- `AIT-T0172`

The digest command records `theorem_count=141` for the contract-ready sparse
entry. The Circle AI certifier receipt records `circle_ai_receipt_theorem_count=132`
for the emitted request receipt. This ASI-side slice requires only the two
theorem IDs above for the pinned first-interval repair and dense-local fallback
acceptance boundary.

Required recommendation IDs:

- `SPARSE-LOCAL-FIRST-INTERVAL-REPAIR`
- `SPARSE-DENSE-LOCAL-COMPLETE-FALLBACK`

## Observed Fixture Facts

The accepted fixture records:

- `sequence_length=120`
- `strides=[7, 13]`
- `path_length=3`
- `local_window=4`
- `candidate_budget_per_query=10`
- `full_attention_budget=120`
- `coverage_complete=false`
- `covered_lag_count=10`
- `uncovered_lag_count=109`
- `first_uncovered_lag=5`
- `first_uncovered_interval_start=5`
- `first_uncovered_interval_stop=6`
- `first_uncovered_interval_length=2`
- `first_uncovered_interval_additional_local_slots=2`
- `first_interval_repair_next_uncovered_lag=8`
- `first_interval_repair_still_has_gap=true`
- `complete_repair_window=119`
- `complete_repair_window_additional_local_slots=115`
- `complete_repair_window_covers_context=true`
- `complete_repair_window_uses_dense_threshold=true`
- `complete_repair_window_minimal_for_declared_stride_family=true`
- `complete_repair_window_minimal_witness_lag=119`
- `local_window_complete_threshold_is_exact_local_minimum=true`
- `interval_repair_plan_step_count=6`
- `interval_repair_plan_final_window=119`
- `interval_repair_plan_covers_context=true`
- `interval_repair_plan_strictly_progresses=true`
- `lag_collision_pair_count=0`
- `query_collision_pair_count=0`

The uncovered intervals are `[5, 6]`, `[8, 12]`, `[15, 20]`, `[22, 25]`,
`[27, 38]`, and `[40, 119]`. The repair plan progresses through proposed local
windows `6`, `12`, `20`, `25`, `38`, and `119`.

The planner recommendation `SPARSE-LOCAL-FIRST-INTERVAL-REPAIR` covers only
the first reported gap interval. It proposes local window `6`, adds `2` local
slots, leaves another uncovered lag at `8`, and is not a complete coverage or
performance recommendation.

The planner recommendation `SPARSE-DENSE-LOCAL-COMPLETE-FALLBACK` records the
dense-local correctness fallback for all positive lags. It proposes local
window `119`, adds `115` local slots, cites `AIT-T0023`, `AIT-T0034`,
`AIT-T0172`, `AIT-T0168`, `AIT-T0169`, and `AIT-T0170`, and is not a claim
that dense local attention is efficient or preferable.

The Circle AI certifier boundary is deliberately negative for coverage:
`request_passed=false`, `decision_verdict=failed`, and the summary states that
the declared sparse pattern does not cover all positive lags. The useful import
is the gap and repair/fallback receipt, not a coverage-success claim.

The strict receipt command was accepted with the required fields and
theorem/recommendation IDs. The Circle CLI test command reported
`10 passed in 1.87s`.

## Command Output Digests

| Output | SHA-256 | Bytes |
|---|---:|---:|
| stride-family sparse-attention certificate JSON | `3521b057c86435df7896d636c98d8981e8bd8550c3ec9ac39d782748c72bd4be` | 11664 |
| Circle AI sparse-attention certifier JSON | `8b3d6787cc13c84a9cdcd9d8312f185acdf126bb110f49ae9c1c194c025bd1e7` | 35487 |
| contract-ready digest text | `3022d3631af609f518accbc8998e9f471f1c8b0929fbc754656215359682d210` | 4664 |
| strict receipt JSON | `668b395f8850be6993a6be32ec7b83326e8056bbdb7d2d55599104a176e871a1` | 11385 |
| sparse-attention CLI pytest output | `bccd01af074f2766287e392495d35e1977aaa5cf050e80710d26a61ef606757f` | 99 |

## Non-Claims

- Does not promote any chapter core claim above `argument`.
- Does not create a support-state transition.
- Does not prove sparse-attention coverage success.
- Does not prove deployed sparse-attention behavior, retrieval quality,
  reasoning quality, long-context quality, model quality, speed, memory
  savings, deployment safety, transfer, benchmark performance, or ASI.
- Does not prove deployed proof-contract transport inside The ASI Stack.
- Does not reproduce Theseus, MoECOT, VCM, PlanForge, retrieval benchmarks,
  long-context benchmarks, policy-training, serving benchmarks, sparse-attention
  benchmarks, or simulation results.
- Does not make the external Circle checkout a vendored public dependency.

## Residuals

The slice surfaces concrete Circle backing for one sparse-attention gap and
repair/fallback structural fixture, but it remains a local external-project
import. A stronger lane would need a vendored or archived public contract pack,
clean ASI-side Circle replay, ordinary full-attention and sparse-attention
baselines, retrieval or long-context workloads, negative controls, memory and
runtime measurements, and a separate accepted evidence-transition record before
any support-state movement.
