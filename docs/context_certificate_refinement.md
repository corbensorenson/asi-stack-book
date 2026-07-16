# Context Certificate reachable-refinement receipt

Recorded: 2026-07-15
Roadmap: `post-v2.3-claim-proof-and-sota-challenge-roadmap` P2/M3
Support-state effect: `none`

## Outcome

`lean/AsiStackProofs/ContextCertificateRefinement.lean` replaces two direct assumption projections with reachable source-binding, derivation, certification, verification, and consumer-admission semantics. State carries exact abstract identities for certificate, source, derived representation, loss contract, omission ledger, and permitted use; source and derived authority; lifecycle epoch; source-binding, certificate, verification, deletion-closure, and evidence-transition receipts; revocation, taint, admission, stage, and logical time.

The five-event witness binds a source within an authority ceiling, derives a source-bound representation without authority escalation, certifies explicit loss, omission, and permitted-use contracts, verifies the exact current certificate with deletion closure, and admits only its exact permitted use. Lean proves that accepted derivation preserves certificate/source identity and does not widen represented authority, and that accepted admission preserves the full represented provenance/contract tuple plus receipt custody. Thirteen named countermodels reject source substitution, authority escalation, missing source-binding receipt, missing loss/omission/use declarations, stale lifecycle epoch, missing verification or deletion-closure receipts, unpermitted use, support promotion without an evidence transition, taint, and revocation.

`python3 scripts/validate_context_certificate_refinement.py` independently reimplements the transition relation. It validates the canonical protocol certificate and all 12 certificate records across the eight context-admission scenarios against the public schema, records eleven active and one stale certificate, keeps that certificate-shape judgment separate from the whole-scenario three-valid/five-invalid admission result, accepts the five-event witness, and rejects 64 of 64 mutations.

## Exact boundary

Schema-valid, shape-complete certificates are not thereby truthful, fresh, adequate, or admissible. Numeric identities, authority ranks, lifecycle epochs, policy decisions, declarations, verifier outcomes, and receipts remain trusted abstract inputs. The packet does not establish source or payload truth, transformation or omission fidelity, verifier independence, deployed certificate enforcement, deletion propagation, natural-workload usefulness, reproduction, transfer, safety, SOTA, AGI, ASI, or chapter-core support. It creates no effect, evidence transition, support transition, or release transition.
