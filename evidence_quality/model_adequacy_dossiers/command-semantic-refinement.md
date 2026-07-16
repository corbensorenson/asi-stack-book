# Model-adequacy dossier: Command semantic-interface refinement

## Ownership

- Chapter: `intent-to-execution-contracts`
- Frozen targets: `lean:command.semantic_interface.operational_invariant`, `lean:command.semantic_interface.failure_blocks_promotion`, `lean:command.semantic_interface.field_confidence_route`
- Stronger model: `lean/AsiStackProofs/CommandSemanticRefinement.lean`
- Independent consumer: `scripts/validate_command_semantic_refinement.py`
- Result: `experiments/command_semantic_refinement/results/2026-07-15-local.json`
- Schema: `schemas/command_semantic_refinement.schema.json`
- Support-state effect: exactly `none`

## Reachable model

The state machine moves through raw, fields-bound, precedence-checked, authority-bound, planning-validated, dispatch-ready, and blocked stages. Six semantic slots carry a nonzero abstract value identity, provenance, and confidence. General command fields may dispatch only when their provenance is human intent, policy, a named source, or a bounded default and their confidence is confirmed, policy-imposed, source-derived, or defaulted. Authority is stricter: only confirmed or policy-imposed confidence is eligible.

Binding requires five non-authority slots to be eligible and a present authority slot. Precedence review requires exact slot identity, the authoritative constraint-source identity, and no applied hidden override. Authority binding requires exact slots, authority-ready provenance/confidence, a request no wider than the ceiling, and an approval receipt. Planning validation requires exact slots and approved authority, no override or blocker, and a validation receipt. Dispatch requires the preserved slots, prior planning-validation custody, exact approved authority, approval, no blocker, and a dispatch receipt.

## Finite consequences and countermodels

The kernel checks validity of every accepted transition, exact preservation through planning validation, exact authority and receipt custody at dispatch, one complete reachable trace, and eight named countermodels. The independent consumer reimplements those rules and rejects 38 mutations across missing or inferred fields, hidden provenance, lineage/time drift, precedence substitution, inferred or widened authority, missing approval, slot substitution, blocker insertion, and missing validation or dispatch receipts.

All 13 plan-execution fixtures carry command contracts that pass the public command schema. The consumer assigns five to command-interface violation, two to correct command-interface block, and six to command-interface admissible. Admissibility is deliberately consumer-relative: five of those six still fail downstream gates. The packet also digest-binds the existing nine-trace handoff result and the nine-scenario, 89-event vertical result without converting their results into broader command claims.

## Assumptions, exclusions, and adequacy verdict

Value hashes are trusted identity tokens, not natural-language meanings. Provenance, confidence, authority, approvals, receipts, and fixture labels are trusted. The model is finite, sequential, deterministic, and synthetic. It neither authenticates principals nor discovers hidden instructions, field meanings, affected parties, or effects.

The model is adequate for the narrowed claim that an exact finite command boundary rejects the represented substitution, confidence, authority, precedence, blocker, and receipt failures before dispatch. It is inadequate for natural-language semantic preservation, calibrated confidence, authentic authority extraction, prompt-injection containment, deployed enforcement, concurrent behavior, useful task completion, reproduction, transfer, safety, SOTA, AGI, ASI, or chapter-core support.

## Disposition

Physically retire the two projection-only declarations while preserving their frozen lineage. Retain the missing-field, accepted-override, and three field-confidence theorems only as bounded negative or reusable finite branches. The reachable refinement becomes the current owner of all three stable command targets. Promotion requires natural ambiguous and adversarial command workloads, independent semantic labels and evaluators, actual parser/model candidates, deployed effect enforcement, matched baselines, reproduction, and transfer.
