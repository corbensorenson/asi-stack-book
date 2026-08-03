# Model-adequacy dossier: Human Intent resolution-to-contract refinement

## Ownership

- Chapter: `human-intent-as-a-formal-input`
- Frozen targets: `lean:intent.contract.operational_invariant`, `lean:intent.contract.failure_blocks_promotion`, `lean:intent.resolution.route_envelope`, `lean:intent.intake.probe_fixture_bridge`, `lean:intent.lowering.information_boundary`
- Stronger model: `lean/AsiStackProofs/IntentResolutionRefinement.lean`
- Consumer: `scripts/validate_intent_resolution_refinement.py`
- Result: `experiments/intent_resolution_refinement/results/2026-07-15-local.json`
- Schema: `schemas/intent_resolution_refinement.schema.json`
- Support-state effect is exactly `none`.

## Reachable model

The state machine moves among received, parsed, clarified, authority-reviewed, accepted, re-contract-required, and rejected states. State carries one root intent, contract version, constraint and stop hashes, authority ceiling and approved authority, ambiguity, acceptance, re-contract, block, and logical time. Events parse, clarify, review authority, compile, continue an unchanged contract, detect a material delta, accept a re-contract, or reject.

Compilation requires exact source/output constraint and stop hashes, the approved authority, no hidden override, no prohibited action, and no open ambiguity. Material means, authority, evidence, stop, affected-party, or support-promotion changes cannot silently continue; they enter re-contract state. Re-contract requires a receipt, a strictly newer version, nonempty hashes, and authority within the original ceiling.

## Finite consequences and countermodels

The kernel checks kind-specific write ownership, arbitrary-run root/ceiling/approved-authority preservation, recursive trace validity, batch composition, exact compile preservation, material-delta custody, re-contract version increase, and four traces covering re-contract, clarification, unchanged continuation, and rejection. Its command boundary proves a thin four-field projection non-injective over authored ten-field intents, rules out recovery of both collision witnesses, and proves the modeled full lowering injective. Its route boundary imports the static router, proves compile-versus-clarify and compile-versus-review collisions under a thin two-field transport, rules out exact recovery of both conflict routes, and proves round-trip, injectivity, and static-route preservation for a complete seven-field transport.

The independent consumer binds 4 valid/6 invalid intake counts, all 6 intake signals, 2 valid/7 invalid re-contract scenarios, and 13 plan fixtures. It checks all 14 trace prefixes and 18 batch splits, then rejects 40/40 single-field or route mutations across lineage, time, payload, prohibition, override, authority, clarification, constraint/stop preservation, ambiguity, material-delta detection, rejection, re-contract versioning, receipts, and ceiling while preserving the accepted prefix state. It additionally reconstructs six thin command-lowering collisions and two route-changing transport collisions, then rejects mutations to all ten full command fields and all seven complete route-transport fields.

## Assumptions and exclusions

Hashes are abstract equality tokens, not semantic equivalence. Authority and receipts are trusted fields, not authenticated facts. The intake result is a bounded summary rather than a raw natural-language corpus, and the plan fixtures are synthetic. The model is finite and sequential and stops before dispatch or effect. A complete route transport is complete only for the seven authored Boolean fields; it is not evidence that those fields are semantically sufficient. The model excludes natural-language understanding, preference elicitation quality, semantic completeness, legitimate authority extraction, valid consent, prompt-injection containment, private-source protection, deployed dispatch, effects, user satisfaction, natural workloads, reproduction, transfer, safety, SOTA, AGI, and ASI.

## Disposition

Physically retire the two assumption-restating headline theorems and three literal intake-summary declarations while preserving frozen lineage. Retain the legacy resolution/admission functions as imported bounded definitions and negative cases. Use the reachable model and independent consumer as the current owner of all five targets, including the route and lowering boundaries. Do not promote chapter support without raw natural-language corpora, calibrated independent labels, real parser/authority-extraction candidates, downstream effect enforcement, reproduction, and transfer.
