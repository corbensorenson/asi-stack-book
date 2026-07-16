# Model-adequacy dossier: SafetyCriticalLifecycle

## Identity and scope

| Field | Value |
|---|---|
| Lean model | `AsiStackProofs.SafetyCriticalLifecycle` |
| Model version | `safety-critical-lifecycle.v1` |
| Trace corpus | `experiments/safety_critical_lifecycle/trace_corpus.json` |
| Corpus SHA-256 | `991bf35d88008e2ff3e356e15a689d38db9a81b700f75fa4a6fff57e4c03a1af` |
| Independent replay | `scripts/validate_safety_critical_lifecycle.py` |
| Consumer trace | `scripts/validate_safety_critical_lifecycle_consumer_trace.py` |
| Consumer result | `experiments/safety_critical_lifecycle/results/2026-07-15-consumer-local.json` |
| Support-state effect | `none` |

The model replaces ten activation-baseline projection targets across
constitutional alignment, corrigibility, value conflict, governance rights,
and recursive self-improvement. It is a shared finite transition model, not a
formalization of moral truth, law, complete human agency, or deployed safety.

## Modeled entities and environment

The model contains a domain, lifecycle phase, Boolean evidence record, high-
impact marker, support-promotion request, current authority, authority ceiling,
and a finite event sequence. Its environment is an abstract event producer that
may record one declared obligation, request an effect or support promotion,
narrow or attempt to widen authority, remove a protected predicate, roll back,
or revoke.

It does not model people, institutions, natural language, world state, model
weights, network services, credentials, physical actuators, legal process,
economic incentives, evaluator competence, or attacker adaptation.

## Trusted computing base and assumptions

- Lean's kernel, the checked model source, and the pinned toolchain are trusted
  for theorem checking.
- The JSON corpus is bound into Lean by its exact SHA-256.
- The Python replay and consumer implementations are separately encoded from
  the Lean transition definitions but still share the declared field vocabulary
  and corpus.
- A recorded Boolean obligation is assumed truthful; the model does not prove
  that notice was material, an evaluator independent, an appeal usable, or a
  rollback effect-complete.
- The trace is sequential. There is no concurrency, partial failure, delayed
  acknowledgement, distributed state, fairness scheduler, or hostile storage.
- Initial protected-predicate truth and authority ceiling are supplied by the
  fixture boundary.

## Transition and trace semantics

`step` is the sole transition authority. Recording an obligation sets its exact
field. Effect commitment is admitted only when the domain predicate and
authority ceiling pass. Support promotion additionally requires an already
committed effect, a promotion request, evidence-transition record, non-claim
boundary, and durable receipt. Authority narrowing cannot increase authority;
actual widening and protected-predicate removal reject. Rollback requires a
recorded rollback path and a committed or promoted phase. Revocation sets
authority to zero.

`run` folds `step` over a finite list. Lean proves readiness of accepted effect
and promotion steps, protected-predicate preservation, non-increasing authority,
authority-ceiling preservation, invariant preservation over accepted traces,
and trace composition.

## Countermodels and mutation coverage

The corpus contains eight accepted and eight rejected traces across all five
domains. Rejections cover missing review, affected party, residual, exit/export,
independent evaluator, protected-predicate preservation, authority monotonicity,
and durable promotion receipt. The independent replay deletes every required
domain obligation in turn and confirms 34 effect-blocking countermodels.

The downstream consumer adds eight rejecting mutations: corpus-digest forgery,
trace-digest forgery, domain substitution, forged acceptance, effect on a
rejected trace, authority excess, support-promotion laundering, and duplicate
receipts.

## Executable refinement boundary

The first Python implementation independently replays the trace transition
semantics and exact final snapshots. The second uses a different set-based state
representation, replays five accepted and five rejected domain traces, and then
acts as a consumer: it commits exactly five bounded fixture effects and emits
five denial residuals. This connects a formal decision surface to an executable
consumer record, but only inside the tracked local fixture boundary.

There is no checked encoder from a deployed runtime event, no real effect
adapter, no production authorization service, no distributed replay, and no
proof that Python execution refines Lean for inputs outside the frozen corpus.

## Liveness, fairness, and recovery

The model proves no liveness or fairness property. It does not guarantee that
review, appeal, correction, rollback, or revocation will eventually occur. It
only constrains an event when supplied. Rollback changes the modeled phase; it
does not restore model, optimizer, cache, credential, external-effect, backup,
or descendant state.

## Consumers

- The Constitutional Alignment chapter consumes the alignment and corrigibility
  targets at their finite transition scope.
- The Moral Uncertainty chapter consumes the value-conflict and governance-
  rights targets at the same scope.
- Recursive Self-Improvement consumes the evaluator, rollback, monitor,
  evidence-transition, authority, and promotion boundaries.
- The effect-gate consumer trace consumes exact accepted/rejected replay results
  and preserves denials as residuals.

## Adequacy adjudication

The model is adequate for the narrow claim that this finite state machine and
its two local executable implementations reject the enumerated missing-field,
authority, protected-predicate, and receipt violations, and that the tracked
consumer emits no effect for the five selected rejected traces. It is not
adequate for any chapter-core claim, normative sufficiency claim, real rights or
corrigibility claim, deployed enforcement claim, empirical safety claim,
reproduction claim, transfer claim, AGI claim, or ASI claim.
In particular, this evidence does not establish a support-state promotion.

The remaining P2 gaps are real-schema encoder/decoder refinement, concurrent
and delayed-effect traces, effect-complete rollback, evaluator and affected-
party semantics, hostile consumer tests, integration-model composition, and
independent reproduction beyond the repository.
