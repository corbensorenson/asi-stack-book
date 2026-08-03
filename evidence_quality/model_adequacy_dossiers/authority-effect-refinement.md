# Model-adequacy dossier: Authority grant-to-effect refinement

## Claim and model owner

- Chapter: `system-boundaries-and-authority`
- Frozen targets: `lean:authority.ceiling.operational_invariant`, `lean:authority.ceiling.failure_blocks_promotion`, `lean:authority.lifecycle.admission_route`, `lean:authority.revocation.trace_surface_bridge`
- Stronger models: `lean/AsiStackProofs/AuthorityEffectRefinement.lean` and `lean/AsiStackProofs/Authority.lean`
- Executable consumer: `scripts/validate_authority_effect_refinement.py`
- Stored result: `experiments/authority_effect_refinement/results/2026-07-15-local.json`
- Result schema: `schemas/authority_effect_refinement.schema.json`
- Support-state effect is exactly `none`.

## State, transitions, and reachable consequences

The modeled state contains a caller ceiling, authority epoch, logical time, an optional active grant, approval and dispatch bindings, revoked grant IDs, material- and observed-effect counts, and rollback state. A grant binds an ID, principal, operation, target, authority level, epoch, expiry, and remaining-use count. Reachable events issue, approve, dispatch, commit an effect, independently observe it, revoke a grant, or roll the observed effect back.

The validity relation requires monotone logical time and event-specific custody. Issuance requires target-owner approval, a nonzero fresh grant ID, a live epoch, a nonexpired positive-use grant, and an authority level no greater than the caller ceiling. Approval, dispatch, and effect all require exact equality with the active grant; dispatch and effect additionally require matching approval/dispatch custody. Revocation clears live custody and increments the epoch. Effect consumes a use and clears approval and dispatch, preventing silent one-shot reuse.

The delegation refinement separately models a root grant and principal, exact operation/target/scope custody, current parent grant, acting principal, child grant and delegate, current ceiling, epoch, expiry, logical time, revocation inventory, depth, receipt count, and support/effect non-authority. An accepted handoff requires exact parent and acting-principal joins, a fresh nonrevoked child, a positive delegate, unchanged operation/target/scope/epoch, non-increasing ceiling and expiry, monotone live time, a receipt, and no support or external-effect request.

## Proven finite consequences

- accepted issuance respects the caller ceiling and current epoch;
- accepted dispatch is exactly grant-bound, approved, unrevoked, current-epoch, nonexpired, positive-use, and receipted;
- accepted effect has the same properties and additionally requires a matching dispatch;
- every successful arbitrary-length run preserves observation/effect accounting, live-grant ceiling/epoch/revocation safety, and exact approval/dispatch custody;
- every successful run yields a recursively valid transition trace and composes across arbitrary event-batch splits;
- revoked grant IDs persist through every successful suffix, and no event in such a suffix can approve, dispatch, or commit an effect under the revoked ID;
- a rejected event returns no successor state, while every accepted rollback clears material and observed effect accounting and marks exact rollback;
- exact one-use and two-use witnesses reach independent observation and exact rollback, while a separate revocation witness clears custody and advances the epoch;
- widening, principal substitution, expiry, stale epoch, revocation, missing dispatch, and one-shot reuse are rejected in concrete countermodels.
- arbitrary finite delegation runs preserve root and effect custody, non-authority, attenuation, epoch continuity, expiry bounds, state invariants, and recursively valid traces, and compose across event batches;
- a two-hop witness reaches an attenuated second-generation delegate with two receipts, while ten closed substitutions reject;
- identical thin summaries can hide opposite authority decisions, so no classifier over that summary can recover exact authority for both witness states;
- a complete 20-field transport round-trips, is injective, and preserves the delegation step.

## Independent executable refinement

The Python consumer independently reimplements both state machines, recompiles
the exact 31- and 59-theorem Lean surfaces, and validates the executed source
records rather than reading a Lean-generated summary. It validates the
governed repository result against its own schema, binds every source by
SHA-256, and records:

- 6 authority fixtures: 3 accepted and 3 rejected;
- 3 reachable witness traces with 20 accepted events;
- 20 invariant-preserving prefixes and 23 exact batch compositions;
- 1 executed local effect, 1 independent observation, and 1 exact rollback;
- 2 pre-effect denials;
- 5 revocation trace entries;
- 9 governed scenarios, 3 releases, and 0 unsafe releases;
- 50 of 50 rejected model/source mutations, each preserving the accepted prefix state.
- 1 two-event delegation trace, 3 invariant states, and 3 exact delegation compositions;
- 17 of 17 rejected delegation mutations, each preserving the exact pre-event state;
- 1 thin-summary authority collision and 20 of 20 rejected complete-transport field mutations.

## Countermodels and mutation adequacy

The mutation set changes one semantically material source field or sequence condition at a time: grant identity, caller-ceiling relation, epoch, expiry, remaining uses, target-owner approval, approval receipt, principal, operation, target, dispatch/effect/revocation receipts, independent observation, observation overcount, exact rollback, rollback ordering, revocation binding, post-revocation dispatch/effect/reissuance, and second use. This demonstrates consequence sensitivity and rejection noninterference within the fixed local schema. It does not establish completeness against unmodeled fields or attacks.

## Assumptions and exclusions

Identifiers are abstract natural numbers; exact equality is not identity proof. Owner approval, delegation and effect receipts, observations, expiry, epoch, and source records are trusted inputs. The models are sequential and finite. The effect probe uses a generated local temporary file, while the repository workload is a bounded synthetic task. The models exclude natural-language interpretation, authentic identity and grant issuance, hidden descendants, cryptography, races, distributed consistency, partial observation, adversarial infrastructure, deployed enforcement, production security, reproduction, transfer, safety, SOTA, AGI, and ASI.

## Disposition

Retain the general ceiling lemmas and lifecycle negative cases at their exact
finite scope. Physically retire the projection-only audit/nonclaim theorem.
Move all four public targets to the reachable model and independent consumer as
the current bounded owner of grant-to-effect refinement. This is adequate only
as a finite authored-record invariant. Do not promote the chapter core until
authentic producers, concurrent revocation, deployed consumers, natural
workloads, independent reproduction, and transfer evidence exist.
