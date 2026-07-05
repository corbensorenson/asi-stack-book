# Circle Seed-Rule Receipt Slice

This directory records the ASI Stack public-safe import of one local external
Circle Calculus seed-rule exact-regeneration receipt slice.

- Result: `results/2026-07-05-local.json`
- Summary: `docs/circle_seed_rule_receipt_slice.md`
- Validator: `python3 scripts/validate_circle_seed_rule_receipt_slice.py`

The fixture is structural evidence only. It records finite exact regeneration,
storage-accounting fields, bounded declared candidate-search fields, theorem
IDs, planner recommendations, command-output digests, and no-promotion
boundaries for a pinned Circle checkout.

Concrete pinned facts:

- Circle commit `63b0f511`
- Contract `CC-AI-CONTRACT-SEED-RULE-001`
- Kind `seed_rule_exact_regeneration`
- Contract fingerprint
  `836594a5f1d448900797e595cb98f0e476c0b9cbd7365fe333cf7ae2622f13c5`
- Theorem IDs `GEN-T0001`, `GEN-T0040`, `GEN-T0041`, `GEN-T0046`,
  `GEN-T0048`, `GEN-T0050`
- `theorem_count=32`
- Recommendations `SEED-RULE-USE-EXACT-REGENERATION-RECIPE` and
  `SEED-RULE-SELECT-BOUNDED-SHORTER-CANDIDATE`
- `fixture_n=128`, `exact_regeneration=true`, `generator_length=383`,
  `explicit_length=454`, `storage_saving=71`,
  `bounded_search_candidate_count=3`,
  `bounded_search_exact_candidate_count=2`, and
  `bounded_search_best_shorter_generator_shorter=true`
- Targeted Circle seed-rule CLI output `2 passed in 4.52s`
- Targeted contract-ready output `1 passed in 2.80s`
- No-promotion decision `circle_seed_rule_receipt_no_change.json`

It does not promote any chapter core claim above `argument`, does not create a
support-state transition, and does not prove useful compression, codec
correctness, semantic utility, useful generation, deployed generator behavior,
fallback execution, downstream utility, optimal search, model quality, context
length, runtime speed, memory scaling, deployment readiness, transfer,
benchmark performance, safety, or ASI.
