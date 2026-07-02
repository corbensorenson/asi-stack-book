# Runtime Adapter Adversarial Boundary Probe

Date: 2026-07-02

This record documents a deterministic synthetic runtime-adapter adversarial
boundary fixture. It adds breadth around the action boundary where typed work
would touch tools, credentials, sandboxes, approvals, receipts, and rollback
records.

The probe is intentionally finite. It checks boundary-review records, not a
deployed adapter. Its role is to make the Runtime Adapters chapter less
dependent on prose by covering the adversarial cases the chapter says must be
blocked.

## Command

```bash
python3 scripts/validate_runtime_adapter_adversarial_boundary_probe.py --write-result
python3 scripts/validate_runtime_adapter_adversarial_boundary_probe.py
```

Result record:
`experiments/runtime_adapter_adversarial_boundary/results/2026-07-02-local.json`

## Recorded Facts

| Field | Value |
|---|---|
| Result ID | `2026-07-02-runtime-adapter-adversarial-boundary-probe` |
| Valid scenarios | two valid synthetic adapter boundary reviews |
| Expected-invalid controls | twelve expected-invalid controls |
| Valid dispatch | `valid_scoped_low_impact_dispatch_review` |
| Valid dispatch | `valid_high_impact_scoped_approval_review` |
| Negative control | confused-deputy parent mismatch |
| Negative control | parent authority ceiling overrun |
| Negative control | lease authority ceiling overrun |
| Negative control | approval scope mismatch |
| Negative control | expired approval |
| Negative control | sandbox escape path |
| Negative control | secret materialized into model-visible context |
| Negative control | missing rollback handle |
| Negative control | missing effect receipt |
| Negative control | missing audit refs |
| Negative control | support-state promotion |
| Negative control | missing non-claim boundary |
| Support-state effect | `none` |
| Chapter-core support effect | `none` |
| Evidence transition created | `false` |
| Boundary phrase | no support-state transition |

## Boundary

This Runtime adapter adversarial boundary probe is a synthetic record gate. It
does not execute a deployed adapter, prove sandbox isolation, prove
approval-service behavior, prove secret-handle safety, prove
policy-enforcement correctness, prove rollback-service behavior, prove
revocation propagation, or create a support-state transition.

It checks only that the local review predicate rejects the listed adversarial
record shapes and admits two complete scoped records. The Runtime Adapters
chapter core claim remains at `argument` support.

## Interpretation

The result expands the adapter chapter's adversarial surface around the most
safety-critical transition in the stack: external effects. It now has explicit
checks for caller parentage, authority ceilings, scoped approval, approval
expiry, sandbox boundaries, secret non-materialization, rollback handles,
effect receipts, audit refs, support-state non-promotion, and non-claim
boundaries.

The remaining evidence gap is still runtime evidence: a deployed adapter
harness, real sandbox isolation, approval-service integration, secret-handle
mediation, live effect receipts, rollback execution in target services,
deployed revocation propagation, policy-enforcement checks, and security
review.
