# Verification Bandwidth reachable-refinement receipt

Recorded: 2026-07-15
Roadmap: `post-v2.3-claim-proof-and-sota-challenge-roadmap` P2/M3
Support-state effect: `none`

## Outcome

`AsiStackProofs.VerificationBandwidthRefinement` replaces the legacy
`allowVerifiedSupport` authority leak and copied summary bridges with a
prospective plan, exact execution binding, exhaustive obligation disposition,
adjudication route, and evidence-gate handoff. The five reachable stages are
proposed, frozen, executed, adjudicated, and handed off. The strongest positive
route is `handoff_to_evidence_gate`; it cannot assign support.

The model binds plan, claim version, context packet digest, admission and
transaction state, risk, requested effect, obligation count, authority, rights,
budget, horizon, stop rule, exact disposition totals, negative-evidence search,
evaluator separation, artifacts, residuals, and expiry. Contradictions block;
open dispositions remain residuals; high-risk correlated evaluation escalates;
and a direct chapter-core promotion request is rejected.

`python3 scripts/validate_verification_bandwidth_refinement.py` independently
recomputes all twelve routes, consumes the existing 3-valid/5-invalid admission
suite, 2-valid/7-invalid contradiction suite, and 3-valid/5-invalid capacity
suite, accepts one complete five-stage lifecycle, and rejects every recorded
mutation—31 of 31—before evidence-gate handoff.

## Exact boundary

This is finite authored structured-record evidence. It does not run a model or
natural claim, discover contradictions, measure distractor resistance,
establish evaluator competence or independence, validate a capacity law,
operate a deployed ledger or escalation service, compare usefulness, prove
causality, reproduce or transfer a result, authorize release, or move chapter
support. An evidence-gate handoff is a request for a different owner to review
evidence, not evidence or promotion itself.
