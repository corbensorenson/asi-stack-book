# P4-C1 Evidence, Claim, and Proof Custody Semantic Audit

Status: **terminal adequate at bounded finite custody scope**.

## Cluster decision

The cluster contains four modules and sixteen public proof targets. The audit
does not use theorem count as an exit criterion. Each module has a proposition,
modeled state, explicit assumptions, countermodels, executable or specification
consumer, rejecting mutation evidence, and a maximum inference in the machine
record at
`proofs/semantic_cluster_audits/evidence_claim_and_proof_custody.json`.

| Module | Disposition | Semantic reason |
|---|---|---|
| `AsiStackProofs.EvidenceStates` | reclassify | The transition route and four executable audit bridges are useful finite policy semantics. Direct conjunct projections remain lineage and receive no semantic credit. |
| `AsiStackProofs.ClaimLedgerRefinement` | adequate | A reachable append-only lifecycle preserves identity/history/effect custody, rejects stale and unauthorized revisions, advances one exact version, and has a 17-route independent consumer with 29 mutations. |
| `AsiStackProofs.ProofCarryingClaimsRefinement` | adequate | A reachable verification lifecycle separates target, artifact, verifier, semantic review, adjudication, and owner authority; a 23-route consumer rejects 36 mutations. |
| `AsiStackProofs.ProofEnvelope` | reclassify | Its negative artifact-admission countermodels are useful, but positive module/build and non-operational results are assumed-record projections. It is retained as specification policy, not runtime enforcement. |

The two reclassifications are not failures hidden behind a green cluster state.
They are the terminal correction required by P4: the useful negative and route
semantics remain, while direct projections lose the stronger interpretation
that their old headline names invited.

## Semantic chain

Evidence States decides whether a requested support change has the required
bounded record. Claim Ledger Refiment owns an append-only versioned history and
the evidence-owner handoff. Proof-Carrying Claims owns one exact verification
event without support or action authority. Proof Envelope classifies what kind
of formal artifact may be named and which bounded records are still missing.
Together they establish a custody chain over authored records, not the truth of
the records' contents.

The strongest countermodels are operationally distinct: missing evidence or
review blocks a transition; stale base or self-approval blocks a ledger append;
missing artifacts, attempt history, dossier, or owner handoff blocks a proof
event; and a non-Lean or inadequately bounded artifact cannot be laundered into
a Lean-proof or support-promotion label.

## Maximum inference

The cluster is adequate only for its finite represented policy and lifecycle
semantics. Trusted identifiers, digests, receipts, evidence references,
semantic-review fields, verifier outcomes, and reviewer/owner claims remain
assumptions. The results do not prove evidence truth, claim truth, semantic
equivalence, proof-kernel soundness, verifier correctness, reviewer competence
or independence, persistence, concurrency, runtime enforcement, usefulness,
safety, transfer, SOTA, AGI, ASI, or any support-state movement.

## Reproduction

```bash
python3 scripts/validate_p4_c1_semantic_proof_cluster.py
python3 scripts/validate_evidence_bundle_completeness_probe.py
python3 scripts/validate_claim_ledger_completeness_audit.py
python3 scripts/validate_accepted_transition_review_audit.py
python3 scripts/validate_claim_state_transition_bridge.py
python3 scripts/validate_claim_ledger_refinement.py
python3 scripts/validate_proof_carrying_claims_refinement.py
(cd lean && lake build)
```

The cluster validator checks the exact frozen membership, all semantic fields,
module declarations, manifest targets, consumer artifacts, chapter limitation
language, and registered negative mutations. The next formal packet is
`P4-C2-safety-assurance-and-oversight-semantic-audit`.
