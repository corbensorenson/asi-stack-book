# QCSA Reference Implementation Report

Date: 2026-07-13

State: twelve bounded lanes implemented and deterministically replayed; held-out
evaluation outcomes unopened

## Result

The standard-library QCSA reference package now implements `QI-01` through
`QI-12` as a file-backed, deterministic local slice. Two clean builder replays
produce byte-identical artifacts. Each lane has a content-addressed envelope,
frozen payload contract, chapter owners, input digests, non-claim boundary, and
at least one rejecting behavioral control. The final manifest binds all eleven
upstream lane digests and the exact implementation code, schemas, fixtures,
configuration, seeds, result summary, replay log, and environment record.

The implementation validator exercises fifteen additional mutations against
the integrated bundle. It rejects digest tampering, identity-kind collapse,
dangling evidence, candidate-epoch authority, signature laundering, question
selection drift, missing receipts, silent migration retargeting, hidden
adversarial misses, grounding-residual erasure, evaluator self-confirmation,
negative resource counters, descendant mutation, hidden failed controls, and
premature held-out access.

## Lane disposition before evaluation

| Lane | Implemented behavior | Preserved limitation |
|---|---|---|
| `QI-01` | Eight separate identity kinds; stable opaque SOIDs; alias, merge, and split lineage; duplicate and retarget rejection. | A finite registry does not establish ontology quality or universal identity. |
| `QI-02` | Typed temporal nodes and hyperedges; contradiction and dangling-reference checks; distinct evidence, belief, authority, lifecycle, and use records. | Graph integrity is not proposition truth. |
| `QI-03` | Three facets; variable paths; top-k, unknown, conflict, and abstention; immutable candidate versus authoritative epochs. | Paths are hand-constructed fixtures, not learned semantic quality. |
| `QI-04` | SAC with identity, context, use, epoch, confidence, provenance, grounding, residual, validity, migration, zero-effect authority ceiling, digest, and fixture signature. | Fixture signing is not cryptographic identity or federation trust. |
| `QI-05` | Expected-decision-value selection net of compute, latency, privacy, burden, and risk under a three-question ceiling. | This is a declared-candidate policy, not a learned or optimal question policy. |
| `QI-06` | Certificate lowering into model/tool/verification steps; separate authority policy; refusal fallback; one receipt per attempted effect. | The adapter is local and deterministic; no production effect or authority system exists. |
| `QI-07` | Same-SOID compatibility, typed failure, merge/split lineage, shadow result, descendants, caches, backups, receipts, and exact rollback identity. | The record does not establish model forgetting, privacy erasure, or storage erasure. |
| `QI-08` | Nine adversarial controls covering alias escalation, collision, poisoning, stale epoch, branch overload, route disagreement, tampering, privacy cost, and missing residuals. | Blocked synthetic fixtures are not a safety or security result. |
| `QI-09` | English/Spanish paired labels and synthetic modality descriptors with explicit coverage boundary. | The control deliberately retains one false equivalence and one unsupported grounding; no universal grounding claim is available. |
| `QI-10` | Nine-dimension structural round trip with a separately implemented evaluator. | A list-order case deliberately preserves disagreement on residuals; evaluator adequacy remains open. |
| `QI-11` | Nonnegative latency, byte/token, question, retrieval, call, verifier, fallback, abstention, repair, migration, and human-burden counters. | These local counters are not production cost or real-human burden measurements. |
| `QI-12` | Content and size digests over code, schemas, fixtures, configuration, seeds, results, logs, and environment; missing/mutated descendant rejection. | File integrity does not establish semantic adequacy or supply-chain trust. |

## Evidence boundary

This closes implementation milestone M3 only. No held-out labels, matched
baseline outcomes, ablation outcomes, performance advantage, safety result,
privacy result, open-world transfer, external reproduction, production
deployment, AGI, ASI, or chapter-core support transition is claimed. The next
authority is the frozen six-family, 180-case evaluation in
`experiments/qcsa_reference/test_plan.json`.
