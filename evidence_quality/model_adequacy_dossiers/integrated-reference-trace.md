# Model-adequacy dossier: integrated reference trace

## Modeled claim

The model owns only the finite cross-layer join proposition: a typed trace can
move through the book's reference layers while preserving exact artifact and
state parentage, non-increasing authority, effect/acknowledgement separation,
evidence custody, residual conservation, rollback disposition, terminal
receipts, and explicit non-claims.

## Entities and transition semantics

- `Layer` names request, intent, context, plan, route, authorization, job,
  adapter, effect, observation, evaluation, evidence, terminal, and quarantine
  boundaries.
- `TraceState` stores the current layer, authority ceiling and active authority,
  canonical state and last artifact, material and acknowledged effect counts,
  open residuals, support level, observation/evaluation completion, terminal
  receipt, rollback state, logical time, and optional revocation time.
- `TraceEvent` carries exact from/to layers, time, parent/output artifacts,
  before/after state, requested authority, effect/acknowledgement/rollback and
  residual deltas, support lineage, governance gates, independent observation
  and evaluation declarations, evidence review, residual owner, rollback,
  receipt, and non-claim fields.
- `Step` is a deterministic partial transition. `Run` composes accepted steps.

## Trusted computing base and assumptions

- Lean's kernel checks
  `lean/AsiStackProofs/IntegratedReferenceTrace.lean`.
- Artifact and state numbers are abstract identities; collision resistance and
  truthful correspondence to runtime objects are assumed, not proved.
- Boolean declarations for independent observation/evaluation, gate presence,
  exact rollback, residual ownership, and receipts are assumed to reflect the
  world facts they name.
- The cross-layer run is sequential and atomic. A second effect-ledger
  transition system models independently identified effects, shared authority
  epochs, equal-logical-time interleavings, revocation-wins ties, observation,
  and mutually exclusive acknowledgement, compensation, or residualization.
  Distributed clocks, network partitions, scheduler behavior, and non-
  linearizable services remain excluded.
- The Python consumer shares the conceptual specification and corpus but not
  the Lean implementation. The later runtime-schema adapter consumes the
  executed governed-result artifact directly, validates it against its public
  JSON Schema, and losslessly round-trips the exact concrete fields used by the
  abstraction. This still does not formally prove that Python refinement code
  corresponds to the Lean transition relation.

## Proved or checked properties

- Every accepted step narrows or preserves active authority and preserves the
  authority ceiling.
- Every accepted step joins its parent artifact and canonical state and emits
  the next exact artifact/state identities.
- Arbitrary accepted finite traces cannot widen active authority.
- Trace execution composes over list concatenation.
- One twelve-event complete trace reaches the exact terminal state.
- Parent/state forks, authority widening, a missing gate, effect at a revocation
  tie, unacknowledged terminal effect, and residual erasure are rejected in
  Lean.
- The independent consumer accepts four outcome paths, rejects fourteen invalid
  paths, and rejects fifteen targeted guard mutations.
- The concrete runtime-schema adapter validates and round-trips all nine source
  scenarios, derives three approved completions, three pre-effect refusals, two
  exact rollbacks, and one failed-rollback quarantine, and rejects twenty
  mutations applied to source-schema fields.
- The logical-time effect ledger rejects an attempt at the same time as an
  already-applied revocation, requires observation to name a prior attempted
  effect, makes accepted acknowledgement close the exact effect, and executes
  one two-effect same-time interleaving whose effects end separately in
  acknowledgement and residual custody.
- The independent effect-ledger consumer checks sixteen traces, including an
  exact idempotent retry, partial-failure compensation and residual custody,
  revocation-tie and stale-epoch rejection, mutually exclusive terminal lanes,
  and twelve additional semantic mutations.

## Countermodels and mutation coverage

The executable packet rejects parent and canonical-state forks, authority
widening, residual erasure, missing residual ownership, missing non-claims,
missing governance gates, effect at revocation time, over-acknowledgement,
self-evaluation, support promotion without a transition and accepted review,
terminal release with unacknowledged effects, incomplete rollback, and
quarantine without a receipt. Mutations additionally delete output artifacts,
rollback readiness, independent observation/evaluation, exact residual closure,
and terminal receipts from the accepted path.

## Executable refinement boundary

`scripts/validate_integrated_reference_trace_consumer.py` is the downstream
finite-event consumer. The next adapter,
`scripts/validate_integrated_runtime_schema_refinement.py`, reads the actual
`asi_stack.governed_repository_change_result.v0` result, validates the entire
source object against its tracked schema, projects the exact fields on which
the trace classification depends, wraps that projection with a custody digest,
decodes it, requires structural equality with the original projection, and
then checks completion, refusal, rollback, quarantine, effect, observation,
evidence, residual, receipt, and no-promotion obligations. Twenty mutations
change the concrete source fields rather than a second hand-authored abstract
corpus, and all are rejected.

This closes the first real-schema executable-refinement placeholder for the
governed repository-change slice. It is not a universal encoder/decoder for all
stack services, and it is not a Lean-verified compiler or a proof that the
runtime implements the Lean relation. The abstract identities used inside the
Lean model still do not carry real cryptographic object semantics.

## Adequacy adjudication

Adequate for: the declared finite transition model, one exact joined terminal
trace, three contained alternative outcome paths, targeted countermodels,
local cross-implementation agreement, and checked executable refinement of the
exact claimed fields in one real governed-result schema across all nine stored
source scenarios.

Not adequate for: semantic equivalence of unprojected or real layer payloads;
real service identity; a Lean-verified encoder/compiler; cryptographic artifact
binding beyond the projection custody digest; non-linearizable distributed
concurrency, clock skew, partitions, retries, or scheduler fairness;
effect-complete rollback outside the fixture; evaluator independence; residual
completeness; natural task quality; deployment; reproduction; transfer; safety;
SOTA; AGI; or ASI.

The model does not establish the integrated architecture chapter core. It is a
useful but too narrow formal and executable slice with support-state effect
`none`. The next adequacy increment is distributed/partitioned retry semantics,
additional live-schema adapters, multi-service replay, and
externally reproducible transfer—not more fixture theorem count.
