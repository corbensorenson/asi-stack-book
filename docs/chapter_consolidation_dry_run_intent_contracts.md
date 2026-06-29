# Chapter Consolidation Dry Run: Intent And Executable Contracts

Last updated: 2026-06-29

This is a non-pilot dry-run package required by
`docs/v1_x_beyond_sota_roadmap.md` and
`docs/chapter_consolidation_sequence.md`. It is a review artifact only. It
does not edit `book_structure.json`, delete a chapter, change a URL, rewrite a
chapter, change source mappings, change proof targets, change support states,
or approve a reader artifact.

Dry-run destination:
`intent-to-execution-contracts`, retitled **Command Contracts: From Intent to
Executable Work**.

Source chapters:

- `intent-to-execution-contracts`
- `command-contracts-and-semantic-interfaces`

Related chapter not merged by this package:

- `human-intent-as-a-formal-input`

Continuity decision:

- Keep `intent-to-execution-contracts` as the public continuity ID if this
  merge later proceeds, because it already owns the execution handoff from
  accepted human goals into typed work.
- Treat `command-contracts-and-semantic-interfaces` as a folded source chapter
  whose semantic interface rules, command-field discipline, prompt/context
  override boundary, validation states, proof hooks, tests, source mappings,
  and reader path become named sections, subclaims, and history records in the
  destination chapter.
- Keep `human-intent-as-a-formal-input` standalone in Part I. If this merge
  later proceeds, slim that chapter only where it pre-states the Part II
  contract spine. It should remain the intake chapter for raw request capture,
  ambiguity, authority extraction, bounded defaults, re-contract triggers, and
  stop conditions.

## Non-Actions

- No manifest edit has been made.
- No chapter file has been removed or rewritten.
- No source note, external source, proof target, test result, or support state
  has changed.
- No support state changes are made or implied.
- No claim is promoted above `argument`.
- No external comparator is treated as proving ASI Stack parser correctness,
  semantic-interface safety, dispatcher behavior, runtime execution,
  tool-effect enforcement, approval enforcement, or deployment behavior.
- No reader, EPUB, DOCX, PDF, or audio artifact is approved by this package.
- No new result is created by this dry run.

## Proposed `book_structure.json` Diff

This proposed `book_structure.json` diff is illustrative and unapplied. If the
merge is later executed, apply one cluster merge in one commit, then regenerate
and validate every generated surface.

```diff
@@ Part II - Planning, Memory, Reasoning, and Execution
 {
   "id": "intent-to-execution-contracts",
-  "title": "Intent-to-Execution Contracts",
+  "title": "Command Contracts: From Intent to Executable Work",
   "file": "chapters/intent-to-execution-contracts.qmd",
   "status": "conceptual",
   "evidence_level": "argument",
   "claim_label": "Design rationale",
   "source_ids": [
     "viea",
     "talos",
     "software_magic_grimoire",
     "genesiscode",
-    "moecot"
+    "moecot",
+    "cognitive_compilation"
   ],
-  "problem": "Human goals need a typed path into execution that preserves requirements, artifacts, verification, deployment, and feedback.",
-  "insufficient": "A model response is not an execution contract; it lacks lifecycle, acceptance, artifact identity, and side-effect control.",
-  "core_claim": "Governed execution transforms intent into explicit contracts before any tool or runtime action occurs.",
-  "minimal_implementation": "A command-contract schema and one end-to-end intent-to-artifact trace.",
-  "beyond_state_of_art": "The mature version is a contract operating spine for the whole stack..."
+  "problem": "Accepted human intent needs a typed command contract whose semantics, authority, artifacts, verification, failure behavior, and execution receipts remain inspectable from intake through delivery.",
+  "insufficient": "Prompt prose, model responses, and ad hoc task descriptions blur objective, context, constraints, authority, output contract, verification, failure behavior, artifact identity, and side-effect control.",
+  "core_claim": "Governed work should pass through explicit command contracts that bind intent, semantic interface fields, authority, artifacts, verification, failure behavior, execution receipts, and residuals before tools or runtimes act.",
+  "minimal_implementation": "Intent-contract, command-contract, and intent-execution-trace fixtures plus a synthetic plan-execution harness with valid and expected-invalid authority, receipt, mismatch, requirement-loss, and cycle cases.",
+  "beyond_state_of_art": "A mature command-contract spine gives humans, planners, verifiers, job runners, policy layers, and later AI agents a shared semantic control language for executable work, with provenance, field confidence, authority basis, re-contract points, dispatch blockers, receipts, artifacts, feedback, and residuals preserved end to end."
 }
-
-{
-  "id": "command-contracts-and-semantic-interfaces",
-  "title": "Command Contracts and Semantic Interfaces",
-  "file": "chapters/command-contracts-and-semantic-interfaces.qmd",
-  ...
-}
```

Manifest notes:

- The proposed Corben/local `source_ids` union is `viea`, `talos`,
  `software_magic_grimoire`, `genesiscode`, `moecot`, and
  `cognitive_compilation`.
- If the merge proceeds, remove only the
  `command-contracts-and-semantic-interfaces` chapter object after all claim,
  source, proof, reader, handoff, URL, and validation steps pass.
- Do not fold `human-intent-as-a-formal-input` into this destination. Update
  its handoff and trim duplicated contract-spine material only if review
  accepts the merge.
- Run `python3 scripts/chapter_adjacency_report.py --if-removing
  command-contracts-and-semantic-interfaces` before editing the manifest.

## Destination Section Outline

The merged chapter should use one chapter skeleton, not two pasted skeletons.

Recommended section sequence:

1. Chapter status: one status block with merged evidence gaps.
2. Drafting guardrail: a command contract is not parser correctness,
   dispatch enforcement, approval enforcement, or runtime execution evidence.
3. Human Reading Path: start from the reader question, "When does a request
   become executable work?"
4. Problem: accepted intent needs a typed command contract that preserves
   semantics, authority, artifacts, verification, failure behavior, receipts,
   and residuals from intake through delivery.
5. Why existing approaches are insufficient: prompt prose and model responses
   hide objective, context, constraints, authority, output, verification,
   failure behavior, artifact identity, and side-effect control.
6. Core Claim: use the merged core claim above.
7. Claim-source mapping status: one table that separates intent-to-execution
   lineage from semantic-interface lineage and keeps all support at
   `argument`.
8. Mechanism:
   - intake receipt and accepted contract boundary;
   - command-field semantics;
   - field provenance and confidence;
   - authority basis and side-effect envelope;
   - output, verification, and failure behavior;
   - re-contract triggers and dispatch blockers;
   - handoff, dispatch, artifact, feedback, and residual receipts;
   - context/prompt override firewall;
   - no-claim boundaries for parser quality, prompt-injection resistance,
     approval enforcement, and runtime execution.
9. Interfaces:
   - Human Intent intake;
   - Planning control layer;
   - PlanForge/DAG compilation;
   - Cognitive Compilation/S-IR lowering;
   - Labor OS and typed jobs;
   - runtime adapters and tool permissions;
   - artifact graph and evidence ledger.
10. Invariants:
    - contract constraints survive compilation;
    - side effects require explicit execution authority;
    - artifacts remain linked to source intent;
    - output and verification requirements are visible;
    - failure behavior is declared;
    - implicit or hidden instructions cannot override explicit constraints;
    - inferred/defaulted authority cannot authorize side effects.
11. Failure modes:
    - response mistaken for completed work;
    - artifact identity lost;
    - approval bypass;
    - semantic ambiguity;
    - prompt or context override;
    - unspecified output contract;
    - field laundering;
    - authority inference treated as permission.
12. Minimum Viable Implementation: combine `intent_contract`,
    `command_contract`, and `intent_execution_trace` fixtures with
    `python3 scripts/validate_plan_execution_contracts.py`. The MVI should
    preserve the valid dispatchable and blocked-authority cases plus invalid
    dispatch-without-receipt, approval-bypass, requirement-loss, contract
    mismatch, and cycle cases.
13. Beyond the State of the Art: describe a semantic control language and
    contract operating spine for governed work. Preserve the claim boundary
    that this is an architectural endpoint, not a demonstrated deployed
    command dispatcher.
14. Codex test plan: union existing contract field completeness, constraint
    preservation, artifact traceability, command schema validation,
    failure-behavior declaration, prompt override, field-confidence, and
    authority-inference tests.
15. Formalization hooks: keep both Lean modules and all four proof tags.
16. Source crosswalk: union Corben/local sources and external comparators.
17. Summary: one synthesis of accepted intent, semantic command fields,
    authority, dispatch, artifacts, feedback, and residuals.
18. Handoff: route directly to `planning-as-a-control-layer`, while preserving
    the backward handoff from `human-intent-as-a-formal-input`.

## Appendix C Row Plan

Proposed merged core row:

| Row | Chapter | Claim label | Support state | Source effect |
|---|---|---|---|---|
| `intent-to-execution-contracts.core` | `intent-to-execution-contracts` | Design rationale | argument | Union the source mappings from both source chapters; keep limits and passage-review notes. |

Proposed merged core claim:

> Governed work should pass through explicit command contracts that bind
> intent, semantic interface fields, authority, artifacts, verification,
> failure behavior, execution receipts, and residuals before tools or runtimes
> act.

Claim-history treatment for folded and adjacent chapters:

| Existing row | Proposed disposition | Required preservation |
|---|---|---|
| `command-contracts-and-semantic-interfaces.core` | Redirect to destination as a subclaim about semantic fields, context override boundaries, field confidence, failure behavior, dispatch blockers, and validation states. | Preserve claim text in history, proof tags, source mappings, fixture/test rows, and no-promotion limits. |
| `human-intent-as-a-formal-input.core` | No merge in this package. | Keep raw-request intake, ambiguity, authority extraction, bounded defaults, re-contract triggers, and stop-condition preservation as the Part I chapter boundary. |

No support state changes are authorized. All core and subclaim rows remain
`argument` unless a separate evidence-transition record later justifies a
change.

## Source Union

Corben/local source union:

- `viea`
- `talos`
- `software_magic_grimoire`
- `genesiscode`
- `moecot`
- `cognitive_compilation`

External-source union:

- `ext_react_2022`
- `ext_dafny_2010`

Adjacent external comparators that stay with `human-intent-as-a-formal-input`:

- `ext_goal_oriented_requirements_engineering_2001`
- `ext_cooperative_inverse_rl_2016`
- `ext_deep_rl_human_preferences_2017`

These external records remain comparators and positioning sources. They do not
prove ASI Stack parser correctness, semantic-interface extraction, dispatcher
behavior, approval enforcement, runtime execution, or prompt-injection
resistance.

## Lean Module And Proof-Manifest Treatment

Keep these modules:

- `AsiStackProofs.IntentToExecution`
- `AsiStackProofs.CommandContracts`

Keep these proof tags:

- `lean:intent_execution.contracts.operational_invariant`
- `lean:intent_execution.contracts.failure_blocks_promotion`
- `lean:command.semantic_interface.operational_invariant`
- `lean:command.semantic_interface.failure_blocks_promotion`

Do not move or retire the `AsiStackProofs.IntentContracts` module or the
`lean:intent.contract.*` proof tags owned by
`human-intent-as-a-formal-input`. The human-intent chapter stays standalone.

## Tests, Schemas, And Fixtures

Preserve these schema and fixture families:

- `schemas/intent_contract.schema.json`
- `schemas/command_contract.schema.json`
- `schemas/intent_execution_trace.schema.json`
- `experiments/plan_execution_contracts/fixtures/valid_dispatchable_linear_plan.json`
- `experiments/plan_execution_contracts/fixtures/valid_blocked_authority_plan.json`
- `experiments/plan_execution_contracts/fixtures/invalid_dispatch_without_receipt.json`
- `experiments/plan_execution_contracts/fixtures/invalid_approval_bypass.json`
- `experiments/plan_execution_contracts/fixtures/invalid_requirement_lost.json`
- `experiments/plan_execution_contracts/fixtures/invalid_contract_mismatch.json`
- `experiments/plan_execution_contracts/fixtures/invalid_cycle_in_dag.json`

Preserve the implemented validator:

- `python3 scripts/validate_plan_execution_contracts.py`

The harness validates synthetic record consistency only. It does not prove a
parser, planner, runtime dispatcher, tool-effect enforcement layer, or
deployed contract system.

## Reader Path, Handoff, And Review Repairs

Before any manifest edit:

- run `python3 scripts/chapter_adjacency_report.py --if-removing
  command-contracts-and-semantic-interfaces`;
- update Human Reading Path prose so the reader sees one command-contract
  argument rather than repeated contract introductions;
- update Handoff sections for `human-intent-as-a-formal-input`,
  `intent-to-execution-contracts`, and `planning-as-a-control-layer`;
- update reader overlays and curated-reader review matrices so folded command
  interface content remains discoverable;
- update `docs/chapter_external_grounding_status.md` and
  `docs/external_sota_positioning_audit.md` after scaffold generation;
- update Appendix C, Appendix K, proof manifests, repository map, README, and
  changelog;
- record URL, redirect, or historical-note policy for the folded command
  contract chapter file.

The reader benefit must be tested explicitly: the destination chapter should
reduce repeated Problem/Insufficiency/Mechanism sections while adding clearer
contract fields, authority boundaries, negative cases, and external-positioning
context.

## MVI And Beyond-SOTA Merge

Merged minimum viable implementation:

- one intent contract record;
- one command contract record;
- one intent-execution trace record;
- one valid dispatchable trace;
- one blocked-authority trace;
- one invalid missing receipt case;
- one invalid approval-bypass case;
- one invalid requirement-loss or contract-mismatch case.

Merged mature endpoint:

- a command-contract operating spine that gives humans, planners, verifiers,
  job runners, policy layers, and future AI agents one semantic control
  language for executable work, with provenance, confidence, authority,
  receipts, artifacts, feedback, and residuals preserved end to end.

This end state remains speculative architecture until a separate implementation
or evaluation lane produces public evidence.

## URL And Redirect Policy

If the merge is executed, do not silently delete reader-visible history. Choose
one of these before touching the manifest:

- keep the folded `.qmd` file as a historical note excluded from the book order
  but linked from the destination chapter;
- add a public redirect page from `command-contracts-and-semantic-interfaces`
  to the destination chapter;
- keep a release-history note that names the last version where the command
  contracts chapter was standalone.

The chosen policy must be visible in the changelog and release notes.

## Expected Generated File Updates

If the merge is executed later, expect updates to:

- `_quarto.yml`
- `appendices/A_source_matrix.qmd`
- `appendices/C_claim_evidence_matrix.qmd`
- `appendices/K_proof_manifest.qmd`
- `appendices/F_changelog.qmd`
- `proofs/proof_manifest.json`
- `docs/book_outline.md`
- `docs/chapter_external_grounding_status.md`
- `docs/external_sota_positioning_audit.md`
- reader overlay and review records

This dry run does not make those generated updates.

## Validation Commands

Run these before any future merge commit:

```bash
python3 scripts/chapter_adjacency_report.py --if-removing command-contracts-and-semantic-interfaces
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py
python3 scripts/validate_chapter_consolidation_sequence.py
python3 scripts/validate_publication.py
python3 scripts/validate_release_profiles.py
python3 scripts/validate_reader_spine.py --check
python3 scripts/validate_book.py
python3 scripts/validate_visual_coverage.py
python3 scripts/validate_schemas.py
python3 scripts/validate_protocol_examples.py
(cd lean && lake build)
quarto render --to html
node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports
```

## Review Questions

- Does `intent-to-execution-contracts` remain the right continuity ID, or does
  the proposed title require a new slug and redirect policy?
- Does the destination preserve command-field semantics strongly enough after
  folding `command-contracts-and-semantic-interfaces`?
- Does `human-intent-as-a-formal-input` stay clearly focused on intake,
  ambiguity, authority extraction, bounded defaults, re-contract triggers, and
  stop conditions?
- Does the handoff to `planning-as-a-control-layer` remain clear after the
  command-contract source chapter is folded?
- Does the destination reduce repeated skeleton load while increasing mechanism
  depth, negative-case clarity, external positioning, proof routing, and reader
  flow?

## Non-Claims

- This dry run does not merge chapters.
- This dry run does not change `book_structure.json`.
- This dry run does not change Appendix C support states.
- This dry run does not create source-derived, external-literature-backed,
  proof-derived, prototype-backed, synthetic-test-backed, or empirical support.
- This dry run does not prove that a future merged chapter will be better.
- This dry run does not approve reader, ebook, PDF, DOCX, audio, DOI, archive,
  or release artifacts.
- This dry run does not validate any new parser, semantic extractor,
  dispatcher, approval-enforcement layer, prompt-injection defense, runtime
  execution, tool-effect enforcement, or deployment result.
