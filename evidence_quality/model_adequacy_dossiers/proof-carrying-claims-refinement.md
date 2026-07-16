# Model-adequacy dossier: Proof-Carrying Claims refinement

## Ownership

- Chapter: `spinoza-verification-and-proof-carrying-claims`
- Frozen targets: the three `lean:spinoza.proof_carrying.*` and
  `lean:spinoza.adversarial_review.*` targets currently backed by
  `AsiStackProofs.ProofCarryingClaims`
- Stronger model: `lean/AsiStackProofs/ProofCarryingClaimsRefinement.lean`
- Independent consumer: `scripts/validate_proof_carrying_claims_refinement.py`
- Result: `experiments/proof_carrying_claims_refinement/results/2026-07-15-local.json`
- Support-state effect: exactly `none`

## Reachable model

The model owns one target-specific verification event from prospective freeze
through artifact binding, verifier execution, bounded adjudication, and owner
writeback. It preserves exact target and interpretation identity; binds the
artifact, verifier version, and trusted base; separates verifier result from
artifact and semantic adequacy; preserves negative attempts and dissent; and
turns the final effect into a handoff rather than direct support assignment.

## Consequences, countermodels, and consumer

General consequences preserve target identity and prevent changes to support-
assignment or external-effect counts across every accepted step. Each accepted
step adds exactly one receipt. Countermodels reject target, artifact, verifier,
result, and writeback substitution; missing interpretation, scope, assumptions,
artifact, trusted base, execution receipt, passed-verifier refs, negative
attempt history, semantic review, independent dossier, dissent, limitations,
residual, and owner handoff; negative promotion; mismatch without tribunal; and
support or external-effect authority leakage. A five-event witness reaches
owner writeback with zero assigned support and zero external effects.

The independent consumer covers all twenty-three routes, consumes the exact
3/5 proof-carrying fixtures and 2/7 adversarial-dossier cases, and rejects 36
mutations across those boundaries.

## Assumptions, exclusions, and adequacy verdict

Identifiers, digests, artifact presence and verification, semantic-review
status, verifier result, trusted-base identity, risk, reviewer independence,
dossier quality, dissent, limitations, residuals, and owner receipt are trusted
inputs. The model is adequate for the exact represented lifecycle, route
priority, binding custody, negative-result handling, and authority separation.
It is inadequate for natural target interpretation, semantic equivalence,
artifact or source truth, proof or verifier soundness, reviewer competence or
independence, verdict quality, claim truth, evidence adequacy, useful outcomes,
causality, safety, cost advantage, concurrency, deployment, reproduction,
transfer, SOTA, AGI, ASI, or chapter-core support.

## Disposition

Retire the four assumption-restating or broad projection bridges in
`AsiStackProofs.ProofCarryingClaims`. Retain the four small artifact-reference
and negative-result lemmas as bounded lineage. Move the three public targets to
the refinement module. No support state changes.
