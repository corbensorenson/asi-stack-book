# Accepted Transition Review Audit

The Accepted Transition Review Audit checks the real accepted transition
records under `evidence_transitions/` and the accepted no-promotion ledger in
`claim_decisions/v1_0_core_claim_no_promotion.json`.

It verifies 45 accepted transition records, including seven bounded non-core
upward transitions and no accepted upward transition for a chapter core claim.
It also checks the accepted no-promotion decision ledger for current manifest
core claims. The audit requires accepted review status, review-accepted
validity state, changelog references, evidence packet references, verification
commands, limitations, reviewer-independence disclosure, support-state effect
boundaries, and non-claims. It runs seven expected-invalid mutation controls
for core upward promotion, missing changelog, missing non-claims, upward
transition without evidence packets, upward transition with unresolved
acceptance blockers, no-change support movement, and no-promotion support
effect drift.

Run:

```bash
python3 scripts/validate_accepted_transition_review_audit.py
```

The local result record is:

```text
experiments/accepted_transition_review/results/2026-07-02-local.json
```

This audit does not prove evidence truth, prove reviewer independence, prove
source interpretation, promote chapter core claims, approve new support-state
transitions, or prove external review quality. In short: no support-state
transition.
