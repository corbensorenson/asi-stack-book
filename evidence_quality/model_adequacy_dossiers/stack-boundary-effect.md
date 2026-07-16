# Model-adequacy dossier: reachable stack-boundary effects

## Modeled claim

The model owns a finite boundary proposition: an accepted material effect is
reachable only through request, within-ceiling target-owner grant, same-epoch
receipt-bound dispatch, and a live non-revoked authority state; the declared
nominal path can then reach independent observation and exact local rollback.
Over-ceiling authorization, missing-dispatch effect, and post-revocation effect
are rejected.

## Entities and transition semantics

- `BoundaryState` records caller ceiling, active grant, authority epoch,
  revocation status, pending request, dispatch receipt, material and observed
  effect counts, rollback state, and logical time.
- `BoundaryEvent` names request, authorize, dispatch, commit-effect, observe,
  revoke, deny, and rollback events plus authority, time, owner, receipt,
  observation, and rollback declarations.
- `BoundaryEventValid` is the bounded admission predicate.
- `BoundaryStep` is a deterministic partial transition and `BoundaryRun`
  composes accepted events.

## Trusted computing base and assumptions

- Lean's kernel checks `lean/AsiStackProofs/StackBoundaries.lean`.
- The Python consumer is independently implemented, but it is not a formally
  verified refinement of the Lean definitions.
- Recorded owner approval, receipt presence, independent observation,
  revocation epoch, and rollback exactness are trusted input assertions.
- The six authority fixtures are synthetic. The source runtime probe executes
  one contained local temporary-file effect; neither source constitutes a
  deployed authority service.
- Logical time is sequential and atomic. Distributed clocks, network
  partitions, concurrency, retries, and scheduler behavior are excluded.

## Proved or checked properties

- An accepted authorization respects the caller authority ceiling.
- An accepted material effect requires a live grant and prior dispatch receipt.
- The declared six-event nominal run reaches zero remaining effects after one
  independently observed effect and exact rollback.
- Explicit Lean countermodels reject over-ceiling authorization, effect without
  a dispatch receipt, and post-revocation effect.
- The consumer classifies six authority fixtures, accepts three runtime paths
  totaling ten events, binds one material effect to one observation and one
  exact rollback, and checks two no-mutation denials plus five revocation entries.
- A generated suite checks all eighteen declared layer-contract admission routes
  against the independent priority-ordered route implementation.
- Twelve semantic mutations are all rejected.

## Countermodels and mutation coverage

The negative suite changes zero-valued requests, widens grant scope, removes
owner approval, removes authorization or dispatch receipts, changes the
authority epoch, removes effect custody, removes independent observation,
removes observation or rollback receipts, falsifies exact rollback, and inserts
revocation before dispatch/effect. These cases target distinct admission guards
rather than merely perturbing formatting.

## Consumer and refinement boundary

`scripts/validate_stack_boundary_effect_consumer.py` consumes the tracked
authority fixtures and checks digest-bound source artifacts from the runtime
effect and revocation probes. Its state machine is separately implemented and
its stored result is schema-validated. This is useful cross-implementation
agreement over a finite corpus; it does not prove semantic equivalence between
Python and Lean or refine a live authorization API.

The eighteen previous theorem-per-record layer-contract normalizations have
been retired from the live Lean source. Their frozen identities and replacement
lineage remain in `proofs/proof_rationalization_registry.json`; the generated
eighteen-case route suite preserves their finite admission behavior, while the
repository traceability audit retains the narrower source/mapping and
no-promotion function it actually exercises.

## Adequacy adjudication

Adequate for: the finite transition semantics above, the three explicit negative
families, one source-anchored contained effect/observation/rollback path, two
denial paths, tracked revocation evidence, and twelve targeted mutations.

Not adequate for: authentic grants or receipts; complete effect discovery; a
real target owner; multidimensional delegation; compromised authorities;
distributed clocks, partitions, or retries; hidden or irreversible rollback;
security; natural-workload usefulness; reproduction; transfer; SOTA; AGI; or
ASI.

The result does not establish the chapter's core architectural thesis. Its
support-state effect is exactly `none`. The next empirical increment is a live
target-owner authorization adapter with cryptographically bound receipts,
effect discovery across multiple effect classes, adversarial revocation races,
and independent reproduction—not additional finite theorem count.
