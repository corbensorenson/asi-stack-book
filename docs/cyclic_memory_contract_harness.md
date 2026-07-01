# Cyclic Memory Contract Harness

Command: `python3 scripts/validate_cyclic_memory_contracts.py`

Result record: `experiments/cyclic_memory_contracts/results/2026-06-30-local.md`

Latest local result:

```text
Cyclic memory contract harness passed: 3 valid fixture(s), 6 expected-invalid fixture(s).
```

## What It Checks

This book-gate-only harness validates synthetic cyclic-memory contract traces
against `schemas/cyclic_memory_contract.schema.json` and additional semantic
guards:

- reused cyclic slots must record residue plus winding/provenance or expose a
  visible alias residual;
- sparse coverage gaps must keep fallback attention available;
- enabled recurrence must carry a positive work budget, exit condition,
  fallback record, and exited state;
- stale reads must fail closed or enter residual escrow before being admitted
  as fresh;
- structural coverage/freshness cannot promote retrieval quality without
  semantic-quality evidence;
- cyclic-memory fixtures cannot promote support state.

## Fixtures

The fixture set in `experiments/cyclic_memory_contracts/fixtures/` contains 3
valid fixtures and 6 expected-invalid fixtures.

Valid fixtures:

- `valid_alias_winding_preserved.json`
- `valid_stale_read_residualized.json`
- `valid_recurrence_exit_fallback.json`

Expected-invalid fixtures:

- `invalid_hidden_alias_without_winding_or_residual.json`
- `invalid_sparse_gap_without_fallback.json`
- `invalid_recurrence_without_exit.json`
- `invalid_stale_read_admitted_without_residual.json`
- `invalid_structural_quality_promotion.json`
- `invalid_support_state_promotion.json`

## Boundary

This is deterministic fixture discipline over structural memory records. It
does not prove retrieval quality, reasoning quality, long-context performance,
memory savings, recurrence quality, KV-cache behavior, sparse-attention
behavior, model behavior, runtime behavior, Circle theorem validity, or Theseus
transfer. It does not promote Appendix C or any chapter core claim above
`argument`.
