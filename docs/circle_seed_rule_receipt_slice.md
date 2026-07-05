# Circle Seed-Rule Receipt Slice

Date: 2026-07-05

This record imports one public-safe Circle Calculus seed-rule exact-regeneration
receipt slice for the Compact Generative Systems chapter. It is structural
contract evidence only: one finite exact-regeneration fixture, storage-accounting
fields, bounded declared candidate-search fields, theorem IDs, receipt
fingerprints, command-output digests, planner recommendations, and non-claim
boundaries.

Tracked result:
`experiments/circle_seed_rule_receipt_slice/results/2026-07-05-local.json`

Validator:
`python3 scripts/validate_circle_seed_rule_receipt_slice.py`

No-promotion decision:
`evidence_transitions/v1_x_measured/circle_seed_rule_receipt_no_change.json`

## Scope

External project: Circle Calculus at commit `63b0f511`.

Accepted contract ID: `CC-AI-CONTRACT-SEED-RULE-001`

Contract kind: `seed_rule_exact_regeneration`

Receipt schema: `circle_calculus.ai_contract_acceptance_receipt.v0`

Pack fingerprint:
`df673f8a661fc89a26372685986c92f2221aaa617d6738fce5c2a76bd5d0eeae`

Contract fingerprint:
`836594a5f1d448900797e595cb98f0e476c0b9cbd7365fe333cf7ae2622f13c5`

Required theorem IDs:

- `GEN-T0001`
- `GEN-T0040`
- `GEN-T0041`
- `GEN-T0046`
- `GEN-T0048`
- `GEN-T0050`

The digest and receipt commands record `theorem_count=32` for the
contract-ready seed-rule exact-regeneration entry.

Required recommendation IDs:

- `SEED-RULE-USE-EXACT-REGENERATION-RECIPE`
- `SEED-RULE-SELECT-BOUNDED-SHORTER-CANDIDATE`

## Observed Fixture Facts

The accepted fixture records:

- `artifact_id="finite_circle"`
- `fixture_n=128`
- `exact_regeneration=true`
- `generator_length=383`
- `explicit_length=454`
- `storage_saving=71`
- `storage_saving_positive=true`
- `generator_shorter=true`
- `generator_shorter_iff_positive_saving=true`
- `storage_saving_add_generator_length_eq_explicit_length=true`
- `bounded_search_id="public_seed_rule_finite_circle_search"`
- `bounded_search_candidate_count=3`
- `bounded_search_exact_candidate_count=2`
- `bounded_search_shorter_candidate_count=1`
- `bounded_search_has_best_exact=true`
- `bounded_search_has_best_shorter=true`
- `bounded_search_exact_candidate_count_le_candidate_count=true`
- `bounded_search_best_exact_exists_iff_exact_count_positive=true`
- `bounded_search_best_exact_regenerates=true`
- `bounded_search_best_shorter_generator_shorter=true`

The planner recommendation `SEED-RULE-USE-EXACT-REGENERATION-RECIPE` identifies
one finite seed/rule recipe for exact regeneration of the declared finite-circle
fixture. It cites `GEN-T0040`, `GEN-T0041`, and `GEN-T0043`; the pinned evidence
field is `exact_regeneration=true`.

The planner recommendation `SEED-RULE-SELECT-BOUNDED-SHORTER-CANDIDATE` exposes
bounded declared candidate-search and storage-accounting fields. It cites
`GEN-T0037`, `GEN-T0044`, `GEN-T0045`, `GEN-T0046`, `GEN-T0047`, `GEN-T0048`,
`GEN-T0049`, and `GEN-T0050`; the pinned evidence field is
`generator_shorter=true`, with `storage_saving=71`.

The Circle AI certifier boundary is deliberately narrow: the request passed as
a theorem-linked structural exact-regeneration and storage-accounting
certificate for one finite fixture. Its unsupported fields include model
quality, reasoning ability, context length, and speed or memory scaling.

The targeted Circle seed-rule CLI test command reported `2 passed in 4.52s`.
The targeted contract-ready recommendation test reported `1 passed in 2.80s`.

## Command Output Digests

| Output | SHA-256 | Bytes |
|---|---:|---:|
| Seed-rule certificate JSON | `0f7f9f872d5aada01540380a5e8c18a0d61176b9de01707ee3e80b62fd7c855b` | 21190 |
| Circle AI seed-rule certifier JSON | `1eda082a6f9d87e19e470e2046478f38b32deac8d1655f005a3de0d58add2b64` | 4481 |
| contract-ready digest text | `00023e90230fe8011f1457fcc3076dfac56f1c4a84a6162cd99d4e12a56398e5` | 8074 |
| strict receipt text | `332824b14a1db65ddb4941f1dfbb570c5802e6bf59aa69977dd46aa97fbfe2be` | 1813 |
| Seed-rule CLI pytest output | `2913a9256c7c7676b44688501dcd29a9fc0b0a43324fd130eeecd61cde09a2da` | 98 |
| Seed-rule contract-ready pytest output | `e02723e582d6fd1e9e052b5f1c9ac4683c27236b02a035a5fb640e5b0ba8a4c6` | 98 |

## Non-Claims

- Does not promote any chapter core claim above `argument`.
- Does not create a support-state transition.
- Does not prove useful compression, compression utility, codec correctness,
  semantic utility, useful generation, deployed generator behavior, fallback
  execution, or downstream utility.
- Does not prove optimal search, search quality, model quality, reasoning
  ability, context length, runtime speed, memory scaling, benchmark
  performance, deployment readiness, transfer, safety, or ASI.
- Does not prove that the bounded declared candidate search is globally optimal
  or that the recorded finite-circle generator should replace ordinary literal,
  lossy, repaired, fallback, or learned representations.
- Does not prove deployed proof-contract transport inside The ASI Stack.
- Does not reproduce Theseus, MoECOT, VCM, PlanForge, BBVCA, RankFold,
  NeuralFold, model training, serving benchmarks, hardware-kernel benchmarks,
  or simulation results.
- Does not make the external Circle checkout a vendored public dependency.

## Residuals

The slice surfaces concrete Circle backing for one finite seed/rule
exact-regeneration and storage-accounting fixture, but it remains a local
external-project import. A stronger lane would need a vendored or archived
public contract pack, clean ASI-side Circle replay, ordinary literal, lossy,
broken-generator, fallback, verifier-independence, codec, semantic-utility,
downstream-utility, runtime, memory, and model-quality baselines where relevant,
negative controls, deployed compact-generation traces, fallback traces, and a
separate accepted evidence-transition record before any support-state movement.
