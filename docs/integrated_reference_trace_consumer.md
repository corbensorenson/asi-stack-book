# Integrated reference trace consumer receipt

Status: validated local finite cross-layer consumer; no chapter-core support
transition and no deployment claim.

## What ran

`AsiStackProofs.IntegratedReferenceTrace` defines a partial transition relation
over request, intent, context, plan, route, authorization, job, adapter, effect,
observation, evaluation, evidence, terminal, and quarantine layers. An accepted
handoff joins the exact parent artifact and canonical state, cannot widen active
authority, preserves the authority ceiling, carries residual ownership and a
non-claim boundary, obeys governance gates and logical time, and keeps material
effects separate from acknowledgement, evaluation, evidence, rollback, and
terminal receipts.

The Python consumer independently reimplements those decisions. It is anchored
to the executed repository-change result at
`experiments/governed_repository_change_slice/results/2026-07-10-local.json`
and verifies the exact required source events for nominal, stale-authorization,
revocation, exact-rollback, and failed-rollback scenarios before replaying the
cross-layer abstraction.

The stored result covers:

- eighteen cases: four accepted and fourteen rejected;
- thirty-five accepted events across approved, blocked/quarantined, exact-
  rollback, and failed-rollback/quarantined paths;
- three attempted material effects, two final net effects, and one final
  acknowledged effect across the four accepted cases;
- three final open residuals, four terminal/quarantine receipts, one exact-
  rollback case, and two quarantined cases;
- zero support transitions; and
- fifteen targeted mutations, all rejected.

The checked runtime-schema refinement then consumes the complete tracked
`asi_stack.governed_repository_change_result.v0` artifact rather than another
abstract corpus. It validates the source against its public schema, projects
and custody-wraps the exact fields used by the abstraction, losslessly decodes
all nine projections, and derives three approved completions, three pre-effect
refusals, two exact rollbacks, and one failed-rollback quarantine. Twenty
mutations applied to concrete source fields are all rejected, including missing
effects, proposal receipts, observations, independent evaluators, evidence,
terminal receipts, refusal receipts, rollback gates, restored state, and open
residuals, plus unsafe release and support-transition laundering.

The corpus SHA-256 is
`36444721042e5e56d0f4a5bada88dbcd6600f14755cb151f3d19a62952cdd630`,
the Lean-model SHA-256 is
`632a75e332fe841ed30f3ae6c5764974e8157c5c52e58b5f66f098b00b4b351e`,
and the stored-result SHA-256 is
`f184037d1cc80a5cad3877a21286e9355af5b44f3339aa20082798282a05649a`.
The runtime-schema refinement result SHA-256 is
`731784e5f7f0edc5f6de91b3a2700ff19950238a69f23449cb24b2a3537b6271`.

Run:

```bash
lake -d lean build
python3 scripts/validate_integrated_reference_trace_consumer.py
python3 scripts/validate_integrated_runtime_schema_refinement.py
```

## Adjudication

The results establish one bounded implementation of the Cross-Layer Trace Join
Contract plus checked executable refinement for the exact claimed projection
of one real result schema. They are stronger than the earlier independent invariant tables because
the same transition function owns layer order, parent/state joins, authority,
effects, acknowledgement, evidence, residuals, rollback, and terminal routing.
The support-state effect is exactly `none`.

## Non-claims

- This is a local finite consumer plus a checked adapter for one exact projected
  governed-result schema; it is not a universal live-stack refinement.
- It is not a Lean-verified encoder or decoder and does not establish semantic
  preservation for unprojected payloads, real models, or distributed components.
- It does not establish deployed authority enforcement, rollback completeness,
  evaluator independence, residual completeness, safety, capability,
  reproduction, transfer, SOTA, AGI, or ASI.
