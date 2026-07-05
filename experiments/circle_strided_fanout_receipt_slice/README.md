# Circle Strided Fanout Receipt Slice

This directory records the ASI Stack public-safe import of one local external
Circle Calculus strided candidate-fanout receipt slice.

- Result: `results/2026-07-05-local.json`
- Summary: `docs/circle_strided_fanout_receipt_slice.md`
- Validator: `python3 scripts/validate_circle_strided_fanout_receipt_slice.py`

The fixture is structural evidence only. It records finite stride reach and
duplicate-collapsed candidate-budget accounting for a pinned Circle checkout.
Concrete pinned facts:

- Circle commit `63b0f511`
- Contract `CC-AI-CONTRACT-FANOUT-001`
- Kind `strided_candidate_fanout`
- Contract fingerprint
  `d4c878563747da9c9f1f55cd689f04e2a0a8e31ce9429a138341ec4e27ee3799`
- Theorem IDs `AIT-T0001`, `AIT-T0002`, `AIT-T0003`, `AIT-T0173`
- `theorem_count=4`
- Recommendations `FANOUT-USE-FULL-COVERAGE-STRIDE-CYCLE` and
  `FANOUT-AUDIT-DUPLICATE-COLLAPSED-BUDGET`
- `context_length=12`, `stride=5`, `gcd=1`, `predicted_reach=12`,
  `full_coverage=true`, `candidate_budget=12`,
  `effective_candidate_budget=12`, `duplicate_count=0`
- Targeted Circle CLI output `3 passed in 4.65s`
- Targeted contract-ready output `1 passed in 2.77s`
- No-promotion decision `circle_strided_fanout_receipt_no_change.json`

It does not promote any chapter core claim above `argument`, does not create a
support-state transition, and does not prove search quality, retrieval quality,
routing quality, sparse-attention quality, model quality, context length,
throughput, latency, runtime speed, memory scaling, deployment readiness,
transfer, benchmark performance, safety, or ASI.
