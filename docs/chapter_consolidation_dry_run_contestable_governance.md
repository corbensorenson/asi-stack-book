# Chapter Consolidation Dry Run: Contestable Governance

Last updated: 2026-06-29

This is the second dry-run merge package required by
`docs/v1_x_beyond_sota_roadmap.md` and
`docs/chapter_consolidation_pilot_plan.md`. It is a review artifact only. It
does not edit `book_structure.json`, delete a chapter, change a URL, rewrite a
chapter, change source mappings, change proof targets, change support states,
or approve a reader artifact.

Dry-run destination: `moral-uncertainty-and-value-conflict`, retitled
**Moral Uncertainty, Value Conflict, and Contestable Governance**.

Source chapters:

- `moral-uncertainty-and-value-conflict`
- `governance-rights-fork-exit-and-audit`

Continuity decision: keep `moral-uncertainty-and-value-conflict` as the public
continuity ID if this merge later proceeds. Treat
`governance-rights-fork-exit-and-audit` as a folded source chapter whose claim,
proof hooks, test rows, reader path, source mappings, and governance interfaces
become named sections, subclaims, and history records in the destination
chapter.

## Non-Actions

- No manifest edit has been made.
- No chapter file has been removed or rewritten.
- No source note, external source, proof target, test result, or support state
  has changed.
- No claim is promoted above `argument`.
- No external comparator is treated as proving moral correctness, legal rights,
  institutional adequacy, or deployed governance.
- No reader, EPUB, DOCX, PDF, or audio artifact is approved by this package.

## Proposed `book_structure.json` Diff

This proposed `book_structure.json` diff is illustrative and unapplied. If the
merge is later executed, apply one pilot merge in one commit, then regenerate
and validate every generated surface.

```diff
@@ Part I - Foundations, Alignment, and Governance
 {
   "id": "moral-uncertainty-and-value-conflict",
-  "title": "Moral Uncertainty and Value Conflict",
+  "title": "Moral Uncertainty, Value Conflict, and Contestable Governance",
   "file": "chapters/moral-uncertainty-and-value-conflict.qmd",
   "status": "conceptual",
   "evidence_level": "argument",
   "claim_label": "Design rationale",
   "source_ids": [
     "ethica_mechanica",
     "alignment_field",
     "coherence_exchange",
     "uat",
     "spinoza",
-    "field_of_god_ai_constitution"
+    "field_of_god_ai_constitution",
+    "ladon_manhattan"
   ],
-  "problem": "A self-improving system will face value conflicts that cannot be honestly collapsed into one scalar objective.",
-  "insufficient": "Single-objective optimization hides moral uncertainty and encourages premature resolution of contested values.",
-  "core_claim": "Value conflicts should be represented as explicit unresolved obligations, review paths, and bounded decisions rather than hidden inside reward functions.",
-  "minimal_implementation": "Begin with a value_conflict_record schema plus a scenario fixture...",
-  "beyond_state_of_art": "Moral uncertainty needs a value-conflict ledger for governed action under disagreement..."
+  "problem": "A self-improving system will face unresolved value conflicts whose affected parties need inspectable, appealable, and portable governance rights rather than hidden reward-weight settlement.",
+  "insufficient": "Single-objective optimization and policy-only transparency both fail when disagreement needs bounded action, dissent preservation, audit, exit, fork, appeal, and safety-limited contestability.",
+  "core_claim": "Value conflicts should be represented as explicit unresolved obligations, residuals, review paths, and bounded decisions, with fork, exit, audit, dissent, and contestability preserved as technical governance interfaces.",
+  "minimal_implementation": "A value-conflict record plus governance-right receipt suite validates residual uncertainty, dissent, bounded decisions, audit material, redaction appeal paths, exit/fork access, and safety obligations.",
+  "beyond_state_of_art": "A mature contestability layer carries unresolved value conflicts into durable rights receipts, appeal surfaces, audit artifacts, safety-limited forks, portable exit paths, and replacement-preserved dissent without claiming moral finality."
 }
-
-{
-  "id": "governance-rights-fork-exit-and-audit",
-  "title": "Governance Rights: Fork, Exit, and Audit",
-  "file": "chapters/governance-rights-fork-exit-and-audit.qmd",
-  ...
-}
```

Manifest notes:

- The proposed Corben/local `source_ids` union is `ethica_mechanica`,
  `alignment_field`, `coherence_exchange`, `uat`, `spinoza`,
  `field_of_god_ai_constitution`, and `ladon_manhattan`.
- If the merge proceeds, remove only the
  `governance-rights-fork-exit-and-audit` chapter object after all claim,
  source, proof, reader, and handoff reconciliation steps pass.
- Run `python3 scripts/chapter_adjacency_report.py --if-removing
  governance-rights-fork-exit-and-audit` before editing the manifest. The
  current report says the destination chapter Handoff must name **Stable
  Capability Fields** after the fold.

## Destination Section Outline

The merged chapter should use one chapter skeleton, not two pasted skeletons.

Recommended section sequence:

1. Chapter status: one status block with merged open evidence gaps.
2. Drafting guardrail: contestable governance is a record and rights-interface
   design, not a solved moral theory, legal guarantee, or deployed institution.
3. Human Reading Path: begin with the reader problem of acting under unresolved
   disagreement while preserving audit, appeal, exit, fork, and dissent.
4. Problem: a self-improving system needs bounded action under value conflict
   and material contestability for affected parties.
5. Why existing approaches are insufficient: reward-only moral uncertainty
   flattens disagreement, while policy-only transparency lacks usable rights
   receipts, access paths, redaction reasons, and appeal routes.
6. Core Claim: use the merged core claim below.
7. Claim-source mapping status: one table that separates moral-conflict
   lineage, governance-rights lineage, security-boundary lineage, and
   connector-only synthesis while keeping all support at `argument`.
8. Mechanism:
   - value conflict record;
   - bounded decision as lease rather than settlement;
   - residual uncertainty and dissent payload preservation;
   - review escalation, deprecated premise, and revisit path states;
   - governance right record and rights receipt;
   - audit, exit, fork, redaction, appeal, and contestability interfaces;
   - safety-obligation preservation for constrained forks;
   - replacement-preserved rights and non-claims about moral correctness,
     legal rights, institutional adequacy, deployed policy, and reviewer
     quality.
9. Interfaces:
   - Value Conflict Record;
   - Governance Right Record;
   - rights receipt;
   - appeal/redaction receipt;
   - plan, runtime, memory, SCF, evidence, and self-improvement handoffs.
10. Invariants:
    - unresolved conflicts remain visible;
    - high-stakes unresolved conflict requires review and residual uncertainty;
    - bounded decisions preserve dissent;
    - unresolved conflict narrows authority;
    - audit records cannot be silently deleted;
    - exit remains materially usable;
    - forks preserve safety obligations.
11. Failure modes:
    - value flattening;
    - false consensus;
    - conflict laundering;
    - dissent deletion;
    - rights theater;
    - governance capture;
    - data hostage-taking;
    - unsafe fork bypass;
    - redaction without appeal;
    - appeal controlled only by the challenged authority.
12. Minimum Viable Implementation: combine `value_conflict_record` and
    `governance_right_record` fixture suites. The MVI should include one
    high-stakes unresolved conflict blocked for missing residual uncertainty,
    one bounded decision that must preserve dissent, one authority-narrowing
    case, one audit response, one redaction with appeal path, one exit export,
    and one fork denial that preserves safety obligations.
13. Beyond the State of the Art: describe contestability infrastructure that
    carries unresolved moral residuals into durable rights receipts, appeal
    surfaces, safety-limited forks, portable exits, audit artifacts,
    replacement-preserved rights, and self-improvement gates.
14. Codex test plan: union the existing value-conflict and governance-rights
    tests without claiming broader evidence.
15. Formalization hooks: keep both Lean modules and all four proof tags.
16. Source crosswalk: union Corben/local sources and external comparators.
17. Summary: one synthesis of moral residual preservation and contestable
    governance interfaces.
18. Handoff: route directly to `stable-capability-fields`.

## Appendix C Row Plan

Proposed merged core row:

| Row | Chapter | Claim label | Support state | Source effect |
|---|---|---|---|---|
| `moral-uncertainty-and-value-conflict.core` | `moral-uncertainty-and-value-conflict` | Design rationale | argument | Union the source mappings from both source chapters; keep limits and passage-review notes. |

Proposed merged core claim:

> Value conflicts should be represented as explicit unresolved obligations,
> residuals, review paths, and bounded decisions, with fork, exit, audit,
> dissent, and contestability preserved as technical governance interfaces.

Claim-history treatment for the folded source chapter:

| Existing row | Treatment if merge proceeds | Boundary |
|---|---|---|
| `moral-uncertainty-and-value-conflict.core` | Retain as the destination core row with merged text. | Support remains `argument`. |
| `governance-rights-fork-exit-and-audit.core` | Redirect to destination as a preserved subclaim and section family: fork, exit, audit, dissent, redaction, appeal, contestability, durable record paths, and safety-limited fork obligations. | Do not silently delete; record the fold in changelog and any claim-decision/history surface required by validators. |

No-support-state-change language:

- The merged chapter remains `Design rationale` + `argument`.
- Existing synthetic harnesses and Lean records are bounded finite-record
  evidence only.
- Moral-uncertainty, contestable-AI, corrigibility, off-switch, and collective
  constitutional-AI sources are comparators and prior art, not reproduction
  evidence, moral-correctness proof, legal proof, or support-state promotion.

## Source Union

Corben/local source union:

- `ethica_mechanica`
- `alignment_field`
- `coherence_exchange`
- `uat`
- `spinoza`
- `field_of_god_ai_constitution`
- `ladon_manhattan`

Current source-note state to preserve:

- `ethica_mechanica`, `alignment_field`, `uat`, `spinoza`,
  `field_of_god_ai_constitution`, and `ladon_manhattan` carry reviewed passage
  references for one or both source chapters where applicable.
- `coherence_exchange` remains connector-only/source-note mapped.

External-source union:

- `ext_reinforcement_learning_moral_uncertainty_2020`
- `ext_contestable_ai_design_2022`
- `ext_collective_constitutional_ai_2024`
- `ext_corrigibility_2015`
- `ext_off_switch_game_2016`

If the merge proceeds:

- preserve all five external records in Appendix H through
  `sources/source_inventory.json` and their source notes;
- update chapter targets and source-note supported-chapter lists only through
  the normal inventory/source-note workflow;
- keep `docs/chapter_external_grounding_status.md` and
  `docs/external_sota_positioning_audit.md` generated and validated;
- continue mining for fair social-choice, deliberative-review, legal-process,
  data-portability, auditability, and contestable-governance baselines before
  any claim split, support-state movement, or preprint positioning;
- do not cite any new external source in prose until its source note exists.

## Lean Module And Proof-Manifest Treatment

Keep both Lean modules:

- `AsiStackProofs.ValueConflict`
- `AsiStackProofs.GovernanceRights`

Keep all four proof tags:

- `lean:values.conflict.operational_invariant`
- `lean:values.conflict.failure_blocks_promotion`
- `lean:governance.rights.operational_invariant`
- `lean:governance.rights.failure_blocks_promotion`

Proof-manifest rule:

- If the source chapter is removed from `book_structure.json`, move the
  governance-rights proof targets into the destination chapter's outline table
  before running `python3 scripts/sync_proof_manifest.py`.
- Do not retire `AsiStackProofs.GovernanceRights` merely because the chapter
  skeleton is folded. The module owns a distinct fork/exit/audit rights record
  family.
- Keep limitation prose explicit: these proofs express finite-record gates and
  small derived review-route, residual, redaction, and fork-safety theorems.
  They do not prove moral correctness, automatic value classification,
  reviewer quality, legal rights, real access-path availability, actual fork
  safety, institutional contestability, redaction quality, real export
  usability, SCF replacement behavior, or deployed rights enforcement.

## Test, Schema, And Harness Rows To Move

Preserve the value-conflict harness lane:

- `docs/value_conflict_harness.md`
- `scripts/validate_value_conflicts.py`
- `experiments/value_conflicts/results/2026-06-28-local.md`
- existing `value_conflict_record` fixtures and schema/example validation

Preserve the governance-rights harness lane:

- `docs/governance_rights_harness.md`
- `scripts/validate_governance_rights.py`
- `experiments/governance_rights/results/2026-06-28-local.md`
- existing `governance_right_record` fixtures and schema/example validation

No new result is created by this dry run. If the manifest merge proceeds, the
destination chapter's test plan should report both harness families with their
existing non-claims, and generated Appendix E should retain both test families.

## Reader Path, Handoff, And Review Repairs

Human Reading Path repair:

- Replace the current two separate Human Reading Paths with one reader route
  that begins at unresolved moral disagreement and immediately explains why
  audit, appeal, exit, fork, redaction reasons, and dissent preservation are
  the operational handles that keep disagreement governable.
- Do not keep two separate reader openings that repeat the same live scaffold.

Handoff repair:

- `chapters/agency-dignity-and-corrigibility.qmd` should hand off to **Moral
  Uncertainty, Value Conflict, and Contestable Governance**.
- The merged destination chapter should hand off to **Stable Capability
  Fields**.
- The current `python3 scripts/chapter_adjacency_report.py --if-removing
  governance-rights-fork-exit-and-audit` output confirms this repair path.

Reader-overlay and reader-review treatment:

- No current reader overlay operation targets either source chapter.
- `docs/reader_chapter_review_matrix.md` currently lists both chapters as
  reviewed; a manifest merge would require regenerating or revising the review
  matrix so the folded chapter does not appear as a rendered current chapter.
- Any curated reader graduation should wait until this merge decision is
  executed or explicitly deferred, because polishing two repeated governance
  skeletons would preserve the duplication this dry run is meant to remove.

## MVI And Beyond-SOTA Merge

Merged Minimum Viable Implementation:

> A value-conflict record plus a governance-right receipt suite. The MVI
> validates `value_conflict_record` and `governance_right_record` fixtures,
> including residual uncertainty, dissent payloads, authority narrowing, review
> routes, audit artifacts, redaction reasons, appeal paths, exit/export
> material, fork safety obligations, durable receipts, and non-claims. It
> starts the idea honestly without claiming moral correctness, legal rights,
> institutional adequacy, deployed policy behavior, real export usability, or
> runtime governance enforcement.

Merged Beyond-SOTA endpoint:

> Contestability infrastructure carries unresolved moral residuals into durable
> governance rights. A mature layer binds value-conflict records to rights
> receipts, appeal surfaces, audit artifacts, safety-limited fork boundaries,
> portable exit paths, dissent payloads, and replacement-preserved obligations.
> Downstream planning, runtime, memory, SCF, evidence, and self-improvement
> gates can then see why an action was bounded, who could contest it, what was
> withheld, where appeal exists, and which residual obligations survive. This
> remains a target architecture until public-safe traces, stronger proofs,
> review evidence, and runtime artifacts justify narrower support-state
> transitions.

## URL, Redirect, And Retired-File Policy

Default policy for this pilot:

- Keep `chapters/moral-uncertainty-and-value-conflict.qmd` as the rendered URL.
- If the merge proceeds, remove `governance-rights-fork-exit-and-audit` from
  `book_structure.json` only after a redirect or historical-note policy is
  chosen.
- Do not preserve a stale rendered page for the retired chapter unless the
  project adds a deliberate redirect mechanism.
- Keep git history as the archive for the retired chapter file; do not delete
  source history or proof/history records.

## Expected Generated-File Updates If Applied

If this dry run becomes an actual manifest merge, expect updates to:

- `_quarto.yml` through `python3 scripts/sync_scaffold.py`;
- `docs/book_outline.md`;
- `proofs/proof_manifest.json`;
- `appendices/C_claim_evidence_matrix.qmd`;
- `appendices/E_codex_test_specs.qmd`;
- `appendices/F_changelog.qmd`;
- `appendices/K_implementation_horizons.qmd`;
- `docs/chapter_external_grounding_status.md`;
- `docs/external_sota_positioning_audit.md`;
- `docs/reader_chapter_review_matrix.md`;
- any reader-manuscript or overlay manifests that list current chapter IDs.

## Validation Commands Before Any Real Merge Commit

Run at minimum:

```bash
python3 scripts/chapter_adjacency_report.py --if-removing governance-rights-fork-exit-and-audit
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py
python3 scripts/validate_chapter_consolidation_pilot_plan.py
python3 scripts/validate_chapter_handoffs.py
python3 scripts/validate_outline_consistency.py
python3 scripts/validate_implementation_horizons.py
python3 scripts/validate_reader_spine.py --check
python3 scripts/validate_reader_overlays.py --check
python3 scripts/validate_reader_manuscript_manifest.py
python3 scripts/validate_chapter_external_grounding_status.py
python3 scripts/validate_external_sota_positioning.py --release
python3 scripts/validate_book.py
(cd lean && lake build)
quarto render --to html
node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports
```

## Open Review Questions

- Should the merged title use **Contestable Governance**, or should it keep
  the shorter moral-uncertainty title while governance rights become a major
  mechanism section?
- Should `governance-rights-fork-exit-and-audit.qmd` remain in the repository
  as an unrendered historical file after manifest removal, or should a redirect
  mechanism be added first?
- Should `ext_collective_constitutional_ai_2024`, `ext_corrigibility_2015`,
  and `ext_off_switch_game_2016` become direct manifest `source_ids` for the
  destination chapter, or remain external grounding records attached through
  inventory/source-note status?
- Should a future proof-depth pass create a shared contestability record that
  composes `AsiStackProofs.ValueConflict` and
  `AsiStackProofs.GovernanceRights`, or should the modules stay separate but
  referenced by one chapter?
