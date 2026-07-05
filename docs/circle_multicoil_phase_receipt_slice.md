# Circle MultiCoil Phase Receipt Slice

Date: 2026-07-05

This record imports one public-safe Circle Calculus MultiCoil phase-feature
receipt slice for the CoilRA, MultiCoil RoPE, and Cyclic Mixers chapter. It is
structural contract evidence only: a deterministic finite phase-bank fixture,
relative-phase shift-invariance fixture, theorem IDs, receipt fingerprints,
command-output digests, planner recommendations, and non-claim boundaries.

Tracked result:
`experiments/circle_multicoil_phase_receipt_slice/results/2026-07-05-local.json`

Validator:
`python3 scripts/validate_circle_multicoil_phase_receipt_slice.py`

No-promotion decision:
`evidence_transitions/v1_x_measured/circle_multicoil_phase_receipt_no_change.json`

## Scope

External project: Circle Calculus at commit `63b0f511`.

Accepted contract ID: `CC-AI-CONTRACT-PHASE-FEATURE-001`

Contract kind: `multicoil_phase_feature`

Receipt schema: `circle_calculus.ai_contract_acceptance_receipt.v0`

Pack fingerprint:
`df673f8a661fc89a26372685986c92f2221aaa617d6738fce5c2a76bd5d0eeae`

Contract fingerprint:
`4b562beab64ec863903e4267f50c90049f0d3fa612f6c1bb2f06ad07e821ffd7`

Required theorem IDs:

- `AIA-T0001`
- `AIA-T0002`
- `AIA-T0004`
- `AIT-T0004`
- `AIT-T0005`

The digest and receipt commands record `theorem_count=5` for the
contract-ready MultiCoil phase-feature entry.

Required recommendation IDs:

- `PHASE-USE-JOINT-REPEAT-HORIZON`
- `PHASE-AUDIT-RELATIVE-SHIFT-INVARIANT`

## Observed Fixture Facts

The accepted fixture records:

- `periods=[5, 7]`
- `position=37`
- `phase_tuple=[2, 2]`
- `shifted_position=72`
- `shifted_phase_tuple=[2, 2]`
- `joint_repeat_horizon=35`
- `query_position=41`
- `key_position=18`
- `relative_period=5`
- `relative_phase=3`
- `shifted_relative_phase=3`
- `relative_phase_invariant=true`

The planner recommendation `PHASE-USE-JOINT-REPEAT-HORIZON` exposes finite
phase tags and the joint repeat horizon for the declared period bank. It cites
`AIA-T0001`, `AIA-T0002`, and `AIA-T0004`; the pinned evidence field is
`joint_repeat_horizon=35`.

The planner recommendation `PHASE-AUDIT-RELATIVE-SHIFT-INVARIANT` audits one
finite query/key relative-phase fixture under a common shift. It cites
`AIT-T0004` and `AIT-T0005`; the pinned evidence field is `relative_phase=3`,
with `shifted_relative_phase=3`.

The Circle AI certifier boundary is deliberately narrow: the request passed as
a theorem-linked structural phase-feature certificate for one deterministic
phase-bank and relative-phase fixture. Its unsupported fields are feature
usefulness in a trained model, attention-quality improvement, training
stability, and all-real-phase RoPE separation.

The targeted Circle CLI test command reported `3 passed in 2.99s`. The
targeted contract-ready recommendation test reported `1 passed in 1.76s`.

## Command Output Digests

| Output | SHA-256 | Bytes |
|---|---:|---:|
| MultiCoil phase-feature certificate JSON | `c09ee4c02492c6909dd0512a75016023ee4ff4aeb7151d61ab5d86f6ca1f60b9` | 6055 |
| Circle AI MultiCoil certifier JSON | `72e5d297069f63596aab41ded949aa85b8321f6e49a0903595449dc4a344e1d8` | 14026 |
| contract-ready digest text | `e4e80f9c65bd8b38820b71c5765164794b24551b05e7be9fe093ece632ba1fb9` | 1562 |
| strict receipt text | `e6a4eb2722b409830ad45a30848b88d1af534fbaa6ac328495316ba47a94ab4d` | 1378 |
| MultiCoil phase CLI pytest output | `74fd32ab05d781b43e82019531ebaeb3be97b7097d9592ad5920069166b639b8` | 98 |
| MultiCoil phase contract-ready pytest output | `6262a8e2e6f2ad2d2de112173e9d549955762f82a7ab80d9fb2f247e0426b472` | 98 |

## Non-Claims

- Does not promote any chapter core claim above `argument`.
- Does not create a support-state transition.
- Does not prove MultiCoil, RoPE, attention, retrieval, or model quality.
- Does not prove context length, runtime speed, memory scaling, hardware
  efficiency, training stability, deployment readiness, transfer, benchmark
  performance, or ASI.
- Does not prove that a MultiCoil phase feature should replace ordinary
  position buckets, learned position embeddings, RoPE, dense attention,
  recurrent, or state-space baselines.
- Does not prove deployed proof-contract transport inside The ASI Stack.
- Does not reproduce Theseus, MoECOT, VCM, PlanForge, model training, serving
  benchmarks, hardware-kernel benchmarks, or simulation results.
- Does not make the external Circle checkout a vendored public dependency.

## Residuals

The slice surfaces concrete Circle backing for one MultiCoil phase-feature
structural fixture, but it remains a local external-project import. A stronger
lane would need a vendored or archived public contract pack, clean ASI-side
Circle replay, ordinary position-bucket, learned-position, RoPE, dense
attention, recurrent, and state-space baselines where relevant, quality,
runtime, memory, hardware, training-stability, long-context, retrieval, and
attention-quality workloads, negative controls, deployment/fallback traces, and
a separate accepted evidence-transition record before any support-state
movement.
