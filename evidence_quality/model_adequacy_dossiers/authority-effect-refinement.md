# Model-adequacy dossier: Authority grant-to-effect refinement

## Claim and model owner

- Chapter: `system-boundaries-and-authority`
- Frozen targets: `lean:authority.ceiling.operational_invariant`, `lean:authority.ceiling.failure_blocks_promotion`, `lean:authority.lifecycle.admission_route`, `lean:authority.revocation.trace_surface_bridge`
- Stronger model: `lean/AsiStackProofs/AuthorityEffectRefinement.lean`
- Executable consumer: `scripts/validate_authority_effect_refinement.py`
- Stored result: `experiments/authority_effect_refinement/results/2026-07-15-local.json`
- Result schema: `schemas/authority_effect_refinement.schema.json`
- Support-state effect is exactly `none`.

## State, transitions, and reachable consequences

The modeled state contains a caller ceiling, authority epoch, logical time, an optional active grant, approval and dispatch bindings, revoked grant IDs, material- and observed-effect counts, and rollback state. A grant binds an ID, principal, operation, target, authority level, epoch, expiry, and remaining-use count. Reachable events issue, approve, dispatch, commit an effect, independently observe it, revoke a grant, or roll the observed effect back.

The validity relation requires monotone logical time and event-specific custody. Issuance requires target-owner approval, a nonzero fresh grant ID, a live epoch, a nonexpired positive-use grant, and an authority level no greater than the caller ceiling. Approval, dispatch, and effect all require exact equality with the active grant; dispatch and effect additionally require matching approval/dispatch custody. Revocation clears live custody and increments the epoch. Effect consumes a use and clears approval and dispatch, preventing silent one-shot reuse.

## Proven finite consequences

- accepted issuance respects the caller ceiling and current epoch;
- accepted dispatch is exactly grant-bound, approved, unrevoked, current-epoch, nonexpired, positive-use, and receipted;
- accepted effect has the same properties and additionally requires a matching dispatch;
- the exact six-event witness reaches independent observation and exact rollback;
- widening, principal substitution, expiry, stale epoch, revocation, missing dispatch, and one-shot reuse are rejected in concrete countermodels.

## Independent executable refinement

The Python consumer independently reimplements the state machine and validates the executed source records rather than reading a Lean-generated summary. It validates the governed repository result against its own schema, binds every source by SHA-256, and records:

- 6 authority fixtures: 3 accepted and 3 rejected;
- 6 reachable witness events;
- 1 executed local effect, 1 independent observation, and 1 exact rollback;
- 2 pre-effect denials;
- 5 revocation trace entries;
- 9 governed scenarios, 3 releases, and 0 unsafe releases;
- 38 of 38 rejected model/source mutations.

## Countermodels and mutation adequacy

The mutation set changes one semantically material source field or sequence condition at a time: grant identity, caller-ceiling relation, epoch, expiry, remaining uses, target-owner approval, approval receipt, principal, operation, target, dispatch receipt, effect receipt, independent observation, exact rollback, revocation ordering, and second use. This demonstrates consequence sensitivity within the fixed local schema. It does not establish completeness against unmodeled fields or attacks.

## Assumptions and exclusions

Identifiers are abstract natural numbers; exact equality is not identity proof. Owner approval, receipts, observations, expiry, epoch, and source records are trusted inputs. The model is sequential and finite. The effect probe uses a generated local temporary file, while the repository workload is a bounded synthetic task. The model excludes natural-language interpretation, authentic identity and grant issuance, cryptography, races, distributed consistency, partial observation, adversarial infrastructure, deployed enforcement, production security, reproduction, transfer, safety, SOTA, AGI, and ASI.

## Disposition

Retain the general ceiling lemmas and lifecycle negative cases at their exact finite scope. Physically retire the projection-only audit/nonclaim theorem. Use the reachable model and independent consumer as the current bounded owner of grant-to-effect refinement. Do not promote the chapter core until authentic producers, concurrent revocation, deployed consumers, natural workloads, independent reproduction, and transfer evidence exist.
