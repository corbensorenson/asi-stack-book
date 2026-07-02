# Runtime Adapter Effect Replay Probe

Date: 2026-07-02

This record documents a public-safe local runtime-adapter effect replay. It
uses the existing low-impact local-write adapter fixture as a template, creates
a generated temporary file outside the repository, applies one bounded write,
records pre/post/rollback hashes, restores the pre-state, and runs two
no-mutation controls for missing permission and expired approval.

The probe is intentionally small. It turns one runtime-adapter row from
record-shape-only evidence into a temp-file effect and rollback trace while
preserving the same support-state boundary.

## Command

```bash
python3 scripts/run_runtime_adapter_effect_probe.py --write-result
python3 scripts/validate_runtime_adapter_effect_probe.py
```

Result record:
`experiments/runtime_adapter_effect_probe/results/2026-07-02-local.json`

## Recorded Facts

| Field | Value |
|---|---|
| Probe ID | `runtime-adapter-effect-replay-2026-07-02-local` |
| Valid scenario | `valid_low_impact_local_write_effect_replay` |
| Template fixture | `experiments/runtime_adapter_permissions/fixtures/valid_low_impact_local_write.json` |
| Executed effect | public-safe temp-file append outside the repository |
| Rollback | rollback-exact restoration to the pre-state digest |
| Negative control | `invalid_missing_permission_no_mutation` denied before mutation |
| Negative control | `invalid_expired_approval_no_mutation` denied before mutation |
| Repository write | `false` |
| Network use | `false` |
| Support-state effect | `none` |
| Chapter-core support effect | `none` |
| Evidence transition created | `false` |

## Boundary

This Runtime adapter effect replay probe is a local toy effect trace, not a
deployed adapter result. It records gate decisions, digests, rollback-exact
state restoration, and no-mutation controls. It does not store the temporary
file contents, publish local absolute paths, call a network service, inject a
secret, use a real approval service, enforce a production sandbox, propagate
revocation in a deployed service, or exercise a rollback service.

The result does not prove deployed adapter behavior, sandbox isolation,
approval-service behavior, secret-handle safety, revocation propagation,
policy-enforcement correctness, rollback-service behavior, benchmark
performance, runtime security, model behavior, or any AI safety property. It
does not promote the Runtime Adapters chapter core claim.

## Interpretation

The result closes only the smallest honest execution gap: the repository now
has one public-safe local effect replay where a bounded write changes a
temporary state, rollback restores the exact pre-state digest, and the same
runner refuses to mutate state when parent permission is missing or approval is
expired. Stronger claims still require a deployed adapter harness, real
sandbox isolation, approval-service behavior, secret-handle mediation,
revocation propagation, live effect receipts, rollback execution in the target
service, and security review.
