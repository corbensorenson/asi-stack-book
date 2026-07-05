# Circle Strided Fanout Receipt Slice

Date: 2026-07-05

This record imports one public-safe Circle Calculus strided candidate-fanout
receipt slice for the Coil Attention, Cyclic Memory, and Recurrence Contracts
chapter. It is structural contract evidence only: a deterministic finite
stride-orbit fixture, duplicate-collapsed candidate-budget accounting, theorem
IDs, receipt fingerprints, command-output digests, planner recommendations, and
non-claim boundaries.

Tracked result:
`experiments/circle_strided_fanout_receipt_slice/results/2026-07-05-local.json`

Validator:
`python3 scripts/validate_circle_strided_fanout_receipt_slice.py`

No-promotion decision:
`evidence_transitions/v1_x_measured/circle_strided_fanout_receipt_no_change.json`

## Scope

External project: Circle Calculus at commit `63b0f511`.

Accepted contract ID: `CC-AI-CONTRACT-FANOUT-001`

Contract kind: `strided_candidate_fanout`

Receipt schema: `circle_calculus.ai_contract_acceptance_receipt.v0`

Pack fingerprint:
`df673f8a661fc89a26372685986c92f2221aaa617d6738fce5c2a76bd5d0eeae`

Contract fingerprint:
`d4c878563747da9c9f1f55cd689f04e2a0a8e31ce9429a138341ec4e27ee3799`

Required theorem IDs:

- `AIT-T0001`
- `AIT-T0002`
- `AIT-T0003`
- `AIT-T0173`

The digest and receipt commands record `theorem_count=4` for the
contract-ready strided candidate-fanout entry.

Required recommendation IDs:

- `FANOUT-USE-FULL-COVERAGE-STRIDE-CYCLE`
- `FANOUT-AUDIT-DUPLICATE-COLLAPSED-BUDGET`

## Observed Fixture Facts

The accepted fixture records:

- `context_length=12`
- `stride=5`
- `start_index=0`
- `path_length=12`
- `gcd=1`
- `predicted_reach=12`
- `full_coverage=true`
- `candidate_budget=12`
- `unique_candidate_count=12`
- `effective_candidate_budget=12`
- `duplicate_count=0`
- `candidate_budget_accounting=true`
- `candidate_budget_shortfall=0`
- `effective_budget_matches_unique_candidates=true`
- `effective_budget_reaches_predicted_reach=true`
- `orbit=[0, 5, 10, 3, 8, 1, 6, 11, 4, 9, 2, 7]`
- `candidate_path=[7, 2, 9, 4, 11, 6, 1, 8, 3, 10, 5, 0]`

The planner recommendation `FANOUT-USE-FULL-COVERAGE-STRIDE-CYCLE` identifies
one finite stride cycle that covers the declared candidate context. It cites
`AIT-T0001`, `AIT-T0002`, and `AIT-T0003`; the pinned evidence field is
`full_coverage=true`.

The planner recommendation `FANOUT-AUDIT-DUPLICATE-COLLAPSED-BUDGET` exposes
finite duplicate-collapse accounting for the declared candidate path. It cites
`AIT-T0001`, `AIT-T0002`, and `AIT-T0173`; the pinned evidence field is
`duplicate_count=0`, with `effective_candidate_budget=12`.

The Circle AI certifier boundary is deliberately narrow: the request passed as
a theorem-linked structural fanout certificate for one deterministic finite
stride fixture. Its unsupported fields are model-quality improvement,
search-quality improvement, throughput or latency, and optimal candidate
schedule.

The targeted Circle CLI test command reported `3 passed in 4.65s`. The
targeted contract-ready recommendation test reported `1 passed in 2.77s`.

## Command Output Digests

| Output | SHA-256 | Bytes |
|---|---:|---:|
| Strided fanout certificate JSON | `5c80d5fdcb74cb80702d7881a554b34fcb8a9f79c1425e7047177afc8b7ea7db` | 6554 |
| Circle AI strided-fanout certifier JSON | `3b0f37ab709e889d2c0fe48658c118b6d1a8a6a61680dbbb2b99960a08c634f5` | 14727 |
| contract-ready digest text | `b42efb4930f735568765585283063ee713e940be7cf5ff65da185eaeaff75c5a` | 2283 |
| strict receipt text | `fb0bc15ff5e6be109843aff1e8ea3bca0975c4c17162c6c2553629bd88b76515` | 1519 |
| Strided fanout CLI pytest output | `5e764caa97fd868cd3f2a2ed51ec2be309fe521a22c655d7a1c9aeb4dbd15f43` | 98 |
| Strided fanout contract-ready pytest output | `2f1cb16c1dd9bb60a700a651b751ec6de3233db6bb10901b373ae4748a9f114f` | 98 |

## Non-Claims

- Does not promote any chapter core claim above `argument`.
- Does not create a support-state transition.
- Does not prove search quality, retrieval quality, routing quality,
  sparse-attention quality, reasoning quality, or model quality.
- Does not prove context length, throughput, latency, runtime speed, memory
  scaling, hardware efficiency, deployment readiness, transfer, benchmark
  performance, safety, or ASI.
- Does not prove that the recorded stride schedule is optimal or should replace
  sequential fanout, random fanout, round-robin fanout, local-window attention,
  dense attention, learned routing, retrieval systems, or ordinary baselines.
- Does not prove deployed proof-contract transport inside The ASI Stack.
- Does not reproduce Theseus, MoECOT, VCM, PlanForge, model training, serving
  benchmarks, hardware-kernel benchmarks, or simulation results.
- Does not make the external Circle checkout a vendored public dependency.

## Residuals

The slice surfaces concrete Circle backing for one strided candidate-fanout
structural fixture, but it remains a local external-project import. A stronger
lane would need a vendored or archived public contract pack, clean ASI-side
Circle replay, ordinary sequential, random, round-robin, local-window, dense
attention, retrieval, and learned-routing baselines where relevant, quality,
runtime, memory, hardware, search, retrieval, routing, long-context, and
model-quality workloads, negative controls, deployment/fallback traces, and a
separate accepted evidence-transition record before any support-state movement.
