# Model-adequacy dossier: Human Intent resolution-to-contract refinement

## Ownership

- Chapter: `human-intent-as-a-formal-input`
- Frozen targets: `lean:intent.contract.operational_invariant`, `lean:intent.contract.failure_blocks_promotion`, `lean:intent.resolution.route_envelope`, `lean:intent.intake.probe_fixture_bridge`
- Stronger model: `lean/AsiStackProofs/IntentResolutionRefinement.lean`
- Consumer: `scripts/validate_intent_resolution_refinement.py`
- Result: `experiments/intent_resolution_refinement/results/2026-07-15-local.json`
- Schema: `schemas/intent_resolution_refinement.schema.json`
- Support-state effect is exactly `none`.

## Reachable model

The state machine moves among received, parsed, clarified, authority-reviewed, accepted, re-contract-required, and rejected states. State carries one root intent, contract version, constraint and stop hashes, authority ceiling and approved authority, ambiguity, acceptance, re-contract, block, and logical time. Events parse, clarify, review authority, compile, continue an unchanged contract, detect a material delta, accept a re-contract, or reject.

Compilation requires exact source/output constraint and stop hashes, the approved authority, no hidden override, no prohibited action, and no open ambiguity. Material means, authority, evidence, stop, affected-party, or support-promotion changes cannot silently continue; they enter re-contract state. Re-contract requires a receipt, a strictly newer version, nonempty hashes, and authority within the original ceiling.

## Finite consequences and countermodels

The kernel checks exact compile preservation, material-delta custody, re-contract version increase, one complete five-event trace, and rejecting cases for absent payload, prohibited action, hidden override, authority widening, constraint substitution, silent material continuation, and missing re-contract receipt.

The independent consumer binds 4 valid/6 invalid intake counts, all 6 intake signals, 2 valid/7 invalid re-contract scenarios, and 13 plan fixtures. It rejects 30 single-field or route mutations across lineage, time, payload, prohibition, override, authority, constraint/stop preservation, ambiguity, material-delta detection, re-contract versioning, receipts, and ceiling.

## Assumptions and exclusions

Hashes are abstract equality tokens, not semantic equivalence. Authority and receipts are trusted fields, not authenticated facts. The intake result is a bounded summary rather than a raw natural-language corpus, and the plan fixtures are synthetic. The model is finite and sequential and stops before dispatch or effect. It excludes natural-language understanding, preference elicitation quality, semantic completeness, legitimate authority extraction, prompt-injection containment, private-source protection, deployed dispatch, effects, user satisfaction, natural workloads, reproduction, transfer, safety, SOTA, AGI, and ASI.

## Disposition

Physically retire the two assumption-restating headline theorems and three literal intake-summary declarations while preserving frozen lineage. Retain the general resolution/admission branches as bounded negative cases. Use the reachable model and independent consumer as the current owner of the two headline targets and intake bridge. Do not promote chapter support without raw natural-language corpora, calibrated independent labels, real parser/authority-extraction candidates, downstream effect enforcement, reproduction, and transfer.
