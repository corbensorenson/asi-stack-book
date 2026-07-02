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

The trace uses two valid synthetic replacement transactions and three
expected-invalid controls. The first transaction keeps
`impl://bounded-router-v1-canary` in canary state after preserving field
identity, regression floors, authority bounds, residuals, and rollback dry-run
metadata. The second transaction records a synthetic monitor trigger and
rollback to `impl://bounded-router-v0-stable`.

Expected-invalid controls:

| Control | Rejection reason |
|---|---|
| `replacement-control://authority-widening` | Candidate expands authority outside the field envelope. |
| `replacement-control://failed-regression` | Candidate loses the baseline regression floor. |
| `replacement-control://missing-rollback` | Candidate lacks a passing rollback dry run. |

This is a local fixture and proof bridge, not a deployment. It records no
support-state transition and makes no claim that a replacement succeeded in
production.

Non-claims:

- It does not execute deployed or runtime replacement behavior.
- It does not prove regression-suite quality or monitor quality.
- It does not execute production rollback.
- It does not promote the Capability Replacement chapter core claim.
- It does not create a support-state transition.
