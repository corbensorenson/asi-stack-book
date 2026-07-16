# Proof-Carrying Claims target-to-writeback refinement receipt

Recorded: 2026-07-15
Roadmap: `post-v2.3-claim-proof-and-sota-challenge-roadmap` P2/M3
Support-state effect: `none`

## Outcome

`AsiStackProofs.ProofCarryingClaimsRefinement` replaces assumed-validity
projections with a reachable six-stage lifecycle: idle, frozen,
artifact-bound, executed, adjudicated, and written back. The lifecycle binds
the exact claim version, target, interpretation, scope, assumptions, artifact,
verifier identity and version, trusted base, execution result, attempt history,
semantic review, dossier, dissent, limitations, residual, and owner handoff.

A passed verifier record cannot advance without verifier artifacts, verified
artifact status, and a reviewed semantic mapping. Failed, timed-out, or
mismatched results cannot request a scoped positive proposal; a mismatch must
route to tribunal. High-risk adjudication requires an independent dossier,
dissent must survive, and final writeback is only a proposal to the owning
ledger/evidence gates. This layer cannot assign support or commit an external
effect.

`python3 scripts/validate_proof_carrying_claims_refinement.py` independently
recomputes all twenty-three routes, consumes the exact three-valid/five-invalid
proof-carrying fixture suite and two-valid/seven-invalid adversarial-dossier
suite, executes the five-event witness, and rejects all 36 mutations.

## Exact boundary

This is finite authored structured-record evidence. Target meaning, semantic
equivalence, artifact truth, proof/citation/procedure/replay/benchmark
soundness, trusted-base correctness, verifier or reviewer competence,
independence, verdict correctness, claim truth, evidence adequacy, action
authority, natural workloads, useful advantage, causality, safety, total cost,
concurrent persistence, deployment, reproduction, and transfer are not
established. The final scoped proposal is an owner handoff, not support
assignment. It creates no chapter support movement, release authority, SOTA
result, AGI claim, or ASI claim.
