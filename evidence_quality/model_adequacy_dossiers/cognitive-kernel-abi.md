# Model-adequacy dossier: Cognitive Kernel ABI

## Modeled claim

The finite model owns only the record-level proposition that a substrate-neutral
control plane can route proposal, commit, migration, and revocation events
across named kernel families while preserving authority and declared checkpoint
identity, separating proposals from effects, rejecting incompatible or revoked
routes, and retaining required custody fields.

## Entities and state

- `ABIState`: active kernel and family, fixed authority ceiling, checkpoint
  schema and digest, pending target, committed-effect count, and one most-recent
  revoked kernel.
- `ABIEvent`: event kind; actor, target, and fallback identities and families;
  requested authority; checkpoint identity; proposal/effect flags; migration,
  fallback, evaluator, assistance, lifecycle-cost, evidence, residual, receipt,
  and rollback fields.
- `Step` and `Run`: deterministic partial transition and finite trace runner.

## Trusted computing base and assumptions

- Lean's kernel checks the declarations in
  `lean/AsiStackProofs/ReplaceableCognitiveSubstrates.lean`.
- Event fields are assumed to be faithfully serialized facts. Boolean
  `evaluatorIndependent`, `rollbackReady`, and similar fields are declarations,
  not proofs of the world facts they name.
- Kernel IDs, family names, checkpoint schemas, and checkpoint digests are
  assumed to have an external registry and collision-resistant meaning.
- The transition is sequential and atomic; logical concurrency and distributed
  partial failure are excluded.
- The Python consumer is an independent set of transition checks but shares the
  corpus and conceptual specification with the Lean model.

## Proved or checked properties

- Accepted steps and accepted arbitrary finite traces preserve the authority
  ceiling and exact checkpoint schema/digest.
- Accepted proposal events do not increment the committed-effect count.
- A revoked actor cannot propose and an incompatible migration cannot execute.
- One exact nine-event mixed-family route reaches the declared final state.
- The independent consumer accepts that route, rejects fifteen malformed or
  unsafe routes, records two commits and zero proposal effects, and rejects
  twelve targeted mutations.

## Countermodels and mutations

The corpus rejects proposal-time observed effects, authority widening,
checkpoint mismatch, missing fallback, self-evaluation, omitted assistance,
omitted lifecycle cost, omitted residual ownership, omitted rollback,
incompatible migration, commit without a pending proposal, commit without an
effect receipt or evidence transition, revocation to self, and readmission of a
revoked target. Mutations independently delete or corrupt the same load-bearing
guards on the accepted route.

## Executable refinement boundary

`scripts/validate_cognitive_kernel_abi_trace.py` is a bounded downstream
consumer. It independently implements the transition decision, applies accepted
events, and verifies the stored final state. This establishes agreement for the
finite corpus only. It is not a checked encoder/decoder between live runtime
objects and Lean values, and no material external effect service is connected.

## Adequacy adjudication

Adequate for: finite ABI record semantics, exact fixture lineage, negative-case
guard use, and one mixed-family control-plane trace.

Not adequate for: real architecture interchangeability; kernel capability or
quality; full-state checkpoint migration; concurrent revocation races;
effect-complete rollback; evaluator independence; lifecycle-cost accuracy;
natural workloads; matched baselines; reproduction; transfer; deployment;
architectural RSI; AGI; or ASI.

The model is therefore useful but too narrow for the chapter core. It does not establish a support-state transition. The next adequacy increment must connect
real runtime schemas and at least three genuinely different kernels, then test
concurrent revocation and effect-complete rollback before empirical tournament
claims are eligible.
