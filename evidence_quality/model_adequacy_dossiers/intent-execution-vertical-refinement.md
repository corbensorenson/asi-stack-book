# Model-adequacy dossier: Intent-to-Execution vertical refinement

## Modeled claim

The model owns a finite consumer-relative conformance proposition: accepted
lowerings preserve one root contract, exact parent artifact, non-widening
authority, and control/data separation; a material effect is reachable only
after approval and dispatch custody; delivery is reachable only after observed
effect, artifact binding, and independent verification; failures terminate in
block, rollback, residual, or quarantine rather than silent success.

## Entities and transition semantics

- `VerticalLayer` names intent, command, plan, job, authorization, dispatch,
  attempted and observed effect, artifact, verification, delivery, block,
  residual, rollback, and quarantine boundaries.
- `VerticalState` stores root contract, exact current artifact, ceiling and
  active authority, approval and dispatch custody, attempted and observed
  effects, artifact and verification state, delivery, residuals, stop state,
  and logical time.
- `VerticalEvent` carries exact from/to layers, contract and artifact joins,
  requested authority, approval and dispatch receipts, hidden-override state,
  effect and observation deltas, observer and verifier declarations, delivery,
  block, residual, rollback, and time fields. `PayloadWellTyped` makes those
  fields exclusive to their event kinds, so a lowering event cannot smuggle an
  effect, observation, delivery, residual, or rollback update.
- `VerticalStep` is a deterministic partial transition; `VerticalRun` composes
  finite accepted events.

## Trusted computing base and assumptions

- Lean's kernel checks `lean/AsiStackProofs/IntentExecutionRefinement.lean`.
- The independently written Python consumer validates the full source result
  against `schemas/governed_repository_change_result.schema.json`; it is not a
  formally verified refinement of the Lean implementation.
- Contract, artifact, authority, receipt, observation, verifier, decision,
  rollback, and residual fields are assumed truthful within the source result.
- The fixed local repository task is sequential and atomic. Natural-language
  interpretation, distributed clocks, concurrency, partitions, retries, and
  irreversible effects are excluded.

## Proved or checked properties

- All 37 expected declarations compile with no `sorry`, `admit`, or `axiom`.
- Every accepted step has a kind-valid payload, preserves the root contract and
  authority ceiling, joins the exact parent artifact, advances logical time,
  preserves or narrows active authority, and rejects hidden overrides.
- Every accepted run preserves the full vertical invariant, contract and
  authority custody, and nondecreasing logical time.
- Accepted dispatch requires approval custody and a dispatch receipt.
- Accepted effect requires a prior dispatch receipt.
- Accepted delivery requires complete observation, independent verification,
  a delivery receipt, and full modeled approval, dispatch, artifact, and
  verification custody.
- Blocking stops without changing effect accounting; residualization increases
  residuals without claiming an effect; quarantine is stopped and residualized.
- One ten-event Lean trace reaches the exact delivered state.
- Eighteen Lean countermodels reject missing approval, authority widening,
  hidden override, effect without dispatch, delivery without verification,
  substituted root or parent identity, stale time, five kinds of smuggled
  payload, premature observation or artifact binding, self-verification,
  inexact rollback, and quarantine without a residual.
- The independent consumer adjudicates nine executed scenarios and 89 events:
  three releases, three pre-effect refusals, two exact-rollback refusals, and
  one failed-rollback quarantine.
- Thirty concrete source mutations are all rejected.

## Countermodels and mutation coverage

Mutations remove or reorder the intent, authority, plan, context, route,
effect, proposal, observation, evidence, and terminal events; introduce an
unauthorized changed path or mismatched artifact digest; collapse evaluator
independence or safety checks; bypass prompt-injection quarantine, stale or
revoked authority, correlated-verifier rejection, exact rollback, residual
custody, failed-rollback quarantine, and cheaper-route rejection; or launder
support, expected disposition, correctness, unsafe release, or non-claims.

## Executable refinement boundary

The consumer reads the complete executed governed repository-change result,
not a second abstract trace corpus. It validates the source schema, derives
the vertical obligations from exact source fields, binds the source, schema,
prior probe, and Lean model digests, and mutates concrete source fields. This
is a checked finite refinement for one versioned result schema. It does not
prove semantic preservation for arbitrary intent text, compiler IR, jobs,
adapters, artifacts, or services.

## Adequacy adjudication

Adequate for: the declared finite transition semantics; kind-exclusive payloads;
one-step and arbitrary-run custody, authority, time, effect-accounting,
delivery, stop, and residual invariants; eighteen closed Lean countermodels;
three contained release paths; three pre-effect refusals; two exact rollbacks;
one failed-rollback quarantine; fixed-path artifact checks; independent
observation/evaluator declarations; residual custody; and thirty targeted
source mutations.

Not adequate for: human-intent correctness; general semantic equivalence;
authentic authority or receipts; verifier correctness; complete effects;
natural workloads; distributed behavior; deployment; reproduction; transfer;
safety; SOTA; AGI; or ASI.

The result does not establish the chapter core. Its support-state effect is exactly `none`.
The next adequacy increment is a natural, ambiguous intent
corpus with competing contract lowerings, independently implemented parsers
and evaluators, live one-shot authority binding, and external reproduction—not
additional theorem-per-fixture declarations.
