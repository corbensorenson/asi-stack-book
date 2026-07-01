# Context Transaction Memory-Store Harness

Command: `python3 scripts/validate_context_transaction_memory_store.py`

Result record:
`experiments/context_transaction_memory_store/results/2026-07-01-local.md`

Latest local result:

```text
Context transaction memory-store harness passed: 3 valid fixture(s), 6 expected-invalid fixture(s).
```

## What It Checks

This book-gate-only harness validates deterministic wrappers around
`context_transaction_record` fixtures and synthetic memory-event records. It
checks the first bounded behavioral rehearsal for the Context Transactions
chapter:

- a committed cell can be read only when visible in the declared snapshot;
- unauthorized mounts must fault instead of silently materializing;
- leaked branch isolation cannot materialize as ordinary context;
- deleted sources and open deletion obligations block materialization unless
  closure is recorded;
- propagated taint without declassification blocks ordinary materialization;
- materialized records must preserve audit and artifact replay boundaries;
- fixture records cannot request chapter-core support-state promotion.

The fixture set covers three accepted scenarios and six expected-invalid
mutation controls: uncommitted reads, deleted-source materialization,
unauthorized mount access, tainted branch leakage, missing replay boundaries,
and support-promotion attempts.

## Boundary

This is fixture discipline over bounded context-transaction and synthetic
memory-event records. It does not implement a deployed memory store, prove VCM
correctness, prove runtime branch isolation, enforce mount permissions outside
the fixture, validate side-channel safety, reproduce VCM-Bench, validate
model-facing context quality, or promote Appendix C or any chapter core claim
above `argument`.
