# Runtime Adapter Permission Harness

This experiment checks synthetic cross-record consistency for typed jobs,
runtime adapter invocations, and authority-use receipts.

It is intentionally not a deployed tool runner, sandbox, approval service,
secret manager, rollback executor, or security evaluation. The fixtures are
small public-safe records that exercise deterministic gate behavior across
already-defined schemas.

## Command

```bash
python3 scripts/validate_runtime_adapter_permissions.py
```

## Fixtures

- `fixtures/valid_low_impact_local_write.json` checks a low-impact local write
  with permission coverage, an authority handle, an effect lease, a receipt,
  verification refs, audit refs, and rollback handle.
- `fixtures/valid_high_impact_approved_preview.json` checks a high-impact
  preview deployment with scoped approval, approved typed-job state, authority
  receipt, effect receipt, verification refs, audit refs, and rollback handle.
- `fixtures/invalid_missing_permission.json` checks that adapter capabilities
  and required permissions must be present in the typed job.
- `fixtures/invalid_high_impact_without_approval.json` checks that high-impact
  invocations cannot run without approval.
- `fixtures/invalid_expired_approval.json` checks that expired approval markers
  block approval-required invocations.
- `fixtures/invalid_executed_without_effect_receipt.json` checks that executed
  invocations need effect receipt, verification refs, and audit refs.
- `fixtures/invalid_irreversible_without_residual.json` checks that irreversible
  effects need rollback handles or irreversible residual records.
- `fixtures/invalid_confused_deputy_ambient_authority.json` checks that an
  adapter cannot substitute its ambient authority for target-specific authority
  absent from the caller ceiling.
- `fixtures/invalid_revoked_authority_receipt.json` checks that an active
  invocation cannot proceed with an authority receipt marked revoked.

## Environment

- Python 3.
- No network access.
- No external packages beyond the repository's dependency-free schema subset
  validator in `scripts/validate_protocol_examples.py`.

## Non-Claims

- This harness validates synthetic runtime-adapter record semantics only.
- It does not prove deployed adapter behavior, sandbox isolation, approval
  service quality, confused-deputy resistance, revocation propagation,
  secret-handle safety, rollback execution, benchmark performance, or any AI
  safety property.
- It does not promote any live chapter claim above `argument`.
