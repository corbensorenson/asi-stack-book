# Authority grant-to-effect refinement receipt

Recorded: 2026-07-15
Roadmap: `post-v2.3-claim-proof-and-sota-challenge-roadmap` P2/M3
Support-state effect: `none`

## Outcome

The `system-boundaries-and-authority` proof family now has a reachable grant-to-effect model in `lean/AsiStackProofs/AuthorityEffectRefinement.lean` and an independently implemented concrete consumer in `scripts/validate_authority_effect_refinement.py`.

The Lean model binds every grant, approval, dispatch, and material effect to the same abstract grant ID, principal, operation, target, authority ceiling, authority epoch, expiry, and remaining-use count. It proves that accepted issuance cannot exceed the caller ceiling, accepted dispatch is exactly bound and fresh, and accepted material effect requires the live grant, its approval, and its dispatch receipt. A six-event witness reaches one independently observed effect and exact rollback. Countermodels reject authority widening, principal substitution, expired or stale dispatch, post-revocation dispatch, effect without dispatch, and reuse of a consumed one-shot grant.

The consumer binds that model to four pre-existing evidence surfaces by digest:

- six authority-decision fixtures: three accepted and three rejected;
- one executed local temporary-file effect with independent digest observation and exact rollback;
- two pre-effect denials with unchanged state;
- five revocation-propagation trace entries;
- nine governed repository-change scenarios, including three releases and zero unsafe releases.

It also rejects 38 single-fault and sequence mutations spanning grant identity, principal, operation, target, ceiling, epoch, expiry, use count, target-owner approval, dispatch/effect receipts, observation independence, rollback exactness, post-revocation dispatch, and one-shot reuse.

## What changed in the proof envelope

The general finite ceiling theorems and useful lifecycle route lemmas remain bounded local results. The projection-only theorem `valid_authority_decision_has_audit_and_nonclaims` is physically retired. Its frozen lineage remains auditable, but current ownership moves to the reachable model, concrete consumer, mutation suite, and this receipt.

## Exact boundary

This packet does not prove natural-language authority extraction, real identity or receipt authenticity, wise grant issuance, complete effect observation, concurrent revocation safety, distributed enforcement, deployed authorization middleware, production security, reproduction, transfer, safety, SOTA, AGI, ASI, or chapter-core support. Numeric identities and receipt fields are trusted finite inputs. The executed effect is public-safe and local; the repository workload is bounded. No support or release transition is created.
