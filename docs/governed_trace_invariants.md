# Four Governed Trace Invariants

Last executed: 2026-07-10

This record derives four cross-stack invariants from the executed event logs in
the governed repository-change slice. The Python result is bound to the exact
vertical-slice result by SHA-256. A separate Lean module expresses the same
finite counts, logical-time rule, and accepted/rejected fixtures.

The model uses finite integer logical time. Events may occupy different control,
effect, and verification lanes. Causal parents may precede a child or share its
logical time when an explicit tie rule exists. For the safety-relevant race,
revocation wins ties against effect.

## Authority monotonicity

Each handoff carries a parent scope, child scope, and requested scope. The child
must be a subset of its parent, and the request must be a subset of the child.
The executed fixture contributes three handoffs: intent to plan, plan to an
independent read-only verifier, and plan to the single-path write adapter. A
mutation that adds `network:write` to the adapter request is rejected.

This proves the set relation only for the normalized fixture trace. It does not
prove that a deployed authorization service represents or enforces the same
scopes.

## Revocation before effect

Every effect attempt carries an effect logical time, revocation time, allowed
flag, and independently observed-effect flag. If revocation time is earlier
than or equal to effect time, both flags must be false. The trace contains one
ordinary pre-revocation effect, one effect concurrent with revocation, and one
attempt under already-stale authority. The concurrent case is blocked with no
observed effect. A mutation that allows and observes the tied effect is
rejected.

This is a finite revocation-wins rule over one process-level trace, not a proof
about distributed clocks, network partitions, schedulers, or deployed effect
sites.

## Evidence-transition integrity

The vertical slice emits nine evidence events, one for each executed scenario.
Because the experiment creates no evidence transition, every event must retain
`argument` before and after and declare `support_state_effect: none`. The model
also defines the stronger branch: if a transition is created, state must
actually change and accepted review, artifact-digest agreement, and independent
effect observation must all be present. A mutation that changes support to
`synthetic-test-backed` without a transition is rejected.

This closes silent promotion in the bounded log. It does not establish general
evidence-pipeline correctness, reviewer quality, or the validity of any future
transition.

## Residual conservation

The hidden-residual and failed-rollback scenarios create two residuals and
independently discover both. Exact rollback discharges one. Failed rollback
leaves one final open residual owned by quarantine. The invariant is:

```text
created = discharged + final_open
2       = 1          + 1
```

A mutation that erases the one final open residual is rejected. The check
therefore distinguishes “not released” from “fully repaired”: quarantine
prevents release but does not discharge the remaining mutation.

This is bounded residual accounting. It cannot prove that every real residual
was discoverable or that a deployed ledger is durable.

## Executable and formal linkage

`scripts/run_governed_trace_invariants.py` regenerates the normalized trace from
`experiments/governed_repository_change_slice/results/2026-07-10-local.json`.
`scripts/validate_governed_trace_invariants.py` re-derives it, checks the source
digest, evaluates the four invariants and four mutation controls, and checks the
Lean/source/manifest linkage. `AsiStackProofs.GovernedRepositoryTrace` proves
the concrete bounded fixtures and combines them in
`governed_repository_trace_four_invariants`.

The support-state effect is `none`. This finite logical-time model over one
executed local fixture workload uses bounded scope sets and residual counts; it
does not prove a distributed clock, scheduler, authorization service, rollback
service, general evidence pipeline, residual completeness, safety, security,
or any chapter-core support-state promotion.
