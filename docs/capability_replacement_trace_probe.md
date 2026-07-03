# Capability Replacement Trace Probe

This note records a deterministic local replacement trace for the Capability
Replacement and Rollback chapter.

Command:

```bash
python3 scripts/validate_capability_replacement_trace_probe.py
```

Generated result:

```text
experiments/capability_replacement_trace/results/2026-07-02-local.json
```

The trace uses two valid synthetic replacement transactions, three
expected-invalid controls at the transaction boundary, and four sequence
controls at the identity boundary. The first transaction keeps
`impl://bounded-router-v1-canary` in canary state after preserving field
identity, regression floors, authority bounds, residuals, and rollback dry-run
metadata. The second transaction records a synthetic monitor trigger and
rollback to `impl://bounded-router-v0-stable`.

Expected-invalid transaction controls:

| Control | Rejection reason |
|---|---|
| `replacement-control://authority-widening` | Candidate expands authority outside the field envelope. |
| `replacement-control://failed-regression` | Candidate loses the baseline regression floor. |
| `replacement-control://missing-rollback` | Candidate lacks a passing rollback dry run. |

Identity sequence assertions:

| Assertion | Boundary checked |
|---|---|
| Same field identity across sequence | Canary and rollback stay within `field://bounded-router-capability`. |
| Monitor failure blocks default promotion | A failed monitor routes to rollback instead of default. |
| Rollback restores prior implementation | The rollback receipt points to `impl://bounded-router-v0-stable`. |
| Authority envelope preserved | The canary and rollback records do not expand route permissions. |
| Residual owner preserved | Rollback remains owned by a non-candidate reviewer boundary. |

Expected-invalid identity sequence controls:

| Control | Rejection reason |
|---|---|
| `replacement-sequence-control://field-identity-drift` | A sequence that changes field identity is not identity-preserving replacement. |
| `replacement-sequence-control://monitor-failed-default` | A failed monitor cannot still default the candidate. |
| `replacement-sequence-control://rollback-prior-mismatch` | Rollback must restore the recorded prior artifact. |
| `replacement-sequence-control://missing-residual-owner` | Residual ownership cannot disappear during rollback. |

This is a local fixture and proof bridge, not a deployment. It records no
support-state transition and makes no claim that a replacement succeeded in
production.

Non-claims:

- It does not execute deployed or runtime replacement behavior.
- It does not prove regression-suite quality or monitor quality.
- It does not execute production rollback.
- It does not promote the Capability Replacement chapter core claim.
- It does not create a support-state transition.
