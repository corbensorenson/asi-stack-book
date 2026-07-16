# Model-adequacy dossier: Context Certificate reachable refinement

## Ownership

- Chapter: `virtual-context-abi`
- Frozen targets: `lean:vcm.certificates.operational_invariant`, `lean:vcm.certificates.failure_blocks_promotion`, `lean:vcm.certificates.lifecycle_admission_route`
- Stronger model: `lean/AsiStackProofs/ContextCertificateRefinement.lean`
- Independent consumer: `scripts/validate_context_certificate_refinement.py`
- Result: `experiments/context_certificate_refinement/results/2026-07-15-local.json`
- Schema: `schemas/context_certificate_refinement.schema.json`
- Support-state effect: exactly `none`

## Reachable model

The state machine moves through raw, source-bound, derived, certified, verified, admitted, revoked, and quarantined stages. The narrowed state uses one certificate and one source identity, one derived-representation identity, source and derived authority ranks, loss-contract, omission-ledger, and permitted-use identities, lifecycle epoch, five receipt classes, revocation and taint flags, admission, and logical time.

Binding requires well-formed nonzero certificate/source identities, source authority within the external ceiling, a nonzero lifecycle epoch, and no revocation or taint. Derivation preserves certificate/source identity, requires a declared source binding and receipt, binds a nonzero derived representation, and forbids represented authority escalation. Certification preserves source/derived identity, requires nonzero loss, omission, and permitted-use contracts plus a certificate receipt, matches the current epoch, and excludes revocation and taint. Verification preserves the full contract tuple, requires verifier references, a passing outcome and receipt, and deletion closure when required. Admission preserves that tuple, requires exact consumer-use scope and prior receipt custody, and requires an evidence-transition receipt for any support-promotion request.

## Consequences, countermodels, and consumer

The kernel checks accepted-transition validity, source and authority preservation at derivation, full provenance/contract and receipt preservation at admission, one five-event witness, and thirteen countermodels. The independent consumer separately implements the transition relation and rejects 64 single-fault mutations.

The public certificate schema and real fixture inventory are consumed at their exact boundary. One canonical protocol fixture and all 12 certificates from eight context-admission scenarios are schema-valid and shape-complete; eleven are active and one is stale. Those facts do not classify the whole scenarios. The distinct admission harness still accepts three and rejects five because adequacy, conflict, deletion, mode, and promotion facts live outside certificate shape.

## Assumptions, exclusions, and adequacy verdict

Numeric identifiers, authority ranks, lifecycle epochs, declarations, policy decisions, verifier results, deletion/evidence-transition receipts, and fixture labels are trusted. One source and one permitted-use slot are finite witnesses, not arbitrary provenance graphs or policy lattices. The model is sequential and deterministic. It does not inspect source or derived content, calculate a digest, validate transformation fidelity or omissions, authenticate authority, execute a verifier, observe deletion, model concurrent revocation, or enforce a consumer.

The model is adequate for the narrowed claim that this exact finite transition system preserves represented provenance, contract, authority, epoch, and receipt custody before admission and rejects the represented lifecycle faults. It is inadequate for certificate truthfulness, source/derived semantic equivalence, omission completeness, verifier independence, deployed enforcement, concurrent revocation, deletion propagation, natural workloads, reproduction, transfer, safety, SOTA, AGI, ASI, or chapter-core support.

## Disposition

Physically retire the two direct projections while preserving frozen lineage. Retain the derived authority-escalation contradiction as a reusable bounded lemma and retain the fifteen general lifecycle routes as explicit negative/admission cases. Make the reachable refinement the current owner of all three stable certificate targets. Promotion requires authenticated multi-source provenance, observed transformations and omissions, independently implemented content verification, concurrent lifecycle/revocation tests, deletion propagation, actual consumer enforcement, natural held-out workloads, matched strong baselines, complete costs and failures, reproduction, and transfer.
