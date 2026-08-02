# Authority grant-to-effect refinement receipt

Recorded: 2026-07-15
Roadmap: `post-v2.3-claim-proof-and-sota-challenge-roadmap` P2/M3
Support-state effect: `none`

## Outcome

The `system-boundaries-and-authority` proof family now has a reachable grant-to-effect model in `lean/AsiStackProofs/AuthorityEffectRefinement.lean` and an independently implemented concrete consumer in `scripts/validate_authority_effect_refinement.py`.

The Lean model binds every grant, approval, dispatch, and material effect to the same abstract grant ID, principal, operation, target, authority ceiling, authority epoch, expiry, and remaining-use count. Its 31 declarations include one-step consequences plus an inductive state invariant and caller-ceiling preservation over arbitrary successful runs, valid-trace extraction, event-batch composition, revoked-ID persistence, and a theorem that no successful suffix can approve, dispatch, or commit an effect for an already revoked grant. Rejected events return no successor state, and accepted rollback clears both effect counters and marks exact rollback. Separate one-use, two-use, and revocation witnesses cover 20 accepted events; the effect traces reach independent observation and exact rollback, while the revocation trace clears grant, approval, and dispatch custody and advances the epoch.

The consumer recompiles the exact thirty-one-theorem surface and binds that model to four pre-existing evidence surfaces by digest:

- six authority-decision fixtures: three accepted and three rejected;
- one executed local temporary-file effect with independent digest observation and exact rollback;
- two pre-effect denials with unchanged state;
- five revocation-propagation trace entries;
- nine governed repository-change scenarios, including three releases and zero unsafe releases.

It independently checks all 20 witness prefixes and 23 event-batch splits. It also rejects 50 single-fault and sequence mutations spanning grant identity, principal, operation, target, ceiling, epoch, expiry, use count, target-owner approval, approval/dispatch/effect/revocation receipts, observation independence and overcount, rollback exactness and ordering, post-revocation dispatch/effect/reissuance, and one-shot reuse. Every rejection is checked against the accepted prefix state so failure cannot mutate authority state in the executable model.

## What changed in the proof envelope

The general finite ceiling theorems and useful lifecycle route lemmas remain bounded local results. The projection-only theorem `valid_authority_decision_has_audit_and_nonclaims` is physically retired. Its frozen lineage remains auditable, but all four public targets now move to the reachable model, concrete consumer, mutation suite, and this receipt at finite authored-record scope.

## Exact boundary

This packet does not prove natural-language authority extraction, real identity or receipt authenticity, wise grant issuance, complete effect observation, concurrent revocation safety, distributed enforcement, deployed authorization middleware, production security, reproduction, transfer, safety, SOTA, AGI, ASI, or chapter-core support. Numeric identities and receipt fields are trusted finite inputs. The executed effect is public-safe and local; the repository workload is bounded. No support or release transition is created.
