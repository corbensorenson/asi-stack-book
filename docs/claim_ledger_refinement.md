# Claim Ledger append-only refinement receipt

Recorded: 2026-07-15
Roadmap: `post-v2.3-claim-proof-and-sota-challenge-roadmap` P2/M3
Support-state effect: `none`

## Outcome

`AsiStackProofs.ClaimLedgerRefinement` replaces checklist acceptance and
support-authority ambiguity with a reachable append-only lifecycle: idle,
proposed, appended, materialized, and acknowledged. A revision is bound to the
exact claim identity, base ledger version, prior head digest, semantic and
ontology versions, prior and next recorded support ranks, history,
non-overwrite attestation, reason, residuals, dependency closure, migration,
surface plan, and surface acknowledgments.

An upward support record requires a receipt from the independent evidence
owner. An open contradiction blocks it. Without the receipt, the strongest
route is `handoff_to_evidence_owner`; the ledger cannot self-approve support or
request an external effect. A successful append advances the ledger and append
count by exactly one, preserves claim identity and the prior head through the
event binding, materializes the current view, and requires exact surface
acknowledgment before completion.

`python3 scripts/validate_claim_ledger_refinement.py` independently recomputes
all seventeen routes, consumes the exact five-valid/seven-invalid revision
suite and one-valid/eleven-invalid five-project contradiction lifecycle,
executes the four-event witness, and rejects all 29 lifecycle mutations.

## Exact boundary

This is finite authored structured-record evidence. Event-digest uniqueness,
claim extraction, semantic equivalence, assumption completeness, source and
evidence validity, contradiction discovery, reviewer competence, dependency
discovery, concurrent persistence, natural multi-surface synchronization,
causal usefulness, reproduction, transfer, and deployment are not established.
The observed support-rank change is a materialized authored evidence-owner
decision, not a support decision by this proof or validator. It creates no
chapter support movement, external effect, release authority, safety result,
SOTA result, AGI claim, or ASI claim.
