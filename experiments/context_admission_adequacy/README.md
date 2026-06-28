# Context Admission/Adequacy Harness

This directory contains synthetic fixtures for
`scripts/validate_context_admission_adequacy.py`.

The harness checks cross-record consistency across existing public schemas:

- `context_abi_record`
- `context_packet`
- `semantic_page_certificate`
- `context_transaction_record`
- `context_adequacy_record`

It tests only deterministic fixture semantics:

- admitted context can still be inadequate for a target claim;
- conflict and contradiction records block evidence-ready classification;
- stale or revoked certificates cannot support adequate packets;
- open deletion obligations block materialization and promotion;
- weak verification modes cannot support empirical, benchmark, deployment, or
  runtime claims;
- high-risk inadequate context requires escalation.

It does not implement a VCM resolver, context compiler, transactional memory
store, model-facing context run, contradiction-rate benchmark, distractor
resistance experiment, or support-state promotion.
