# Authority Revocation Propagation Trace

Command:

```bash
python3 scripts/validate_authority_revocation_trace.py
```

Result:

```text
experiments/authority_revocation_trace/results/2026-07-03-local.json
```

This trace is a bounded repository artifact for System Boundaries and Authority.
It reads already committed authority, runtime-adapter, security-kernel, SCIF,
and reference-trace artifacts to check that revoked, expired, or missing
authority remains visible as a denial, no-mutation, or blocked-path record
across layers.

It checks five trace entries:

| Entry | Boundary checked |
|---|---|
| `authority-transition-denial` | Over-ceiling authority is denied with a denial reason, no effect receipt, audit refs, and no support-state promotion. |
| `runtime-adapter-revoked-receipt` | A runtime adapter fixture with a revoked authority receipt is expected-invalid and cannot be treated as deployed revocation propagation. |
| `runtime-adapter-expired-no-mutation` | The local effect-replay probe rejects an expired approval before mutation and records unchanged state hashes. |
| `security-scif-inactive-approval-block` | The SCIF commit probe blocks a commit when approval is inactive or the destination is unapproved. |
| `reference-trace-blocked-authority` | The reference trace preserves a blocked authority stop condition and promotion blocker. |

Lean bridge:

- `authority_revocation_trace_surface_bridge` in
  `lean/AsiStackProofs/Authority.lean` mirrors the finite trace summary:
  authority denial is visible, revoked receipts are blocked, expired approvals
  preserve no-mutation evidence, SCIF inactive approval blocks commit,
  reference-trace authority blockers are preserved, support effect remains
  none, and deployed revocation propagation is not claimed.

Non-claims:

- This does not prove deployed authorization enforcement.
- This does not prove deployed revocation propagation.
- This does not prove tool-wrapper security, approval-service quality,
  sandbox isolation, or secret-handle safety.
- This does not prove model quality, benchmark performance, safety, or ASI.
- This does not create an evidence transition or support-state transition.
- This does not promote any chapter core claim.
